# Layer 6 — Phase 5g Taxonomy Pivot: Age → Size
**תאריך:** 2026-05-04
**Phase:** 5g — Business Decision: Replace CAT-B Age with Size Taxonomy
**PLANNING ONLY — DRY RUN — אין כתיבה ל-Shopify, אין commit, אין push**

---

## 1. SYSTEM STATE

| פרמטר | ערך |
|-------|-----|
| Phase 5f | ✅ COMPLETE (2026-05-04) — 7 bugs fixed, dry-run 58 products |
| Phase 5g (age-source pack) | ⚠️ SUPERSEDED — see section 3 |
| Phase 6 | NOT OPEN |
| Shopify live | NO |
| Git HEAD | d4a1c2e — "docs+logic(layer6): harden tagger after Phase 5e safety audit" |
| Phase 5f PASS | 23/58 | avg_quality | 80.6 |
| Phase 6 prior blocker | age_source — 6/9 candidates lacked reliable age evidence |
| New blocker | SIZE_PIVOT_REQUIRED — CAT-B must change before Phase 6 |

**Unstaged changes (DO NOT TOUCH):**
- M docs/product/reborn/reborn-landing-asset-map.md
- M docs/product/reborn/reborn-product-page-state.md
- M docs/product/reborn/reborn-task-checklist.md
- M teams/organic/agents/04-organic-blog-writer.md

**Old age-source report:**
- Path: `output/tags/phase5g-age-source-human-review-pack.md`
- Status: **UNTRACKED — not staged, not committed**
- Created under superseded age-source assumption. DO NOT STAGE.

---

## 2. BUSINESS DECISION (אייל — 2026-05-04)

> **BabyMania filters clothing and shoes by SIZE — not by age.**
> All other product types (accessories, toys, reborn, sleep, bath, swimming) require neither age nor size.

**Decision breakdown:**

| מוצר | מה נדרש לניווט | מה אינו נדרש |
|------|----------------|---------------|
| ביגוד (clothing) — romper, bodysuit, dress, set, pants, top, coat, hat, swimwear | `size-*` filter | ❌ `age-*` |
| נעליים (shoes) — shoes, sandals, sneakers, boots | `size-*` filter | ❌ `age-*` |
| בובת ריבורן | ללא size / age | ❌ שניהם |
| צעצועים / מוצרי שינה / אמבטיה / מצופים | ללא size / age | ❌ שניהם |

**Navigation intent:**

A customer on BabyMania searches for clothing or shoes by the size their baby wears — not by the baby's age bracket. Size labels like "מידה 3-6 חודשים" are familiar and product-specific. Age labels like "3-6 months" are ambiguous across product types (a 3-month-old can wear size NB or 0-3m depending on brand).

**This decision is final and supersedes all prior age-source research (Phase 5e, Phase 5g age-source pack).**

---

## 3. CURRENT PROBLEM — Why Age Was Wrong

### 3.1 What the current taxonomy specifies

`docs/organic/layer6-taxonomy-spec-v1.md` — Section 4 (CAT-B) defines:

```
CAT-B — Age Group
Prefix: age-
Tags: age-0-3m, age-3-6m, age-6-12m, age-12-18m, age-18-24m, age-2-3y, age-3-5y, age-newborn, age-unknown
Required for: clothing and shoes (Phase 5b rule)
Confidence minimum: 0.85
```

### 3.2 What this caused

- The tagger spent Phases 1–5f searching for a reliable age SOURCE in title/handle/existing_tags/YAML.
- Allowed sources were: title, description, existing Shopify tags, YAML age_range field, Shopify variant option.
- This created a long chain of heuristic problems:
  - `toddler` in handle → age-2-3y at confidence 0.75 (below spec minimum)
  - `first-walker` in handle → age-6-12m at confidence 0.75 (below spec minimum)
  - `newborn-clothing` existing tag vs `first-walker` handle → unresolvable conflict
  - "0-to-3-years-old" in handle → RANGE_TOO_BROAD (uncollapseable 3-year span)
- Phase 5e audit found 8 of 9 Phase 6 candidates UNSAFE due to age source problems.
- Phase 5f hardened the logic (7 bug fixes), correctly moving bad age tags to NO_AGE_FOUND.
- Phase 5g (old pack) recommended human review to supply missing age evidence.
- **None of this was useful** because age is not the correct filter dimension for BabyMania.

### 3.3 Why Phase 5f was still valuable

