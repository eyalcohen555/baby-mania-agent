# Layer 6 — Phase 5e Candidate Safety Audit
**תאריך:** 2026-05-04  
**ביצוע:** AUDIT ONLY — אין כתיבה ל-Shopify, אין commit, אין push  
**מקור:** Phase 5d Rerun (9 candidates)

---

## 1. SYSTEM STATE

| פרמטר | ערך |
|-------|-----|
| Phase 5d status | COMPLETE — WAITING AYAL REVIEW |
| Phase 6 | NOT OPEN |
| Shopify live | NO |
| Git HEAD actual | **f33ddd1** (one commit above expected 8f2a52e) |
| Commit f33ddd1 | "docs: close bridge room prototypes 1-3 5-6" — docs only, no Layer 6 impact |
| Phase 5d files | UNCHANGED by f33ddd1 |
| Unstaged files (do not touch) | docs/product/reborn/*.md, teams/organic/agents/04-organic-blog-writer.md |

---

## 2. FILES READ

| קובץ | סטטוס |
|------|--------|
| BABYMANIA-MASTER-PROMPT.md | ✅ READ |
| docs/organic/מצב-הפרויקט-האורגני.md | ✅ READ |
| docs/organic/organic-journal.md | ✅ READ |
| docs/organic/layer6-taxonomy-spec-v1.md | ✅ READ |
| docs/organic/layer6-full-tag-system-navigation-planning-spec-v1.md | ✅ READ |
| output/tags/phase5d-rerun-comparison.md | ✅ READ |
| output/tags/phase5d-rerun-report.md | ✅ READ |
| output/tags/phase5d-rerun-report.json | ✅ READ |
| output/tags/phase5d-rerun-sample-59.json | ✅ READ (all 9 candidates extracted) |
| output/tags/phase5-human-review-pack.md | ✅ READ |
| output/tags/phase5-human-review-summary.md | ✅ READ |

---

## 3. GIT STATE

```
HEAD: f33ddd1 — "docs: close bridge room prototypes 1-3 5-6"
Expected HEAD per task: 8f2a52e — "docs(layer6): add Phase 5d rerun after taxonomy updates"
Delta: 1 commit ahead — documentation only, no Layer 6 file changes
Confirmed: output/tags/ Phase 5d files are unchanged
```

**Unstaged changes (DO NOT TOUCH):**
- M docs/product/reborn/reborn-landing-asset-map.md
- M docs/product/reborn/reborn-product-page-state.md
- M docs/product/reborn/reborn-product-page-state.md
- M teams/organic/agents/04-organic-blog-writer.md

---

## 4. PHASE 5D SUMMARY

| מדד | ערך |
|-----|-----|
| מוצרים שנבדקו | 59 |
| PASS | 30 (50.8%) |
| NEEDS_REVIEW | 29 (49.2%) |
| BLOCKED | 0 |
| avg quality score | 82.3 |
| NO_AGE_FOUND (total) | 32 |
| NO_AGE_FOUND (clothing/shoes only) | ~18 |
| RANGE_TOO_BROAD | 4 |
| type-sleep-soother (new) | 1 (פיל נושם — תוקן מ-type-reborn-doll) |
| Phase6 candidates suggested | 9 |

---

## 5. 9 CANDIDATE TABLE

| # | product_id | title (קצר) | type | age | score | phase5d status | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 9688932909369 | אוברול אריה חמוד דגם שמר | type-romper | age-2-3y | 86.4 | PASS | **REVIEW_ONLY** |
| 2 | 9874906349881 | אוברול ג'ינס מתוק דגם זוהר | type-romper | age-newborn | 96.6 | PASS | **REVIEW_ONLY** |
| 3 | 9688660312377 | אוברול ג׳ינס דגם אתי | type-romper | age-2-3y | 96.2 | PASS | **REVIEW_ONLY** |
| 4 | 9895864205625 | אוברול ג'ינס יוניסקס דגם שלו | type-romper | age-2-3y | 93.8 | PASS | **REJECT** |
| 5 | 9687579033913 | אוברול לבבות דגם הילה | type-romper | age-2-3y | 89.7 | PASS | **REVIEW_ONLY** |
| 6 | 9615375565113 | נעל אלגנטית צעד ראשון לבנות | type-shoes | age-6-12m | 95.4 | PASS | **REVIEW_ONLY** |
| 7 | 9606764462393 | נעל קז'ואל במיוחד לתינוקות | type-shoes | age-2-3y | 94.5 | PASS | **REVIEW_ONLY** |
| 8 | 9606764298553 | נעלי אופנה קז'ואל מונעות החלקה | type-shoes | age-2-3y | 94.5 | PASS | **REVIEW_ONLY** |
| 9 | 9838580662585 | מצוף שחייה לתינוקות | type-swimming-ring | EXEMPT | 80.2 | PASS | **REVIEW_ONLY** |

---

## 6. PRODUCT-BY-PRODUCT EVIDENCE

---

### Candidate 1 — 9688932909369 | אוברול אריה חמוד דגם שמר

| שדה | ערך |
|-----|-----|
| handle | babys-little-lion-print-casual-long-sleeve-romper-hat-baby-mittens-toddler-infant-boys-bodysuit |
| product_group | clothing_yaml |
| has_yaml | true |
| current_tags | אוברול |
| proposed_tags | type-romper, age-2-3y, season-unknown, occ-everyday, gender-boy, style-casual |
| quality_score | 86.4 |

**Source Traces:**

| tag | source | confidence | rule |
|-----|--------|------------|------|
| type-romper | existing_tag "אוברול" | 0.88 | tag_map |
| age-2-3y | handle (toddler) | **0.75** | toddler_heuristic |
| season-unknown | category_default | 0.00 | fallback |
| gender-boy | handle "boys" | 0.90 | keyword |
| style-casual | title | 0.80 | keyword |

**Evidence checks:**

- **type:** type-romper ← existing_tag "אוברול" ✅ approved, confidence 0.88 ≥ 0.90 minimum ≈ acceptable (existing_tag is MEDIUM source, not YAML)
- **age:** age-2-3y ← handle "toddler" via toddler_heuristic, confidence **0.75 < 0.85 MINIMUM** for required CAT-B tag
  - taxonomy-spec-v1 rule 10.2: "required tag + confidence < 0.85 → לא להוסיף → tag = *-unknown"
  - VIOLATION: age-2-3y should not have been added — should be age-unknown
  - Additional conflict: handle contains BOTH "toddler" (2-3y) AND "infant" (≈ 0-6m) — contradictory age signals
- **gender:** gender-boy ← handle "boys" keyword, confidence 0.90 ✅ source clear
- **season:** season-unknown (fallback) — acceptable for a romper with no season signal
- **variants/sizes evidence:** no variant data inspected — handle is only source
- **handle conflicts:** handle has "toddler-infant-boys" — both toddler and infant present = age source unreliable

**VERDICT: REVIEW_ONLY**
**Reason:** age-2-3y confidence 0.75 below 0.85 minimum threshold. Handle conflict (toddler AND infant). Age tag must be age-unknown per spec.

---

### Candidate 2 — 9874906349881 | אוברול ג'ינס מתוק מבית בייבי מניה דגם זוהר

| שדה | ערך |
|-----|-----|
| handle | baby-summer-clothing-denim-rompers-toddler-newborn-baby-boys-girls-sleeveless-button-pocket-rompers-jumpsuits-casual-outfits |
| product_group | clothing_yaml |
| has_yaml | true |
| current_tags | אוברול |
| proposed_tags | type-romper, age-newborn, season-summer, fabric-denim, occ-everyday, gender-girl, style-casual |
| quality_score | 96.6 |

**Source Traces:**

| tag | source | confidence | rule |
|-----|--------|------------|------|
| type-romper | existing_tag "אוברול" | 0.88 | tag_map |
| age-newborn | handle "newborn" | **0.85** | regex_narrow |
| season-summer | **"title"** (claimed) | 0.88 | keyword |
| fabric-denim | title/handle | 0.90 | keyword |
| gender-girl | handle "girls" | 0.90 | keyword |

**Evidence checks:**

- **type:** type-romper ← existing_tag ✅
- **age:** age-newborn ← handle contains "newborn" explicitly, regex_narrow at 0.85 (exactly at threshold)
  - Handle conflict: handle also contains "toddler" (2-3y signal contradicts newborn)
  - "regex_narrow" is stronger than "toddler_heuristic" but conflict remains
- **gender:** gender-girl ← handle "girls" ✅ — handle also has "boys" but "girls" is explicit
- **season:** season-summer — JSON records src=**title**, confidence 0.88
  - Hebrew title "אוברול ג'ינס מתוק מבית בייבי מניה דגם זוהר" does NOT contain "summer" or "קיץ"
  - "summer" IS in the handle: "baby-summer-clothing"
  - **SOURCE LABEL MISMATCH:** system labeled source as "title" but evidence is in handle
  - G3 (SOURCE_TRACEABLE) concern: auditor looking at title will not find "summer"
- **fabric-denim:** title/handle source — handle has "denim-rompers" ✅
- **handle conflicts:** toddler AND newborn both present — age reliability question

**VERDICT: REVIEW_ONLY**
**Reason:** Source label mismatch — season-summer attributed to "title" but "summer" is in the handle, not the Hebrew title. Handle age conflict (toddler+newborn). G3 SOURCE_TRACEABLE concern.

---

### Candidate 3 — 9688660312377 | אוברול ג׳ינס דגם אתי
**(P2 Special Check — was age still wrong?)**

| שדה | ערך |
|-----|-----|
| handle | babys-stylish-ruffled-ripped-denim-long-sleeve-belted-romper-toddler-infant-girls-button-down-bodysuit-for-spring-fall-outdoor-wear |
| product_group | clothing_yaml |
| has_yaml | true |
| current_tags | אוברול |
| proposed_tags | type-romper, age-2-3y, season-spring-fall, fabric-denim, occ-everyday, gender-girl, style-modern |
| quality_score | 96.2 |

**Source Traces:**

| tag | source | confidence | rule |
|-----|--------|------------|------|
| type-romper | existing_tag "אוברול" | 0.88 | tag_map |
| age-2-3y | handle "toddler" | **0.75** | toddler_heuristic |
| season-spring-fall | "title" (claimed) | 0.85 | keyword |
| fabric-denim | title | 0.90 | keyword |
| gender-girl | handle "girls" | 0.90 | keyword |
| style-modern | body | 0.78 | keyword_desc |

**Evidence checks:**

- **type:** type-romper ← existing_tag ✅
- **age — P2 SPECIAL CHECK:** age-2-3y ← handle "toddler_heuristic", confidence **0.75 < 0.85 MINIMUM**
  - Handle conflict: contains BOTH "toddler" AND "infant" — same issue from Phase 5 human review
  - **Phase 5 review pack noted this explicitly as age conflict**
  - **RESULT: AGE IS STILL WRONG in Phase 5d** — confidence below threshold + handle conflict unresolved
- **season:** source labeled "title" — Hebrew title "אוברול ג׳ינס דגם אתי" does NOT contain "spring-fall"
  - "spring-fall" IS in handle: "for-spring-fall-outdoor-wear"
  - **SOURCE LABEL MISMATCH** — title vs handle
- **gender:** gender-girl ← handle "girls" ✅
- **fabric-denim:** title source — title in Hebrew doesn't contain "denim". Handle has "denim". Source label mismatch.

**P2 ANSWER: YES — age is STILL wrong in Phase 5d.** Confidence 0.75 below threshold. Handle conflict identical to Phase 5 issue.

**VERDICT: REVIEW_ONLY**
**Reason:** Age still wrong (P2 confirmed). Confidence 0.75 < 0.85. Handle conflict (toddler+infant). Multiple source label mismatches (title vs handle).

---

### Candidate 4 — 9895864205625 | אוברול ג'ינס יוניסקס לתינוקות דגם שלו

| שדה | ערך |
|-----|-----|
| handle | diimuu-baby-children-boys-clothes-rompers-toddler-kids-overalls-denim-pants-casual-toddler-unisex |
| product_group | clothing_yaml |
| has_yaml | true |
| current_tags | אוברול |
| proposed_tags | type-romper, age-2-3y, season-unknown, fabric-denim, occ-everyday, **gender-boy**, style-casual |
| quality_score | 93.8 |

**Source Traces:**

| tag | source | confidence | rule |
|-----|--------|------------|------|
| type-romper | existing_tag "אוברול" | 0.88 | tag_map |
| age-2-3y | handle "toddler" | **0.75** | toddler_heuristic |
| fabric-denim | title | 0.90 | keyword |
| gender-boy | handle "boys" | **0.90** | keyword |
| style-casual | title | 0.80 | keyword |

**Evidence checks:**

- **type:** type-romper ← existing_tag ✅
- **age:** age-2-3y ← handle "toddler_heuristic", confidence **0.75 < 0.85 MINIMUM**
- **gender — CRITICAL FAILURE:**
  - Proposed: gender-boy ← handle "boys" keyword
  - Title: "אוברול ג'ינס יוניסקס לתינוקות דגם שלו" — contains **"יוניסקס"**
  - taxonomy-spec-v1 CAT-F allowed_sources: "Shopify title — 'ניוטרלי', 'unisex'" ← "יוניסקס" maps to gender-neutral
  - Source hierarchy: YAML > title (HIGH) > handle (MEDIUM-HIGH)
  - The title explicitly declares "יוניסקס" = gender-neutral, which is a HIGHER-PRIORITY source than handle "boys"
  - The system assigned gender-boy from the lower-priority handle source, OVERRIDING the explicit title declaration
  - **G4 NO_FORBIDDEN_INFERENCE VIOLATION:** gender inferred from handle keyword despite title explicitly declaring the contrary
  - Correct tag: gender-neutral (from title "יוניסקס")
  - Handle also has "unisex" as the last word — "diimuu-baby-children-boys-clothes-...toddler-unisex" — further evidence of neutral
- **Two critical failures: age below threshold + wrong gender**

**VERDICT: REJECT**
**Reason:** gender-boy is WRONG — title explicitly says "יוניסקס" (unisex = gender-neutral). System used lower-priority handle "boys" and ignored higher-priority title "יוניסקס". This is a G4 violation. Cannot push gender-boy to Shopify for a product explicitly declared as unisex.

---

### Candidate 5 — 9687579033913 | אוברול לבבות דגם הילה

| שדה | ערך |
|-----|-----|
| handle | babys-cartoon-heart-full-print-ruffle-decor-ribbed-long-sleeve-cotton-romper-toddler-girls-long-sleeve-pullover |
| product_group | clothing_yaml |
| has_yaml | true |
| current_tags | אוברול |
| proposed_tags | type-romper, age-2-3y, season-winter, fabric-cotton, occ-everyday, gender-girl |
| quality_score | 89.7 |

**Source Traces:**

| tag | source | confidence | rule |
|-----|--------|------------|------|
| type-romper | existing_tag "אוברול" | 0.88 | tag_map |
| age-2-3y | handle "toddler" | **0.75** | toddler_heuristic |
| season-winter | "title" (claimed) | 0.88 | keyword |
| fabric-cotton | "title" (claimed) | 0.90 | keyword |
| gender-girl | handle "girls" | 0.90 | keyword |

**Evidence checks:**

- **type:** type-romper ← existing_tag ✅
- **age:** age-2-3y ← toddler_heuristic, confidence **0.75 < 0.85 MINIMUM**
  - Handle has "toddler" and "girls" but no direct age conflict (no "infant" seen)
  - Still below minimum threshold
- **gender:** gender-girl ← handle "girls" ✅
- **season-winter:** src=title, confidence 0.88 — Hebrew title "אוברול לבבות דגם הילה" does NOT contain "winter" or "חורף"
  - Handle "babys-cartoon-heart-full-print-ruffle-decor-ribbed-long-sleeve-cotton-romper-toddler-girls" does NOT contain "winter" either
  - **No verifiable source for season-winter** — possible the season came from body_html, but source labeled as "title"
  - **SOURCE LABEL MISMATCH or SOURCE NOT TRACEABLE**
- **fabric-cotton:** src=title, confidence 0.90 — Handle has "cotton-romper" ✅ but source labeled as "title" not "handle"
  - Source label mismatch — verifiable from handle, not title
- **handle conflicts:** no age conflict (only "toddler"), but age still below threshold

**VERDICT: REVIEW_ONLY**
**Reason:** Age confidence 0.75 below 0.85 minimum. Season source not traceable (labeled as "title" but Hebrew title doesn't contain "winter"). Source label mismatch on fabric-cotton.

---

### Candidate 6 — 9615375565113 | נעל אלגנטית צעד ראשון לבנות
**(P3 Special Check — was age still wrong?)**

| שדה | ערך |
|-----|-----|
| handle | girls-mary-jane-shoes-children-solid-color-bow-round-toe-bow-2024-new-kids-fashion-soft-moccasin-shoes-baby-first-walker-shoes |
| product_group | shoes_yaml |
| has_yaml | true |
| current_tags | baby-gift, baby-shoes, elegant-baby, everyday-baby-wear, girls-clothing, **newborn-clothing** |
| proposed_tags | type-shoes, age-6-12m, season-unknown, occ-gift, occ-special-event, occ-everyday, occ-first-step, gender-girl, style-elegant |
| quality_score | 95.4 |

**Source Traces:**

| tag | source | confidence | rule |
|-----|--------|------------|------|
| type-shoes | existing_tag "baby-shoes" | 0.88 | tag_map |
| age-6-12m | handle "first-walker" | **0.75** | first_walker_heuristic |
| season-unknown | category_default | 0.00 | fallback |
| occ-gift | existing_tag "baby-gift" | 0.88 | tag_map |
| occ-first-step | title "צעד ראשון" | 0.90 | keyword |
| gender-girl | existing_tag "girls-clothing" | 0.90 | tag_map |
| style-elegant | existing_tag "elegant-baby" | 0.85 | tag_map |

**Evidence checks:**

- **type:** type-shoes ← existing_tag "baby-shoes" ✅ approved, clear
- **age — P3 SPECIAL CHECK:**
  - Proposed: age-6-12m ← handle "first-walker" via first_walker_heuristic, confidence **0.75 < 0.85 MINIMUM**
  - CONFLICT: existing tag "newborn-clothing" on Shopify = implies age 0-3m (newborn range)
  - These two sources give OPPOSITE age signals (0-3m vs 6-12m)
  - **RESULT: AGE IS STILL WRONG in Phase 5d** — same conflict from Phase 5 human review unresolved
  - To verify correct age: must check Shopify product page or variants — requires live access
- **gender:** gender-girl ← existing_tag "girls-clothing" (0.90) ✅ clean source
- **type correct:** type-shoes is appropriate (not sneakers/sandals — handle has "moccasin-shoes")
- **season:** season-unknown = correct for an all-season shoe ✅

**P3 ANSWER: YES — age is STILL wrong in Phase 5d.** "newborn-clothing" existing tag directly conflicts with proposed age-6-12m. Both sources are present and contradictory.

**VERDICT: REVIEW_ONLY**
**Reason:** Age still wrong (P3 confirmed). age-6-12m confidence 0.75 below 0.85 minimum. Existing tag "newborn-clothing" directly contradicts proposed age. Cannot resolve without Shopify live verification (violates "no Shopify live required" criterion for SAFE_FOR_PHASE6).

---

### Candidate 7 — 9606764462393 | נעל קז'ואל במיוחד לתינוקות
**(P4 Special Check — was age still wrong?)**

| שדה | ערך |
|-----|-----|
| handle | baby-toddler-shoes-four-seasons-shoes-0-to-3-years-old-baby-shoes-soft-bottom-non-slip-girls-boys-mesh-breathable-single-shoes |
| product_group | shoes_yaml |
| has_yaml | true |
| current_tags | baby-gift, baby-shoes, everyday-baby-wear, neutral-baby-outfit, newborn-clothing |
| proposed_tags | type-shoes, age-2-3y, season-unknown, occ-gift, occ-everyday, gender-neutral, style-casual |
| quality_score | 94.5 |

**Source Traces:**

| tag | source | confidence | rule |
|-----|--------|------------|------|
| type-shoes | existing_tag "baby-shoes" | 0.88 | tag_map |
| age-2-3y | handle "toddler" | **0.75** | toddler_heuristic |
| season-unknown | category_default | 0.00 | fallback ("four-seasons" → unknown) ✅ |
| occ-gift | existing_tag "baby-gift" | 0.88 | tag_map |
| gender-neutral | existing_tag "neutral-baby-outfit" | 0.88 | tag_map |
| style-casual | title "קז'ואל" | 0.80 | keyword |

**Evidence checks:**

- **type:** type-shoes ← existing_tag "baby-shoes" ✅
- **gender:** gender-neutral ← existing_tag "neutral-baby-outfit" ✅ clear source
- **season:** season-unknown ← "four-seasons" in handle = correct logic ✅
- **age — P4 SPECIAL CHECK:**
  - Proposed: age-2-3y ← "baby-toddler" in handle via toddler_heuristic, confidence **0.75 < 0.85 MINIMUM**
  - Handle also contains "0-to-3-years-old" — this is a 3-year range (0-36m)
  - taxonomy-spec rule: handle "0-to-3-years-old" should trigger RANGE_TOO_BROAD (similar to "0-24m" logic)
  - Phase 5d did NOT fire RANGE_TOO_BROAD for this product — inconsistency with product 10005779808569 (which WAS blocked for "0-24m")
  - "0-to-3-years-old" = 0-36m range = broader than "0-24m" that was blocked → this is a **RANGE_TOO_BROAD BYPASS**
  - **RESULT: AGE IS STILL WRONG in Phase 5d** — same issue from Phase 5 human review
  - Additionally, existing tag "newborn-clothing" on Shopify contradicts toddler/2-3y assignment
- **handle confirms:** "four-seasons" → no season tag (correct), "0-to-3-years-old" should block age

**P4 ANSWER: YES — age is STILL wrong in Phase 5d.** Handle contains "0-to-3-years-old" which should trigger RANGE_TOO_BROAD but did not. Confidence below threshold. Existing tag "newborn-clothing" also contradicts.

**VERDICT: REVIEW_ONLY**
**Reason:** Age still wrong (P4 confirmed). "0-to-3-years-old" in handle = RANGE_TOO_BROAD should have fired but didn't. Confidence 0.75 < 0.85 minimum. Inconsistency with how the validator handled similar range for other products.

---

### Candidate 8 — 9606764298553 | נעלי אופנה קז'ואל מונעות החלקה לתינוקות

| שדה | ערך |
|-----|-----|
| handle | childrens-sneakers-kids-fashion-design-white-non-slip-casual-shoes-for-boys-girls-little-kids |
| product_group | shoes_yaml |
| has_yaml | true |
| current_tags | baby-gift, baby-shoes, everyday-baby-wear, neutral-baby-outfit, newborn-clothing |
| proposed_tags | type-shoes, age-2-3y, season-unknown, occ-gift, occ-everyday, gender-neutral, style-casual |
| quality_score | 94.5 |

**Source Traces:**

| tag | source | confidence | rule |
|-----|--------|------------|------|
| type-shoes | existing_tag "baby-shoes" | 0.88 | tag_map |
| age-2-3y | handle | **0.75** | toddler_heuristic |
| season-unknown | category_default | 0.00 | fallback |
| occ-gift | existing_tag "baby-gift" | 0.88 | tag_map |
| gender-neutral | existing_tag "neutral-baby-outfit" | 0.88 | tag_map |
| style-casual | title | 0.80 | keyword |

**Evidence checks:**

- **type — CONFLICT:**
  - Proposed: type-shoes ← existing_tag "baby-shoes" (0.88)
  - Handle explicitly says: "childrens-**sneakers**-kids-fashion-design"
  - taxonomy-spec-v1 CAT-A: type-sneakers is an approved type (confidence_min 0.95, allowed_source: handle "baby-sneakers")
  - Handle "sneakers" is a direct keyword for type-sneakers
  - type-shoes vs type-sneakers conflict — existing_tag "baby-shoes" is generic, handle "sneakers" is specific
  - The more specific classification (type-sneakers) should have overridden the generic existing_tag
- **age:** age-2-3y ← toddler_heuristic, confidence **0.75 < 0.85 MINIMUM**
  - "little-kids" in handle may have triggered toddler_heuristic (indirect)
  - No "toddler" keyword explicitly visible in handle
  - Existing tag "newborn-clothing" also contradicts proposed age-2-3y
- **gender:** gender-neutral ← existing_tag "neutral-baby-outfit" ✅ — handle also has "boys-girls" supporting neutral
- **season:** season-unknown = reasonable for all-season shoes ✅

**VERDICT: REVIEW_ONLY**
**Reason:** Type conflict — handle says "sneakers" but type-shoes was assigned from generic existing tag. Age confidence 0.75 below 0.85 minimum. Age source unclear (no explicit "toddler" in handle). Existing tag "newborn-clothing" conflicts with proposed age.

---

### Candidate 9 — 9838580662585 | מצוף שחייה לתינוקות עם גגון וחגורות

| שדה | ערך |
|-----|-----|
| handle | baby-swimming-ring-with-canopy-inflatable-baby-float-swimming-pool-children-accessories |
| product_group | reborn_toys (classified incorrectly — swimming ring is not reborn/toy) |
| has_yaml | true |
| current_tags | (ריק — אין תגים) |
| proposed_tags | type-swimming-ring, season-summer, occ-beach, gender-unknown |
| quality_score | 80.2 |

**Source Traces:**

| tag | source | confidence | rule |
|-----|--------|------------|------|
| type-swimming-ring | title "מצוף שחייה" | **0.95** | keyword |
| season-summer | "title" (claimed) | 0.88 | keyword |
| occ-beach | type_default | 0.88 | type_inference |
| gender-unknown | category_default | 0.00 | fallback |

**Evidence checks:**

- **type:** type-swimming-ring ← title "מצוף שחייה" ✅ direct keyword, high confidence (0.95)
  - This is NOT a clothing/shoes item — age NOT required per Phase 5b rule
- **age exempt:** catb_exempt_reason = **"DOLL_NO_AGE_APPLICABLE"**
  - **WRONG LABEL** — a swimming ring is NOT a doll. This product has NO connection to reborn/dolls.
  - Correct exempt reason should be "NON_CLOTHING_SHOES_TYPE" or similar
  - Phase 5d report groups this in "reborn_toys" group (product_group) — also incorrect classification
  - The age exemption logic is CORRECT (swimming rings don't need age) but the REASON is wrong
  - This indicates the tagger's exempt logic relies on a flawed group classification (reborn_toys for a swimming ring)
- **season-summer:** src="title", rule=keyword, confidence 0.88
  - Hebrew title: "מצוף שחייה לתינוקות עם גגון וחגורות ורצועה" — does NOT contain "summer" or "קיץ"
  - Handle: "baby-swimming-ring-with-canopy-inflatable-baby-float-swimming-pool-children-accessories" — no "summer"
  - **SOURCE NOT VERIFIABLE** — source labeled "title" but no "summer" keyword in title or handle
  - Summer inference for a swimming ring may be semantically correct, but the G3 (SOURCE_TRACEABLE) gate is not satisfied
- **occ-beach:** type_inference from type-swimming-ring → occ-beach — this IS an approved inference per taxonomy-spec-v1 ("type-swimming-ring → occ-water-play/occ-beach") ✅
- **gender-unknown:** fallback — no source = correct (no existing tags, no gender signal) ✅
- **no existing tags:** this product has no current Shopify tags — higher-risk for Phase 6 (no baseline to compare against)
- **Phase 5d comparison note:** "remaining risk: medium confidence — review before live"

**VERDICT: REVIEW_ONLY**
**Reason:** Wrong catb_exempt label (DOLL_NO_AGE_APPLICABLE for a swimming ring — logic error in group classification). Season source not traceable (labeled "title" but Hebrew title doesn't contain "summer"). No existing tags. Medium confidence risk flag in Phase 5d output itself.

---

## 7. SAFE_FOR_PHASE6 LIST

**Total SAFE_FOR_PHASE6: 0**

No candidates qualified. Primary blockers across all 9:
1. Age confidence 0.75 below required 0.85 minimum (candidates 1, 3, 4, 5, 6, 7, 8)
2. Source label mismatches / G3 SOURCE_TRACEABLE failures (candidates 1, 2, 3, 5, 9)
3. Handle age conflicts requiring Shopify live verification (candidates 1, 2, 3, 6, 7)
4. Wrong gender tag (candidate 4 — REJECT)
5. Type conflict (candidate 8)
6. Wrong exempt label (candidate 9)

---

## 8. REVIEW_ONLY LIST

| # | product_id | title | blocking reason |
|---|---|---|---|
| 1 | 9688932909369 | אוברול אריה חמוד דגם שמר | age conf 0.75 < 0.85, handle conflict (toddler+infant) |
| 2 | 9874906349881 | אוברול ג'ינס מתוק דגם זוהר | season source mislabeled, handle age conflict (toddler+newborn) |
| 3 | 9688660312377 | אוברול ג׳ינס דגם אתי | age still wrong (P2), conf 0.75, handle conflict, source mislabeling |
| 5 | 9687579033913 | אוברול לבבות דגם הילה | age conf 0.75, season source not traceable, source label mismatches |
| 6 | 9615375565113 | נעל אלגנטית צעד ראשון לבנות | age still wrong (P3), existing "newborn-clothing" conflicts with age-6-12m |
| 7 | 9606764462393 | נעל קז'ואל במיוחד לתינוקות | age still wrong (P4), "0-to-3-years-old" RANGE_TOO_BROAD bypass |
| 8 | 9606764298553 | נעלי אופנה קז'ואל מונעות החלקה | type conflict (sneakers vs shoes), age conf 0.75, source unclear |
| 9 | 9838580662585 | מצוף שחייה לתינוקות | wrong catb_exempt label, season source not traceable |

---

## 9. REJECT LIST

| # | product_id | title | rejection reason |
|---|---|---|---|
| 4 | 9895864205625 | אוברול ג'ינס יוניסקס לתינוקות דגם שלו | G4 VIOLATION: gender-boy assigned from handle "boys" despite title explicitly declaring "יוניסקס" (unisex = gender-neutral). Higher-priority title source overridden by lower-priority handle source. Would push WRONG gender tag to Shopify. |

---

## 10. D1 STATUS — NO_AGE_FOUND for Real Clothing/Shoes

**D1: NO_AGE_FOUND — CONFIRMED AS REAL PROBLEM FOR CLOTHING/SHOES**

| עובדה | ערך |
|------|-----|
| Total NO_AGE_FOUND | 32 |
| Relevant (clothing/shoes only) | ~18 confirmed |
| Root cause | Age heuristic confidence 0.75 below 0.85 minimum threshold |
| All 5 clothing candidates | Have age-2-3y at 0.75 confidence — all below threshold |
| All 3 shoe candidates | Have age-2-3y or age-6-12m at 0.75 confidence — all below threshold |
| Effective result | 0 clothing/shoes candidates with verified age source |

**Classification: D1 = ACTIVE_PROBLEM — NOT RESOLVED**

Root cause is not missing age data — it is that the toddler_heuristic and first_walker_heuristic produce confidence 0.75, which is below the 0.85 minimum that the taxonomy spec requires for required tags.

---

## 11. D2 STATUS — RANGE_TOO_BROAD

**D2: PARTIALLY_RESOLVED BUT INCONSISTENT**

| עובדה | ערך |
|------|-----|
| Products correctly blocked (RANGE_TOO_BROAD) | 4 |
| Known bypass case | Candidate 7 (9606764462393): handle "0-to-3-years-old" (=36m range) was NOT blocked |
| Comparison: 10005779808569 | handle "0-24m" WAS blocked correctly |
| Inconsistency | "0-to-3-years-old" (=36m) was not treated as RANGE_TOO_BROAD while "0-24m" (=24m) was |

**Classification: D2 = INCONSISTENT — one bypass case found**

---

## 12. D4 STATUS — At Least 5 Truly Safe Candidates?

**D4: NO — 0 SAFE_FOR_PHASE6 candidates**

| criteria | result |
|---------|--------|
| Source trace clear | ❌ FAIL — source label mismatches across 8/9 candidates |
| No age conflict | ❌ FAIL — age below threshold in 7/9 candidates (clothing/shoes), P2/P3/P4 age still wrong |
| No gender without source | ❌ FAIL — candidate 4 gender-boy wrong (title says יוניסקס) |
| Type is approved | ✅ type tags themselves are approved values |
| No handle-only assumption | ❌ FAIL — all age tags come from handle-only heuristics at 0.75 |
| No malformed tag as source | ✅ PASS — 3-6M6-9M not used as source |
| No collection tag as type | ✅ PASS — collection-special-picks/collection-new-arrivals not in type position |
| No Shopify live required | ❌ FAIL — age conflicts on P3/P6 require live verification |

**D4 = PHASE6_NOT_READY — 0 candidates, minimum 5 required**

---

## 13. SPECIAL CHECKS — STATUS

| Special Check | Result |
|---------------|--------|
| P2 (candidate 3, 9688660312377) — age still wrong? | ✅ CONFIRMED: age-2-3y still at 0.75 confidence, handle still has "toddler+infant" conflict. Age is STILL WRONG. |
| P3 (candidate 6, 9615375565113) — age still wrong? | ✅ CONFIRMED: age-6-12m at 0.75 confidence, existing tag "newborn-clothing" still conflicts. Age is STILL WRONG. |
| P4 (candidate 7, 9606764462393) — age still wrong? | ✅ CONFIRMED: age-2-3y at 0.75 confidence, "0-to-3-years-old" in handle was not blocked. Age is STILL WRONG. |
| P14 (10005779808569) — gender-girl without source? | ⚠️ CONFIRMED PARTIAL: gender-girl IS proposed, source IS handle "girls" keyword (0.9). However, the handle says "boys-girls" — system extracted "girls" alone from "boys-girls" context, which points to gender-neutral not gender-girl. The source exists but the result is questionable. P14 is NOT in the 9 candidates (rejected with "other"). |
| Breathing elephant (9587715244345) — type-sleep-soother not type-reborn-doll? | ✅ CONFIRMED: Phase 5d corrected this to type-sleep-soother. is_reborn overridden to False. NOT in Phase 6 candidates (YAML_GAP + NO_AGE_FOUND exempted it). |
| collection-special-picks / collection-new-arrivals as type tags? | ✅ CLEAN: Neither appears as a type tag in any of the 9 candidates. |
| malformed tag 3-6M6-9M used as age source? | ✅ CLEAN: 3-6M6-9M exists on P14's Shopify tags but was NOT used as an age source for any candidate. Age for P14 was blocked via RANGE_TOO_BROAD. |

---

## 14. FINAL VERDICT

```
FINAL VERDICT: PHASE6_BLOCKED
```

**Reason:** 0 SAFE_FOR_PHASE6 candidates (minimum required: 5). Systematic issues prevent live batch.

### Root causes that must be fixed before Phase 5e rerun:

| Issue | Severity | Affects |
|-------|----------|---------|
| Age heuristic confidence 0.75 below 0.85 minimum | CRITICAL | 7/9 candidates |
| toddler_heuristic and first_walker_heuristic → should produce age-unknown when < 0.85 | CRITICAL | 7/9 |
| Handle conflict detection missing (toddler+infant, toddler+newborn = age-unknown) | CRITICAL | 3/9 |
| Gender source priority (title "יוניסקס" must override handle "boys") | CRITICAL | 1/9 REJECT |
| Source label mislabeling (season/fabric tagged as "title" when evidence is in "handle") | HIGH | 5/9 |
| RANGE_TOO_BROAD bypass ("0-to-3-years-old" should trigger like "0-24m") | HIGH | 1/9 |
| catb_exempt label wrong for non-clothing non-doll types (swimming ring → DOLL_NO_AGE) | MEDIUM | 1/9 |
| product_group "reborn_toys" for swimming ring = wrong group classification | MEDIUM | 1/9 |

---

## 15. NEXT RECOMMENDED ACTION

**< 5 SAFE candidates (0 found) → Phase 6 remains BLOCKED.**

Recommended Phase 5e fixes:

1. **Fix age confidence enforcement:** toddler_heuristic and first_walker_heuristic MUST produce age-unknown when confidence < 0.85. Do not add any age tag below the minimum threshold.

2. **Add handle conflict detection:** if handle contains BOTH "toddler" AND "infant", OR BOTH "toddler" AND "newborn" → result = age-unknown (conflicting sources).

3. **Fix RANGE_TOO_BROAD detection:** handle containing "0-to-3-years-old" or any "X-to-Y-years-old" pattern covering >18 months must trigger RANGE_TOO_BROAD blocking, same as "0-24m".

4. **Fix gender source priority:** title keyword "יוניסקס" or "unisex" MUST map to gender-neutral and MUST override handle "boys"/"girls" keywords. Source hierarchy: title > handle.

5. **Fix source label attribution:** when a keyword is found in the handle, record source="handle", not source="title". This must be consistent for all categories.

6. **Fix catb_exempt labeling:** type-swimming-ring and other non-clothing non-doll types must receive a correct exempt label (e.g., NON_CLOTHING_SHOES_TYPE), not "DOLL_NO_AGE_APPLICABLE".

7. **Fix product_group classification:** swimming ring must NOT be in the "reborn_toys" group.

8. **After fixes:** Run Phase 5e (a new logic-corrected dry-run) before reconsidering Phase 6.

**Do NOT open Phase 6 until a new dry-run produces ≥5 SAFE_FOR_PHASE6 candidates.**

---

## SUMMARY

| metric | value |
|--------|-------|
| Report path | output/tags/phase5e-candidate-safety-audit.md |
| Final verdict | **PHASE6_BLOCKED** |
| SAFE_FOR_PHASE6 | **0** |
| REVIEW_ONLY | **8** |
| REJECT | **1** (candidate 4 — gender-boy overrides title יוניסקס) |
| Phase 6 remains blocked | **YES** |
| Shopify live | NO — unchanged |
| Commit | NO |
| Push | NO |

---

*Phase 5e — AUDIT ONLY. אין שינויים בשופיפיי. אין commit. אין push.*
