# Bridge Room T2 — conductor.py Integration Design

**TYPE:** Design document — T1 only  
**STATUS:** DRAFT  
**APPROVAL TIER:** T1  
**LAYER:** 1  
**CREATED:** 2026-05-04  
**COVERS BLOCKERS:** #2, #8 from bridge-room-runtime-readiness.md Section 13  
**READY FOR T2 DESIGN REVIEW:** YES — both prerequisite docs now written (#1 bridge.py + #2 conductor.py)  
**READY FOR RUNTIME INTEGRATION:** NO

> **CRITICAL:** This document describes a future design only.  
> No change to conductor.py, bridge.py, bridge/**, or any runtime file is authorized at T1.  
> Every action described here requires a separate T2 approval before execution.

---

## 1. SYSTEM STATE

| Item | Status |
|------|--------|
| Bridge Room prototypes #1–#8 | ALL PASS (sandbox only) |
| conductor.py current state | Operational — multi-stage plan executor (conductor plan YAML → bridge tasks) |
| conductor.py ↔ Bridge Room connection | NOT DESIGNED, NOT CONNECTED |
| bridge.py integration design | DESIGNED (bridge-room-t2-bridge-integration.md) |
| Execution Pack v1 schema | PROVEN in sandbox (P5–P8) |
| conductor.py as Execution Pack lifecycle owner | PROPOSED — this document |
| Pack ingestion design | YES — this document |
| Stage dispatch design | YES — this document (completes bridge-room-t2-bridge-integration.md Section 5b) |
| Verdict routing design | YES — this document |
| TOKEN_SAFE_STOP handling design | YES — this document |
| Pack chaining trigger design | YES — this document |
| Session registry / pack registry design | YES — this document |
| T2 approval for conductor.py changes | NOT GRANTED |
| Runtime integration | BLOCKED |

---

## 2. Why This Document Is Required

`bridge-room-runtime-readiness.md` (Section 13) identifies two hard blockers this document addresses:

**Blocker #2:** No conductor.py integration design — Required deliverable: T2 design doc: conductor.py interface spec  
**Blocker #8:** No pack registry design — Required deliverable: T2 design doc: pack registry spec

Additionally, `bridge-room-t2-bridge-integration.md` (Section 5b) explicitly states:
> "Who dispatches: conductor.py (or a Bridge Room controller process — not designed yet)."

That document's READY FOR T2 DESIGN REVIEW remains NO precisely because this document does not yet exist.

This document:
1. Establishes conductor.py as the **owner** of the Execution Pack lifecycle in Bridge Room
2. Designs pack ingestion (how conductor.py reads an Execution Pack YAML)
3. Designs stage dispatch (the missing dispatcher piece from bridge-room-t2-bridge-integration.md Section 5)
4. Designs verdict routing: PASS / FAIL / BLOCKED / ERROR
5. Designs TOKEN_SAFE_STOP detection and relay
6. Designs pack chaining trigger with Codex authorization gate
7. Designs session registry and pack registry

This document does NOT change any file. All designs require T2 approval before implementation.

---

## 3. What conductor.py Does Today

Based on `docs/management/conductor-plan-format.md`:

### 3a. Current Execution Flow

```
conductor.py loads plan YAML from plans/<plan-name>.yaml
         ↓
reads plan_id, plan_name, approval_tier, telegram_notify, stages[]
         ↓
for each stage (ordered, following next_on_pass / next_on_fail routing):
    translate stage → bridge task
    write to bridge/next-task.md
    poll bridge/status.md until "done"
    read bridge/last-result.md
    evaluate: PASS / FAIL / LOGIC_YES / LOGIC_NO / AWAITING_APPROVAL
    update conductor-state.md
    route to next stage
         ↓
DONE → PLAN_VERDICT: PASS
STOP → PLAN_VERDICT: FAILED
```

### 3b. Current Plan Format (conductor-plan-format.md)

conductor.py reads plans in YAML format from `plans/<plan-name>.yaml`:

| Field | Purpose |
|-------|---------|
| `plan_id` | Unique plan identifier |
| `plan_name` | Human-readable name |
| `approval_tier` | Plan-level tier (must be >= highest stage tier) |
| `telegram_notify` | Notification policy (start / milestones / done / blocked / questions) |
| `stages[]` | Ordered list of stages |

Each stage must include:

| Field | Purpose |
|-------|---------|
| `id` (STAGE-N) | Unique stage identifier within the plan |
| `type` (AUDIT/FIX/LOGIC/RETEST) | Stage classification |
| `goal` + `action` | Merged instruction to Claude |
| `approval_tier` | Per-stage tier (required — conductor stops if absent) |
| `exit_conditions` / `fail_conditions` | List-type PASS/FAIL criteria |
| `next_on_pass` / `next_on_fail` | Routing (STAGE-X / DONE / STOP / SKIP) |
| `files_allowed` / `files_forbidden` | Scope passed to bridge task |

### 3c. Stage → Bridge Task Translation (Existing)

conductor.py currently maps plan stages to bridge tasks as follows:

| Stage Field | Bridge Task Field | Format |
|-------------|------------------|--------|
| `plan_id` + `stage.id` + timestamp | `TASK_ID` | `conductor-<plan_id>-<stage_id>-<ts>` |
| `stage.goal` + `stage.action` | `GOAL` + `ACTION` | Merged |
| `stage.approval_tier` | `APPROVAL_TIER` | Pass through |
| `stage.files_allowed` | `FILES_ALLOWED` | Pass through |
| `stage.files_forbidden` | `FILES_FORBIDDEN` | Pass through |
| `stage.expected_output` | `EXPECTED` | Pass through |

### 3d. What conductor.py Does NOT Do Today

- Does NOT read Execution Pack YAML (only conductor plan YAML format)
- Does NOT know about Bridge Room file structure (outbox/, inbox/, verdicts/, reports/)
- Does NOT track pack_id, Bridge Room stage IDs, or command/output/verdict ID chains
- Does NOT handle TOKEN_SAFE_STOP artifacts (18-field schema)
- Does NOT manage pack chaining or prior_pack_id resolution
- Does NOT maintain a session registry or pack registry

---

## 4. What Bridge Room Needs from conductor.py

The Bridge Room loop (proven P1–P8) requires a controller that:

| Bridge Room Requirement | conductor.py Must Provide |
|------------------------|--------------------------|
| Read Execution Pack YAML | Pack ingestion (Section 6) |
| Issue stage commands to outbox/ | Stage dispatch loop (Section 7) |
| Translate pack stage → bridge task | Field mapping (Section 7c) |
| Wait for Claude output in inbox/ | Poll via bridge.py interface (bridge-room-t2-bridge-integration.md) |
| Signal Codex that output is ready | Update room-state.json, log journal event |
| Route on PASS / FAIL / BLOCKED / ERROR | Verdict routing (Section 8) |
| Handle TOKEN_SAFE_STOP | TOKEN_SAFE_STOP detection + relay (Section 9) |
| Chain packs (Pack N → Pack N+1) | Pack chaining trigger with Codex gate (Section 10) |
| Maintain TASK_ID → room_id mapping | Session registry (Section 11) |
| Index all pack runs | Pack registry (Section 11e) |

---

## 5. Is conductor.py the Owner of Execution Pack Lifecycle?

**YES — conductor.py is the designated owner of the Execution Pack lifecycle.**

### 5a. Rationale

1. conductor.py already owns multi-stage plan lifecycle: YAML → dispatch → collect → route → done
2. Execution Pack is a multi-stage lifecycle: AUDIT → FIX → RETEST → verdict → chaining
3. The structural pattern is identical — the source format and output destinations differ
4. bridge.py must remain a **single-task executor** — it must not know about packs or room concepts
5. Codex (verdict authority) must not be burdened with dispatch mechanics or bridge polling

### 5b. Authority Model

```
Execution Pack YAML
         ↓ read by
conductor.py (Bridge Room mode)
         ↓ translates stages, issues bridge tasks
bridge.py (single-task executor — unchanged)
         ↓ runs Claude, captures stdout
Claude
         ↓ output ingested via bridge.py stdout → bridge/last-result.md
conductor.py (ingestion layer — per bridge-room-t2-bridge-integration.md Section 6)
         ↓ writes to inbox/, signals Codex
Codex (verdict authority — only entity that writes to verdicts/)
         ↓ writes verdict JSON
conductor.py (reads verdict, routes to next stage, triggers chaining)
```

### 5c. Authority Boundaries

| Entity | Writes To | Must NOT Write To |
|--------|-----------|-------------------|
| conductor.py | outbox/, inbox/ (via ingestion), room-state.json, journal/, session-registry, pack-registry | verdicts/ — Codex authority |
| Claude | inbox/ (via bridge.py stdout capture) | verdicts/, outbox/, room-state.json |
| Codex | verdicts/, outbox/ (commands), room-state.json (verdict phase) | Direct bridge.py interaction |
| bridge.py | bridge/last-result.md, bridge/status.md | inbox/, verdicts/, room-state.json |

---

## 6. Pack Ingestion Design

### 6a. Execution Pack YAML Location

Execution Packs are distinct from conductor plans. Proposed convention (design only):

```
plans/execution-packs/<pack-id>.yaml
Example: plans/execution-packs/exec-pack-p9-001.yaml
```

The format follows the Execution Pack v1 schema proven in P5–P8 — NOT the conductor plan YAML format.  
conductor.py must support a **Bridge Room mode** activated when loading an Execution Pack YAML.

### 6b. Pack Ingestion Trigger

Two entry paths (design only — no implementation authorized):

**Path A — Direct invocation:**
```
conductor.py --mode bridge-room --pack plans/execution-packs/<pack-id>.yaml
```

**Path B — Chaining invocation (authorized by Codex after prior pack completes):**
```
conductor.py --mode bridge-room --pack plans/execution-packs/<pack-id>.yaml \
             --prior-pack <prior-pack-id>
```

### 6c. Ingestion Steps (Design Only)

```
Step 1 — Load and validate Pack YAML:
  Read plans/execution-packs/<pack-id>.yaml
  Validate required fields (Section 6d)
  If validation fails → PACK_INGESTION_ERROR → do not proceed, do not write any file

Step 2 — Resolve room_id:
  Look up active session in session registry (Section 11)
  If first pack for this room → register new session
  If chaining invocation → validate prior_pack_id matches last completed session for this room

Step 3 — Confirm bridge ready:
  Poll bridge/status.md → must be "idle" before pack starts
  If not idle within timeout N → PACK_START_BLOCKED → log and do not proceed
  (Timeout N is TBD — defined in bridge-room-t2-runtime-contract.md)

Step 4 — Log PACK_START:
  Append EVT_PACK_START to journal/<pack_id>-log.jsonl
  Write room-state.json: { pack_status: "RUNNING", pack_id: ..., current_stage: "STAGE-01", ... }

Step 5 — Begin stage dispatch loop (Section 7)
```

### 6d. Execution Pack YAML Required Fields

For Bridge Room mode, conductor.py must read and validate:

| Field | Required | Maps From Sandbox Proof |
|-------|----------|------------------------|
| `pack_id` | YES | EXEC-PACK-P5-001 through P8 |
| `prior_pack_id` | NO (required for chained packs) | Proven P8 (`prior_pack_id: EXEC-PACK-P7-001`) |
| `approval_policy` | YES | P5–P8 |
| `global_rules` | YES | P5–P8 |
| `stop_conditions` | YES | P5–P8 |
| `targets[]` | YES | P5 (1 target), P7 (3 targets), P8 (1 active + 2 read-only) |
| `stages[]` | YES | P5–P8 |
| `token_safe_stop` | YES | 18-field schema proven P8 |

---

## 7. Stage Dispatch Design

### 7a. Bridge Room Stages vs. conductor.py Stages

conductor.py currently dispatches STAGE-N stages from a conductor plan (YAML conductor format).  
In Bridge Room mode, stages come from the Execution Pack: STAGE-01 (ISSUE_AUDIT or AUDIT), STAGE-02 (FIX), STAGE-03 (RETEST), ROLLBACK stages.

The dispatch mechanics are structurally identical — conductor.py translates each stage to a bridge task. The differences:
- Source: Execution Pack YAML (not conductor plan YAML)
- Stage type set: AUDIT / FIX / RETEST / ISSUE_AUDIT / ROLLBACK (not LOGIC)
- Output destination: Bridge Room outbox/ and inbox/ (not just bridge/last-result.md)
- TASK_ID format: `brm-<pack_id>-<stage_id>-<ts>` (not `conductor-<plan_id>-<stage_id>-<ts>`)

### 7b. Stage Dispatch Loop (Design Only)

```
For each stage in execution_pack.stages[]:

  Step 1 — Validate stage:
    Verify required fields: id, type, task, command_id, output_id, verdict_id
    Verify approval_tier is present
    If stage.type == ISSUE_AUDIT → enforce: only valid as STAGE-01 of a chained pack
    If approval_tier == T3 → HALT — write AWAITING_APPROVAL — do not dispatch

  Step 2 — Write command JSON to outbox/:
    Compose command JSON from stage fields
    Write: docs/management/bridge-room-<room_id>/outbox/<pack_id>-<stage_id>-command.json
    Log EVT_STAGE_COMMAND_WRITTEN to journal

  Step 3 — Translate stage → bridge task:
    Apply field mapping (Section 7c)
    Write bridge/next-task.md
    (Follows bridge-room-t2-bridge-integration.md Section 5b Steps 1–4)
    Poll bridge/status.md until "running"
    If not "running" within timeout N → DISPATCH_TIMEOUT (Section 7d)
    Log EVT_STAGE_DISPATCH_CONFIRMED

  Step 4 — Wait for Claude output:
    Poll bridge/status.md until "done" | "error" | "token_safe_stop"
    Match TASK_ID in bridge/last-result.md
    (Execution timeout M handled by watchdog.py — unchanged)

  Step 5 — Ingest output:
    Parse bridge/last-result.md per bridge-room-t2-bridge-integration.md Section 6
    Write: docs/management/bridge-room-<room_id>/inbox/<pack_id>-<stage_id>-output.json
    Log EVT_OUTPUT_WRITTEN

  Step 6 — Signal Codex (verdict pending):
    Update room-state.json: stage_status = "AWAITING_VERDICT"
    Log EVT_AWAITING_VERDICT

  Step 7 — Wait for Codex verdict:
    Poll verdicts/<pack_id>-<stage_id>-verdict.json
    If verdict not written within timeout P → TOKEN_SAFE_STOP evaluation (Section 9)
    On verdict received → route per Section 8

  Step 8 — Route on verdict (Section 8)
```

### 7c. Field Mapping — Execution Pack Stage → Bridge Task

Extends bridge-room-t2-bridge-integration.md Section 5c with conductor.py as the dispatcher:

| Execution Pack Stage Field | bridge/next-task.md Field | Notes |
|--------------------------|--------------------------|-------|
| `pack_id` + `stage_id` + timestamp | `TASK_ID` | Format: `brm-<pack_id>-<stage_id>-<YYYYMMDD-HHmm>` |
| room_id (from session registry) | `ROOM_ID` | Additional field — requires T2 change to bridge/task-format.md |
| `pack_id` | `PACK_ID` | Additional field |
| `stage_id` | `STAGE_ID` | Additional field |
| stage.approval_tier | `APPROVAL_TIER` | Per-stage tier from pack YAML |
| stage.type + stage.instruction | `GOAL` | Stage type prefix + instruction body |
| stage.files_allowed | `FILES_ALLOWED` | Pass through |
| stage.files_forbidden | `FILES_FORBIDDEN` | Pass through |
| stage.expected_output | `OUTPUT_REQUIRED` | Pass through |

### 7d. Dispatch Timeout Handling

Timeout values are TBD — must be defined in `bridge-room-t2-runtime-contract.md`.  
Behavior design:

| Timeout Event | conductor.py Action |
|--------------|---------------------|
| bridge status ≠ "idle" before pack start | PACK_START_BLOCKED — do not write task |
| bridge status ≠ "running" after task written (N seconds) | DISPATCH_TIMEOUT → stage_status = TIMEOUT → HALT |
| bridge stuck in "running" (M seconds) | watchdog.py handles → produces status = "error" |
| Codex verdict not written within P seconds | TOKEN_SAFE_STOP evaluation (Section 9b, Scenario B) |

---

## 8. Verdict Routing Design

### 8a. Verdict Source

In Bridge Room, only Codex writes verdicts. conductor.py reads from:
```
verdicts/<pack_id>-<stage_id>-verdict.json
```

The verdict JSON carries a `verdict` field: one of `PASS | FAIL | BLOCKED | RETEST | ROLLBACK_REQUIRED | TOKEN_SAFE_STOP | PACK_PASS | PACK_PASS_PARTIAL | PACK_COMPLETE`

### 8b. PASS Routing

```
On verdict = PASS (stage-level) or PACK_COMPLETE / PACK_PASS_PARTIAL (pack-level):

  1. Log EVT_STAGE_PASS to journal
  2. Update room-state.json: stage_status = PASS
  3. Determine next stage from pack YAML (next_on_pass)
  4. If next stage exists → return to dispatch loop Step 1 (Section 7b)
  5. If no next stage (pack complete):
       Confirm final-report.json written by Claude in last RETEST stdout
       Update room-state.json: pack_status = PACK_COMPLETE (or PACK_PASS_PARTIAL if partial)
       Append EVT_PACK_COMPLETE to journal
       Update pack registry (Section 11e): status = PACK_COMPLETE, open_issues = [...]
       Evaluate pack chaining (Section 10)
```

### 8c. FAIL Routing

```
On verdict = FAIL:

  1. Log EVT_STAGE_FAIL to journal
  2. Update room-state.json: stage_status = FAIL
  3. Read next_on_fail from pack stage definition
  4. If next_on_fail → STOP:
       Update room-state.json: pack_status = PACK_FAILED
       Append EVT_PACK_FAILED to journal
       Update pack registry: status = PACK_FAILED
       If telegram_notify.blocked → queue Telegram alert (Telegram relay T2 doc required)
       HALT — do not dispatch further stages
  5. If next_on_fail → another stage_id:
       Dispatch that stage (return to Section 7b Step 1)
```

### 8d. BLOCKED Routing

```
On verdict = BLOCKED:

  1. Log EVT_STAGE_BLOCKED to journal
  2. Update room-state.json:
       stage_status = BLOCKED
       pack_status = WAITING_FOR_USER_DECISION
       pending_decision = { escalation_id, decision_spec (from verdict), consumed: false }
  3. HALT — conductor.py stops dispatching

  Resumption path (after user writes decision file):
  4. conductor.py polls inbox/ for user-decision-<escalation_id>.json
  5. On valid decision file detected:
       Validate 5 IDs match: decision_id, pack_id, task_id, command_id, escalation_id
       Validate consumed = false
       Mark consumed = true in decision file
       Log EVT_USER_DECISION_ACCEPTED
       Update room-state.json: pending_decision = null
       Dispatch RESUME stage per next_on_blocked from pack YAML
```

### 8e. ERROR Routing

```
On verdict = ERROR (or bridge failure escalated from bridge-room-t2-bridge-integration.md Section 8):

  1. Log EVT_STAGE_ERROR to journal
  2. Update room-state.json: stage_status = ERROR
  3. Read rollback_required from verdict JSON

  If rollback_required = true:
    3a. Issue ROLLBACK stage command:
          Write outbox/<pack_id>-rollback-command.json
          Dispatch bridge task (rollback instruction)
          Wait for ROLLBACK output → await ROLLBACK verdict
    3b. On ROLLBACK_PASS verdict:
          Log EVT_ROLLBACK_PASS
          Update room-state.json: rollback_status = ROLLBACK_PASS
          Update pack registry: rollback recorded
          Evaluate pack stop_conditions: continue to RETEST, or PACK_FAILED
    3c. On ROLLBACK_FAIL verdict:
          CRITICAL_ERROR state
          Update room-state.json: pack_status = CRITICAL_ROLLBACK_FAILURE
          Log EVT_CRITICAL_ROLLBACK_FAILURE
          HALT — human review required before any further action

  If rollback_required = false:
    4. Log EVT_STAGE_ERROR_NO_ROLLBACK
    5. Evaluate next_on_fail from pack stage
    6. Route accordingly (or HALT if next_on_fail = STOP)
```

---

## 9. TOKEN_SAFE_STOP Handling

### 9a. Token Safe Stop Sources in Runtime

In sandbox (P6–P8): Claude writes TOKEN_SAFE_STOP directly to `reports/<pack_id>-safe-stop-state.json`.  
In runtime, TOKEN_SAFE_STOP arrives via two paths:

| Source | Detection Mechanism |
|--------|-------------------|
| Claude-generated (pre-stop signal in stdout) | bridge/status.md = `"token_safe_stop"` (proposed new status value — requires T2 bridge.py change) |
| System-generated (bridge failure mid-pack) | bridge/status.md = `"error"` during FIX stage + snapshot confirmed written |
| Stage verdict timeout (P seconds elapsed) | conductor.py stage timeout monitor |

### 9b. TOKEN_SAFE_STOP Detection Flow

**Scenario A — Claude emits TOKEN_SAFE_STOP:**

```
bridge.py detects TOKEN_SAFE_STOP signal in Claude stdout
bridge.py sets bridge/status.md = "token_safe_stop" (new value — T2 change required)
  ↓
conductor.py detects status = "token_safe_stop"
conductor.py reads reports/<pack_id>-safe-stop-state.json (written by Claude before stopping)
conductor.py validates 18-field completeness (Section 9c)
If valid:
  Update room-state.json: pack_status = TOKEN_SAFE_STOP
  Append EVT_TOKEN_SAFE_STOP to journal
  Update pack registry: status = TOKEN_SAFE_STOP, safe_to_stop = <value from file>
  HALT — do not dispatch next stage
  Notify Codex (file flag or Telegram relay — Telegram T2 doc required)
```

**Scenario B — Stage verdict timeout (P seconds):**

```
conductor.py stage timeout monitor fires (verdict not written in P seconds)
  ↓
conductor.py generates system TOKEN_SAFE_STOP on Claude's behalf
  (per bridge-room-t2-bridge-integration.md Section 10c design)
  Writes reports/<pack_id>-safe-stop-state.json with:
    known fields filled, unknown fields = null
    current_stage_status = "TOKEN_SAFE_STOP_TIMEOUT"
    safe_to_stop = true (if in AUDIT/RETEST) | evaluated (if in FIX)
    risk_level = "medium" (AUDIT/RETEST) | "high" (FIX without snapshot) | "low" (FIX with snapshot)
  ↓
Update room-state.json: pack_status = TOKEN_SAFE_STOP_TIMEOUT
Append EVT_TOKEN_SAFE_STOP_TIMEOUT to journal
HALT
```

### 9c. 18-Field Completeness Validation

Before accepting a Claude-generated TOKEN_SAFE_STOP as valid, conductor.py must confirm all 18 fields are present (schema proven in P8):

| Field Group | Fields |
|------------|--------|
| Core (10 fields, proven P6) | report_id, pack_id, safe_to_stop, captured_at, current_stage, current_stage_status, pending_stage, files_read, files_written, last_verdict |
| Extended (4 fields, proven P7) | targets_completed, targets_pending, rollback_state, snapshots_available |
| Pack chaining (4 fields, proven P8) | prior_pack_id, prior_pack_report, inherited_fixed_targets, inherited_open_issues |

If any field is missing → conductor.py treats as PARTIAL_TOKEN_SAFE_STOP → logs warning → proceeds as system-generated TOKEN_SAFE_STOP with safe_to_stop = false, risk_level = "high".

### 9d. Resume Protocol (Design Only)

TOKEN_SAFE_STOP resume is NOT autonomous. Codex must authorize:

```
TOKEN_SAFE_STOP state preserved in: reports/<pack_id>-safe-stop-state.json

Resume authorization flow:
  1. Codex reviews TOKEN_SAFE_STOP file (reads safe_to_stop, resume_instruction, risk_level)
  2. Codex writes resume authorization to inbox/:
       inbox/token-safe-stop-resume-<pack_id>.json
       Contains: decision_id, pack_id, session_id, resume_from_stage, authorized_by, timestamp
  3. conductor.py detects resume authorization file
  4. conductor.py validates session_id matches current session
  5. conductor.py reads resume_instruction from TOKEN_SAFE_STOP file
  6. conductor.py reloads pack YAML, skips completed stages, resumes from pending_stage
  7. Log EVT_TOKEN_SAFE_STOP_RESUME_AUTHORIZED
  8. Dispatch pending_stage (return to Section 7b)
```

---

## 10. Pack Chaining Trigger

### 10a. When Pack Chaining Applies

Pack chaining (proven P7→P8) occurs when:
1. Pack N reaches PACK_COMPLETE or PACK_PASS_PARTIAL with `open_issues` in final report
2. A follow-up pack YAML declares `prior_pack_id` matching Pack N's `pack_id`
3. Codex authorizes the chain (never automatic)

### 10b. Pack Chaining Trigger Flow (Design Only)

```
Pack N reaches PACK_COMPLETE:

  Step 1 — Check final report for open issues:
    Read reports/<pack_id>-final-report.json
    Extract open_issues[]
    Update pack registry: pack_N.open_issues = [...]

  Step 2 — Scan for follow-up pack:
    Scan plans/execution-packs/ for YAML where prior_pack_id = <pack_N.pack_id>
    If found → candidate follow-up pack identified
    Update room-state.json: chain_pending = { next_pack_yaml: ..., open_issues: [...] }
    Log EVT_CHAIN_CANDIDATE_FOUND

  Step 3 — Request Codex chaining authorization:
    conductor.py does NOT automatically start the follow-up pack
    conductor.py HALTS and waits for Codex authorization
    Codex reviews open_issues, final report, and candidate follow-up pack

  Step 4 — On Codex authorization:
    Codex writes: inbox/chain-authorization-<pack_N_id>.json
    conductor.py validates authorization (pack_id match, authorized_by, timestamp)
    Log EVT_CHAIN_AUTHORIZED
    Invoke: conductor.py --mode bridge-room --pack <follow-up-pack.yaml> --prior-pack <pack_N_id>

  Step 5 — ISSUE_AUDIT enforcement on chained pack:
    conductor.py validates: chained pack STAGE-01 must be type ISSUE_AUDIT
    If STAGE-01 is NOT ISSUE_AUDIT → PACK_FORMAT_ERROR → do not dispatch
    ISSUE_AUDIT receives as read-only inputs:
      reports/<prior_pack_id>-final-report.json
      Current state of each inherited target file
```

### 10c. Chain Safety Guards

| Guard | Rule |
|-------|------|
| No automatic chaining | All chain triggers require Codex authorization file |
| ISSUE_AUDIT mandatory | First stage of any chained pack must be ISSUE_AUDIT |
| Snapshot lineage isolation | Each chained pack creates new snapshots — P8 snapshot ≠ P7 snapshot |
| Maximum chain depth | TBD — defined in bridge-room-t2-runtime-contract.md (suggested: 3 hops before full re-review) |
| Cross-pack state preservation | conductor.py verifies prior-pack targets are still in expected final state before issuing any new FIX commands |

---

## 11. Session Registry / room_id Coordination

### 11a. Problem

conductor.py needs to:
- Know which Bridge Room directory (BRM-001) a pack's files belong to
- Map each `brm-*` TASK_ID back to the correct room for output ingestion
- Track pack chain history across sessions

Both this document and bridge-room-t2-bridge-integration.md (Section 7d) identify the same gap: a session registry is needed but not yet specified.

### 11b. Session Registry Design (Design Only)

File: `docs/management/bridge-room-session-registry.json`  
(New file — not yet created — requires T2 approval)

```json
{
  "registry_version": "1.0",
  "last_updated": "<ISO timestamp>",
  "active_sessions": [
    {
      "session_id": "SES-<YYYYMMDD-HHmm>",
      "room_id": "BRM-001",
      "pack_id": "EXEC-PACK-P9-001",
      "pack_status": "RUNNING",
      "current_stage": "STAGE-01",
      "started_at": "<ISO timestamp>",
      "prior_pack_id": null,
      "chain_depth": 0,
      "task_id_map": {
        "brm-EXEC-PACK-P9-001-STAGE-01-20260601-1400": "BRM-001"
      }
    }
  ],
  "completed_sessions": [
    {
      "session_id": "SES-20260501-1000",
      "room_id": "BRM-001",
      "pack_id": "EXEC-PACK-P8-001",
      "pack_status": "PACK_COMPLETE",
      "ended_at": "<ISO timestamp>"
    }
  ]
}
```

### 11c. room_id → File Path Convention

Consistent with bridge-room-t2-bridge-integration.md Section 7c:

```
room_id: BRM-001
  → outbox:    docs/management/bridge-room-prototype/outbox/
  → inbox:     docs/management/bridge-room-prototype/inbox/
  → verdicts:  docs/management/bridge-room-prototype/verdicts/
  → reports:   docs/management/bridge-room-prototype/reports/
  → journal:   docs/management/bridge-room-prototype/journal/
  → state:     docs/management/bridge-room-prototype/room-state.json
```

### 11d. Single-Room Constraint (Current Design)

At T1 design stage: only BRM-001 exists. Multi-room routing is not designed.  
Session registry supports BRM-001 only.  
Future multi-room extension requires a separate T2/T3 design document.

### 11e. Pack Registry Design (Addresses Blocker #8)

From bridge-room-runtime-readiness.md Section 13, Blocker #8: "No pack registry design."

File: `docs/management/bridge-room-pack-registry.json`  
(New file — not yet created — requires T2 approval)

Purpose: Persistent index of all packs ever executed in any Bridge Room, their final status, open issues, and chain relationships.

```json
{
  "registry_version": "1.0",
  "last_updated": "<ISO timestamp>",
  "packs": {
    "EXEC-PACK-P7-001": {
      "room_id": "BRM-001",
      "status": "PACK_PASS_PARTIAL",
      "open_issues": ["ISS-P7-002"],
      "chained_to": "EXEC-PACK-P8-001",
      "final_report": "docs/management/bridge-room-prototype/reports/pack-p7-final-report.json",
      "completed_at": "<ISO timestamp>"
    },
    "EXEC-PACK-P8-001": {
      "room_id": "BRM-001",
      "status": "PACK_COMPLETE",
      "prior_pack_id": "EXEC-PACK-P7-001",
      "open_issues": [],
      "final_report": "docs/management/bridge-room-prototype/reports/pack-p8-final-report.json",
      "completed_at": "<ISO timestamp>"
    }
  }
}
```

conductor.py writes to pack registry on: PACK_START, PACK_COMPLETE, PACK_FAILED, TOKEN_SAFE_STOP.  
Codex reads pack registry to evaluate chain authorization.  
Pack registry is append-friendly — completed pack entries are never deleted or overwritten.

---

## 12. Relation to bridge.py Integration Document

This document builds directly on `bridge-room-t2-bridge-integration.md`. Both documents form a pair that together cover the dispatch-to-verdict loop:

| Component | Designed In |
|-----------|------------|
| bridge.py task format (next-task.md fields) | bridge-room-t2-bridge-integration.md Section 3b |
| TASK_ID format (`brm-<pack_id>-<stage_id>-<ts>`) | bridge-room-t2-bridge-integration.md Section 5d |
| Field mapping: Bridge Room command → bridge task | bridge-room-t2-bridge-integration.md Section 5c |
| Output ingestion: last-result.md → inbox/ | bridge-room-t2-bridge-integration.md Section 6 |
| ROOM_ID field addition to bridge task format | bridge-room-t2-bridge-integration.md Section 7b |
| System-generated TOKEN_SAFE_STOP on bridge failure | bridge-room-t2-bridge-integration.md Section 10c |
| Proposed new bridge status value (`token_safe_stop`) | bridge-room-t2-bridge-integration.md Section 10d |
| **conductor.py as the dispatcher (who writes next-task.md)** | **This document Section 5, 7** |
| **Pack ingestion from Execution Pack YAML** | **This document Section 6** |
| **Stage dispatch loop** | **This document Section 7b** |
| **Verdict routing: PASS / FAIL / BLOCKED / ERROR** | **This document Section 8** |
| **TOKEN_SAFE_STOP detection, validation, resume** | **This document Section 9** |
| **Pack chaining trigger with Codex gate** | **This document Section 10** |
| **Session registry and pack registry** | **This document Section 11** |

---

## 13. What Must NOT Be Connected Yet

All of the following are explicitly prohibited at T1 and require separate approvals:

| Component | Why Forbidden | Required Before Connecting |
|-----------|--------------|---------------------------|
| `conductor.py` source file | T2 required for any code changes | T2 approval + this doc reviewed |
| `plans/execution-packs/` directory | New directory, new YAML format | T2 approval |
| `bridge-room-session-registry.json` | New runtime state file | T2 approval |
| `bridge-room-pack-registry.json` | New runtime state file | T2 approval |
| Bridge Room mode flag (`--mode bridge-room`) | New conductor.py entry point | T2 approval + conductor.py modification |
| Writing `bridge/next-task.md` from Bridge Room packs | Changes live bridge protocol | bridge-room-t2-bridge-integration.md + T2 approval |
| `bridge/last-result.md` reading by ingestion layer | Must not interfere with live tasks | T2 approval |
| `bridge/task-format.md` (ROOM_ID, PACK_ID, STAGE_ID fields) | Changes bridge protocol spec | T2 approval |
| `bridge.py` (new `token_safe_stop` status value) | Code change to live system | T2 approval + separate bridge.py modification approval |
| Automatic pack chaining (no Codex gate) | Unreviewed state propagation | Never — Codex gate is mandatory by design |
| Telegram notification from Bridge Room conductor events | Separate T2 doc required | `bridge-room-t2-telegram-relay.md` |
| Multi-room routing (BRM-002+) | Not designed | Future T2/T3 design document |
| Execution Pack against real Shopify targets | T3 required | Full T2 sequence + T3 approval |

---

## 14. Risks

| Risk | Severity | Description | Mitigation |
|------|----------|-------------|-----------|
| conductor.py plan mode / Bridge Room mode confusion | HIGH | Conductor plan YAML loaded in Bridge Room mode (or vice versa) — fields silently misread | Bridge Room mode must be explicit `--mode bridge-room` flag + YAML schema validation on first read |
| Execution Pack YAML schema mismatch | HIGH | Execution Pack fields differ from conductor plan fields — silent parsing failure dispatches wrong task | Strict required-field validation before any dispatch; abort on first missing field |
| Automatic pack chaining without Codex gate | CRITICAL | Follow-up pack starts without Codex review of open_issues — invalid or unresolved state propagated | Chaining requires Codex authorization file — conductor.py must never self-authorize |
| Verdict polling without timeout | HIGH | conductor.py waits indefinitely for Codex verdict — pack hangs with no recovery path | Mandatory verdict timeout P with TOKEN_SAFE_STOP fallback |
| Pack registry corruption | HIGH | Session ends without writing to registry — TASK_ID map lost — ingestion routes output to wrong room | Registry write confirmed before stage marked dispatched; registry write failure = HALT |
| ISSUE_AUDIT skipped on chained pack | HIGH | Follow-up pack starts with AUDIT not ISSUE_AUDIT — inherited issues not confirmed | conductor.py enforces: prior_pack_id present → STAGE-01 must be type ISSUE_AUDIT; format error halts dispatch |
| Resume from stale TOKEN_SAFE_STOP | HIGH | TOKEN_SAFE_STOP from prior session used to resume new session — corrupted context | TOKEN_SAFE_STOP file must carry session_id; conductor.py validates session_id match before accepting resume |
| Verdict forgery via conductor.py auto-generation | MEDIUM | conductor.py auto-generates PASS verdicts to unblock a stuck stage — bypasses Codex authority | conductor.py must never write to verdicts/ — only reads; any auto-verdict attempt = design violation |
| Cross-pack snapshot confusion | MEDIUM | P8 snapshot used as P7 rollback source (or vice versa) | Snapshot file names carry pack_id (SNAP-<pack_id>-xx); conductor.py validates pack_id in snapshot name before accepting |
| conductor.py crash mid-pack | HIGH | Pack state left undefined — bridge may be in "running" | conductor-state.md updated after every step; on restart, conductor.py reads conductor-state.md + room-state.json to recover position |
| TOKEN_SAFE_STOP 18-field completeness not validated | MEDIUM | Partial TOKEN_SAFE_STOP accepted as valid — incomplete resume_instruction used | Strict 18-field count validation before accepting; missing fields → PARTIAL_TOKEN_SAFE_STOP → safe_to_stop forced false |
| Pack chaining depth unbounded | MEDIUM | A→B→C→D→... chain grows without limit — state accumulates without review | Maximum chain depth cap (TBD in runtime-contract.md); at cap → require full Codex re-review before continuing |

---

## 15. T2 Approval Requirements

Before any component of this design may be implemented, all of the following must be satisfied:

| # | Requirement | Status |
|---|-------------|--------|
| 1 | This document reviewed and accepted by project owner | NOT DONE |
| 2 | `bridge-room-t2-bridge-integration.md` reviewed and accepted | NOT DONE |
| 3 | `bridge-room-t2-runtime-contract.md` written (timeout values N/M/P, TASK_ID schema) | NOT WRITTEN |
| 4 | T2 approval explicitly granted for changes to `conductor.py` | NOT GRANTED |
| 5 | T2 approval explicitly granted for new `plans/execution-packs/` directory | NOT GRANTED |
| 6 | T2 approval explicitly granted for `bridge-room-session-registry.json` | NOT GRANTED |
| 7 | T2 approval explicitly granted for `bridge-room-pack-registry.json` | NOT GRANTED |
| 8 | T2 approval for `bridge/task-format.md` changes (ROOM_ID, PACK_ID, STAGE_ID fields) | NOT GRANTED |
| 9 | T2 approval for `bridge.py` changes (new `token_safe_stop` status value) | NOT GRANTED |
| 10 | Pack chaining authorization model agreed and documented | NOT DONE |
| 11 | Verdict authority model agreed: who can write to verdicts/ in runtime | NOT DONE |
| 12 | TOKEN_SAFE_STOP resume authorization protocol agreed (who writes resume file, format) | NOT DONE |
| 13 | conductor.py Bridge Room mode entry point agreed (`--mode` flag vs. separate script) | NOT DONE |

**Until all 13 items are satisfied: no implementation work begins.**

Implementation tier for each component (once T2 approved):

| Component | Tier | Notes |
|-----------|------|-------|
| conductor.py Bridge Room mode (pack ingestion, dispatch loop) | T2 | New code path in core orchestrator |
| `plans/execution-packs/` directory + YAML schema validator | T2 | New directory + new format support |
| bridge-room-session-registry.json | T2 | New runtime state file |
| bridge-room-pack-registry.json | T2 | New runtime state file |
| ROOM_ID / PACK_ID / STAGE_ID fields in bridge/task-format.md | T2 | Protocol spec change |
| New `token_safe_stop` status in bridge.py | T2 | Code change to live bridge |
| System-generated TOKEN_SAFE_STOP writer | T2 | New conductor.py behavior |
| Chain authorization enforcement | T2 | New conductor.py + inbox/ logic |

---

## 16. READY FOR T2 DESIGN REVIEW: YES

**Condition met by this document:**  
Both required prerequisite documents from bridge-room-runtime-readiness.md Section 15 are now written:
- `bridge-room-t2-bridge-integration.md` — bridge.py interface (blockers #1, #4) ✅ written  
- `bridge-room-t2-conductor-integration.md` — conductor.py interface (blockers #2, #8) ✅ this document

bridge-room-runtime-readiness.md Section 15 states:
> "The T2 review can begin only after: this document is reviewed and accepted + at least documents #1 and #2 from the T2 sequence are drafted."

That condition is now met.

**Remaining T2 design package documents (not yet written):**

| Order | Document | Covers Blockers |
|-------|---------|-----------------|
| 3 | `bridge-room-t2-telegram-relay.md` | #3 |
| 4 | `bridge-room-t2-runtime-contract.md` | #5 |
| 5 | `bridge-room-t2-rollback-safety.md` | #6 |
| 6 | `bridge-room-t2-token-safe-stop-runtime.md` | #7 |

**T2 REVIEW PACKAGE COMPLETE:** NO — 4 more documents required before full package review.  
**THIS DOCUMENT READY FOR T2 DESIGN REVIEW:** YES — ready for review by project owner.

**Condition to change bridge-room-t2-bridge-integration.md to YES:**  
- This document reviewed and accepted  
- `bridge-room-t2-runtime-contract.md` also written  
- Both docs re-reviewed for consistency  
- No new blockers identified  
- Project owner explicitly confirms

---

## 17. READY FOR RUNTIME INTEGRATION: NO

This document is design only. It authorizes no changes to conductor.py, bridge.py, bridge/**, or any runtime file.

Runtime integration remains blocked until:
1. Full T2 design package complete (all 6 documents — bridge-room-runtime-readiness.md Section 14)
2. T2 approval explicitly granted for each component in Section 15
3. All 13 items in Section 15 satisfied
4. Controlled integration test plan approved (not yet designed)

---

*Prereq reading: [bridge-room-runtime-readiness.md](bridge-room-runtime-readiness.md)*  
*Companion document: [bridge-room-t2-bridge-integration.md](bridge-room-t2-bridge-integration.md)*  
*Next document: [bridge-room-t2-runtime-contract.md](bridge-room-t2-runtime-contract.md) (not yet written)*  
*conductor.py plan format: [conductor-plan-format.md](conductor-plan-format.md)*  
*Sandbox closure: [bridge-room-prototype/PROTOTYPE-CLOSURE.md](bridge-room-prototype/PROTOTYPE-CLOSURE.md)*
