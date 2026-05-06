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

### Gap 3 — conductor task_id format mismatch (STAGE-3 UNKNOWN pattern)
Conductor generates task IDs like `conductor-plan-STAGE-X-YYYYMMDD-HHmmSS`.
Bridge generates its own task IDs in format `YYYYMMDD-HHMMSS`.
Conductor's verdict check (`analyze_verdict`) cannot match its expected task_id
to the bridge-generated task_id in last-result.md → returns UNKNOWN.

**Impact:** LOGIC stages (STAGE-3) always return UNKNOWN. The conductor routes to
the `next_on_pass` fallback in YAML, so the plan still progresses — but STAGE-3
never gets a proper PASS verdict and shows in `failed_stages`.

**Fix required:** Either bridge should write the conductor task_id (passed in the
task body) to last-result.md, or conductor should match on a content field rather
than task_id.

---

## Why Organic Night Mode is Still NO

1. **Gap 3 unresolved**: LOGIC stages always return UNKNOWN. Night mode plans that
   rely on cleanup/routing decisions will misclassify and may take wrong paths.
2. **bridge.py not committed to main**: Fixes are on `bridge-room-plan-mode-verify`
   only. Night mode runs on main.
3. **Plan-level Telegram visibility missing** (Gap 2): operator cannot monitor
   unattended runs from phone.

## Next Required Fix Before Unattended Automation

**Priority 1:** Fix conductor task_id matching (Gap 3).
This is a design-level fix — either bridge embeds the conductor task_id in its
output, or conductor uses a different matching strategy. Until this is resolved,
every LOGIC stage in every plan will return UNKNOWN and rely on fallback routing.

**Priority 2:** Merge branch to main and update bridge runtime on production path.

---

## Files Changed

| File | Change |
|------|--------|
| `bridge.py` | needs_response() structured-first fix + subprocess binary decode fix |
| `plans/bridge-telegram-stabilization-001.yaml` | New plan file (untracked → committed) |
| `docs/management/bridge-telegram-stabilization-001-result.md` | This file |
