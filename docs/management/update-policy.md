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

## Post-Publish Flow — חובה לכל מאמר/HUB אורגני חדש

```
שלב 1: publish          → POST /blogs/{id}/articles.json → expect 201
שלב 2: verify           → GET article_id → confirm published_at != null
שלב 3: GSC inspect      → python scripts/submit_gsc.py <url>  [בדיקת סטטוס]
שלב 3b: GSC request     → GSC UI: URL Inspection → "Request Indexing"  [ידני]
שלב 4: docs update      → hub-registry.json + organic-journal.md + מצב-הפרויקט-האורגני.md
```

### API LIMITATION (חשוב)
Google **לא מספק API** לבקשת indexing עבור מאמרי בלוג רגילים.
- `scripts/submit_gsc.py` — משתמש ב-Search Console URL Inspection API: **בדיקת סטטוס בלבד**
- "Request Indexing" חייב להתבצע **ידנית** דרך GSC UI:
  `GSC → URL Inspection → הדבק URL → "Request Indexing"`

### סטטוסי GSC ב-hub-registry.json

| סטטוס | מתי | script / ידני |
|-------|-----|----------------|
| `gsc_pending` | published, inspection טרם בוצע | — |
| `gsc_unknown` | inspection רץ, Google לא מכיר את ה-URL | script output |
| `gsc_pending_manual_request` | inspection רץ, manual request עדיין לא בוצע ב-GSC UI | אחרי script, לפני UI |
| `gsc_inspected` | inspection רץ וסטטוס ידוע | script ran |
| `gsc_indexed` | URL אושר כ-indexed על ידי Google | script / GSC UI |
| `gsc_crawled_not_indexed` | גוגל סרק אבל לא אינדקס — לבדוק סיבה | script output |

**הבדל קריטי:**
- `gsc_unknown` = תוצאת ה-inspection (מה Google יודע על ה-URL)
- `gsc_pending_manual_request` = סטטוס action (מה עוד צריך לעשות ידנית)
- HUB שהסתיים inspection + לא בוצע manual request → `gsc_pending_manual_request`

### GSC Credentials
```
service account: gsc-access@babymania-001.iam.gserviceaccount.com
property (GSC): https://www.babymania-il.com/  (siteOwner)
scope: https://www.googleapis.com/auth/webmasters
credentials: C:\Users\3024e\Downloads\קלוד קוד\babymania-001-8baf1b2408d7.json
env var: GSC_SERVICE_ACCOUNT_JSON (ב-.env)
inspect: python scripts/submit_gsc.py <url> [url2 ...]
```

> **כלל:** publish complete ≠ FULLY COMPLETE.
> FULLY COMPLETE = publish + verify + `gsc_pending_manual_request` (inspection רץ) + manual Request Indexing + docs.

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
