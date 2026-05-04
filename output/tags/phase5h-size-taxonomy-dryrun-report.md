# Layer 6 — Phase 5h Size Taxonomy Dry Run Report
**תאריך:** 2026-05-04
**Phase:** 5h — CAT-B Pivot: Age → Size + Dry Run Revalidation
**DRY RUN ONLY — אין כתיבה ל-Shopify**

---

## 1. SYSTEM STATE

| פרמטר | ערך |
|-------|-----|
| Phase | 5h |
| תאריך | 2026-05-04 |
| Shopify live | **NO** |
| Phase 6 | **NOT OPEN** |
| T3 approval (אייל) | PENDING |
| CAT-B pivot | age-* → size-* |
| Source pivot | handle/heuristics → variants/tags/title מפורשים |
| Git HEAD | 16c280c — "docs+logic(layer6): pivot CAT-B from age to size" |

---

## 2. החלטה עסקית: גיל הוחלף במידה

BabyMania אינה דורשת תגיות גיל על מוצרים.
ביגוד ונעליים ישתמשו בתגיות **מידה** (size-*) בלבד.
שאר המוצרים (צעצועים, ריבורן, אביזרים) פטורים ממידה חובה.

**לפני (Phase 5f):** `CAT-B = age-*` — מקורות: handle keywords, heuristics
**אחרי (Phase 5h):** `CAT-B = size-*` — מקורות: variants, tags, title מפורשים בלבד

| לפני (Phase 5f) | אחרי (Phase 5h) |
|---|---|
| `age-0-3m` | `size-0-3m` |
| `age-3-6m` | `size-3-6m` |
| `age-6-12m` | הוסר — מוחלף ב-`size-6-9m` + `size-9-12m` |
| `age-12-18m` | `size-12-18m` |
| `age-18-24m` | `size-18-24m` |
| `age-2-3y` | `size-2y` |
| `age-3-5y` | הוסר — מוחלף ב-`size-3y` + `size-4y` |
| `age-0-6m` | הוסר — לא מידה variant תקינה |
| `age-newborn` | `size-newborn` |
| `age-unknown` | `size-unknown` |

---

## 3. קבצים ששונו

| קובץ | שינוי |
|------|-------|
| `docs/organic/layer6-taxonomy-spec-v1.md` | Section 4: CAT-B Age → Size; ALLOWED VALUES; YAML_GAP row |
| `docs/organic/layer6-full-tag-system-navigation-planning-spec-v1.md` | CAT-B row → "Size"; labels updated |
| `scripts/tags/layer6_validate_tags.py` | `ALLOWED_VALUES["CAT-B"]` = size-*; `PREFIX_TO_CAT["size"]="CAT-B"`; `NON_SIZE_TYPES` |
| `scripts/tags/run_layer6_phase5d_rerun.py` | `CUSTOMER_LABELS` age-* → size-*; `extract_cat_b()` rewritten; stats renamed |
| `scripts/tags/run_layer6_phase5h_dryrun.py` | new wrapper with phase5h output paths |
| `output/tags/phase5g-age-to-size-taxonomy-pivot.md` | business decision document |
| `output/tags/phase5h-size-taxonomy-dryrun-report.md` | this report |
| `output/tags/phase5h-size-taxonomy-dryrun-report.json` | dry-run stats JSON |
| `output/tags/phase5h-size-taxonomy-sample-58.json` | 58-product sample results |

**לא שונו (DO NOT TOUCH):**
- `docs/product/reborn/*`
- `teams/organic/agents/04-organic-blog-writer.md`
- `output/tags/phase5g-age-source-human-review-pack.md` (לא נכנס לגיט)

---

## 4. תוצאות לפני / אחרי

| מדד | Phase 5f | Phase 5h | שינוי |
|---|---|---|---|
| Products tested | 58 | 58 | 0 |
| PASS | 23 (39.7%) | 23 (39.7%) | 0 |
| NEEDS_REVIEW | 35 | 35 | 0 |
| BLOCKED | 0 | 0 | 0 |
| avg quality score | 80.6 | 80.7 | +0.1 |
| total_proposed_tags | 323 | 320 | -3 |
| RANGE_TOO_BROAD | 5 | 5 | 0 |
| NO_SIZE_FOUND (prev NO_AGE_FOUND) | 41 | 44 | +3 |
| DOLL_NO_AGE_APPLICABLE | 6 | 6 | 0 |
| Phase5b exempt (swim-ring) | 1 | 1 | 0 |
| type-sleep-soother | 1 | 1 | 0 |
| taxonomy_gaps | 0 | 0 | 0 |
| CATEGORY_COVERAGE fails | 33 | 33 | 0 |
| QUALITY_SCORE fails | 18 | 18 | 0 |
| age-* tags generated | 41 | **0** | -41 ✅ |
| size-* tags generated | 0 | **3** | +3 ✅ |

---

## 5. בדיקת 9 מועמדי Phase 6 המקוריים

מועמדים מ-Phase 5f בודקים שוב תחת size taxonomy.

