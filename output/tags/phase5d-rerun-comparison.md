# Layer 6 — Phase 5d Rerun Comparison Report
**תאריך:** 2026-05-03  
**Phase 4 baseline:** 2026-05-03  
**DRY RUN ONLY — אין כתיבה ל-Shopify**

---

## A. השוואת Phase 4 מול Phase 5d

| מדד | Phase 4 | Phase 5d | שינוי |
|---|---|---|---|
| Products tested | 59 | 59 | +0 |
| PASS | 30 (50.8%) | 30 (50.8%) | +0 |
| NEEDS_REVIEW | 29 | 29 | +0 |
| BLOCKED | 0 | 0 | +0 |
| avg quality score | 77.7 | 82.3 | +4.6 |
| NO_AGE_FOUND (total) | 31 | 32 | +1 |
| NO_AGE_FOUND (clothing/shoes only) | ~18 (est.) | ~18 (est.) | 0 |
| RANGE_TOO_BROAD | 4 | 4 | +0 |
| DOLL_NO_AGE | 9 | 8 | -1 |
| Phase5b exempt (new) | 0 | 0 | +0 |
| type-sleep-soother (new) | 0 | 1 | +1 |
| Taxonomy gaps | 0 | 0 | +0 |
| CATEGORY_COVERAGE fails | 26 | 26 | +0 |
| QUALITY_SCORE fails | 17 | 17 | +0 |

---

## B. בדיקת מוצרים קריטיים

| מוצר | כותרת (קצר) | סטטוס | age_status | score | tags (ראשונות) |
|---|---|---|---|---|---|
| P2 | — | — | not matched | — | — |
| P3 | — | — | not matched | — | — |
| P4 | נעל קז'ואל במיוחד לתינוקות | PASS | OK | 94.5 | type-shoes, age-2-3y, season-unknown, occ-gift, oc |
| P6 | — | — | not matched | — | — |
| P7 | — | — | not matched | — | — |
| P10 | — | — | not matched | — | — |
| P13 | בובה נושמת פיל ועוד חיות מחמד | PASS | NO_AGE_FOUND | 95.1 | type-sleep-soother, season-winter, fabric-fleece,  |
| P14 | אוברול בייבי מניה דגם חן | PASS | RANGE_TOO_BROAD | 96.5 | type-romper, season-winter, fabric-cotton, occ-eve |
| P15 | — | — | not matched | — | — |

### פירוט מוצרים קריטיים שזוהו

**אוברול בייבי מניה דגם חן** (ID: 10005779808569)
- status: PASS | score: 96.5 | age: RANGE_TOO_BROAD
- exempt: RANGE_TOO_BROAD
- tags: `type-romper`, `season-winter`, `fabric-cotton`, `occ-everyday`, `gender-girl`, `style-modern`
- notes: RANGE_TOO_BROAD:0-24m

**נעל קז'ואל במיוחד לתינוקות** (ID: 9606764462393)
- status: PASS | score: 94.5 | age: OK
- exempt: 
- tags: `type-shoes`, `age-2-3y`, `season-unknown`, `occ-gift`, `occ-everyday`, `gender-neutral`, `style-casual`
- notes: —

**בובה נושמת פיל ועוד חיות מחמד** (ID: 9587715244345)
- status: PASS | score: 95.1 | age: NO_AGE_FOUND
- exempt: YAML_GAP
- tags: `type-sleep-soother`, `season-winter`, `fabric-fleece`, `occ-sleep`, `occ-calming`, `occ-gift`, `gender-unknown`
- notes: Phase5c: type-sleep-soother, is_reborn overridden to False; NO_AGE_FOUND

---

## C. Navigation / Hebrew Labels Check

| Internal Tag | תווית לקוח | סטטוס |
|---|---|---|
| `type-sleep-soother` | מוצרי שינה והרגעה | ✅ נמצא |
| `collection-special-picks` | המיוחדים שלנו | ℹ️ שכבת merchandising — לא מופק ע"י tagger |
| `collection-new-arrivals` | חדשים | ℹ️ שכבת merchandising — לא מופק ע"י tagger |
| type-reborn-doll על breathing elephant | FORBIDDEN | ✅ תוקן |

**כלל:** מוצרים שאינם clothing/shoes לא מקבלים age filter בניווט הלקוח.
מוצרים שקיבלו Phase5b exempt: 0 — אלה לא יכללו ב-age filters.

---

## D. Phase 6 Candidates (Small Live Batch)

**מספר candidates שעמדו בכל הקריטריונים:** 9

