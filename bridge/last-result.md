task_id: 20260330-111000
---
## AUDIT RESULT: WATCHDOG FALSE IDLE ALERT

**ROOT CAUSE:** Faulty OR logic in `check()` — line 213 of `watchdog.py`

```python
is_active = bridge_status in ACTIVE_BRIDGE or stage in ACTIVE_STAGE
```

**LAYER:** LOGIC

**WHY SYSTEM ALLOWS THIS:**

The watchdog report at `11:09:26` shows:
- `bridge_status: starting` (new task cycle spinning up)
- `stage: DONE` (previous task 20260330-110415 already finished)
- `state_age_seconds: 157` (stale timestamp from completed task)
- `reminder_sent: YES` ← **false alert**

The sequence:
1. Task `20260330-110415` completes → `stage=DONE`
2. Bridge transitions to next cycle → `bridge_status=starting`
3. Watchdog checks: `"starting" in ACTIVE_BRIDGE` → **True** (OR short-circuits)
4. Age calculated from the **old** task timestamp → 157s > 120s warn threshold
5. Sends "ריצה ממתינה" alert for a task that's already done

The OR condition means **any** active bridge status overrides a terminal stage. There is no check for terminal states (`DONE`, `BLOCKED`, `FAILED`) to suppress the alert.

**RISK LEVEL:** Low — noise only, no data corruption. But erodes trust in alerts over time.

**RECOMMENDED FIX:** Add terminal stage guard before the active check: if `stage in {"DONE", "BLOCKED", "FAILED"}`, force `is_active = False` regardless of bridge_status.