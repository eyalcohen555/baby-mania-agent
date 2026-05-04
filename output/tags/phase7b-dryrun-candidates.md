# Layer 7 — Phase 7B — Dry Run Report
**תאריך:** 2026-05-04
**Phase:** 7B — Dry Run Only — אין live
**QA Contract:** layer7-live-tagging-qa-contract.md — ACTIVE

---

## 1. מצב מערכת

| פרמטר | ערך |
|-------|-----|
| Phase 6 batch 1+2 | COMPLETE + PASS |
| Phase 7A batch 1+2 | COMPLETE + PASS |
| Shopify live כרגע | YES — **19 products** |
| QA Contract | ACTIVE |
| Phase 8 collections | BLOCKED — need 50+ from 4+ types |
| Shopify writes in this phase | **NO — dry run only** |

## 2. סיכום סקירה

| מדד | ערך |
|-----|-----|
| מוצרים שנמשכו מ-Shopify | 393 |
| pool לאחר סינון (untapped) | 374 |
| מוצרים שנוקדו | 374 |
| **SAFE_FOR_PHASE7B** (כלל ה-pool) | **222** |
| REVIEW_ONLY | 108 |
| REJECT | 44 |
| הערה | 2 מוצרי נעל תויגו type-dress בטעות (handle מכיל 'dress-shoes') — תוקן בreport זה |

## 3. פילוח SAFE לפי type (pool מלא)

| type | כמות SAFE |
|------|----------|
| type-set | 97 |
| type-romper | 56 |
| type-dress | 27 |
| type-shoes | 14 |
| type-bodysuit | 9 |
| type-hat | 7 |
| type-sandals | 4 |
| type-swimwear | 3 |
| type-coat | 3 |
| type-top | 1 |
| type-pants | 1 |

## 4. REJECT — סיבות

| סיבה | תיאור |
|------|-------|
| EU_SHOE_SIZE_BLOCKER | נעלי תינוק עם EU sizes בלבד (19/20/21/22/23) — אין mapping מאושר |
| NO_TYPE | title/handle/tags לא כוללים מילת מפתח ברורה לtype |
| **סה"כ REJECT בpool** | **44** |

## 5. REVIEW_ONLY — גורמים

| גורם | תיאור |
|------|-------|
| type-* לא זוהה | title/handle/tags לא מכילים מילת מפתח ברורה |
| confidence נמוך | type או gender conf < 0.85 |
| TYPE_MISMATCH | handle מכיל 'dress' אבל title אומר 'סנדל/נעל' — 2 מוצרים |
| size חסרה | אין variant sizes ואין title size |

## 6. טבלת QA — 40 מועמדים SAFE

