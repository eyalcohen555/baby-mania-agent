# Layer 6 — Phase 3b Taxonomy & Source Normalization Report

**Date:** 2026-05-03  
**Input:** Phase 2b sample (30 products)  
**Normalization rules applied:** gender-unisex, type-doll, type-other, occ-sport/holiday, style-cartoon

---

## 1. Before / After Comparison

| Gate | Fail BEFORE (Phase 3) | Fail AFTER (Phase 3b) | Delta |
|---|---|---|---|
| SOURCE_EXISTS | 0 | 0 | 0 |
| FORMAT_VALID | 0 | 0 | 0 |
| ALLOWED_VALUE | 24 | 0 | -24 |
| SOURCE_TRACEABLE | 6 | 0 | -6 |
| NO_FORBIDDEN_INFERENCE | 0 | 0 | 0 |
| CATEGORY_COVERAGE | 17 | 17 | 0 |
| DUPLICATE_CONFLICT | 1 | 1 | 0 |
| QUALITY_SCORE | 12 | 13 | +1 |

| **Overall PASS** | **3/30** | **12/30** | **+9** |

---

## 2. Taxonomy Gaps — Before / After

| Tag | Before | After | Action |
|---|---|---|---|
| `gender-unisex` | 18 | 0 | explicit src->gender-neutral; deprecated src->gender-unknown |
| `occ-holiday` | 1 | 0 | ->BLOCKED (TAXONOMY_GAP, no approved equivalent) |
| `occ-sport` | 2 | 0 | ->BLOCKED (TAXONOMY_GAP, no approved equivalent) |
| `style-cartoon` | 1 | 0 | ->BLOCKED (TAXONOMY_GAP, no approved equivalent) |
| `type-doll` | 5 | 0 | reborn context->type-reborn-doll; no reborn->type-toy |
| `type-other` | 2 | 0 | ->type-unknown (src=category_default) |

---

## 3. Normalization Conditions Check

| Condition | Status |
|---|---|
| gender-unisex removed from proposed_tags | YES |
| gender-neutral assigned only with explicit source | YES |
| type-doll removed from proposed_tags | YES |
| type-reborn-doll only with reborn context | YES |
| style-cartoon blocked (TAXONOMY_GAP) | YES |
| default_unisex source eliminated | YES |
| fallback source eliminated | YES |
| negative tests still 10/10 blocked | YES |
| Shopify live changes | 0 |
| Phase 4 NOT opened | YES |

---

## 4. Normalization Log — Products Changed

| Product ID | Title | Changes |
|---|---|---|
| `10029649002809` | Alure™ Baby | gender-unisex->gender-neutral (src=title) |
| `10029649133881` | Lino™ – סט סריג רך לתינוקות בעיצוב אירופ | gender-unisex->gender-neutral (src=existing_tag) |
| `10029648970041` | LumiBear™ חליפת פרמיום לחורף | gender-unisex->gender-neutral (src=existing_tag) |
| `10029649101113` | LUMI™  – אוברול נוחות יוקרתי לתינוקות | gender-unisex->gender-neutral (src=title) |
| `9657091293497` | WarmNest™– אוברול חורף מחבק לתינוקות | gender-unisex->gender-neutral (src=title); style-cartoon->BLOCKED (TAXONOMY_GAP) |
| `9179155693881` | אוברול אלגנט דגם עומרי | gender-unisex->gender-unknown (deprecated src='default_unisex') |
| `9096606908729` | אוברול ארוך | gender-unisex->gender-neutral (src=existing_tag) |
| `9096599994681` | אוברול ארוך עם רוכסן | gender-unisex->gender-neutral (src=existing_tag) |
| `9615669461305` | מגפי חורף נוצצים עם כוכבים | gender-unisex->gender-neutral (src=existing_tag) |
| `9615375794489` | מגפי חורף צעד ראשון | gender-unisex->gender-neutral (src=existing_tag) |
| `9607365132601` | נעל אולסטאר צעד ראשון לתינוק | gender-unisex->gender-neutral (src=existing_tag) |
| `9607363756345` | נעל אופנתית אלגנטית לתינוק | gender-unisex->gender-neutral (src=title) |
| `9615376023865` | נעל חורף מחממת ואלגנטית צעד ראשון | gender-unisex->gender-unknown (deprecated src='default_unisex') |
| `9615376089401` | נעל חורף צעד ראשון אופנתיות | gender-unisex->gender-neutral (src=existing_tag) |
| `9607363461433` | נעל ספורט קז'ואל נוחה לתינוק | gender-unisex->gender-neutral (src=title) |
| `10190522810681` | 46CM Finished Reborn Baby Doll Felicia N | type-doll->type-reborn-doll; occ-sport->BLOCKED (TAXONOMY_GAP); gender-unisex->gender-unknown (deprecated src='default_unisex') |
| `10190523040057` | 50CM  Whole Silicone Vinyl Reborn Doll 2 | occ-holiday->BLOCKED (TAXONOMY_GAP) |
| `10190522777913` | NPK 46CM Meadow Reborn Baby Doll - Soft  | type-doll->type-reborn-doll; gender-unisex->gender-unknown (deprecated src='default_unisex') |
| `10190523072825` | NPK 50CM Full Body Maddie Reborn Baby Gi | type-doll->type-reborn-doll |
| `10190523007289` | Open Mouth 33cm Pascale Full Body Silico | type-doll->type-reborn-doll |
| `10190522941753` | 2Pcs Baby Boys' Sports and Leisure Set l | occ-sport->BLOCKED (TAXONOMY_GAP) |
| `9166992900409` | BABY MANIA™  בובה  נושמת מבית | type-doll->type-toy (no reborn context) |
| `9839001633081` | Babyfree100 | type-other->type-unknown (deprecated src='fallback'); gender-unisex->gender-unknown (deprecated src='default_unisex') |
| `9839252472121` | BabySleep Pro – רעש לבן ואור מרגיע לשינה | type-other->type-unknown (deprecated src='fallback') |

