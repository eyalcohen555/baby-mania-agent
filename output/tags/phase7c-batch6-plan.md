# Phase 7C Batch 6 — Read-Only Tagging Plan

## MODE
READ-ONLY PLANNING. No Shopify writes.

**Timestamp:** 2026-05-06T05:59:21.669834+00:00  
**Shopify writes:** NONE — GET only  

---

## 1. Selection Summary

| Item | Count |
|------|-------|
| Active products fetched | 393 |
| Already written Batch 1/2/3/4/5 (excluded) | 87 |
| Selected SAFE candidates | **20** |
| Need Hebrew month normalization | 0 |
| Safety flags | 0 ✅ |

### Type Breakdown

| Type | Count |
|------|-------|
| `type-set` | 16 |
| `type-dress` | 4 |
| `type-romper` | 0 |
| `type-bodysuit` | 0 |

---

## 2. Excluded / Blocked

- Already written in Batch 1/2/3/4/5 (explicit PID exclusion): excluded
- Already tagged with `type-*` in Shopify: excluded
- Shoe/sandal/sneaker title keyword: excluded
- False-positive keyword (מגבת/תיק/שמיכה/towel/bag/blanket/swimwear): excluded
- Low confidence (< type min_conf): excluded
- Non-preferred types (hat/coat/pants/top/swimwear): excluded
- REVIEW_ONLY: excluded (not in SAFE pool)

---

## 3. Per-Product Evidence

### [01] `9606694011193` — שמלת קיץ מיוחדת לבנות

| Field | Value |
|-------|-------|
| product_id | `9606694011193` |
| title | שמלת קיץ מיוחדת לבנות |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-dress`, `baby-gift`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing`, `summer-baby-wear` |
| proposed_new_tags | `type-dress`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `baby-dress`, `baby-gift`, `gender-girl`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing`, `occ-seasonal`, `summer-baby-wear...` |
| proposed_type | `type-dress` |
| type_source | handle |
| type_keyword | `dress` |
| type_conf | 0.90 |
| proposed_gender | `gender-girl` |
| gender_source | title |
| gender_keyword | `בנות` |
| gender_conf | 0.90 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'dress' in handle (conf=0.90); gender matched 'בנות' in title (conf=0.90); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.90 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.90, kw='dress', gender-source=title, kw='בנות', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [02] `9895864402233` — שמלת קיץ פרחונית לתינוקות דגם אלין

| Field | Value |
|-------|-------|
| product_id | `9895864402233` |
| title | שמלת קיץ פרחונית לתינוקות דגם אלין |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-dress`, `baby-gift`, `floral-baby`, `newborn-clothing`, `summer-baby-wear` |
| proposed_new_tags | `type-dress`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `baby-dress`, `baby-gift`, `floral-baby`, `gender-girl`, `newborn-clothing`, `occ-seasonal`, `summer-baby-wear`, `type-dress` |
| proposed_type | `type-dress` |
| type_source | handle |
| type_keyword | `dress` |
| type_conf | 0.90 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'dress' in handle (conf=0.90); gender matched 'girl' in handle (conf=0.90); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.90 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.90, kw='dress', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [03] `9605887590713` — שמלת שמש לתינוקות וילדות

| Field | Value |
|-------|-------|
| product_id | `9605887590713` |
| title | שמלת שמש לתינוקות וילדות |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-dress`, `baby-gift`, `cotton-baby`, `everyday-baby-wear`, `kids-clothing`, `neutral-baby-outfit` |
| proposed_new_tags | `type-dress`, `gender-girl` |
| final_tags_after_merge | `baby-dress`, `baby-gift`, `cotton-baby`, `everyday-baby-wear`, `gender-girl`, `kids-clothing`, `neutral-baby-outfit`, `type-dress` |
| proposed_type | `type-dress` |
| type_source | handle |
| type_keyword | `dress` |
| type_conf | 0.90 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'dress' in handle (conf=0.90); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.90 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.90, kw='dress', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [04] `9892620960057` — שמלת תחרה כפלים דגם טליה

| Field | Value |
|-------|-------|
| product_id | `9892620960057` |
| title | שמלת תחרה כפלים דגם טליה |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-dress`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-dress` |
| proposed_type | `type-dress` |
| type_source | handle |
| type_keyword | `dress` |
| type_conf | 0.90 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'dress' in handle (conf=0.90); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.90 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.90, kw='dress', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [05] `9096607400249` — חליפת דוב  סוודר כותנה  - דגם דנה

| Field | Value |
|-------|-------|
| product_id | `9096607400249` |
| title | חליפת דוב  סוודר כותנה  - דגם דנה |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-suit`, `bear-print-baby`, `cotton-baby`, `everyday-baby-wear`, `newborn-clothing` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `bear-print-baby`, `cotton-baby`, `everyday-baby-wear`, `newborn-clothing`, `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [06] `9096606810425` — חליפת דוב  סוודר כותנה  - דגם רותם

| Field | Value |
|-------|-------|
| product_id | `9096606810425` |
| title | חליפת דוב  סוודר כותנה  - דגם רותם |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-suit`, `bear-print-baby`, `cotton-baby`, `everyday-baby-wear`, `newborn-clothing` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `bear-print-baby`, `cotton-baby`, `everyday-baby-wear`, `newborn-clothing`, `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [07] `9688965022009` — חליפת דובי דגם נתן

| Field | Value |
|-------|-------|
| product_id | `9688965022009` |
| title | חליפת דובי דגם נתן |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-suit`, `bear-print-baby`, `everyday-baby-wear`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-boy` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `bear-print-baby`, `everyday-baby-wear`, `gender-boy`, `newborn-clothing`, `type-set` |
| proposed_type | `type-set` |
| type_source | handle |
| type_keyword | `set` |
| type_conf | 0.88 |
| proposed_gender | `gender-boy` |
| gender_source | handle |
| gender_keyword | `boy` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'set' in handle (conf=0.88); gender matched 'boy' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [08] `9096606974265` — חליפת וופל במגוון צבעים

| Field | Value |
|-------|-------|
| product_id | `9096606974265` |
| title | חליפת וופל במגוון צבעים |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing`, `waffle-knit` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing`, `type-set`, `waffle-knit` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [09] `10005779710265` — חליפת חורף לתינוקת עם כובע דגם שון

| Field | Value |
|-------|-------|
| product_id | `10005779710265` |
| title | חליפת חורף לתינוקת עם כובע דגם שון |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-suit`, `cotton-baby`, `neutral-baby-outfit`, `newborn-clothing`, `winter-baby-wear` |
| proposed_new_tags | `type-set`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `cotton-baby`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `occ-seasonal`, `type-set...` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'חליפת' in title (conf=0.88); gender matched 'girl' in handle (conf=0.90); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [10] `9179167654201` — חליפת חצאית תחרה אלגנטית - קארין