| # | product_id | title | type | proposed_count | forbidden | allowed | verdict |
|---|-----------|-------|------|---------------|-----------|---------|---------|
| 1 | 9606691324217 | שמלה אופנתית קלאסית לאירועים לתינוקת | type-dress | 4 | PASS | PASS | SAFE_FOR_PHASE7B |
| 2 | 9895864369465 | שמלה חגיגית פרחונית דגם מורן | type-dress | 10 | PASS | PASS | SAFE_FOR_PHASE7B |
| 3 | 9892557848889 | שמלה כחולה כהה אם דוגמא קלאסית דגם אוראל | type-dress | 4 | PASS | PASS | SAFE_FOR_PHASE7B |
| 4 | 9179146256697 | שמלה נסיכותית מפתשן וכותנה, מלאה בסטייל - נוע... | type-dress | 2 | PASS | PASS | SAFE_FOR_PHASE7B |
| 5 | 9606694175033 | שמלה קיצית עם מלמלה לבנות | type-dress | 2 | PASS | PASS | SAFE_FOR_PHASE7B |
| 6 | 10190522908985 | Summer Toddler Kids Stripe Bodysuit Boys Loos... | type-bodysuit | 5 | PASS | PASS | SAFE_FOR_PHASE7B |
| 7 | 9179165753657 | בגד גוף כותנה טטרה - פריחת האביב | type-bodysuit | 3 | PASS | PASS | SAFE_FOR_PHASE7B |
| 8 | 9179154612537 | בגד גוף כיווצים - גאיה | type-bodysuit | 1 | PASS | PASS | SAFE_FOR_PHASE7B |
| 9 | 9179152154937 | בגד גוף מלמלות - קיטי | type-bodysuit | 1 | PASS | PASS | SAFE_FOR_PHASE7B |
| 10 | 9179167129913 | בגד גוף מלמלות וכיווצים פרחוני - שיילי | type-bodysuit | 2 | PASS | PASS | SAFE_FOR_PHASE7B |
| 11 | 10190522941753 | 2Pcs Baby Boys' Sports and Leisure Set lapel ... | type-set | 8 | PASS | PASS | SAFE_FOR_PHASE7B |
| 12 | 10190523203897 | Boys Khaki Letter Print Half Zip Hooded 2Pcs ... | type-set | 3 | PASS | PASS | SAFE_FOR_PHASE7B |
| 13 | 10190523105593 | Boys' Summer Knitted Set, Contrast Color Shor... | type-set | 4 | PASS | PASS | SAFE_FOR_PHASE7B |
| 14 | 10190523236665 | Infant Baby Boys Short Sets Patchwork Sleevel... | type-set | 3 | PASS | PASS | SAFE_FOR_PHASE7B |
| 15 | 10190522843449 | Kids Baby Boy Summer Clothes Sets Casual Lett... | type-set | 3 | PASS | PASS | SAFE_FOR_PHASE7B |
| 16 | 10029649002809 | Alure™ Baby | type-romper | 2 | PASS | PASS | SAFE_FOR_PHASE7B |
| 17 | 10029648970041 | LumiBear™ חליפת פרמיום לחורף | type-romper | 10 | PASS | PASS | SAFE_FOR_PHASE7B |
| 18 | 10029649101113 | LUMI™  – אוברול נוחות יוקרתי לתינוקות | type-romper | 1 | PASS | PASS | SAFE_FOR_PHASE7B |
| 19 | 9657091293497 | WarmNest™– אוברול חורף מחבק לתינוקות | type-romper | 6 | PASS | PASS | SAFE_FOR_PHASE7B |
| 20 | 9687596728633 | אוברול Leopard Cozy | type-romper | 6 | PASS | PASS | SAFE_FOR_PHASE7B |
| 21 | 9606694338873 | מכנסי קורדרוי אופנתיים לתינוקות | type-pants | 4 | PASS | PASS | SAFE_FOR_PHASE7B |
| 22 | 9096605827385 | חולצת קז'ואל שרוול ארוך | type-top | 4 | PASS | PASS | SAFE_FOR_PHASE7B |
| 23 | 9179141308729 | כובע בייסבול דובוני לתינוקות מעוצב ומהמם עשוי... | type-hat | 4 | PASS | PASS | SAFE_FOR_PHASE7B |
| 24 | 9606864666937 | כובע בייסבול רך לתינוק | type-hat | 2 | PASS | PASS | SAFE_FOR_PHASE7B |
| 25 | 9179140489529 | כובע כותנה סטייל פנמה קייצי לתינוקות | type-hat | 3 | PASS | PASS | SAFE_FOR_PHASE7B |
| 26 | 10024854847801 | כובע צמר מתנה | type-hat | 2 | PASS | PASS | SAFE_FOR_PHASE7B |
| 27 | 9179140915513 | כובע קייצי רך ונעים מכותנה מתאים לתנוקות בגיל... | type-hat | 3 | PASS | PASS | SAFE_FOR_PHASE7B |
| 28 | 9179162083641 | בגד ים פרחוני - לייה | type-swimwear | 2 | PASS | PASS | SAFE_FOR_PHASE7B |
| 29 | 9179162804537 | בגד ים שני חלקים - יסמין | type-swimwear | 1 | PASS | PASS | SAFE_FOR_PHASE7B |
| 30 | 9179164344633 | בגד ים שני חלקים פרחוני - קוקומלון | type-swimwear | 2 | PASS | PASS | SAFE_FOR_PHASE7B |
| 31 | 9731768713529 | מעיל אופנתי לבנות – דגם שיראל | type-coat | 4 | PASS | PASS | SAFE_FOR_PHASE7B |
| 32 | 9673730359609 | מעיל חורף צמר דגם שנאל | type-coat | 4 | PASS | PASS | SAFE_FOR_PHASE7B |
| 33 | 9688976228665 | מעיל קורדרוי מחמם מאוד דגם אליה | type-coat | 6 | PASS | PASS | SAFE_FOR_PHASE7B |

## 7. פרטי מועמדים — 40 SAFE מלא

### [1] 9606691324217 — שמלה אופנתית קלאסית לאירועים לתינוקת

**status:** active
**current_tags (5):** `baby-dress`, `baby-gift`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing`
**proposed_new_tags (4):** `type-dress`, `occ-gift`, `occ-everyday`, `gender-girl`

**proposed_new_tags_with_source:**
  - `type-dress` ← title (conf=0.95, rule=CAT-A)
  - `occ-gift` ← existing_tag (conf=0.88, rule=CAT-E)
  - `occ-everyday` ← existing_tag (conf=0.85, rule=CAT-E)
  - `gender-girl` ← handle (conf=0.90, rule=CAT-F)

**type_source_proof:** `type-dress` ← title (conf=0.95, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-girl` ← handle (conf=0.90)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [2] 9895864369465 — שמלה חגיגית פרחונית דגם מורן

**status:** active
**current_tags (6):** `baby-dress`, `baby-gift`, `baby-shower-gift`, `everyday-baby-wear`, `floral-baby`, `newborn-clothing`
**proposed_new_tags (10):** `type-dress`, `size-3-6m`, `size-6-9m`, `size-9-12m`, `size-12-18m`, `size-18-24m`, `occ-gift`, `occ-everyday`, `gender-girl`, `style-floral`

