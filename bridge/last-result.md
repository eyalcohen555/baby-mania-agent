task_id: 20260330-111000
round: 1
---
Diagnosis complete. Here's the result:

---

## WATCHDOG FALSE IDLE ALERT — ROOT CAUSE

**ROOT CAUSE:** Logic flaw — OR condition in active-state check ignores terminal stage.

**LAYER:** LOGIC

**WHY THE SYSTEM ALLOWS THIS:**

At `11:09:26`, the watchdog read:
- `bridge/status.md` → `status: starting` (new cycle beginning)
- `bridge/runtime-state.md` → `stage: DONE`, `task_id: 20260330-110415` (old task, already finished)

The active check on `watchdog.py:213`:
```python
is_active = bridge_status in ACTIVE_BRIDGE or stage in ACTIVE_STAGE
```

`"starting"` is in `ACTIVE_BRIDGE` → **OR evaluates to True** → watchdog treats the system as active, even though `stage` is `DONE`. It then computes age from the old task's timestamp (`state_age_seconds: 157`), exceeds `warn_timeout (120s)`, and fires the "ריצה ממתינה" Telegram alert for a task that already completed.

**Race condition sequence:**
1. Task `20260330-110415` completes → `runtime-state.md` stage = `DONE`
2. Bridge starts new cycle → `status.md` = `starting`
3. Watchdog reads both files → sees `starting` + old `DONE` timestamp → false alert

**RISK LEVEL:** Low — cosmetic false alert, no data corruption or task disruption.

**RECOMMENDED FIX:** Add a terminal-stage guard before the age check: if `stage` is in `{"DONE", "FAILED", "BLOCKED"}`, skip the alert regardless of `bridge_status`. Alternatively, require both `bridge_status` AND `stage` to be active (AND instead of OR).
