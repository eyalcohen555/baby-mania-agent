# Bridge Room — Prototype #8 Design
# Follow-Up Pack from P7 Open Issue — Pack Chaining

**STATUS:** DESIGN ONLY — NOT BUILT  
**APPROVAL_TIER:** T1  
**LAYER:** 1  
**CREATED:** 2026-05-04  
**PROTOTYPE:** #8 — Follow-Up Pack / Pack Chaining  
**BASED ON:**
- `docs/management/bridge-room-prototype/reports/pack-p7-final-report.json`
- `docs/management/bridge-room-prototype/reports/pack-p7-safe-stop-state.json`
- `docs/management/bridge-room-prototype/execution-pack-p7.yaml`

---

## SYSTEM STATE

| Field | Value |
|-------|-------|
| Last closed prototype | Prototype #7 — PACK_PASS_PARTIAL |
| Pack ID | EXEC-PACK-P7-001 |
| Commit | f7281f1 |
| Approval tier | T1 |
| Runtime integration | NOT APPROVED |
| Telegram | NOT APPROVED |
| Ready for next sandbox | YES |

**Capabilities proven through P7 (14 total):**

1. Single-stage AUDIT with verdict
2. Single-stage FIX with PRE_FIX_SNAPSHOT
3. RETEST after FIX
4. PASS / FAIL / BLOCKED / ERROR status values
5. Evidence blocks: FIELD_CHECK, SCOPE_CHECK, VALIDATION
6. ID chain: pack_id → task_id → stage_id → command_id → output_id → verdict_id
7. TOKEN_SAFE_STOP (10 fields, P6)
8. Multi-target AUDIT with per-target PASS/FAIL
9. Selective FIX — only audit-failing targets
10. ERROR state with error_type + error_detail + rollback_required
11. PRE_FIX_SNAPSHOT before any FIX write
12. ROLLBACK stage triggered only after ERROR verdict
13. ROLLBACK_PASS verdict with matches_snapshot confirmation
14. PACK_PASS_PARTIAL with targets_fixed / targets_rolled_back / targets_unchanged
15. TOKEN_SAFE_STOP extended to 14 fields (adds: targets_completed, targets_pending, rollback_state, snapshots_available)

---

## P7 OPEN ISSUE CONFIRMED

**Source:** `reports/pack-p7-final-report.json` → `open_issues`

```
ISS-P7-002
  target_id:    TGT-P7-02
  file:         mock-target-p7-02.md
  field:        review_status
  issue_type:   INVALID_VALUE
  expected:     "approved"
  actual:       "unreviewed"
  fix_result:   ERROR (review_status written as null — wrong type)
  rollback:     ROLLBACK_PASS — file restored to pre-fix state
  issue_status: OPEN — requires follow-up pack
```

**Why it is still open:**
- P7 FIX wrote `review_status: null` instead of `review_status: "approved"`.
- ERROR verdict triggered ROLLBACK.
- ROLLBACK restored file to `review_status: unreviewed` (original broken value).
- P7 ended as PACK_PASS_PARTIAL — issue not resolved.

**Current file state (mock-target-p7-02.md after P7):**
```
review_status: unreviewed   ← broken, not fixed
```

**TGT-P7-01 current state:** `quality_standard: premium` — FIXED by P7, must remain fixed in P8.  
**TGT-P7-03 current state:** All fields clean — UNCHANGED through P7, must remain unchanged in P8.

---

## WHY PROTOTYPE #8 IS NEEDED

P7 proved ERROR + ROLLBACK flow but left ISS-P7-002 unresolved.  
P8 proves the missing capability:

> **Pack chaining** — a new Execution Pack is issued specifically to resolve an open issue
> from a prior pack's final report. P8 reads P7's report as its *input*, not as context.

