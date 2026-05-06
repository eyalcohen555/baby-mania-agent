# Bridge + Telegram Stabilization Plan — Result Report
**Plan ID:** bridge-telegram-stabilization-001
**Date completed:** 2026-05-06
**Branch:** bridge-room-plan-mode-verify
**Overall verdict:** PASS_WITH_KNOWN_GAPS

---

## Plan Result

| Field | Value |
|-------|-------|
| Plan result | PASS_WITH_KNOWN_GAPS |
| ready_for_full_automation | false |
| ready_for_organic_night_mode | false |
| Runtime fixes validated | 2 |
| Known gaps documented | 3 |

---

## Stages Completed

| Stage | Type | Verdict | Notes |
|-------|------|---------|-------|
| STAGE-1 | AUDIT | PASS | Process audit: 1 bridge.py, 1 watchdog.py, no duplicates |
| STAGE-2 | AUDIT | PASS | Bridge file audit: status=running, lock PID alive, telegram-response empty |
| STAGE-3 | LOGIC | UNKNOWN × 3 | Cleanup not needed — routed to STAGE-5 via fallback. See gap #3 |
| STAGE-4 | FIX | SKIPPED | No cleanup required (STAGE-3 result: CLEANUP_REQUIRED=NO) |
| STAGE-5 | AUDIT | PASS | Telegram coverage: 5/6 event types covered. CONDUCTOR_EVENTS missing from design |
| STAGE-6 | AUDIT | PASS | False positive simulation confirmed: STAGE_VERDICT:PASS short-circuits correctly |
| STAGE-7 | RETEST | PASS | End-to-end retest: both fixes behave correctly under plan load |

---

## Fixes Validated

### Fix 1 — needs_response() false positive (bridge.py:32)

**Root cause:** Broad keyword scan caught "APPROVAL NEEDED" as literal text in audit reports
(e.g. Telegram coverage audit says "APPROVAL_NEEDED: COVERED"). Bridge entered
`waiting_response` state even when STAGE_VERDICT: PASS was present.

**Fix:** Structured-first detection with priority order:
1. `STAGE_VERDICT: PASS` → return None immediately (short-circuit)
2. `STAGE_VERDICT: AWAITING_APPROVAL` → return APPROVAL_NEEDED
3. `STATUS: PASS` → return None
4. `RESPONSE_NEEDED: YES` → return based on RESPONSE_TYPE
5. Keyword scan — only fires when **no STAGE_VERDICT line is found**

**Test results:** 5/5 cases PASS

### Fix 2 — Hebrew subprocess output crash (bridge.py:~358)

**Root cause:** Python 3.14 on Windows Hebrew locale uses cp1255 in subprocess reader
threads even when `encoding="utf-8"` is specified. Claude outputs Hebrew UTF-8 characters
that cp1255 cannot decode, causing `UnicodeDecodeError` in `_readerthread`. The exception
truncated Claude's output to ~50 bytes before the offending character, causing bridge to
write a partial result and conductor to get UNKNOWN verdict for the stage.

**Fix:** Remove `text=True, encoding="utf-8"` from Claude subprocess call. Use binary
capture and manual decode:
```python
raw = result.stdout or result.stderr or b""
output = raw.decode("utf-8", errors="replace").strip()
```

**Verified:** STAGE-5 completed cleanly with full Hebrew output after fix.

---

## Known Gaps

### Gap 1 — auto-resume listener not wired
`telegram-response.md` → conductor approval gate is not implemented.
When a stage requires human approval (T3 or AWAITING_APPROVAL), the conductor
has no listener for the response file. Currently requires manual restart.
**Blocking for:** unattended T3 plan execution.

### Gap 2 — plan-level approval events missing from design
`conductor-notify.md` is not read by `telegram_bot.py`.
STAGE transitions (PLAN_STARTED, STAGE_PASS, STAGE_FAIL, PLAN_COMPLETE) produce
no Telegram notification. The design doc (`docs/operations/telegram-channel-design.md`)
has no conductor-plan event contract.
**Blocking for:** operator visibility during unattended runs.

### Gap 3 — LOGIC stage output contract failure (STAGE-3 UNKNOWN pattern)

**Corrected root cause** (previous description was wrong — task_id mismatch does
not affect verdict routing; `analyze_verdict` never matches by task_id).

**Actual mechanism:** `conductor.py:analyze_verdict()` handles LOGIC-type stages
by scanning output lines for an exact pattern: a line whose cleaned, uppercased
form ends with `: YES` or `: NO`. If no such line is found, it returns UNKNOWN.

STAGE-3 Claude output did not contain a line in this exact format. The stage goal
and action description asked for `CLEANUP_REQUIRED: YES` or `CLEANUP_REQUIRED: NO`,
but the output format contract was not enforced as a hard requirement in the YAML.

**Note on task_id mismatch:** Conductor formats task IDs as
`conductor-{plan_id}-{stage_id}-{YYYYMMDD-HHmmSS}`. Bridge generates its own IDs
(`YYYYMMDD-HHMMSS`). This mismatch is real but affects tracking only — it does not
cause UNKNOWN verdicts.

**Impact:** LOGIC stages return UNKNOWN when Claude output lacks an exact
`KEY: YES` or `KEY: NO` line. Conductor routes to the `next_on_pass` fallback,
so the plan still progresses — but the stage shows in `failed_stages`.

**Fix required:** Every LOGIC stage YAML must include a hard `required_logic_output`
field specifying the exact decision key. The stage prompt must explicitly instruct
Claude to output exactly one line: `<KEY>: YES` or `<KEY>: NO` with no variation.
This is a plan-level contract fix — no runtime code changes needed.

---

## Why Organic Night Mode is Still NO

1. **Gap 3 unresolved**: LOGIC stages return UNKNOWN when output lacks exact
   `KEY: YES / KEY: NO` line. Night mode plans that rely on cleanup/routing
   decisions will misclassify and may take wrong paths.
2. **bridge.py not committed to main**: Fixes are on `bridge-room-plan-mode-verify`
   only. Night mode runs on main.
3. **Plan-level Telegram visibility missing** (Gap 2): operator cannot monitor
   unattended runs from phone.

## Next Required Fix Before Unattended Automation

**Priority 1:** Enforce LOGIC output contract in every plan (Gap 3).
Add `required_logic_output` to every LOGIC stage in every plan YAML. Stage prompt
must explicitly require Claude to output exactly `<KEY>: YES` or `<KEY>: NO` as a
standalone line. No code changes needed — this is a plan authoring requirement.

**Priority 2:** Merge branch to main and update bridge runtime on production path.

---

## Files Changed

| File | Change |
|------|--------|
| `bridge.py` | needs_response() structured-first fix + subprocess binary decode fix |
| `plans/bridge-telegram-stabilization-001.yaml` | New plan file (untracked → committed) |
| `docs/management/bridge-telegram-stabilization-001-result.md` | This file |
