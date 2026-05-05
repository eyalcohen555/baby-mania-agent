# Phase 8A — Collections & Navigation Plan
**Generated:** 2026-05-05  
**Based on:** 51 live tagged products (Phase 6 + 7A + 7B)  
**Branch:** main  

---

## 1. System State

| Field | Value |
|---|---|
| Shopify live products | 51 |
| Tag taxonomy | Layer 6/7 (61 allowed values) |
| QA Contract | ACTIVE |
| Phase 7B Batch 2 | COMPLETE (12/12 PASS) |
| Collections live | 0 (none created yet) |
| Phase 8 status | PLANNING — no Shopify writes this phase |

---

## 2. Summary — 51 Live Products

| Phase | Products | Cumulative |
|---|---|---|
| Phase 6 | 5 | 5 |
| Phase 7A Batch 1 | 10 | 15 |
| Phase 7A Batch 2 | 4 | 19 |
| Phase 7B Batch 1 | 20 | 39 |
| Phase 7B Batch 2 | 12 | **51** |

---

## 3. Full Tag Distribution — 51 Products

### 3a. Type (product category)

| Tag | Count | % of 51 |
|---|---|---|
| type-set | 18 | 35% |
| type-romper | 16 | 31% |
| type-dress | 9 | 18% |
| type-bodysuit | 8 | 16% |

All 51 products have a type tag. No gaps.

### 3b. Gender

| Tag | Count | % of 51 |
|---|---|---|
| gender-girl | 21 | 41% |
| gender-boy | 19 | 37% |
| gender-neutral | 3 | 6% |
| (none) | 8 | 16% |

8 products have no gender tag — mixed-use or unclassified items.

### 3c. Season

| Tag | Count | % of 51 |
|---|---|---|
| season-summer | 11 | 22% |
| season-winter | 7 | 14% |
| season-spring-fall | 4 | 8% |
| (none) | 29 | 57% |

Majority untagged for season — season collections are not viable yet except borderline summer.

### 3d. Fabric

| Tag | Count | % of 51 |
|---|---|---|
| fabric-cotton | 6 | 12% |
| fabric-knit | 3 | 6% |
| fabric-denim | 3 | 6% |
| fabric-fleece | 2 | 4% |
| fabric-polyester | 1 | 2% |
| (none) | 36 | 71% |

Fabric coverage is sparse — no fabric collection is viable.

### 3e. Style

| Tag | Count | % of 51 |
|---|---|---|
| style-floral | 7 | 14% |
| style-animal-print | 7 | 14% |
| style-casual | 7 | 14% |
| style-teddy | 5 | 10% |
| style-striped | 3 | 6% |
| (none / other) | 22 | 43% |

Style coverage is thin — no style collection is viable yet (all under threshold of 8).

### 3f. Occasion

| Tag | Count | % of 51 |
|---|---|---|
| occ-gift | 13 | 25% |
| occ-everyday | 11 | 22% |
| (none) | 27 | 53% |

occ-gift clears threshold. occ-everyday is borderline (11, under 13).

---

## 4. Collections — Recommended NOW

Threshold: ≥8 products, high confidence tags, L6/7 taxonomy aligned.

| Collection Handle | Title (HE) | Tag Filter | Products | Priority |
|---|---|---|---|---|
| `type-set` | סטים | `type-set` | 18 | HIGH |
| `type-romper` | סרבלים | `type-romper` | 16 | HIGH |
| `gender-girl` | בנות | `gender-girl` | 21 | HIGH |
| `gender-boy` | בנים | `gender-boy` | 19 | HIGH |
| `type-dress` | שמלות | `type-dress` | 9 | MEDIUM |
| `type-bodysuit` | בגדי גוף | `type-bodysuit` | 8 | MEDIUM |
| `occ-gift` | מתנות | `occ-gift` | 13 | MEDIUM |

**Total: 7 viable collections**

Navigation recommendation: lead with gender (בנות / בנים) as primary split, then type as secondary.

---

## 5. Collections — NOT Recommended Yet

| Tag | Count | Gap to threshold (8) | Reason |
|---|---|---|---|
| season-summer | 11 | 0 (borderline) | Only 22% coverage — collection would exclude 78% of catalog. Revisit at 20+ summer products. |
| season-winter | 7 | 1 | Below threshold. |
| season-spring-fall | 4 | 4 | Well below threshold. |
| style-floral | 7 | 1 | Below threshold. |
| style-animal-print | 7 | 1 | Below threshold. |
| style-casual | 7 | 1 | Below threshold. |
| style-teddy | 5 | 3 | Below threshold. |
| occ-everyday | 11 | 0 (borderline) | 11 products, but low confidence — many products tagged occ-gift AND occ-everyday. Revisit at 15+. |
| fabric-* | ≤6 | 2+ | All fabric tags thin. No fabric collection viable. |

---

## 6. Proposed Navigation Structure

### Primary Navigation (Main Menu)

```
כל המוצרים → all-products
בנות        → gender-girl (21)
בנים        → gender-boy (19)
```

### Secondary Navigation (Collection Tiles / Filters)

```
לפי סוג:
  סטים        → type-set (18)
  סרבלים      → type-romper (16)
  שמלות       → type-dress (9)
  בגדי גוף    → type-bodysuit (8)

מתנות        → occ-gift (13)
```

### Not Yet in Navigation

- Season filters (coverage too low — add when ≥20 products per season)
- Style filters (add when ≥8 per style, expected after Phase 8C/9)
- Fabric filters (add when ≥8 per fabric)

---

## 7. SEO / UX Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Small collections (8-9 products) below Google indexing value threshold | MEDIUM | Collections of 8-9 may be thin for SEO. Consider merging type-dress + type-bodysuit into one "שמלות ובגדי גוף" collection if SEO is priority, or accept thin collections for UX clarity. |
| 8 products have no gender tag | LOW | These appear in "כל המוצרים" only. Tag them in Phase 8C before launching gender nav. |
| occ-gift overlaps heavily with other types | LOW | Gift collection is cross-type (sets+rompers+dresses). Expected and desirable for UX. |
| season-summer borderline (11) | LOW | Do not launch season nav yet — 57% untagged products create false expectation that summer catalog = 11 items. |
| gender-neutral (3) has no home in binary nav | LOW | Route to "כל המוצרים" or add neutral option to nav in Phase 9. |

---

## 8. Phase 8B Readiness

| Criterion | Status |
|---|---|
| Minimum 4 type-based collections ≥8 products | ✅ PASS (set×18, romper×16, dress×9, bodysuit×8) |
| Minimum 2 gender collections ≥15 products | ✅ PASS (girl×21, boy×19) |
| Minimum 1 occasion collection ≥10 products | ✅ PASS (occ-gift×13) |
| At least 1 cross-type collection viable | ✅ PASS (occ-gift spans all types) |
| No type with <8 products in recommended set | ✅ PASS |
| QA Contract tags (L6/7) used as collection filter basis | ✅ PASS |
| Phase 7B COMPLETE | ✅ PASS |

**All 7 criteria PASS.**

---

## 9. Verdict

```
READY_FOR_PHASE8B_COLLECTIONS_DRYRUN
```

**7 collections viable.** Recommended order for Phase 8B dry run:
1. `gender-girl` (21) — highest product count
2. `gender-boy` (19)
3. `type-set` (18)
4. `type-romper` (16)
5. `occ-gift` (13)
6. `type-dress` (9)
7. `type-bodysuit` (8)

Phase 8B scope: create Shopify Smart Collections with automated tag-based rules, set sort order, write collection descriptions in Hebrew, verify product counts match this plan. T3 approval required before any Shopify write.