This is the first sandbox to demonstrate:
- A pack that is born from another pack's open issue
- Cross-pack state preservation (P7-fixed targets must survive P8)
- `prior_pack_id` field in Execution Pack YAML and TOKEN_SAFE_STOP
- ISSUE_AUDIT stage type (new): reads P7 report + current file state, confirms issue is still open before proceeding

Without P8, "follow-up packs" and "pack chaining" remain unproven design concepts.

---

## PROPOSED PROTOTYPE #8

**Pack ID:** EXEC-PACK-P8-001  
**Pack Name:** Execution Pack v1 — Prototype #8  
**Goal:** Resolve ISS-P7-002 (TGT-P7-02 review_status) via follow-up pack.  
**Source pack:** EXEC-PACK-P7-001  
**Source issue:** ISS-P7-002  
**Targets:** 1 active (TGT-P7-02) + 2 read-only for cross-pack RETEST  

### Flow

```
[Codex reads P7 final report]
     │
     ▼
STAGE-01: ISSUE_AUDIT
  Read: pack-p7-final-report.json + mock-target-p7-02.md
  Confirm: ISS-P7-002 still open, review_status ≠ "approved"
  Output: pack-p8-stage-01-output.json
  Verdict: CONFIRMED or RESOLVED (exit if already fixed)
     │
     ▼ (if CONFIRMED)
STAGE-02: PRE_FIX_SNAPSHOT + FIX
  Snapshot: pre-fix-target-p8-02.md.bak  ← new P8 snapshot, not P7 .bak
  Fix: mock-target-p7-02.md → review_status: "approved"  (string, not null)
  Output: pack-p8-stage-02-output.json
  Verdict: PASS / ERROR
     │                      │
     ▼ (PASS)               ▼ (ERROR)
STAGE-03: RETEST         STAGE-ROLLBACK
  Read all 3 targets         Restore from pre-fix-target-p8-02.md.bak
  Verify:                    Output: pack-p8-rollback-output.json
    TGT-P7-02 = approved     Verdict: ROLLBACK_PASS / ROLLBACK_FAIL
    TGT-P7-01 = premium (from P7, must still hold)
    TGT-P7-03 = unchanged (from P7, must still hold)
  Output: pack-p8-stage-03-output.json
  Verdict: PACK_PASS → PACK_COMPLETE
               │
               ▼
  ISS-P7-002 RESOLVED
  pack-p8-final-report.json
  pack-p8-safe-stop-state.json
  execution-pack-p8-log.jsonl
```

### Stage Summary

| Stage ID | Type | Actor | Goal |
|----------|------|-------|------|
| STAGE-01 | ISSUE_AUDIT | Claude reads, Codex verdicts | Confirm ISS-P7-002 still open |
| STAGE-02 | PRE_FIX_SNAPSHOT + FIX | Claude | Snapshot + fix review_status correctly |
| STAGE-ROLLBACK | ROLLBACK | Claude | Restore from P8 snapshot (if ERROR) |
| STAGE-03 | RETEST | Claude reads, Codex verdicts | Confirm all 3 targets in expected state |

### New Capabilities Proven by P8

1. **Pack chaining** — P8 ingests P7 final report as primary input
2. **ISSUE_AUDIT stage** — reads prior pack report + current file state, confirms open issue before proceeding
3. **Single-target follow-up pack** — 1 active fix target, 2 read-only cross-pack verification targets
4. **Cross-pack state preservation** — RETEST confirms TGT-P7-01 (P7-fixed) and TGT-P7-03 (P7-clean) survive P8
5. **Prior pack fields in TOKEN_SAFE_STOP** — `prior_pack_id`, `prior_pack_report`, `inherited_fixed_targets`, `inherited_open_issues`
6. **RESOLVED issue closure** — `resolved_issues: [ISS-P7-002]` in P8 final report
7. **P8-specific snapshot** — separate from P7 snapshots, ensures clean rollback lineage
8. **Correct string FIX** — demonstrates that the P7 error (null type) is avoidable with proper type validation

---

## PACK CHAINING DESIGN

