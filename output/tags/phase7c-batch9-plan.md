# Phase 7C Batch 9 — Read-Only Tagging Plan

## MODE
READ-ONLY PLANNING. No Shopify writes.

**Timestamp:** 2026-05-06T14:29:19.539811+00:00  
**Shopify writes:** NONE — GET only  

---

## 1. Selection Summary

| Item | Count |
|------|-------|
| Active products fetched | 393 |
| Already written Batch 1/2/3/4/5/6/7/8 (excluded) | 146 |
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

- Already written in Batch 1/2/3/4/5/6/7/8 (explicit PID exclusion): excluded
- T3-manually-excluded: `10011383202105` סוודר סרוג לתינוקות (requires explicit re-approval)
- Already tagged with `type-*` in Shopify: excluded
- Shoe/sandal/sneaker title keyword: excluded
- False-positive keyword (מגבת/תיק/שמיכה/towel/bag/blanket/swimwear/hat/rack/brushes/טטרה): excluded
- Low confidence (< type min_conf): excluded
- Non-preferred types (hat/coat/pants/top/swimwear): excluded
- REVIEW_ONLY: excluded (not in SAFE pool)

---

## 3. Per-Product Evidence

### [01] `10011383071033` — סט מכנס וחולצה מהממים דגם דניאל

| Field | Value |
|-------|-------|
| product_id | `10011383071033` |
| title | סט מכנס וחולצה מהממים דגם דניאל |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-boy` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `gender-boy`, `neutral-baby-outfit`, `newborn-clothing`, `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `סט` |
| type_conf | 0.88 |
| proposed_gender | `gender-boy` |
| gender_source | handle |
| gender_keyword | `boy` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'סט' in title (conf=0.88); gender matched 'boy' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='סט', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [02] `9724813476153` — סט מכנס וחולצה קואלה דגם ראם

| Field | Value |
|-------|-------|
| product_id | `9724813476153` |
| title | סט מכנס וחולצה קואלה דגם ראם |
| status | active |
| current_tags_count | 6 |
| current_tags | `animal-print-baby`, `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `animal-print-baby`, `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `gender-girl`, `newborn-clothing`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [03] `9855017648441` — סט מכנס וחולצה קיצי דגם גילי

| Field | Value |
|-------|-------|
| product_id | `9855017648441` |
| title | סט מכנס וחולצה קיצי דגם גילי |
| status | active |
| current_tags_count | 7 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `cotton-baby`, `neutral-baby-outfit`, `newborn-clothing...` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `cotton-baby`, `neutral-baby-outfit`, `newborn-clothing`, `summer-baby-wear`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [04] `9096636694841` — סט מלא לתינוקות - קופסת מתנה

| Field | Value |
|-------|-------|
| product_id | `9096636694841` |
| title | סט מלא לתינוקות - קופסת מתנה |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set`, `occ-gift` |
| final_tags_after_merge | `occ-gift`, `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `סט` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `occ-gift` |
| source_trace | type matched 'סט' in title (conf=0.88); occ: occ-gift |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='סט', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [05] `9688955978041` — סט מתוק מפליז אם ווסט תואם דגם ראם

| Field | Value |
|-------|-------|
| product_id | `9688955978041` |
| title | סט מתוק מפליז אם ווסט תואם דגם ראם |
| status | active |
| current_tags_count | 6 |
| current_tags | `12-18 חודש`, `18-24 חודש`, `2-3 שנים`, `6-12 חודש`, `חורף`, `סט` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `12-18 חודש`, `18-24 חודש`, `2-3 שנים`, `6-12 חודש`, `type-set`, `חורף`, `סט` |
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
| month_normalization_needed | ⚠️ YES — ['12-18 חודש', '18-24 חודש', '6-12 חודש'] |
| reason_selected | type-source=handle, conf=0.88, kw='set', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [06] `10029649068345` — סט נוחות אליאב

| Field | Value |
|-------|-------|
| product_id | `10029649068345` |
| title | סט נוחות אליאב |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [07] `9096607203641` — סט סוודר חורפי דניאל

| Field | Value |
|-------|-------|
| product_id | `9096607203641` |
| title | סט סוודר חורפי דניאל |
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
| reason_selected | type-source=title, conf=0.88, kw='סט', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [08] `9606693749049` — סט פיג'מה ארוכה דובונים לחורף

| Field | Value |
|-------|-------|
| product_id | `9606693749049` |
| title | סט פיג'מה ארוכה דובונים לחורף |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `neutral-baby-outfit`, `newborn-clothing`, `winter-baby-wear` |
| proposed_new_tags | `type-set`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `occ-seasonal`, `type-set...` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [09] `9606694306105` — סט פיג'מה ארוכה לילד

| Field | Value |
|-------|-------|
| product_id | `9606694306105` |
| title | סט פיג'מה ארוכה לילד |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `kids-clothing`, `neutral-baby-outfit` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `gender-girl`, `kids-clothing`, `neutral-baby-outfit`, `type-set` |
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
| reason_selected | type-source=title, conf=0.88, kw='סט', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [10] `9606671008057` — סט פרחוני וג'ינס לתינוקת

