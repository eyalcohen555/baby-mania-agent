# Bridge Task Format — Official Schema

## עקרון הפעולה

```
bridge.py קורא next-task.md
        ↓
מריץ: claude.cmd --print --dangerously-skip-permissions "<task>"
        ↓
לוכד stdout של Claude
        ↓
כותב stdout → last-result.md
```

**RULE:** המשימה לעולם לא מבקשת מ-Claude לכתוב ל-`last-result.md`.
Claude מבצע עבודה ומדפיס תוצאה — bridge.py לוכד ושומר.

---

## קובץ משימה: bridge/next-task.md

```
TASK_ID: <YYYY-MM-DD-NNN>
GOAL: <מה לעשות — פעולה על קבצי הפרויקט>
FILES_ALLOWED: <קבצים מותרים לגעת, מופרדים בפסיק>
OUTPUT_REQUIRED: <מה Claude צריך להדפיס ב-stdout>
```

### דוגמה:
```
TASK_ID: 2026-03-25-001
GOAL: עדכן שורה 12 בקובץ BABYMANIA-MASTER-PROMPT.md — שנה HUB-5 מ-IN_PROGRESS ל-DONE
FILES_ALLOWED: BABYMANIA-MASTER-PROMPT.md
OUTPUT_REQUIRED: הדפס TASK_ID + STATUS: PASS + FILES_UPDATED
```

---

## קובץ תוצאה: bridge/last-result.md

**מנוהל ע"י bridge.py בלבד — לא ע"י Claude.**
מכיל את ה-stdout שהדפיס Claude.

פורמט מצופה ב-stdout של Claude:
```
TASK_ID: <same id>
STATUS: PASS | FAIL
FILES_UPDATED: <list>
OUTPUT: <תיאור קצר>
ERRORS: <none | תיאור>
```

---

## קובץ סטטוס: bridge/status.md

מנוהל אוטומטית ע"י bridge.py ו-github-bridge.py.
ערכים: `idle | running | done | error | pushed`
