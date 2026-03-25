# BabyMania — Update Policy
**תפקיד:** חוקי עדכון ברורים — מה מעדכנים, מתי, ואיך.
**כלל:** אחרי כל 3–5 משימות משמעותיות — journal update חובה.

---

## מה הוא כל קובץ

### MASTER PROMPT = חוקה + snapshot
- מכיל: מצב שוטף, סוכנים, HUBs, חוקים, פורמטים
- **אינו מכיל:** היסטוריה מפורטת, logs, debugging notes
- **עדכון ע"י:** Claude Code דרך bridge task

### JOURNAL = יומן תחום
- מכיל: כל מה שקרה בתחום — ביצוע, blockers, החלטות, next step
- **עדכון ע"י:** Claude Code דרך bridge task אחרי כל משימה משמעותית

---

## מתי לעדכן MASTER PROMPT

| אירוע | חובה? |
|-------|--------|
| Blocker משמעותי נסגר | ✅ חובה |
| Agent חדש נוסף לpipeline | ✅ חובה |
| קטגוריה חדשה / HUB חדש | ✅ חובה |
| החלטה ארכיטקטונית | ✅ חובה |
| כל 3 שינויים ב-שכבה אחת | ✅ חובה |
| לפני handoff / chat חדש | ✅ חובה |
| תיקון קטן שאינו משנה מצב | ❌ לא נדרש |
| audit בלבד ללא שינויים | ❌ לא נדרש |

---

## מתי לעדכן JOURNAL

| אירוע | Journal לעדכן |
|-------|----------------|
| כל משימה שמשנה קוד/קבצים | Journal הרלוונטי לתחום |
| Blocker נמצא | Journal + OPEN ISSUES |
| Blocker נסגר | Journal + NEXT STEP |
| החלטת ניהול רחבה | management-journal.md |
| שינוי workflow | management-journal.md |
| שינוי bridge / runtime | bridge-operations-journal.md |
| שינוי shoes pipeline | shoes-journal.md |
| שינוי clothing | clothing-journal.md |
| שינוי orchestrator/config | infrastructure-journal.md |
| HUB חדש / organic שינוי | organic-journal.md |

---

## חוקי Handoff (לפני מעבר chat)

```
לפני סגירת chat — חובה:
1. עדכן NEXT STEP בjournal הרלוונטי
2. עדכן SYSTEM STATE בjournal
3. אם היה milestone — עדכן גם MASTER PROMPT
4. אל תשאיר open issues רק בראש — כתוב אותם בקובץ
```

---

## מה נחשב "משימה משמעותית"

**כן — משמעותית:**
- שינוי בקובץ agent
- שינוי בorchestrator / config
- סגירת blocker
- הוספת agent / stage
- שינוי ב-bridge / runtime
- הוספת HUB / milestone

**לא — לא משמעותית:**
- קריאת קבצים בלבד
- audit ללא שינויים
- תיקון typo קל
- הפקת output ביניים

---

## פורמט עדכון master (bridge task)

```
TASK_ID: YYYY-MM-DD-master-update
GOAL: עדכן BABYMANIA-MASTER-PROMPT.md — [מה בדיוק]
FILES_ALLOWED: BABYMANIA-MASTER-PROMPT.md
OUTPUT_REQUIRED: הדפס TASK_ID + STATUS: PASS + שורות שעודכנו
```

## פורמט עדכון journal (bridge task)

```
TASK_ID: YYYY-MM-DD-journal-[domain]
GOAL: עדכן docs/[path]/[journal].md — הוסף entry מתאריך היום
FILES_ALLOWED: docs/[path]/[journal].md
OUTPUT_REQUIRED: הדפס TASK_ID + STATUS: PASS
```
