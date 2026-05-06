# Phase 7C Batch 5 — Read-Only Tagging Plan

## MODE
READ-ONLY PLANNING. No Shopify writes.

**Timestamp:** 2026-05-06T05:06:58.255562+00:00  
**Shopify writes:** NONE — GET only  

---

## 1. Selection Summary

| Item | Count |
|------|-------|
| Active products fetched | 393 |
| Already written Batch 1/2/3/4 (excluded) | 67 |
| Selected SAFE candidates | **20** |
| Need Hebrew month normalization | 0 |
| Safety flags | 0 ✅ |

### Type Breakdown

| Type | Count |
|------|-------|
| `type-set` | 6 |
| `type-dress` | 5 |
| `type-bodysuit` | 5 |
| `type-romper` | 4 |

---

## 2. Excluded / Blocked

- Already written in Batch 1/2/3/4 (explicit PID exclusion): excluded
- Already tagged with `type-*` in Shopify: excluded
- Shoe/sandal/sneaker title keyword: excluded
- False-positive keyword (מגבת/תיק/שמיכה/towel/bag/blanket/swimwear): excluded
- Low confidence (< type min_conf): excluded
- Non-preferred types (hat/coat/pants/top/swimwear): excluded
- REVIEW_ONLY: excluded (not in SAFE pool)

---

## 3. Per-Product Evidence

### [01] `9892620894521` — שמלת פליסה דגם אוריה

| Field | Value |
|-------|-------|
| product_id | `9892620894521` |
| title | שמלת פליסה דגם אוריה |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-dress`, `baby-gift`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-dress`, `gender-girl` |
| final_tags_after_merge | `baby-dress`, `baby-gift`, `everyday-baby-wear`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `type-dress` |
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
| reason_selected | type-source=handle, conf=0.90, kw='dress', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [02] `9179151008057` — שמלת פפיון אחורי קלאסית - לוראן

| Field | Value |
|-------|-------|
| product_id | `9179151008057` |
| title | שמלת פפיון אחורי קלאסית - לוראן |
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
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.90, kw='שמלת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [03] `9179149173049` — שמלת פפיון אלגנטית קלאסית - לין

| Field | Value |
|-------|-------|
| product_id | `9179149173049` |
| title | שמלת פפיון אלגנטית קלאסית - לין |
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
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.90, kw='שמלת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [04] `9892196417849` — שמלת פפיון כחולה דגם אביבה

| Field | Value |
|-------|-------|
| product_id | `9892196417849` |
| title | שמלת פפיון כחולה דגם אביבה |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-dress`, `baby-gift`, `neutral-baby-outfit`, `newborn-clothing`, `spring-baby-wear` |
| proposed_new_tags | `type-dress`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `baby-dress`, `baby-gift`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `occ-seasonal`, `spring-baby-wear`, `type-dress` |
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
| reason_selected | type-source=handle, conf=0.90, kw='dress', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [05] `9606693978425` — שמלת קיץ חגיגית עם מלמלה

| Field | Value |
|-------|-------|
| product_id | `9606693978425` |
| title | שמלת קיץ חגיגית עם מלמלה |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-dress`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `gender-girl`, `occ-seasonal`, `type-dress` |
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
| reason_selected | type-source=handle, conf=0.90, kw='dress', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [06] `9858268528953` — חליפת אביב יוקרתית דגם  דין

| Field | Value |
|-------|-------|
| product_id | `9858268528953` |
| title | חליפת אביב יוקרתית דגם  דין |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-shower-gift`, `baby-suit`, `newborn-clothing`, `special-occasion-baby`, `spring-baby-wear` |
| proposed_new_tags | `type-set`, `gender-boy`, `occ-seasonal` |
| final_tags_after_merge | `baby-gift`, `baby-shower-gift`, `baby-suit`, `gender-boy`, `newborn-clothing`, `occ-seasonal`, `special-occasion-baby`, `spring-baby-wear...` |
| proposed_type | `type-set` |
| type_source | title |
| type_keyword | `חליפת` |
| type_conf | 0.88 |
| proposed_gender | `gender-boy` |
| gender_source | handle |
| gender_keyword | `boy` |
| gender_conf | 0.90 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'חליפת' in title (conf=0.88); gender matched 'boy' in handle (conf=0.90); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='חליפת', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [07] `9179145568569` — חליפת אוברול קיצית נושמת ונעימה - גיא

| Field | Value |
|-------|-------|
| product_id | `9179145568569` |
| title | חליפת אוברול קיצית נושמת ונעימה - גיא |
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
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [08] `10011383103801` — חליפת אלופים מהממת דגם שון  מבית בייבי מניה

| Field | Value |
|-------|-------|
| product_id | `10011383103801` |
| title | חליפת אלופים מהממת דגם שון  מבית בייבי מניה |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-boy` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `everyday-baby-wear`, `gender-boy`, `neutral-baby-outfit`, `newborn-clothing`, `type-set` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [09] `9179151335737` — חליפת גופייה פרחונית - מאיה

| Field | Value |
|-------|-------|
| product_id | `9179151335737` |
| title | חליפת גופייה פרחונית - מאיה |
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
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [10] `9179152875833` — חליפת גופייה קיצית - מאור

| Field | Value |
|-------|-------|
| product_id | `9179152875833` |
| title | חליפת גופייה קיצית - מאור |
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
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [11] `10009173033273` — אוברול קטיפתי לתינוק – חמימות, נוחות וסטייל לחורף

