# Bridge Room — Controlled Dry Run Plan

**TYPE:** Plan document — T1 only  
**STATUS:** DRAFT — NOT APPROVED FOR EXECUTION  
**APPROVAL TIER:** T1 (plan) / T2 required before execution  
**LAYER:** 1  
**CREATED:** 2026-05-04  
**SCOPE:** First controlled Bridge Room integration test after T2 design package approval  
**READY TO RUN CONTROLLED DRY RUN:** NO — T2 implementations not yet done  
**READY FOR RUNTIME INTEGRATION:** NO

> **CRITICAL:** This is a plan document only.  
> The dry run described here has NOT been executed.  
> No bridge.py, conductor.py, or runtime file is changed by this document.  
> Execution requires explicit T2 approval AND all prerequisite implementations listed in Section 14.

---

## 1. SYSTEM STATE

| Item | Status |
|------|--------|
| Bridge Room prototypes #1–#8 | ALL PASS — sandbox only, CLOSED |
| T2 design package | COMPLETE — 6 documents written and pushed |
| T2 approval | NOT GRANTED |
| conductor.py Bridge Room mode | NOT IMPLEMENTED |
| bridge.py `token_safe_stop` status | NOT IMPLEMENTED |
| bridge/task-format.md new fields | NOT UPDATED |
| plans/execution-packs/ directory | NOT CREATED |
| Session registry / pack registry | NOT CREATED |
| Test Execution Pack YAML | NOT CREATED |
| Dry run execution | NOT STARTED |
| Production files | UNTOUCHED — no change authorized |

---

## 2. Purpose

The T2 design package defines how conductor.py, bridge.py, and Bridge Room integrate. Before any real production execution is attempted, a controlled dry run must verify that:

1. The design is implementable (no gaps or contradictions)
2. The integration works end-to-end in an isolated test environment
3. All safety mechanisms function correctly (TOKEN_SAFE_STOP, rollback, verdict routing)
4. Session separation simulation is adequate for the first integration
5. No production file, Shopify resource, or Telegram channel is affected

This plan defines the exact test scenario, pass/fail criteria, and approval gates. It does not execute anything.

---

## 3. What Will Be Tested

### 3a. Core Flow

| # | Test | What It Verifies |
|---|------|-----------------|
| T1 | Pack ingestion | conductor.py reads Execution Pack YAML in Bridge Room mode, validates all required fields |
| T2 | Stage dispatch | conductor.py translates STAGE-01 to bridge task, writes bridge/next-task.md with ROOM_ID/PACK_ID/STAGE_ID fields |
| T3 | Bridge pickup | bridge.py detects next-task.md, sets status = "running", executes Claude task |
| T4 | Output ingestion | conductor.py reads bridge/last-result.md, parses BRIDGE_ROOM_OUTPUT_START block, writes inbox/ |
| T5 | Verdict signaling | conductor.py updates room-state.json: stage_status = AWAITING_VERDICT |
| T6 | Verdict polling | conductor.py polls verdicts/, detects verdict file, routes correctly |
| T7 | PASS routing | Full AUDIT → FIX → RETEST loop reaches PACK_COMPLETE |
| T8 | Journal events | All required EVT_* events logged in journal/ |
| T9 | Pack registry | pack-registry.json updated on PACK_COMPLETE |

### 3b. Error Path Tests

| # | Test | What It Verifies |
|---|------|-----------------|
| E1 | FAIL routing | Codex writes FAIL verdict → conductor.py halts pack correctly |
| E2 | ERROR + rollback | Injected FIX error → ROLLBACK stage dispatched → ROLLBACK_PASS → RETEST |
| E3 | Snapshot pre-write | Snapshot confirmed before FIX → rollback possible after intentional ERROR |
| E4 | Pre-dispatch validation | Malformed task YAML → conductor.py rejects before writing next-task.md |

### 3c. TOKEN_SAFE_STOP Test

