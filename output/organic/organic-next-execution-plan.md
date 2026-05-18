# ORGANIC NEXT EXECUTION PLAN
**תאריך:** 2026-05-17
**גרסה:** 1.0
**צוות:** Organic
**מאשר:** ממתין לאישור אייל לפני ביצוע כל שלב T2/T3

---

## A. SYSTEM STATE

### מצב שכבות

| שכבה | סטטוס | פרטים |
|---|---|---|
| Layer 3 — Product SEO | COMPLETE | 244 מוצרים |
| Layer 4 — GEO Tags | COMPLETE | 241 מוצרים |
| Layer 6 — Smart Tagging | COMPLETE | 218 מוצרים, 6 Smart Collections |
| Layer 7 — QA Contract | ACTIVE | 11 checks חובה לכל write |
| Phase 7C — Clothing Tags | COMPLETE | 177+ clothing tagged live |
| Phase 8 — Navigation | COMPLETE | 6 Smart Collections, nav updated |

### תכן מאמרים חי

| מדד | ערך |
|---|---|
| מאמרים live | 68 (HUB-1 עד HUB-11) |
| HUB אחרון שפורסם | HUB-11 — בגדי קיץ לתינוק |
| תאריך פרסום אחרון | 2026-04-29 |
| ימים ללא פרסום | **18 ימים** |
| HUB הבא מתוכנן | HUB-12 — לא בוצע עדיין |

### תיוג נעליים

| מדד | ערך |
|---|---|
| מוצרי נעליים מסווגים | 65/65 ✅ |
| פריטי REVIEW פתוחים | 0 ✅ |
| חבילת T3 קיימת | YES — shoes-live-tagging-t3-approval-packet.md (2026-05-12) |
| סקריפט מוכן | YES — scripts/t3_shoe_tagging.py |
| Rollback מוכן | YES — scripts/t3_rollback.py |

### Shopify API

| מדד | ערך |
|---|---|
| סטטוס | **403 STILL_DISABLED** |
| שגיאה | `[API] API Access has been disabled` |
| בדיקה אחרונה | 2026-05-17 (T0 test) |
| סיבה | Shopify Partner Governance — security incident |
| טיקט | 551d1c4c |

### מה חסום

- כל קריאות Shopify API (GET + PUT + POST)
- Live write נעליים (T3)
- פרסום מאמרים דרך API
- אימות לאחר תיוג

### מה בטוח לבצע עכשיו

- שחזור / אישור חבילת T3 נעליים מקומית
- Dry-run simulation מקומי
- ייצור טיוטות מאמרים מקומי
- QA מקומי על מאמרים
- תכנון HUB-12

---

## B. WORKSTREAM S — SHOES TAGGING

### Stage S1 — אישור חבילת T3

**מטרה:** לוודא שחבילת T3 תקפה ומלאה לפני שה-API יחזור.

**סטטוס:** `shoes-live-tagging-t3-approval-packet.md` קיים (2026-05-12). לוודא:

**בדיקת פיזור תגים (65 מוצרים):**

| תג | כמות | סטטוס |
|---|---|---|
| shoes-sandals | 21 | ✅ |
| shoes-sneakers | 16 | ✅ |
| shoes-sneakers + shoes-lights | 8 | ✅ |
| shoes-first-step | 5 | ✅ |
| shoes-first-step + shoes-anti-slip | 4 | ✅ |
| shoes-boots | 5 | ✅ |
| shoes-occasion | 3 | ✅ |
| shoes-water | 3 | ✅ |
| **סה"כ** | **65** | ✅ |

**פעולה:** קרא את הקובץ. אשר 65/65 ואפס REVIEW פתוח. דווח PASS/FAIL.

**קבצים מורשים:**
- `output/tags/shoes-live-tagging-t3-approval-packet.md`
- `output/tags/shoes-tagging-ready-for-review-v2.md`

**פלט צפוי:**
```
PACKET_EXISTS: YES
PRODUCTS_COUNT: 65
REVIEW_OPEN: 0
TAG_DISTRIBUTION: PASS
S1_VERDICT: PASS / FAIL
```

---

### Stage S2 — שחזור חבילה (אם חסרה)

**מטרה:** אם S1 FAIL — בנה מחדש חבילת T3 מקומית.

**תנאי הפעלה:** S1 FAIL בלבד.

**קבצי מקור:**
- `output/tags/shoes-tagging-ready-for-review-v2.md`
- `output/tags/all-shoes-from-600-title-scan.json`
- `scripts/t3_shoe_tagging.py` (classify logic)

**תוכן חבילה נדרש:**
```
לכל מוצר (65 שורות):
  product_id | title | handle | tags_current | tags_target | reason | confidence
```

**פלט:**
- `output/tags/shoes-live-tagging-t3-approval-packet-rebuilt.md`

**Shopify writes:** NONE

---

### Stage S3 — Backup Plan

