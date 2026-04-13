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
APPROVAL_TIER: <T0 | T1 | T2 | T3>
GOAL: <מה לעשות — פעולה על קבצי הפרויקט>
FILES_ALLOWED: <קבצים מותרים לגעת, מופרדים בפסיק>
OUTPUT_REQUIRED: <מה Claude צריך להדפיס ב-stdout>
```

### ערכי APPROVAL_TIER

| ערך | משמעות | התנהגות Claude |
|-----|---------|---------------|
| `T0` | אוטומטי מלא — קריאה בלבד | מבצע בשקט |
| `T1` | Team Lead מאשר — output ביניים, journal | מבצע ומדווח |
| `T2` | Team Lead + בדיקה כפולה — קוד, config | מבצע + validator + RISK LEVEL |
| `T3` | אייל חובה — Shopify live, ארכיטקטורה | עוצר ומחזיר `AWAITING_APPROVAL` |

**שדה חובה.** אם חסר — Claude חייב לחשב לפי מטריצת ההחלטה ב-`docs/management/approval-policy.md` ולדווח את ה-Tier שנבחר.

### דוגמה:
```
TASK_ID: 2026-03-25-001
APPROVAL_TIER: T1
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
APPROVAL_TIER: <T0 | T1 | T2 | T3>
STATUS: PASS | FAIL | AWAITING_APPROVAL
FILES_UPDATED: <list>
OUTPUT: <תיאור קצר>
ERRORS: <none | תיאור>
```

> אם `APPROVAL_TIER: T3` ואין אישור אייל → Claude מחזיר `STATUS: AWAITING_APPROVAL` ולא מבצע.

---

## קובץ סטטוס: bridge/status.md

מנוהל אוטומטית ע"י bridge.py ו-github-bridge.py.
ערכים: `idle | running | done | error | pushed | awaiting_approval`

---

## תוספת — Template למשימה אורגנית

**כשהמשימה שייכת לפעילות אורגנית, יש להוסיף את השדות הבאים:**

```
TASK_ID: <YYYY-MM-DD-NNN>
APPROVAL_TIER: <T0 | T1 | T2 | T3>
DOMAIN: ORGANIC
STATE_FILE: docs/organic/מצב-הפרויקט-האורגני.md
STATE_CHECK_REQUIRED: YES
GOAL: <מה לעשות>
FILES_ALLOWED: <קבצים מותרים>
OUTPUT_REQUIRED: הדפס STATE_CHECK_BLOCK + TASK_ID + STATUS: PASS + FILES_UPDATED
```

**בלוק STATE_CHECK חובה בתחילת כל output אורגני:**

```
STATE FILE READ: YES
CURRENT LAYER: [שכבה נוכחית — לדוגמה: LAYER 2b]
NEXT OPEN ITEM: [הפריט הפתוח הראשון לפי state doc]
WHY THIS TASK NOW: [נימוק — למה משימה זו ולא אחרת]
WHAT IS BLOCKED AFTER THIS: [מה ייפתח / מה עדיין חסום]
```

**כלל מפעיל:** אם `DOMAIN: ORGANIC` קיים בmשימה — בלוק זה חובה לפני כל output אחר.
אם state doc לא נקרא או לא ניתן לפתור — דווח `ORGANIC_STATE_UNRESOLVED` ועצור.

### דוגמה — משימת פרסום HUB-8:
```
TASK_ID: 2026-04-14-001
APPROVAL_TIER: T3
DOMAIN: ORGANIC
STATE_FILE: docs/organic/מצב-הפרויקט-האורגני.md
STATE_CHECK_REQUIRED: YES
GOAL: פרסם את מאמרי HUB-8 לShopify — 6 מאמרים מ-output/hub8/
FILES_ALLOWED: output/hub8/, teams/organic/hub-registry.json, output/site-map/internal_content_map.json
OUTPUT_REQUIRED: STATE_CHECK_BLOCK + TASK_ID + STATUS: PASS + ARTICLES_PUBLISHED
```