| # | Test | What It Verifies |
|---|------|-----------------|
| S1 | Claude self-stop | Test task instructs Claude to emit TOKEN_SAFE_STOP_START block in stdout |
| S2 | bridge.py detection | bridge/status.md set to "token_safe_stop" |
| S3 | conductor.py ingestion | 18-field validation passes, safe-stop-state.json written |
| S4 | Pack halted | room-state.json: pack_status = TOKEN_SAFE_STOP |
| S5 | Resume authorization | Manual resume authorization file written → conductor.py resumes |

---

## 4. What Will NOT Be Tested

| Item | Why Excluded | When Covered |
|------|-------------|-------------|
| Shopify write targets | T3 scope only — no production writes | Future T3 dry run |
| Telegram decision relay | Telegram Decision Adapter not yet implemented | After adapter T2 implementation |
| Real Codex/Claude session separation | First dry run uses same session for both roles | Future T2 session-separation test |
| Pack chaining (A→B) | Adds complexity not needed for first dry run | After single-pack dry run passes |
| Multi-room routing (BRM-002) | Not designed | Future design |
| github-bridge.py | Out of scope for Bridge Room integration | Separate design |
| Multi-agent parallel flows | Not designed | Future design |
| Production bridge.py tasks | Dry run uses isolated test environment | After full T2 integration approval |

---

## 5. Test Environment

### 5a. Isolation Requirements

- **Machine:** Local development machine only — no staging or production server
- **Branch:** A new Git branch `bridge-room-dry-run-001` created from main for all dry run changes
- **Bridge scope:** bridge.py is active in test mode — only dry run TASK_IDs (prefix `brm-DRY-`) are processed
- **Room scope:** BRM-001 only — existing sandbox directory
- **Target files:** New mock files created specifically for the dry run (not any existing project file)
- **Registry files:** New session-registry.json and pack-registry.json created in dry-run branch only

### 5b. Environment Verification Before Run

Before any step is executed, verify:

```
1. git status → on branch bridge-room-dry-run-001 (not main)
2. bridge/status.md = "idle"
3. No active bridge.py tasks (check bridge/next-task.md TASK_ID — must not be a live task)
4. Sandbox directory exists: docs/management/bridge-room-prototype/
5. No RUNNING sessions in session-registry.json
6. Telegram bot NOT connected to Bridge Room (conductor-notify.md does not route Bridge Room events)
7. Shopify API NOT reachable in dry-run mode (config isolated or conductor Bridge Room mode has Shopify disabled)
```

### 5c. Test Pack Identity

```
Pack ID:      EXEC-DRY-RUN-001
Room ID:      BRM-001
Session ID:   SES-DRY-RUN-001 (hardcoded for dry run traceability)
YAML path:    plans/execution-packs/exec-dry-run-001.yaml
Target:       docs/management/bridge-room-prototype/dry-run-target.md  (new mock file)
```

---

## 6. Files Allowed During Dry Run

The dry run may touch ONLY the following files:

| File | Action | Purpose |
|------|--------|---------|
| `bridge/next-task.md` | WRITE | Conductor dispatches stage task |
| `bridge/last-result.md` | READ | Conductor ingests output |
| `bridge/status.md` | READ | Conductor polls bridge state |
| `bridge/conductor-state.md` | WRITE | Conductor checkpoints |
| `docs/management/bridge-room-prototype/outbox/*.json` | WRITE | Stage commands |
| `docs/management/bridge-room-prototype/inbox/*.json` | WRITE | Stage outputs |
| `docs/management/bridge-room-prototype/inbox/snapshots/*.bak` | WRITE | Pre-fix snapshots |
| `docs/management/bridge-room-prototype/verdicts/*.json` | WRITE (Codex role only) | Stage verdicts |
| `docs/management/bridge-room-prototype/reports/*.json` | WRITE | Final report, safe-stop |
| `docs/management/bridge-room-prototype/journal/*.jsonl` | WRITE | Event log |
| `docs/management/bridge-room-prototype/room-state.json` | WRITE | Room state machine |
| `docs/management/bridge-room-prototype/dry-run-target.md` | WRITE (FIX stage only) | Test target |
| `docs/management/bridge-room-session-registry.json` | WRITE | Session tracking |
| `docs/management/bridge-room-pack-registry.json` | WRITE | Pack tracking |
| `plans/execution-packs/exec-dry-run-001.yaml` | READ | Pack definition |

