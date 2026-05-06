# Phase 7C Batch 8 — Read-Only Tagging Plan

## MODE
READ-ONLY PLANNING. No Shopify writes.

**Timestamp:** 2026-05-06T12:13:25.437066+00:00  
**Shopify writes:** NONE — GET only  

---

## 1. Selection Summary

| Item | Count |
|------|-------|
| Active products fetched | 393 |
| Already written Batch 1/2/3/4/5/6/7 (excluded) | 126 |
| Selected SAFE candidates | **20** |
| Need Hebrew month normalization | 0 |
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

- Already written in Batch 1/2/3/4/5/6/7 (explicit PID exclusion): excluded
- T3-manually-excluded: `10011383202105` סוודר סרוג לתינוקות (requires explicit re-approval)
- Already tagged with `type-*` in Shopify: excluded
- Shoe/sandal/sneaker title keyword: excluded
- False-positive keyword (מגבת/תיק/שמיכה/towel/bag/blanket/swimwear/hat/rack/brushes): excluded
- Low confidence (< type min_conf): excluded
- Non-preferred types (hat/coat/pants/top/swimwear): excluded
- REVIEW_ONLY: excluded (not in SAFE pool)

---

## 3. Per-Product Evidence

### [01] `9096622473529` — סט Solé™

| Field | Value |
|-------|-------|
| product_id | `9096622473529` |
| title | סט Solé™ |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `סט` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'סט' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='סט', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [02] `9606691848505` — סט אבטיח לקיץ דגם אביבית

| Field | Value |
|-------|-------|
| product_id | `9606691848505` |
| title | סט אבטיח לקיץ דגם אביבית |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `gender-girl`, `occ-seasonal`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [03] `9606694240569` — סט אוברול וחולצה דגם קובי

| Field | Value |
|-------|-------|
| product_id | `9606694240569` |
| title | סט אוברול וחולצה דגם קובי |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-set`, `gender-boy` |
| final_tags_after_merge | `gender-boy`, `type-set`, `אוברול` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [04] `9606670909753` — סט אופנתי קצר לתינוק

| Field | Value |
|-------|-------|
| product_id | `9606670909753` |
| title | סט אופנתי קצר לתינוק |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set`, `gender-boy` |
| final_tags_after_merge | `gender-boy`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [05] `9606694076729` — סט אלגנטי דגם מעיין

| Field | Value |
|-------|-------|
| product_id | `9606694076729` |
| title | סט אלגנטי דגם מעיין |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `elegant-baby`, `everyday-baby-wear`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `elegant-baby`, `everyday-baby-wear`, `gender-girl`, `newborn-clothing`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [06] `9096622604601` — סט בגדי תינוקות  בנות

| Field | Value |
|-------|-------|
| product_id | `9096622604601` |
| title | סט בגדי תינוקות  בנות |
| status | active |
| current_tags_count | 7 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `girls-clothing`, `neutral-baby-outfit...` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `gender-girl`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing...` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `סט` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | title |
| gender_keyword | `בנות` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'סט' in title (conf=0.88); gender matched 'בנות' in title (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='סט', gender-source=title, kw='בנות', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [07] `10011383234873` — סט בגדים לתינוקות – חולצה ארוכה + אוברול גינס

| Field | Value |
|-------|-------|
| product_id | `10011383234873` |
| title | סט בגדים לתינוקות – חולצה ארוכה + אוברול גינס |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-set`, `אוברול` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `סט` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'סט' in title (conf=0.88); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='סט', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [08] `9873511055673` — סט בייסיק לתינוקות דגם  לירון

| Field | Value |
|-------|-------|
| product_id | `9873511055673` |
| title | סט בייסיק לתינוקות דגם  לירון |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [09] `9606694371641` — סט בסגנון וינטג' אלגנטי לתינוקת

| Field | Value |
|-------|-------|
| product_id | `9606694371641` |
| title | סט בסגנון וינטג' אלגנטי לתינוקת |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `סט` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'סט' in title (conf=0.88); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='סט', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [10] `9606693945657` — סט ג'ינס אופנתי לבנות

| Field | Value |
|-------|-------|
| product_id | `9606693945657` |
| title | סט ג'ינס אופנתי לבנות |
| status | active |
| current_tags_count | 8 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `denim-baby`, `denim-style-baby`, `everyday-baby-wear...` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `denim-baby`, `denim-style-baby`, `everyday-baby-wear`, `gender-girl`, `girls-clothing...` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=title, kw='בנות', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [11] `9724813410617` — סט גי'נס מושלם דגם נחמן