| # | product_id | title | type | age | score | group | source trace |
|---|---|---|---|---|---|---|---|
| 1 | 9688932909369 | אוברול אריה חמוד דגם שמר | `type-romper` | `age-2-3y` | 86.4 | clothing_yaml | existing_tag, title, handle |
| 2 | 9874906349881 | אוברול ג'ינס מתוק מבית בייבי מ | `type-romper` | `age-newborn` | 96.6 | clothing_yaml | existing_tag, title, handle |
| 3 | 9688660312377 | אוברול ג׳ינס דגם אתי | `type-romper` | `age-2-3y` | 96.2 | clothing_yaml | existing_tag, body, title |
| 4 | 9895864205625 | אוברול ג’ינס יוניסקס לתינוקות  | `type-romper` | `age-2-3y` | 93.8 | clothing_yaml | existing_tag, title, handle |
| 5 | 9687579033913 | אוברול לבבות דגם הילה | `type-romper` | `age-2-3y` | 89.7 | clothing_yaml | existing_tag, title, handle |
| 6 | 9615375565113 | נעל אלגנטית צעד ראשון לבנות | `type-shoes` | `age-6-12m` | 95.4 | shoes_yaml | existing_tag, title, handle |
| 7 | 9606764462393 | נעל קז'ואל במיוחד לתינוקות | `type-shoes` | `age-2-3y` | 94.5 | shoes_yaml | existing_tag, title, handle |
| 8 | 9606764298553 | נעלי אופנה קז'ואל מונעות החלקה | `type-shoes` | `age-2-3y` | 94.5 | shoes_yaml | existing_tag, title, handle |
| 9 | 9838580662585 | מצוף שחייה לתינוקות עם גגון וח | `type-swimming-ring` | `DOLL_NO_AGE_APP` | 80.2 | reborn_toys | title, type_default |

### Why safe — per candidate

**1. אוברול אריה חמוד דגם שמר**
- type: clothing/shoes=True | age tag: age-2-3y | score: 86.4
- source trace: existing_tag, category_default, title, handle
- remaining risk: none visible

**2. אוברול ג'ינס מתוק מבית בייבי מניה דגם זוהר**
- type: clothing/shoes=True | age tag: age-newborn | score: 96.6
- source trace: existing_tag, category_default, title, handle
- remaining risk: none visible

**3. אוברול ג׳ינס דגם אתי**
- type: clothing/shoes=True | age tag: age-2-3y | score: 96.2
- source trace: category_default, handle, title, existing_tag
- remaining risk: none visible

**4. אוברול ג’ינס יוניסקס לתינוקות דגם שלו**
- type: clothing/shoes=True | age tag: age-2-3y | score: 93.8
- source trace: existing_tag, category_default, title, handle
- remaining risk: none visible

**5. אוברול לבבות דגם הילה**
- type: clothing/shoes=True | age tag: age-2-3y | score: 89.7
- source trace: existing_tag, category_default, title, handle
- remaining risk: none visible

**6. נעל אלגנטית צעד ראשון לבנות**
- type: clothing/shoes=True | age tag: age-6-12m | score: 95.4
- source trace: existing_tag, category_default, title, handle
- remaining risk: none visible

**7. נעל קז'ואל במיוחד לתינוקות**
- type: clothing/shoes=True | age tag: age-2-3y | score: 94.5
- source trace: existing_tag, category_default, title, handle
- remaining risk: none visible

**8. נעלי אופנה קז'ואל מונעות החלקה לתינוקות**
- type: clothing/shoes=True | age tag: age-2-3y | score: 94.5
- source trace: existing_tag, category_default, title, handle
- remaining risk: none visible

**9. מצוף שחייה לתינוקות עם גגון וחגורות ורצועה – **
- type: clothing/shoes=False | age tag: exempt | score: 80.2
- source trace: title, type_default, category_default
- remaining risk: medium confidence — review before live

**Rejected candidates** (PASS אך score < 80 או בעיה אחרת):

- אוברול אריה מתוק דגם שמר — score=79.6
- אוברול בייבי מניה דגם חן — other
- אוברול דוב מתוק דגם אייל — score=79.2
- אוברול דובי דגם דניאל — other
- אוברול חורפי לתינוקות דגם אנגל — other

---

## E. Final Recommendation

| תנאי | Phase 5d |
|---|---|
| avg quality >= 75 | ✅ (82.3) |
| BLOCKED = 0% | ✅ (0.0%) |
| >= 70% PASS+NR | ✅ (100.0%) |
| No taxonomy gaps | ✅ |
| No Shopify live | ✅ |
| Phase6 candidates >= 5 | ✅ (9) |

**Phase 6 אפשרי:** YES — רק אחרי אישור אייל T3

**הבהרה:** Phase 6 NOT OPEN. Shopify live NO.
אפשרות Phase 6 = טכנית מוכן. אישור אייל T3 נדרש לפני כל live batch.

---

*Phase 5d — DRY RUN ONLY. אין שינויים ב-Shopify.*