### 6a. New Files to Be Created Before Run

These files do not exist yet and must be created as part of dry run setup (T2 implementation phase):

```
plans/execution-packs/exec-dry-run-001.yaml         — Execution Pack YAML for dry run
docs/management/bridge-room-prototype/dry-run-target.md  — Mock target file with intentional defect
docs/management/bridge-room-session-registry.json   — Empty registry, initialized
docs/management/bridge-room-pack-registry.json       — Empty registry, initialized
```

---

## 7. Files Forbidden During Dry Run

| File / Pattern | Reason |
|---------------|--------|
| `BABYMANIA-MASTER-PROMPT.md` | Out of scope |
| `config.yaml` | T3 required |
| `bridge.py` (source) | Implementation was approved T2, but source not modified during run |
| `bridge/github-bridge.py` | Out of scope |
| `scripts/**` | Out of scope |
| `teams/**` (except conductor.py invocation) | Out of scope |
| `output/**` | Out of scope |
| Any Shopify API endpoint | T3 required |
| Any Telegram message send | Telegram relay not implemented |
| Any file in `docs/management/bridge-room-prototype/` OTHER than those listed in Section 6 | Scope discipline |
| Any existing bridge TASK_ID (non-`brm-DRY-` prefix) | Must not interfere with live tasks |
| `main` branch | All dry run changes on `bridge-room-dry-run-001` branch |

---

## 8. Execution Method

### 8a. Session Roles (First Dry Run)

The first dry run uses the same Claude Code session to play both Codex and Claude roles (identical to sandbox prototypes P1–P8). Real session separation is NOT tested in this dry run.

**Role assignment:**
- **Claude role:** Executes stage tasks (via bridge.py as normal)
- **Codex role:** Writes verdicts to `verdicts/` manually within the same session

This is acknowledged as a simulation. Verdict authority enforcement (Codex only writes verdicts) is enforced by discipline in the first dry run, not by access control. Real access-control enforcement is a T2 session-separation test (future).

### 8b. Step-by-Step Execution Plan

Each step requires manual confirmation before proceeding. No autonomous multi-step execution.

**PHASE 0 — Environment Setup (before run starts):**

```
Step 0.1: Create branch bridge-room-dry-run-001
Step 0.2: Create plans/execution-packs/exec-dry-run-001.yaml (see Section 9)
Step 0.3: Create docs/management/bridge-room-prototype/dry-run-target.md with intentional defect
Step 0.4: Initialize empty session-registry.json and pack-registry.json
Step 0.5: Verify bridge/status.md = "idle"
Step 0.6: Run environment verification checklist (Section 5b)
CHECKPOINT: Human confirms all 6 pre-conditions met → proceed
```

**PHASE 1 — Pack Ingestion (T1 test):**

```
Step 1.1: Run: conductor.py --mode bridge-room --pack plans/execution-packs/exec-dry-run-001.yaml
Step 1.2: Verify: session-registry.json updated with SES-DRY-RUN-001
Step 1.3: Verify: room-state.json: pack_status = RUNNING, current_stage = STAGE-01
Step 1.4: Verify: journal: EVT_PACK_START recorded
CHECKPOINT: Human confirms registry + state match → proceed
```

**PHASE 2 — STAGE-01: AUDIT (T2, T3, T4, T5 tests):**

```
Step 2.1: Verify: outbox/EXEC-DRY-RUN-001-STAGE-01-command.json written
Step 2.2: Verify: bridge/next-task.md contains TASK_ID=brm-DRY-RUN-001-STAGE-01-*,
          ROOM_ID=BRM-001, PACK_ID=EXEC-DRY-RUN-001, STAGE_ID=STAGE-01
Step 2.3: Verify: bridge/status.md changes idle → running → done
Step 2.4: Verify: bridge/last-result.md contains BRIDGE_ROOM_OUTPUT_START block
Step 2.5: Verify: inbox/EXEC-DRY-RUN-001-STAGE-01-output.json written
Step 2.6: Verify: room-state.json: stage_status = AWAITING_VERDICT
Step 2.7: Verify: journal: EVT_STAGE_DISPATCH_CONFIRMED, EVT_OUTPUT_WRITTEN, EVT_AWAITING_VERDICT
CHECKPOINT: Human confirms all 7 checks → write Codex verdict
Step 2.8: [Codex role] Write verdicts/EXEC-DRY-RUN-001-STAGE-01-verdict.json: verdict = PASS
Step 2.9: Verify: conductor.py routes to STAGE-02 (FIX)
Step 2.10: Verify: journal: EVT_STAGE_PASS
```