**מטרה:** הגדר את artifact הגיבוי שחייב להיווצר לפני כל live write.

**תנאי:** Backup חייב להיווצר ב-Phase 1 של `t3_shoe_tagging.py` בזמן ריצה.

**מבנה backup נדרש לכל מוצר:**
```json
{
  "id": "<product_id>",
  "title": "<title>",
  "handle": "<handle>",
  "tags_before": "<current tags string>",
  "timestamp": "<ISO timestamp>"
}
```

**נתיב:** `output/tags/backup/shoes-tags-backup-<YYYYMMDD-HHMMSS>.json`

**כלל:** אם backup נכשל ב-3+ מוצרים — ABORT, לא להמשיך ל-live write.

**פעולה עכשיו:** אין (backup נוצר רק כשה-API חוזר ו-T3 מאושר).

---

### Stage S4 — Dry-Run Plan (מקומי)

**מטרה:** סימולציה מקומית של שינויי תגים — בלי כתיבה לשופיפיי.

**פעולה:** הרץ dry-run simulation על בסיס classify logic:

```python
# קרא: output/tags/all-shoes-from-600-title-scan.json
# הרץ: classify(product) לכל 65 מוצרים
# בדוק: merge_tags(tags_before="", new_tags)
# פלט: לכל מוצר — tags_before, tags_after, added, removed
# שמור: output/tags/dry-run/shoes-dry-run-local-<timestamp>.json
```

**בדיקות חובה בdry-run:**

| בדיקה | כלל | FAIL אם |
|---|---|---|
| age-* tags | אסור | נמצא age- כלשהו |
| type/gender conflict | אסור | shoes + clothing tag אחד |
| EU size tags | אסור | נמצא EU- כלשהו |
| כפילויות | אסור | תג מופיע פעמיים |
| מוצר לא-נעל | אסור | classify מחזיר None |
| removals | אסור | removed[] לא ריק |

**סקריפט:** dry-run כבר מובנה בתוך `scripts/t3_shoe_tagging.py` כ-Phase 2.

**פלט צפוי:**
```
DRY_RUN_PRODUCTS: 65
REMOVALS: 0
CONFLICTS: 0
AGE_TAGS: 0
DUPLICATES: 0
DRY_RUN_VERDICT: PASS / FAIL
```

---

### Stage S5 — Live T3 Gate (חסום עד לפתיחת API)

**מטרה:** הגדרת טקסט האישור המדויק שאייל חייב לשלוח.

**תנאי הרצה — כל 4 חייבים להתקיים:**

```
1. API returns 200 (T0 test PASS)
2. Backup קיים (output/tags/backup/*.json)
3. Dry-run PASS (0 removals, 0 conflicts)
4. אייל שולח בדיוק:
   "APPROVED T3 GO — נעליים"
```

**פקודת הרצה (לאחר אישור):**
```
py scripts/t3_shoe_tagging.py
```

**ה-script יבצע:**
- Phase 0: connectivity test
- Phase 1: backup (65 GETs)
- Phase 2: dry-run (local diff)
- Phase 3: live write (65 PUTs, 0.55s delay)
- Phase 4: verify (65 GETs)

**זמן הרצה משוער:** ~4 דקות (65 × 0.55s × 3 phases ≈ 107s + overhead)

---

### Stage S6 — Verify לאחר live

**מטרה:** אימות שכל 65 מוצרים קיבלו את התגים הנכונים.

**פלט:** `output/tags/verify/shoes-verify-<timestamp>.json`

**קריטריון הצלחה:**
```
PASS: 65/65
FAIL: 0
STATUS: SUCCESS
```

**Layer 7 QA Contract — 11 checks לכל מוצר:**
1. תג נמצא בפועל ב-Shopify
2. אין age-* tags
3. אין EU-size tags
4. אין removals של תגים ישנים
5. אין type/gender conflicts
6. אין כפילויות
7. confidence ≥ HIGH
8. title match לclassification
9. handle match (אם רלוונטי)
10. מוצר active (לא draft/archived)
11. backup קיים לפני write

---

## C. WORKSTREAM A — ARTICLE PRODUCTION

### Stage A1 — Backlog Audit

**מצב נוכחי:**
- 68 מאמרים live (HUB-1 עד HUB-11)
- HUB-11 הושלם: 2026-04-29 (7 מאמרים, בגדי קיץ לתינוק)
- **18 ימים ללא פרסום**
- HUB-12: לא קיים ב-hub-registry.json
- טיוטות HUB-12: לא נמצאו

**פעולה:** סרוק קבצים אלה לגילוי טיוטות קיימות:
```
output/organic/
output/organic/hub12/
docs/organic/
```

**פלט:**
```
DRAFTS_FOUND: YES / NO
DRAFTS_COUNT: N
HUB_DECISION_NEEDED: YES / NO
```

---

### Stage A2 — החלטת Batch תוכן

