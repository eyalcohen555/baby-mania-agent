# Layer 6 — Phase 5d Rerun Comparison Report
**תאריך:** 2026-05-04  
**Phase 4 baseline:** 2026-05-03  
**DRY RUN ONLY — אין כתיבה ל-Shopify**

---

## A. השוואת Phase 4 מול Phase 5d

| מדד | Phase 4 | Phase 5d | שינוי |
|---|---|---|---|
| Products tested | 59 | 58 | -1 |
| PASS | 30 (50.8%) | 32 (55.2%) | +2 |
| NEEDS_REVIEW | 29 | 26 | -3 |
| BLOCKED | 0 | 0 | +0 |
| avg quality score | 77.7 | 83.5 | +5.8 |
| NO_AGE_FOUND (total) | 31 | 0 | -31 |
| NO_AGE_FOUND (clothing/shoes only) | ~18 (est.) | ~18 (est.) | 0 |
| RANGE_TOO_BROAD | 4 | 5 | +1 |
| DOLL_NO_AGE | 9 | 0 | -9 |
| Phase5b exempt (new) | 0 | 1 | +1 |
| type-sleep-soother (new) | 0 | 1 | +1 |
| Taxonomy gaps | 0 | 0 | +0 |
| CATEGORY_COVERAGE fails | 26 | 24 | -2 |
| QUALITY_SCORE fails | 17 | 13 | -4 |

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
| P13 | בובה נושמת פיל ועוד חיות מחמד | PASS | NO_SIZE_FOUND | 95.1 | type-sleep-soother, season-winter, fabric-fleece,  |
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
- status: PASS | score: 95.1 | age: NO_SIZE_FOUND
- exempt: YAML_GAP
- tags: `type-sleep-soother`, `season-winter`, `fabric-fleece`, `occ-sleep`, `occ-calming`, `occ-gift`, `gender-unknown`
- notes: Phase5c: type-sleep-soother, is_reborn overridden to False; NO_SIZE_FOUND

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

**מספר candidates שעמדו בכל הקריטריונים:** 9

| # | product_id | title | type | age | score | group | source trace |
|---|---|---|---|---|---|---|---|
| 1 | 9688932909369 | אוברול אריה חמוד דגם שמר | `type-romper` | `` | 88.8 | clothing_yaml | title, existing_tag, handle |
| 2 | 9678573240633 | אוברול אריה מתוק דגם שמר | `type-romper` | `` | 81.6 | clothing_yaml | existing_tag, handle |
| 3 | 9874906349881 | אוברול ג'ינס מתוק מבית בייבי מ | `type-romper` | `` | 97.2 | clothing_yaml | title, existing_tag, handle |
| 4 | 9858268430649 | אוברול גינס מהמם דגם רוית | `type-romper` | `` | 91.1 | clothing_yaml | title, existing_tag, handle |
| 5 | 9688660312377 | אוברול ג׳ינס דגם אתי | `type-romper` | `` | 97.4 | clothing_yaml | existing_tag, body, handle |
| 6 | 9895864205625 | אוברול ג’ינס יוניסקס לתינוקות  | `type-romper` | `` | 95.7 | clothing_yaml | title, existing_tag, handle |
| 7 | 9688965087545 | אוברול דוב מתוק דגם אייל | `type-romper` | `` | 82.5 | clothing_yaml | existing_tag, handle |
| 8 | 9864947827001 | אוברול חגיגי דגם אנה | `type-romper` | `` | 90.9 | clothing_yaml | title, existing_tag, handle |
| 9 | 9687579033913 | אוברול לבבות דגם הילה | `type-romper` | `` | 91.2 | clothing_yaml | existing_tag, handle |

### Why safe — per candidate

**1. אוברול אריה חמוד דגם שמר**
- type: clothing/shoes=True | age tag: exempt | score: 88.8
- source trace: category_default, title, existing_tag, handle
- remaining risk: none visible

**2. אוברול אריה מתוק דגם שמר**
- type: clothing/shoes=True | age tag: exempt | score: 81.6
- source trace: category_default, existing_tag, handle
- remaining risk: medium confidence — review before live

**3. אוברול ג'ינס מתוק מבית בייבי מניה דגם זוהר**
- type: clothing/shoes=True | age tag: exempt | score: 97.2
- source trace: category_default, title, existing_tag, handle
- remaining risk: none visible

**4. אוברול גינס מהמם דגם רוית**
- type: clothing/shoes=True | age tag: exempt | score: 91.1
- source trace: category_default, title, existing_tag, handle
- remaining risk: none visible

**5. אוברול ג׳ינס דגם אתי**
- type: clothing/shoes=True | age tag: exempt | score: 97.4
- source trace: category_default, existing_tag, body, handle
- remaining risk: none visible

**6. אוברול ג’ינס יוניסקס לתינוקות דגם שלו**
- type: clothing/shoes=True | age tag: exempt | score: 95.7
- source trace: category_default, title, existing_tag, handle
- remaining risk: none visible

**7. אוברול דוב מתוק דגם אייל**
- type: clothing/shoes=True | age tag: exempt | score: 82.5
- source trace: category_default, existing_tag, handle
- remaining risk: medium confidence — review before live

**8. אוברול חגיגי דגם אנה**
- type: clothing/shoes=True | age tag: exempt | score: 90.9
- source trace: category_default, title, existing_tag, handle
- remaining risk: none visible

**9. אוברול לבבות דגם הילה**
- type: clothing/shoes=True | age tag: exempt | score: 91.2
- source trace: category_default, existing_tag, handle
- remaining risk: none visible

**Rejected candidates** (PASS אך score < 80 או בעיה אחרת):

- אוברול בייבי  לתינוק – Baby Bear Cozy Se — gender-unknown
- אוברול בייבי מניה דגם חן — other
- אוברול דובי דגם דניאל — other
- אוברול חורפי לתינוקות דגם אנגל — other
- אוברול לתינוקות דגם סטייסי — other

---

## E. Final Recommendation

| תנאי | Phase 5d |
|---|---|
| avg quality >= 75 | ✅ (83.5) |
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