**PHASE 3 — STAGE-02: FIX with Snapshot (T7, E3 tests):**

```
Step 3.1: Verify: outbox/EXEC-DRY-RUN-001-STAGE-02-command.json written
Step 3.2: Verify: bridge/next-task.md STAGE_ID=STAGE-02
Step 3.3: Verify: bridge.py executes — Claude writes snapshot first
Step 3.4: Verify: inbox/snapshots/pre-fix-dry-run-target-DRY-RUN.md.bak exists
Step 3.5: Verify: FIX output confirms snapshot_confirmed = true
Step 3.6: Verify: dry-run-target.md updated with fix
CHECKPOINT: Human confirms snapshot confirmed → write verdict
Step 3.7: [Codex role] Write verdicts/EXEC-DRY-RUN-001-STAGE-02-verdict.json: verdict = PASS
Step 3.8: Verify: conductor.py routes to STAGE-03 (RETEST)
```

**PHASE 4 — STAGE-03: RETEST (T7 continued):**

```
Step 4.1: Verify: RETEST command written, bridge executes
Step 4.2: Verify: RETEST output confirms fix applied in dry-run-target.md
Step 4.3: Verify: reports/EXEC-DRY-RUN-001-final-report.json written by Claude in stdout
CHECKPOINT: Human confirms final report → write verdict
Step 4.4: [Codex role] Write verdicts/EXEC-DRY-RUN-001-STAGE-03-verdict.json: verdict = PACK_PASS
Step 4.5: Verify: room-state.json: pack_status = PACK_COMPLETE
Step 4.6: Verify: pack-registry.json updated
Step 4.7: Verify: journal: EVT_PACK_COMPLETE
CHECKPOINT: Core flow test PASS confirmed by human
```

**PHASE 5 — ERROR + ROLLBACK Test (E1, E2, E3):**

```
Create second test pack: EXEC-DRY-RUN-002 (3 stages, intentional FIX error)
Step 5.1: Run pack ingestion for EXEC-DRY-RUN-002
Step 5.2: STAGE-01 AUDIT → PASS → route to STAGE-02
Step 5.3: STAGE-02 FIX — Claude writes intentionally malformed output (simulating ERROR)
Step 5.4: Verify: snapshot was written BEFORE the error
Step 5.5: [Codex role] Write verdict: verdict = ROLLBACK_REQUIRED, rollback_targets = [TGT-DRY-02]
Step 5.6: Verify: conductor.py dispatches ROLLBACK stage
Step 5.7: Verify: snapshot restored to dry-run-target-02.md
Step 5.8: Verify: ROLLBACK_PASS verdict → RETEST follows
Step 5.9: Verify: pack result = PACK_PASS_PARTIAL
CHECKPOINT: Rollback test PASS confirmed
```

**PHASE 6 — TOKEN_SAFE_STOP Test (S1–S5):**

```
Create third test pack: EXEC-DRY-RUN-003 (1 stage that triggers TOKEN_SAFE_STOP)
Step 6.1: Task instructs Claude to emit TOKEN_SAFE_STOP_START block in stdout
Step 6.2: Verify: bridge/status.md = "token_safe_stop"
Step 6.3: Verify: conductor.py reads TOKEN_SAFE_STOP block from last-result.md
Step 6.4: Verify: 18-field validation passes
Step 6.5: Verify: reports/EXEC-DRY-RUN-003-safe-stop-state.json written with all 18 fields + session_id
Step 6.6: Verify: room-state.json: pack_status = TOKEN_SAFE_STOP
Step 6.7: Write resume authorization: inbox/token-safe-stop-resume-EXEC-DRY-RUN-003.json
Step 6.8: Verify: conductor.py validates authorization and resumes from pending_stage
CHECKPOINT: TOKEN_SAFE_STOP test PASS confirmed
```