### What Pack Chaining Means

Pack chaining is the ability for a new Execution Pack to:
1. Read a prior pack's final report as its *authoritative input*
2. Identify specific open issues from that report
3. Scope itself only to those open issues
4. Reference the prior pack in its own artifacts
5. Demonstrate that prior pack's fixed targets are not disturbed

It is **not** a runtime feature. It is a **design contract** enforced by:
- The `prior_pack_id` field in `execution-pack-p8.yaml`
- The ISSUE_AUDIT stage as the mandatory first stage
- The cross-pack RETEST in STAGE-03
- The TOKEN_SAFE_STOP `inherited_*` fields

### How Codex Authorizes P8

1. Codex reads `reports/pack-p7-final-report.json`
2. Locates `open_issues: ["ISS-P7-002 — TGT-P7-02 review_status: unreviewed"]`
3. Reads current `mock-target-p7-02.md` directly → confirms `review_status: unreviewed`
4. Issues P8 pack with:
   ```yaml
   prior_pack_id: EXEC-PACK-P7-001
   source_issue: ISS-P7-002
   source_report: docs/management/bridge-room-prototype/reports/pack-p7-final-report.json
   ```
5. Issues STAGE-01 command to Claude: confirm issue still open

### ISSUE_AUDIT Stage (New Stage Type)

Claude must:
- Read `reports/pack-p7-final-report.json` → find `open_issues[]`
- Read `mock-target-p7-02.md` → read current `review_status` value
- Return per-field evidence: `{field: "review_status", current: "unreviewed", expected: "approved", status: "OPEN"}`
- Do NOT modify any file
- Output status: `CONFIRMED` (still open) or `RESOLVED` (already fixed — pack exits cleanly)

If RESOLVED: Codex issues PACK_EXIT_CLEAN verdict. No FIX needed.  
If CONFIRMED: Codex issues PROCEED_TO_FIX verdict → STAGE-02 issued.

### What Claude Must NOT Do in P8

- Must NOT read P7 snapshots (`pre-fix-target-p7-02.md.bak`) as rollback source — P8 uses its own snapshot
- Must NOT modify TGT-P7-01 or TGT-P7-03 at any stage
- Must NOT reference P8 snap as P7 snap or vice versa (separate ID and filename)
- Must NOT skip ISSUE_AUDIT and jump directly to FIX

### Cross-Pack State Preservation in RETEST

STAGE-03 must verify 3 separate state claims:

| Target | Expected state | Source of truth | Verification |
|--------|---------------|-----------------|-------------|
| TGT-P7-02 | `review_status: "approved"` | Fixed by P8 STAGE-02 | Read file directly |
| TGT-P7-01 | `quality_standard: "premium"` | Fixed by P7 STAGE-02, untouched by P8 | Read file + confirm not in P8 write list |
| TGT-P7-03 | All fields clean, unchanged | Clean throughout P7 and P8 | Read file + confirm not in any P8 write list |

All 3 must PASS for PACK_COMPLETE verdict.

---

## TOKEN_SAFE_STOP — P8 EXTENSION

P7 TOKEN_SAFE_STOP had 14 required fields.  
P8 adds 4 new fields for pack chaining. Total: **18 required fields**.

### New Fields (P8)

| Field | Type | Content |
|-------|------|---------|
| `prior_pack_id` | string | `"EXEC-PACK-P7-001"` |
| `prior_pack_report` | string | Path to P7 final report |
| `inherited_fixed_targets` | array | `["TGT-P7-01"]` — targets fixed in P7, confirmed in P8 RETEST |
| `inherited_open_issues` | array | `["ISS-P7-002"]` — issues carried in from P7 |

### Full 18-Field TOKEN_SAFE_STOP for P8