---

## 5. Per-Product Detail — After Normalization

**10029649002809** — Alure™ Baby — `PASS`
  - Normalization: gender-unisex->gender-neutral (src=title)

**10029649133881** — Lino™ – סט סריג רך לתינוקות בעיצוב אירופאי — `PASS`
  - Normalization: gender-unisex->gender-neutral (src=existing_tag)

**10029648970041** — LumiBear™ חליפת פרמיום לחורף — `PASS`
  - Normalization: gender-unisex->gender-neutral (src=existing_tag)

**10029649101113** — LUMI™  – אוברול נוחות יוקרתי לתינוקות — `PASS`
  - Normalization: gender-unisex->gender-neutral (src=title)

**9855017550137** — Veloura Baby™ חליפה פרחונית — `PASS`

**9657091293497** — WarmNest™– אוברול חורף מחבק לתינוקות — `FAIL`
  - Failed gates: DUPLICATE_CONFLICT
  - Normalization: gender-unisex->gender-neutral (src=title); style-cartoon->BLOCKED (TAXONOMY_GAP)

**9687596728633** — אוברול Leopard Cozy — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE

**9179155693881** — אוברול אלגנט דגם עומרי — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE
  - Normalization: gender-unisex->gender-unknown (deprecated src='default_unisex')

**9096606908729** — אוברול ארוך — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE
  - Normalization: gender-unisex->gender-neutral (src=existing_tag)

**9096599994681** — אוברול ארוך עם רוכסן — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE
  - Normalization: gender-unisex->gender-neutral (src=existing_tag)

**9607363625273** — מגפי חורף לילדות דגם לין — `PASS`

**9615669461305** — מגפי חורף נוצצים עם כוכבים — `PASS`
  - Normalization: gender-unisex->gender-neutral (src=existing_tag)

**9615375794489** — מגפי חורף צעד ראשון — `PASS`
  - Normalization: gender-unisex->gender-neutral (src=existing_tag)

**9607365132601** — נעל אולסטאר צעד ראשון לתינוק — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE
  - Normalization: gender-unisex->gender-neutral (src=existing_tag)

**9607363756345** — נעל אופנתית אלגנטית לתינוק — `FAIL`
  - Failed gates: CATEGORY_COVERAGE
  - Normalization: gender-unisex->gender-neutral (src=title)

**9615375565113** — נעל אלגנטית צעד ראשון לבנות — `FAIL`
  - Failed gates: CATEGORY_COVERAGE

**9607363232057** — נעל הלו קיטי עם אורות לילדות — `FAIL`
  - Failed gates: CATEGORY_COVERAGE

