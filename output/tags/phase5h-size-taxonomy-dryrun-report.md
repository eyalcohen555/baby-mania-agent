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

---

## 2. Phase 5h vs Phase 5f — השוואה

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

**הסבר +3 ב-NO_SIZE_FOUND:** שלושה מוצרים שנמצאו בעבר עם `age-*` ממיפוי Hebrew tags (למשל "6-12 חודש") — כעת לא ממופים למידה מכיוון שהם מייצגים טווחי גיל ולא מידות variant מפורשות. נדרש YAML/variant source.

---

## 3. Pivot: CAT-B age-* → size-*

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
| — | `size-6-9m` (חדש) |
| — | `size-9-12m` (חדש) |
| — | `size-3y` (חדש) |
| — | `size-4y` (חדש) |

**Prefix שינוי:** `age-` → `size-`

---

## 4. New ALLOWED_VALUES — CAT-B

```python
"CAT-B": {
    "size-newborn", "size-0-3m", "size-3-6m", "size-6-9m", "size-9-12m",
    "size-12-18m", "size-18-24m", "size-2y", "size-3y", "size-4y",
    "size-unknown",
}
```

`PREFIX_TO_CAT` עדכון: `"age" → "size"` — כל תגית `size-*` ממופה ל-`CAT-B`.

---

## 5. Source Hierarchy — CAT-B (size)

| עדיפות | source | דוגמה | confidence |
|--------|--------|-------|-----------|
| 1 | Shopify variant option | "0-3M", "3-6M", "NB", "2Y" | 0.95 |
| 2 | existing Hebrew/clean tag | "0-3 חודש", "newborn" | 0.90 |
| 3 | title/handle מפורש | "size 3-6m", "newborn" בכותרת | 0.88 |
| ❌ | toddler/infant/first-walker | אסור | — |
| ❌ | desc/body בלבד | לא מספיק | — |
| ❌ | טווח רחב (0-3Y) | RANGE_TOO_BROAD | — |

---

## 6. Gate Results

| Gate | כשלונות | פירוש |
|---|---|---|
| SOURCE_EXISTS | 0/58 | ✅ |
| FORMAT_VALID | 0/58 | ✅ |
| ALLOWED_VALUE | 0/58 | ✅ — כל size-* תגים בטקסונומיה |
| SOURCE_TRACEABLE | 0/58 | ✅ |
| NO_FORBIDDEN_INFERENCE | 0/58 | ✅ |
| CATEGORY_COVERAGE | 33/58 | ⚠️ NO_SIZE_FOUND על clothing/shoes |
| DUPLICATE_CONFLICT | 0/58 | ✅ |
| QUALITY_SCORE | 18/58 | ⚠️ קשור ל-CATEGORY_COVERAGE |

**taxonomy_gaps:** 0 — כל size-* tags חוקיים. ✅

---

## 7. PASS Products (23/58)

מוצרים שעברו PASS קיבלו size tag מאחד מ-3 sources מורשים (variant/tag/title).

| קטגוריה | PASS (אומדן) |
|---------|------------|
| clothing_yaml | ~11 |
| shoes_yaml | ~6 |
| reborn_toys | 6 (exempt Phase5b) |
| accessories | 1 (exempt Phase5b) |
| yaml_gap | ~1 |
| edge_cases | ~2 |

---

## 8. NEEDS_REVIEW Analysis (35/58)

| סיבה עיקרית | כמות (אומדן) |
|------------|------------|
| NO_SIZE_FOUND (clothing/shoes) | ~27 |
| RANGE_TOO_BROAD | 5 |
| YAML_GAP+NO_SIZE_FOUND (exempt) | ~17 |

**מסקנה:** רוב ה-NEEDS_REVIEW נובע מ-NO_SIZE_FOUND — מוצרי ביגוד/נעליים ללא variant option data.

---

## 9. NO_SIZE_FOUND Breakdown (44 products)

| סיבה | כמות (אומדן) |
|------|------------|
| אין variants עם size option בנתוני ה-fetch הנוכחי | ~20 |
| Hebrew tags מייצגים גיל ולא מידה variant | ~8 |
| handle/title לא כולל size מפורש | ~12 |
| YAML_GAP + אין title size | ~4 |

**שורש הבעיה:** ה-fetch הנוכחי לא מכלול `variants` ב-fields:
```python
# נדרש לעדכן:
fields=id,title,handle,tags,body_html,product_type,variants
```
לאחר הוספת variants — מצופה שרוב מוצרי clothing/shoes יקבלו size-* מ-variant options.

---

## 10. Phase 5h Pass Criteria

| תנאי | סטטוס |
|------|-------|
| no_shopify_live | ✅ |
| no_forbidden_tags | ✅ |
| no_type_reborn_on_sleep_soother | ✅ |
| no_wide_range_bypass | ✅ |
| all_size_tags_in_allowed_values | ✅ (0 taxonomy gaps) |
| prefix_to_cat_updated | ✅ ("size" → CAT-B) |
| no_age_prefix_in_proposed_tags | ✅ (0 age-* tags generated) |
| avg_score_gte_75 | ✅ (80.7) |
| blocked_pct_lt_20 | ✅ (0.0%) |
| validator_accepts_size_tags | ✅ |
| docs_updated_taxonomy_nav_spec | ✅ |

---

## 11. Phase 6 Verdict + הצעד הבא

**PHASE6_STILL_BLOCKED** — נדרשים:

1. **Phase 5i — Variant data fetch** — הוספת `variants` ל-`fields` ב-`fetch_shopify_products()`.
2. **≥5 SAFE candidates** — לאחר variant fetch צפוי מספיק מוצרי PASS עם size tag מ-variant source.
3. **T3 approval (אייל)** — אישור לפני Phase 6 live.

**Phase 6 NOT OPEN** — Shopify live: NO.

---

*Phase 5h — DRY RUN ONLY. אין שינויים ב-Shopify.*
