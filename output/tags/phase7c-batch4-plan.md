# Phase 7C Batch 4 — Read-Only Tagging Plan

## MODE
READ-ONLY PLANNING. No Shopify writes.

**Timestamp:** 2026-05-06T04:41:23.086606+00:00  
**Shopify writes:** NONE — GET only  

---

## 1. Selection Summary

| Item | Count |
|------|-------|
| Active products fetched | 393 |
| Already written Batch 1/2/3 (excluded) | 47 |
| Selected SAFE candidates | **20** |
| Safety flags | 0 ✅ |

### Type Breakdown

| Type | Count |
|------|-------|
| `type-dress` | 5 |
| `type-set` | 5 |
| `type-romper` | 5 |
| `type-bodysuit` | 5 |

---

## 2. Excluded / Blocked

- Already written in Batch 1/2/3 (explicit PID exclusion): excluded
- Already tagged with `type-*` in Shopify: excluded
- Shoe/sandal/sneaker title keyword: excluded
- False-positive keyword (מגבת/תיק/שמיכה/towel/bag/blanket/swimwear): excluded
- Low confidence (< type min_conf): excluded
- Non-preferred types (hat/coat/pants/top/swimwear): excluded
- REVIEW_ONLY: excluded (not in SAFE pool)

---

## 3. Per-Product Evidence

### [01] `9179162444089` — שמלת כיווצים קיצית מכותנה - ענבל

| Field | Value |
|-------|-------|
| product_id | `9179162444089` |
| title | שמלת כיווצים קיצית מכותנה - ענבל |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-dress` |
| final_tags_after_merge | `type-dress` |
| proposed_type | `type-dress` |
| type_source | title |
| type_keyword | `שמלת` |
| type_conf | 0.90 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'שמלת' in title (conf=0.90) |
| risk_level | LOW |
| confidence | 0.90 |
| reason_selected | type-source=title, conf=0.90, kw='שמלת', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [02] `9179150516537` — שמלת מלמלות מתוקה מכותנה - לין

| Field | Value |
|-------|-------|
| product_id | `9179150516537` |
| title | שמלת מלמלות מתוקה מכותנה - לין |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-dress` |
| final_tags_after_merge | `type-dress` |
| proposed_type | `type-dress` |
| type_source | title |
| type_keyword | `שמלת` |
| type_conf | 0.90 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'שמלת' in title (conf=0.90) |
| risk_level | LOW |
| confidence | 0.90 |
| reason_selected | type-source=title, conf=0.90, kw='שמלת', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [03] `9179142750521` — שמלת סטרפלס סטייל קז'ואל - ליאל

| Field | Value |
|-------|-------|
| product_id | `9179142750521` |
| title | שמלת סטרפלס סטייל קז'ואל - ליאל |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-dress` |
| final_tags_after_merge | `type-dress` |
| proposed_type | `type-dress` |
| type_source | title |
| type_keyword | `שמלת` |
| type_conf | 0.90 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'שמלת' in title (conf=0.90) |
| risk_level | LOW |
| confidence | 0.90 |
| reason_selected | type-source=title, conf=0.90, kw='שמלת', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [04] `9605887721785` — שמלת סרבל לתינוקת

| Field | Value |
|-------|-------|
| product_id | `9605887721785` |
| title | שמלת סרבל לתינוקת |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-romper`, `cotton-baby`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-dress`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-romper`, `cotton-baby`, `everyday-baby-wear`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `type-dress` |
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
| reason_selected | type-source=handle, conf=0.90, kw='dress', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [05] `9179136131385` — שמלת ערב נסיכותית - רצ'ל

| Field | Value |
|-------|-------|
| product_id | `9179136131385` |
| title | שמלת ערב נסיכותית - רצ'ל |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-dress` |
| final_tags_after_merge | `type-dress` |
| proposed_type | `type-dress` |
| type_source | title |
| type_keyword | `שמלת` |
| type_conf | 0.90 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'שמלת' in title (conf=0.90) |
| risk_level | LOW |
| confidence | 0.90 |
| reason_selected | type-source=title, conf=0.90, kw='שמלת', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [06] `9855017582905` — חליפה מעוצבת סטייל שובב דגם ליאם