```
P6 fields (10):
  pack_id, current_stage, completed_stages, pending_stage,
  files_read, files_written, last_verdict, next_required_action,
  resume_instruction, risk_level

P7 fields added (4):
  targets_completed, targets_pending, rollback_state, snapshots_available

P8 fields added (4):
  prior_pack_id, prior_pack_report,
  inherited_fixed_targets, inherited_open_issues
```

---

## HOW ROLLBACK IS PRESERVED IF P8 FIX FAILS

If STAGE-02 produces ERROR (again writing wrong type, or any write failure):

1. P8's own snapshot is used: `inbox/snapshots/pre-fix-target-p8-02.md.bak`
   - Contains the state of mock-target-p7-02.md at P8 STAGE-02 start
   - This equals the P7 post-rollback state: `review_status: unreviewed`
2. STAGE-ROLLBACK restores from `pre-fix-target-p8-02.md.bak`
3. Verdict: `ROLLBACK_PASS` → RETEST skipped, pack closes as `PACK_FAIL_ROLLBACK`
4. ISS-P7-002 remains open → would require Prototype #9

**P7 snapshots (pre-fix-target-p7-02.md.bak) are NOT used as P8 rollback source.**  
They remain frozen as historical artifacts only.

---

## FILES TO CREATE

### New files (P8 artifacts only — 18 total)

```
docs/management/bridge-room-prototype/
├── execution-pack-p8.yaml                         ← pack definition with prior_pack_id
│
├── outbox/
│   ├── pack-p8-stage-01-command.json              ← ISSUE_AUDIT command
│   ├── pack-p8-stage-02-command.json              ← PRE_FIX_SNAPSHOT + FIX command
│   ├── pack-p8-rollback-command.json              ← ROLLBACK command (if ERROR)
│   └── pack-p8-stage-03-command.json              ← RETEST command
│
├── inbox/
│   ├── pack-p8-stage-01-output.json               ← ISSUE_AUDIT result
│   ├── pack-p8-stage-02-output.json               ← FIX result
│   ├── pack-p8-rollback-output.json               ← ROLLBACK result (if needed)
│   ├── pack-p8-stage-03-output.json               ← RETEST result
│   └── snapshots/
│       └── pre-fix-target-p8-02.md.bak            ← P8 snapshot (separate from P7)
│
├── verdicts/
│   ├── pack-p8-stage-01-verdict.json              ← CONFIRMED / RESOLVED
│   ├── pack-p8-stage-02-verdict.json              ← PASS / ERROR
│   ├── pack-p8-rollback-verdict.json              ← ROLLBACK_PASS (if needed)
│   └── pack-p8-stage-03-verdict.json              ← PACK_PASS / PACK_FAIL
│
├── reports/
│   ├── pack-p8-final-report.json                  ← resolved_issues: [ISS-P7-002]
│   └── pack-p8-safe-stop-state.json               ← 18-field TOKEN_SAFE_STOP
│
└── journal/
    └── execution-pack-p8-log.jsonl                ← append-only event trace
```

### File modified (not created)

```
docs/management/bridge-room-prototype/
└── mock-target-p7-02.md                           ← FIX writes review_status: "approved"
```

### Files used as read-only input (not modified, not created)

```
docs/management/bridge-room-prototype/
├── reports/pack-p7-final-report.json              ← pack chaining source
├── reports/pack-p7-safe-stop-state.json           ← optional context
├── mock-target-p7-01.md                           ← RETEST cross-check (read only)
├── mock-target-p7-02.md                           ← ISSUE_AUDIT + FIX + RETEST
└── mock-target-p7-03.md                           ← RETEST cross-check (read only)
```

**P7 snapshot files (read-only, historical):**
```
docs/management/bridge-room-prototype/inbox/snapshots/
├── pre-fix-target-p7-01.md.bak                   ← P7 artifact, do not use in P8 rollback
└── pre-fix-target-p7-02.md.bak                   ← P7 artifact, do not use in P8 rollback
```