| Field | Value |
|-------|-------|
| product_id | `9606671008057` |
| title | סט פרחוני וג'ינס לתינוקת |
| status | active |
| current_tags_count | 7 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `denim-baby`, `everyday-baby-wear`, `floral-baby...` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `denim-baby`, `everyday-baby-wear`, `floral-baby`, `gender-girl`, `newborn-clothing...` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [11] `9606691586361` — סט פשתן קלאסי ואלגנטי לבנים ובנות

| Field | Value |
|-------|-------|
| product_id | `9606691586361` |
| title | סט פשתן קלאסי ואלגנטי לבנים ובנות |
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
| gender_source | title |
| gender_keyword | `בנות` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'סט' in title (conf=0.88); gender matched 'בנות' in title (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='סט', gender-source=title, kw='בנות', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [12] `9605887820089` — סט קיצי לתינוקות וילדות

| Field | Value |
|-------|-------|
| product_id | `9605887820089` |
| title | סט קיצי לתינוקות וילדות |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `kids-clothing`, `neutral-baby-outfit`, `summer-baby-wear` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `gender-girl`, `kids-clothing`, `neutral-baby-outfit`, `summer-baby-wear`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [13] `9864947728697` — סט קיצי משגע לבנות דגם בת אל

| Field | Value |
|-------|-------|
| product_id | `9864947728697` |
| title | סט קיצי משגע לבנות דגם בת אל |
| status | active |
| current_tags_count | 7 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing...` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `gender-girl`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing`, `summer-baby-wear...` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=title, kw='בנות', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [14] `10029649035577` — סט רומפר מעבר דגם אורן

| Field | Value |
|-------|-------|
| product_id | `10029649035577` |
| title | סט רומפר מעבר דגם אורן |
| status | active |
| current_tags_count | 6 |
| current_tags | `autumn-baby-wear`, `baby-gift`, `baby-romper`, `baby-shower-gift`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `autumn-baby-wear`, `baby-gift`, `baby-romper`, `baby-shower-gift`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `type-set` |
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
| reason_selected | type-source=title, conf=0.88, kw='סט', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [15] `9606691389753` — סט שיא הסטייל לבנים

| Field | Value |
|-------|-------|
| product_id | `9606691389753` |
| title | סט שיא הסטייל לבנים |
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
| gender_source | title |
| gender_keyword | `בנים` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'set' in handle (conf=0.88); gender matched 'בנים' in title (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=title, kw='בנים', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [16] `9873510957369` — סט של 3 אוברולים עונת מעבר דגם ישראל

| Field | Value |
|-------|-------|
| product_id | `9873510957369` |
| title | סט של 3 אוברולים עונת מעבר דגם ישראל |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set`, `אוברול` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [17] `9687653024057` — סט שני חליפות חד קרן דגם אנה

| Field | Value |
|-------|-------|
| product_id | `9687653024057` |
| title | סט שני חליפות חד קרן דגם אנה |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `newborn-clothing`, `unicorn-baby` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `newborn-clothing`, `type-set`, `unicorn-baby` |
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
| reason_selected | type-source=title, conf=0.88, kw='סט', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [18] `10011383136569` — סטים 3 חליפות סגירה קלה דגם רוני

| Field | Value |
|-------|-------|
| product_id | `10011383136569` |
| title | סטים 3 חליפות סגירה קלה דגם רוני |
| status | active |
| current_tags_count | 7 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `cotton-baby`, `everyday-baby-wear`, `neutral-baby-outfit...` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `cotton-baby`, `everyday-baby-wear`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing...` |
| proposed_type | `type-set` |
| type_source | handle |
| type_keyword | `pcs` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'pcs' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='pcs', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [19] `9678573207865` — סרבל מעוצב אלגנטי דגם מאור

| Field | Value |
|-------|-------|
| product_id | `9678573207865` |
| title | סרבל מעוצב אלגנטי דגם מאור |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-romper`, `elegant-baby`, `everyday-baby-wear`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-boy` |
| final_tags_after_merge | `baby-gift`, `baby-romper`, `elegant-baby`, `everyday-baby-wear`, `gender-boy`, `newborn-clothing`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
- t3_excluded_check: ✅ PASS

---

### [20] `9605887492409` — סרבל עבודה אופנתי לתינוק

| Field | Value |
|-------|-------|
| product_id | `9605887492409` |
| title | סרבל עבודה אופנתי לתינוק |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-romper`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-romper`, `everyday-baby-wear`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `type-set` |
| proposed_type | `type-set` |
| type_source | handle |
| type_keyword | `suit` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'suit' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='suit', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4/5/6/7/8 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch12345678_check: ✅ PASS
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
| Not in Batch 1/2/3/4/5/6/7/8 | ✅ PASS |
| T3-excluded not leaked | ✅ PASS |
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

**READY_FOR_PHASE7C_BATCH9_T3_APPROVAL**

✅ 20 SAFE candidates selected.
All safety checks PASS. No age-* tags. No type collision. No forbidden tags.
No overlap with Batch 1/2/3/4/5/6/7/8 written products. 1 product(s) need Hebrew month normalization in live stage.
Next step: request T3 approval from Ayal → Phase 7C Batch 9 live.

---

*Generated by scripts/phase7c_batch9_plan.py*