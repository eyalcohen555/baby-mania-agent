# Layer 6 — Phase 3 Validation Gates Report

**Date:** 2026-05-03  
**Gates:** SOURCE_EXISTS, FORMAT_VALID, ALLOWED_VALUE, SOURCE_TRACEABLE, NO_FORBIDDEN_INFERENCE, CATEGORY_COVERAGE, DUPLICATE_CONFLICT, QUALITY_SCORE

---

## 1. Positive Sample (30 products from Phase 2b)

| Metric | Value |
|---|---|
| Total products | 30 |
| Overall PASS (all 8 gates) | **3** |
| Overall FAIL (any gate) | **27** |

### Gate Results — Positive Sample

| Gate | PASS | FAIL |
|---|---|---|
| SOURCE_EXISTS | 30 | 0 |
| FORMAT_VALID | 30 | 0 |
| ALLOWED_VALUE | 6 | 24 |
| SOURCE_TRACEABLE | 24 | 6 |
| NO_FORBIDDEN_INFERENCE | 30 | 0 |
| CATEGORY_COVERAGE | 13 | 17 |
| DUPLICATE_CONFLICT | 29 | 1 |
| QUALITY_SCORE | 18 | 12 |

### Taxonomy Gaps Found — Positive Sample

| Tag | Count | Note |
|---|---|---|
| `gender-unisex` | 18 | spec uses gender-neutral |
| `occ-holiday` | 1 | not in taxonomy spec |
| `occ-sport` | 2 | not in taxonomy spec |
| `style-cartoon` | 1 | not in taxonomy spec |
| `type-doll` | 5 |  |
| `type-other` | 2 | spec uses type-unknown |

---

## 2. Negative Test Cases (10 synthetic failure scenarios)

| Metric | Value |
|---|---|
| Total test cases | 10 |
| Verification passed (all expected gates fired) | **10/10** |
| All verified | YES |

### Gate Results — Negative Tests

| Gate | PASS | FAIL |
|---|---|---|
| SOURCE_EXISTS | 9 | 1 |
| FORMAT_VALID | 9 | 1 |
| ALLOWED_VALUE | 6 | 4 |
| SOURCE_TRACEABLE | 8 | 2 |
| NO_FORBIDDEN_INFERENCE | 9 | 1 |
| CATEGORY_COVERAGE | 8 | 2 |
| DUPLICATE_CONFLICT | 9 | 1 |
| QUALITY_SCORE | 8 | 2 |

### Negative Test Verification Detail

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

## 3. Per-Product Detail — Positive Sample

**10029649002809** — Alure™ Baby — `FAIL`
  - Failed gates: ALLOWED_VALUE
  - Taxonomy gaps: gender-unisex

**10029649133881** — Lino™ – סט סריג רך לתינוקות בעיצוב אירופאי — `FAIL`
  - Failed gates: ALLOWED_VALUE
  - Taxonomy gaps: gender-unisex

**10029648970041** — LumiBear™ חליפת פרמיום לחורף — `FAIL`
  - Failed gates: ALLOWED_VALUE
  - Taxonomy gaps: gender-unisex

**10029649101113** — LUMI™  – אוברול נוחות יוקרתי לתינוקות — `FAIL`
  - Failed gates: ALLOWED_VALUE
  - Taxonomy gaps: gender-unisex

**9855017550137** — Veloura Baby™ חליפה פרחונית — `PASS`

**9657091293497** — WarmNest™– אוברול חורף מחבק לתינוקות — `FAIL`
  - Failed gates: ALLOWED_VALUE, DUPLICATE_CONFLICT
  - Taxonomy gaps: gender-unisex, style-cartoon

**9687596728633** — אוברול Leopard Cozy — `FAIL`
  - Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE

**9179155693881** — אוברול אלגנט דגם עומרי — `FAIL`
  - Failed gates: ALLOWED_VALUE, SOURCE_TRACEABLE, CATEGORY_COVERAGE, QUALITY_SCORE
  - Taxonomy gaps: gender-unisex

**9096606908729** — אוברול ארוך — `FAIL`
  - Failed gates: ALLOWED_VALUE, CATEGORY_COVERAGE, QUALITY_SCORE
  - Taxonomy gaps: gender-unisex

**9096599994681** — אוברול ארוך עם רוכסן — `FAIL`
  - Failed gates: ALLOWED_VALUE, CATEGORY_COVERAGE, QUALITY_SCORE
  - Taxonomy gaps: gender-unisex

**9607363625273** — מגפי חורף לילדות דגם לין — `PASS`

**9615669461305** — מגפי חורף נוצצים עם כוכבים — `FAIL`
  - Failed gates: ALLOWED_VALUE
  - Taxonomy gaps: gender-unisex

