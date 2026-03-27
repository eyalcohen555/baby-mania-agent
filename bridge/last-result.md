task_id: 20260327-124826
---
The bridge has already advanced to STAGE-10. My STAGE-9 code fix is applied to `scripts/telegram_bot.py`.

**STAGE-9 Summary — FIX TELEGRAM MESSAGES: DONE**

Two fixes applied to `scripts/telegram_bot.py`:

1. **STARTED notification** (lines 589-595): Was `pass` (silent). Now sends `🔄 [task_id] משימה התחילה (tier) + detail preview` on every `running` transition.

2. **T0/T1 completion** (lines 612-614): Was suppressed with only a `print()`. Now sends `✅ [task_id] משימה הסתיימה + detail` — short notice without the full result dump (that stays T2/T3 only).

No logic changes made, only message wording. All messages are short and phone-readable.