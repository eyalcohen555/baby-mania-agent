# Layer 6 — Phase 6 Small Live Batch Plan
**תאריך:** 2026-05-04
**Phase:** 6 — Small Live Batch Plan — **תכנון בלבד**
**STATUS: PENDING T3 APPROVAL — אין כתיבה ל-Shopify**

---

> **חובה:** מסמך זה הוא תכנון בלבד.
> אין שינויים ב-Shopify עד שאייל מאשר (T3).
> Phase 6 NOT OPEN. Shopify live = NO.

---

## 1. SYSTEM STATE

| פרמטר | ערך |
|-------|-----|
| Phase 5k | COMPLETE (commit 3f953f0) |
| SAFE_FOR_PHASE6 | **5** (C1, C2, C3, C4, C5) |
| Phase 6 | **NOT OPEN** |
| Shopify live | **NO** |
| T3 approval (אייל) | **PENDING** |
| age-* tags | 0 ✅ |
| taxonomy_gaps | 0 ✅ |
| blocked_pct | 0.0% ✅ |
| avg quality score (Phase 5k) | 83.5 ✅ |

---

## 2. SELECTED BATCH

**Batch ראשון: 3 מוצרים** — C3, C2, C4 (לפי score יורד)

| # | candidate | product_id | כותרת | score | verdict |
|---|-----------|-----------|-------|-------|---------|
| 1 | **C3** | 9688660312377 | אוברול ג׳ינס דגם אתי | **97.4** | SAFE_FOR_PHASE6 |
| 2 | **C2** | 9874906349881 | אוברול ג'ינס מתוק מבית בייבי מניה דגם זוהר | **97.2** | SAFE_FOR_PHASE6 |
| 3 | **C4** | 9895864205625 | אוברול ג'ינס יוניסקס לתינוקות דגם שלו | **95.7** | SAFE_FOR_PHASE6 |

**הרחבה אפשרית (לא ברירת מחדל):**
אם batch ראשון עובר verify ללא בעיות, batch שני:
- C5 (9687579033913) — score 91.2 — 5 מידות (0-3m עד 12-18m)
- C1 (9688932909369) — score 88.8 — גבול הסף

**למה C3, C2, C4 ולא C5/C1 כברירת מחדל:**
C3 ו-C2 הם הציונים הגבוהים ביותר עם מקורות ברורים לכל שדה חובה.
C4 נוסף לבדיקת תיקון ה-normalization של Phase 5k בסביבה חיה.
C5 ו-C1 ישמרו ל-batch שני אם batch ראשון מצליח.

### לכל מועמד — source trace ו-why safe

**C3 — 9688660312377:**
- type-romper: existing Hebrew tag "אוברול" (confidence 0.88)
- size-3-6m/6-9m/9-12m/12-18m: Shopify variant option "מידה" (confidence 0.95 each)
- season-spring-fall: handle "spring-fall" (confidence 0.85)
- fabric-denim: handle "denim" (confidence 0.90)
- gender-girl: handle "girls" (confidence 0.90)
- כל 8 gates: PASS. כל מקורות traceable. אין inference אסור.

**C2 — 9874906349881:**
- type-romper: existing Hebrew tag "אוברול" (confidence 0.88)
- size-3-6m/6-9m/9-12m: Shopify variant option "מידה" (confidence 0.95 each)
- season-summer: handle "baby-summer-clothing" (confidence 0.88)
- fabric-denim: title "ג'ינס" (confidence 0.90)
- gender-neutral: handle "boys-girls" (confidence 0.85)
- style-casual: title "casual" (confidence 0.80)
- כל 8 gates: PASS. כל מקורות traceable.

**C4 — 9895864205625:**
- type-romper: existing Hebrew tag "אוברול" (confidence 0.88)
- size-0-3m/3-6m/9-12m/12-18m: Shopify variant option "מידה" (conf 0.95) — Phase 5k normalization fix
- season-unknown: fallback (conf 0.0 — אין signal עונה)
- fabric-denim: handle "denim" (confidence 0.90)
- gender-neutral: title "יוניסקס" (confidence 0.85)
- style-casual: title "casual" (confidence 0.80)
- כל 8 gates: PASS, score 95.7.

---

## 3. EXACT TAGS TO ADD

מדיניות: **להוסיף בלבד**. לא למחוק תגיות קיימות. לא לשנות title, description, metafields.