Phase 5f logic hardening corrected real bugs (gender priority, source labels, swimming ring classification, type specificity). These fixes remain valid regardless of the age→size pivot. The tagger logic for CAT-A, CAT-C, CAT-D, CAT-E, CAT-F, CAT-G is correct and unaffected.

Only CAT-B must change: from `age-*` to `size-*`.

---

## 4. NEW CAT-B PROPOSAL — Size Taxonomy

**Replace `age-*` prefix with `size-*` prefix throughout Layer 6.**

### 4.1 Size Tag Definitions

| internal_tag | customer_label_he | collection_slug | confidence_min | notes |
|---|---|---|---|---|
| size-newborn | NB / ניו בורן | size-newborn | 0.90 | Explicit "newborn" or "NB" in source |
| size-0-3m | 0-3 חודשים | size-0-3m | 0.88 | Explicit "0-3" or "0-3M" in source |
| size-3-6m | 3-6 חודשים | size-3-6m | 0.88 | Explicit "3-6" or "3-6M" |
| size-6-9m | 6-9 חודשים | size-6-9m | 0.88 | Explicit "6-9" or "6-9M" |
| size-9-12m | 9-12 חודשים | size-9-12m | 0.88 | Explicit "9-12" or "9-12M" |
| size-12-18m | 12-18 חודשים | size-12-18m | 0.88 | Explicit "12-18" or "12-18M" |
| size-18-24m | 18-24 חודשים | size-18-24m | 0.88 | Existing tag "18-24M" → mapped here |
| size-2y | מידה 2 | size-2y | 0.88 | "size 2" or "2T" or "2 year" in source |
| size-3y | מידה 3 | size-3y | 0.88 | "size 3" or "3T" or "3 year" in source |
| size-4y | מידה 4 | size-4y | 0.88 | "size 4" or "4T" or "4 year" in source |
| size-unknown | — | — | 0.00 | fallback — clothing/shoes with no size source |

### 4.2 Customer Navigation Labels

| internal_tag | customer_label_he | display format |
|---|---|---|
| size-newborn | ניו בורן / NB | NB |
| size-0-3m | 0-3 חודשים | 0-3M |
| size-3-6m | 3-6 חודשים | 3-6M |
| size-6-9m | 6-9 חודשים | 6-9M |
| size-9-12m | 9-12 חודשים | 9-12M |
| size-12-18m | 12-18 חודשים | 12-18M |
| size-18-24m | 18-24 חודשים | 18-24M |
| size-2y | מידה 2 | מידה 2 |
| size-3y | מידה 3 | מידה 3 |
| size-4y | מידה 4 | מידה 4 |

### 4.3 Size vs Age — Key Difference

| נושא | age-* (ישן) | size-* (חדש) |
|------|------------|-------------|
| מקור | גיל תינוק | מידת המוצר |
| מה מאפשר | סינון לפי גיל | סינון לפי מידה |
| מקור נתון | title/handle/tags (עמום) | **Shopify variant option values** (ספציפי) |
| דיוק | תלוי בשיקול דעת | תלוי בנתוני ה-variant בפועל |
| מתאים ל | רפואה/שלב התפתחות | **קנייה בחנות** |
| מה שIkea/H&M/Zara עושים | מוצג כמידה | מוצג כמידה |

---

## 5. SIZE SOURCE RULES

### 5.1 Allowed Sources (לפי סדר עדיפות)

| עדיפות | מקור | דוגמה |
|--------|------|--------|
| 1 (HIGHEST) | **Shopify variant `option` values** | size: "3-6M", "6-9M", "12-18M", "2T" |
| 2 | **YAML `size` or `variants` fields** | size_options: [0-3m, 3-6m] |
| 3 | **Shopify `title`** — explicit size declaration | "אוברול מידה 3-6 חודשים" |
| 4 | **Shopify current `tags`** — clean size tags | "6-12 חודש", "18-24M", "12-18 חודש" |
| 5 | **Shopify `description/body_html`** | explicit size table or mention |

**Note on existing Shopify tags:**
The current taxonomy includes existing tags like "0-3 חודש", "3-6 חודש", "6-12 חודש", "12-18 חודש", "18-24 חודש", "2-3 שנים", "18-24M" — these map cleanly to size-* tags:

| existing tag | maps to size-* |
|---|---|
| 0-3 חודש / 0-3 חודשים | size-0-3m |
| 3-6 חודש / 3-6 חודשים | size-3-6m |
| 6-12 חודש / 6-12 חודשים | size-6-9m + size-9-12m (or size-6-12m if added) |
| 12-18 חודש / 12-18 חודשים | size-12-18m |
| 18-24 חודש / 18-24 חודשים / 18-24M | size-18-24m |
| 2-3 שנים | size-2y (+ size-3y if product covers both) |

