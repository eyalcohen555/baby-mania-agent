# Layer 7 — Phase 7B — Candidate Expansion Plan
**תאריך:** 2026-05-04
**Phase:** 7B — Planning Only — אין live
**מטרה:** להגיע מ-19 ל-50+ מוצרים מתויגים לפני Phase 8 (collections)

---

## 1. מצב מערכת

| פרמטר | ערך |
|-------|-----|
| Phase 6 batch 1+2 | COMPLETE + PASS |
| Phase 7A batch 1 | COMPLETE + PASS |
| Phase 7A batch 2 | COMPLETE + PASS |
| Shopify live tagged | **19 products** |
| target לPhase 8 | **50+ products + 4+ types** |
| collections | NO — חסום |
| Mega Menu | NO |
| live בשלב זה | NO — planning only |
| QA Contract | ACTIVE (layer7-live-tagging-qa-contract.md) |

---

## 2. למה collections עדיין חסום

| סיבה | ערך נוכחי | target |
|------|-----------|--------|
| מוצרים מתויגים | 19 | 50+ |
| סוגי מוצר live | 4 (romper, bodysuit, dress, set) | 4+ (מספיק אבל צריך נפח) |
| coverage מתוך inventory | ~4.8% (19/393) | לפחות 12.7% |
| UX: collection עם 19 מוצרים | דלה — לא ערך ללקוח | 50+ = ערך ממשי |

**כלל:** Phase 8 (collections + navigation) נפתח **רק** אחרי 50+ מוצרים מ-4+ סוגים שונים.

---

## 3. פער ויעד

| מדד | ערך |
|-----|-----|
| מוצרים מתויגים עכשיו | 19 |
| target מינימום | 50 |
| **חסרים** | **31 לפחות** |
| recommended expansion pool | **35–40 candidates** לdry-run |
| live batch הבא | עד 20 בכל פעם |
| batches נדרשים (20/batch) | 2 batches נוספים |

---

## 4. מוצרים שכבר חיים — לא לבחור שוב

| product_id | type | phase |
|-----------|------|-------|
| 9688660312377 | type-romper | Phase 6 |
| 9874906349881 | type-romper | Phase 6 |
| 9895864205625 | type-romper | Phase 6 |
| 9687579033913 | type-romper | Phase 6 |
| 9688932909369 | type-romper | Phase 6 |
| 9731768746297 | type-dress | Phase 7A B1 |
| 9179166671161 | type-bodysuit | Phase 7A B1 |
| 9874906382649 | type-bodysuit | Phase 7A B1 |
| 9874906546489 | type-set | Phase 7A B1 |
| 9688660377913 | type-set | Phase 7A B1 |
| 9688976326969 | type-set | Phase 7A B1 |
| 9688964989241 | type-set | Phase 7A B1 |
| 9688674566457 | type-set | Phase 7A B1 |
| 9688976294201 | type-set | Phase 7A B1 |
| 10190523302201 | type-set | Phase 7A B1 |
| 9606694437177 | type-set | Phase 7A B2 |
| 9688885985593 | type-romper | Phase 7A B2 |
| 9688934973753 | type-romper | Phase 7A B2 |
| 10190523138361 | type-set | Phase 7A B2 |

---

## 5. עדיפות סוגי מוצר לExpansion

| type | עדיפות | הערות |
|------|--------|-------|
| type-bodysuit | גבוהה מאוד | רק 2 עכשיו, פוטנציאל גבוה ב-inventory |
| type-dress | גבוהה | רק 1 עכשיו |
| type-set | גבוהה | 10 עכשיו, עדיין צריך עוד |
| type-romper | בינונית | 7 עכשיו, מספיק לCollection |
| type-top | בינונית | אם יש מקורות ברורים |
| type-pants | בינונית | אם יש מקורות ברורים |
| type-hat | בינונית | רק עם YAML או title מפורש |
| type-swimwear | בינונית | רק בקיץ, season-summer ברור |
| type-shoes | **חסום** | EU sizes בלי mapping — אסור |
| type-sandals | **חסום** | EU sizes בלי mapping — אסור |
| type-sneakers | **חסום** | EU sizes בלי mapping — אסור |
| type-coat | נמוכה | בדוק inventory |
| type-accessory | נמוכה | רק עם source trace ברור |
| type-reborn-doll | נמוכה | קטגוריה נפרדת — not yet |

---

## 6. כללי פסילה — אין לבחור candidates עם:

| כלל | הסבר |
|-----|-------|
| verdict = REVIEW_ONLY | לא עברו screening — דורשים בדיקה ידנית |
| size_status = RANGE_TOO_BROAD | טווח גדול מדי (0-3Y) — אין מידה ספציפית |
| EU shoe size ללא mapping | נעל עם מידות 19/20/21 — אין normalization |
| source trace חלש (conf < 0.85 לtype) | type לא מוכח — REVIEW_ONLY automatically |
| gender inferred from color | ורוד = בנות, כחול = בנים — forbidden inference |
| tag concatenation (3-6M6-9M) | malformed source — אינו source תקין |
| YAML_GAP + אין title source ל-fabric | ללא YAML, fabric אסור אלא אם בכותרת |
| score < 85 | ממוצע confidence נמוך מדי |
| title_not_in_Hebrew + no_YAML | מוצרים אנגלית בלי YAML — בדוק source trace בזהירות |

---

## 7. תהליך expansion מומלץ

### שלב 1 — Fetch Pool (לא live)
- משוך מ-Shopify 100-150 מוצרים שאין להם type-* tag
- סנן: status=active בלבד
- הוצא: כל 19 המוצרים שכבר חיים

### שלב 2 — Dry Run על 40 candidates
- הרץ scoring לכל מוצר
- וודא SAFE_FOR_PHASE7B (score ≥ 85, source trace ברור)
- צור source trace לכל תגית
- שמור ב: `output/tags/phase7b-candidates-dryrun.md`

### שלב 3 — Live Batch (לאחר T3 approval)
- עד 20 מוצרים בbatch
- מוצר אחד בכל פעם עם QA מלא
- QA Contract: layer7-live-tagging-qa-contract.md

### שלב 4 — Verify + Monitor
- אחרי batch: monitor דומה לphase7a-post-live-monitor
- אם 50+: פתיחת Phase 8 planning

---

## 8. פילוח inventory קיים (הערכה)

מתוך 393 active products, ה-untaged pool (374 לא מתויגים):

| type משוער | כמות (הערכה) | SAFE estimate |
|-----------|-------------|--------------|
| type-bodysuit | ~80-100 | ~50-60 SAFE |
| type-set | ~60-80 | ~40-50 SAFE |
| type-romper | ~40-50 | ~25-30 SAFE |
| type-dress | ~20-30 | ~15-20 SAFE |
| type-shoes/sandals | ~30-40 | 0 (EU size blocker) |
| type-top | ~15-25 | ~10-15 SAFE |
| type-hat | ~10-15 | ~5-8 SAFE |
| type-coat | ~5-10 | ~3-5 SAFE |
| type-swimwear | ~5-10 | ~3-5 SAFE |
| other/accessories | ~30-50 | ~10-15 SAFE |

**הערכה:** pool של ~160-200 SAFE candidates לbatches עתידיים.
מגיעים ל-50 בpatch 1 ו-2 בלבד.

---

## 9. Blocker פתוח: EU Shoe Sizes

| blocker | תיאור |
|---------|-------|
| בעיה | נעלי תינוק עם מידות אירופאיות (19, 20, 21, 22, 23) |
| חסר | mapping: EU size → size-* tag (size-newborn? size-0-3m?) |
| השפעה | ~30-40 מוצרי נעלי תינוק חסומים |
| פתרון | צריך בכל פעם קצת טבלת מיפוי לפני Phase 7C/7D |
| action item | אייל לאשר: 19 EU = newborn, 20-21 = 0-3m, 22-23 = 3-6m, 24+ = 6-9m |

---

## 10. Verdict

**READY_FOR_PHASE7B_DRYRUN**

| בדיקה | תוצאה |
|-------|-------|
| Phase 7A COMPLETE | YES |
| QA Contract הוגדר | YES |
| collections חסום | YES — 19 < 50 |
| pool קיים לdry-run | YES — ~160+ candidates משוערים |
| dry-run עוד לא בוצע | PENDING |
| live בשלב זה | NO |
| T3 approval לPhase 7B dryrun | PENDING |
| EU shoes blocker | OPEN — needs mapping |
| **VERDICT** | **READY_FOR_PHASE7B_DRYRUN** |

---

## 11. הצעדים הבאים

1. **Fetch** — משוך 100-150 מוצרים untapped מ-Shopify (read-only)
2. **Score** — הרץ dry-run classifier על כולם
3. **Select** — בחר 35-40 SAFE candidates
4. **Document** — שמור ב-`output/tags/phase7b-candidates-dryrun.md`
5. **T3 approval** — קבל אישור מאייל לbatch
6. **Live** — עד 20 מוצרים עם QA Contract מלא

---

*Phase 7B — Planning only. אין כתיבה ל-Shopify. 2026-05-04.*