| Field | Value |
|-------|-------|
| product_id | `10009173033273` |
| title | אוברול קטיפתי לתינוק – חמימות, נוחות וסטייל לחורף |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-romper`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `gender-girl`, `occ-seasonal`, `type-romper`, `אוברול` |
| proposed_type | `type-romper` |
| type_source | handle |
| type_keyword | `romper` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'romper' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='romper', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [12] `9895864435001` — אוברול קיץ לתינוקות בעיצוב דובי דגם שי

| Field | Value |
|-------|-------|
| product_id | `9895864435001` |
| title | אוברול קיץ לתינוקות בעיצוב דובי דגם שי |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-romper`, `gender-girl`, `occ-seasonal` |
| final_tags_after_merge | `gender-girl`, `occ-seasonal`, `type-romper`, `אוברול` |
| proposed_type | `type-romper` |
| type_source | title |
| type_keyword | `אוברול` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `occ-seasonal` |
| source_trace | type matched 'אוברול' in title (conf=0.88); gender matched 'girl' in handle (conf=0.90); occ: occ-seasonal |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=title, conf=0.88, kw='אוברול', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [13] `9605503516985` — סרבל ארנב לתינוק

| Field | Value |
|-------|-------|
| product_id | `9605503516985` |
| title | סרבל ארנב לתינוק |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-romper`, `cotton-baby`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-romper`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-romper`, `cotton-baby`, `everyday-baby-wear`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `type-romper` |
| proposed_type | `type-romper` |
| type_source | handle |
| type_keyword | `romper` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'romper' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='romper', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [14] `9874906415417` — רומפר קייצי מבית בייבי מניה דגם דין

| Field | Value |
|-------|-------|
| product_id | `9874906415417` |
| title | רומפר קייצי מבית בייבי מניה דגם דין |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-romper`, `neutral-baby-outfit`, `newborn-clothing`, `summer-baby-wear` |
| proposed_new_tags | `type-romper`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-romper`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `summer-baby-wear`, `type-romper` |
| proposed_type | `type-romper` |
| type_source | handle |
| type_keyword | `romper` |
| type_conf | 0.88 |
| proposed_gender | `gender-girl` |
| gender_source | handle |
| gender_keyword | `girl` |
| gender_conf | 0.90 |
| proposed_occs | `—` |
| source_trace | type matched 'romper' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.88 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.88, kw='romper', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [15] `9864947859769` — סט פרחוני קיצי דגם לירון

| Field | Value |
|-------|-------|
| product_id | `9864947859769` |
| title | סט פרחוני קיצי דגם לירון |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `floral-baby`, `newborn-clothing`, `summer-baby-wear` |
| proposed_new_tags | `type-bodysuit`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `floral-baby`, `gender-girl`, `newborn-clothing`, `summer-baby-wear`, `type-bodysuit` |
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
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [16] `9855017615673` — סט קיצי אלגנטי דגם מיה

| Field | Value |
|-------|-------|
| product_id | `9855017615673` |
| title | סט קיצי אלגנטי דגם מיה |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `elegant-baby`, `newborn-clothing`, `summer-baby-wear` |
| proposed_new_tags | `type-bodysuit` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `elegant-baby`, `newborn-clothing`, `summer-baby-wear`, `type-bodysuit` |
| proposed_type | `type-bodysuit` |
| type_source | handle |
| type_keyword | `bodysuit` |
| type_conf | 0.90 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'bodysuit' in handle (conf=0.90) |
| risk_level | LOW |
| confidence | 0.90 |
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [17] `9605503451449` — סרבל ללא שרוולים לתינוק

| Field | Value |
|-------|-------|
| product_id | `9605503451449` |
| title | סרבל ללא שרוולים לתינוק |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-romper`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-bodysuit`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-romper`, `everyday-baby-wear`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `type-bodysuit` |
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
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [18] `9687502422329` — סריג דובי דגם אריאל

| Field | Value |
|-------|-------|
| product_id | `9687502422329` |
| title | סריג דובי דגם אריאל |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-bodysuit`, `gender-boy` |
| final_tags_after_merge | `gender-boy`, `type-bodysuit`, `אוברול` |
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
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [19] `9687653056825` — שלוש חליפות בייבי  דגם אנה

| Field | Value |
|-------|-------|
| product_id | `9687653056825` |
| title | שלוש חליפות בייבי  דגם אנה |
| status | active |
| current_tags_count | 5 |
| current_tags | `baby-gift`, `baby-set`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-bodysuit`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `everyday-baby-wear`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `type-bodysuit` |
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
| month_normalization_needed | ✅ NO |
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

---

### [20] `9096606056761` — חליפת ג׳ינס וחמניות- גיילוס

| Field | Value |
|-------|-------|
| product_id | `9096606056761` |
| title | חליפת ג׳ינס וחמניות- גיילוס |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-suit`, `denim-baby`, `denim-style-baby`, `everyday-baby-wear`, `newborn-clothing` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `baby-gift`, `baby-suit`, `denim-baby`, `denim-style-baby`, `everyday-baby-wear`, `newborn-clothing`, `type-set` |
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
| reason_selected | type-source=title, conf=0.88, kw='חליפת', no false-positive flags, no shoe title, active product, not in batch1/2/3/4 |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS
- not_in_batch1234_check: ✅ PASS

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
| Not in Batch 1/2/3/4 | ✅ PASS |
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

**READY_FOR_PHASE7C_BATCH5_T3_APPROVAL**

✅ 20 SAFE candidates selected.
All safety checks PASS. No age-* tags. No type collision. No forbidden tags.
No overlap with Batch 1/2/3/4 written products. 0 product(s) need Hebrew month normalization in live stage.
Next step: request T3 approval from Ayal → Phase 7C Batch 5 live.

---

*Generated by scripts/phase7c_batch5_plan.py*