**9615375794489** — מגפי חורף צעד ראשון — `FAIL`
  - Failed gates: ALLOWED_VALUE
  - Taxonomy gaps: gender-unisex

**9607365132601** — נעל אולסטאר צעד ראשון לתינוק — `FAIL`
  - Failed gates: ALLOWED_VALUE, CATEGORY_COVERAGE, QUALITY_SCORE
  - Taxonomy gaps: gender-unisex

**9607363756345** — נעל אופנתית אלגנטית לתינוק — `FAIL`
  - Failed gates: ALLOWED_VALUE, CATEGORY_COVERAGE
  - Taxonomy gaps: gender-unisex

**9615375565113** — נעל אלגנטית צעד ראשון לבנות — `FAIL`
  - Failed gates: CATEGORY_COVERAGE

**9607363232057** — נעל הלו קיטי עם אורות לילדות — `FAIL`
  - Failed gates: CATEGORY_COVERAGE

**9615376023865** — נעל חורף מחממת ואלגנטית צעד ראשון — `FAIL`
  - Failed gates: ALLOWED_VALUE, SOURCE_TRACEABLE
  - Taxonomy gaps: gender-unisex

**9615376089401** — נעל חורף צעד ראשון אופנתיות — `FAIL`
  - Failed gates: ALLOWED_VALUE
  - Taxonomy gaps: gender-unisex

**9607363461433** — נעל ספורט קז'ואל נוחה לתינוק — `FAIL`
  - Failed gates: ALLOWED_VALUE, CATEGORY_COVERAGE
  - Taxonomy gaps: gender-unisex

**10190522810681** — 46CM Finished Reborn Baby Doll Felicia Newborn Ope... — `FAIL`
  - Failed gates: ALLOWED_VALUE, SOURCE_TRACEABLE, CATEGORY_COVERAGE, QUALITY_SCORE
  - Taxonomy gaps: type-doll, occ-sport, gender-unisex

**10190523040057** — 50CM  Whole Silicone Vinyl Reborn Doll 20 Inch Gir... — `FAIL`
  - Failed gates: ALLOWED_VALUE, CATEGORY_COVERAGE
  - Taxonomy gaps: occ-holiday

**10190522777913** — NPK 46CM Meadow Reborn Baby Doll - Soft Touch 3D S... — `FAIL`
  - Failed gates: ALLOWED_VALUE, SOURCE_TRACEABLE, CATEGORY_COVERAGE, QUALITY_SCORE
  - Taxonomy gaps: type-doll, gender-unisex

**10190523072825** — NPK 50CM Full Body Maddie Reborn Baby Girl Doll - ... — `FAIL`
  - Failed gates: ALLOWED_VALUE, CATEGORY_COVERAGE, QUALITY_SCORE
  - Taxonomy gaps: type-doll

**10190523007289** — Open Mouth 33cm Pascale Full Body Silicone Reborn ... — `FAIL`
  - Failed gates: ALLOWED_VALUE, CATEGORY_COVERAGE, QUALITY_SCORE
  - Taxonomy gaps: type-doll

**10190523334969** — 0-18 Months old Newborn Baby boy Jumpsuit Cute Lit... — `PASS`

**10190522941753** — 2Pcs Baby Boys' Sports and Leisure Set lapel Color... — `FAIL`
  - Failed gates: ALLOWED_VALUE
  - Taxonomy gaps: occ-sport

**9166992900409** — BABY MANIA™  בובה  נושמת מבית — `FAIL`
  - Failed gates: ALLOWED_VALUE, CATEGORY_COVERAGE, QUALITY_SCORE
  - Taxonomy gaps: type-doll

**9839001633081** — Babyfree100 — `FAIL`
  - Failed gates: ALLOWED_VALUE, SOURCE_TRACEABLE, CATEGORY_COVERAGE, QUALITY_SCORE
  - Taxonomy gaps: type-other, gender-unisex

**9839252472121** — BabySleep Pro – רעש לבן ואור מרגיע לשינה עמוקה לתי... — `FAIL`
  - Failed gates: ALLOWED_VALUE, SOURCE_TRACEABLE, CATEGORY_COVERAGE, QUALITY_SCORE
  - Taxonomy gaps: type-other

---

## 4. Open Decisions

| # | Issue | Count | Decision Needed |
|---|---|---|---|
| 1 | RANGE_TOO_BROAD products (CAT-B blocked) | 9 | Manual age split or range-tag strategy |
| 2 | NO_AGE_FOUND products | 9 | Product enrichment or age-unknown fallback |
| 3 | TAXONOMY_GAP tags (positive sample) | 6 unique | Migrate to valid values or extend spec |

_Phase 4 Dry Run is gated on reviewing these open decisions._