| Field | Value |
|-------|-------|
| product_id | `9724813410617` |
| title | סט גי'נס מושלם דגם נחמן |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-boy` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `gender-boy`, `neutral-baby-outfit`, `newborn-clothing`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [12] `9673732260153` — סט דובי פליז מחמם דגם נאור

| Field | Value |
|-------|-------|
| product_id | `9673732260153` |
| title | סט דובי פליז מחמם דגם נאור |
| status | active |
| current_tags_count | 7 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `bear-print-baby`, `fleece-baby`, `newborn-clothing...` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `bear-print-baby`, `fleece-baby`, `gender-girl`, `newborn-clothing`, `type-set...` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [13] `9864947958073` — סט חגיגי לקיץ דגם שירה

| Field | Value |
|-------|-------|
| product_id | `9864947958073` |
| title | סט חגיגי לקיץ דגם שירה |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `newborn-clothing`, `special-occasion-baby`, `summer-baby-wear` |
| proposed_new_tags | `type-set`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `gender-girl`, `newborn-clothing`, `occ-seasonal`, `special-occasion-baby`, `summer-baby-wear...` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `סט` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'סט' in title (conf=0.88); gender matched 'girl' in handle (conf=0.90); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='סט', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [14] `9606670942521` — סט חגיגי לתינוקת

| Field | Value |
|-------|-------|
| product_id | `9606670942521` |
| title | סט חגיגי לתינוקת |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `newborn-clothing`, `special-occasion-baby` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `gender-girl`, `newborn-clothing`, `special-occasion-baby`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [15] `9687579066681` — סט חד קרן דגם לינוי

| Field | Value |
|-------|-------|
| product_id | `9687579066681` |
| title | סט חד קרן דגם לינוי |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [16] `9606691619129` — סט חולצה וחצאית ג'ינס חגיגי

| Field | Value |
|-------|-------|
| product_id | `9606691619129` |
| title | סט חולצה וחצאית ג'ינס חגיגי |
| status | active |
| current_tags_count | 7 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `denim-baby`, `denim-style-baby`, `everyday-baby-wear...` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `denim-baby`, `denim-style-baby`, `everyday-baby-wear`, `gender-girl`, `newborn-clothing...` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [17] `9687563403577` — סט חתול קלאסי דגם אדל

| Field | Value |
|-------|-------|
| product_id | `9687563403577` |
| title | סט חתול קלאסי דגם אדל |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [18] `9672569749817` — סט לב גדול דגם שני

| Field | Value |
|-------|-------|
| product_id | `9672569749817` |
| title | סט לב גדול דגם שני |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `סט` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'סט' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='סט', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [19] `9606691422521` — סט לילדה וינטג' - מורן

| Field | Value |
|-------|-------|
| product_id | `9606691422521` |
| title | סט לילדה וינטג' - מורן |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-set` |
| proposed_type | `type-set` |
| type_source | handle |
| type_keyword | `set` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | title |
| gender_keyword | `ילדה` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'set' in handle (conf=0.88); gender matched 'ילדה' in title (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=title, kw='ילדה', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [20] `9688674500921` — סט מכנס וחולצה דובי דגם רפאל

| Field | Value |
|-------|-------|
| product_id | `9688674500921` |
| title | סט מכנס וחולצה דובי דגם רפאל |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `bear-print-baby`, `everyday-baby-wear`, `newborn-clothing` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `bear-print-baby`, `everyday-baby-wear`, `newborn-clothing`, `type-set` |
| proposed_type | `type-set` |
| type_source | handle |
| type_keyword | `set` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'set' in handle (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='set', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234567_check: ✅ PASS
- t3_excluded_check: ✅ PASS

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
| Not in Batch 1/2/3/4/5/6/7 | ✅ PASS |
| T3-excluded not leaked | ✅ PASS |
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

**READY_FOR_PHASE7C_BATCH8_T3_APPROVAL**

✅ 20 SAFE candidates selected.
All safety checks PASS. No age-* tags. No type collision. No forbidden tags.
No overlap with Batch 1/2/3/4/5/6/7 written products. 0 product(s) need Hebrew month normalization in live stage.
Next step: request T3 approval from Ayal → Phase 7C Batch 8 live.

---

*Generated by scripts/phase7c_batch8_plan.py*