### 5.2 Forbidden Size Sources

- ❌ `toddler` in handle — handle keyword, NOT a size. May indicate age range but not product size.
- ❌ `infant` in handle — same problem.
- ❌ `first-walker` in handle — approximate developmental milestone, not a size.
- ❌ Collapsing a broad range (0-3y) into one size tag — use variant data instead.
- ❌ Malformed existing tag `3-6M6-9M` — tag is corrupt, not a valid source.
- ❌ `newborn-clothing` existing tag without verification — may be a legacy/incorrect tag.
- ❌ Inferring size from product type alone (e.g. "type-romper → size-0-3m").
- ❌ Inferring size from style, season, or price.

### 5.3 WIDE_RANGE still applies

Products with size ranges covering more than 18 months cannot receive a single size tag.
The WIDE_RANGE_PATS logic from Phase 5f remains valid and applies to size-* as well:
- "0-to-3-years-old" → RANGE_TOO_BROAD (3-year span, cannot collapse)
- "0-24m" → RANGE_TOO_BROAD
- "0-18m" → RANGE_TOO_BROAD

If a product sells across a wide range, the size tag should only reflect what the SPECIFIC AVAILABLE VARIANTS show.

---

## 6. NON-SIZE PRODUCTS

The following product types require **no size or age tag** under the new taxonomy.
CAT-B is fully exempt for these types (extends the existing Phase 5b NON_AGE_TYPES rule).

| type tag | product category | size required | age required |
|---|---|---|---|
| type-reborn-doll | בובות ריבורן | ❌ NO | ❌ NO |
| type-toy | צעצועים | ❌ NO | ❌ NO |
| type-sleep-soother | מוצרי שינה/הרגעה | ❌ NO | ❌ NO |
| type-bath-accessory | מוצרי אמבטיה | ❌ NO | ❌ NO |
| type-swimming-ring | מצופי שחייה | ❌ NO | ❌ NO |
| type-accessory | אביזרים | ❌ NO | ❌ NO |
| type-unknown | לא ידוע | ❌ NO | ❌ NO |

**Note:** type-hat requires further business decision — a baby hat has sizes (NB, 0-3m, 3-6m etc.) but is an accessory. Recommend: include in size-required list along with clothing/shoes, but defer to Phase 5h planning.

---

## 7. FILES THAT NEED CHANGES IN PHASE 5H

Phase 5h = Size Taxonomy Implementation. The following files require changes:

### 7.1 Specification Documents

| קובץ | שינוי נדרש |
|------|------------|
| `docs/organic/layer6-taxonomy-spec-v1.md` | Replace Section 4 (CAT-B Age) with new CAT-B Size spec. Update allowed_values, allowed_sources, forbidden_inference, confidence_min. Remove all `age-*` prefix references from CAT-B. |
| `docs/organic/layer6-full-tag-system-navigation-planning-spec-v1.md` | Update Section 4 (7 tag categories) — CAT-B row changes from Age to Size. Update navigation labels. Update Phase 9 navigation planning section. |

### 7.2 Tagger Logic

| קובץ | שינוי נדרש |
|------|------------|
| `scripts/tags/run_layer6_phase5d_rerun.py` | • Replace `CUSTOMER_LABELS` age-* entries with size-* entries. • Rename `extract_cat_b()` → `extract_cat_b_size()`. • Replace all age-* tag generation with size-* tag generation. • Update `HEB_AGE_MAP` → `HEB_SIZE_MAP` (existing Hebrew size tags). • Replace `NARROW_PATS` with size-equivalent patterns. • Remove `toddler_heuristic` and `first_walker_heuristic` entirely. • Update `build_md_report()` and `build_comparison_md()` labels. • Update `NON_AGE_TYPES` → `NON_SIZE_TYPES` (same set of types). |
| `scripts/tags/layer6_validate_tags.py` | • Replace `ALLOWED_VALUES["CAT-B"]` — change all `age-*` → `size-*` values. • Update `NON_AGE_TYPES` → `NON_SIZE_TYPES`. • Update `_catb_exempt()` → `_catb_size_exempt()` or rename. • Update `WIDE_RANGE_PATS` note (logic stays same, applies to size). |

### 7.3 Output/Report Generators

