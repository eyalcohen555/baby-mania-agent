# Layer 6 — Phase 5j Three-Candidate Size Review
**תאריך:** 2026-05-04
**Phase:** 5j — בדיקה נקודתית ל-C4/C6/C8
**DRY RUN — אין כתיבה ל-Shopify**

---

## 1. SYSTEM STATE

| פרמטר | ערך |
|-------|-----|
| Phase 5i | ✅ COMPLETE |
| Phase 5i SAFE_FOR_PHASE6 | 4 (C1, C2, C3, C5) |
| Phase 5i REVIEW_ONLY | C4, C6, C8 |
| Phase 6 | **NOT OPEN** |
| Shopify live | **NO** |
| T3 approval (אייל) | PENDING |

---

## 2. שלושת המוצרים שנבדקו

### C4 — product_id: 9895864205625

**כותרת:** אוברול ג'ינס יוניסקס לתינוקות דגם שלו
**handle:** `diimuu-baby-children-boys-clothes-rompers-toddler-kids-overalls-denim-pants-casual-jumpsuits-long-sleeve-fashion-trousers`

**נתוני Shopify (read-only fetch):**
- Options: `מידה` → values: `['0-3 M', '9-12 M', '3-6 M', '12-18 M']`
- Variants (4): `0-3 M`, `3-6 M`, `9-12 M`, `12-18 M`
- Tags: Hebrew tag (garbled in fetch — not a size tag)
- No size in handle or title

**ניתוח:**
המוצר מגיע בארבע מידות ב-Shopify: 0-3 M, 3-6 M, 9-12 M, 12-18 M.
שם האפשרות הוא "מידה" (מידה בעברית).
הערכים תואמים ישירות למיפוי המאושר.

**למה לא זוהה ב-Phase 5i:**
`VARIANT_SIZE_MAP` מכיל `"0-3m"` ו-`"0-3"` אך **לא** `"0-3 m"` (עם רווח לפני M).
הערך בפועל הוא `"0-3 M"` → לאחר `strip().lower()` → `"0-3 m"` — לא ב-map.

**תיקון נדרש (Phase 5k):** הוסף לNORMALIZATION:
```python
key = re.sub(r'\s+', '', opt.strip().lower())  # "0-3 m" → "0-3m"
```
או הוסף ל-`VARIANT_SIZE_MAP`:
```python
"0-3 m": "size-0-3m", "3-6 m": "size-3-6m",
"9-12 m": "size-9-12m", "12-18 m": "size-12-18m",
```

**מקור מידה:** Shopify variant option "מידה" — מקור ראשי מדרגה 1.
**סתירות:** אין — handle מכיל "toddler" (אסור כמקור) אך ה-variant source עצמאי ותקין.
**Proposed tags:** size-0-3m, size-3-6m, size-9-12m, size-12-18m

---

### C6 — product_id: 9615375565113

**כותרת:** נעל אלגנטית צעד ראשון לבנות
**handle:** `girls-mary-jane-shoes-children-solid-color-bow-round-toe-bow-2024-new-kids-fashion-soft-moccasin-shoes-baby-first-walker-shoes`

**נתוני Shopify (read-only fetch):**
- Options:
  - Option 1 (צבע): 2 ערכי צבע בעברית
  - Option 2 (מספר): `['21', '22', '23', '24', '25', '26', '27', '28', '29', '30']`
- Variants: 20 (צבע × מספר)
- Tags: `baby-gift, baby-shoes, elegant-baby, everyday-baby-wear, girls-clothing, newborn-clothing`

**ניתוח:**
Option 2 הוא מספרי נעל אירופאי EU (21–30).
מספרי EU אלו **אינם** מיפוי ישיר לתגיות `size-*` של BabyMania בלי טבלת המרה מאושרת.

| EU size | גיל משוער | מיפוי BabyMania size-* |
|---------|-----------|----------------------|
| 21 | ~12-15 חודשים | לא מוגדר |
| 22 | ~15-18 חודשים | לא מוגדר |
| 23-24 | ~18-24 חודשים | לא מוגדר |
| 25-26 | ~2-3 שנים | לא מוגדר |

**הערה:** handle מכיל "first-walker-shoes" — **אסור** כמקור מידה.
tag "newborn-clothing" — **לא מדויק** לנעל מספר 21+.

**מקור מידה תקין:** אין — EU sizes אינם ב-VARIANT_SIZE_MAP ואין טבלת המרה מאושרת.

---

### C8 — product_id: 9606764298553