### C3 — 9688660312377 — אוברול ג׳ינס דגם אתי

**תגיות קיימות (לא לגעת):**
```
אוברול
```

**תגיות Layer 6 להוספה:**

| tag | cat | conf | source | PUSH? |
|-----|-----|------|--------|-------|
| type-romper | CAT-A | 0.88 | existing_tag "אוברול" | **PUSH** |
| size-3-6m | CAT-B | 0.95 | variant option "מידה" | **PUSH** |
| size-6-9m | CAT-B | 0.95 | variant option "מידה" | **PUSH** |
| size-9-12m | CAT-B | 0.95 | variant option "מידה" | **PUSH** |
| size-12-18m | CAT-B | 0.95 | variant option "מידה" | **PUSH** |
| season-spring-fall | CAT-C | 0.85 | handle "spring-fall" | **PUSH** |
| fabric-denim | CAT-D | 0.90 | handle "denim" | **PUSH** |
| occ-everyday | CAT-E | 0.60 | category_default | **SKIP** (conf 0.60 < 0.80) |
| gender-girl | CAT-F | 0.90 | handle "girls" | **PUSH** |
| style-modern | CAT-G | 0.78 | body | **SKIP** (conf 0.78 < 0.80) |

**תגיות שיתווספו בפועל (8):**
`type-romper, size-3-6m, size-6-9m, size-9-12m, size-12-18m, season-spring-fall, fabric-denim, gender-girl`

---

### C2 — 9874906349881 — אוברול ג'ינס מתוק מבית בייבי מניה דגם זוהר

**תגיות קיימות (לא לגעת):**
```
אוברול
```

**תגיות Layer 6 להוספה:**

| tag | cat | conf | source | PUSH? |
|-----|-----|------|--------|-------|
| type-romper | CAT-A | 0.88 | existing_tag "אוברול" | **PUSH** |
| size-3-6m | CAT-B | 0.95 | variant option "מידה" | **PUSH** |
| size-6-9m | CAT-B | 0.95 | variant option "מידה" | **PUSH** |
| size-9-12m | CAT-B | 0.95 | variant option "מידה" | **PUSH** |
| season-summer | CAT-C | 0.88 | handle "baby-summer-clothing" | **PUSH** |
| fabric-denim | CAT-D | 0.90 | title "ג'ינס" | **PUSH** |
| occ-everyday | CAT-E | 0.60 | category_default | **SKIP** (conf 0.60 < 0.80) |
| gender-neutral | CAT-F | 0.85 | handle "boys-girls" | **PUSH** |
| style-casual | CAT-G | 0.80 | title "casual" | **PUSH** |

**תגיות שיתווספו בפועל (8):**
`type-romper, size-3-6m, size-6-9m, size-9-12m, season-summer, fabric-denim, gender-neutral, style-casual`

---

### C4 — 9895864205625 — אוברול ג'ינס יוניסקס לתינוקות דגם שלו

**תגיות קיימות (לא לגעת):**
```
אוברול
```

**תגיות Layer 6 להוספה:**

| tag | cat | conf | source | PUSH? |
|-----|-----|------|--------|-------|
| type-romper | CAT-A | 0.88 | existing_tag "אוברול" | **PUSH** |
| size-0-3m | CAT-B | 0.95 | variant option "מידה" (Phase 5k fix) | **PUSH** |
| size-3-6m | CAT-B | 0.95 | variant option "מידה" | **PUSH** |
| size-9-12m | CAT-B | 0.95 | variant option "מידה" | **PUSH** |
| size-12-18m | CAT-B | 0.95 | variant option "מידה" | **PUSH** |
| season-unknown | CAT-C | 0.00 | category_default (fallback) | **SKIP** (fallback, אין signal) |
| fabric-denim | CAT-D | 0.90 | handle "denim" | **PUSH** |
| occ-everyday | CAT-E | 0.60 | category_default | **SKIP** (conf 0.60 < 0.80) |
| gender-neutral | CAT-F | 0.85 | title "יוניסקס" | **PUSH** |
| style-casual | CAT-G | 0.80 | title "casual" | **PUSH** |

**תגיות שיתווספו בפועל (8):**
`type-romper, size-0-3m, size-3-6m, size-9-12m, size-12-18m, fabric-denim, gender-neutral, style-casual`