**Total new files: 18**  
**Files modified: 1** (mock-target-p7-02.md — only by FIX stage)  
**Files frozen: all P1–P7 artifacts** (except mock-target-p7-02.md which is the live target)

---

## PASS / FAIL / BLOCKED / ERROR RULES

### STAGE-01 — ISSUE_AUDIT

| Status | Condition |
|--------|-----------|
| `CONFIRMED` | P7 report shows ISS-P7-002 open AND current file shows review_status ≠ "approved" |
| `RESOLVED` | Current file already shows review_status: "approved" — no FIX needed |
| `BLOCKED` | P7 final report not readable or not found |
| `FAIL` | P7 report is readable but `open_issues` field missing or malformed |

### STAGE-02 — FIX

| Status | Condition |
|--------|-----------|
| `PASS` | review_status written as string `"approved"` — field type: string, value exact match |
| `ERROR` | review_status written as wrong type (null, int, bool) — `rollback_required: true` |
| `FAIL` | review_status written as wrong string (e.g., "Approved", "APPROVED") — case mismatch |
| `BLOCKED` | Snapshot not written before FIX attempted |

### STAGE-ROLLBACK (if P8 FIX → ERROR)

| Status | Condition |
|--------|-----------|
| `ROLLBACK_PASS` | mock-target-p7-02.md matches pre-fix-target-p8-02.md.bak |
| `ROLLBACK_FAIL` | Restoration incomplete or snapshot not readable |

### STAGE-03 — RETEST

| Status | Condition |
|--------|-----------|
| `PASS` → `PACK_COMPLETE` | TGT-P7-02 approved + TGT-P7-01 premium + TGT-P7-03 unchanged |
| `FAIL` | Any of the 3 targets not in expected state |
| `BLOCKED` | Any target file unreadable |

---

## ID CHAIN FOR P8

```
pack_id:      EXEC-PACK-P8-001
stage_01:     task_id=TASK-P8-001  cmd=CMD-P8-001  out=OUT-P8-001  vrd=VRD-P8-001
stage_02:     task_id=TASK-P8-002  cmd=CMD-P8-002  out=OUT-P8-002  vrd=VRD-P8-002
stage_rb:     task_id=TASK-P8-RB   cmd=CMD-P8-RB   out=OUT-P8-RB   vrd=VRD-P8-RB
stage_03:     task_id=TASK-P8-003  cmd=CMD-P8-003  out=OUT-P8-003  vrd=VRD-P8-003
snapshot_id:  SNAP-P8-01  (pre-fix-target-p8-02.md.bak)
issue_source: ISS-P7-002  (carried from P7)
```

All IDs must be consistent across: command → output → verdict → journal → final report.  
P7 IDs (`EXEC-PACK-P7-001`, `ISS-P7-002`) are reference-only — not reused for P8 artifacts.

---

## OWNERSHIP BOUNDARIES

| Role | Writes |
|------|--------|
| Claude | `inbox/pack-p8-stage-01-output.json` |
| Claude | `inbox/snapshots/pre-fix-target-p8-02.md.bak` |
| Claude | `inbox/pack-p8-stage-02-output.json` |
| Claude | `inbox/pack-p8-rollback-output.json` (if ROLLBACK triggered) |
| Claude | `inbox/pack-p8-stage-03-output.json` |
| Claude | `mock-target-p7-02.md` (FIX stage only) |
| Codex | `outbox/pack-p8-stage-*-command.json` (all 3 or 4) |
| Codex | `verdicts/pack-p8-*-verdict.json` (all 3 or 4) |
| Codex | `reports/pack-p8-final-report.json` |
| Codex | `reports/pack-p8-safe-stop-state.json` |
| Codex | `journal/execution-pack-p8-log.jsonl` |
| Codex | `execution-pack-p8.yaml` |

---

## SAFETY RULES

