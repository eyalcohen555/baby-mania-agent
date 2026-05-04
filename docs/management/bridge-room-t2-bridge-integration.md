# Bridge Room T2 — bridge.py Integration Design

**TYPE:** Design document — T1 only  
**STATUS:** DRAFT  
**APPROVAL TIER:** T1  
**LAYER:** 1  
**CREATED:** 2026-05-04  
**COVERS BLOCKERS:** #1, #4 from bridge-room-runtime-readiness.md Section 13  
**READY FOR T2 DESIGN REVIEW:** NO — conductor.py integration doc (#2) not yet written  
**READY FOR RUNTIME INTEGRATION:** NO

> **CRITICAL:** This document describes a future design only.  
> No change to bridge.py, bridge/**, or any runtime file is authorized at T1.  
> Every action described here requires a separate T2 approval before execution.

---

## 1. SYSTEM STATE

| Item | Status |
|------|--------|
| Bridge Room prototypes #1–#8 | ALL PASS (sandbox only) |
| bridge.py current state | Operational — single-task executor |
| bridge.py ↔ Bridge Room connection | NOT DESIGNED, NOT CONNECTED |
| next-task.md / last-result.md contract | PROVEN in live system (bridge.py) |
| Bridge Room outbox/inbox contract | PROVEN in sandbox (P1–P8) |
| Interface mapping designed | YES — this document |
| Interface mapping implemented | NO — T2 required |
| Session separation model | DESIGNED (Section 8) — not tested |
| T2 approval for bridge.py changes | NOT GRANTED |
| Runtime integration | BLOCKED |

---

## 2. Why This Document Is Required

`bridge-room-runtime-readiness.md` (Section 13, Blocker #1) identifies:

> "No bridge.py integration design — Required deliverable: T2 design doc: bridge.py interface spec"

The Bridge Room sandbox (P1–P8) proved all command/output/verdict loop mechanics using a
file-based mock. Before any runtime connection can be considered, the interface between the
Bridge Room file protocol and the live bridge.py execution protocol must be explicitly designed.

This document defines that interface — design only. It does not change any file.

---

## 3. What bridge.py Does Today

Based on `bridge/task-format.md` and `bridge/EXECUTION_RULES.md`:

### 3a. Execution Flow

```
bridge.py reads bridge/next-task.md
         ↓
runs: claude.cmd --print --dangerously-skip-permissions "<task>"
         ↓
captures stdout of Claude session
         ↓
writes stdout → bridge/last-result.md
         ↓
updates bridge/status.md
```

### 3b. Task Input Format (bridge/next-task.md)

```
TASK_ID: <YYYY-MM-DD-NNN>
APPROVAL_TIER: <T0 | T1 | T2 | T3>
GOAL: <what to do>
FILES_ALLOWED: <comma-separated>
OUTPUT_REQUIRED: <what Claude must print to stdout>
```

### 3c. Task Output Format (bridge/last-result.md — written by bridge.py)

```
TASK_ID: <same id>
APPROVAL_TIER: <T0 | T1 | T2 | T3>
STATUS: PASS | FAIL | AWAITING_APPROVAL
FILES_UPDATED: <list>
OUTPUT: <description>
ERRORS: <none | description>
```

### 3d. Status File (bridge/status.md)

Managed automatically by bridge.py and github-bridge.py.  
Values: `idle | running | done | error | pushed | awaiting_approval`

### 3e. Key Constraints

- bridge.py is a **single-task executor** — it does not know about multi-stage plans or packs
- Claude writes to files; bridge.py captures stdout only
- `bridge/last-result.md` is managed by bridge.py — Claude must NOT write to it directly
- T3 tasks return `STATUS: AWAITING_APPROVAL` without executing
- conductor.py sits above bridge.py and manages multi-stage orchestration

---

## 4. What Bridge Room Needs from bridge.py

The Bridge Room loop (proven in P1–P8) operates as:

```
Codex writes command → outbox/claude-command.json (or pack stage command)
Claude reads command, executes, writes output → inbox/claude-output.json
Codex reads output, writes verdict → verdicts/pack-Pn-stage-Nn-verdict.json
journal/stage-log.jsonl records full event trace
```

For runtime integration, bridge.py must serve as the **transport layer** that:

| Bridge Room Requirement | bridge.py Capability |
|------------------------|---------------------|
| Deliver a stage command to Claude | Write task to `bridge/next-task.md` |
| Receive Claude's output | Read `bridge/last-result.md` after status = done |
| Know when Claude is executing | Poll `bridge/status.md` for `running` → `done/error` |
| Handle Claude failure | Detect `STATUS: FAIL` or `error` in status.md |
| Enforce T2/T3 approval gates | Pass `APPROVAL_TIER` in task; respect `AWAITING_APPROVAL` |
| Support TOKEN_SAFE_STOP | Detect new status value (design below) |

---

## 5. Command Dispatch Interface — Design Only

### 5a. Problem

In sandbox: Codex writes `outbox/claude-command.json` and Claude reads it directly.  
In runtime: Claude does not poll outbox/ — bridge.py must push the command to Claude via
`bridge/next-task.md`.

### 5b. Proposed Interface

**Who dispatches:** conductor.py (or a Bridge Room controller process — not designed yet).  
**How:**

```
Step 1 — Wait for bridge ready:
  Poll bridge/status.md until value = "idle"
  Timeout if not idle within N seconds → ERROR

Step 2 — Translate Bridge Room command to bridge task:
  Read outbox/<pack-id>-stage-<N>-command.json
  Map fields (see Section 5c)
  Write to bridge/next-task.md

Step 3 — Signal bridge.py:
  bridge.py detects next-task.md changed (file watcher or polling interval)
  bridge.py sets status.md = "running"
  bridge.py executes claude.cmd with task content

Step 4 — Confirm dispatch:
  Poll status.md until "running" — confirms bridge.py picked up the task
  Log EVT dispatch to journal/stage-log.jsonl
```

### 5c. Field Mapping — Bridge Room Command → bridge Task

| Bridge Room Command Field | bridge/next-task.md Field | Notes |
|--------------------------|--------------------------|-------|
| `command_id` | `TASK_ID` | Prefix with `brm-` to distinguish from manual tasks |
| `pack_id` + `stage_id` | embedded in TASK_ID | Format: `brm-<pack_id>-<stage_id>-<ts>` |
| `approval_tier` | `APPROVAL_TIER` | Pass through directly |
| `stage_type` (AUDIT/FIX/RETEST/ISSUE_AUDIT) | `GOAL` prefix | Include stage type in goal string |
| `instruction` | `GOAL` | Main instruction body |
| `files_allowed` | `FILES_ALLOWED` | Pass through |
| `files_forbidden` | `FILES_FORBIDDEN` | Pass through (add to template) |
| `expected_output` | `OUTPUT_REQUIRED` | Pass through |

### 5d. TASK_ID Convention

```
brm-<pack_id>-<stage_id>-<YYYYMMDD-HHmm>
Example: brm-EXEC-PACK-P9-001-STAGE-01-20260601-1400
```

This prevents collision with non-Bridge-Room tasks dispatched through the same bridge.

### 5e. Constraint

- Only one task may be in-flight at a time (bridge.py is single-task)
- If bridge status ≠ idle when dispatch is attempted → dispatcher must wait or abort
- Dispatcher must never overwrite next-task.md while status = running

---

## 6. Output Ingestion Interface — Design Only

### 6a. Problem

In sandbox: Claude writes directly to `inbox/pack-Pn-stage-Nn-output.json`.  
In runtime: Claude's output is captured by bridge.py as stdout → `bridge/last-result.md`.
The Bridge Room inbox must be populated from last-result.md.

### 6b. Proposed Interface

```
Step 1 — Detect completion:
  Poll bridge/status.md until value = "done" or "error"
  Match TASK_ID in last-result.md to the dispatched brm-* task

Step 2 — Validate output:
  Read bridge/last-result.md
  Check: STATUS = PASS | FAIL | AWAITING_APPROVAL
  Check: TASK_ID matches expected brm-* id
  Check: required output fields present (pack-specific schema)

Step 3 — Translate and write to Bridge Room inbox:
  Parse last-result.md OUTPUT field
  Map to Bridge Room output JSON schema (output_id, stage_id, pack_id, etc.)
  Write to inbox/<pack_id>-stage-<N>-output.json

Step 4 — Update room state:
  Update room-state.json: stage_status = AWAITING_VERDICT
  Log EVT output_written to journal/stage-log.jsonl

Step 5 — Notify Codex (verdict pending):
  Mechanism TBD (see Section 7 — session binding)
```

### 6c. stdout Contract Extension

Claude's stdout in runtime Bridge Room tasks must include all standard last-result.md fields
PLUS the Bridge Room output schema fields. The full output block printed to stdout becomes
the authoritative output record.

Example stdout structure (design only):

```
TASK_ID: brm-EXEC-PACK-P9-001-STAGE-01-20260601-1400
APPROVAL_TIER: T1
STATUS: PASS
FILES_UPDATED: inbox/pack-p9-stage-01-output.json
OUTPUT: STAGE_TYPE=AUDIT STAGE_RESULT=CONFIRMED issue_confirmed=true
ERRORS: none
--- BRIDGE_ROOM_OUTPUT_START ---
{
  "output_id": "OUT-P9-001",
  "pack_id": "EXEC-PACK-P9-001",
  "stage_id": "STAGE-01",
  ...
}
--- BRIDGE_ROOM_OUTPUT_END ---
```

The ingestion layer parses the `BRIDGE_ROOM_OUTPUT_START/END` block and writes it to `inbox/`.  
If the block is missing, status = FAIL (malformed output).

### 6d. Constraint

- last-result.md is written by bridge.py — the ingestion layer must only READ it, never write it
- If STATUS = FAIL in last-result.md → Bridge Room stage = ERROR → rollback evaluation begins
- If STATUS = AWAITING_APPROVAL → Bridge Room stage = BLOCKED → Codex must intervene

---

## 7. Session Binding / room_id Mapping

### 7a. Problem

bridge.py currently has no concept of a "Bridge Room" or "room_id". It executes one task at
a time with no room context. When multiple Bridge Room packs are designed (future), there
must be a way to route a task result back to the correct room and pack.

### 7b. Proposed room_id Contract

Every Bridge Room task dispatched through bridge.py must carry a `ROOM_ID` header:

```
TASK_ID: brm-EXEC-PACK-P9-001-STAGE-01-20260601-1400
ROOM_ID: BRM-001
PACK_ID: EXEC-PACK-P9-001
STAGE_ID: STAGE-01
APPROVAL_TIER: T1
GOAL: ...
```

The `ROOM_ID` is an additional field beyond the current bridge task format spec.  
Adding it requires a T2 change to `bridge/task-format.md` (not done at T1).

### 7c. room_id → File Path Mapping

```
ROOM_ID: BRM-001
  → outbox:  docs/management/bridge-room-prototype/outbox/
  → inbox:   docs/management/bridge-room-prototype/inbox/
  → journal: docs/management/bridge-room-prototype/journal/
  → verdicts: docs/management/bridge-room-prototype/verdicts/
  → state:   docs/management/bridge-room-prototype/room-state.json
```

For future multi-room deployment (not designed):
```
ROOM_ID: BRM-002
  → outbox:  docs/management/bridge-room-002/outbox/
  → ...
```

### 7d. Binding Enforcement

- The dispatcher must record the `brm-*` TASK_ID → ROOM_ID mapping in a session registry
  (file-based: `bridge-room-session-registry.json` — design only, not yet specified)
- On ingestion, the registry is looked up by TASK_ID to determine which room's inbox to write
- If TASK_ID not in registry → ingestion aborts with ERROR (not written to any inbox)

### 7e. Single-Room Constraint (Current Design)

At T1, only one Bridge Room exists (BRM-001). Multi-room routing is not designed.  
The session registry is a forward-looking stub. Initial implementation: hardcoded BRM-001.

---

## 8. Error Propagation

### 8a. bridge.py Error Sources

| Error Source | bridge.py Behavior | Bridge Room Impact |
|-------------|-------------------|-------------------|
| Claude session fails to start | status.md = "error" | Stage = ERROR |
| Claude stdout is empty | last-result.md missing or empty | Stage = ERROR |
| Claude returns STATUS: FAIL | last-result.md STATUS = FAIL | Stage = ERROR → rollback evaluation |
| Claude returns STATUS: AWAITING_APPROVAL | last-result.md STATUS = AWAITING_APPROVAL | Stage = BLOCKED |
| bridge.py process crashes | status.md may remain "running" | Detected by watchdog → Stage = TIMEOUT |
| next-task.md malformed | bridge.py behavior undefined | Stage = ERROR (pre-dispatch validation required) |

### 8b. Error Propagation Chain

```
bridge.py error
      ↓
Ingestion layer detects: status.md = "error" OR STATUS: FAIL in last-result.md
      ↓
Write ERROR record to inbox/<pack_id>-stage-<N>-output.json
  { "status": "ERROR", "error_source": "bridge", "bridge_status": "...", ... }
      ↓
Update room-state.json: stage_status = ERROR
      ↓
Log EVT bridge_error to journal/stage-log.jsonl
      ↓
Codex receives ERROR signal → evaluates: rollback required? TOKEN_SAFE_STOP?
      ↓
If rollback required:
  → Restore from PRE_FIX_SNAPSHOT (if FIX stage failed)
  → Write verdict: ROLLBACK_REQUIRED
If not rollback:
  → Write verdict: RETEST or escalate
```

### 8c. Pre-Dispatch Validation (Guard)

Before writing any task to `bridge/next-task.md`, the dispatcher must validate:
- All required fields present in the source command JSON
- `files_allowed` list is non-empty and within approved scope
- `approval_tier` is present and valid
- bridge status = idle

If validation fails → do NOT write to next-task.md → report DISPATCH_ERROR to room state.

---

## 9. Timeout Handling

### 9a. Timeout Types

| Type | Definition | Current Handling |
|------|-----------|-----------------|
| Bridge pickup timeout | bridge.py does not change status from idle within N seconds after task written | Not designed |
| Execution timeout | bridge.py status remains "running" for > M seconds | watchdog.py handles (existing) |
| Output ingestion timeout | status = done but last-result.md not updated within N seconds | Not designed |
| Stage timeout | Bridge Room stage has no verdict within P seconds | Not designed |

### 9b. Proposed Timeout Chain (Design Only)

```
Dispatch timeout (N = TBD, suggested 30s):
  Poll status.md after writing next-task.md
  If still "idle" after N seconds → DISPATCH_TIMEOUT
  → room-state: stage_status = TIMEOUT
  → Do NOT retry automatically — Codex must decide

Execution timeout (M = handled by watchdog.py):
  watchdog.py already monitors bridge.py execution
  If timeout → watchdog kills process, status.md = "error"
  → Bridge Room ingestion detects "error" → propagates as ERROR

Stage timeout (P = TBD, suggested 300s):
  Separate from bridge execution timeout
  Covers the full stage lifecycle: dispatch → execute → ingest → await verdict
  If stage P timeout expires → TOKEN_SAFE_STOP evaluation (Section 10)
```

### 9c. Timeout Values (Not Yet Set)

All timeout values (N, M, P) are TBD. They must be defined in the T2 runtime contract
document (`bridge-room-t2-runtime-contract.md`) — not in this document.

---

## 10. TOKEN_SAFE_STOP Trigger from bridge Failure

### 10a. When TOKEN_SAFE_STOP Is Relevant

TOKEN_SAFE_STOP (18-field schema, proven in P8) is triggered when Claude cannot complete
the current stage due to context window limits. In runtime, bridge.py failures create an
additional trigger path.

### 10b. TOKEN_SAFE_STOP Trigger Conditions from bridge

| Condition | Action |
|-----------|--------|
| bridge.py error during FIX stage | TOKEN_SAFE_STOP if snapshot was already written (safe to stop — rollback available) |
| bridge.py error during AUDIT stage | TOKEN_SAFE_STOP: safe_to_stop = true, no writes pending |
| bridge.py error during RETEST stage | TOKEN_SAFE_STOP: safe_to_stop = true IF all targets verified before crash |
| bridge.py error mid-FIX, no snapshot | TOKEN_SAFE_STOP: safe_to_stop = false, risk_level = HIGH — Codex must inspect manually |
| Stage timeout (P) expires | TOKEN_SAFE_STOP: triggered by stage timeout monitor (not Claude) |

### 10c. runtime TOKEN_SAFE_STOP Writer

In sandbox: Claude writes `reports/pack-Pn-safe-stop-state.json` directly.  
In runtime: If bridge.py crashes before Claude completes, Claude never writes TOKEN_SAFE_STOP.

**Design requirement:** The ingestion/dispatcher layer must be able to write a partial
TOKEN_SAFE_STOP on Claude's behalf when bridge failure is detected:

```json
{
  "report_id": "SST-RUNTIME-BRIDGE-FAIL",
  "pack_id": "...",
  "safe_to_stop": true | false,
  "captured_at": "<timestamp>",
  "current_stage": "...",
  "current_stage_status": "ERROR_BRIDGE_FAILURE",
  "risk_level": "high | medium | none",
  "next_required_action": "CODEX_MANUAL_REVIEW",
  "resume_instruction": "Bridge failure detected. Manual inspection required before resume.",
  ...all 18 fields with known values filled, unknowns = null...
}
```

This is a **system-generated** TOKEN_SAFE_STOP, distinct from a Claude-generated one.
Codex must treat `current_stage_status = ERROR_BRIDGE_FAILURE` as requiring human review
before any resume attempt.

### 10d. New bridge/status.md Value (Design Only)

Current values: `idle | running | done | error | pushed | awaiting_approval`  
Proposed addition: `token_safe_stop`

When bridge.py detects Claude has emitted a TOKEN_SAFE_STOP signal in stdout before completing
the task, bridge.py would set `status.md = "token_safe_stop"` instead of `"done"`.
This allows the ingestion layer to distinguish clean TOKEN_SAFE_STOP from error.

**This requires a T2 change to bridge.py.** Not authorized at T1.

---

## 11. What Must NOT Be Connected Yet

The following are explicitly prohibited at T1 and require separate approvals before any
integration attempt:

| Component | Why Forbidden | Required Before Connecting |
|-----------|--------------|---------------------------|
| `bridge.py` (source file) | T2 required for code changes | T2 approval + this doc reviewed |
| `bridge/next-task.md` (writing from Bridge Room) | Changes bridge live protocol | T2 approval |
| `bridge/last-result.md` (reading from Bridge Room) | Must not interfere with existing live tasks | T2 approval |
| `bridge/status.md` (new status value) | Requires bridge.py code change | T2 approval + bridge.py modification |
| `conductor.py` (dispatch logic) | conductor.py integration not yet designed | conductor.py T2 doc first |
| Telegram relay | Separate T2 doc required | `bridge-room-t2-telegram-relay.md` |
| Shopify writes via Bridge Room pack | T3 required | Full T2 sequence + T3 approval |
| Real Claude session (non-sandbox) | Session separation not tested | Session separation T2 doc |
| `github-bridge.py` | Out of scope for Bridge Room integration | Separate design required |
| `config.yaml` | T3 required for changes | Explicit T3 approval |
| `scripts/**` | Out of scope | No Bridge Room dependency |
| `teams/**` | Out of scope | No Bridge Room dependency |

---

## 12. Risks

| Risk | Severity | Description | Mitigation |
|------|----------|-------------|-----------|
| Task collision | HIGH | Bridge Room task overwrites a live non-BRM task in next-task.md | Strict idle check before dispatch; brm- prefix in TASK_ID; registry validation |
| TASK_ID collision | HIGH | brm- prefix not unique if clock collision | Include pack_id + stage_id + microsecond timestamp |
| last-result.md stale read | HIGH | Ingestion reads previous task's result if TASK_ID match is skipped | Always match TASK_ID before ingesting; abort if mismatch |
| bridge.py not watching for ROOM_ID | MEDIUM | Current bridge.py ignores unknown fields — ROOM_ID silently dropped | Design validation layer before T2 implementation |
| PRE_FIX_SNAPSHOT not written before bridge crash | HIGH | FIX stage crashes before snapshot → no rollback available | Enforce: snapshot must be confirmed WRITTEN before FIX proceeds; never start FIX without snapshot confirmation |
| Token context overflow mid-FIX | HIGH | Claude runs out of context, bridge returns partial output | TOKEN_SAFE_STOP trigger on partial output detection |
| Status.md race condition | MEDIUM | Dispatcher reads "idle" but another process writes task simultaneously | Atomic file write discipline; bridge.py must be only writer |
| Verdict forgery | MEDIUM | Claude writes to verdicts/ directly in runtime (not allowed) | Access control: verdicts/ directory writeable only by Codex/conductor process |
| Session confusion | HIGH | One bridge.py session shared between BRM tasks and non-BRM tasks | Runtime isolation design required (Section 8) |
| Watchdog kills Bridge Room execution | MEDIUM | Stage timeout longer than watchdog threshold | Coordinate watchdog timeout with Bridge Room stage timeout |

---

## 13. T2 Approval Requirements

Before any component of this design may be implemented, all of the following must be satisfied:

| # | Requirement | Status |
|---|-------------|--------|
| 1 | This document reviewed and accepted by project owner | NOT DONE |
| 2 | `bridge-room-t2-conductor-integration.md` written (covers dispatch logic) | NOT WRITTEN |
| 3 | `bridge-room-t2-runtime-contract.md` written (covers TASK_ID schema, timeout values) | NOT WRITTEN |
| 4 | `bridge-room-t2-session-separation.md` written (covered in conductor doc, #2) | NOT WRITTEN |
| 5 | T2 approval explicitly granted for changes to `bridge/task-format.md` | NOT GRANTED |
| 6 | T2 approval explicitly granted for changes to `bridge.py` (new status value, ROOM_ID) | NOT GRANTED |
| 7 | T2 approval explicitly granted for the dispatch/ingestion layer (new code) | NOT GRANTED |
| 8 | Timeout values (N, M, P) agreed and documented in runtime contract | NOT DONE |
| 9 | TASK_ID collision policy agreed | NOT DONE |
| 10 | Verdict authority model agreed (who can write to verdicts/) | NOT DONE |

**Until all 10 items are satisfied: no implementation work begins.**

Implementation Tier for each component (once T2 approved):

| Component | Tier | Notes |
|-----------|------|-------|
| Add ROOM_ID to bridge/task-format.md | T2 | Changes bridge protocol |
| Add token_safe_stop to bridge/status.md values | T2 | Changes bridge.py behavior |
| Dispatch layer (writes to next-task.md) | T2 | New code affecting bridge |
| Ingestion layer (reads last-result.md, writes inbox/) | T2 | New code affecting bridge room |
| Session registry file | T2 | New file in bridge-room scope |
| system-generated TOKEN_SAFE_STOP writer | T2 | New behavior on bridge failure |
| Verdict authority access control | T2 | Process-level enforcement |

---

## 14. READY FOR T2 DESIGN REVIEW: NO

**Reason:** The following prerequisite documents are not yet written:

- `bridge-room-t2-conductor-integration.md` — dispatch logic lives in conductor.py, not bridge.py.
  The dispatch interface designed here (Section 5) is incomplete without the conductor design.
- `bridge-room-t2-runtime-contract.md` — timeout values, TASK_ID schema, and output
  contract completeness depend on the runtime contract spec.

**Condition to change to YES:**
- The two prerequisite docs above are written
- This document is re-reviewed against them for consistency
- No new blockers are identified
- Project owner explicitly confirms T2 review package is complete

---

## 15. READY FOR RUNTIME INTEGRATION: NO

This document is design only. It authorizes no changes to bridge.py, bridge/**, conductor.py,
or any runtime file.

Runtime integration remains blocked until:
1. Full T2 design package complete (6 documents — see `bridge-room-runtime-readiness.md` Section 14)
2. T2 approval explicitly granted for each component
3. All 10 items in Section 13 satisfied
4. Controlled integration test plan approved (not yet designed)

---

*Prereq reading: [bridge-room-runtime-readiness.md](bridge-room-runtime-readiness.md)*  
*Next document: [bridge-room-t2-conductor-integration.md](bridge-room-t2-conductor-integration.md) (not yet written)*  
*Bridge protocol source: [bridge/task-format.md](../bridge/task-format.md)*
