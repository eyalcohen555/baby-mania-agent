# Bridge Room T2 — Telegram Relay Design

**TYPE:** Design document — T1 only  
**STATUS:** DRAFT  
**APPROVAL TIER:** T1  
**LAYER:** 1  
**CREATED:** 2026-05-04  
**COVERS BLOCKERS:** #3 from bridge-room-runtime-readiness.md Section 13  
**READY FOR T2 DESIGN REVIEW:** YES  
**READY FOR RUNTIME INTEGRATION:** NO

> **CRITICAL:** This document describes a future design only.  
> No Telegram bot token, chat_id, or live connection appears anywhere in this document.  
> No message is sent. No Telegram API is called.  
> Every action described here requires a separate T2 approval before execution.

---

## 1. SYSTEM STATE

| Item | Status |
|------|--------|
| Bridge Room prototypes #1–#8 | ALL PASS (sandbox only) |
| Telegram integration in prototypes | EXPLICITLY DISABLED — `telegram: false` in all sandbox safety fields |
| user-decision-mock.json pattern | PROVEN (P3, P6) — file-based decision relay |
| Telegram bot | EXISTS in project (separate system) — NOT connected to Bridge Room |
| Telegram relay design for Bridge Room | NOT DESIGNED until this document |
| Live Telegram connection | NOT AUTHORIZED |
| T2 approval for Telegram in Bridge Room | NOT GRANTED |
| Runtime integration | BLOCKED |

---

## 2. Why This Document Is Required

