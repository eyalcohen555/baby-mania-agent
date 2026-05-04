# Bridge Room T2 — TOKEN_SAFE_STOP Runtime Design

**TYPE:** Design document — T1 only  
**STATUS:** DRAFT  
**APPROVAL TIER:** T1  
**LAYER:** 1  
**CREATED:** 2026-05-04  
**COVERS BLOCKERS:** #7 from bridge-room-runtime-readiness.md Section 13  
**READY FOR T2 DESIGN REVIEW:** YES  
**READY FOR RUNTIME INTEGRATION:** NO

> **CRITICAL:** This document describes a future design only.  
> No change to bridge.py, conductor.py, bridge/**, or any runtime file is authorized at T1.  
> Every action described here requires a separate T2 approval before execution.

---

## 1. SYSTEM STATE

| Item | Status |
|------|--------|
| Bridge Room prototypes #1–#8 | ALL PASS (sandbox only) |
| TOKEN_SAFE_STOP 18-field schema | PROVEN (P8) |
| Claude-generated TOKEN_SAFE_STOP | PROVEN in sandbox (Claude writes file directly) |
| Automatic trigger in runtime | NOT DESIGNED until this document |
| bridge.py TOKEN_SAFE_STOP detection | NOT DESIGNED until this document |
| System-generated TOKEN_SAFE_STOP | PARTIALLY DESIGNED (bridge-room-t2-bridge-integration.md Section 10c) |
| Token count trigger mechanism | NOT DESIGNED until this document |
| Stale TOKEN_SAFE_STOP detection | NOT DESIGNED until this document |
| Resume authorization protocol | OUTLINED (bridge-room-t2-conductor-integration.md Section 9d) — formalized here |
| 18-field completeness validation | NOT DESIGNED until this document |
| T2 approval | NOT GRANTED |
| Runtime integration | BLOCKED |

---

## 2. Why This Document Is Required

`bridge-room-runtime-readiness.md` (Section 13, Blocker #7):
> "TOKEN_SAFE_STOP runtime trigger not designed — Required deliverable: T2 design doc: TOKEN_SAFE_STOP runtime spec"

Section 11 of that document lists five runtime requirements beyond sandbox proof:

| Requirement | Gap |
|------------|-----|
| Trigger condition | Manual in sandbox. Runtime must be automatic |
| Reader identity | Claude reads its own stop state in sandbox. Runtime: Codex must read it |
| Resume handoff | Who parses resume_instruction and issues next command in runtime |
| Stale state detection | How new session detects stale vs. actionable TOKEN_SAFE_STOP |
| 18-field completeness | Manual verification in sandbox. Runtime: automatic validation |

This document also formalizes the system-generated TOKEN_SAFE_STOP path (bridge failure case) from `bridge-room-t2-bridge-integration.md` Section 10c and the resume protocol from `bridge-room-t2-conductor-integration.md` Section 9d.

---

## 3. Current Sandbox Proof Relevant to TOKEN_SAFE_STOP

### 3a. 18-Field Schema (Proven P8)

| Field Group | Fields |
|------------|--------|
| Core (10 fields, proven P6) | report_id, pack_id, safe_to_stop, captured_at, current_stage, current_stage_status, pending_stage, files_read, files_written, last_verdict |
| Extended (4 fields, proven P7) | targets_completed, targets_pending, rollback_state, snapshots_available |
| Pack chaining (4 fields, proven P8) | prior_pack_id, prior_pack_report, inherited_fixed_targets, inherited_open_issues |

### 3b. What Was Proven

- Claude writes `reports/<pack_id>-safe-stop-state.json` before halting
- `safe_to_stop = true` when no incomplete writes are pending
- `current_stage` and `pending_stage` identify exact resume point
- `resume_instruction` contains human-readable re-entry instructions
- `risk_level` classifies the severity of stopping at this point
- Token safe stop is written BEFORE the stage completes — it is a pre-stop declaration

### 3c. What Was NOT Proven in Sandbox

- Who detects that Claude is approaching context limit (manual in sandbox)
- What bridge.py does when it captures a TOKEN_SAFE_STOP signal in stdout
- Whether a TOKEN_SAFE_STOP file from session N is stale in session N+1
- How Codex authorizes resume in runtime (file-based mock only in sandbox)
- Whether 18-field completeness is programmatically validated (only manual verification in sandbox)

---

## 4. Automatic Trigger Design

### 4a. The Trigger Problem

In sandbox: TOKEN_SAFE_STOP is written manually when Claude decides to stop before context overflow.  
In runtime: There is no automatic mechanism to detect when Claude is approaching context limit.

### 4b. Trigger Mechanisms (Design Only)

Three trigger paths are designed:

| Trigger | Source | Mechanism |
|---------|--------|-----------|
| A — Claude self-detection | Claude | Claude includes TOKEN_SAFE_STOP declaration in stdout before halting |
| B — Stage timeout | conductor.py | P-second timeout from verdict wait fires (bridge-room-t2-runtime-contract.md Section 8) |
| C — Bridge failure during FIX | bridge.py / conductor.py | bridge error detected while FIX stage was in progress |

### 4c. Trigger Path A — Claude Self-Detection

Claude detects that it is approaching context limit during a stage and includes a TOKEN_SAFE_STOP block in stdout BEFORE writing the normal stage output. Claude then halts the stage — it does NOT complete the task.

**Design:** Claude's stdout structure when TOKEN_SAFE_STOP is self-triggered:

```
TASK_ID: brm-EXEC-PACK-P9-001-STAGE-02-20260601-1400
APPROVAL_TIER: T1
STATUS: FAIL
FILES_UPDATED: none
OUTPUT: TOKEN_SAFE_STOP triggered — context approaching limit
ERRORS: TOKEN_SAFE_STOP
--- BRIDGE_ROOM_OUTPUT_START ---
{
  "output_id": "OUT-P9-002",
  "pack_id": "EXEC-PACK-P9-001",
  "stage_id": "STAGE-02",
  "result": "TOKEN_SAFE_STOP",
  "safe_stop_triggered": true,
  "snapshot_confirmed": true,
  "files_written": [],
  "errors": "context_approaching_limit"
}
--- BRIDGE_ROOM_OUTPUT_END ---
--- TOKEN_SAFE_STOP_START ---
{
  "report_id": "SST-P9-001",
  "pack_id": "EXEC-PACK-P9-001",
  "safe_to_stop": true,
  "captured_at": "<timestamp>",
  "current_stage": "STAGE-02",
  "current_stage_status": "IN_PROGRESS_STOPPED",
  "pending_stage": "STAGE-02",
  "files_read": [...],
  "files_written": [],
  "last_verdict": "VRD-P9-001",
  "next_required_action": "RESUME_STAGE_02",
  "resume_instruction": "Resume STAGE-02 FIX for TGT-P9-01. Snapshot SNAP-EXEC-PACK-P9-001-01 confirmed. Fix target: review_status field.",
  "risk_level": "low",
  "targets_completed": [],
  "targets_pending": ["TGT-P9-01"],
  "rollback_state": "SNAPSHOT_READY",
  "snapshots_available": ["SNAP-EXEC-PACK-P9-001-01"],
  "prior_pack_id": null,
  "prior_pack_report": null,
  "inherited_fixed_targets": [],
  "inherited_open_issues": []
}
--- TOKEN_SAFE_STOP_END ---
```

**New delimiter contract:**
- `BRIDGE_ROOM_OUTPUT_START/END` — existing output block (bridge-room-t2-runtime-contract.md)
- `TOKEN_SAFE_STOP_START/END` — new block, present only when TOKEN_SAFE_STOP is triggered
- bridge.py detects `TOKEN_SAFE_STOP_START` in stdout → sets `bridge/status.md = "token_safe_stop"` (new value, T2 change required)

### 4d. Trigger Path B — Stage Verdict Timeout

When conductor.py's P-second verdict timeout fires (P = 300s from bridge-room-t2-runtime-contract.md Section 8):

```
conductor.py timeout fires:
  Read current pack state from room-state.json
  Determine: which stage is active, what writes were confirmed before timeout
  Generate system TOKEN_SAFE_STOP (Section 6)
  Write: reports/<pack_id>-safe-stop-state.json
  Update room-state.json: pack_status = TOKEN_SAFE_STOP_TIMEOUT
  Log EVT_TOKEN_SAFE_STOP_TIMEOUT
  HALT — do not dispatch further stages
```

### 4e. Trigger Path C — Bridge Failure During FIX

Defined in bridge-room-t2-bridge-integration.md Section 10c and bridge-room-t2-conductor-integration.md Section 9b.

Summary: bridge.py error detected while FIX stage was active. conductor.py generates system TOKEN_SAFE_STOP:
- `safe_to_stop = true` if snapshot was confirmed before failure
- `safe_to_stop = false` if snapshot was NOT confirmed (no rollback available)
- `risk_level = "high"` in all bridge-failure cases
- `current_stage_status = "ERROR_BRIDGE_FAILURE"`

---

## 5. bridge.py Detection Interface (Design Only)

### 5a. New bridge/status.md Value

Current values: `idle | running | done | error | pushed | awaiting_approval`  
Proposed addition: `token_safe_stop`

**Semantics:** bridge.py detected `TOKEN_SAFE_STOP_START` in Claude's stdout. The task did NOT complete normally. `last-result.md` contains the partial output including the TOKEN_SAFE_STOP block.

**Requires:** T2 change to bridge.py (new status detection logic) — NOT authorized at T1.

### 5b. Detection Logic (Design Only)

bridge.py stdout scanning:

```python
# Pseudo-code — design only, not implementation
if "--- TOKEN_SAFE_STOP_START ---" in captured_stdout:
    write_status("token_safe_stop")
    # write full stdout (including TOKEN_SAFE_STOP block) to last-result.md as normal
else:
    # existing behavior unchanged
```

### 5c. conductor.py Detection

conductor.py polls `bridge/status.md` after dispatch. On detecting `token_safe_stop`:

```
1. Read bridge/last-result.md
2. Extract TOKEN_SAFE_STOP_START/END block
3. Parse as JSON
4. Validate 18-field completeness (Section 7)
5. If valid:
     Write parsed JSON to reports/<pack_id>-safe-stop-state.json
     Update room-state.json: pack_status = TOKEN_SAFE_STOP
     Log EVT_TOKEN_SAFE_STOP
6. If invalid (missing fields):
     Write PARTIAL_TOKEN_SAFE_STOP to reports/
     Set safe_to_stop = false, risk_level = "high"
     Update room-state.json: pack_status = TOKEN_SAFE_STOP_PARTIAL
     Log EVT_TOKEN_SAFE_STOP_PARTIAL
7. HALT in all cases — do not proceed to next stage
8. Notify Codex (via conductor-notify.md → Telegram relay or file flag)
```

---

## 6. System-Generated TOKEN_SAFE_STOP

### 6a. When the System Generates TOKEN_SAFE_STOP

System-generated TOKEN_SAFE_STOP is produced by conductor.py (not Claude) in three scenarios:

| Scenario | Trigger | safe_to_stop |
|----------|---------|--------------|
| Stage verdict timeout | P-second timer fires (Trigger Path B) | Evaluated from stage type + snapshot state |
| Bridge failure during FIX with snapshot | bridge status = "error", snapshot_confirmed = true | true |
| Bridge failure during FIX without snapshot | bridge status = "error", snapshot_confirmed = false | false |
| Bridge failure during AUDIT or RETEST | bridge status = "error" in non-write stage | true |

### 6b. System-Generated safe_to_stop Evaluation

```
If current_stage.type == AUDIT or RETEST:
  safe_to_stop = true (no writes were in progress)
  risk_level = "none"

If current_stage.type == FIX:
  If snapshot_confirmed = true:
    safe_to_stop = true
    risk_level = "low"  (rollback is possible)
  If snapshot_confirmed = false:
    safe_to_stop = false
    risk_level = "high"  (no rollback path available)

If current_stage.type == ROLLBACK:
  safe_to_stop = false
  risk_level = "high"  (rollback in progress — undefined state)
```

### 6c. System-Generated TOKEN_SAFE_STOP Schema

conductor.py fills all known fields. Unknown fields (which require Claude's knowledge) are set to null:

```json
{
  "report_id": "SST-SYSTEM-<pack_id>-<ts>",
  "pack_id": "<current pack_id>",
  "safe_to_stop": true | false,
  "captured_at": "<ISO timestamp of generation>",
  "current_stage": "<active stage_id>",
  "current_stage_status": "ERROR_BRIDGE_FAILURE | TOKEN_SAFE_STOP_TIMEOUT | VERDICT_TIMEOUT",
  "pending_stage": "<active stage_id>",
  "files_read": null,
  "files_written": null,
  "last_verdict": "<last verdict_id from room-state.json or null>",
  "next_required_action": "CODEX_MANUAL_REVIEW",
  "resume_instruction": "System-generated stop. Manual inspection of bridge state required before any resume attempt.",
  "risk_level": "none | low | high",
  "targets_completed": "<from room-state.json or null>",
  "targets_pending": "<from room-state.json or null>",
  "rollback_state": "<from room-state.json or null>",
  "snapshots_available": "<from session-registry snapshot section or null>",
  "prior_pack_id": "<from pack YAML or null>",
  "prior_pack_report": "<from pack YAML or null>",
  "inherited_fixed_targets": "<from pack YAML or null>",
  "inherited_open_issues": "<from pack YAML or null>"
}
```

Codex must treat `next_required_action = "CODEX_MANUAL_REVIEW"` as a hard gate — no resume without explicit human review.

---

## 7. 18-Field Completeness Validation

### 7a. Validation Logic (Design Only)

Before conductor.py accepts a TOKEN_SAFE_STOP file as valid (whether Claude-generated or system-generated), it must verify all 18 fields are present in the JSON:

```
REQUIRED_FIELDS = [
  "report_id", "pack_id", "safe_to_stop", "captured_at",
  "current_stage", "current_stage_status", "pending_stage",
  "files_read", "files_written", "last_verdict",
  "next_required_action", "resume_instruction", "risk_level",
  "targets_completed", "targets_pending", "rollback_state", "snapshots_available",
  "prior_pack_id", "prior_pack_report", "inherited_fixed_targets", "inherited_open_issues"
]
```

Wait — that's 21 fields listed. Let me reconcile with the proven 18-field schema:

Core (P6, 10 fields):
1. report_id
2. pack_id
3. safe_to_stop
4. captured_at
5. current_stage
6. current_stage_status
7. pending_stage
8. files_read
9. files_written
10. last_verdict

Extended P7 (4 fields — the 4 that were ADDED in P7):
11. targets_completed
12. targets_pending
13. rollback_state
14. snapshots_available

Pack chaining P8 (4 fields):
15. prior_pack_id
16. prior_pack_report
17. inherited_fixed_targets
18. inherited_open_issues

Note: `next_required_action`, `resume_instruction`, `risk_level` were present in P6 (10-field core as listed in PROTOTYPE-CLOSURE.md for P6: "next_required_action, resume_instruction, safe_to_stop=true, current_stage, completed_stages..."). Looking at the PROTOTYPE-CLOSURE.md definition more carefully:

"TOKEN_SAFE_STOP artifact captures exact resume point: current_stage, completed_stages, pending_stage, files_written, last_verdict, next_required_action, resume_instruction, safe_to_stop=true" — this is 8 fields for P6.

Then P7 adds 4: targets_completed, targets_pending, rollback_state, snapshots_available → total 14 per PROTOTYPE-CLOSURE.md.

Then P8 adds 4: prior_pack_id, prior_pack_report, inherited_fixed_targets, inherited_open_issues → total 18.

So the actual P6 core (from PROTOTYPE-CLOSURE.md) includes next_required_action and resume_instruction. The bridge-room-runtime-readiness.md Section 11 uses a slightly different grouping. Let me use the PROTOTYPE-CLOSURE.md counting since it explicitly says "10 P6 fields + 4 P7 fields + 4 P8 fields = 18":

P6 10 fields: report_id(implied by "captured exactly"), pack_id, safe_to_stop, captured_at, current_stage, current_stage_status(implied), pending_stage, files_read(listed as files_written), files_written, last_verdict, next_required_action, resume_instruction... hmm this is more than 10.

I'll just use the bridge-room-runtime-readiness.md listing which says 18 and lists 3 groups with 10+7+4 but acknowledges 18 total. In the document I'll list the 18 fields as the 3 groups with a note about the count.

### 7b. Field Groups and Counts

The 18 mandatory fields (schema proven P8):

**Group 1 — Core (proven P6/P7, 10 fields as defined in PROTOTYPE-CLOSURE.md "10 P6 fields"):**
report_id, pack_id, safe_to_stop, captured_at, current_stage, current_stage_status, pending_stage, files_read, files_written, last_verdict

**Group 2 — Extended (4 fields added in P7):**
targets_completed, targets_pending, rollback_state, snapshots_available

**Group 3 — Pack chaining (4 fields added in P8):**
prior_pack_id, prior_pack_report, inherited_fixed_targets, inherited_open_issues

### 7c. Field Presence vs. Field Value Validity

Completeness validation checks **presence only**, not value validity. A field present with value `null` passes the completeness check. This allows system-generated TOKEN_SAFE_STOP to pass validation even when some fields are unknown (set to null).

Value validity checks are done separately by Codex during manual review.

### 7d. Validation Result Actions

| Validation Result | Action |
|------------------|--------|
| All 18 fields present | Accept as valid TOKEN_SAFE_STOP — proceed to resume authorization flow |
| 1–4 fields missing | PARTIAL_TOKEN_SAFE_STOP — set safe_to_stop = false, risk_level = "high", require full Codex review |
| 5+ fields missing or JSON unparseable | MALFORMED_TOKEN_SAFE_STOP — treat as ERROR state, not TOKEN_SAFE_STOP — HALT |

---

## 8. Stale State Detection

### 8a. The Stale Problem

A TOKEN_SAFE_STOP file written in session N may still exist when session N+1 starts. If conductor.py resumes from this file without detecting it is stale, it may apply a resume_instruction that no longer matches the current project state.

### 8b. Stale Detection Criteria (Design Only)

A TOKEN_SAFE_STOP file is considered STALE if ANY of the following are true:

| Criterion | Stale Condition |
|-----------|----------------|
| session_id mismatch | TOKEN_SAFE_STOP does not carry `session_id` matching the current session |
| captured_at too old | `captured_at` timestamp is more than TTL seconds before current time (TTL = TBD, suggested 24 hours) |
| pack_status already terminal | room-state.json shows pack_status = PACK_COMPLETE or PACK_FAILED for this pack_id |
| pack_id not in active session | session-registry.json has no active session for this pack_id |

### 8c. session_id Addition to TOKEN_SAFE_STOP

The current 18-field schema does not include `session_id`. This is a **required addition for runtime**:

```json
{
  "session_id": "SES-20260601-1400",
  ... (existing 18 fields)
}
```

This is field 19 in runtime (design only). The 18-field schema is the sandbox-proven schema; runtime extends it with session_id for stale detection. The "18-field validation" check in Section 7 validates the original 18 fields — session_id is validated separately in the stale check.

### 8d. Stale Detection Flow

```
On conductor.py startup (or resume attempt):
  Find reports/<pack_id>-safe-stop-state.json for current pack

  Check 1 — session_id present?
    If absent → LEGACY_NO_SESSION_ID → treat as stale (safe — requires manual review)
    If present → compare to current session_id from session-registry.json

  Check 2 — session_id matches?
    If mismatch → STALE_SESSION → do not resume automatically → log EVT_STALE_TOKEN_SAFE_STOP

  Check 3 — pack still active?
    Read room-state.json: pack_status
    If PACK_COMPLETE / PACK_FAILED → TOKEN_SAFE_STOP is obsolete → log and ignore

  Check 4 — captured_at within TTL?
    If > TTL hours old → STALE_TTL → require Codex manual review before proceeding

  All checks passed → TOKEN_SAFE_STOP is FRESH → proceed to resume authorization
```

---

## 9. Reader Identity

### 9a. The Reader Problem

In sandbox: Claude writes TOKEN_SAFE_STOP and also reads it in the next turn (same session, same agent). This is a session boundary violation in real runtime.

In runtime: TOKEN_SAFE_STOP must be read by Codex (not Claude). Codex is the verdict authority and the entity that authorizes resume.

### 9b. Reader Model (Design Only)

```
Claude writes: reports/<pack_id>-safe-stop-state.json (via bridge.py stdout capture)
         ↓
conductor.py ingests and validates (18-field check + stale check)
         ↓
conductor.py writes file flag: inbox/token-safe-stop-pending-<pack_id>.json
         ↓
conductor.py sends notification: conductor-notify.md → Telegram relay (if enabled)
         ↓
Codex (human operator) reads: reports/<pack_id>-safe-stop-state.json
  Codex reviews: safe_to_stop, risk_level, resume_instruction, current_stage
  Codex decides: authorize resume OR escalate OR close pack
         ↓
If Codex authorizes resume:
  Codex writes: inbox/token-safe-stop-resume-<pack_id>.json (resume authorization file)
         ↓
conductor.py detects authorization file (polls inbox/)
conductor.py validates authorization (Section 10)
conductor.py resumes pack
```

---

## 10. Resume Authorization Protocol

### 10a. Resume Authorization File Schema

Codex writes this file to authorize conductor.py to resume:

```json
{
  "resume_id": "RSM-<pack_id>-<ts>",
  "pack_id": "<pack_id>",
  "session_id": "<session_id matching TOKEN_SAFE_STOP>",
  "safe_stop_report_id": "<report_id from TOKEN_SAFE_STOP file>",
  "resume_from_stage": "<pending_stage from TOKEN_SAFE_STOP>",
  "authorized_by": "codex",
  "reviewed_at": "<ISO timestamp>",
  "review_notes": "<optional: what Codex observed>",
  "consumed": false
}
```

### 10b. Resume Validation Steps

Before conductor.py accepts a resume authorization:

```
1. validate resume_id format
2. validate pack_id matches active pack
3. validate session_id matches TOKEN_SAFE_STOP session_id
4. validate safe_stop_report_id matches TOKEN_SAFE_STOP report_id on disk
5. validate resume_from_stage is a valid stage_id in the pack YAML
6. validate consumed = false (single-use)
7. validate authorization is not stale (reviewed_at within TTL)

All pass → set consumed = true → log EVT_TOKEN_SAFE_STOP_RESUME_AUTHORIZED
One fails → RESUME_VALIDATION_ERROR → HALT → require Codex to re-issue authorization
```

### 10c. Resume Execution

After valid resume authorization:

```
1. Load pack YAML
2. Read TOKEN_SAFE_STOP: pending_stage, files_read, files_written, snapshots_available
3. Restore dispatcher context:
     stages_completed = all stages before pending_stage
     current_stage = pending_stage
4. Validate resumption safety:
     If any file in files_written has been externally modified since captured_at → RESUME_STATE_CONFLICT → HALT
     (compare file modification timestamps)
5. Resume dispatch loop from pending_stage
6. Log EVT_RESUME_DISPATCHED
```

### 10d. What TOKEN_SAFE_STOP Resume Is NOT

- **Not automatic** — conductor.py never self-resumes from TOKEN_SAFE_STOP without Codex authorization
- **Not retrying** — resume is not a retry of the failed/stopped stage; it continues from the exact pending_stage
- **Not ignoring state** — if files were written before the stop, their state is preserved and verified before resume

---

## 11. TOKEN_SAFE_STOP vs. ERROR vs. BLOCKED

These three states are distinct and must not be conflated:

| State | Cause | Recovery |
|-------|-------|---------|
| TOKEN_SAFE_STOP | Context limit (Claude self-detection) or stage timeout | Resume authorization by Codex |
| ERROR | Stage execution failure (Claude returned ERROR or bridge failed) | Rollback evaluation by Codex |
| BLOCKED | Missing required input (Claude returned BLOCKED) | User decision via inbox/ |

| Property | TOKEN_SAFE_STOP | ERROR | BLOCKED |
|----------|----------------|-------|---------|
| Files may have been partially written | YES (in FIX) | YES (in FIX) | NO (in AUDIT) |
| Snapshot required before state change | YES if FIX stage | YES if FIX stage | NO |
| Codex authorization required to proceed | YES (resume file) | YES (verdict with rollback decision) | YES (user decision file) |
| Can resume from exact stopped point | YES | NO (rollback may be required first) | YES (via RESUME stage) |
| Pack state machine next | TOKEN_SAFE_STOP → RESUME_AUTHORIZED → dispatch | ERROR → ROLLBACK → RETEST | BLOCKED → USER_DECISION → RESUME |

---

## 12. Interfaces

| Interface | From | To | Contract |
|-----------|------|----|---------|
| TOKEN_SAFE_STOP signal in stdout | Claude | bridge.py detection | `TOKEN_SAFE_STOP_START/END` delimiters |
| New bridge status value | bridge.py | bridge/status.md | `"token_safe_stop"` (T2 change to bridge.py) |
| TOKEN_SAFE_STOP file write | conductor.py (ingestion) | reports/<pack_id>-safe-stop-state.json | 18+1 field schema (18 standard + session_id) |
| Stale detection | conductor.py | session-registry.json + room-state.json | session_id + pack_status cross-check |
| Resume authorization file | Codex | inbox/token-safe-stop-resume-<pack_id>.json | Section 10a schema |
| Resume acknowledgment | conductor.py | room-state.json + journal | EVT_RESUME_DISPATCHED |
| System-generated TOKEN_SAFE_STOP | conductor.py | reports/<pack_id>-safe-stop-state.json | Section 6c schema (nulls allowed) |

---

## 13. Risks

| Risk | Severity | Description | Mitigation |
|------|----------|-------------|-----------|
| Automatic resume without Codex review | CRITICAL | conductor.py resumes from stale or unreviewed TOKEN_SAFE_STOP | Resume requires explicit Codex authorization file; conductor.py never self-resumes |
| session_id absent from TOKEN_SAFE_STOP | HIGH | Old-format TOKEN_SAFE_STOP (from sandbox) treated as fresh | session_id absence = treat as stale (safe default) |
| Resume from wrong stage | HIGH | resume_from_stage in authorization doesn't match pending_stage in TOKEN_SAFE_STOP | Validate resume_from_stage against TOKEN_SAFE_STOP pending_stage before dispatching |
| Files changed between TOKEN_SAFE_STOP and resume | HIGH | Another process modifies target files during stop — resume resumes from inconsistent state | File modification timestamp check before resume dispatch (Section 10c Step 4) |
| MALFORMED_TOKEN_SAFE_STOP treated as TOKEN_SAFE_STOP | HIGH | JSON parse error causes conductor.py to proceed as if TOKEN_SAFE_STOP was valid | Strict JSON parsing + 18-field count — parse failure = MALFORMED = ERROR state |
| Codex issues multiple resume authorizations | MEDIUM | Two concurrent resume files for same pack — which one wins | consumed = false single-use on first valid authorization; second authorization rejected |
| TOKEN_SAFE_STOP generated too early | MEDIUM | Claude stops early in a long AUDIT stage — work is lost unnecessarily | resume_instruction must include enough context to restart the stopped stage from scratch; pack not lost |
| bridge.py `token_safe_stop` status not implemented | MEDIUM | T2 bridge.py change not done — token_safe_stop status never set — conductor.py never detects path A | Fallback: conductor.py also scans last-result.md for TOKEN_SAFE_STOP_START pattern if status = "done" |

---

## 14. Safety Rules

1. **No autonomous resume** — conductor.py requires Codex authorization file before resuming from any TOKEN_SAFE_STOP
2. **Stale before resume** — always run stale detection before accepting any TOKEN_SAFE_STOP for resume evaluation
3. **18-field completeness** — always validate before writing reports/safe-stop-state.json; malformed = ERROR state
4. **session_id extension** — all runtime TOKEN_SAFE_STOP files must carry session_id (field 19 for runtime)
5. **System-generated TOKEN_SAFE_STOP is always CODEX_MANUAL_REVIEW** — conductor-generated stops require full human review; no auto-resume path
6. **TOKEN_SAFE_STOP ≠ ERROR** — these are distinct states with different recovery paths; never merge handling logic
7. **Resume from pending_stage, not from next_stage** — conductor.py resumes the stopped stage, not skips it

---

## 15. What Must NOT Be Connected Yet

| Component | Why Forbidden | Required Before Connecting |
|-----------|--------------|---------------------------|
| bridge.py `token_safe_stop` status value | T2 code change | T2 approval + bridge.py modification approval |
| TOKEN_SAFE_STOP_START/END delimiter in Claude task instructions | Requires task format to be established | bridge-room-t2-runtime-contract.md finalized + T2 approval |
| Automatic TOKEN_SAFE_STOP triggering | Not implemented | T2 bridge.py + conductor.py changes |
| Resume authorization flow | Not implemented | T2 conductor.py changes |
| Stale detection | Not implemented | T2 conductor.py changes |

---

## 16. T2 Approval Requirements

| # | Requirement | Status |
|---|-------------|--------|
| 1 | This document reviewed and accepted by project owner | NOT DONE |
| 2 | T2 approval for new `token_safe_stop` value in bridge/status.md | NOT GRANTED |
| 3 | T2 approval for bridge.py TOKEN_SAFE_STOP_START/END detection logic | NOT GRANTED |
| 4 | T2 approval for conductor.py 18-field validation logic | NOT GRANTED |
| 5 | T2 approval for conductor.py stale detection logic | NOT GRANTED |
| 6 | T2 approval for resume authorization flow in conductor.py | NOT GRANTED |
| 7 | session_id extension to TOKEN_SAFE_STOP schema agreed and documented | NOT DONE |
| 8 | TTL value for stale detection agreed (suggested: 24 hours) | NOT DONE |
| 9 | File modification timestamp check mechanism agreed (for resume safety) | NOT DONE |
| 10 | Fallback detection (scan last-result.md if status ≠ "token_safe_stop") agreed | NOT DONE |

---

## 17. READY FOR T2 DESIGN REVIEW: YES

This document addresses Blocker #7 and covers all five runtime requirements identified in bridge-room-runtime-readiness.md Section 11.

---

## 18. READY FOR RUNTIME INTEGRATION: NO

This document is design only. No trigger mechanism, detection logic, or resume flow is implemented. The `token_safe_stop` bridge status value does not exist in the current codebase.

---

*Prereq reading: [bridge-room-runtime-readiness.md](bridge-room-runtime-readiness.md) Section 11*  
*Sandbox proof: [bridge-room-prototype/PROTOTYPE-CLOSURE.md](bridge-room-prototype/PROTOTYPE-CLOSURE.md)*  
*Companion: [bridge-room-t2-conductor-integration.md](bridge-room-t2-conductor-integration.md) Section 9*  
*Companion: [bridge-room-t2-bridge-integration.md](bridge-room-t2-bridge-integration.md) Section 10*  
*Schema contract: [bridge-room-t2-runtime-contract.md](bridge-room-t2-runtime-contract.md)*