**PHASE 7 — Post-Run Cleanup:**

```
Step 7.1: Verify dry-run-target.md, dry-run-target-02.md restored to initial state (or documented as changed)
Step 7.2: Verify no files outside Section 6 scope were created or modified
Step 7.3: Run: git diff --name-only to confirm only allowed files changed
Step 7.4: Document all deviations from expected flow (if any)
Step 7.5: Merge dry-run results back to main as documentation only (no runtime changes merged)
```

---

## 9. Test Pack YAML Design (to be created in T2 implementation phase)

### 9a. EXEC-DRY-RUN-001 — Core Flow Pack

```yaml
pack_id: EXEC-DRY-RUN-001
prior_pack_id: null
approval_policy:
  tier: T2
  requires_owner_approval: true
global_rules:
  - "Only touch files in docs/management/bridge-room-prototype/"
  - "Do not touch Shopify, Telegram, or any production system"
stop_conditions:
  - "Any file outside scope is written"
  - "Any Shopify or Telegram call is made"
targets:
  - target_id: TGT-DRY-01
    file: docs/management/bridge-room-prototype/dry-run-target.md
    read_only: false
    expected_fields:
      - name: quality_standard
        expected_value: premium
    checks:
      - field: quality_standard
        must_equal: premium
stages:
  - stage_id: STAGE-01
    type: AUDIT
    task: "Read dry-run-target.md. Check if quality_standard field equals 'premium'. If missing or wrong, report FAIL."
    command_id: CMD-DRY-01
    output_id: OUT-DRY-01
    verdict_id: VRD-DRY-01
    files_allowed:
      - docs/management/bridge-room-prototype/dry-run-target.md
    files_forbidden:
      - bridge.py
      - scripts/**
      - teams/**
    expected_output: "AUDIT result with quality_standard check"
    pass_conditions:
      - "quality_standard field checked"
      - "BRIDGE_ROOM_OUTPUT_START block present"
    fail_conditions:
      - "file not readable"
      - "BRIDGE_ROOM_OUTPUT_START missing"
    next_on_pass: STAGE-02
    next_on_fail: STOP

  - stage_id: STAGE-02
    type: FIX
    task: "Write PRE_FIX_SNAPSHOT first. Then fix dry-run-target.md: set quality_standard to 'premium'. Confirm snapshot_confirmed=true in output."
    command_id: CMD-DRY-02
    output_id: OUT-DRY-02
    verdict_id: VRD-DRY-02
    files_allowed:
      - docs/management/bridge-room-prototype/dry-run-target.md
      - docs/management/bridge-room-prototype/inbox/snapshots/
    files_forbidden:
      - bridge.py
      - scripts/**
    expected_output: "FIX result with snapshot_confirmed=true and fix confirmed"
    pass_conditions:
      - "snapshot_confirmed: true"
      - "dry-run-target.md updated"
    fail_conditions:
      - "snapshot_confirmed: false"
      - "fix not applied"
    next_on_pass: STAGE-03
    next_on_fail: STOP

  - stage_id: STAGE-03
    type: RETEST
    task: "Read dry-run-target.md. Verify quality_standard equals 'premium'. Report PACK_COMPLETE if verified."
    command_id: CMD-DRY-03
    output_id: OUT-DRY-03
    verdict_id: VRD-DRY-03
    files_allowed:
      - docs/management/bridge-room-prototype/dry-run-target.md
      - docs/management/bridge-room-prototype/reports/
    files_forbidden:
      - bridge.py
    expected_output: "RETEST result with verification + PACK_COMPLETE"
    pass_conditions:
      - "quality_standard = premium confirmed"
      - "final-report.json written"
    fail_conditions:
      - "quality_standard still wrong after FIX"
    next_on_pass: DONE
    next_on_fail: STOP

token_safe_stop:
  report_id: SST-DRY-RUN-001
  pack_id: EXEC-DRY-RUN-001
  safe_to_stop: null
  captured_at: null
  current_stage: null
  current_stage_status: null
  pending_stage: null
  files_read: null
  files_written: null
  last_verdict: null
  next_required_action: null
  resume_instruction: null
  risk_level: null
  targets_completed: null
  targets_pending: null
  rollback_state: null
  snapshots_available: null
  prior_pack_id: null
  prior_pack_report: null
  inherited_fixed_targets: null
  inherited_open_issues: null
```