`bridge-room-runtime-readiness.md` (Section 13, Blocker #3):
> "No Telegram relay design — Required deliverable: T2 design doc: Telegram relay spec"

Section 7 of that document lists six open questions that must be answered before T2:
1. Relay direction: Codex → Claude command relay, Claude → Codex output relay, or both?
2. Message format: How does a Telegram message map to a Bridge Room command?
3. Verdict delivery: How does a Telegram verdict get written to `verdicts/`?
4. Authentication: Which bot/account is authoritative? How is impersonation prevented?
5. Ordering guarantee: Telegram does not guarantee message ordering — how is this handled?
6. Offline handling: Can the Bridge Room proceed file-only if Telegram is unavailable?

This document answers all six questions in design form only. No live connection is made.

---

## 3. Current Sandbox Proof Relevant to Telegram Relay

### 3a. user-decision-mock.json Pattern (P3, P6)

The sandbox established the file-based decision relay protocol:

```
BLOCKED state triggers:
  Codex writes outbox/ with escalation spec
  room-state.json: pending_decision = { escalation_id, decision_spec, consumed: false }
  Pack HALTS

User resolution:
  User writes inbox/user-decision-<escalation_id>.json with:
    { decision_id, pack_id, task_id, command_id, escalation_id, consumed: false, resolution: {...} }

Resume validation (proven P3, P6):
  5-ID match: decision_id + pack_id + task_id + command_id + escalation_id
  consumed = false (single-use enforcement)
  After validation: consumed = true, resume dispatched
```

### 3b. What the Mock Does NOT Prove

- Who writes the user-decision file in runtime (human via UI? Telegram? Direct file write?)
- How a Telegram message maps to the decision JSON schema
- How the system confirms the decision came from an authorized source
- What happens if a second message arrives before consumed=true is written

---

## 4. Relay Direction Design

### 4a. Decision

**Telegram relay in Bridge Room is bidirectional:**

| Direction | Sender | Receiver | Purpose |
|-----------|--------|----------|---------|
| Outbound (notification) | conductor.py | Telegram (Codex/user) | Escalation alert when pack is BLOCKED or FAILED |
| Inbound (decision) | Telegram (Codex/user) | conductor.py | Decision resolution for BLOCKED state |
| Outbound (status) | conductor.py | Telegram | Pack milestone events (PACK_COMPLETE, TOKEN_SAFE_STOP) |

Telegram is NOT used to relay Claude's stage outputs or Codex's verdicts.  
Verdicts are always written to `verdicts/` as JSON files — Telegram cannot substitute for this.

### 4b. What Telegram Does NOT Replace

| Component | Always File-Based | Telegram Cannot Replace |
|-----------|------------------|------------------------|
| Stage commands | outbox/<pack_id>-<stage_id>-command.json | YES — command structure too complex for single message |
| Claude outputs | inbox/<pack_id>-<stage_id>-output.json | YES — output contains structured JSON |
| Codex verdicts | verdicts/<pack_id>-<stage_id>-verdict.json | YES — verdict is authoritative record |
| room-state.json | Bridge Room state | YES — state machine cannot be in Telegram |
| journal events | append-only audit trail | YES — journal must be file-based |

---

## 5. Outbound Relay Design (conductor.py → Telegram)

### 5a. Trigger Events

conductor.py sends a Telegram message when:

| Event | Trigger Condition | Message Type |
|-------|-------------------|-------------|
| PACK_BLOCKED | verdict = BLOCKED on any stage | Escalation notice |
| PACK_FAILED | pack_status = PACK_FAILED | Failure alert |
| PACK_COMPLETE | pack_status = PACK_COMPLETE | Success notice |
| TOKEN_SAFE_STOP | pack_status = TOKEN_SAFE_STOP | Stop alert |
| CRITICAL_ROLLBACK_FAILURE | pack_status = CRITICAL_ROLLBACK_FAILURE | Critical alert |
| PACK_START (optional) | pack ingestion begins | Status notice |

### 5b. Outbound Message Format (Design Only)

Messages are sent via an existing `conductor-notify.md` mechanism (per conductor-plan-format.md Section 10 design boundary).

Proposed escalation message format:

```
BRIDGE_ROOM_EVENT: PACK_BLOCKED
pack_id: EXEC-PACK-P9-001
room_id: BRM-001
stage_id: STAGE-01
stage_type: AUDIT
escalation_id: ESC-P9-001
decision_required: YES
decision_spec_summary: <single line description of what decision is needed>
pack_journal: docs/management/bridge-room-prototype/journal/<pack_id>-log.jsonl
RESPOND_WITH: BRIDGE_ROOM_DECISION:<escalation_id>:<decision>
```

### 5c. Outbound Constraints

- conductor.py writes to `conductor-notify.md` only — it does NOT call Telegram API directly
- Telegram delivery is handled by the existing `telegram_bot.py` (separate system, not modified)
- If telegram_notify is disabled for the pack → escalation written to journal only, no Telegram message sent
- No pack-internal data (target file contents, verdict JSON bodies) is sent via Telegram

---

## 6. Inbound Relay Design (Telegram → conductor.py)

### 6a. Problem

In sandbox: user writes `inbox/user-decision-<escalation_id>.json` directly (file-based mock).  
In runtime: user/Codex responds via Telegram message.  
The Bridge Room loop does not know about Telegram — it only polls `inbox/` for decision files.  
Therefore: a **Telegram-to-file translator** is needed.

### 6b. Translator Component (Design Only)

A new component — **Telegram Decision Adapter** — runs between Telegram and the Bridge Room:

```
User sends Telegram message:
  BRIDGE_ROOM_DECISION:ESC-P9-001:target_quality_bar=premium
         ↓
Telegram Decision Adapter (not yet designed — T2 component):
  parses escalation_id from message
  looks up pending_decision in room-state.json by escalation_id
  constructs user-decision-*.json from message + pending_decision spec
  writes: inbox/user-decision-<escalation_id>.json
         ↓
conductor.py polls inbox/ and finds decision file
conductor.py validates 5 IDs (same as sandbox)
Resume dispatched
```

The Telegram Decision Adapter is a **new, separate component** — not conductor.py, not bridge.py.  
Its implementation is T2 scope. This document designs its interface only.

### 6c. Inbound Message Format (Design Only)

User/Codex sends via Telegram:

```
BRIDGE_ROOM_DECISION:<escalation_id>:<resolution>
```

Examples:
```
BRIDGE_ROOM_DECISION:ESC-P9-001:target_quality_bar=premium
BRIDGE_ROOM_DECISION:ESC-P9-002:proceed=yes
BRIDGE_ROOM_DECISION:ESC-P9-003:rollback=approved
```

The Adapter constructs the full decision JSON from this prefix plus data from `room-state.json`.

### 6d. Generated Decision JSON Schema

The Adapter produces a file matching the sandbox pattern proven in P3/P6:

```json
{
  "decision_id": "DEC-<escalation_id>-<ts>",
  "escalation_id": "<from Telegram message>",
  "pack_id": "<from room-state.json pending_decision>",
  "task_id": "<from room-state.json pending_decision>",
  "command_id": "<from room-state.json pending_decision>",
  "decision_source": "telegram",
  "authorized_by": "<Telegram sender chat_id>",
  "sent_at": "<Telegram message timestamp>",
  "received_at": "<Adapter processing timestamp>",
  "consumed": false,
  "resolution": { "<key>": "<value from message>" }
}
```

---

## 7. Authentication Design

### 7a. Problem

Telegram does not inherently authenticate that a message is from an authorized Codex operator.  
A forged message could inject a fake decision and bypass the BLOCKED state.

### 7b. Authentication Model (Design Only)

**Layer 1 — Chat ID whitelist:**
- Only messages from a pre-configured whitelist of chat_ids are processed by the Adapter
- Messages from unknown chat_ids are logged and ignored
- Whitelist stored in project config (not hardcoded in Adapter code) — T2 approval required for whitelist management

**Layer 2 — Escalation ID binding:**
- Adapter only processes messages that reference a valid, active escalation_id
- If `escalation_id` in message does not match `room-state.json.pending_decision.escalation_id` → message rejected
- This prevents replay attacks with stale escalation IDs

**Layer 3 — Consumed flag (proven P3/P6):**
- Decision file carries `consumed: false` on creation
- First validation by conductor.py sets `consumed: true`
- Any second resolution attempt on the same escalation_id is rejected (stale decision)

**Layer 4 — Timestamp freshness:**
- Adapter validates `sent_at` timestamp is within acceptable window (TBD — e.g., 30 minutes)
- Messages older than the window are rejected as stale

### 7c. What Is NOT Authenticated

- The content of the resolution (e.g., `target_quality_bar=premium`) — semantic validation is done by conductor.py against the pending_decision decision_spec
- The identity of the Telegram account (beyond chat_id whitelist) — this is a known limitation

---

## 8. Ordering and Stale Decision Handling

### 8a. Telegram Ordering Constraint

Telegram does not guarantee message delivery order. If two decision messages are sent rapidly, they may arrive out of order. The Bridge Room must handle this.

### 8b. Ordering Design (Design Only)

| Scenario | Handling |
|----------|---------|
| Two messages for same escalation_id | First to be processed wins; second is rejected (consumed=true) |
| Message arrives for escalation_id that is already consumed | Rejected — logged as DECISION_ALREADY_CONSUMED |
| Message arrives for escalation_id that no longer exists (pack resumed by file) | Rejected — logged as ESCALATION_ID_NOT_FOUND |
| Message arrives before BLOCKED state is written to room-state.json | Adapter buffers for N seconds, retries lookup; if still not found → rejected |

### 8c. Duplicate Message Prevention

The Telegram Decision Adapter must track:
- `processed_message_ids: []` — list of Telegram message_ids already processed
- Before writing any decision file: check message_id not already in list
- After writing: add message_id to processed list

---

## 9. Offline / Fallback Design

### 9a. Fallback Requirement

From bridge-room-runtime-readiness.md Section 7:
> "If the Telegram relay is unavailable, can the Bridge Room proceed file-only? What is the fallback?"

### 9b. File-Based Fallback (Design Only)

The Telegram relay is a **convenience layer**, not a hard dependency. The Bridge Room file protocol is the primary interface.

**Fallback rule:** If Telegram relay is unavailable or not yet implemented, any authorized operator may write a decision file directly:

```
inbox/user-decision-<escalation_id>.json
```

Using the exact same schema (Section 6d with `decision_source: "file"` instead of `"telegram"`).

conductor.py does not distinguish between Telegram-generated and file-generated decision files at validation time. Both must pass the same 5-ID validation.

### 9c. Fallback Priority

```
Priority 1: Telegram Decision Adapter writes decision file → conductor.py processes
Priority 2: Human operator writes decision file directly → conductor.py processes
Priority 3: Telegram relay offline → no decision → pack remains HALTED until resolved
```

There is no auto-resume on Telegram timeout. The pack waits indefinitely in BLOCKED state.

---

## 10. Interfaces

### 10a. conductor.py → Telegram (outbound)

| Interface | Mechanism | T2 Change Required |
|-----------|-----------|-------------------|
| Escalation notice | Write to conductor-notify.md (existing) | Extend format for Bridge Room events |
| Pack milestone (COMPLETE/FAILED) | Write to conductor-notify.md | Extend format |
| TOKEN_SAFE_STOP alert | Write to conductor-notify.md | Extend format |

### 10b. Telegram → inbox/ (inbound via Adapter)

| Interface | Mechanism | T2 Change Required |
|-----------|-----------|-------------------|
| Decision file creation | Adapter writes inbox/user-decision-<escalation_id>.json | New component — Adapter not yet written |
| Authentication whitelist | Config file (location TBD) | New config file |
| Processed message tracking | Adapter internal state (file TBD) | New file |

### 10c. conductor.py Decision File Polling

No change to conductor.py polling interface — it polls `inbox/` for decision files by escalation_id exactly as in sandbox (proven P3/P6).

---

## 11. Risks

| Risk | Severity | Description | Mitigation |
|------|----------|-------------|-----------|
| Forged decision via Telegram | HIGH | Attacker sends BRIDGE_ROOM_DECISION message from non-whitelisted account | Chat_id whitelist (Layer 1) + escalation_id binding (Layer 2) |
| Stale Telegram message replayed | HIGH | Decision from resolved escalation replayed in new pack with same escalation_id format | Escalation IDs must be globally unique (include pack_id + timestamp); consumed flag prevents reuse |
| Telegram relay delay causes pack to wait indefinitely | MEDIUM | Telegram message delayed 10+ minutes — pack stays BLOCKED | File-based fallback always available; no auto-timeout on BLOCKED state |
| Two users send simultaneous decisions | HIGH | Race condition — both messages processed, two decision files written | Processed message_id tracking in Adapter; first-writer wins, second rejected |
| Adapter crashes between receiving message and writing file | HIGH | Decision lost — no file written — pack stays BLOCKED | Adapter must be idempotent — can re-process same message_id safely; logs all received messages before processing |
| Decision content not validated | MEDIUM | User sends malformed resolution (e.g., wrong key name) | conductor.py validates resolution against decision_spec from pending_decision; rejects if schema mismatch |
| Live Telegram tokens in design docs | CRITICAL | Bot token or chat_id appears in any design document | THIS DOCUMENT contains no tokens or chat_ids; this constraint must be enforced in all T2 implementation docs |

---

## 12. Safety Rules

1. **No live Telegram token or chat_id may appear in any Bridge Room design document** — even as an example
2. **Telegram relay is optional** — Bridge Room must function without it (file fallback always works)
3. **Telegram does not replace the verdict file protocol** — verdicts/ is always file-based
4. **No stage commands are sent via Telegram** — commands are always files in outbox/
5. **No Claude outputs are relayed via Telegram** — outputs are always files in inbox/
6. **Decision authority requires 5-ID validation** — Telegram-sourced decisions must pass the same checks as file-sourced ones
7. **The existing Telegram bot (`telegram_bot.py`) is not modified** — a new Adapter component is designed separately

---

## 13. What Must NOT Be Connected Yet

| Component | Why Forbidden | Required Before Connecting |
|-----------|--------------|---------------------------|
| Telegram bot in Bridge Room | T2 required | This doc reviewed + T2 approval |
| Telegram Decision Adapter (new component) | Not yet written | T2 approval + implementation |
| Live Telegram chat_ids or tokens | Never in design docs | T2 approval + secure config management |
| Telegram as command relay (outbox/ replacement) | Not designed — commands are file-only | Future T3 design only if ever needed |
| Telegram as verdict relay (verdicts/ replacement) | Not designed — verdicts are file-only | Not planned |
| conductor-notify.md Bridge Room event extensions | Requires conductor.py change | T2 approval |

---

## 14. T2 Approval Requirements

| # | Requirement | Status |
|---|-------------|--------|
| 1 | This document reviewed and accepted by project owner | NOT DONE |
| 2 | T2 approval for Telegram Decision Adapter (new component) | NOT GRANTED |
| 3 | T2 approval for conductor-notify.md Bridge Room event format extensions | NOT GRANTED |
| 4 | Chat_id whitelist management policy agreed | NOT DONE |
| 5 | Processed message_id tracking mechanism agreed (file location, format) | NOT DONE |
| 6 | Escalation_id globally-unique format agreed | NOT DONE |
| 7 | Adapter idempotency design agreed (re-processing safety) | NOT DONE |
| 8 | Fallback procedure documented for operations team | NOT DONE |

**Until all 8 items are satisfied: no Telegram integration with Bridge Room begins.**

---

## 15. READY FOR T2 DESIGN REVIEW: YES

This document addresses Blocker #3 from bridge-room-runtime-readiness.md and answers all six open questions from Section 7 of that document.

---

## 16. READY FOR RUNTIME INTEGRATION: NO

This document is design only. It authorizes no change to telegram_bot.py, conductor.py, bridge.py, or any runtime file. No Telegram message is sent. No Telegram token is used.

---

*Prereq reading: [bridge-room-runtime-readiness.md](bridge-room-runtime-readiness.md)*  
*Sandbox proof: [bridge-room-prototype/PROTOTYPE-CLOSURE.md](bridge-room-prototype/PROTOTYPE-CLOSURE.md)*  
*Companion documents: [bridge-room-t2-bridge-integration.md](bridge-room-t2-bridge-integration.md), [bridge-room-t2-conductor-integration.md](bridge-room-t2-conductor-integration.md)*
