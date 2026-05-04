# Bridge Room Runtime Readiness

**TYPE:** Design document — T1 only  
**STATUS:** DRAFT  
**APPROVAL TIER:** T1  
**LAYER:** 1  
**CREATED:** 2026-05-04  
**READY FOR T2 DESIGN REVIEW:** NO  
**READY FOR RUNTIME INTEGRATION:** NO

---

## 1. SYSTEM STATE

| Item | Status |
|------|--------|
| Prototypes completed | #1, #2, #3, #5, #6, #7, #8 — ALL PASS |
| Execution Pack v1 schema | PROVEN (P6–P8) |
| Pack chaining | PROVEN (P7→P8) |
| ISSUE_AUDIT stage | PROVEN (P8) |
| Cross-pack state preservation | PROVEN (P8) |
| TOKEN_SAFE_STOP | PROVEN (18 fields, P8) |
| bridge.py integration | NOT DESIGNED |
| conductor.py integration | NOT DESIGNED |
| Telegram relay | NOT APPROVED |
| Shopify writes | NOT APPROVED |
| Real Codex/Claude session separation | NOT TESTED |
| Persistent decision store | NOT DESIGNED |
| T2 approval | NOT GRANTED |
| Runtime integration | BLOCKED |

---

## 2. What Was Proven in Prototypes #1–#8

**Prototypes #1–#3 — Core Bridge Room Loop**
- File-based command/output/verdict cycle (outbox → inbox → verdict)
- Room state machine: WAITING_COMMAND → EXECUTING → AWAITING_VERDICT → VERDICT_ISSUED
- AUDIT → RETEST scenario end-to-end
- journal/stage-log.jsonl append-only event trace
- Codex/Claude role separation (simulated, not real sessions)

**Prototype #5 — Execution Pack v1 Schema**
- pack_id, approval_policy, global_rules, stop_conditions, token_safe_stop
- TARGET definition: file, expected fields, checks
- STAGE definition: task, command, output, verdict IDs
- Decision lifecycle: PASS / RETEST / ROLLBACK / TOKEN_SAFE_STOP

**Prototype #6 — Error State + Rollback**
- ERROR state handling in FIX stage
- PRE_FIX_SNAPSHOT → FIX → RETEST → ROLLBACK if FIX fails
- Snapshot-based rollback (pre-fix-target.md.bak)
- Pack-level rollback: all targets restored on ERROR

**Prototype #7 — Multi-Target Pack + TOKEN_SAFE_STOP Extended**
- 3 targets in one pack (TGT-P7-01, -02, -03)
- Partial-fix scenario: TGT-P7-01 FIXED, TGT-P7-02 ERROR/ROLLED BACK, TGT-P7-03 UNCHANGED
- TOKEN_SAFE_STOP 14-field schema (adds targets_completed, targets_pending, rollback_state, snapshots_available)
- ISS-P7-002 carried forward as open issue

**Prototype #8 — Pack Chaining + ISSUE_AUDIT + 18-Field TOKEN_SAFE_STOP**
- prior_pack_id contract: P8 ingests P7 final report as authoritative input
- ISSUE_AUDIT stage type: mandatory first stage, reads prior report + current file, returns CONFIRMED/RESOLVED/BLOCKED
- Single-target follow-up pack (1 active, 2 read-only cross-pack verification targets)
- Cross-pack RETEST: verifies P8-fixed + P7-fixed + P7-clean targets in one pass
- TOKEN_SAFE_STOP 18 fields: adds prior_pack_id, prior_pack_report, inherited_fixed_targets, inherited_open_issues
- Snapshot lineage separation: P8 snapshot distinct from P7 snapshot
- ISS-P7-002 resolved, open_issues: []

**36 total sandbox capabilities proven across P1–P8.**

---

## 3. Why Prototype #9 Is Not Required

The sandbox series has achieved full coverage of all designed pack patterns:

| Pattern | Proven In |
|---------|-----------|
| Single-stage audit loop | P1–P3 |
| Multi-stage execution pack | P5 |
| ERROR state + rollback | P6 |
| Multi-target pack | P7 |
| TOKEN_SAFE_STOP (full 18-field) | P7–P8 |
| Pack chaining (A→B) | P8 |
| ISSUE_AUDIT stage | P8 |
| Cross-pack state preservation | P8 |
| Open issue carry-forward + resolution | P7→P8 |

No sandbox pattern has been designed that is not already covered. The remaining gaps (multi-hop chaining A→B→C, branching packs, concurrent packs) are NOT designed and are not required before T2 design review.

A Prototype #9 would only be justified if:
- A new sandbox pattern is identified that cannot be derived from existing proofs
- A new stage type is needed that has no analog in P1–P8
- A structural failure is found in the existing schema

None of these conditions are met. **P9 is not required.**

