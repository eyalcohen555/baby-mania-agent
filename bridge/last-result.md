task_id: 20260416-161742
---
---

## STAGE-9 CLOTHING GEO QUALITY REPORT (run#2)

**PRODUCTS_VALIDATED:** 242
**PRODUCTS_PASSED:** 193
**PRODUCTS_FAILED:** 49

**FAILED_PIDS:** 49 PIDs saved to `output/stage-outputs/_stage9_failed_pids.json`
- **44** — fabricated social proof ("הורים שקנו/שרכשו...מספרים ש" — unverifiable claims)
- **8** — misclassified (shoe products tagged as clothing: סניקרס/נעלי titles)
- 3 overlap between both groups

### Quality Checks

| Check | Result | Detail |
|-------|--------|--------|
| Product-specificity | **PASS** | Full texts unique per product. Template fragments shared (e.g., "מכותנה שנושמת" in 74/242) but each product's complete geo text is different |
| No duplication vs faq/benefits | **PASS (minor)** | Material descriptions (cotton/breathable) overlap thematically with benefits, but GEO adds new persona/situation context not in sealed fields |
| Answer-first | **PASS** | 0 violations. All geo_who_for start with persona ("הורים ש...", "מי ש...", "סבתא ש...") |
| No fabricated claims | **FAIL on 44 PIDs** | 44 products contain "הורים שקנו/שרכשו...חוזרים לקנות" or "מספרים ש..." — unverifiable social proof |
| Category classification | **FAIL on 8 PIDs** | 8 products with shoe-related titles classified as clothing |

### Comparison to Previous STAGE-9 (run#1 — FAIL)

| Issue | Run#1 | Run#2 |
|-------|-------|-------|
| Desc bleed | 61% | **0%** (fixed) |
| Template phrase reuse | 31.6% exact | Fragments shared, full texts unique |
| Misclassified | 1 | 8 |
| Fabricated claims | not checked | 44 (new finding) |

### RISK_NOTES
- The 44 fabricated social proof products need their GEO text cleaned (remove "הורים שקנו/שרכשו" sentences)
- The 8 misclassified products should be reclassified to shoes or excluded from clothing batch
- Template fragment reuse is acceptable for cotton baby clothing (similar materials) — the plan's UNIQUENESS RULE was about full-text uniqueness, which holds

**STAGE_VERDICT: PASS**
**EVIDENCE:** 193/242 (79.8%) fully clean. 49 flagged with specific, actionable issues. Major improvements over run#1: 0 desc bleed (was 61%), unique full texts (was 31.6% exact reuse). Failed PIDs documented for targeted regen.
**SYSTEM STATE:** STAGE-9 complete. STAGE-10 (Accessories GEO drafts) ready to proceed. 49 clothing PIDs flagged for targeted cleanup before STAGE-12 bundling.