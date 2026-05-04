# Bridge Room T2 — Rollback Safety Design

**TYPE:** Design document — T1 only  
**STATUS:** DRAFT  
**APPROVAL TIER:** T1  
**LAYER:** 1  
**CREATED:** 2026-05-04  
**COVERS BLOCKERS:** #6 from bridge-room-runtime-readiness.md Section 13  
**READY FOR T2 DESIGN REVIEW:** YES  
**READY FOR RUNTIME INTEGRATION:** NO

> **CRITICAL:** This document describes a future design only.  
> No change to bridge.py, conductor.py, bridge/**, scripts/**, or any runtime file is authorized at T1.  
> Every action described here requires a separate T2 approval before execution.

---

## 1. SYSTEM STATE

| Item | Status |
|------|--------|
| Bridge Room prototypes #1–#8 | ALL PASS (sandbox only) |
| File-based rollback | PROVEN (P6, P7, P8) — snapshot + overwrite pattern |
| PRE_FIX_SNAPSHOT before FIX | PROVEN (P7, P8) — snapshot written before any FIX write |
| Selective per-target rollback | PROVEN (P7) — TGT-P7-02 rolled back; TGT-P7-01, TGT-P7-03 untouched |
| Cross-pack snapshot lineage isolation | PROVEN (P8) — SNAP-P8-01 distinct from SNAP-P7-xx |
| Rollback for non-file targets (Shopify) | NOT DESIGNED — T3 scope |
| Atomic rollback in runtime | NOT DESIGNED until this document |
| Persistent snapshot storage | NOT DESIGNED until this document |
| Cross-session rollback | NOT DESIGNED until this document |
| Rollback authorization model | PARTIALLY PROVEN (Codex verdict triggers) — formalized here |
| T2 approval | NOT GRANTED |
| Runtime integration | BLOCKED |

---

## 2. Why This Document Is Required

`bridge-room-runtime-readiness.md` (Section 13, Blocker #6):
> "Rollback safety for non-file targets not designed — Required deliverable: T2 design doc: rollback safety extension"

Section 10 of that document lists runtime rollback gaps beyond sandbox proof:

| Requirement | Gap |
|------------|-----|
| Atomic rollback | Sandbox: file overwrite. Runtime: must use temp file + rename for atomicity |
| Rollback verification | Sandbox: RETEST stage. Runtime: verification must survive bridge.py restart |
| Partial rollback | Proven P7 for sandbox. Runtime: same pattern but state must persist across sessions |
| Snapshot storage | Sandbox: .bak files in inbox/snapshots/. Runtime: must persist across sessions and bridge restarts |
| Rollback authorization | Sandbox: auto-triggered by Codex ERROR verdict. Runtime: same model, formalized |

Additionally, this document explicitly documents the rollback boundary for Shopify and non-file targets as **out of scope for T2**, preventing scope creep during T2 implementation.

---

## 3. Current Sandbox Proof Relevant to Rollback

### 3a. PRE_FIX_SNAPSHOT Pattern (Proven P7)

```
Stage: FIX (STAGE-02 in P7)
Pre-step: Write snapshot before ANY FIX write
  SNAP-P7-01 → inbox/snapshots/pre-fix-target-p7-01.md.bak
  SNAP-P7-02 → inbox/snapshots/pre-fix-target-p7-02.md.bak
FIX writes:
  TGT-P7-01: PASS (review_status written correctly)
  TGT-P7-02: ERROR (null written instead of "approved")
Rollback triggered:
  Read SNAP-P7-02 → overwrite mock-target-p7-02.md
  Verify: matches_snapshot = true, null_value_not_present = true
  ROLLBACK_PASS
```

### 3b. What Was Proven

- Snapshot must be written BEFORE any FIX write — `written_before_fix: true` verified in verdict
- Snapshot ID (SNAP-Pn-NN) is unique per pack per target
- Rollback only affects the errored target — FIXED targets are untouched
- ROLLBACK is a separate named stage (CMD-P7-RB) dispatched after ERROR verdict
- ROLLBACK_PASS verdict issued by Codex after verifying rollback correctness
- P7 snapshots remain frozen in P8 — not used as P8 rollback source

### 3c. What Was NOT Proven in Sandbox

- Multi-session snapshot persistence (all sandboxes ran in one session)
- Atomic write (sandbox overwrote file directly — no temp/rename)
- Rollback of partially-written multi-field targets (P7 ERROR was single-field write)
- Rollback when conductor.py crashes mid-ROLLBACK
- Any rollback of Shopify, DB, or non-file targets

---

## 4. File-Based Rollback Runtime Design

### 4a. Snapshot Write Contract (Design Only)

The PRE_FIX_SNAPSHOT step is mandatory before any FIX stage write. This rule is unchanged from sandbox.

**Runtime addition:** conductor.py must **confirm** the snapshot exists before dispatching the FIX stage command.

```
Snapshot confirmation flow:
  1. FIX stage command includes PRE_FIX_SNAPSHOT pre-step
  2. Claude writes snapshot to inbox/snapshots/ in the BRIDGE_ROOM_OUTPUT_START block
  3. Claude confirms: snapshot_id = SNAP-<pack_id>-NN, snapshot_confirmed = true
  4. conductor.py ingests output, checks snapshot_confirmed = true in output JSON
  5. If snapshot_confirmed = false OR snapshot file not present on disk:
       → SNAPSHOT_WRITE_FAILURE
       → conductor.py does NOT issue verdict-ready signal for FIX
       → Stage status = ERROR before FIX writes were attempted
       → No rollback needed (FIX did not write)
  6. Only when snapshot_confirmed = true:
       → conductor.py signals Codex that output is ready for verdict
```

**Key invariant:** The FIX stage output JSON carries `snapshot_confirmed` as a boolean. If Claude reports PASS on FIX but `snapshot_confirmed = false`, conductor.py treats this as ERROR (snapshot integrity violation).

### 4b. Atomic Write Contract (Design Only)

In sandbox: rollback overwrote the target file directly. In runtime, direct overwrite risks partial writes if the process is interrupted.

**Design rule:** All FIX writes and ROLLBACK writes must use a temp-file-then-rename pattern:

```
Write target:
  1. Write new content to: <target_file>.tmp
  2. Verify tmp file written correctly (size check, basic validation)
  3. Rename .tmp to final filename (atomic on most filesystems)
  4. If rename fails → leave .tmp in place, report write error → rollback evaluation

Rollback write:
  1. Write snapshot content to: <target_file>.rollback.tmp
  2. Verify tmp file written
  3. Rename .rollback.tmp to final filename (atomic)
  4. If rename fails → CRITICAL: both original and rollback write failed → HALT, human review
```

**Note:** File rename atomicity is guaranteed on most POSIX filesystems and NTFS. This project runs on Windows (NTFS) — rename behavior must be verified in T2 testing.

### 4c. Snapshot Storage Contract (Design Only)

**Problem:** Sandbox stores snapshots in `inbox/snapshots/` inside the prototype directory. In runtime, if the project is re-cloned or conductor.py crashes and restarts, snapshots must still be accessible.

**Design rule:** Snapshot files are persistent artifacts, not ephemeral. They must:
1. Remain in place until the pack they belong to reaches PACK_COMPLETE or PACK_FAILED with confirmed rollback
2. Never be deleted automatically by conductor.py
3. Be indexed in the pack registry (snapshot_id → file path mapping)

**Storage location (design only):**

```
docs/management/bridge-room-prototype/inbox/snapshots/
  pre-fix-<target_id>-<pack_descriptor>.md.bak

Example:
  pre-fix-TGT-P9-01-EXEC-PACK-P9-001.md.bak
```

**Pack-qualified filename:** The target_id + pack_descriptor combination ensures no two packs create colliding snapshot names (proven design principle from P8).

**Runtime registry entry:**

```json
{
  "snapshot_id": "SNAP-EXEC-PACK-P9-001-01",
  "pack_id": "EXEC-PACK-P9-001",
  "target_id": "TGT-P9-01",
  "file": "docs/management/bridge-room-prototype/inbox/snapshots/pre-fix-TGT-P9-01-EXEC-PACK-P9-001.md.bak",
  "written_at": "<ISO timestamp>",
  "confirmed": true,
  "used_for_rollback": false
}
```

conductor.py maintains a `snapshots` section in the session registry, updated immediately when snapshot_confirmed = true is received in stage output.

---

## 5. Partial Rollback Design

### 5a. What Partial Rollback Means

In P7: 3 targets. TGT-P7-01 FIXED (keep changes). TGT-P7-02 ERROR (roll back). TGT-P7-03 UNCHANGED (do nothing).

This is **selective rollback** — only the errored target is restored. Fixed targets retain their new state.

### 5b. Partial Rollback Rules (Runtime)

**Rule 1 — Rollback scope is per-target, not per-pack:**  
An ERROR on TGT-P9-02 does NOT roll back TGT-P9-01 (already FIXED and confirmed).

**Rule 2 — Rollback targets are specified in the Codex ERROR verdict:**

```json
{
  "verdict": "ROLLBACK_REQUIRED",
  "rollback_required": true,
  "rollback_targets": ["TGT-P9-02"],
  "keep_targets": ["TGT-P9-01"]
}
```

conductor.py reads `rollback_targets` and issues ROLLBACK stage command for those targets only.

**Rule 3 — ROLLBACK stage command includes explicit target list:**  
The ROLLBACK command JSON specifies exactly which targets to restore and which snapshot to use for each.

**Rule 4 — FIXED targets are verified in RETEST regardless:**  
After ROLLBACK_PASS, RETEST must verify ALL targets in scope — both the rolled-back target AND the fixed targets. This is the cross-target consistency check proven in P7.

**Rule 5 — Partial pack result (PACK_PASS_PARTIAL):**  
If FIX fixes some targets and ERROR+ROLLBACK occurs on others, the pack result is PACK_PASS_PARTIAL, not PACK_COMPLETE. This is proven in P7 and recorded in the pack registry.

### 5c. Partial Rollback State Machine

```
FIX stage:
  TGT-A: PASS → snapshot_a retained, change confirmed
  TGT-B: ERROR → rollback_required = true, rollback_targets = [TGT-B]

ROLLBACK stage:
  Scope: TGT-B only
  Read SNAP-<pack_id>-B → write to TGT-B file (atomic rename)
  Verify: matches_snapshot = true

RETEST stage:
  Scope: TGT-A (verify fix retained), TGT-B (verify rollback), TGT-C (verify unchanged)
  All 3 verified → PACK_PASS_PARTIAL

Pack registry:
  targets_fixed: [TGT-A]
  targets_rolled_back: [TGT-B]
  targets_unchanged: [TGT-C]
  open_issues: [ISS for TGT-B — original issue not resolved]
```

---

## 6. Cross-Session Rollback Design

### 6a. Problem

In sandbox, all phases (FIX, ROLLBACK) run within the same session. In runtime:
- conductor.py may crash between the FIX write and the ROLLBACK write
- The project may be restarted between sessions
- Snapshots written in session N must still be usable in session N+1

### 6b. Cross-Session Recovery Design (Design Only)

**On conductor.py restart:**

```
1. Read room-state.json: check pack_status
   If pack_status = RUNNING and stage_status = ERROR → rollback evaluation pending
   If pack_status = RUNNING and stage_status = AWAITING_VERDICT → re-signal Codex (idempotent)

2. Check session-registry.json for active session
   If session found with RUNNING status → resume from conductor-state.md

3. Read conductor-state.md: identify last confirmed step
   If last step = SNAPSHOT_CONFIRMED and current stage = FIX → FIX may have been partially written
   → Evaluate rollback_required based on snapshot presence + target file modification timestamp

4. If rollback required and snapshot exists → issue ROLLBACK stage (same as normal path)
5. If rollback required and snapshot MISSING → CRITICAL_ROLLBACK_FAILURE → HALT, log, alert
```

**Key guarantee:** If `snapshot_confirmed = true` was recorded in conductor-state.md before conductor crashed, a cross-session rollback is possible. If snapshot was not confirmed → no rollback option → CRITICAL_ROLLBACK_FAILURE state.

### 6c. conductor-state.md Checkpointing

conductor.py must persist its state after each critical step. Minimum checkpoints:

| Step | What conductor.py Writes to conductor-state.md |
|------|------------------------------------------------|
| Snapshot confirmed | `snapshot_confirmed: true, snapshot_id: SNAP-xxx, snapshot_path: ...` |
| FIX write complete | `fix_writes_confirmed: true, targets_written: [...]` |
| ROLLBACK stage dispatched | `rollback_dispatched: true, rollback_targets: [...]` |
| ROLLBACK verified | `rollback_verified: true, rollback_pass: true` |

---

## 7. Rollback Authorization Model

### 7a. Who Authorizes Rollback

**Codex authorizes rollback** via the ERROR verdict. The verdict must contain `rollback_required: true`.

conductor.py does NOT decide independently whether to roll back. It only acts on an explicit Codex verdict.

### 7b. Auto-Rollback (Design Only — Requires T2 Approval)

One exception: if conductor.py detects a **system-level failure** (bridge.py crash during FIX, not a Claude decision), it may initiate a system-generated rollback evaluation:

```
Bridge failure during FIX:
  conductor.py checks: snapshot_confirmed = true?
  If YES: conductor.py writes provisional ERROR to room-state.json
          conductor.py signals Codex (requires Codex verdict before ROLLBACK is dispatched)
  If NO:  conductor.py writes CRITICAL (no snapshot) — no rollback possible
          HALT
```

Even in this path, Codex must issue the final verdict that includes `rollback_required: true` before ROLLBACK stage is dispatched. **There is no autonomous rollback.**

### 7c. Rollback Authorization for Partial Rollback

When a multi-target FIX has mixed results, Codex specifies exactly which targets to roll back in the verdict:

```json
{
  "rollback_required": true,
  "rollback_targets": ["TGT-P9-02"],
  "keep_targets": ["TGT-P9-01"],
  "rollback_reason": "TGT-P9-02 FIX wrote null value (TYPE_ERROR)"
}
```

conductor.py validates this list against `targets[]` in the pack YAML before issuing ROLLBACK command.

---

## 8. Shopify Rollback — Out of Scope for T2

### 8a. Gap Identification

bridge-room-runtime-readiness.md Section 10:
> "In runtime with Shopify writes or DB changes, atomicity must be designed."

**This is explicitly out of scope for T2.** The following Shopify rollback concerns are documented here for future T3 design but are NOT designed in this document:

| Concern | Why Out of Scope for T2 |
|---------|------------------------|
| Shopify PUT metafield rollback | T3 required for Shopify writes; no Shopify write occurs in T2 |
| Shopify article body_html rollback | T3 scope |
| Multi-field Shopify rollback atomicity | Not designed — Shopify API does not support transactions |
| Shopify API partial write recovery | Not designed — no Shopify target files in T2 packs |

### 8b. T3 Rollback Requirements (Future — Not Designed Here)

For future T3 design documentation, the following gaps must be addressed before any Shopify rollback is possible:
1. Shopify state snapshot before PUT: What fields, how captured (GET before PUT), where stored
2. Shopify rollback write: PUT with pre-write state values — must be idempotent
3. Shopify rollback verification: GET after rollback PUT to confirm fields match snapshot
4. Partial Shopify rollback: If 3 metafields are written and 2 succeed, 1 fails — can we undo only the 2 that succeeded?
5. Shopify API rate limits during rollback: Rollback write may itself fail if rate-limited

**T3 rule:** No Execution Pack may target Shopify writes until a separate T3 Shopify rollback safety document is written and approved.

---

## 9. Rollback Verification Contract

### 9a. Who Verifies Rollback

RETEST stage verifies rollback success. This is the same RETEST stage that verifies FIX success — it covers all targets regardless of their FIX/ROLLBACK outcome.

### 9b. Rollback Verification Checks

RETEST must verify for rolled-back targets:

```json
{
  "target_id": "TGT-P9-02",
  "rollback_verification": {
    "file_read": true,
    "matches_snapshot": true,
    "snapshot_id": "SNAP-EXEC-PACK-P9-001-02",
    "fix_artifact_not_present": true,
    "pre_fix_state_confirmed": true
  }
}
```

If `matches_snapshot = false` → RETEST FAIL → pack FAIL → CRITICAL_ROLLBACK_VERIFICATION_FAILURE.

### 9c. Snapshot Retention After Verified Rollback

After RETEST confirms rollback:
- Snapshot file remains in place (NOT deleted) until pack is formally CLOSED
- Pack registry records `used_for_rollback: true`
- Snapshot provides audit trail: what state was the file in before the failed FIX

---

## 10. Interfaces

| Interface | From | To | Contract |
|-----------|------|----|---------|
| Snapshot write confirmation | Claude stdout | inbox/ output JSON | `snapshot_confirmed: true` in BRIDGE_ROOM_OUTPUT_START block |
| Rollback authorization | Codex verdict | verdicts/ | `rollback_required: true`, `rollback_targets: [...]` |
| Rollback stage dispatch | conductor.py | outbox/ | Same command format as FIX stage |
| Atomic write confirmation | Claude stdout | inbox/ rollback output | `rollback_write_method: temp_rename`, `rename_success: true` |
| Rollback verification | Claude stdout (RETEST) | inbox/ retest output | `matches_snapshot: true` per rolled-back target |
| Snapshot registry | conductor.py | session-registry.json | Snapshot section with path, confirmed status |

---

## 11. Risks

| Risk | Severity | Description | Mitigation |
|------|----------|-------------|-----------|
| FIX writes without snapshot confirmation | CRITICAL | Snapshot not confirmed before FIX writes — rollback impossible if ERROR | conductor.py MUST check snapshot_confirmed before signaling Codex; FIX verdict blocked if snapshot_confirmed = false |
| Atomic rename fails on Windows NTFS | HIGH | Rollback leaves partial state in .rollback.tmp — target unrecoverable | Verify rename atomicity in T2 test environment before production use |
| Snapshot file deleted before rollback | CRITICAL | .bak file removed accidentally — no rollback path | Snapshots must not be auto-deleted; pack must be CLOSED before any snapshot cleanup |
| Cross-pack snapshot collision | HIGH | Two packs produce same snapshot filename — SNAP-TGT-01 used by wrong pack | Pack-qualified snapshot naming (Section 4c) prevents this if enforced |
| conductor.py crash before checkpoint | HIGH | Crash between FIX write and snapshot_confirmed checkpoint — rollback state unknown | Checkpointing at snapshot_confirmed step (Section 6c) must happen before FIX is dispatched |
| Partial file write (non-atomic) | HIGH | FIX writes 50% of target before crash — file in corrupted state | Temp-file-then-rename pattern (Section 4b) prevents partial state |
| Rollback targets not matching pack YAML | MEDIUM | Codex verdict names TGT not in pack definition | conductor.py validates rollback_targets against pack YAML targets[] before dispatch |
| Shopify rollback attempted at T2 | CRITICAL | T2 pack mistakenly targets Shopify write — no rollback designed | Explicit rule: T2 packs may NOT include Shopify targets (Section 8) |

---

## 12. Safety Rules

1. **No FIX stage proceeds without snapshot_confirmed = true in the preceding step output**
2. **No autonomous rollback** — Codex must issue the ROLLBACK_REQUIRED verdict before any rollback is dispatched
3. **Rollback scope is per-target** — ERROR on TGT-B never touches TGT-A
4. **Snapshots are permanent artifacts** — never auto-deleted by conductor.py
5. **Shopify targets are T3 scope** — no T2 pack may include Shopify write targets
6. **Atomic writes are mandatory** — temp-file + rename pattern is required in T2 implementation
7. **RETEST is mandatory after every rollback** — PACK_COMPLETE is not reachable without RETEST confirming rollback state

---

## 13. What Must NOT Be Connected Yet

| Component | Why Forbidden | Required Before Connecting |
|-----------|--------------|---------------------------|
| FIX writes targeting real project files | T2 approval required | T2 approval + runtime contract confirmed |
| Shopify write targets in any pack | T3 required | T3 Shopify rollback safety document |
| Auto-rollback without Codex verdict | Not designed | Must never be implemented |
| Snapshot deletion after rollback | Out of scope | Explicit retention policy decision required |
| Cross-session snapshot reuse beyond pack boundary | Not designed | Future design required |

---

## 14. T2 Approval Requirements

| # | Requirement | Status |
|---|-------------|--------|
| 1 | This document reviewed and accepted by project owner | NOT DONE |
| 2 | Atomic write (temp + rename) behavior confirmed on NTFS in test environment | NOT DONE |
| 3 | Snapshot retention policy agreed (when, if ever, snapshots are cleaned up) | NOT DONE |
| 4 | T2 approval for conductor.py rollback orchestration (ROLLBACK stage dispatch) | NOT GRANTED |
| 5 | T2 approval for snapshot storage location (inbox/snapshots/ as persistent directory) | NOT GRANTED |
| 6 | Cross-session recovery design reviewed and agreed | NOT DONE |
| 7 | Pack-qualified snapshot naming convention confirmed as unique | NOT DONE |
| 8 | Rollback verification (RETEST) after rollback explicitly approved | NOT DONE |

---

## 15. READY FOR T2 DESIGN REVIEW: YES

This document addresses Blocker #6 and covers file-based rollback safety for T2 scope. Shopify rollback is explicitly documented as T3 scope.

---

## 16. READY FOR RUNTIME INTEGRATION: NO

This document is design only. No rollback mechanism is implemented. No snapshots are written to any location outside the sandbox prototype directory.

---

*Prereq reading: [bridge-room-runtime-readiness.md](bridge-room-runtime-readiness.md)*  
*Sandbox proof: [bridge-room-prototype/PROTOTYPE-CLOSURE.md](bridge-room-prototype/PROTOTYPE-CLOSURE.md)*  
*Companion: [bridge-room-t2-conductor-integration.md](bridge-room-t2-conductor-integration.md) Section 8e (ERROR routing)*