| # | product_id | Phase 5f status | Phase 5h status | size tag | score | Phase 5h verdict |
|---|---|---|---|---|---|---|
| C1 | 9688932909369 | NEEDS_REVIEW NO_AGE_FOUND | NEEDS_REVIEW NO_SIZE_FOUND | — | 71.1 | REVIEW_ONLY |
| C2 | 9874906349881 | PASS age-newborn | PASS size-newborn | size-newborn | 96.5 | **SAFE_FOR_PHASE6** |
| C3 | 9688660312377 | NEEDS_REVIEW NO_AGE_FOUND | NEEDS_REVIEW NO_SIZE_FOUND | — | 81.4 | REVIEW_ONLY |
| C4 | 9895864205625 | NEEDS_REVIEW NO_AGE_FOUND | NEEDS_REVIEW NO_SIZE_FOUND | — | 78.4 | REVIEW_ONLY |
| C5 | 9687579033913 | NEEDS_REVIEW NO_AGE_FOUND | NEEDS_REVIEW NO_SIZE_FOUND | — | 75.0 | REVIEW_ONLY |
| C6 | 9615375565113 | NEEDS_REVIEW NO_AGE_FOUND | NEEDS_REVIEW NO_SIZE_FOUND | — | 80.4 | REVIEW_ONLY |
| C7 | 9606764462393 | PASS RANGE_TOO_BROAD | PASS RANGE_TOO_BROAD | — | 94.4 | KEEP_BLOCKED |
| C8 | 9606764298553 | NEEDS_REVIEW NO_AGE_FOUND | NEEDS_REVIEW NO_SIZE_FOUND | — | 79.5 | REVIEW_ONLY |
| C9 | 9838580662585 | PASS Phase5b:type-swimming-ring | PASS Phase5b:type-swimming-ring | — | 80.2 | EXEMPT_NON_SIZE |

**הערות:**
- C2: size-newborn מ-YAML/title — מקור מהימן. SAFE_FOR_PHASE6.
- C1,C3-C6,C8: type clothing/shoes + NO_SIZE_FOUND — ממתינים ל-variant data.
- C7: handle מכיל "0-to-3-years-old" — RANGE_TOO_BROAD נשאר חסום.
- C9: type-swimming-ring — Phase5b exempt, לא דורש מידה.

---

## 6. ספירה

| קטגוריה | כמות | מועמדים |
|---------|------|---------|
| **SAFE_FOR_PHASE6** | **1** | C2 |
| **REVIEW_ONLY** | **6** | C1, C3, C4, C5, C6, C8 |
| **KEEP_BLOCKED** | **1** | C7 (RANGE_TOO_BROAD) |
| **EXEMPT_NON_SIZE** | **1** | C9 (type-swimming-ring) |

**סה"כ מועמדים:** 9 | **SAFE ≥ 5 נדרשים ל-Phase 6:** ❌ (רק 1 SAFE)

---

## 7. Source Hierarchy — CAT-B (size)

| עדיפות | source | דוגמה | confidence |
|--------|--------|-------|-----------|
| 1 | Shopify variant option | "0-3M", "3-6M", "NB", "2Y" | 0.95 |
| 2 | existing Hebrew/clean tag | "0-3 חודש", "newborn" | 0.90 |
| 3 | title/handle מפורש | "size 3-6m", "newborn" בכותרת | 0.88 |
| ❌ | toddler/infant/first-walker | אסור | — |
| ❌ | desc/body בלבד | לא מספיק | — |
| ❌ | טווח רחב (0-3Y) | RANGE_TOO_BROAD | — |

---

## 8. Gate Results

| Gate | כשלונות | פירוש |
|---|---|---|
| SOURCE_EXISTS | 0/58 | ✅ |
| FORMAT_VALID | 0/58 | ✅ |
| ALLOWED_VALUE | 0/58 | ✅ — כל size-* tags בטקסונומיה |
| SOURCE_TRACEABLE | 0/58 | ✅ |
| NO_FORBIDDEN_INFERENCE | 0/58 | ✅ |
| CATEGORY_COVERAGE | 33/58 | ⚠️ NO_SIZE_FOUND על clothing/shoes |
| DUPLICATE_CONFLICT | 0/58 | ✅ |
| QUALITY_SCORE | 18/58 | ⚠️ קשור ל-CATEGORY_COVERAGE |

---

## 9. NO_SIZE_FOUND Breakdown (44 products)

**שורש הבעיה:** ה-fetch הנוכחי אינו כולל `variants` ב-fields:
```python
# נדרש ל-Phase 5i:
fields=id,title,handle,tags,body_html,product_type,variants
```

| סיבה | כמות (אומדן) |
|------|------------|
| אין variants עם size option בנתוני ה-fetch | ~20 |
| Hebrew tags מייצגים גיל ולא מידה variant | ~8 |
| handle/title לא כולל size מפורש | ~12 |
| YAML_GAP + אין title size | ~4 |

לאחר הוספת `variants` — מצופה ש-6 ה-REVIEW_ONLY candidates יקבלו size-* מ-variant options.

---

## 10. אישורים

| בדיקה | תוצאה |
|-------|-------|
| age-* tags שיצאו בדוח | **0** ✅ |
| size-* tags שיצאו בדוח | **3** ✅ |
| Phase 6 פתוח | **NO** ✅ |
| Shopify live | **NO** ✅ |
| כתיבה ל-Shopify | **NO** ✅ |
| taxonomy_gaps | **0** ✅ |
| blocked_pct | **0.0%** ✅ |
| avg_score ≥ 75 | **80.7** ✅ |

---

## 11. Verdict סופי

**PHASE6_STILL_BLOCKED**

סיבות:
1. SAFE_FOR_PHASE6 = 1/9 (נדרש ≥ 5)
2. 6 candidates ממתינים ל-variant size data
3. T3 approval (אייל) טרם התקבל

**הצעד הבא — Phase 5i:**
- הוסף `variants` ל-`fetch_shopify_products()` fields
- הרץ dry-run מחדש
- צפוי: 6 REVIEW_ONLY → SAFE לאחר variant fetch

**Phase 6 NOT OPEN** — Shopify live: NO.

---

*Phase 5h — DRY RUN ONLY. אין שינויים ב-Shopify.*
