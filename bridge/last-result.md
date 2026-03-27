task_id: 20260327-124851
round: 1
---
---

## Summary — BEFORE vs AFTER

### Change 1: STARTED notification (line 589-592)

**BEFORE:**
```python
elif current_status == "running":
    pass  # suppressed — no STARTED/RUNNING notifications per exception policy
```

**AFTER:**
```python
elif current_status == "running":
    task_id = extract_field(current_status_content, "task_id")
    id_str  = f"[{task_id}] " if task_id else ""
    send(f"🔄 {id_str}משימה התחילה")
```

### Change 2: T0/T1 completion notification (line 609-611)

**BEFORE:**
```python
# T1 done — update dedup state silently
elif tier == "T1":
    print(f"[monitor] T1 DONE [{task_id}] — suppressed per exception policy")
```

**AFTER:**
```python
else:
    # T0/T1 — short completion notice
    send(f"✅ {id_str}משימה הסתיימה\n{current_detail}")
```

---

STAGE_VERDICT: PASS
EVIDENCE: Fixed both message gaps identified in STAGE-7/8: (1) Added STARTED notification for running status — user now sees `🔄 [task_id] משימה התחילה` when a task begins. (2) Replaced silent T1 suppression with short completion notice — all tiers now get `✅ [task_id] משימה הסתיימה` (T2/T3 also get full result). Messages are short, clear, phone-readable. Only `scripts/telegram_bot.py` was modified.
SYSTEM STATE: telegram_bot.py messages fixed — start and completion notifications now active for all task tiers. Existing question/approval/blocked messages unchanged (were already good per STAGE-7 audit).
