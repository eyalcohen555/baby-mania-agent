# Layer 7 — Live Tagging QA Contract
**גרסה:** 1.0 | **תאריך:** 2026-05-04
**סטטוס:** ACTIVE — חובה מ-Phase 7B ואילך
**reference:** docs/organic/layer6-taxonomy-spec-v1.md

---

> **חובה בלתי ניתנת לדחייה:**
> כל live tag write ל-Shopify חייב לעבור את כל הסעיפים בחוזה זה.
> אין דרך עוקפת. אין "PASS כללי". אין "verified". אין "אין שגיאות".
> אם שדה חובה חסר — הדוח הוא FAIL, גם אם כל התגיות נכתבו.

---

## 1. כלל-על: Strong QA חובה לכל live write

לכל מוצר שנכתב ל-Shopify, חייב להיות תיעוד מלא של **כל** 11 הנקודות הבאות לפני ואחרי הכתיבה.

אסור להסתפק ב:
- "PASS כללי"
- "נראה תקין"
- "verified"
- "אין שגיאות"
- ספירת תגיות בלבד

---

## 2. Data Schema — שדות חובה לכל מוצר

לכל מוצר שנכתב, הדוח חייב להכיל את כל השדות הבאים:

```
product_id              — מזהה המוצר שנשלח ל-Shopify PUT
title_from_shopify      — הכותרת שנמשכה בפועל מ-GET
status_before           — "active" / "draft" לפני הכתיבה
before_tags             — רשימת כל התגיות לפני הכתיבה
before_tags_count       — מספר התגיות לפני
proposed_new_tags       — כל תגית שמתוכננת להוספה (רק תגיות חדשות)
proposed_new_tags_with_source — לכל תגית: source + rule + confidence
confidence_per_tag      — לכל תגית המינימום conf שהוגדר ב-taxonomy-spec
source_per_tag          — title / handle / existing_tag / variant / body / yaml
allowed_values_check    — כל תגית חדשה נבדקת מול ALLOWED_VALUES בlayer6-taxonomy-spec-v1.md
forbidden_tags_check    — תוצאת בדיקת כל הדגלים האסורים (ראה סעיף 4)
final_tags_before_write — current_tags + new_tags, מסודר, ללא כפילויות
after_tags              — רשימת התגיות שנמשכה מ-GET אחרי PUT
after_tags_count        — מספר התגיות אחרי
missing_new_tags        — תגיות שהיו ב-proposed_new_tags ולא נמצאו ב-after
removed_old_tags        — תגיות שהיו ב-before_tags ולא נמצאו ב-after
unexpected_tags         — תגיות ב-after שאינן ב-final_tags_before_write
title_changed           — "NO" / "YES" / "WARN"
status_after            — "active" / "draft" אחרי הכתיבה
rollback_needed         — YES / NO
final_verdict           — PASS / FAIL
```

אם **אחד** מהשדות חסר — הדוח הוא FAIL.

---

## 3. 11 בדיקות חובה לכל מוצר

### [1] PRODUCT ID CHECK
- product_id שבוצע עליו GET לפני ה-PUT
- title שנמשך מ-Shopify
- status (חייב להיות active לפני הכתיבה)
- לוודא שזה בדיוק המוצר לפי התוכנית

### [2] BEFORE TAGS CHECK
- GET מ-Shopify של כל התגיות לפני הכתיבה
- ספירת תגיות לפני
- שמירה בגיבוי JSON לפני כל batch

### [3] PROPOSED TAGS CHECK
- כל תגית שמתוכננת להוספה
- לכל תגית: source + rule + confidence
- כל תגית נבדקת מול ALLOWED_VALUES בטבלה הסופית ב-layer6-taxonomy-spec-v1.md §14
- תגית שאינה ב-ALLOWED_VALUES = FAIL מיידי לאותו מוצר

### [4] FORBIDDEN TAGS CHECK
חובה לוודא שאין בתגיות המוצעות:

| דגל | תיאור |
|-----|-------|
| `age-*` | prefix אסור — הוחלף ב-size-* |
| `season-unknown` | fallback tag — אסור לדחוף ל-live |
| `size-unknown` | fallback tag — אסור לדחוף ל-live |
| `gender-unknown` | fallback tag — אסור לדחוף ל-live |
| `3-6M6-9M` | malformed concatenated tag |
| תגית עם רווח | `type-romper baby` = אסור |
| תגית בעברית כתגית Layer 6/7 חדשה | Hebrew native tags = אסור (legacy Hebrew נשמר, חדש לא) |
| תגית שאינה ב-ALLOWED_VALUES | ראה §14 ב-taxonomy-spec |
| fallback inference ללא source trace | תגית שנוצרה מ-GPT/AI ללא מקור מוצהר |

### [5] SIZE SOURCE CHECK
לכל `size-*` tag חובה להוכיח:
- מקור: `variant` / `existing_clean_tag` / `title_explicit`
- אם variant:
  - שם option (כגון: "Size")
  - ערך המקור (כגון: "3-6M")
  - ערך אחרי normalization (כגון: "3-6m")
  - התגית שנוצרה (כגון: "size-3-6m")