---

## 10. Expected Flow

```
conductor.py --mode bridge-room --pack plans/execution-packs/exec-dry-run-001.yaml
    ↓
Pack ingested → session registered → PACK_START logged
    ↓
STAGE-01 (AUDIT):
  CMD-DRY-01 written to outbox/
  bridge/next-task.md: TASK_ID=brm-DRY-RUN-001-STAGE-01-*, ROOM_ID=BRM-001
  bridge.py: idle → running → done
  Claude: reads dry-run-target.md, reports AUDIT FAIL (quality_standard missing)
  OUT-DRY-01 written to inbox/
  Codex writes VRD-DRY-01: verdict = PASS → route to STAGE-02
    ↓
STAGE-02 (FIX):
  Claude writes PRE_FIX_SNAPSHOT → snapshot_confirmed = true
  Claude writes quality_standard = "premium" to dry-run-target.md
  OUT-DRY-02 written: snapshot_confirmed=true, fix confirmed
  Codex writes VRD-DRY-02: verdict = PASS → route to STAGE-03
    ↓
STAGE-03 (RETEST):
  Claude reads dry-run-target.md: quality_standard = "premium" confirmed
  Claude writes reports/EXEC-DRY-RUN-001-final-report.json
  OUT-DRY-03: PACK_COMPLETE
  Codex writes VRD-DRY-03: verdict = PACK_PASS
    ↓
conductor.py:
  room-state.json: pack_status = PACK_COMPLETE
  pack-registry.json: updated
  journal: EVT_PACK_COMPLETE
```

---

## 11. Success Criteria

All of the following must be true for the dry run to be considered PASS:

