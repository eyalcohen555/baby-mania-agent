# Bridge Room T2 — Execution Pack Runtime Contract

**TYPE:** Design document — T1 only  
**STATUS:** DRAFT  
**APPROVAL TIER:** T1  
**LAYER:** 1  
**CREATED:** 2026-05-04  
**COVERS BLOCKERS:** #5 from bridge-room-runtime-readiness.md Section 13  
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
| Execution Pack v1 schema | PROVEN in sandbox (P5–P8) |
| Execution Pack runtime ownership | NOT DEFINED until this document |
| TASK_ID / ROOM_ID / PACK_ID schema | PARTIALLY DEFINED (bridge-room-t2-bridge-integration.md Section 5d, 7b) |
| Output schema contract | NOT DEFINED until this document |
| Verdict authority model | NOT FORMALLY DEFINED until this document |
| Timeout values | ALL TBD — placeholders in this document |
| Pack registry schema | DESIGNED (bridge-room-t2-conductor-integration.md Section 11e) |
| Runtime contract | NOT COMPLETE until this document |
| T2 approval | NOT GRANTED |
| Runtime integration | BLOCKED |

---

## 2. Why This Document Is Required

`bridge-room-runtime-readiness.md` (Section 13, Blocker #5):
> "Execution Pack runtime contract not defined — Required deliverable: T2 design doc: runtime contract spec"

Section 9 of that document lists what the runtime contract must add beyond the sandbox proof:

| Requirement | Gap |
|------------|-----|
| Pack ingestion ownership | Who reads the YAML |
| Stage trigger | Who issues the first command |
| Output validation | Schema validated before verdict? |
| Verdict authority | Who can write to verdicts/ |
| Pack result propagation | Who writes final-report.json |
| Chain trigger | Who reads prior_pack_id and dispatches next pack |
| Pack registry | Where all packs are indexed |

Additionally, `bridge-room-t2-bridge-integration.md` and `bridge-room-t2-conductor-integration.md` reference this document for timeout values (N, M, P) that must be defined centrally.

This document is the single authoritative source for runtime IDs, schemas, timeout values, and authority boundaries.

---

## 3. Current Sandbox Proof Relevant to This Contract

### 3a. Execution Pack v1 Schema (Proven P5–P8)

The sandbox established the following YAML pack structure:

```yaml
pack_id: EXEC-PACK-P5-001
prior_pack_id: null              # null for first pack; EXEC-PACK-P7-001 for P8
approval_policy: { ... }
global_rules: { ... }
stop_conditions: { ... }
targets:
  - target_id: TGT-P7-01
    file: mock-target-p7-01.md
    read_only: false
    expected_fields: [...]
    checks: [...]
stages:
  - stage_id: STAGE-01
    type: ISSUE_AUDIT | AUDIT | FIX | RETEST
    task: "..."
    command_id: CMD-P8-001
    output_id: OUT-P8-001
    verdict_id: VRD-P8-001
    files_allowed: [...]
    files_forbidden: [...]
    expected_output: "..."
    pass_conditions: [...]
    fail_conditions: [...]
    blocked_conditions: [...]
    next_on_blocked: USER_DECISION
token_safe_stop:
  report_id: SST-...
  ... (18-field schema)
```

### 3b. ID Chains Proven in Sandbox

Every artifact in P5–P8 carries a consistent chain of IDs:
- `pack_id` → present in all artifacts
- `stage_id` → present in all commands, outputs, verdicts
- `command_id` → links outbox/ to inbox/
- `output_id` → links inbox/ to verdicts/
- `verdict_id` → links verdicts/ to journal/

---

## 4. Runtime Ownership Model

### 4a. Component Ownership (Authoritative)

| Component | Owner | Reads | Writes |
|-----------|-------|-------|--------|
| Execution Pack YAML | conductor.py | YES | NO |
| outbox/ command JSON | conductor.py | NO | YES |
| bridge/next-task.md | conductor.py | NO | YES |
| bridge/last-result.md | bridge.py | NO (writes only) | conductor.py reads |
| bridge/status.md | bridge.py | conductor.py reads | bridge.py only |
| inbox/ output JSON | Claude (via bridge.py stdout) | NO | YES |
| verdicts/ verdict JSON | Codex | NO | YES |
| reports/ final-report.json | Claude (stdout in RETEST) + conductor.py | NO | YES |
| reports/ safe-stop-state.json | Claude (stdout) + conductor.py (system-gen) | NO | YES |
| room-state.json | conductor.py | YES | YES |
| journal/ event log | conductor.py | NO | YES |
| session-registry.json | conductor.py | YES | YES |
| pack-registry.json | conductor.py | YES | YES |

### 4b. Who May NOT Write to What

| File/Directory | May NOT Be Written By |
|----------------|----------------------|
| verdicts/ | conductor.py, Claude, bridge.py — Codex only |
| bridge/last-result.md | Claude, conductor.py — bridge.py only |
| bridge/status.md | Claude, conductor.py — bridge.py and watchdog.py only |
| outbox/ | Claude, bridge.py — conductor.py and Codex only |

---

## 5. ID Schema Contract (Authoritative)

### 5a. TASK_ID

```
Format:  brm-<pack_id>-<stage_id>-<YYYYMMDD-HHmm>
Example: brm-EXEC-PACK-P9-001-STAGE-01-20260601-1400
```

Rules:
- Prefix `brm-` distinguishes Bridge Room tasks from conductor plan tasks (`conductor-`)
- `pack_id` must match the `pack_id` field in the Execution Pack YAML exactly
- `stage_id` must match the `stage_id` field in the pack stage definition exactly
- Timestamp is `YYYYMMDD-HHmm` (minute precision) — not seconds, to avoid log noise
- If two tasks are dispatched in the same minute (should not occur in single-task model) → append `-N` suffix

### 5b. ROOM_ID

```
Format:  BRM-<NNN>
Example: BRM-001
```

Rules:
- `NNN` is a zero-padded 3-digit integer
- Current only valid value: `BRM-001`
- Multi-room routing not designed — BRM-002+ requires future T2/T3 design

### 5c. PACK_ID

```
Format:  EXEC-PACK-<descriptor>-<NNN>
Example: EXEC-PACK-P9-001
```

Rules:
- `descriptor` is the pack semantic name (e.g., `P9` for prototype 9, or a domain slug)
- `NNN` is a zero-padded 3-digit sequential number per descriptor
- Must be globally unique across all Bridge Room sessions

### 5d. STAGE_ID

```
Format:  STAGE-<NN>
Example: STAGE-01, STAGE-02, STAGE-03
```

Rules:
- `NN` is a zero-padded 2-digit integer
- Stages are numbered from 01 within each pack
- ROLLBACK stages: `ROLLBACK-<NN>` (e.g., `ROLLBACK-01`)
- RESUME stages (post-BLOCKED): `RESUME-<NN>` (e.g., `RESUME-01`)

### 5e. Supporting ID Formats

| ID Type | Format | Example |
|---------|--------|---------|
| command_id | `CMD-<pack_descriptor>-<NN>` | `CMD-P9-001` |
| output_id | `OUT-<pack_descriptor>-<NN>` | `OUT-P9-001` |
| verdict_id | `VRD-<pack_descriptor>-<NN>` | `VRD-P9-001` |
| snapshot_id | `SNAP-<pack_id>-<NN>` | `SNAP-EXEC-PACK-P9-001-01` |
| escalation_id | `ESC-<pack_descriptor>-<NNN>` | `ESC-P9-001` |
| session_id | `SES-<YYYYMMDD-HHmm>` | `SES-20260601-1400` |
| report_id | `RPT-<pack_descriptor>-<NNN>` | `RPT-P9-001` |
| safe_stop_id | `SST-<pack_descriptor>-<NNN>` | `SST-P9-001` |

---

## 6. Output Schema Contract

### 6a. Claude Stdout Structure in Runtime Bridge Room Tasks

When Claude executes a Bridge Room stage task via bridge.py, its stdout must conform to the following structure. This is the authoritative runtime output schema.

```
TASK_ID: brm-EXEC-PACK-P9-001-STAGE-01-20260601-1400
APPROVAL_TIER: T1
STATUS: PASS | FAIL | AWAITING_APPROVAL
FILES_UPDATED: <comma-separated list, or "none">
OUTPUT: STAGE_TYPE=<type> STAGE_RESULT=<result> <brief summary>
ERRORS: none | <description>
--- BRIDGE_ROOM_OUTPUT_START ---
<JSON block — see Section 6b>
--- BRIDGE_ROOM_OUTPUT_END ---
```

Rules:
- The `BRIDGE_ROOM_OUTPUT_START` / `BRIDGE_ROOM_OUTPUT_END` block is mandatory in all Bridge Room tasks
- If the block is absent → ingestion layer treats the task as FAIL (malformed output)
- All fields between `---` markers must be valid JSON
- The STATUS field before the block is the bridge.py-level status
- The `result` field inside the JSON is the Bridge Room-level result

### 6b. BRIDGE_ROOM_OUTPUT_START JSON Schema

```json
{
  "output_id": "OUT-P9-001",
  "pack_id": "EXEC-PACK-P9-001",
  "stage_id": "STAGE-01",
  "stage_type": "AUDIT | FIX | RETEST | ISSUE_AUDIT | ROLLBACK | RESUME",
  "result": "PASS | FAIL | BLOCKED | ERROR | TOKEN_SAFE_STOP | ROLLBACK_PASS | ROLLBACK_FAIL",
  "targets": [
    {
      "target_id": "TGT-P9-01",
      "file": "path/to/target",
      "status": "PASS | FAIL | BLOCKED | ERROR | UNCHANGED",
      "findings": [],
      "issues_found": [],
      "issues_resolved": []
    }
  ],
  "files_read": [],
  "files_written": [],
  "snapshot_id": null,
  "snapshot_confirmed": false,
  "evidence": {},
  "errors": null,
  "safe_stop_triggered": false
}
```

### 6c. Output Validation Before Verdict

Before conductor.py signals Codex that output is ready for verdict:

1. Validate `BRIDGE_ROOM_OUTPUT_START` block is present and parseable as JSON
2. Validate `output_id` matches `expected output_id` from pack stage definition
3. Validate `pack_id` matches current pack session
4. Validate `stage_id` matches dispatched stage
5. Validate `result` is one of the allowed values
6. If any validation fails → conductor.py writes ERROR to room-state.json, does NOT signal Codex

---

## 7. Verdict Authority Contract

### 7a. Authoritative Rule

**Only Codex may write to `verdicts/`.** This rule is absolute.

| Entity | May Write Verdicts | Enforcement |
|--------|-------------------|-------------|
| Codex | YES | Authorized |
| conductor.py | NO | Must never write to verdicts/ |
| Claude | NO | Claude writes only to inbox/ via bridge.py stdout |
| bridge.py | NO | bridge.py writes only to bridge/ files |

### 7b. Verdict JSON Schema

```json
{
  "verdict_id": "VRD-P9-001",
  "pack_id": "EXEC-PACK-P9-001",
  "stage_id": "STAGE-01",
  "output_id": "OUT-P9-001",
  "verdict": "PASS | FAIL | BLOCKED | RETEST | ROLLBACK_REQUIRED | TOKEN_SAFE_STOP | PACK_PASS | PACK_PASS_PARTIAL | PACK_COMPLETE",
  "verdict_by": "codex",
  "issued_at": "<ISO timestamp>",
  "rollback_required": false,
  "rollback_targets": [],
  "escalation_id": null,
  "decision_spec": null,
  "notes": ""
}
```

### 7c. Verdict Polling Contract

conductor.py polls for verdicts after writing output to inbox/:

```
Poll: verdicts/<pack_id>-<stage_id>-verdict.json
Interval: TBD (suggested: 5 seconds)
Timeout: P seconds (see Section 8)
On file found:
  Validate verdict_id, pack_id, stage_id, output_id all match
  If mismatch on any field → VERDICT_MISMATCH → do NOT route on this verdict → log error
  If match → route per verdict value (Section 8 of conductor integration doc)
```

---

## 8. Timeout Contract

All timeout values are **placeholder values**. They must be reviewed, tested, and confirmed before T2 approval is granted. Values here are design targets only.

### 8a. Timeout Definitions

| Timeout | Symbol | Placeholder Value | Description | Who Enforces |
|---------|--------|-------------------|-------------|-------------|
| Bridge pickup | N | 30 seconds | Time from writing next-task.md to bridge/status.md = "running" | conductor.py |
| Execution | M | 300 seconds | Time from status = "running" to status = "done/error" | watchdog.py (existing) |
| Output ingestion | N₂ | 10 seconds | Time from status = "done" to last-result.md available | conductor.py |
| Verdict | P | 300 seconds | Time from inbox/ output written to verdicts/ verdict written | conductor.py |
| Stage total | S | 660 seconds | Total time from dispatch to verdict (N + M + N₂ + P as upper bound) | conductor.py stage timer |
| Pack total | T | No hard limit (yet) | Total time for all stages in a pack | Not enforced in initial design |
| BLOCKED wait | ∞ | Indefinite | Pack waits in BLOCKED until decision received | None — requires human action |

### 8b. Timeout Action Table

| Timeout | On Expiry | conductor.py Action |
|---------|-----------|---------------------|
| N (bridge pickup) | DISPATCH_TIMEOUT | stage_status = TIMEOUT, HALT, log EVT_DISPATCH_TIMEOUT |
| M (execution) | watchdog kills process | bridge status = "error" → conductor.py detects error path |
| N₂ (output ingestion) | OUTPUT_NOT_AVAILABLE | stage_status = TIMEOUT, HALT, log EVT_OUTPUT_TIMEOUT |
| P (verdict) | TOKEN_SAFE_STOP triggered | System-generated TOKEN_SAFE_STOP (see bridge-room-t2-token-safe-stop-runtime.md) |
| S (stage total) | Stage total exceeded | Log EVT_STAGE_TIMEOUT, evaluate TOKEN_SAFE_STOP |

### 8c. Timeout Review Requirement

Before T2 approval:
- All timeout values must be reviewed against typical bridge.py execution times in this project
- Watchdog.py existing timeout must be checked to ensure it is < M placeholder
- Verdict timeout P must account for human review time (Codex is a human operator)

---

## 9. bridge/task-format.md Extension

### 9a. New Fields Required in next-task.md

Current bridge/task-format.md does not include Bridge Room fields. The following additions are required (T2 approval before adding):

```
TASK_ID: brm-EXEC-PACK-P9-001-STAGE-01-20260601-1400
ROOM_ID: BRM-001
PACK_ID: EXEC-PACK-P9-001
STAGE_ID: STAGE-01
APPROVAL_TIER: T1
GOAL: <stage instruction>
FILES_ALLOWED: <list>
FILES_FORBIDDEN: <list>
OUTPUT_REQUIRED: <expected output description>
```

New fields: `ROOM_ID`, `PACK_ID`, `STAGE_ID`

### 9b. Backward Compatibility

The three new fields are additional — they do not break existing bridge.py behavior.  
Current bridge.py reads `TASK_ID`, `APPROVAL_TIER`, `GOAL`, `FILES_ALLOWED`, `OUTPUT_REQUIRED`.  
Unknown fields are currently ignored by bridge.py.  
Adding `ROOM_ID`, `PACK_ID`, `STAGE_ID` to the spec formalizes what the ingestion layer needs.

**T2 change required:** `bridge/task-format.md` must be updated to document these fields. bridge.py may need to be updated to pass these fields through to stdout (so the ingestion layer can validate from last-result.md).

---

## 10. Pack Registry Schema (Authoritative)

Extends the design from bridge-room-t2-conductor-integration.md Section 11e:

File: `docs/management/bridge-room-pack-registry.json`

```json
{
  "registry_version": "1.0",
  "last_updated": "<ISO timestamp>",
  "packs": {
    "<pack_id>": {
      "pack_id": "<pack_id>",
      "room_id": "BRM-001",
      "pack_yaml": "plans/execution-packs/<pack_id>.yaml",
      "session_id": "SES-<YYYYMMDD-HHmm>",
      "prior_pack_id": null,
      "chain_depth": 0,
      "status": "RUNNING | PACK_COMPLETE | PACK_PASS_PARTIAL | PACK_FAILED | TOKEN_SAFE_STOP | CRITICAL_ROLLBACK_FAILURE",
      "started_at": "<ISO timestamp>",
      "completed_at": "<ISO timestamp or null>",
      "open_issues": [],
      "resolved_issues": [],
      "chained_to": null,
      "final_report": "<path or null>",
      "stages_completed": ["STAGE-01", "STAGE-02"],
      "stages_failed": [],
      "rollback_targets": []
    }
  }
}
```

Rules:
- Pack entries are never deleted — only status is updated
- `chained_to` field links to the follow-up pack_id once a chain is authorized
- conductor.py is the only writer to pack-registry.json

---

## 11. Execution Pack File Layout Contract

### 11a. Directory Structure (Design Only)

```
plans/
  execution-packs/
    <pack_id>.yaml              ← Execution Pack YAML (read by conductor.py)

docs/management/bridge-room-prototype/   ← BRM-001 room directory
  outbox/
    <pack_id>-<stage_id>-command.json
  inbox/
    <pack_id>-<stage_id>-output.json
    user-decision-<escalation_id>.json
    token-safe-stop-resume-<pack_id>.json
    chain-authorization-<pack_id>.json
    snapshots/
      pre-fix-<target_id>-<pack_descriptor>.md.bak
  verdicts/
    <pack_id>-<stage_id>-verdict.json
  reports/
    <pack_id>-final-report.json
    <pack_id>-safe-stop-state.json
  journal/
    <pack_id>-log.jsonl
  room-state.json

docs/management/
  bridge-room-session-registry.json
  bridge-room-pack-registry.json
```

### 11b. File Naming Rules

| File | Format | Notes |
|------|--------|-------|
| Command | `<pack_id>-<stage_id>-command.json` | Use exact pack_id and stage_id from YAML |
| Output | `<pack_id>-<stage_id>-output.json` | Match output_id from stage definition |
| Verdict | `<pack_id>-<stage_id>-verdict.json` | Match verdict_id from stage definition |
| Snapshot | `pre-fix-<target_id>-<pack_descriptor>.md.bak` | Pack descriptor prevents cross-pack collision |
| Final report | `<pack_id>-final-report.json` | One per pack, written at PACK_COMPLETE |
| Safe stop | `<pack_id>-safe-stop-state.json` | One per pack, written on TOKEN_SAFE_STOP |
| Journal | `<pack_id>-log.jsonl` | Append-only, one per pack |

---

## 12. Journal Event Contract

### 12a. Event Schema

All journal events must conform to:

```json
{
  "event_id": "EVT-<NN>",
  "timestamp": "<ISO timestamp>",
  "event_type": "<EVENT_TYPE>",
  "pack_id": "<pack_id>",
  "stage_id": "<stage_id or null>",
  "task_id": "<brm-* task_id or null>",
  "actor": "conductor | codex | claude | bridge | system",
  "summary": "<one-line description>",
  "data": {}
}
```

### 12b. Required Event Types

| Event Type | Actor | Trigger |
|-----------|-------|---------|
| EVT_PACK_START | conductor | Pack ingestion begins |
| EVT_STAGE_COMMAND_WRITTEN | conductor | outbox/ command written |
| EVT_STAGE_DISPATCH_CONFIRMED | conductor | bridge status = "running" |
| EVT_OUTPUT_WRITTEN | conductor | inbox/ output written after ingestion |
| EVT_AWAITING_VERDICT | conductor | Codex signaled to review |
| EVT_VERDICT_RECEIVED | conductor | verdicts/ file read |
| EVT_STAGE_PASS | conductor | verdict = PASS |
| EVT_STAGE_FAIL | conductor | verdict = FAIL |
| EVT_STAGE_BLOCKED | conductor | verdict = BLOCKED |
| EVT_STAGE_ERROR | conductor | verdict = ERROR or bridge error |
| EVT_ROLLBACK_PASS | conductor | ROLLBACK stage completes successfully |
| EVT_ROLLBACK_FAIL | conductor | ROLLBACK stage fails |
| EVT_USER_DECISION_ACCEPTED | conductor | Decision file validated |
| EVT_PACK_COMPLETE | conductor | All stages PASS |
| EVT_PACK_FAILED | conductor | Pack halted on FAIL/STOP |
| EVT_TOKEN_SAFE_STOP | conductor | TOKEN_SAFE_STOP detected |
| EVT_CHAIN_AUTHORIZED | conductor | Codex authorizes chaining |

---

## 13. Interfaces

### 13a. External Interfaces (All T2)

| Interface | From | To | Contract |
|-----------|------|----|---------|
| Bridge task write | conductor.py | bridge/next-task.md | Section 9a (new fields) |
| Bridge result read | conductor.py | bridge/last-result.md | bridge-room-t2-bridge-integration.md Section 6 |
| Bridge status poll | conductor.py | bridge/status.md | Values: idle/running/done/error/token_safe_stop |
| Command write | conductor.py | outbox/ | Section 6b JSON schema |
| Output ingestion | conductor.py | inbox/ | Section 6b JSON schema |
| Verdict poll | conductor.py | verdicts/ | Section 7b |
| Pack YAML read | conductor.py | plans/execution-packs/ | Section 3a |

---

## 14. Risks

| Risk | Severity | Description | Mitigation |
|------|----------|-------------|-----------|
| Timeout values too short | HIGH | bridge.py execution takes longer than N/M/P — false timeouts | Review with actual bridge execution times before T2 implementation |
| Timeout values too long | MEDIUM | Pack hangs for 10+ minutes on a real failure before TOKEN_SAFE_STOP | P = 300s (5 min) should be reasonable for Codex human review |
| ID collision between packs | HIGH | Two packs generate same TASK_ID | Timestamp in TASK_ID + pack_id uniqueness prevents this |
| verdict/ mismatch not detected | HIGH | conductor routes on stale verdict from previous stage | Strict 4-field validation (verdict_id, pack_id, stage_id, output_id) before routing |
| Pack registry out of sync | MEDIUM | conductor crashes after PACK_COMPLETE before writing registry | Registry write is the last step of PACK_COMPLETE — crash safety: re-read room-state.json on restart |
| Output schema drift | MEDIUM | Claude stdout format diverges from contract over time | Schema validation at ingestion (Section 6c) rejects malformed output |

---

## 15. T2 Approval Requirements

| # | Requirement | Status |
|---|-------------|--------|
| 1 | This document reviewed and accepted by project owner | NOT DONE |
| 2 | All timeout placeholder values reviewed and confirmed | NOT DONE |
| 3 | T2 approval for `bridge/task-format.md` updates (ROOM_ID, PACK_ID, STAGE_ID fields) | NOT GRANTED |
| 4 | T2 approval for `plans/execution-packs/` directory creation | NOT GRANTED |
| 5 | T2 approval for `bridge-room-pack-registry.json` creation | NOT GRANTED |
| 6 | T2 approval for `bridge-room-session-registry.json` creation | NOT GRANTED |
| 7 | ID uniqueness enforcement mechanism agreed | NOT DONE |
| 8 | Output schema validation implementation agreed | NOT DONE |

---

## 16. READY FOR T2 DESIGN REVIEW: YES

This document addresses Blocker #5 and provides the central schema contract referenced by all other T2 design documents.

---

## 17. READY FOR RUNTIME INTEGRATION: NO

This document is design only. All schemas, timeout values, and ID formats are proposals until explicitly approved.

---

*Central reference for all Bridge Room T2 design documents.*  
*Prereq: [bridge-room-runtime-readiness.md](bridge-room-runtime-readiness.md)*  
*Depends on: [bridge-room-t2-bridge-integration.md](bridge-room-t2-bridge-integration.md), [bridge-room-t2-conductor-integration.md](bridge-room-t2-conductor-integration.md)*
