# Phase 7C Batch 7 — Read-Only Tagging Plan

## MODE
READ-ONLY PLANNING. No Shopify writes.

**Timestamp:** 2026-05-06T08:06:22.981905+00:00  
**Shopify writes:** NONE — GET only  

---

## 1. Selection Summary

| Item | Count |
|------|-------|
| Active products fetched | 393 |
| Already written Batch 1/2/3/4/5/6 (excluded) | 107 |
| Selected SAFE candidates | **20** |
| Need Hebrew month normalization | 1 |
| Safety flags | 0 ✅ |

### Type Breakdown

| Type | Count |
|------|-------|
| `type-set` | 20 |
| `type-dress` | 0 |
| `type-romper` | 0 |
| `type-bodysuit` | 0 |

---

## 2. Excluded / Blocked

- Already written in Batch 1/2/3/4/5/6 (explicit PID exclusion): excluded
- Already tagged with `type-*` in Shopify: excluded
- Shoe/sandal/sneaker title keyword: excluded
- False-positive keyword (מגבת/תיק/שמיכה/towel/bag/blanket/swimwear): excluded
- Low confidence (< type min_conf): excluded
- Non-preferred types (hat/coat/pants/top/swimwear): excluded
- REVIEW_ONLY: excluded (not in SAFE pool)

---

## 3. Per-Product Evidence

### [01] `9688935039289` — חליפת מתוקה הדפס אריהדגם שמר

| Field | Value |
|-------|-------|
| product_id | `9688935039289` |
| title | חליפת מתוקה הדפס אריהדגם שמר |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-boy` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `gender-boy`, `neutral-baby-outfit`, `newborn-clothing`, `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `gender-boy` |
| gender_source | handle |
| gender_keyword | `boy` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88); gender matched 'boy' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [02] `9606694273337` — חליפת ספורט-אלגנט לילד