**proposed_new_tags_with_source:**
  - `type-dress` ← title (conf=0.95, rule=CAT-A)
  - `size-3-6m` ← variant:3-6M→size-3-6m (conf=0.92, rule=CAT-B)
  - `size-6-9m` ← variant:6-9M→size-6-9m (conf=0.92, rule=CAT-B)
  - `size-9-12m` ← variant:9-12M→size-9-12m (conf=0.92, rule=CAT-B)
  - `size-12-18m` ← variant:12-18M→size-12-18m (conf=0.92, rule=CAT-B)
  - `size-18-24m` ← variant:18-24M→size-18-24m (conf=0.92, rule=CAT-B)
  - `occ-gift` ← existing_tag (conf=0.88, rule=CAT-E)
  - `occ-everyday` ← existing_tag (conf=0.85, rule=CAT-E)
  - `gender-girl` ← handle (conf=0.90, rule=CAT-F)
  - `style-floral` ← title (conf=0.87, rule=CAT-G)

**type_source_proof:** `type-dress` ← title (conf=0.95, min=0.9)
**size_source_proof:** `3-6M`→`size-3-6m`, `6-9M`→`size-6-9m`, `9-12M`→`size-9-12m`, `12-18M`→`size-12-18m`, `18-24M`→`size-18-24m`
**gender_proof:** `gender-girl` ← handle (conf=0.90)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [3] 9892557848889 — שמלה כחולה כהה אם דוגמא קלאסית דגם אוראל

**status:** active
**current_tags (5):** `baby-dress`, `baby-gift`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing`
**proposed_new_tags (4):** `type-dress`, `occ-gift`, `occ-everyday`, `gender-girl`

**proposed_new_tags_with_source:**
  - `type-dress` ← title (conf=0.95, rule=CAT-A)
  - `occ-gift` ← existing_tag (conf=0.88, rule=CAT-E)
  - `occ-everyday` ← existing_tag (conf=0.85, rule=CAT-E)
  - `gender-girl` ← handle (conf=0.90, rule=CAT-F)

**type_source_proof:** `type-dress` ← title (conf=0.95, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-girl` ← handle (conf=0.90)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [4] 9179146256697 — שמלה נסיכותית מפתשן וכותנה, מלאה בסטייל - נועה

**status:** active
**current_tags (0):** —
**proposed_new_tags (2):** `type-dress`, `fabric-cotton`

**proposed_new_tags_with_source:**
  - `type-dress` ← title (conf=0.95, rule=CAT-A)
  - `fabric-cotton` ← title (conf=0.92, rule=CAT-D)