---

## 4. What Is Still Not Ready for Runtime

The following capabilities were explicitly NOT tested in any prototype and remain undesigned:

| Capability | Gap | Blocker Level |
|-----------|-----|---------------|
| bridge.py integration | No design, no interface spec | HARD |
| conductor.py integration | No design | HARD |
| Telegram decision relay | No design, T2 not approved | HARD |
| Real Codex/Claude session separation | Simulated only in prototypes | HARD |
| Persistent decision store | File-based only, no persistence layer design | HARD |
| Shopify writes from pack execution | Not approved | HARD |
| T2 approval | Not granted for any runtime component | HARD |
| Multi-hop pack chaining (A→B→C) | Not designed | SOFT |
| Concurrent pack execution | Not designed | SOFT |
| Pack branching (conditional chains) | Not designed | SOFT |

HARD = must be resolved before any runtime connection.  
SOFT = not required for initial runtime design review.

---

## 5. bridge.py Integration Points (Design Only)

**Current state:** bridge.py exists in the project but is explicitly disconnected from all prototypes. No interface has been designed between the Bridge Room loop and bridge.py.

**Required before T2:**

- **Command dispatch interface:** How does Codex write a command to outbox/ in a way that bridge.py can route it to the correct Claude session? File watcher? Event bus? Direct call?
- **Output ingestion interface:** How does bridge.py deliver Claude's output back to inbox/? Async callback? Polling? Webhook?
- **Session binding:** Which bridge.py session corresponds to which Bridge Room instance? Session ID → room ID mapping required.
- **Error propagation:** If bridge.py loses connection mid-pack, what is the Bridge Room state? How is TOKEN_SAFE_STOP triggered?
- **Timeout handling:** If Claude does not respond within a stage timeout, what does bridge.py report? Who writes the ERROR verdict?

**Design constraint:** bridge.py integration must NOT be prototyped at T1. All integration design requires T2 approval before any file in `scripts/` or `bridge.py` is touched.

---

## 6. conductor.py Integration Points (Design Only)

**Current state:** conductor.py role is implied but not specified in any prototype. No interface has been designed.

**Required before T2:**

- **Pack dispatch:** Does conductor.py own the Execution Pack lifecycle? Does it read the YAML, issue STAGE commands, and collect verdicts?
- **Room orchestration:** Does conductor.py manage multiple Bridge Room instances? How does it route packs to rooms?
- **TOKEN_SAFE_STOP handling:** When Claude issues TOKEN_SAFE_STOP, who reads it — conductor.py or Codex directly? What is the recovery flow?
- **Pack chaining trigger:** When pack_result = PACK_COMPLETE and open_issues = [], does conductor.py automatically trigger the next pack? Or does Codex intervene?
- **Failure escalation:** If a pack reaches ERROR + ROLLBACK_COMPLETE with unresolved issues, does conductor.py halt or notify?

**Design constraint:** conductor.py integration is T2. No conductor.py files may be modified at T1.

---

## 7. Telegram Decision Relay (Design Only)

**Current state:** Telegram integration is explicitly NOT approved. All prototypes have `telegram: false` in safety fields.

**Required before T2:**

- **Relay direction:** Is Telegram used for Codex → Claude command relay, or Claude → Codex output relay, or both?
- **Message format:** How does a Telegram message map to a Bridge Room command? Is it JSON in message body? Attachment? Structured markup?
- **Verdict delivery:** How does a verdict issued via Telegram get written to `verdicts/`? Who is the intermediary?
- **Authentication:** Which Telegram bot/account is authoritative for Bridge Room commands? How is impersonation prevented?
- **Ordering guarantee:** Telegram does not guarantee message ordering. How does the Bridge Room handle out-of-order stage commands?
- **Offline handling:** If the Telegram relay is unavailable, can the Bridge Room proceed file-only? What is the fallback?

**Design constraint:** Telegram integration is T2. No Telegram bot IDs, tokens, or chat IDs may appear in T1 documents.

---

## 8. Codex/Claude Real Session Separation

**Current state:** In all prototypes, "Codex" and "Claude" are roles played by the same agent (Claude Code) writing to different directories. Real session separation has never been tested.

**Required before T2:**

- **Session identity:** In a real deployment, Codex is a distinct system (e.g., OpenAI Codex, or a human operator). Claude is a distinct Claude session (e.g., claude-sonnet-4-6 via API or Claude Code CLI). These must be genuinely separate processes.
- **Authority boundary:** Only Codex may write to `outbox/` and `verdicts/`. Only Claude may write to `inbox/`. This boundary is enforced by convention in prototypes — in runtime it must be enforced by access control or process separation.
- **Verdict forgery risk:** In prototypes, Claude could theoretically write a verdict to `verdicts/` directly. In runtime, this must be structurally impossible.
- **TOKEN_SAFE_STOP reader:** In prototypes, TOKEN_SAFE_STOP is written by Claude and read by Codex. In runtime, the reading process must be a genuine Codex session — not Claude reading its own stop state.
- **Concurrent access:** If both sessions are active simultaneously, what file locking or coordination mechanism prevents race conditions on `room-state.json`?

