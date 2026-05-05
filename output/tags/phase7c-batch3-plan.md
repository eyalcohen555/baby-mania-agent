# Phase 7C Batch 3 — Read-Only Tagging Plan

## MODE
READ-ONLY PLANNING. No Shopify writes.

**Timestamp:** 2026-05-05T21:24:42.692147+00:00  
**Shopify writes:** NONE — GET only  

---

## 1. Selection Summary

| Item | Count |
|------|-------|
| Active products fetched | 393 |
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

- Already tagged with `type-*`: excluded
- Shoe/sandal/sneaker title keyword: excluded
- False-positive keyword (מגבת/תיק/שמיכה/towel/bag/blanket): excluded
- Low confidence (< type min_conf): excluded
- Non-preferred types (hat/coat/pants/top/swimwear): excluded
- REVIEW_ONLY: excluded (not in SAFE pool)

---

## 3. Per-Product Evidence

### [01] `9864947827001` — אוברול חגיגי דגם אנה

| Field | Value |
|-------|-------|
| product_id | `9864947827001` |
| title | אוברול חגיגי דגם אנה |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-dress`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-dress`, `אוברול` |
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
| reason_selected | type-source=handle, conf=0.90, kw='dress', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [02] `9179136426297` — שמלת ורדים חגיגית אלגנטית מלאה בסטייל - קיילי

| Field | Value |
|-------|-------|
| product_id | `9179136426297` |
| title | שמלת ורדים חגיגית אלגנטית מלאה בסטייל - קיילי |
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
| reason_selected | type-source=title, conf=0.90, kw='שמלת', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [03] `9179151794489` — שמלת טול חגיגית - אוריאן

| Field | Value |
|-------|-------|
| product_id | `9179151794489` |
| title | שמלת טול חגיגית - אוריאן |
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
| reason_selected | type-source=title, conf=0.90, kw='שמלת', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [04] `9179137048889` — שמלת כותנה חגיגית - אלין

| Field | Value |
|-------|-------|
| product_id | `9179137048889` |
| title | שמלת כותנה חגיגית - אלין |
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
| reason_selected | type-source=title, conf=0.90, kw='שמלת', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [05] `9179147829561` — שמלת כותנה קיצית עם טקסטורה - יעל

| Field | Value |
|-------|-------|
| product_id | `9179147829561` |
| title | שמלת כותנה קיצית עם טקסטורה - יעל |
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
| reason_selected | type-source=title, conf=0.90, kw='שמלת', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [06] `9687596663097` — אוברול סריג מתוק לתינוקות דגם שוהם

| Field | Value |
|-------|-------|
| product_id | `9687596663097` |
| title | אוברול סריג מתוק לתינוקות דגם שוהם |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-set`, `אוברול` |
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
| reason_selected | type-source=handle, conf=0.88, kw='set', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [07] `9724813443385` — אוברול סריג פסים דגם רפאל

| Field | Value |
|-------|-------|
| product_id | `9724813443385` |
| title | אוברול סריג פסים דגם רפאל |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-set`, `אוברול` |
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
| reason_selected | type-source=handle, conf=0.88, kw='outfit', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [08] `9179138457913` — אוברול קיצי מתוק סטייל קז'ואל - יואבי

| Field | Value |
|-------|-------|
| product_id | `9179138457913` |
| title | אוברול קיצי מתוק סטייל קז'ואל - יואבי |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
| proposed_type | `type-set` |
| type_source | handle |
| type_keyword | `סט` |
| type_conf | 0.88 |
| proposed_gender | `—` |
| gender_source | — |
| gender_keyword | `—` |
| gender_conf | 0.00 |
| proposed_occs | `—` |
| source_trace | type matched 'סט' in handle (conf=0.88) |
| risk_level | LOW |
| confidence | 0.88 |
| reason_selected | type-source=handle, conf=0.88, kw='סט', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [09] `9673732292921` — חליפה 3 חלקים מבית בייבי מניה דגם אריאל