| Field | Value |
|-------|-------|
| product_id | `9179167654201` |
| title | חליפת חצאית תחרה אלגנטית - קארין |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [11] `9179170799929` — חליפת טטרה קיצית מכותנה - עידודו

| Field | Value |
|-------|-------|
| product_id | `9179170799929` |
| title | חליפת טטרה קיצית מכותנה - עידודו |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [12] `9606691356985` — חליפת טניס קיצית לבנות

| Field | Value |
|-------|-------|
| product_id | `9606691356985` |
| title | חליפת טניס קיצית לבנות |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-suit`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing`, `summer-baby-wear` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `gender-girl`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing`, `summer-baby-wear`, `type-set` |
| proposed_type | `type-set` |
| type_source | handle |
| type_keyword | `set` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | title |
| gender_keyword | `בנות` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'set' in handle (conf=0.88); gender matched 'בנות' in title (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=title, kw='בנות', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [13] `9179157725497` — חליפת כותנה אורגנית - בילי

| Field | Value |
|-------|-------|
| product_id | `9179157725497` |
| title | חליפת כותנה אורגנית - בילי |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [14] `9179133870393` — חליפת כותנה וופל בשילוב דובי - בנים, בנות

| Field | Value |
|-------|-------|
| product_id | `9179133870393` |
| title | חליפת כותנה וופל בשילוב דובי - בנים, בנות |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | title |
| gender_keyword | `בנות` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88); gender matched 'בנות' in title (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', gender-source=title, kw='בנות', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [15] `9179158839609` — חליפת כותנה ופשתן - בייבילו

| Field | Value |
|-------|-------|
| product_id | `9179158839609` |
| title | חליפת כותנה ופשתן - בייבילו |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [16] `9179164705081` — חליפת כותנה משובצת - נטע

| Field | Value |
|-------|-------|
| product_id | `9179164705081` |
| title | חליפת כותנה משובצת - נטע |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [17] `9179166376249` — חליפת כותנה סרוגה בייסיק - אדריאן

| Field | Value |
|-------|-------|
| product_id | `9179166376249` |
| title | חליפת כותנה סרוגה בייסיק - אדריאן |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [18] `9179148190009` — חליפת כותנה קז'ואל - מאורי

| Field | Value |
|-------|-------|
| product_id | `9179148190009` |
| title | חליפת כותנה קז'ואל - מאורי |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [19] `9179168473401` — חליפת מלמלות טטרה- אלכסה

| Field | Value |
|-------|-------|
| product_id | `9179168473401` |
| title | חליפת מלמלות טטרה- אלכסה |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

### [20] `9179170144569` — חליפת מלמלות מכותנה ופשתן - מיילי

| Field | Value |
|-------|-------|
| product_id | `9179170144569` |
| title | חליפת מלמלות מכותנה ופשתן - מיילי |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345_check: ✅ PASS

---

## 4. Batch-Level Safety Summary

| Check | Result |
|-------|--------|
| No age-* tags | ✅ PASS |
| No type collision | ✅ PASS |
| No gender collision | ✅ PASS |
| No forbidden tags | ✅ PASS |
| No shoe title leak | ✅ PASS |
| No Shopify writes | ✅ PASS — GET only |
| Not in Batch 1/2/3/4/5 | ✅ PASS |
| All tags in ALLOWED_VALUES | ✅ PASS |
| Hebrew month norm flagged | 0 product(s) need normalization in live stage |

---

## 5. Required Gates for Live Batch

Before any live write, each product must pass:
1. backup before write
2. dry run verification
3. forbidden tag check
4. age-* check
5. RANGE_TOO_BROAD check
6. type collision check
7. gender collision check
8. false-positive keyword check
9. Hebrew month normalization (X חודש → X חודשים) if needed
10. Shopify PUT only after T3 approval
11. Shopify GET verify
12. post-verify independent check
13. rollback plan on file
14. report
15. explicit git add only (no git add -A)

---

## 6. Verdict

**READY_FOR_PHASE7C_BATCH6_T3_APPROVAL**

✅ 20 SAFE candidates selected.
All safety checks PASS. No age-* tags. No type collision. No forbidden tags.
No overlap with Batch 1/2/3/4/5 written products. 0 product(s) need Hebrew month normalization in live stage.
Next step: request T3 approval from Ayal → Phase 7C Batch 6 live.

---

*Generated by scripts/phase7c_batch6_plan.py*