| Field | Value |
|-------|-------|
| product_id | `9606694273337` |
| title | חליפת ספורט-אלגנט לילד |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `kids-clothing`, `sporty-baby` |
| proposed_new_tags | `type-set`, `gender-boy` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `gender-boy`, `kids-clothing`, `sporty-baby`, `type-set` |
| proposed_type | `type-set` |
| type_source | handle |
| type_keyword | `set` |
| type_conf | 0.88 |
| proposed_gender | `gender-boy` |
| gender_source | title |
| gender_keyword | `ילד` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'set' in handle (conf=0.88); gender matched 'ילד' in title (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=title, kw='ילד', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [03] `9179172077881` — חליפת סריג אלגנטית - מייגן

| Field | Value |
|-------|-------|
| product_id | `9179172077881` |
| title | חליפת סריג אלגנטית - מייגן |
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
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [04] `9673732194617` — חליפת פליז דגם שרון

| Field | Value |
|-------|-------|
| product_id | `9673732194617` |
| title | חליפת פליז דגם שרון |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-suit`, `fleece-baby`, `neutral-baby-outfit`, `newborn-clothing`, `winter-baby-wear` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `fleece-baby`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `type-set`, `winter-baby-wear` |
| proposed_type | `type-set` |
| type_source | handle |
| type_keyword | `set` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'set' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [05] `9874906513721` — חליפת פסים מהפנטת דגם ריף

| Field | Value |
|-------|-------|
| product_id | `9874906513721` |
| title | חליפת פסים מהפנטת דגם ריף |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-suit`, `cotton-baby`, `everyday-baby-wear`, `newborn-clothing`, `striped-baby` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `cotton-baby`, `everyday-baby-wear`, `gender-girl`, `newborn-clothing`, `striped-baby`, `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפת' in title (conf=0.88); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [06] `9179158217017` — חליפת פפיון - אלין

| Field | Value |
|-------|-------|
| product_id | `9179158217017` |
| title | חליפת פפיון - אלין |
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
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [07] `9179169128761` — חליפת פפיון קיצית - קרן

| Field | Value |
|-------|-------|
| product_id | `9179169128761` |
| title | חליפת פפיון קיצית - קרן |
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
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [08] `9606693880121` — חליפת פרווה סטייל לבנות

| Field | Value |
|-------|-------|
| product_id | `9606693880121` |
| title | חליפת פרווה סטייל לבנות |
| status | active |
| current_tags_count | 8 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `faux-fur-baby`, `girls-clothing`, `neutral-baby-outfit...` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `faux-fur-baby`, `gender-girl`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing...` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=title, kw='בנות', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [09] `9605887754553` — חליפת פשתן לתינוק

| Field | Value |
|-------|-------|
| product_id | `9605887754553` |
| title | חליפת פשתן לתינוק |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `linen-baby`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-boy` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `gender-boy`, `linen-baby`, `neutral-baby-outfit`, `newborn-clothing`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [10] `9179157266745` — חליפת פשתן מלמלות - קיילי

| Field | Value |
|-------|-------|
| product_id | `9179157266745` |
| title | חליפת פשתן מלמלות - קיילי |
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
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [11] `9858268463417` — חליפת קיץ מהפנטת דגם עומרי

| Field | Value |
|-------|-------|
| product_id | `9858268463417` |
| title | חליפת קיץ מהפנטת דגם עומרי |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-suit`, `neutral-baby-outfit`, `newborn-clothing`, `summer-baby-wear` |
| proposed_new_tags | `type-set`, `gender-boy`, `occ-seasonal` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `gender-boy`, `neutral-baby-outfit`, `newborn-clothing`, `occ-seasonal`, `summer-baby-wear`, `type-set` |
| proposed_type | `type-set` |
| type_source | handle |
| type_keyword | `set` |
| type_conf | 0.88 |
| proposed_gender | `gender-boy` |
| gender_source | handle |
| gender_keyword | `boy` |
| gender_conf | 0.90 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'set' in handle (conf=0.88); gender matched 'boy' in handle (conf=0.90); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [12] `9874906480953` — חליפת קיץ מושלמת דגם רונה

| Field | Value |
|-------|-------|
| product_id | `9874906480953` |
| title | חליפת קיץ מושלמת דגם רונה |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-suit`, `neutral-baby-outfit`, `newborn-clothing`, `summer-baby-wear` |
| proposed_new_tags | `type-set`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `occ-seasonal`, `summer-baby-wear`, `type-set` |
| proposed_type | `type-set` |
| type_source | handle |
| type_keyword | `set` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'set' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [13] `9179159888185` — חליפת קיץ מכותנה - 1977

| Field | Value |
|-------|-------|
| product_id | `9179159888185` |
| title | חליפת קיץ מכותנה - 1977 |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-suit`, `cotton-baby`, `neutral-baby-outfit`, `newborn-clothing`, `summer-baby-wear` |
| proposed_new_tags | `type-set`, `occ-seasonal` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `cotton-baby`, `neutral-baby-outfit`, `newborn-clothing`, `occ-seasonal`, `summer-baby-wear`, `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'חליפת' in title (conf=0.88); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [14] `9179173617977` — חליפת קיץ פרחונית לתינוקות – מורן

| Field | Value |
|-------|-------|
| product_id | `9179173617977` |
| title | חליפת קיץ פרחונית לתינוקות – מורן |
| status | active |
| current_tags_count | 5 |
| current_tags | `0-3 חודש`, `12-18 חודש`, `3-6 חודש`, `6-12 חודש`, `חליפה` |
| proposed_new_tags | `type-set`, `occ-seasonal` |
| final_tags_after_merge | `0-3 חודש`, `12-18 חודש`, `3-6 חודש`, `6-12 חודש`, `occ-seasonal`, `type-set`, `חליפה` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'חליפת' in title (conf=0.88); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ⚠️ YES — ['0-3 חודש', '12-18 חודש', '3-6 חודש', '6-12 חודש'] |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [15] `9606694043961` — חליפת קרופ לקיץ

| Field | Value |
|-------|-------|
| product_id | `9606694043961` |
| title | חליפת קרופ לקיץ |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-suit`, `neutral-baby-outfit`, `newborn-clothing`, `summer-baby-wear` |
| proposed_new_tags | `type-set`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `occ-seasonal`, `summer-baby-wear`, `type-set` |
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
| reason_selected | type-source=title, conf=0.88, kw='חליפת', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [16] `9688935006521` — חליפת שלוש חלקים פיל דגם אימרי

| Field | Value |
|-------|-------|
| product_id | `9688935006521` |
| title | חליפת שלוש חלקים פיל דגם אימרי |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `elephant-print-baby`, `everyday-baby-wear`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-boy` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `elephant-print-baby`, `everyday-baby-wear`, `gender-boy`, `newborn-clothing`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [17] `9179167949113` — חליפת תחרה אלגנטית - אלינויה

| Field | Value |
|-------|-------|
| product_id | `9179167949113` |
| title | חליפת תחרה אלגנטית - אלינויה |
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
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [18] `10011383202105` — סוודר סרוג לתינוקות וילדים דגם שילה

| Field | Value |
|-------|-------|
| product_id | `10011383202105` |
| title | סוודר סרוג לתינוקות וילדים דגם שילה |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-set` |
| proposed_type | `type-set` |
| type_source | handle |
| type_keyword | `outfit` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'outfit' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='outfit', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [19] `9864947990841` — סט  קיץ לבנות דגם אודיה

| Field | Value |
|-------|-------|
| product_id | `9864947990841` |
| title | סט  קיץ לבנות דגם אודיה |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `gender-girl`, `occ-seasonal`, `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `סט` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | title |
| gender_keyword | `בנות` |
| gender_conf | 0.90 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'סט' in title (conf=0.88); gender matched 'בנות' in title (conf=0.90); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='סט', gender-source=title, kw='בנות', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

---

### [20] `10025300853049` — סט Breeze™ – חולצה קצרה ומכנסי קיץ לפעוטות

| Field | Value |
|-------|-------|
| product_id | `10025300853049` |
| title | סט Breeze™ – חולצה קצרה ומכנסי קיץ לפעוטות |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-pants`, `baby-shower-gift`, `neutral-baby-outfit`, `summer-baby-wear`, `toddler` |
| proposed_new_tags | `type-set`, `occ-seasonal` |
| final_tags_after_merge | `baby-gift`, `baby-pants`, `baby-shower-gift`, `neutral-baby-outfit`, `occ-seasonal`, `summer-baby-wear`, `toddler`, `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `סט` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'סט' in title (conf=0.88); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='סט', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123456_check: ✅ PASS

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
| Not in Batch 1/2/3/4/5/6 | ✅ PASS |
| All tags in ALLOWED_VALUES | ✅ PASS |
| Hebrew month norm flagged | 1 product(s) need normalization in live stage |

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

**READY_FOR_PHASE7C_BATCH7_T3_APPROVAL**

✅ 20 SAFE candidates selected.
All safety checks PASS. No age-* tags. No type collision. No forbidden tags.
No overlap with Batch 1/2/3/4/5/6 written products. 1 product(s) need Hebrew month normalization in live stage.
Next step: request T3 approval from Ayal → Phase 7C Batch 7 live.

---

*Generated by scripts/phase7c_batch7_plan.py*