| Field | Value |
|-------|-------|
| product_id | `9673732292921` |
| title | חליפה 3 חלקים מבית בייבי מניה דגם אריאל |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-set`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `gender-girl`, `neutral-baby-outfit`, `newborn-clothing`, `type-set` |
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
| reason_selected | type-source=title, conf=0.88, kw='חליפה', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [10] `9179156742457` — חליפה מסוגננת פרחונית - מיקה

| Field | Value |
|-------|-------|
| product_id | `9179156742457` |
| title | חליפה מסוגננת פרחונית - מיקה |
| status | active |
| current_tags_count | 0 |
| current_tags | `` |
| proposed_new_tags | `type-set` |
| final_tags_after_merge | `type-set` |
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
| reason_selected | type-source=title, conf=0.88, kw='חליפה', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [11] `9858268430649` — אוברול גינס מהמם דגם רוית

| Field | Value |
|-------|-------|
| product_id | `9858268430649` |
| title | אוברול גינס מהמם דגם רוית |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-romper`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-romper`, `אוברול` |
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
| reason_selected | type-source=handle, conf=0.88, kw='romper', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [12] `9179176141113` — אוברול דובונים מכותנה - ליאור

| Field | Value |
|-------|-------|
| product_id | `9179176141113` |
| title | אוברול דובונים מכותנה - ליאור |
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
| reason_selected | type-source=title, conf=0.88, kw='אוברול', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [13] `9179161231673` — אוברול כותנה קיצי - נועה

| Field | Value |
|-------|-------|
| product_id | `9179161231673` |
| title | אוברול כותנה קיצי - נועה |
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
| reason_selected | type-source=title, conf=0.88, kw='אוברול', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [14] `10005779743033` — אוברול לתינוקות דגם סטייסי

| Field | Value |
|-------|-------|
| product_id | `10005779743033` |
| title | אוברול לתינוקות דגם סטייסי |
| status | active |
| current_tags_count | 1 |
| current_tags | `אוברול` |
| proposed_new_tags | `type-romper`, `gender-girl` |
| final_tags_after_merge | `gender-girl`, `type-romper`, `אוברול` |
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
| reason_selected | type-source=handle, conf=0.88, kw='romper', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [15] `9096607138105` — אוברול מכופתרת

| Field | Value |
|-------|-------|
| product_id | `9096607138105` |
| title | אוברול מכופתרת |
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
| reason_selected | type-source=title, conf=0.88, kw='אוברול', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [16] `9688965087545` — אוברול דוב מתוק דגם אייל

| Field | Value |
|-------|-------|
| product_id | `9688965087545` |
| title | אוברול דוב מתוק דגם אייל |
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
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [17] `9719189635385` — אוברול דובי אם רגלית דגם אוריאל

| Field | Value |
|-------|-------|
| product_id | `9719189635385` |
| title | אוברול דובי אם רגלית דגם אוריאל |
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
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=handle, kw='boy', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [18] `9717957525817` — אוברול דובי דגם דניאל

| Field | Value |
|-------|-------|
| product_id | `9717957525817` |
| title | אוברול דובי דגם דניאל |
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
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [19] `10005779841337` — אוברול חורפי לתינוקות דגם אנגל

| Field | Value |
|-------|-------|
| product_id | `10005779841337` |
| title | אוברול חורפי לתינוקות דגם אנגל |
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
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=handle, kw='girl', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

---

### [20] `9688885952825` — חליפה מכנס וחולצה לבנות דגם אנה

| Field | Value |
|-------|-------|
| product_id | `9688885952825` |
| title | חליפה מכנס וחולצה לבנות דגם אנה |
| status | active |
| current_tags_count | 6 |
| current_tags | `baby-gift`, `baby-top`, `everyday-baby-wear`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing` |
| proposed_new_tags | `type-bodysuit`, `gender-girl` |
| final_tags_after_merge | `baby-gift`, `baby-top`, `everyday-baby-wear`, `gender-girl`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing`, `type-bodysuit` |
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
| reason_selected | type-source=handle, conf=0.90, kw='bodysuit', gender-source=title, kw='בנות', no false-positive flags, no shoe title, active product |
| safety_flags | NONE ✅ |

**Checks:**
- allowed_values_check: ✅ PASS
- forbidden_tags_check: ✅ PASS
- age_tags_check: ✅ PASS
- type_collision_check: ✅ PASS
- gender_collision_check: ✅ PASS
- shoe_title_check: ✅ PASS
- false_positive_check: ✅ PASS

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

**READY_FOR_PHASE7C_BATCH3_T3_APPROVAL**

✅ 20 SAFE candidates selected.
All safety checks PASS. No age-* tags. No type collision. No forbidden tags.
Next step: request T3 approval from Ayal → Phase 7C Batch 3 live.

---

*Generated by scripts/phase7c_batch3_plan.py*