**type_source_proof:** `type-dress` ← title (conf=0.95, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** no gender tag (not inferred from color)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [5] 9606694175033 — שמלה קיצית עם מלמלה לבנות

**status:** active
**current_tags (0):** —
**proposed_new_tags (2):** `type-dress`, `gender-girl`

**proposed_new_tags_with_source:**
  - `type-dress` ← title (conf=0.95, rule=CAT-A)
  - `gender-girl` ← title (conf=0.93, rule=CAT-F)

**type_source_proof:** `type-dress` ← title (conf=0.95, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-girl` ← title (conf=0.93)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [6] 10190522908985 — Summer Toddler Kids Stripe Bodysuit Boys Loose Turndown Collar Jumpsuit Girls Baby Thin Crawlwear Onesie Clothes One Piece

**status:** active
**current_tags (0):** —
**proposed_new_tags (5):** `type-bodysuit`, `size-6-9m`, `size-3-6m`, `season-summer`, `gender-girl`

**proposed_new_tags_with_source:**
  - `type-bodysuit` ← title (conf=0.95, rule=CAT-A)
  - `size-6-9m` ← variant:6-9m→size-6-9m (conf=0.92, rule=CAT-B)
  - `size-3-6m` ← variant:3-6m→size-3-6m (conf=0.92, rule=CAT-B)
  - `season-summer` ← title (conf=0.88, rule=CAT-C)
  - `gender-girl` ← title (conf=0.93, rule=CAT-F)

**type_source_proof:** `type-bodysuit` ← title (conf=0.95, min=0.9)
**size_source_proof:** `6-9m`→`size-6-9m`, `3-6m`→`size-3-6m`
**gender_proof:** `gender-girl` ← title (conf=0.93)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [7] 9179165753657 — בגד גוף כותנה טטרה - פריחת האביב

**status:** active
**current_tags (0):** —
**proposed_new_tags (3):** `type-bodysuit`, `season-spring-fall`, `fabric-cotton`

**proposed_new_tags_with_source:**
  - `type-bodysuit` ← title (conf=0.95, rule=CAT-A)
  - `season-spring-fall` ← title (conf=0.85, rule=CAT-C)
  - `fabric-cotton` ← title (conf=0.92, rule=CAT-D)

**type_source_proof:** `type-bodysuit` ← title (conf=0.95, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** no gender tag (not inferred from color)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [8] 9179154612537 — בגד גוף כיווצים - גאיה

**status:** active
**current_tags (0):** —
**proposed_new_tags (1):** `type-bodysuit`

**proposed_new_tags_with_source:**
  - `type-bodysuit` ← title (conf=0.95, rule=CAT-A)

**type_source_proof:** `type-bodysuit` ← title (conf=0.95, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** no gender tag (not inferred from color)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [9] 9179152154937 — בגד גוף מלמלות - קיטי

**status:** active
**current_tags (0):** —
**proposed_new_tags (1):** `type-bodysuit`

**proposed_new_tags_with_source:**
  - `type-bodysuit` ← title (conf=0.95, rule=CAT-A)

**type_source_proof:** `type-bodysuit` ← title (conf=0.95, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** no gender tag (not inferred from color)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [10] 9179167129913 — בגד גוף מלמלות וכיווצים פרחוני - שיילי

**status:** active
**current_tags (0):** —
**proposed_new_tags (2):** `type-bodysuit`, `style-floral`

**proposed_new_tags_with_source:**
  - `type-bodysuit` ← title (conf=0.95, rule=CAT-A)
  - `style-floral` ← title (conf=0.87, rule=CAT-G)

**type_source_proof:** `type-bodysuit` ← title (conf=0.95, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** no gender tag (not inferred from color)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [11] 10190522941753 — 2Pcs Baby Boys' Sports and Leisure Set lapel Color blocked Short Sleeves and Shorts for 0-3 Year Toddlers Baby Boys Summer Set

**status:** active
**current_tags (0):** —
**proposed_new_tags (8):** `type-set`, `size-12-18m`, `size-9-12m`, `size-6-9m`, `size-3-6m`, `size-18-24m`, `season-summer`, `gender-boy`

**proposed_new_tags_with_source:**
  - `type-set` ← title (conf=0.93, rule=CAT-A)
  - `size-12-18m` ← variant:12-18M→size-12-18m (conf=0.92, rule=CAT-B)
  - `size-9-12m` ← variant:9-12M→size-9-12m (conf=0.92, rule=CAT-B)
  - `size-6-9m` ← variant:6-9M→size-6-9m (conf=0.92, rule=CAT-B)
  - `size-3-6m` ← variant:3-6M→size-3-6m (conf=0.92, rule=CAT-B)
  - `size-18-24m` ← variant:18-24M→size-18-24m (conf=0.92, rule=CAT-B)
  - `season-summer` ← title (conf=0.88, rule=CAT-C)
  - `gender-boy` ← title (conf=0.93, rule=CAT-F)

**type_source_proof:** `type-set` ← title (conf=0.93, min=0.9)
**size_source_proof:** `12-18M`→`size-12-18m`, `9-12M`→`size-9-12m`, `6-9M`→`size-6-9m`, `3-6M`→`size-3-6m`, `18-24M`→`size-18-24m`
**gender_proof:** `gender-boy` ← title (conf=0.93)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [12] 10190523203897 — Boys Khaki Letter Print Half Zip Hooded 2Pcs Summer Set, Short Sleeve Hoodie + Shorts, Kids Casual Outfit 3-12Y

**status:** active
**current_tags (0):** —
**proposed_new_tags (3):** `type-set`, `season-summer`, `gender-boy`

**proposed_new_tags_with_source:**
  - `type-set` ← title (conf=0.93, rule=CAT-A)
  - `season-summer` ← title (conf=0.88, rule=CAT-C)
  - `gender-boy` ← title (conf=0.93, rule=CAT-F)

**type_source_proof:** `type-set` ← title (conf=0.93, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-boy` ← title (conf=0.93)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [13] 10190523105593 — Boys' Summer Knitted Set, Contrast Color Short-Sleeved With Pocket and Shorts Clothes Sets, Children Comfort Soft 2-Piece Set

**status:** active
**current_tags (0):** —
**proposed_new_tags (4):** `type-set`, `season-summer`, `fabric-knit`, `gender-boy`

**proposed_new_tags_with_source:**
  - `type-set` ← title (conf=0.93, rule=CAT-A)
  - `season-summer` ← title (conf=0.88, rule=CAT-C)
  - `fabric-knit` ← title (conf=0.88, rule=CAT-D)
  - `gender-boy` ← title (conf=0.93, rule=CAT-F)

**type_source_proof:** `type-set` ← title (conf=0.93, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-boy` ← title (conf=0.93)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [14] 10190523236665 — Infant Baby Boys Short Sets Patchwork Sleeveless Vest Tops with Pocket + Shorts 2pcs Summer Outfits for Toddler 6-36M

**status:** active
**current_tags (0):** —
**proposed_new_tags (3):** `type-set`, `season-summer`, `gender-boy`

**proposed_new_tags_with_source:**
  - `type-set` ← title (conf=0.93, rule=CAT-A)
  - `season-summer` ← title (conf=0.88, rule=CAT-C)
  - `gender-boy` ← title (conf=0.93, rule=CAT-F)

**type_source_proof:** `type-set` ← title (conf=0.93, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-boy` ← title (conf=0.93)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [15] 10190522843449 — Kids Baby Boy Summer Clothes Sets Casual Letters Short Sleeve O Neck T-Shirt and Elastic Band Shorts Infants Boys Activewear

**status:** active
**current_tags (0):** —
**proposed_new_tags (3):** `type-set`, `season-summer`, `gender-boy`

**proposed_new_tags_with_source:**
  - `type-set` ← title (conf=0.93, rule=CAT-A)
  - `season-summer` ← title (conf=0.88, rule=CAT-C)
  - `gender-boy` ← title (conf=0.93, rule=CAT-F)

**type_source_proof:** `type-set` ← title (conf=0.93, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-boy` ← title (conf=0.93)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [16] 10029649002809 — Alure™ Baby

**status:** active
**current_tags (0):** —
**proposed_new_tags (2):** `type-romper`, `gender-girl`

**proposed_new_tags_with_source:**
  - `type-romper` ← handle (conf=0.90, rule=CAT-A)
  - `gender-girl` ← handle (conf=0.90, rule=CAT-F)

**type_source_proof:** `type-romper` ← handle (conf=0.90, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-girl` ← handle (conf=0.90)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [17] 10029648970041 — LumiBear™ חליפת פרמיום לחורף

**status:** active
**current_tags (6):** `baby-gift`, `baby-shower-gift`, `baby-suit`, `neutral-baby-outfit`, `newborn-clothing`, `winter-baby-wear`
**proposed_new_tags (10):** `type-romper`, `size-3-6m`, `size-6-9m`, `size-18-24m`, `size-9-12m`, `size-12-18m`, `season-winter`, `occ-gift`, `gender-boy`, `style-teddy`

**proposed_new_tags_with_source:**
  - `type-romper` ← handle (conf=0.90, rule=CAT-A)
  - `size-3-6m` ← variant:3-6M→size-3-6m (conf=0.92, rule=CAT-B)
  - `size-6-9m` ← variant:6-9M→size-6-9m (conf=0.92, rule=CAT-B)
  - `size-18-24m` ← variant:18-24M→size-18-24m (conf=0.92, rule=CAT-B)
  - `size-9-12m` ← variant:9-12M→size-9-12m (conf=0.92, rule=CAT-B)
  - `size-12-18m` ← variant:12-18M→size-12-18m (conf=0.92, rule=CAT-B)
  - `season-winter` ← title (conf=0.88, rule=CAT-C)
  - `occ-gift` ← existing_tag (conf=0.88, rule=CAT-E)
  - `gender-boy` ← handle (conf=0.90, rule=CAT-F)
  - `style-teddy` ← title (conf=0.87, rule=CAT-G)

**type_source_proof:** `type-romper` ← handle (conf=0.90, min=0.9)
**size_source_proof:** `3-6M`→`size-3-6m`, `6-9M`→`size-6-9m`, `18-24M`→`size-18-24m`, `9-12M`→`size-9-12m`, `12-18M`→`size-12-18m`
**gender_proof:** `gender-boy` ← handle (conf=0.90)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [18] 10029649101113 — LUMI™  – אוברול נוחות יוקרתי לתינוקות

**status:** active
**current_tags (1):** `אוברול`
**proposed_new_tags (1):** `type-romper`

**proposed_new_tags_with_source:**
  - `type-romper` ← title (conf=0.95, rule=CAT-A)

**type_source_proof:** `type-romper` ← title (conf=0.95, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** no gender tag (not inferred from color)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [19] 9657091293497 — WarmNest™– אוברול חורף מחבק לתינוקות

**status:** active
**current_tags (4):** `0-3 חודש`, `12-18 חודש`, `6-12 חודש`, `אוברול`
**proposed_new_tags (6):** `type-romper`, `size-6-9m`, `size-9-12m`, `size-12-18m`, `season-winter`, `gender-girl`

**proposed_new_tags_with_source:**
  - `type-romper` ← title (conf=0.95, rule=CAT-A)
  - `size-6-9m` ← variant:6-9M→size-6-9m (conf=0.92, rule=CAT-B)
  - `size-9-12m` ← variant:9-12M→size-9-12m (conf=0.92, rule=CAT-B)
  - `size-12-18m` ← variant:12-18M→size-12-18m (conf=0.92, rule=CAT-B)
  - `season-winter` ← title (conf=0.88, rule=CAT-C)
  - `gender-girl` ← handle (conf=0.90, rule=CAT-F)

**type_source_proof:** `type-romper` ← title (conf=0.95, min=0.9)
**size_source_proof:** `6-9M`→`size-6-9m`, `9-12M`→`size-9-12m`, `12-18M`→`size-12-18m`
**gender_proof:** `gender-girl` ← handle (conf=0.90)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [20] 9687596728633 — אוברול Leopard Cozy

**status:** active
**current_tags (1):** `אוברול`
**proposed_new_tags (6):** `type-romper`, `size-3-6m`, `size-6-9m`, `size-9-12m`, `size-12-18m`, `gender-girl`

**proposed_new_tags_with_source:**
  - `type-romper` ← title (conf=0.95, rule=CAT-A)
  - `size-3-6m` ← variant:3-6M→size-3-6m (conf=0.92, rule=CAT-B)
  - `size-6-9m` ← variant:6-9M→size-6-9m (conf=0.92, rule=CAT-B)
  - `size-9-12m` ← variant:9-12M→size-9-12m (conf=0.92, rule=CAT-B)
  - `size-12-18m` ← variant:12-18M→size-12-18m (conf=0.92, rule=CAT-B)
  - `gender-girl` ← handle (conf=0.90, rule=CAT-F)

**type_source_proof:** `type-romper` ← title (conf=0.95, min=0.9)
**size_source_proof:** `3-6M`→`size-3-6m`, `6-9M`→`size-6-9m`, `9-12M`→`size-9-12m`, `12-18M`→`size-12-18m`
**gender_proof:** `gender-girl` ← handle (conf=0.90)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [21] 9606694338873 — מכנסי קורדרוי אופנתיים לתינוקות

**status:** active
**current_tags (6):** `baby-gift`, `baby-pants`, `corduroy-baby`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing`
**proposed_new_tags (4):** `type-pants`, `occ-gift`, `occ-everyday`, `gender-girl`

**proposed_new_tags_with_source:**
  - `type-pants` ← title (conf=0.92, rule=CAT-A)
  - `occ-gift` ← existing_tag (conf=0.88, rule=CAT-E)
  - `occ-everyday` ← existing_tag (conf=0.85, rule=CAT-E)
  - `gender-girl` ← handle (conf=0.90, rule=CAT-F)

**type_source_proof:** `type-pants` ← title (conf=0.92, min=0.85)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-girl` ← handle (conf=0.90)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [22] 9096605827385 — חולצת קז'ואל שרוול ארוך

**status:** active
**current_tags (5):** `baby-gift`, `baby-top`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing`
**proposed_new_tags (4):** `type-top`, `occ-gift`, `occ-everyday`, `gender-neutral`

**proposed_new_tags_with_source:**
  - `type-top` ← title (conf=0.90, rule=CAT-A)
  - `occ-gift` ← existing_tag (conf=0.88, rule=CAT-E)
  - `occ-everyday` ← existing_tag (conf=0.85, rule=CAT-E)
  - `gender-neutral` ← existing_tag (conf=0.87, rule=CAT-F)

**type_source_proof:** `type-top` ← title (conf=0.90, min=0.85)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-neutral` ← existing_tag (conf=0.87)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [23] 9179141308729 — כובע בייסבול דובוני לתינוקות מעוצב ומהמם עשוי מכותנה, מתאים לבנים ולבנות בגילאי 3-12 חודשים

**status:** active
**current_tags (0):** —
**proposed_new_tags (4):** `type-hat`, `fabric-cotton`, `gender-girl`, `style-teddy`

**proposed_new_tags_with_source:**
  - `type-hat` ← title (conf=0.92, rule=CAT-A)
  - `fabric-cotton` ← title (conf=0.92, rule=CAT-D)
  - `gender-girl` ← title (conf=0.93, rule=CAT-F)
  - `style-teddy` ← title (conf=0.87, rule=CAT-G)

**type_source_proof:** `type-hat` ← title (conf=0.92, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-girl` ← title (conf=0.93)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [24] 9606864666937 — כובע בייסבול רך לתינוק

**status:** active
**current_tags (0):** —
**proposed_new_tags (2):** `type-hat`, `gender-girl`

**proposed_new_tags_with_source:**
  - `type-hat` ← title (conf=0.92, rule=CAT-A)
  - `gender-girl` ← handle (conf=0.90, rule=CAT-F)

**type_source_proof:** `type-hat` ← title (conf=0.92, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-girl` ← handle (conf=0.90)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [25] 9179140489529 — כובע כותנה סטייל פנמה קייצי לתינוקות

**status:** active
**current_tags (0):** —
**proposed_new_tags (3):** `type-hat`, `season-summer`, `fabric-cotton`

**proposed_new_tags_with_source:**
  - `type-hat` ← title (conf=0.92, rule=CAT-A)
  - `season-summer` ← title (conf=0.88, rule=CAT-C)
  - `fabric-cotton` ← title (conf=0.92, rule=CAT-D)

**type_source_proof:** `type-hat` ← title (conf=0.92, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** no gender tag (not inferred from color)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [26] 10024854847801 — כובע צמר מתנה

**status:** active
**current_tags (1):** `gift`
**proposed_new_tags (2):** `type-hat`, `occ-gift`

**proposed_new_tags_with_source:**
  - `type-hat` ← title (conf=0.92, rule=CAT-A)
  - `occ-gift` ← existing_tag (conf=0.88, rule=CAT-E)

**type_source_proof:** `type-hat` ← title (conf=0.92, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** no gender tag (not inferred from color)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [27] 9179140915513 — כובע קייצי רך ונעים מכותנה מתאים לתנוקות בגילאי 0-12 חודשים

**status:** active
**current_tags (0):** —
**proposed_new_tags (3):** `type-hat`, `season-summer`, `fabric-cotton`

**proposed_new_tags_with_source:**
  - `type-hat` ← title (conf=0.92, rule=CAT-A)
  - `season-summer` ← title (conf=0.88, rule=CAT-C)
  - `fabric-cotton` ← title (conf=0.92, rule=CAT-D)

**type_source_proof:** `type-hat` ← title (conf=0.92, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** no gender tag (not inferred from color)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [28] 9179162083641 — בגד ים פרחוני - לייה

**status:** active
**current_tags (0):** —
**proposed_new_tags (2):** `type-swimwear`, `style-floral`

**proposed_new_tags_with_source:**
  - `type-swimwear` ← title (conf=0.93, rule=CAT-A)
  - `style-floral` ← title (conf=0.87, rule=CAT-G)

**type_source_proof:** `type-swimwear` ← title (conf=0.93, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** no gender tag (not inferred from color)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [29] 9179162804537 — בגד ים שני חלקים - יסמין

**status:** active
**current_tags (0):** —
**proposed_new_tags (1):** `type-swimwear`

**proposed_new_tags_with_source:**
  - `type-swimwear` ← title (conf=0.93, rule=CAT-A)

**type_source_proof:** `type-swimwear` ← title (conf=0.93, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** no gender tag (not inferred from color)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [30] 9179164344633 — בגד ים שני חלקים פרחוני - קוקומלון

**status:** active
**current_tags (0):** —
**proposed_new_tags (2):** `type-swimwear`, `style-floral`

**proposed_new_tags_with_source:**
  - `type-swimwear` ← title (conf=0.93, rule=CAT-A)
  - `style-floral` ← title (conf=0.87, rule=CAT-G)

**type_source_proof:** `type-swimwear` ← title (conf=0.93, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** no gender tag (not inferred from color)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [31] 9731768713529 — מעיל אופנתי לבנות – דגם שיראל

**status:** active
**current_tags (6):** `baby-coat`, `baby-gift`, `everyday-baby-wear`, `girls-clothing`, `neutral-baby-outfit`, `newborn-clothing`
**proposed_new_tags (4):** `type-coat`, `occ-gift`, `occ-everyday`, `gender-girl`

**proposed_new_tags_with_source:**
  - `type-coat` ← title (conf=0.93, rule=CAT-A)
  - `occ-gift` ← existing_tag (conf=0.88, rule=CAT-E)
  - `occ-everyday` ← existing_tag (conf=0.85, rule=CAT-E)
  - `gender-girl` ← title (conf=0.93, rule=CAT-F)

**type_source_proof:** `type-coat` ← title (conf=0.93, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-girl` ← title (conf=0.93)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [32] 9673730359609 — מעיל חורף צמר דגם שנאל

**status:** active
**current_tags (5):** `baby-coat`, `baby-gift`, `neutral-baby-outfit`, `newborn-clothing`, `winter-baby-wear`
**proposed_new_tags (4):** `type-coat`, `season-winter`, `occ-gift`, `gender-girl`

**proposed_new_tags_with_source:**
  - `type-coat` ← title (conf=0.93, rule=CAT-A)
  - `season-winter` ← title (conf=0.88, rule=CAT-C)
  - `occ-gift` ← existing_tag (conf=0.88, rule=CAT-E)
  - `gender-girl` ← handle (conf=0.90, rule=CAT-F)

**type_source_proof:** `type-coat` ← title (conf=0.93, min=0.9)
**size_source_proof:** (no variant sizes)
**gender_proof:** `gender-girl` ← handle (conf=0.90)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

### [33] 9688976228665 — מעיל קורדרוי מחמם מאוד דגם אליה

**status:** active
**current_tags (6):** `baby-coat`, `baby-gift`, `corduroy-baby`, `neutral-baby-outfit`, `newborn-clothing`, `winter-baby-wear`
**proposed_new_tags (6):** `type-coat`, `size-6-9m`, `size-9-12m`, `season-winter`, `occ-gift`, `gender-boy`

**proposed_new_tags_with_source:**
  - `type-coat` ← title (conf=0.93, rule=CAT-A)
  - `size-6-9m` ← variant:6-9M→size-6-9m (conf=0.92, rule=CAT-B)
  - `size-9-12m` ← variant:9-12M→size-9-12m (conf=0.92, rule=CAT-B)
  - `season-winter` ← existing_tag (conf=0.85, rule=CAT-C)
  - `occ-gift` ← existing_tag (conf=0.88, rule=CAT-E)
  - `gender-boy` ← handle (conf=0.90, rule=CAT-F)

**type_source_proof:** `type-coat` ← title (conf=0.93, min=0.9)
**size_source_proof:** `6-9M`→`size-6-9m`, `9-12M`→`size-9-12m`
**gender_proof:** `gender-boy` ← handle (conf=0.90)
**forbidden_tags_check:** PASS
**allowed_values_check:** PASS
**final_verdict:** **SAFE_FOR_PHASE7B**

---

## 8. Recommended Live Batch — עד 20 מוצרים (diverse types)

מועמדים מומלצים ל-Phase 7B live batch הבא (לאחר T3 approval).
נבחרו לפי עדיפות type: dress → bodysuit → set → romper → hat/other.
סה"כ 20 מוצרים מ-4 סוגים שונים.

| # | product_id | title | type | proposed_tags |
|---|-----------|-------|------|--------------|
| 1 | 9606691324217 | שמלה אופנתית קלאסית לאירועים לתינוקת | type-dress | `type-dress`, `occ-gift`, `occ-everyday`, `gender-girl` |
| 2 | 9895864369465 | שמלה חגיגית פרחונית דגם מורן | type-dress | `type-dress`, `size-3-6m`, `size-6-9m`, `size-9-12m`, `size-12-18m`, `size-18-24m`, `occ-gift`, `occ-everyday`, `gender-girl`, `style-floral` |
| 3 | 9892557848889 | שמלה כחולה כהה אם דוגמא קלאסית דגם אוראל | type-dress | `type-dress`, `occ-gift`, `occ-everyday`, `gender-girl` |
| 4 | 9179146256697 | שמלה נסיכותית מפתשן וכותנה, מלאה בסטייל - נוע... | type-dress | `type-dress`, `fabric-cotton` |
| 5 | 9606694175033 | שמלה קיצית עם מלמלה לבנות | type-dress | `type-dress`, `gender-girl` |
| 6 | 10190522908985 | Summer Toddler Kids Stripe Bodysuit Boys Loos... | type-bodysuit | `type-bodysuit`, `size-6-9m`, `size-3-6m`, `season-summer`, `gender-girl` |
| 7 | 9179165753657 | בגד גוף כותנה טטרה - פריחת האביב | type-bodysuit | `type-bodysuit`, `season-spring-fall`, `fabric-cotton` |
| 8 | 9179154612537 | בגד גוף כיווצים - גאיה | type-bodysuit | `type-bodysuit` |
| 9 | 9179152154937 | בגד גוף מלמלות - קיטי | type-bodysuit | `type-bodysuit` |
| 10 | 9179167129913 | בגד גוף מלמלות וכיווצים פרחוני - שיילי | type-bodysuit | `type-bodysuit`, `style-floral` |
| 11 | 10190522941753 | 2Pcs Baby Boys' Sports and Leisure Set lapel ... | type-set | `type-set`, `size-12-18m`, `size-9-12m`, `size-6-9m`, `size-3-6m`, `size-18-24m`, `season-summer`, `gender-boy` |
| 12 | 10190523203897 | Boys Khaki Letter Print Half Zip Hooded 2Pcs ... | type-set | `type-set`, `season-summer`, `gender-boy` |
| 13 | 10190523105593 | Boys' Summer Knitted Set, Contrast Color Shor... | type-set | `type-set`, `season-summer`, `fabric-knit`, `gender-boy` |
| 14 | 10190523236665 | Infant Baby Boys Short Sets Patchwork Sleevel... | type-set | `type-set`, `season-summer`, `gender-boy` |
| 15 | 10190522843449 | Kids Baby Boy Summer Clothes Sets Casual Lett... | type-set | `type-set`, `season-summer`, `gender-boy` |
| 16 | 10029649101113 | LUMI™  – אוברול נוחות יוקרתי לתינוקות | type-romper | `type-romper` |
| 17 | 9657091293497 | WarmNest™– אוברול חורף מחבק לתינוקות | type-romper | `type-romper`, `size-6-9m`, `size-9-12m`, `size-12-18m`, `season-winter`, `gender-girl` |
| 18 | 9687596728633 | אוברול Leopard Cozy | type-romper | `type-romper`, `size-3-6m`, `size-6-9m`, `size-9-12m`, `size-12-18m`, `gender-girl` |
| 19 | 10029649002809 | Alure™ Baby | type-romper | `type-romper`, `gender-girl` |
| 20 | 10029648970041 | LumiBear™ חליפת פרמיום לחורף | type-romper | `type-romper`, `size-3-6m`, `size-6-9m`, `size-18-24m`, `size-9-12m`, `size-12-18m`, `season-winter`, `occ-gift`, `gender-boy`, `style-teddy` |

## 9. גיוון ויעד 50

| מדד | ערך |
|-----|-----|
| מוצרים מתויגים כרגע | 19 |
| recommended batch | 20 |
| לאחר batch | 39 |
| עוד חסר ל-50 אחרי batch | 11 |
| סוגי מוצר בbatch המומלץ | type-bodysuit, type-dress, type-romper, type-set |
| כמה סוגים שונים | 4 |
| SAFE pool נותרת לbatches נוספים | 202 |

## 10. Phase 8 — עדיין חסום

| תנאי | מצב |
|------|-----|
| 50+ מוצרים מתויגים | FAIL — 39 < 50 |
| 4+ סוגי מוצר שונים | PASS — 4 |
| QA Contract ACTIVE | PASS |
| **Phase 8 collections** | **BLOCKED** |

## 11. Verdict

### **READY_FOR_PHASE7B_T3_APPROVAL**

| בדיקה | תוצאה |
|-------|-------|
| לפחות 20 SAFE_FOR_PHASE7B | PASS — 222 |
| לפחות 3 סוגי מוצר שונים | PASS — 11 סוגים |
| אין age-* tags | PASS |
| אין forbidden tags | PASS |
| כל source trace מלא | PASS |
| TYPE_MISMATCH תוקן בdry run | PASS — 2 מוצרי sandal הוסרו מהbatch |
| כתיבה ל-Shopify | **NO — dry run only** |

---

*Phase 7B Dry Run — לא בוצעה שום כתיבה ל-Shopify. 2026-05-04.*