**המלצה:** בהיעדר טיוטות HUB-12 — בנה HUB-12 מלא מקומית.

**נושא מוצע: HUB-12 — בגדי שמחה לתינוק**
(Occasion/celebration clothing — משלים את HUB-11 קיץ ו-HUB-10 חורף)

**לוגיקת Topic Cluster:**
- HUB-10: בגדי חורף → HUB-11: בגדי קיץ → **HUB-12: בגדי שמחה** (אוקזיון)

**מבנה HUB-12 מוצע (7 מאמרים):**

| # | סוג | נושא |
|---|---|---|
| P | Pillar | מדריך מלא לבגדי שמחה לתינוקות — ברית/בר מצוה/חתונה/ימי הולדת |
| C1 | Cluster | בגדי ברית לבנים — מה ללבוש ואיך לבחור |
| C2 | Cluster | שמלות שמחה לבנות — סגנון לכל אירוע |
| C3 | Cluster | בגדי שמחה לגיל שנה — טרנדים ומדריך מידות |
| C4 | Cluster | איך להלביש תינוק לחתונה — 5 כלים שחייבים לדעת |
| C5 | Cluster | בגדי שמחה לתינוק — שאלות נפוצות ותשובות |
| C6 | Cluster | סטים לאירועים לתינוקות — המדריך לרכישה נכונה |

---

### Stage A3 — ייצור מאמרים מקומי

**כלי:** `.claude/skills/babymania-organic-article-production/SKILL.md` — 8 שלבים.

**לכל מאמר (7 × 7 שלבים):**

```
שלב 1 — Planning: SEO title, meta, slug, topic cluster position
שלב 2 — Writing: body_html עברית, 1200-2000 מילה
שלב 3 — Images: 2 תמונות מינימום, CDN Shopify, alt text בעברית
שלב 4 — QA: 8/8 checks (ראה Stage A4)
שלב 5 — Ayal Sign-Off: הצג לאייל לפני publish
שלב 6 — Pipeline: אין publish ללא API
שלב 7 — Verify: N/A עד API פתוח
שלב 8 — GSC: לאחר publish
```

**פלט לכל מאמר:**
```
output/organic/hub12/<slug>.md
```

---

### Stage A4 — Organic QA

**8 בדיקות חובה לכל מאמר:**

| בדיקה | כלל | FAIL אם |
|---|---|---|
| Inline styles | אסור | style= נמצא |
| Hero בbody_html | אסור | <img class="hero"> בתוך body |
| Video | אסור | <video> כלשהו |
| תמונות | מינימום 2 | נמצאות פחות מ-2 |
| Internal links | חובה | 0 קישורים פנימיים |
| Product bridge | חובה | אין קישור למוצר |
| עברית | חובה | תוכן באנגלית בלתי מוסבר |
| FAQ | חובה | חסר לחלוטין |

---

### Stage A5 — Publish Packet

**פלט:** `output/organic/hub12/hub12-publish-packet.md`

**תוכן:**
```
סדר publish: P → C1 → C2 → C3 → C4 → C5 → C6
blog_id: 109164036409
publish_command: py scripts/create_blog_article.py --hub 12
fallback: Shopify Admin ידני (אם API עדיין חסום)
```

**הגבלה:** אין publish ללא אישור אייל + API פתוח.

---

## D. CONDUCTOR YAML PLAN

קובץ: `plans/organic-shoes-and-articles-local-prep-001.yaml`
(פורמט מלא — ראה קובץ YAML נפרד)

---

## E. DAY WORK PRIORITY

```
עדיפות 1: Stage S1 — אשר חבילת T3 נעליים (15 דקות)
עדיפות 2: Stage S4 — הרץ dry-run מקומי (30 דקות)
עדיפות 3: Stage A1 — בדוק backlog מאמרים (10 דקות)
עדיפות 4: Stage A2-A3 — ייצר HUB-12 מקומית (2-4 שעות)
HOLD: Stage S5 — live write (חסום עד API + "APPROVED T3 GO — נעליים")
HOLD: Stage A5 — publish (חסום עד API)
NEVER: navigation work לפני T3 נעליים
```

---

## APPROVAL GATE SUMMARY

| שלב | Tier | בלוק עד |
|---|---|---|
| S1 — אשר packet | T0 | — |
| S2 — שחזור packet | T1 | S1 FAIL |
| S3 — backup plan | T0 | — |
| S4 — dry-run מקומי | T0 | — |
| S5 — live write | **T3** | API 200 + backup + dry-run PASS + "APPROVED T3 GO — נעליים" |
| S6 — verify | T0 | S5 done |
| A1 — backlog audit | T0 | — |
| A2 — HUB decision | T1 | A1 done |
| A3 — production | T1 | A2 approved |
| A4 — QA | T0 | A3 done |
| A5 — publish packet | T0 | A4 PASS |
| Publish live | **T3** | API 200 + Ayal approval |