```yaml
safety:
  bridge_connection: false
  runtime_connection: false
  telegram: false
  shopify_writes: false
  git_operations: false
  scope: docs/management/bridge-room-prototype/**
  outside_scope_writes: false
  prototypes_1_to_7_frozen: true          # new vs P7 (was 1_to_6)
  p7_snapshots_frozen: true               # pre-fix-target-p7-0*.md.bak — read-only
  p7_artifacts_frozen: true               # all inbox/verdicts/reports from P7 — read-only
  allowed_target_write: mock-target-p7-02.md (FIX stage only)
  forbidden_target_writes:
    - mock-target-p7-01.md               # fixed by P7, must survive P8 untouched
    - mock-target-p7-03.md               # clean through P7 and P8
```

**Stop conditions specific to P8:**
- FIX attempted without CONFIRMED verdict from ISSUE_AUDIT → STOP
- ROLLBACK uses P7 snapshot instead of P8 snapshot → STOP
- TGT-P7-01 or TGT-P7-03 written at any stage → STOP
- review_status written as any type other than string → ERROR (triggers rollback)
- Any P7 artifact (except mock-target-p7-02.md) modified → STOP

---

## SUCCESS CONDITIONS

**Minimum for Prototype #8 PASS:**

| # | Condition |
|---|-----------|
| 1 | ISSUE_AUDIT reads pack-p7-final-report.json and confirms ISS-P7-002 open |
| 2 | ISSUE_AUDIT reads mock-target-p7-02.md and confirms review_status ≠ "approved" |
| 3 | PRE_FIX_SNAPSHOT written (pre-fix-target-p8-02.md.bak) before any FIX write |
| 4 | FIX writes review_status as string "approved" — not null, not int, not "Approved" |
| 5 | RETEST: TGT-P7-02 shows review_status: "approved" |
| 6 | RETEST: TGT-P7-01 shows quality_standard: "premium" (P7 fix preserved) |
| 7 | RETEST: TGT-P7-03 shows all fields clean, not in any P8 write list |
| 8 | pack-p8-final-report.json records resolved_issues: ["ISS-P7-002"] and prior_pack_id: "EXEC-PACK-P7-001" |
| 9 | TOKEN_SAFE_STOP contains all 18 fields (14 from P7 + 4 chain fields) |
| 10 | All artifacts stay within docs/management/bridge-room-prototype/** |

**Bonus (not required for PASS but worth proving):**
- STAGE-01 cleanly exits if ISS-P7-002 were already resolved (RESOLVED path — testable as edge case in notes)

---

## FILES TO FREEZE BEFORE BUILDING P8

Before issuing any P8 command, Codex must confirm:

```
mock-target-p7-01.md       → quality_standard: premium     (FIXED by P7)
mock-target-p7-02.md       → review_status: unreviewed     (ROLLED BACK by P7)
mock-target-p7-03.md       → all fields valid               (UNCHANGED through P7)
```

If any of these do not match → P8 cannot start. Codex must investigate before proceeding.

---

## WHAT IS STILL NOT PROVEN AFTER P8

| Gap | Status after P8 |
|-----|-----------------|
| Multi-hop pack chains (A → B → C) | Not yet — P8 proves A → B only |
| Parallel target packs | Not yet |
| Conditional pack branching | Not yet |
| Real Codex/Claude context separation | Not yet — both in sandbox |
| Persistent decision store | Not yet |
| Telegram integration | NOT APPROVED |
| Runtime integration | NOT APPROVED |
| Shopify writes | NOT APPROVED |

---

## READY TO BUILD PROTOTYPE #8: YES

All design preconditions met:
- ISS-P7-002 confirmed open in P7 final report ✓
- P7 target files in known state ✓
- Pack chaining flow fully specified ✓
- ID chain defined ✓
- TOKEN_SAFE_STOP 18-field schema defined ✓
- Rollback lineage separated from P7 ✓
- Ownership boundaries clear ✓
- Safety rules explicit ✓
- No runtime, Telegram, Shopify, git required ✓

## READY FOR RUNTIME INTEGRATION: NO
