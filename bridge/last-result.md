I've traced the full approval cycle. Here's what I found:

## מעגל ה-Approval — מצב נוכחי

### הזרימה:
```
1. bridge.py מריץ משימה → Claude כותב תוצאה → last-result.md
2. telegram_bot.py מזהה "נדרש אישור" בתוצאה → שולח כפתורים (אשר/דחה) לטלגרם
3. משתמש לוחץ כפתור → telegram_bot.py כותב ל-telegram-response.md
4. bridge.py (consume_telegram_response) קורא את הקובץ, מנקה אותו
```

### הבעיה: **המעגל לא סגור**

`bridge.py` שורות 167-175 — אחרי שצורך את התגובה, הוא רק:
- מדפיס לקונסול
- מעדכן status ל-idle

**אבל לא עושה שום דבר עם התגובה** — לא מפעיל את המשימה הבאה, לא מעביר approve/reject חזרה ל-Claude, ולא כותב ל-next-task.md.

### מה עובד:
- זיהוי אירועים (`detect_result_event`) — תקין
- כפתורים בטלגרם (`send_approval_prompt`) — תקין
- כתיבת תגובה (`write_response`) — תקין
- צריכת תגובה (`consume_telegram_response`) — תקין
- Safety: לא דורסים תגובה שלא נקראה — תקין

### מה חסר:
בעצם ה-bridge צריך **לפעול לפי התגובה** — למשל:
- `approve` → להריץ את next-task.md הבא (או לשלוח ל-Claude פקודת המשך)
- `reject` → לכתוב FAIL ולעצור
- `answer` → להזריק את התשובה למשימה חדשה

רוצה שאוסיף את הלוגיקה החסרה ל-bridge.py כדי לסגור את המעגל?