> **הערה C4:** season-unknown מושמט — אין signal עונה. לא תיווסף תגית season. CAT-C יישאר ריק עבור C4 בפועל.

---

## 4. BACKUP PLAN

**לפני כל כתיבה:**

1. לבצע fetch של כל שלושת המוצרים מ-Shopify
2. לשמור גיבוי:

```
output/tags/phase6-small-batch-tags-backup.json
```

**מבנה הקובץ:**

```json
{
  "backup_timestamp": "YYYY-MM-DDTHH:MM:SS",
  "phase": "Phase 6 small batch pre-write backup",
  "products": [
    {
      "product_id": "9688660312377",
      "title": "אוברול ג׳ינס דגם אתי",
      "current_tags": ["אוברול"],
      "proposed_new_tags": ["type-romper","size-3-6m","size-6-9m","size-9-12m","size-12-18m","season-spring-fall","fabric-denim","gender-girl"],
      "final_tags_after_write": ["אוברול","type-romper","size-3-6m","size-6-9m","size-9-12m","size-12-18m","season-spring-fall","fabric-denim","gender-girl"]
    },
    {
      "product_id": "9874906349881",
      "title": "אוברול ג'ינס מתוק מבית בייבי מניה דגם זוהר",
      "current_tags": ["אוברול"],
      "proposed_new_tags": ["type-romper","size-3-6m","size-6-9m","size-9-12m","season-summer","fabric-denim","gender-neutral","style-casual"],
      "final_tags_after_write": ["אוברול","type-romper","size-3-6m","size-6-9m","size-9-12m","season-summer","fabric-denim","gender-neutral","style-casual"]
    },
    {
      "product_id": "9895864205625",
      "title": "אוברול ג'ינס יוניסקס לתינוקות דגם שלו",
      "current_tags": ["אוברול"],
      "proposed_new_tags": ["type-romper","size-0-3m","size-3-6m","size-9-12m","size-12-18m","fabric-denim","gender-neutral","style-casual"],
      "final_tags_after_write": ["אוברול","type-romper","size-0-3m","size-3-6m","size-9-12m","size-12-18m","fabric-denim","gender-neutral","style-casual"]
    }
  ]
}
```

**הכלל:** אם verify נכשל — מחזירים את `current_tags` בלבד מתוך הגיבוי.

---

## 5. FINAL DRY RUN PLAN

**לפני כל כתיבה — לבצע בדיקה אחרונה:**

```python
python scripts/tags/run_layer6_phase5k_dryrun.py
```

**בדיקות שחייבות לעבור:**

| בדיקה | תנאי |
|-------|------|
| כל התגים באנגלית ASCII | `re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)+$', tag)` |
| אין age-* tags | לא קיים שום tag שמתחיל ב-`age-` |
| אין תגיות שבורות | אין `3-6M6-9M`, אין spaces בתוך tag |
| כל size-* מגיע מ-variant source | source=existing_tag, detail=variant_option |
| אין tag לא מאושר | כל tag ב-ALLOWED_VALUES |
| אין מחיקת תגיות קיימות | current_tags כלולים ב-final_tags |
| taxonomy_gaps = 0 | לא נוצרו tags חדשים מחוץ לspec |
| C3, C2, C4 final_status = PASS | כל 8 gates עוברים |

**אם אחד מהתנאים לא עובר — לא לבצע כתיבה.**

---

## 6. LIVE WRITE PLAN

**רק אחרי T3 approval מאייל:**

### פעולה:
```
API: PUT /admin/api/2024-01/products/{id}.json
שדה: tags
פעולה: MERGE (current_tags + new_tags) — לא replace
```

### כלל הכתיבה:
```python
final_tags = list(dict.fromkeys(current_tags + new_layer6_tags))
# current_tags ראשונים — לא נמחקים
```

### אסור בהחלט:
- לא למחוק תגיות קיימות
- לא לשנות `title`
- לא לשנות `body_html`
- לא לשנות `metafields`
- לא לשנות `collections`
- לא לשנות `variants`
- לא לגעת ב-theme
- לא לגעת ב-Mega Menu
- לכתוב מוצר אחד בכל פעם (לא batch PUT)
- לאמת תגובת API לפני המוצר הבא

### סדר כתיבה:
1. C3 (9688660312377) — score הגבוה ביותר
2. C2 (9874906349881)
3. C4 (9895864205625)