| # | Criterion | Verification |
|---|-----------|-------------|
| SC-01 | EXEC-DRY-RUN-001 reaches PACK_COMPLETE | room-state.json: pack_status = PACK_COMPLETE |
| SC-02 | All 3 stage output files exist in inbox/ | ls docs/management/bridge-room-prototype/inbox/ |
| SC-03 | All 3 verdict files exist in verdicts/ | ls docs/management/bridge-room-prototype/verdicts/ |
| SC-04 | final-report.json exists in reports/ | ls docs/management/bridge-room-prototype/reports/ |
| SC-05 | Journal has all required EVT_* events (≥ 12 events) | wc -l journal/*.jsonl |
| SC-06 | bridge/status.md cycled correctly (idle→running→done per stage) | Check bridge/status.md at each checkpoint |
| SC-07 | TASK_IDs all have brm-DRY- prefix | grep TASK_ID bridge/next-task.md |
| SC-08 | No file outside Section 6 scope was written | git diff --name-only |
| SC-09 | pack-registry.json updated with PACK_COMPLETE | Read pack-registry.json |
| SC-10 | ROLLBACK test: ROLLBACK_PASS, RETEST confirms restoration | matches_snapshot = true in RETEST output |
| SC-11 | TOKEN_SAFE_STOP test: safe-stop-state.json has all 18 standard fields + session_id | Count fields |
| SC-12 | TOKEN_SAFE_STOP test: resume successful after authorization | conductor.py continued after resume file written |

---

## 12. Failure Criteria

Any of the following causes an immediate HALT and escalation to human review:

| # | Failure Condition | Severity |
|---|-----------------|---------|
| FC-01 | Any file outside Section 6 scope was written | CRITICAL — stop all activity |
| FC-02 | Any Shopify API call detected | CRITICAL — stop all activity |
| FC-03 | Any Telegram message sent | CRITICAL — stop all activity |
| FC-04 | bridge/status.md stuck in "running" > 300 seconds | HIGH — watchdog should have fired |
| FC-05 | BRIDGE_ROOM_OUTPUT_START block missing from any stage output | HIGH — schema contract broken |
| FC-06 | snapshot_confirmed = false when FIX stage reports PASS | HIGH — rollback would be impossible |
| FC-07 | TOKEN_SAFE_STOP file missing any of the 18 standard fields | HIGH — schema incomplete |
| FC-08 | ROLLBACK failed: matches_snapshot = false | HIGH — data integrity issue |
| FC-09 | Verdict written to verdicts/ by non-Codex role | MEDIUM — authority violation |
| FC-10 | conductor.py resumed from TOKEN_SAFE_STOP without authorization file | CRITICAL — autonomous resume not allowed |
| FC-11 | Pack reached PACK_COMPLETE without RETEST stage completing | HIGH — stage-skip not allowed |

---

## 13. Rollback Plan

If any critical failure (FC-01 to FC-10) occurs during the dry run:

### 13a. Immediate Stop

```
Step R1: Stop conductor.py immediately
Step R2: Set bridge/status.md to "idle" manually if stuck in "running"
Step R3: Do NOT delete any artifacts — preserve for post-mortem
Step R4: Write incident log to: docs/management/bridge-room-prototype/journal/DRY-RUN-INCIDENT-001.md
Step R5: Human reviews all files changed (git diff on dry-run branch)
```

### 13b. File Restoration

```
If dry-run-target.md was corrupted:
  Restore from: inbox/snapshots/pre-fix-dry-run-target-DRY-RUN.md.bak
  Verify restore: compare to original content
  If snapshot also missing: restore from Git (dry-run branch has original in initial commit)

If bridge/next-task.md left in non-idle state:
  Clear bridge/next-task.md content manually
  Set bridge/status.md = "idle"
  Verify bridge.py is not actively executing (check process list)
```

### 13c. Recovery Scope

The dry-run-target.md mock file is the ONLY file that can be corrupted by the dry run. All other files are new (created for the dry run) and can simply be deleted if needed. No existing project file is at risk.

---

## 14. Approval Required Before Run

All of the following must be explicitly granted before the dry run starts:

| # | Required Approval | Status |
|---|------------------|--------|
| A1 | T2 design package reviewed and accepted by project owner (all 6 docs) | NOT DONE |
| A2 | T2 approval explicitly granted for conductor.py changes (Bridge Room mode) | NOT GRANTED |
| A3 | T2 approval explicitly granted for bridge.py changes (token_safe_stop status) | NOT GRANTED |
| A4 | T2 approval explicitly granted for bridge/task-format.md updates | NOT GRANTED |
| A5 | conductor.py Bridge Room mode implemented and unit-tested (not in this plan) | NOT DONE |
| A6 | bridge.py token_safe_stop detection implemented and unit-tested | NOT DONE |
| A7 | plans/execution-packs/exec-dry-run-001.yaml created and validated | NOT DONE |
| A8 | dry-run-target.md mock file created with intentional defect | NOT DONE |
| A9 | Session registry and pack registry initialized (empty) | NOT DONE |
| A10 | branch bridge-room-dry-run-001 created and isolated | NOT DONE |
| A11 | Environment verification checklist passed (Section 5b) | NOT DONE |
| A12 | Human operator available for all manual Codex role steps | NOT CONFIRMED |

**Until all 12 items are satisfied: this dry run does NOT start.**

---

## 15. Implementation Prerequisites (T2 Phase)

Before A5–A9 can be checked off, the following T2 implementations must be completed:

| Implementation | Document | T2 Approval Required |
|---------------|---------|---------------------|
| conductor.py Bridge Room mode | bridge-room-t2-conductor-integration.md | YES |
| bridge.py token_safe_stop status value | bridge-room-t2-token-safe-stop-runtime.md | YES |
| bridge/task-format.md ROOM_ID/PACK_ID/STAGE_ID | bridge-room-t2-runtime-contract.md | YES |
| Output schema BRIDGE_ROOM_OUTPUT_START/END | bridge-room-t2-runtime-contract.md | YES |
| 18-field TOKEN_SAFE_STOP validation in conductor.py | bridge-room-t2-token-safe-stop-runtime.md | YES |
| Rollback stage dispatch in conductor.py | bridge-room-t2-rollback-safety.md | YES |
| Session registry and pack registry files | bridge-room-t2-conductor-integration.md | YES |
| plans/execution-packs/ directory | bridge-room-t2-conductor-integration.md | YES |

---

## 16. Relation to Full T2 Design Package

This controlled dry run tests the following design documents:

| Document | Sections Tested in Dry Run |
|----------|--------------------------|
| bridge-room-t2-bridge-integration.md | Section 5 (dispatch), Section 6 (output ingestion), Section 8 (error) |
| bridge-room-t2-conductor-integration.md | Sections 6–11 (full lifecycle) |
| bridge-room-t2-runtime-contract.md | Section 5 (ID schema), Section 6 (output schema), Section 8 (timeouts) |
| bridge-room-t2-rollback-safety.md | Section 4 (snapshot), Section 5 (partial rollback) |
| bridge-room-t2-token-safe-stop-runtime.md | Sections 4–10 (full TOKEN_SAFE_STOP lifecycle) |
| bridge-room-t2-telegram-relay.md | NOT tested in this dry run — Telegram relay not implemented |

---

## 17. Risks

| Risk | Severity | Description | Mitigation |
|------|----------|-------------|-----------|
| bridge.py picks up dry run task while live task is active | HIGH | brm-DRY- task overwrites a live task in next-task.md | Strict idle check before dispatch; dry run must only run when bridge has been confirmed idle for 5+ minutes |
| conductor.py Bridge Room mode bug writes to wrong directory | HIGH | Output written outside BRM-001 room directory | Pre-run path validation; git diff check at each phase checkpoint |
| session-separation simulation masks real authority violation | MEDIUM | Same session plays Codex + Claude roles — verdicts/ boundary not enforced | Acknowledged limitation; explicitly document in dry-run results; enforce by discipline, not access control |
| dry-run-target.md corrupted without snapshot | HIGH | FIX stage crashes before snapshot is confirmed | Snapshot confirmation gate in conductor.py (abort if snapshot_confirmed = false) |
| bridge.py still running non-dry-run task during dry run | CRITICAL | Collision — live task output overwrites dry run result | Full idle check + TASK_ID brm-DRY- prefix mismatch detection |
| T2 implementation bugs not caught before dry run | HIGH | Implementation diverged from design — dry run tests wrong behavior | Unit tests for conductor.py Bridge Room mode before dry run |
| Human operator unavailable during dry run | MEDIUM | Dry run stalls waiting for Codex verdict | All checkpoints require human confirmation — do not start dry run without dedicated operator time |

---

## 18. READY TO RUN CONTROLLED DRY RUN: NO

**Reason:** All 12 approval items in Section 14 are NOT satisfied. Specifically:
- A2–A4: T2 approval not granted
- A5–A9: T2 implementations not complete
- A10–A11: Test environment not set up

**Condition to change to YES:**
- All 12 items in Section 14 explicitly checked off
- Project owner confirms approval in writing
- Bridge Room dry-run branch created and environment verified

---

## 19. READY FOR RUNTIME INTEGRATION: NO

This document is a plan only. It authorizes no change to any runtime file, no execution of any script, and no connection to any live system.

Runtime integration (production execution against real Shopify targets) remains blocked until:
1. This dry run completes PASS on all success criteria
2. Real Codex/Claude session separation tested (separate design required)
3. T3 Shopify rollback safety document written and approved
4. Explicit T3 approval granted by project owner

---

*Prereq: [bridge-room-runtime-readiness.md](bridge-room-runtime-readiness.md)*  
*T2 design package: bridge-room-t2-bridge-integration.md, bridge-room-t2-conductor-integration.md, bridge-room-t2-telegram-relay.md, bridge-room-t2-runtime-contract.md, bridge-room-t2-rollback-safety.md, bridge-room-t2-token-safe-stop-runtime.md*  
*Sandbox proof: [bridge-room-prototype/PROTOTYPE-CLOSURE.md](bridge-room-prototype/PROTOTYPE-CLOSURE.md)*