| Field | Value |
|-------|-------|
| product_id | `9855017582905` |
| title | חליפה מעוצבת סטייל שובב דגם ליאם |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [07] `10009173721401` — חליפה קטיפתית לתינוק – חמימות, נוחות וסטייל בשלושה חלקים

| Field | Value |
|-------|-------|
| product_id | `10009173721401` |
| title | חליפה קטיפתית לתינוק – חמימות, נוחות וסטייל בשלושה חלקים |
| status | active |
| current_tags_count | 7 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `neutral-baby-outfit`, `newborn-clothing`, `velvet-baby...` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `type-set`, `velvet-baby...` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפה` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפה' in title (conf=0.88); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| reason_selected | type-source=title, conf=0.88, kw='חליפה', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [08] `9179173191993` — חליפה קיצית פרחונית - היילי

| Field | Value |
|-------|-------|
| product_id | `9179173191993` |
| title | חליפה קיצית פרחונית - היילי |
| status | active |
| current_tags_count | 5 |
| current_tags | `0-3 חודש`, `12-18 חודש`, `18-24 חודש`, `3-6 חודש`, `6-12 חודש` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `0-3 חודש`, `12-18 חודש`, `18-24 חודש`, `3-6 חודש`, `6-12 חודש`, `type-set` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפה` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'חליפה' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| reason_selected | type-source=title, conf=0.88, kw='חליפה', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [09] `9606691914041` — חליפה קלאסית ואופנתית לבנות

| Field | Value |
|-------|-------|
| product_id | `9606691914041` |
| title | חליפה קלאסית ואופנתית לבנות |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `gender-girl`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=title, kw='בנות', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [10] `9688955912505` — חליפת 3 חלקים אריה מתוקה אם ווסט פרוותי דגם חן

| Field | Value |
|-------|-------|
| product_id | `9688955912505` |
| title | חליפת 3 חלקים אריה מתוקה אם ווסט פרוותי דגם חן |
| status | active |
| current_tags_count | 5 |
| current_tags | `12-18 חודש`, `18-24 חודש`, `2-3 שנים`, `6-12 חודש`, `סט` |
| proposed_new_tags | `type-set`, `gender-boy` |
| final_tags_after_merge | `12-18 חודש`, `18-24 חודש`, `2-3 שנים`, `6-12 חודש`, `gender-boy`, `type-set`, `סט` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [11] `9179137933625` — אוברול מתוק מכותנה מלאה ללא כתפיות - נויה

| Field | Value |
|-------|-------|
| product_id | `9179137933625` |
| title | אוברול מתוק מכותנה מלאה ללא כתפיות - נויה |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-romper` |
| final_tags_after_merge | `type-romper` |
| proposed_type | `type-romper` |
| type_source | title |
| type_keyword | `אוברול` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'אוברול' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| reason_selected | type-source=title, conf=0.88, kw='אוברול', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [12] `9096607072569` — אוברול סרבל ארוך

| Field | Value |
|-------|-------|
| product_id | `9096607072569` |
| title | אוברול סרבל ארוך |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-overall`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-romper` |
| final_tags_after_merge | `baby-gift`, `baby-overall`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing`, `type-romper` |
| proposed_type | `type-romper` |
| type_source | title |
| type_keyword | `אוברול` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'אוברול' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| reason_selected | type-source=title, conf=0.88, kw='אוברול', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [13] `9688670110009` — אוברול פינגווין דגם נועם

| Field | Value |
|-------|-------|
| product_id | `9688670110009` |
| title | אוברול פינגווין דגם נועם |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-romper` |
| final_tags_after_merge | `type-romper`, `אוברול` |
| proposed_type | `type-romper` |
| type_source | title |
| type_keyword | `אוברול` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'אוברול' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| reason_selected | type-source=title, conf=0.88, kw='אוברול', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [14] `9657036374329` — אוברול פליז דובי לתינוק – Teddy Cozy Suit

| Field | Value |
|-------|-------|
| product_id | `9657036374329` |
| title | אוברול פליז דובי לתינוק – Teddy Cozy Suit |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-romper` |
| final_tags_after_merge | `type-romper`, `אוברול` |
| proposed_type | `type-romper` |
| type_source | title |
| type_keyword | `אוברול` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'אוברול' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| reason_selected | type-source=title, conf=0.88, kw='אוברול', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [15] `9179158479161` — אוברול פשתן וכותנה וינטג׳ - קייגו

