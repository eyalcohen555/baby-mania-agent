# Bridge Task Format — Official Schema

## קובץ משימה: bridge/next-task.md

```
TASK_ID: <YYYY-MM-DD-NNN>
GOAL: <מה צריך לקרות — משפט אחד>
FILES_ALLOWED: <רשימת קבצים מותרים לגעת, מופרדים בפסיק, או * לכל קובץ>
OUTPUT_REQUIRED: <קובץ יעד + תוכן צפוי>
```

### דוגמה:
```
TASK_ID: 2026-03-25-001
GOAL: עדכן את BABYMANIA-MASTER-PROMPT.md — שנה סטטוס HUB-5 ל-DONE
FILES_ALLOWED: BABYMANIA-MASTER-PROMPT.md
OUTPUT_REQUIRED: bridge/last-result.md יכיל STATUS: PASS
```

---

## קובץ תוצאה: bridge/last-result.md

```
TASK_ID: <same id>
STATUS: PASS | FAIL
FILES_UPDATED: <list>
OUTPUT: <תיאור קצר של מה בוצע>
ERRORS: <none | תיאור שגיאה>
```

### דוגמה:
```
TASK_ID: 2026-03-25-001
STATUS: PASS
FILES_UPDATED: BABYMANIA-MASTER-PROMPT.md
OUTPUT: HUB-5 status changed to DONE on line 47
ERRORS: none
```

---

## קובץ סטטוס: bridge/status.md

מנוהל אוטומטית ע"י bridge.py ו-github-bridge.py.
ערכים אפשריים: `idle | running | done | error | pushed`
