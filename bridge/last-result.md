task_id: 20260413-174747
---
---

**STAGE_VERDICT: PASS**

**CHANGES MADE:**
1. **`prompts/seo-aeo-rules.md`** (NEW) — Complete category-aware rules for SEO title, meta description, and FAQ across all 4 categories (reborn/shoes/clothing/accessories). Includes answer-first structure, priority bias, GSC winner protection, blacklist, and output format spec.
2. **`prompts/faq.md`** (UPDATED) — Added `{category}` input parameter and category routing block that forces topic selection per category before writing. Prevents clothing FAQ on non-clothing products.
3. **`teams/product/agents/seo-specialist.md`** (UPDATED) — Added required reading reference and category routing instruction.

**RULES ADDED:** 9 new rules including per-category formulas for title/description/FAQ, answer-first structure, GSC winner protection, priority bias ordering, and forbidden topics per category.

**EVIDENCE:** All 4 categories have dedicated rules in all 3 fields (12 rule sets total). No architecture changes, no Shopify live touched, no theme changes.

**SYSTEM STATE:** STAGE-4 complete. Ready for STAGE-5 (reborn dolls generation).