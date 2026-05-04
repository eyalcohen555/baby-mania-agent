# Layer 6 — Phase 5d Rerun Comparison Report
**תאריך:** 2026-05-04  
**Phase 4 baseline:** 2026-05-03  
**DRY RUN ONLY — אין כתיבה ל-Shopify**

---

## A. השוואת Phase 4 מול Phase 5d

| מדד | Phase 4 | Phase 5d | שינוי |
|---|---|---|---|
| Products tested | 59 | 58 | -1 |
| PASS | 30 (50.8%) | 23 (39.7%) | -7 |
| NEEDS_REVIEW | 29 | 35 | +6 |
| BLOCKED | 0 | 0 | +0 |
| avg quality score | 77.7 | 80.6 | +2.9 |
| NO_AGE_FOUND (total) | 31 | 41 | +10 |
| NO_AGE_FOUND (clothing/shoes only) | ~18 (est.) | ~18 (est.) | 0 |
| RANGE_TOO_BROAD | 4 | 5 | +1 |
| DOLL_NO_AGE | 9 | 6 | -3 |
| Phase5b exempt (new) | 0 | 1 | +1 |
| type-sleep-soother (new) | 0 | 1 | +1 |
| Taxonomy gaps | 0 | 0 | +0 |
| CATEGORY_COVERAGE fails | 26 | 33 | +7 |
| QUALITY_SCORE fails | 17 | 18 | +1 |

---

## B. בדיקת מוצרים קריטיים

| מוצר | כותרת (קצר) | סטטוס | age_status | score | tags (ראשונות) |
|---|---|---|---|---|---|
| P2 | — | — | not matched | — | — |
| P3 | — | — | not matched | — | — |
| P4 | נעל קז'ואל במיוחד לתינוקות | PASS | RANGE_TOO_BROAD | 94.4 | type-shoes, season-unknown, occ-gift, occ-everyday |
| P6 | — | — | not matched | — | — |
| P7 | — | — | not matched | — | — |
| P10 | — | — | not matched | — | — |
| P13 | בובה נושמת פיל ועוד חיות מחמד | PASS | NO_AGE_FOUND | 95.1 | type-sleep-soother, season-winter, fabric-fleece,  |
| P14 | אוברול בייבי מניה דגם חן | PASS | RANGE_TOO_BROAD | 96.4 | type-romper, season-winter, fabric-cotton, occ-eve |
| P15 | — | — | not matched | — | — |

### פירוט מוצרים קריטיים שזוהו

**אוברול בייבי מניה דגם חן** (ID: 10005779808569)
- status: PASS | score: 96.4 | age: RANGE_TOO_BROAD
- exempt: RANGE_TOO_BROAD
- tags: `type-romper`, `season-winter`, `fabric-cotton`, `occ-everyday`, `gender-neutral`, `style-modern`
- notes: RANGE_TOO_BROAD:0-24m

**נעל קז'ואל במיוחד לתינוקות** (ID: 9606764462393)
- status: PASS | score: 94.4 | age: RANGE_TOO_BROAD
- exempt: RANGE_TOO_BROAD
- tags: `type-shoes`, `season-unknown`, `occ-gift`, `occ-everyday`, `gender-neutral`, `style-casual`
- notes: RANGE_TOO_BROAD:0-to-Xy

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
מוצרים שקיבלו Phase5b exempt: 1 — אלה לא יכללו ב-age filters.

---

## D. Phase 6 Candidates (Small Live Batch)

**מספר candidates שעמדו בכל הקריטריונים:** 1

| # | product_id | title | type | age | score | group | source trace |
|---|---|---|---|---|---|---|---|
| 1 | 9874906349881 | אוברול ג'ינס מתוק מבית בייבי מ | `type-romper` | `age-newborn` | 96.5 | clothing_yaml | existing_tag, title, handle |

### Why safe — per candidate

**1. אוברול ג'ינס מתוק מבית בייבי מניה דגם זוהר**
- type: clothing/shoes=True | age tag: age-newborn | score: 96.5
- source trace: existing_tag, category_default, title, handle
- remaining risk: none visible

**Rejected candidates** (PASS אך score < 80 או בעיה אחרת):

- אוברול אריה מתוק דגם שמר — score=79.6
- אוברול בייבי מניה דגם חן — other
- אוברול דובי דגם דניאל — other
- אוברול חורפי לתינוקות דגם אנגל — other
- אוברול לתינוקות דגם סטייסי — other

---

## E. Final Recommendation

| תנאי | Phase 5d |
|---|---|
| avg quality >= 75 | ✅ (80.6) |
| BLOCKED = 0% | ✅ (0.0%) |
| >= 70% PASS+NR | ✅ (100.0%) |
| No taxonomy gaps | ✅ |
| No Shopify live | ✅ |
| Phase6 candidates >= 5 | ❌ (1) |

**Phase 6 אפשרי:** NO — עדיין ממתין

**הבהרה:** Phase 6 NOT OPEN. Shopify live NO.
אפשרות Phase 6 = טכנית מוכן. אישור אייל T3 נדרש לפני כל live batch.

---

*Phase 5d — DRY RUN ONLY. אין שינויים ב-Shopify.*