| קובץ | שינוי נדרש |
|------|------------|
| `scripts/tags/run_layer6_phase5d_rerun.py` (report functions) | • Phase 5h runner will output to `phase5h-size-*` files. • MD report header: "Phase 5h Size-Based Dry Run". • Comparison columns: size vs age candidates. |

### 7.4 Files NOT to change

| קובץ | סיבה |
|------|-------|
| All Phase 5a–5f output files | Historical record. Keep as-is. |
| `output/tags/phase5g-age-source-human-review-pack.md` | Untracked. Superseded. Leave untracked. |
| CAT-A, CAT-C, CAT-D, CAT-E, CAT-F, CAT-G logic | Unaffected by pivot. Phase 5f fixes remain valid. |

---

## 8. PHASE 6 IMPACT

### Current status

Phase 6 remains blocked. The prior blocker (age source evidence for 6 candidates) is now moot. The new blocker is the CAT-B taxonomy pivot itself — Phase 6 cannot proceed until size taxonomy is implemented and validated.

### Path to Phase 6

```
Phase 5h (SIZE TAXONOMY IMPLEMENTATION)
  ├── Update docs: layer6-taxonomy-spec-v1.md (CAT-B → size)
  ├── Update tagger: run_layer6_phase5d_rerun.py (age-* → size-*)
  ├── Update validator: layer6_validate_tags.py (age-* → size-*)
  ├── Create Phase 5h runner: run_layer6_phase5h_dryrun.py
  ├── Run dry-run on same 58-product sample
  └── Output: phase5h-size-dryrun-report.md + .json + sample.json

Phase 5h PASS criteria (proposed):
  ├── ≥5 clothing/shoes products with size-* tag from Shopify variant data
  ├── 0 BLOCKED products
  ├── avg quality score ≥ 75
  ├── 0 forbidden size inferences
  └── All Phase 5f logic fixes remain intact (CAT-A/C/D/E/F/G)

Phase 5i (HUMAN REVIEW — size candidates)
  └── אייל reviews candidate list → provides T3 approval

Phase 6 (LIVE BATCH)
  └── T3 approval → 10-20 product pilot → size-* tags pushed to Shopify
```

### What changes and what doesn't

| נושא | Phase 5f state | Phase 5h state |
|------|----------------|----------------|
| CAT-A (type) | ✅ stable | ✅ unchanged |
| CAT-B (age → size) | ❌ broken — age wrong for BabyMania | ✅ to be fixed |
| CAT-C (season) | ✅ stable (Bug 6 fixed) | ✅ unchanged |
| CAT-D (fabric) | ✅ stable (Bug 6 fixed) | ✅ unchanged |
| CAT-E (occasion) | ✅ stable | ✅ unchanged |
| CAT-F (gender) | ✅ stable (Bug 4 fixed) | ✅ unchanged |
| CAT-G (style) | ✅ stable | ✅ unchanged |
| Swimming ring | ✅ correctly exempt (Bug 7) | ✅ unchanged |
| type-sneakers override | ✅ working (Bug 5) | ✅ unchanged |

### Expected Phase 5h outcome

The size-* approach has a structural advantage over age-*: **Shopify variant option values are the primary source**. Many BabyMania clothing products already have size variants (e.g. "3-6M", "6-9M", "12-18M"). Querying variant options directly from Shopify API will yield much higher confidence and coverage than trying to extract age from handle keywords.

This means Phase 5h dry-run should produce **more PASS products and fewer NO_SIZE_FOUND** than the age-based runs produced NO_AGE_FOUND.

---

## 9. FINAL VERDICT

**SIZE_PIVOT_REQUIRED**
**PHASE6_STILL_BLOCKED**

| תנאי | סטטוס |
|------|--------|
| Phase 5f complete | ✅ |
| Business decision clear | ✅ — age → size pivot confirmed by אייל |
| CAT-B spec updated | ❌ — Phase 5h required |
| Tagger updated for size | ❌ — Phase 5h required |
| Validator updated for size | ❌ — Phase 5h required |
| Size dry-run complete | ❌ — Phase 5h required |
| ≥5 safe size candidates | ❌ — not yet run |
| T3 approval (אייל) | ❌ — not yet requested |
| Phase 6 NOT OPEN | ✅ |
| Shopify live NO | ✅ |

**Recommended next step:** Begin Phase 5h — Size Taxonomy Implementation.
Start with: update `docs/organic/layer6-taxonomy-spec-v1.md` Section 4, then update tagger logic, then run dry-run.

---

*Phase 5g — PLANNING ONLY. אין כתיבה ל-Shopify. אין commit. אין push.*