**9615376023865** — נעל חורף מחממת ואלגנטית צעד ראשון — `PASS`
  - Normalization: gender-unisex->gender-unknown (deprecated src='default_unisex')

**9615376089401** — נעל חורף צעד ראשון אופנתיות — `PASS`
  - Normalization: gender-unisex->gender-neutral (src=existing_tag)

**9607363461433** — נעל ספורט קז'ואל נוחה לתינוק — `FAIL`
  - Failed gates: CATEGORY_COVERAGE
  - Normalization: gender-unisex->gender-neutral (src=title)

**10190522810681** — 46CM Finished Reborn Baby Doll Felicia Newborn Ope... — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE
  - Normalization: type-doll->type-reborn-doll; occ-sport->BLOCKED (TAXONOMY_GAP); gender-unisex->gender-unknown (deprecated src='default_unisex')

**10190523040057** — 50CM  Whole Silicone Vinyl Reborn Doll 20 Inch Gir... — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE
  - Normalization: occ-holiday->BLOCKED (TAXONOMY_GAP)

**10190522777913** — NPK 46CM Meadow Reborn Baby Doll - Soft Touch 3D S... — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE
  - Normalization: type-doll->type-reborn-doll; gender-unisex->gender-unknown (deprecated src='default_unisex')

**10190523072825** — NPK 50CM Full Body Maddie Reborn Baby Girl Doll - ... — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE
  - Normalization: type-doll->type-reborn-doll

**10190523007289** — Open Mouth 33cm Pascale Full Body Silicone Reborn ... — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE
  - Normalization: type-doll->type-reborn-doll

**10190523334969** — 0-18 Months old Newborn Baby boy Jumpsuit Cute Lit... — `PASS`

**10190522941753** — 2Pcs Baby Boys' Sports and Leisure Set lapel Color... — `PASS`
  - Normalization: occ-sport->BLOCKED (TAXONOMY_GAP)

**9166992900409** — BABY MANIA™  בובה  נושמת מבית — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE
  - Normalization: type-doll->type-toy (no reborn context)

**9839001633081** — Babyfree100 — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE
  - Normalization: type-other->type-unknown (deprecated src='fallback'); gender-unisex->gender-unknown (deprecated src='default_unisex')

**9839252472121** — BabySleep Pro – רעש לבן ואור מרגיע לשינה עמוקה לתי... — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE
  - Normalization: type-other->type-unknown (deprecated src='fallback')

---

## 6. Negative Test Cases — Still Blocked

| ID | Expected Failures | Actual Failures | Verified |
|---|---|---|---|
| TC01 | SOURCE_EXISTS | SOURCE_EXISTS, SOURCE_TRACEABLE | YES |
| TC02 | ALLOWED_VALUE, FORMAT_VALID | ALLOWED_VALUE, FORMAT_VALID | YES |
| TC03 | ALLOWED_VALUE | ALLOWED_VALUE | YES |
| TC04 | SOURCE_TRACEABLE | SOURCE_TRACEABLE | YES |
| TC05 | NO_FORBIDDEN_INFERENCE | NO_FORBIDDEN_INFERENCE | YES |
| TC06 | CATEGORY_COVERAGE, QUALITY_SCORE | CATEGORY_COVERAGE, QUALITY_SCORE | YES |
| TC07 | DUPLICATE_CONFLICT | DUPLICATE_CONFLICT | YES |
| TC08 | QUALITY_SCORE | CATEGORY_COVERAGE, QUALITY_SCORE | YES |
| TC09 | ALLOWED_VALUE | ALLOWED_VALUE | YES |
| TC10 | ALLOWED_VALUE | ALLOWED_VALUE | YES |

---

## 7. Remaining Open Decisions (not fixed by Phase 3b)

| # | Issue | Count | Decision Needed |
|---|---|---|---|
| 1 | RANGE_TOO_BROAD (CAT-B blocked) | 9 | Manual age split or range strategy |
| 2 | NO_AGE_FOUND | 9 | Product enrichment or age-unknown fallback |
| 3 | DUPLICATE_CONFLICT (multi-age WarmNest) | 1 | Decide if CAT-B can be multi-value |

_Phase 4 Dry Run may proceed after Ayal review of this report._