### עצירה אוטומטית:
אם מוצר אחד מחזיר שגיאה — לעצור, לא להמשיך.

---

## 7. VERIFY PLAN

**מיד אחרי כל כתיבה:**

לכל מוצר שנכתב:
```python
GET /admin/api/2024-01/products/{id}.json?fields=id,title,tags
```

**בדיקות verify:**

| בדיקה | תנאי הצלחה |
|-------|-----------|
| כל תגית Layer 6 קיימת | כל tag מרשימת new_layer6_tags נמצא ב-tags |
| תגיות קיימות לא נמחקו | "אוברול" עדיין קיים |
| אין age-* tags | אין שום tag שמתחיל ב-`age-` |
| אין תגים לא מאושרים | כל tag ב-ALLOWED_VALUES + legacy |
| title לא שונה | title זהה לפני הכתיבה |

**אם verify עובר:**
לשמור דוח:
```
output/tags/phase6-small-batch-live-verify.md
```

---

## 8. ROLLBACK PLAN

**אם verify נכשל:**

1. לקרוא מ-`output/tags/phase6-small-batch-tags-backup.json`
2. לכל מוצר שנכשל:
```python
PUT /admin/api/2024-01/products/{id}.json
{"product": {"id": id, "tags": backup["current_tags"]}}
```
3. לוודא שהחזרנו לתגיות המקוריות בלבד
4. לשמור דוח:
```
output/tags/phase6-small-batch-rollback-report.md
```

**מבנה דוח rollback:**

```json
{
  "rollback_timestamp": "YYYY-MM-DDTHH:MM:SS",
  "reason": "verify failed: [תיאור]",
  "products_rolled_back": [
    {
      "product_id": "...",
      "restored_tags": [...],
      "success": true
    }
  ]
}
```

---

## 9. T3 APPROVAL TEXT

הטקסט הבא לשלוח לאייל לפני Phase 6:

---

**אייל, נדרש אישורך לפני Phase 6.**

**מה מוכן:**
Phase 5 הסתיים. 5 מוצרים אושרו לכתיבה אוטומטית (SAFE_FOR_PHASE6).
כל 8 שערי אימות עוברים. אין age-* tags. אין taxonomy gaps.

**Batch ראשון — 3 מוצרים בלבד:**

| מוצר | product_id | תגיות שיתווספו |
|------|-----------|---------------|
| אוברול ג׳ינס דגם אתי | 9688660312377 | type-romper, size-3-6m/6-9m/9-12m/12-18m, season-spring-fall, fabric-denim, gender-girl |
| אוברול ג'ינס מתוק דגם זוהר | 9874906349881 | type-romper, size-3-6m/6-9m/9-12m, season-summer, fabric-denim, gender-neutral, style-casual |
| אוברול ג'ינס יוניסקס דגם שלו | 9895864205625 | type-romper, size-0-3m/3-6m/9-12m/12-18m, fabric-denim, gender-neutral, style-casual |

**מה לא ישתנה:**
תגיות קיימות, title, description, metafields, collections, theme, Mega Menu.

**גיבוי מלא יבוצע לפני הכתיבה.**

**לאישור, השב:**
`מאשר Phase 6 batch ראשון — C3, C2, C4`

---

## 10. FINAL VERDICT

**READY_FOR_T3_APPROVAL**

| בדיקה | סטטוס |
|-------|-------|
| Phase 5k COMPLETE | YES |
| SAFE_FOR_PHASE6 >= 5 | YES (5/9) |
| 3 מוצרים נבחרו לbatch | YES (C3, C2, C4) |
| כל proposed tags מתועדים | YES |
| backup plan מוגדר | YES |
| dry run plan מוגדר | YES |
| live write plan מוגדר | YES |
| verify plan מוגדר | YES |
| rollback plan מוגדר | YES |
| T3 approval text מוכן | YES |
| Phase 6 פתוח | **NO** |
| Shopify live | **NO** |
| כתיבה בוצעה | **NO** |

**הצעד הבא:** שלח T3 approval text לאייל ← חכה לאישורו ← רק אחרי "מאשר Phase 6 batch ראשון" — בצע Live Write Plan.

---

*מסמך זה הוא תכנון בלבד. אין שינויים ב-Shopify. Phase 6 NOT OPEN.*