- אין להסיק מידה מ-"toddler" / "infant" / "first-walker" בלבד
- אין להסיק מידה מטווח רחב (0-3Y) — כל מידה בנפרד

**דוגמה תקינה:**
```
variant option "Size" = "3-6M" → normalized "3-6m" → size-3-6m  conf=0.95
```

**דוגמה אסורה:**
```
"infant size" → size-0-3m  ← אסור, אין מקור מפורש
```

### [6] TYPE CHECK
לכל `type-*` tag חובה להוכיח:
- מקור מפורש (title / handle / existing_tag / yaml)
- למה זה type ספציפי ולא אחר
- confidence ≥ 0.88 (כפי שמוגדר ב-taxonomy-spec §3)

### [7] GENDER CHECK
אם יש `gender-*`:
- מקור מוכח: title / handle / existing_tag / yaml
- **לא** מוסק מצבע המוצר
- **לא** מוסק מהדפס (פרחים ≠ בנות, מכוניות ≠ בנים)
- boys + girls = gender-neutral (לא gender-girl ולא gender-boy)
- אם לא ברור → אין gender tag (לא gender-unknown ב-live)

### [8] WRITE SAFETY CHECK
לפני כל PUT לוודא:
- `final_tags = current_tags UNION new_tags` — merge בלבד
- אין מחיקה של תגיות קיימות
- אין כפילויות ב-final_tags
- PUT body מכיל רק `id` + `tags` — לא title, לא body_html, לא metafields, לא variants

### [9] AFTER WRITE VERIFY
אחרי כל PUT:
- GET מ-Shopify (לא מה-response של ה-PUT)
- ספירת תגיות אחרי
- כל תגית חדשה (proposed) נמצאת ב-after
- כל תגית ישנה (before) נמצאת ב-after
- title לא השתנה (strcmp)
- status = active
- אין age-* בתגיות after
- אין תגיות שבורות (broken encoding, garbled chars)
- אין תגיות לא מאושרות (unexpected)

### [10] FAILURE POLICY
אם **מוצר אחד** נכשל בכל שלב:

1. **עצירה מיידית** — לא עוברים למוצר הבא
2. **rollback** — רק למוצרים שכבר נכתבו באותו batch
3. **rollback source** — קובץ הגיבוי שנוצר לפני הbatch
4. **דוח FAIL מפורט** — עם פירוט מה נכשל
5. **אין PASS חלקי** — לא "10/11 מוצרים עברו" בלי פירוט על האחד שנכשל
6. **commit rollback** בנפרד עם message: `rollback(layer7): ...`

### [11] REPORT FORMAT

הדוח חייב לכלול **טבלת QA לכל מוצר** בפורמט:

| product_id | title | before_count | new_count | after_count | forbidden | miss_new | removed | title_changed | status | verdict |
|-----------|-------|-------------|----------|------------|----------|---------|---------|--------------|--------|---------|

**חסרה שורה אחת** = הדוח FAIL.

---

## 4. Pre-Batch Checklist

לפני כל batch live, חובה לאשר:

```
[ ] גיבוי JSON נוצר לכל מוצרי ה-batch לפני הכתיבה
[ ] dry run הרץ ו-PASS לכל מוצרי ה-batch
[ ] T3 approval התקבל במפורש
[ ] אין collections / Mega Menu בתוכנית
[ ] מוצרים מ-REVIEW_ONLY לא נכללים
[ ] מוצרים עם EU shoe sizes לא נכללים (עד שיש mapping)
[ ] מוצרים עם gender inferred from color לא נכללים
[ ] מוצרים עם source trace חלש (conf < 0.85) לא נכללים
[ ] batch ≤ 20 מוצרים בבת אחת
[ ] מוצר אחד בכל פעם עם verify מיידי
```

---

## 5. Reference

| מסמך | שימוש |
|------|-------|
| `docs/organic/layer6-taxonomy-spec-v1.md` §14 | ALLOWED_VALUES המלאה |
| `docs/organic/layer6-taxonomy-spec-v1.md` §13 | BLOCKED/FORBIDDEN tags |
| `docs/organic/layer6-taxonomy-spec-v1.md` §10 | SOURCE RULES + confidence minimums |
| `docs/organic/layer6-taxonomy-spec-v1.md` §11 | YAML_GAP policy |
| `output/tags/phase7a-batch2-live-verify.md` | דוגמה לdoח QA תקין |

---

## 6. היסטוריה

| גרסה | תאריך | שינוי |
|------|-------|-------|
| v1.0 | 2026-05-04 | נוצר — Strong QA Contract for all live tag writes from Phase 7B onward |

---

*חוזה זה מחייב. כל live write שמתבצע ללא עמידה בסעיפים אלה נחשב FAIL גם אם התגיות נכתבו.*
