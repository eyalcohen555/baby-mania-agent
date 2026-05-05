task_id: 20260506-004045
---
RESUME_GAP_CONFIRMED: YES

GAP_DESCRIPTION:
`bridge.py` / `scripts/telegram_bot.py` only consume `telegram-response.md` while a single task is in flight (the `_waiting_for_reply` / `_waiting_for_response` state in the bot is True only after the bot itself prompts the user from a `last-result.md` question/approval/blocked event). When the conductor is between stages and the bridge has no active task, an inbound Telegram reply is still written to `telegram-response.md`, but no component polls that file on behalf of the conductor — so the conductor's stage-gate approval is never resumed automatically.

Confirmed from current state:
- `bridge/conductor-state.md` shows the conductor drives multi-stage plans (`current_stage: STAGE-6`, `waiting_for: ''`), i.e. an approval gate would set `waiting_for` but no listener reacts to `telegram-response.md` against that field.
- `bridge/last-result.md` (prior stage 5) explicitly flagged: `conductor-notify.md` integration into `telegram_bot.py` monitor loop is undesigned. The design doc (`docs/operations/telegram-channel-design.md`) defines reply routing only for task-level events (TASK_STARTED / QUESTION / APPROVAL_NEEDED / BLOCKED / TASK_DONE), not for plan-level / between-stage approval.
- `bridge/status.md` shows `status: running` for a single task — confirming reply routing is task-scoped, not conductor-scoped.

CURRENT_WORKAROUND:
Operator manually triggers conductor resume after a Telegram approval lands between stages — either by re-issuing the next stage task to the bridge, or by running the conductor resume command locally. The Telegram reply is captured in `telegram-response.md` for audit, but it does not auto-advance the plan.

FIX_REQUIRED (description only — no code changes):
1. Define a conductor-aware listener: while `conductor-state.md.waiting_for` is non-empty (e.g. `approval:STAGE-N`), `telegram_bot.py` (or a new conductor-side watcher) must treat inbound replies as conductor approvals, not task replies.
2. Extend the design in `docs/operations/telegram-channel-design.md` with plan-level events: `STAGE_APPROVAL_NEEDED`, `STAGE_APPROVED`, `STAGE_REJECTED`, mapped to the `approve` / `reject` `RESPONSE_TYPE` payload already defined in Phase 2.
3. On approve/reject, the conductor must consume `telegram-response.md`, clear `waiting_for`, and dispatch the next stage's `next-task.md` automatically — closing the resume loop without operator action.
4. Disambiguate ownership: when both a task is active (`status=running`) and the conductor is gated, the reply must be routed to the conductor gate (plan-level takes precedence) or carry a correlation id (`STAGE-N` / `TASK_ID`) to avoid mis-routing.

---

STAGE_VERDICT: PASS

EVIDENCE:
- Read-only stage; no files modified, no FILES_FORBIDDEN opened.
- Gap reproducible from `bridge/conductor-state.md` (multi-stage plan, `waiting_for` field exists) + `bridge/last-result.md` (prior stage 5 already documented the missing `conductor-notify.md` ↔ telegram_bot.py integration).
- All 4 required fields produced (RESUME_GAP_CONFIRMED, GAP_DESCRIPTION, CURRENT_WORKAROUND, FIX_REQUIRED).

SYSTEM STATE:
- Plan `bridge-telegram-stabilization-001` STAGE-6 documentation produced.
- conductor-state remains `RUNNING / current_stage: STAGE-6`; conductor must transition to next stage or `overall_verdict` finalization on its next tick.
- Gap is documentation-only output; no code change executed, no follow-up file write performed (task forbade touching files).