**כותרת:** נעלי אופנה קז'ואל מונעות החלקה לתינוקות
**handle:** `childrens-sneakers-kids-fashion-design-white-non-slip-casual-shoes-for-boys-girls-hook-breathable-sneakers-toddler-outdoor-shoe`

**נתוני Shopify (read-only fetch):**
- Options:
  - Option 1 (צבע): 3 ערכי צבע בעברית
  - Option 2 (מספר): `['30', '21', '22', '23', '24', '25', '26', '27', '28', '29']`
- Variants: 30 (צבע × מספר)
- Tags: `baby-gift, baby-shoes, everyday-baby-wear, neutral-baby-outfit, newborn-clothing`

**ניתוח:**
זהה ל-C6 — מספרי נעל EU (21–30). אין מיפוי מאושר.
handle מכיל "toddler" — **אסור** כמקור.
tag "newborn-clothing" — **לא מדויק**.

**מקור מידה תקין:** אין — EU sizes אינם ב-VARIANT_SIZE_MAP ואין טבלת המרה מאושרת.

---

## 3. מקור מידה לכל מוצר

| מועמד | option name | ערכים | סוג | מיפוי ל-size-* | תקין? |
|-------|------------|-------|-----|--------------|-------|
| C4 | מידה | 0-3 M, 3-6 M, 9-12 M, 12-18 M | חודשי תינוק | ✅ ישיר | **כן** |
| C6 | מספר | 21, 22, 23, 24, 25, 26, 27, 28, 29, 30 | EU shoe size | ❌ אין מיפוי | לא |
| C8 | מספר | 21, 22, 23, 24, 25, 26, 27, 28, 29, 30 | EU shoe size | ❌ אין מיפוי | לא |

---

## 4. Verdict לכל מוצר

| מועמד | product_id | verdict | הסבר |
|-------|-----------|---------|------|
| **C4** | 9895864205625 | **SAFE_FOR_PHASE6** | variant sizes תקינות (0-3 M, 3-6 M, 9-12 M, 12-18 M) — source ראשי אמין. תיקון טכני מינורי ל-VARIANT_SIZE_MAP נדרש. |
| C6 | 9615375565113 | REVIEW_ONLY | EU shoe sizes (21–30) — אין מיפוי ל-size-* ללא טבלת המרה מאושרת. |
| C8 | 9606764298553 | REVIEW_ONLY | EU shoe sizes (21–30) — זהה ל-C6. |

---

## 5. האם הגענו ל-5 SAFE_FOR_PHASE6?

| מועמד | Phase 5i | Phase 5j | שינוי |
|-------|---------|---------|-------|
| C1 (9688932909369) | SAFE | SAFE | — |
| C2 (9874906349881) | SAFE | SAFE | — |
| C3 (9688660312377) | SAFE | SAFE | — |
| **C4 (9895864205625)** | REVIEW_ONLY | **SAFE** | **+1** |
| C5 (9687579033913) | SAFE | SAFE | — |
| C6 (9615375565113) | REVIEW_ONLY | REVIEW_ONLY | — |
| C7 (9606764462393) | KEEP_BLOCKED | KEEP_BLOCKED | — |
| C8 (9606764298553) | REVIEW_ONLY | REVIEW_ONLY | — |
| C9 (9838580662585) | EXEMPT | EXEMPT | — |

**SAFE_FOR_PHASE6: 5** ✅ (C1, C2, C3, C4, C5)

---

## 6. Verdict סופי

**READY_FOR_PHASE6_SMALL_BATCH_PLAN** ✅

הגענו ל-5 SAFE_FOR_PHASE6.

**המלצה לתוכנית Phase 6 Small Live Batch:**
- batch ראשון: 3-5 מוצרים בלבד
- קריטריונים: PASS + score ≥ 88 + size-* מ-variant source
- מועמדים מומלצים: C3 (97.4), C2 (97.2), C5 (91.2), C1 (88.8)
- C4 זקוק לתיקון `VARIANT_SIZE_MAP` לפני Phase 6 (הוספת "0-3 m" וכדומה)

**לא לפתוח Phase 6** — נדרש T3 approval (אייל) תחילה.
**לא לעשות live** — עד אישור T3.

---

## 7. אישורים

| בדיקה | תוצאה |
|-------|-------|
| age-* tags שיצאו | **0** ✅ |
| Phase 6 פתוח | **NO** ✅ |
| Shopify live | **NO** ✅ |
| כתיבה ל-Shopify | **NO** ✅ |
| תגיות נוספו למוצרים חיים | **NO** ✅ |

---

*Phase 5j — בדיקה ידנית בלבד. אין שינויים ב-Shopify.*