| Field | Value |
|-------|-------|
| product_id | `9179158479161` |
| title | אוברול פשתן וכותנה וינטג׳ - קייגו |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-romper` |
| final_tags_after_merge | `type-romper`, `אוברול` |
| proposed_type | `type-romper` |
| type_source | title |
| type_keyword | `אוברול` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'אוברול' in title (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| reason_selected | type-source=title, conf=0.88, kw='אוברול', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [16] `9605887787321` — חליפה סרוגה לתינוק

| Field | Value |
|-------|-------|
| product_id | `9605887787321` |
| title | חליפה סרוגה לתינוק |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing`, `soft-knit` |
| proposed_new_tags | `type-bodysuit`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `soft-knit`, `type-bodysuit` |
| proposed_type | `type-bodysuit` |
| type_source | handle |
| type_keyword | `bodysuit` |
| type_conf | 0.90 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'bodysuit' in handle (conf=0.90); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.90 |
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [17] `9606691750201` — יחידת בגד גוף עם סרט לשיער לתינוק

| Field | Value |
|-------|-------|
| product_id | `9606691750201` |
| title | יחידת בגד גוף עם סרט לשיער לתינוק |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-bodysuit`, `baby-gift`, `cotton-baby`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-bodysuit`, `gender-girl` |
| final_tags_after_merge | `baby-bodysuit`, `baby-gift`, `cotton-baby`, `everyday-baby-wear`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `type-bodysuit` |
| proposed_type | `type-bodysuit` |
| type_source | handle |
| type_keyword | `bodysuit` |
| type_conf | 0.90 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'bodysuit' in handle (conf=0.90); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.90 |
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [18] `9687563305273` — סט 3 אוברולים ארנב דגם  שני

| Field | Value |
|-------|-------|
| product_id | `9687563305273` |
| title | סט 3 אוברולים ארנב דגם  שני |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-bodysuit`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-bodysuit`, `אוברול` |
| proposed_type | `type-bodysuit` |
| type_source | handle |
| type_keyword | `bodysuit` |
| type_conf | 0.90 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'bodysuit' in handle (conf=0.90); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.90 |
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [19] `9687563370809` — סט לב לבנות דגם נועה

| Field | Value |
|-------|-------|
| product_id | `9687563370809` |
| title | סט לב לבנות דגם נועה |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-bodysuit`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-bodysuit` |
| proposed_type | `type-bodysuit` |
| type_source | handle |
| type_keyword | `bodysuit` |
| type_conf | 0.90 |
| proposed_gender | `gender-girl` |
| gender_source | title |
| gender_keyword | `בנות` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'bodysuit' in handle (conf=0.90); gender matched 'בנות' in title (conf=0.90) |
| risk_level | LOW |
| confidence | 0.90 |
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=title, kw='בנות', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

---

### [20] `9719189733689` — סט מכנס וחולצה דגם הלל

| Field | Value |
|-------|-------|
| product_id | `9719189733689` |
| title | סט מכנס וחולצה דגם הלל |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-bodysuit`, `gender-boy` |
| final_tags_after_merge | `gender-boy`, `type-bodysuit` |
| proposed_type | `type-bodysuit` |
| type_source | handle |
| type_keyword | `bodysuit` |
| type_conf | 0.90 |
| proposed_gender | `gender-boy` |
| gender_source | handle |
| gender_keyword | `boy` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'bodysuit' in handle (conf=0.90); gender matched 'boy' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.90 |
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch123_check: ✅ PASS

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
| Not in Batch 1/2/3 | ✅ PASS |
| All tags in ALLOWED_VALUES | ✅ PASS |

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
9. Shopify PUT only after T3 approval
10. Shopify GET verify
11. post-verify independent check
12. rollback plan on file
13. report
14. explicit git add only (no git add -A)

---

## 6. Verdict

**READY_FOR_PHASE7C_BATCH4_T3_APPROVAL**

✅ 20 SAFE candidates selected.
All safety checks PASS. No age-* tags. No type collision. No forbidden tags.
No overlap with Batch 1/2/3 written products.
Next step: request T3 approval from Ayal → Phase 7C Batch 4 live.

---

*Generated by scripts/phase7c_batch4_plan.py*