**Design constraint:** Real session separation design is T2. At T1, the role separation is documented but not enforced.

---

## 9. Execution Pack Runtime Contract

**What the sandbox proved:**

The Execution Pack v1 schema (YAML) is a complete specification for a single pack execution:
- pack_id, prior_pack_id, approval_policy, global_rules, stop_conditions
- targets[]: file, expected fields, checks, read_only flag
- stages[]: type, task, command, output, verdict IDs, allowed files
- token_safe_stop: all 18 fields defined

**What the runtime contract must add:**

| Requirement | Design Needed |
|------------|---------------|
| Pack ingestion | Who reads the YAML — conductor.py? bridge.py? Codex directly? |
| Stage trigger | Who issues the first command after pack_start? |
| Output validation | Is OUT-xxx validated against expected schema before verdict? |
| Verdict authority | Is verdict written by Codex only, or can it be auto-generated on PASS? |
| Pack result propagation | When PACK_COMPLETE, who writes the final-report.json? Claude or conductor? |
| Chain trigger | On PACK_COMPLETE + open_issues=[], who reads prior_pack_id and dispatches next pack? |
| Pack registry | Where are all active and completed packs indexed? No registry exists in T1. |

**Design constraint:** The Execution Pack runtime contract must be fully specified in a T2 design document before any pack is executed outside the sandbox.

---

## 10. Rollback Safety Requirements

**What the sandbox proved:**

- PRE_FIX_SNAPSHOT written before FIX (confirmed in P6, P7, P8)
- Snapshot ID (SNAP-Pn-xx) is unique per pack per target
- Snapshot lineage is separate across packs (P7 snapshot ≠ P8 snapshot)
- Rollback restores the pre-fix state of the target file
- rollback_required: true triggers ROLLBACK stage before PACK_COMPLETE
- P7 snapshots frozen in P8 — cannot be used as P8 rollback source

**What runtime rollback must add:**

| Requirement | Gap |
|------------|-----|
| Atomic rollback | In sandbox, rollback = overwrite file. In runtime with Shopify writes or DB changes, atomicity must be designed. |
| Rollback verification | After rollback, who verifies the file matches the snapshot? RETEST stage covers files — but Shopify state is not file-based. |
| Partial rollback | If a 3-target pack fixes TGT-01 and TGT-02 but fails on TGT-03, can TGT-01 and TGT-02 be selectively rolled back? Not designed. |
| Snapshot storage | .bak files in inbox/snapshots/ are local. In runtime, snapshots must persist across sessions. |
| Rollback authorization | In sandbox, rollback is auto-triggered on ERROR verdict. In runtime, does rollback require Codex authorization? |

**Design constraint:** Rollback safety for runtime (especially Shopify writes) is T2. Do not extend rollback design beyond file-based patterns at T1.

---

## 11. TOKEN_SAFE_STOP Runtime Requirements

**Current schema (18 fields, proven in P8):**

| Field group | Fields |
|------------|--------|
| Core (P5) | report_id, pack_id, safe_to_stop, captured_at, current_stage, current_stage_status, pending_stage, files_read, files_written, last_verdict |
| Extended (P7) | next_required_action, resume_instruction, risk_level, targets_completed, targets_pending, rollback_state, snapshots_available |
| Pack chaining (P8) | prior_pack_id, prior_pack_report, inherited_fixed_targets, inherited_open_issues |

**Runtime requirements:**

- **Trigger condition:** TOKEN_SAFE_STOP must be written before any context window limit is reached. In sandbox this is manual. In runtime, the trigger must be automatic — based on token count or stage boundary.
- **Reader identity:** The TOKEN_SAFE_STOP file must be read by Codex (not Claude) to authorize resume. In sandbox, Claude writes it and also reads it in the next turn — this is a session boundary violation in real runtime.
- **Resume handoff:** `resume_instruction` field contains the re-entry point. In runtime, who parses this and issues the next command? conductor.py? Codex directly?
- **Stale state detection:** If TOKEN_SAFE_STOP was written in a previous session and a new session starts, how does the system detect it is stale vs. actionable?
- **18-field completeness validation:** In sandbox, field count is manually verified. In runtime, TOKEN_SAFE_STOP ingestion must validate all 18 fields are present before allowing resume.

---

## 12. Approval Tier Policy

