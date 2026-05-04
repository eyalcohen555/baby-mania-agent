# Bridge Room — Next Design: Prototype #7
# Multi-File Execution Pack + ERROR Rollback Spec

**STATUS:** DESIGN ONLY — NO RUNTIME, NO BRIDGE, NO TELEGRAM
**APPROVAL TIER:** T1
**LAYER:** 1
**BASED ON:** Prototypes #1–#3, #5–#6 (all PASSED, all CLOSED)
**CREATED:** 2026-05-04
**NEXT STEP:** T1 approval → build Prototype #7 artifacts → sandbox only

---

## SYSTEM STATE

```
Prototypes #1–3, #5–6:  CLOSED / PASSED
Bridge Room V1 schema:  STABLE
Execution Pack v1:      PROVEN (single-file, single-target)
Runtime integration:    NOT APPROVED
Telegram integration:   NOT APPROVED
Next action:            Design Prototype #7 — Multi-File Pack + ERROR Rollback
```

---

## WHAT IS ALREADY PROVEN

| Capability | Proven In | Evidence |
|---|---|---|
| AUDIT → RETEST basic loop | #1 | codex-verdict.json, stage-log.jsonl |
| Role separation: Codex=controller, Claude=executor | #1 | ownership blocks across all artifacts |
| Evidence Schema v1 (10 required fields) | #1–#3, #5–#6 | every output + verdict |
| ID matching across all artifacts (task_id, stage_id, command_id) | #1–#3 | room-state.json id_matching block |
| AUDIT → FIX → RETEST with targeted write | #2 | fix-output.json, mock-target.md state change |
| RETEST is read-only for the target file | #2, #3, #5, #6 | files_forbidden enforcement |
| BLOCKED state semantics (not FAIL, not PASS) | #3, #6 | distinct status, escalation_id |
| Decision lifecycle: BLOCKED → USER_DECISION → RESUME | #3, #6 | 5-ID validation chain |
| Single-use decision enforcement (consumed=false → consumed=true) | #6 | VRD-P6-003 + RETEST check |
| Execution Pack v1 schema (pack-level + per-stage) | #5, #6 | execution-pack.yaml, execution-pack-p6.yaml |
| AUDIT → FIX → RETEST inside single pack | #5 | reports/pack-final-report.json |
| BLOCKED → RESUME inside single pack | #6 | reports/pack-p6-final-report.json |
| TOKEN_SAFE_STOP artifact with 10 required fields | #6 | reports/pack-safe-stop-state.json |
| Scope enforcement: all writes in bridge-room-prototype/** | #1–#3, #5–#6 | safety block in all reports |
| No bridge.py, Telegram, Shopify, git in any prototype | #1–#3, #5–#6 | safety.connected_to_* = false |

---

## GAPS BEFORE RUNTIME INTEGRATION

The following capabilities are **not designed or not proven** and must be resolved before any
runtime integration (T2 approval required for each):

| Gap | Status | Blocking What |
|---|---|---|
| Multi-file target packs | NOT PROTOTYPED | Any real execution task touches multiple files |
| ERROR state handling (not FAIL, not BLOCKED) | NOT DESIGNED | Unexpected write failure has no recovery path |
| Pack-level rollback on ERROR | NOT DESIGNED | No rollback spec → unrecoverable mid-pack error |
| Conditional stage routing (skip clean targets) | NOT DESIGNED | Current pack always runs all stages |
| Persistent decision store | NOT DESIGNED | Mock JSON file only — no durable queue |
| Real user input channel | NOT DESIGNED | Telegram as decision channel not prototyped |
| Pack chaining (output of Pack A feeds Pack B) | NOT DESIGNED | Required for multi-phase real tasks |
| Parallel / multi-agent flows | NOT PROTOTYPED | Single Claude executor only |
| Real Codex/Claude separation across contexts | NOT TESTED | Both roles played in same session |
| Runtime Pack integration (execution-pack.yaml drives bridge.py) | NOT APPROVED | Requires T2 + separate design |

**Prototype #7 addresses gaps 1–3 (multi-file, ERROR, rollback).**
Gaps 4–10 remain out of scope for Prototype #7.

---

## PROPOSED PROTOTYPE #7

### Name
**Multi-File Execution Pack + ERROR Rollback**

### Why This Prototype

Prototypes #5 and #6 proved the Execution Pack schema on a single-target file.
Every real task (e.g., product SEO, hub article QA) involves multiple files.
Without multi-file support and ERROR recovery, the pack schema cannot be trusted
for real execution even in a future sandbox.

Prototype #7 adds exactly two new capabilities:
1. AUDIT across N mock targets (with per-target result tracking)
2. ERROR state path + rollback spec (so a bad FIX can be identified and recovered)

No Telegram, no bridge, no runtime.

### Scenario

```
Pack starts → AUDIT 3 mock targets
  → target-01: FAIL (issues found)
  → target-02: FAIL (issues found)
  → target-03: PASS (clean, skip FIX)

FIX stage → fix target-01 and target-02 only
  → target-01 fix: writes correctly → FIX PASS
  → target-02 fix: writes WRONG content (intentional test) → ERROR

ERROR path → ROLLBACK_REQUIRED
  → Codex issues ROLLBACK command
  → Claude reverts target-02 to pre-fix state
  → Codex issues verdict: ROLLBACK_PASS

RETEST → verify target-01 fixed, target-02 reverted, target-03 unchanged
  → PACK_PASS with partial fix summary
```

### New Capabilities to Prove

| Capability | Description |
|---|---|
| Multi-target AUDIT | AUDIT output contains `targets[]` array with per-target result |
| Selective FIX | FIX stage only touches targets with AUDIT verdict = FAIL |
| ERROR state | Distinct from FAIL and BLOCKED — unexpected write error |
| ROLLBACK_REQUIRED state | Pack holds when FIX produces ERROR |
| Codex ROLLBACK command | New command type: revert target file to pre-fix snapshot |
| Claude ROLLBACK execution | Claude reverts file, writes rollback output to inbox/ |
| ROLLBACK_PASS verdict | Codex confirms revert successful |
| Partial PACK_PASS | Pack can complete with some targets fixed and one rolled back |
| Per-target result table | Final report includes result per target file |
| PRE_FIX_SNAPSHOT | Before FIX, Claude writes a snapshot of the target to a backup artifact |

---

## HOW CODEX DECIDES: PASS / FAIL / BLOCKED / ERROR

```
AUDIT stage:
  PASS     → all targets clean, no issues found
  FAIL     → one or more targets have fixable issues (proceed to FIX)
  BLOCKED  → required field missing from pack brief or target metadata
  ERROR    → cannot read one or more target files

FIX stage:
  PASS     → all targeted files written correctly (verified against schema)
  FAIL     → fix was written but does not resolve the original AUDIT issue
  BLOCKED  → fix requires information not present (user decision needed)
  ERROR    → file written with wrong structure / scope violation detected

RETEST stage:
  PASS     → fixed targets now clean; rolled-back targets match pre-fix state
  FAIL     → fix did not resolve issue (should have been caught at FIX stage)
  BLOCKED  → verdict file from FIX or ROLLBACK missing or unreadable
  ERROR    → target file missing (unexpected deletion)

ROLLBACK stage (new):
  PASS     → target reverted to pre-fix snapshot; no scope drift
  FAIL     → revert incomplete or wrong snapshot applied
  BLOCKED  → pre-fix snapshot file missing
  ERROR    → scope violation during revert attempt
```

**Codex verdict rules (unchanged from v1):**
- Never issue PASS without evidence block
- Never skip a stage
- BLOCKED always requires escalation_id
- ERROR always requires error_type and error_detail fields
- ROLLBACK can only be issued after an ERROR verdict on FIX stage

---

## HOW CLAUDE EXECUTES WITHOUT SCOPE DRIFT

```
Per-stage scope contract (enforced via files_allowed / files_forbidden in pack yaml):

AUDIT:
  read:   mock-target-01.md, mock-target-02.md, mock-target-03.md
  write:  inbox/pack-p7-stage-01-output.json only
  never:  modify any target file

PRE_FIX_SNAPSHOT (new, before FIX):
  read:   mock-target-01.md, mock-target-02.md  (failing targets only)
  write:  inbox/snapshots/pre-fix-target-01.md.bak
          inbox/snapshots/pre-fix-target-02.md.bak
  never:  read target-03 (it passed AUDIT)

FIX:
  read:   mock-target-01.md, mock-target-02.md, pre-fix snapshots
  write:  mock-target-01.md (FIX only), mock-target-02.md (FIX only)
          inbox/pack-p7-stage-02-output.json
  never:  touch target-03, never write outside bridge-room-prototype/**

ROLLBACK:
  read:   inbox/snapshots/pre-fix-target-02.md.bak
  write:  mock-target-02.md (revert to snapshot), inbox/pack-p7-rollback-output.json
  never:  touch target-01 (successfully fixed), never touch target-03

RETEST:
  read:   mock-target-01.md, mock-target-02.md, mock-target-03.md
          inbox/pack-p7-stage-02-output.json
          inbox/pack-p7-rollback-output.json
  write:  inbox/pack-p7-stage-03-output.json only
  never:  modify any target file
```

**Claude scope rules (unchanged from v1):**
- Only writes inbox/ files unless explicitly a FIX or ROLLBACK stage
- Never reads files outside files_allowed list for the current stage
- Never issues its own verdict
- Never modifies the pack yaml
- Never initiates the next stage without receiving a command

---

## TOKEN_SAFE_STOP INTEGRATION

TOKEN_SAFE_STOP from Prototype #6 carries forward with the following additions for #7:

```yaml
token_safe_stop:
  enabled: true
  required_fields:           # same 10 as P6, plus:
    - pack_id
    - current_stage
    - completed_stages
    - pending_stage
    - files_read
    - files_written
    - last_verdict
    - next_required_action
    - resume_instruction
    - risk_level
    # new in P7:
    - targets_completed      # list of target files with per-target final verdict
    - targets_pending        # list of target files not yet retested
    - rollback_state         # null | ROLLBACK_REQUIRED | ROLLBACK_PASS | ROLLBACK_FAIL
    - snapshots_available    # list of .bak files written before FIX

  stop_points:
    - After AUDIT (before any FIX) — safe, no targets modified
    - After FIX PASS on target-01 (before target-02 attempt) — partial, snapshots required
    - After ERROR on target-02 FIX — ROLLBACK_REQUIRED captured in stop state
    - After ROLLBACK_PASS — safe to stop, target-02 reverted
    - After RETEST PASS — safe, full state captured
```

The stop state must capture which targets are dirty (modified, not yet retested) so
any session resuming from a TOKEN_SAFE_STOP can verify file integrity before proceeding.

---

## WHEN TELEGRAM ENTERS THE PICTURE (FUTURE — NOT PROTOTYPE #7)

Telegram integration is NOT part of Prototype #7 and NOT approved. The design
placeholder for future T2 approval is recorded here for completeness only:

```
Future state (T2 required):
  USER_DECISION channel → Telegram (replaces user-decision-mock.json)
  ESCALATION notification → Telegram (replaces manual Codex review)
  PACK_PASS notification → Telegram (summary message to user)

What Prototype #7 does NOT do:
  - No Telegram messages sent
  - No Telegram reads
  - User decision still provided via inbox/user-decision-mock.json (same as #6)
  - BLOCKED escalations still resolved manually (Codex writes resume command)

Future integration point (for T2 design only):
  - inbox/user-decision-mock.json → replaced by telegram-decision-relay.json
    (a real-time write from Telegram bot, not a mock)
  - Escalation ID (ESC-P7-XXX) → sent as Telegram message to user channel
  - User reply in Telegram → parsed into decision JSON by relay agent
  - This relay agent is NOT designed in Prototype #7
```

---

## FILES TO CREATE FOR PROTOTYPE #7

All files must be within `docs/management/bridge-room-prototype/**`.
No new directories outside this path.

### New schema files (Codex writes)

```
docs/management/bridge-room-prototype/
├── execution-pack-p7.yaml          ← Multi-file pack schema, ERROR + ROLLBACK stages
```

### New mock targets (Codex writes initial state)

```
├── mock-target-p7-01.md            ← Broken state: missing required field A
├── mock-target-p7-02.md            ← Broken state: wrong value for field B
├── mock-target-p7-03.md            ← Clean state: all fields present and valid
```

### Command files (Codex writes before each stage)

```
├── outbox/
│   ├── pack-p7-stage-01-command.json     ← AUDIT command
│   ├── pack-p7-stage-02-command.json     ← FIX command (targets 01, 02 only)
│   ├── pack-p7-rollback-command.json     ← ROLLBACK command (target-02 only)
│   └── pack-p7-stage-03-command.json     ← RETEST command
```

### Output files (Claude writes)

```
├── inbox/
│   ├── pack-p7-stage-01-output.json      ← AUDIT result: 3 targets, per-target verdict
│   ├── snapshots/
│   │   ├── pre-fix-target-p7-01.md.bak   ← Snapshot before FIX
│   │   └── pre-fix-target-p7-02.md.bak   ← Snapshot before FIX
│   ├── pack-p7-stage-02-output.json      ← FIX result: target-01 PASS, target-02 ERROR
│   ├── pack-p7-rollback-output.json      ← ROLLBACK result: target-02 reverted
│   └── pack-p7-stage-03-output.json      ← RETEST result: PACK_PASS with partial summary
```

### Verdict files (Codex writes)

```
├── verdicts/
│   ├── pack-p7-stage-01-verdict.json     ← AUDIT verdict (FIX target-01, FIX target-02)
│   ├── pack-p7-stage-02-verdict.json     ← FIX verdict (PASS target-01, ERROR target-02)
│   ├── pack-p7-rollback-verdict.json     ← ROLLBACK verdict (ROLLBACK_PASS target-02)
│   └── pack-p7-stage-03-verdict.json     ← RETEST verdict (PACK_PASS)
```

### Report + journal files (Codex writes)

```
├── reports/
│   ├── pack-p7-final-report.json         ← Per-target results, partial fix summary
│   └── pack-p7-safe-stop-state.json      ← TOKEN_SAFE_STOP with rollback_state field
├── journal/
│   └── execution-pack-p7-log.jsonl       ← Append-only, all events including ROLLBACK
```

**Total new files: ~19**

---

## SAFETY RULES FOR PROTOTYPE #7

```
ALLOWED:
  Read/write within docs/management/bridge-room-prototype/**
  New files in inbox/, outbox/, verdicts/, reports/, journal/
  New mock target files: mock-target-p7-01.md, 02.md, 03.md
  New pack schema: execution-pack-p7.yaml
  Snapshot writes in inbox/snapshots/ (new subdirectory, still inside allowed root)

FORBIDDEN:
  bridge.py — any connection
  bridge/github-bridge.py
  scripts/** — any read or write
  teams/** — any read or write
  Telegram — any send or receive
  Shopify — any read or write
  git add / git commit / git push
  config.yaml — any read or write
  BABYMANIA-MASTER-PROMPT.md
  Any file outside docs/management/bridge-room-prototype/**
  Modifying existing prototype artifacts (#1–#6 files are frozen)
  Running any live Python script
  Connecting to any external API
  Invoking bridge room conductor or watchdog

FROZEN (do not modify):
  All existing prototype artifacts (#1–#6)
  execution-pack.yaml (P5 schema)
  execution-pack-p6.yaml (P6 schema)
  PROTOTYPE-CLOSURE.md
  README.md
  room-state.json (reflects P3 final state — P7 has its own room state in reports)
```

---

## WHAT SUCCESS LOOKS LIKE FOR PROTOTYPE #7

```
STAGE-01 AUDIT:
  target-01: FAIL (missing field A detected)
  target-02: FAIL (wrong value for field B detected)
  target-03: PASS (clean, excluded from FIX)

PRE_FIX_SNAPSHOT:
  inbox/snapshots/pre-fix-target-p7-01.md.bak written
  inbox/snapshots/pre-fix-target-p7-02.md.bak written

STAGE-02 FIX:
  target-01: FIX PASS (field A added correctly)
  target-02: FIX ERROR (wrong structure written intentionally)
  pack-p7-stage-02-verdict.json: status = ERROR for target-02

ROLLBACK:
  Codex issues ROLLBACK command for target-02
  Claude reverts target-02 from .bak snapshot
  pack-p7-rollback-verdict.json: status = ROLLBACK_PASS

STAGE-03 RETEST:
  target-01: RETEST PASS (field A present)
  target-02: RETEST PASS (reverted to pre-fix state, original state confirmed clean)
  target-03: SKIP (was PASS at AUDIT — included in report as UNCHANGED)

PACK_PASS (partial):
  targets_fixed: [target-01]
  targets_rolled_back: [target-02]
  targets_unchanged: [target-03]
  pack_result: PACK_PASS
  note: "Partial fix — target-02 ERROR rolled back, requires follow-up pack"

TOKEN_SAFE_STOP:
  rollback_state: ROLLBACK_PASS
  targets_completed: all 3
  safe_to_stop: true

Safety block in final report:
  bridge_connection: false
  runtime_connection: false
  telegram: false
  shopify_writes: false
  git_operations: false
  outside_scope_files_touched: false
```

---

## SUMMARY FLAGS

```
SYSTEM STATE:                           Prototypes #1–3, #5–6 CLOSED / PUSHED
WHAT IS ALREADY PROVEN:                 See table above — 14 proven capabilities
GAPS BEFORE RUNTIME:                    10 gaps identified, 3 addressed by P7
PROPOSED PROTOTYPE #7:                  Multi-File Pack + ERROR + ROLLBACK
FILES TO CREATE:                        ~19 new files, all in bridge-room-prototype/**
SAFETY RULES:                           No bridge, no runtime, no Telegram, no git
READY TO BUILD PROTOTYPE #7:            YES
READY FOR RUNTIME INTEGRATION:          NO
```