| Tier | Scope | Current Status |
|------|-------|---------------|
| T1 | Sandbox/design only. No bridge.py, no Telegram, no Shopify writes, no runtime. File operations inside docs/management/bridge-room-prototype/** only. | ACTIVE — all prototypes ran at T1 |
| T2 | Integration design and controlled testing. Covers: bridge.py interface design, conductor.py interface design, Telegram relay design, real session separation design. No live Shopify writes. No autonomous production execution. | NOT GRANTED |
| T3 | Live production. Autonomous pack execution against real Shopify store, real Telegram relay, real Claude sessions. | NOT GRANTED — requires T2 completion first |

**T2 gate conditions (all must be met before T2 is granted):**
1. bridge.py integration design complete and reviewed
2. conductor.py integration design complete and reviewed
3. Telegram relay design complete and reviewed
4. Real session separation design complete and reviewed
5. Execution Pack runtime contract complete and reviewed
6. Rollback safety for runtime complete and reviewed
7. TOKEN_SAFE_STOP runtime requirements complete and reviewed
8. Explicit T2 approval from project owner

**T1 hard rules (remain in effect regardless of T2 status):**
- DO NOT connect to bridge.py
- DO NOT import or reference scripts/
- DO NOT push to Telegram
- DO NOT write to Shopify
- DO NOT run as a live system
- DO NOT modify files outside docs/management/bridge-room-prototype/**

---

## 13. Hard Blockers Before Runtime

The following must ALL be resolved before any runtime connection is permitted. None are currently resolved.

| # | Blocker | Required Deliverable |
|---|---------|---------------------|
| 1 | No bridge.py integration design | T2 design doc: bridge.py interface spec |
| 2 | No conductor.py integration design | T2 design doc: conductor.py interface spec |
| 3 | No Telegram relay design | T2 design doc: Telegram relay spec |
| 4 | Real session separation not tested | T2 design doc: session separation model |
| 5 | Execution Pack runtime contract not defined | T2 design doc: runtime contract spec |
| 6 | Rollback safety for non-file targets not designed | T2 design doc: rollback safety extension |
| 7 | TOKEN_SAFE_STOP runtime trigger not designed | T2 design doc: TOKEN_SAFE_STOP runtime spec |
| 8 | No pack registry design | T2 design doc: pack registry spec |
| 9 | T2 approval not granted | Explicit approval from project owner |
| 10 | No T2 sandbox design document | This document + T2 design docs must exist first |

**Until all 10 blockers are resolved: READY FOR RUNTIME INTEGRATION = NO.**

---

## 14. Recommended Next Milestone

**Milestone: T2 Design Review Package**

Produce a set of T2 design documents (design-only, no code changes, no runtime connections) covering each blocker in Section 13. Each document must be reviewed and explicitly approved before any integration work begins.

**Recommended document sequence:**

| Order | Document | Covers Blockers |
|-------|---------|-----------------|
| 1 | `bridge-room-t2-bridge-integration.md` | #1, #4 |
| 2 | `bridge-room-t2-conductor-integration.md` | #2, #8 |
| 3 | `bridge-room-t2-telegram-relay.md` | #3 |
| 4 | `bridge-room-t2-runtime-contract.md` | #5 |
| 5 | `bridge-room-t2-rollback-safety.md` | #6 |
| 6 | `bridge-room-t2-token-safe-stop-runtime.md` | #7 |

Each document follows the same pattern as this document: design-only, T1 approval tier, no tool calls to live systems, explicit READY FOR T2 DESIGN REVIEW and READY FOR RUNTIME INTEGRATION fields.

**After all 6 documents are written and reviewed:** Request T2 approval from project owner. T2 approval unlocks controlled integration testing in an isolated non-production environment.

---

## 15. READY FOR T2 DESIGN REVIEW: NO

**Reason:** The T2 design documents listed in Section 14 do not yet exist. This document is a prerequisite for the T2 design review package — it defines what T2 must cover. The T2 review can begin only after:
- This document is reviewed and accepted
- At least documents #1 and #2 from the T2 sequence (bridge.py + conductor.py integration) are drafted

**Condition to change to YES:**
- All 6 T2 design documents from Section 14 are complete
- Project owner has reviewed Section 13 hard blockers
- No new hard blockers are identified

---

## 16. READY FOR RUNTIME INTEGRATION: NO

All prototypes (#1–#8) are sandbox-only. No component of the Bridge Room has been connected to a live system. This status does not change until:

1. T2 design review package is complete (Section 14)
2. T2 approval is explicitly granted (Section 12)
3. All hard blockers in Section 13 are resolved
4. A controlled integration test plan is approved (not yet designed)

**This document does not change the runtime integration status. It is a design-only artifact.**

---

*See [PROTOTYPE-CLOSURE.md](bridge-room-prototype/PROTOTYPE-CLOSURE.md) for full sandbox closure record.*  
*See [README.md](bridge-room-prototype/README.md) for current prototype status.*
