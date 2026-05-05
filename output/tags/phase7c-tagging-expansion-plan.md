# Phase 7C — Tagging Expansion Plan

**Date:** 2026-05-05 21:43:06  
**Shop:** a2756c-c0.myshopify.com  
**Type:** READ-ONLY — planning only, no Shopify writes  
**Token suffix:** `de6d`  

---

## 1. System State

| Item | Status |
|------|--------|
| Phase 8 Navigation Pipeline | ✅ COMPLETE |
| Phase 8G Post-Live Monitor | ✅ PASS (15/15) |
| Phase 8H Visual UX Polish | ⏳ פתוח — לא חוסם |
| Currently tagged live | **51 products** |
| QA Contract | ✅ ACTIVE |
| Shopify writes this phase | NONE — GET only |

---

## 2. Product Pool

| Category | Count |
|----------|-------|
| Active products (Shopify) | **393** |
| Already tagged (type-*) | **51** |
| SAFE candidates | **207** |
| REVIEW_ONLY | **135** |
| REJECT | **0** |
| Unknown/unscanned | 0 (all scanned) |

---

## 3. Recommended Batch — Phase 7C Live

**Batch size:** 30 products  
**Selection criteria:** highest conf, max 6/type, priority: dress/bodysuit/set/romper/coat/hat  

### Type Breakdown

| Type | Count |
|------|-------|
| `type-dress` | 6 |
| `type-set` | 6 |
| `type-romper` | 6 |
| `type-bodysuit` | 5 |
| `type-hat` | 4 |
| `type-coat` | 3 |

### Gender Breakdown

| Gender | Count |
|--------|-------|
| `gender-girl` | 12 |
| `no-gender` | 10 |
| `gender-boy` | 5 |
| `gender-neutral` | 3 |

---

## 4. Recommended Batch — Product List

| # | product_id | title | type | conf | type_src | gender | gender_src | proposed_tags |
|---|-----------|-------|------|------|----------|--------|-----------|---------------|
| 1 | `9607363592505` | סנדלי קיץ וינטג' | `type-dress` | 0.90 | handle | gender-girl | handle | type-dress, gender-girl, occ-gift, occ-seasonal |
| 2 | `9607363559737` | סנדלים אופנתיים לתינוקות צעד ראשון | `type-dress` | 0.90 | handle | gender-girl | handle | type-dress, gender-girl, occ-gift, occ-everyday |
| 3 | `9606694142265` | שמלת אירועים אלגנטית לתינוקת | `type-dress` | 0.90 | handle | gender-girl | handle | type-dress, gender-girl |
| 4 | `9606690111801` | שמלת בסגנון אמריקאי לבנות | `type-dress` | 0.90 | handle | gender-girl | title | type-dress, gender-girl |
| 5 | `9892620927289` | שמלת וי פסים דגם יהלי | `type-dress` | 0.90 | handle | gender-girl | handle | type-dress, gender-girl |
| 6 | `9179134132537` | שמלת טוטו נסיכותית - אלין | `type-dress` | 0.90 | title | — | — | type-dress |
| 7 | `9179152482617` | בגד גוף אלגנטי - מייקל | `type-bodysuit` | 0.90 | title | — | — | type-bodysuit |
| 8 | `9179168964921` | בגד גוף כיווצים אלגנטי - נטלי | `type-bodysuit` | 0.90 | title | — | — | type-bodysuit |
| 9 | `9096607301945` | בגד גוף פליז שרוולים ארוכים ופונפונים | `type-bodysuit` | 0.90 | title | gender-neutral | existing_tag | type-bodysuit, gender-neutral, occ-gift, occ-seasonal |
| 10 | `9179172733241` | בגד גוף פסים אלגנטי - ריף | `type-bodysuit` | 0.90 | title | — | — | type-bodysuit |
| 11 | `9179138687289` | בגד גוף קיצי נוח ואוורירי, כולל כובע מתוק - ג | `type-bodysuit` | 0.90 | title | — | — | type-bodysuit |
| 12 | `10190523334969` | 0-18 Months old Newborn Baby boy Jumpsuit Cut | `type-set` | 0.88 | title | gender-boy | title | type-set, gender-boy, occ-seasonal |
| 13 | `10190522876217` | Toddler Summer Outfits 2026 New Baby Boy Clot | `type-set` | 0.88 | title | gender-boy | title | type-set, gender-boy, occ-everyday, occ-seasonal |
| 14 | `9855017550137` | Veloura Baby™ חליפה פרחונית | `type-set` | 0.88 | handle | gender-girl | handle | type-set, gender-girl, occ-gift, occ-everyday |
| 15 | `10190523269433` | VISgogo Toddler Baby Boys Clothes Set Short S | `type-set` | 0.88 | title | gender-boy | title | type-set, gender-boy, occ-everyday, occ-seasonal |
| 16 | `9688934940985` | אוברול בייבי  לתינוק – Baby Bear Cozy Set | `type-set` | 0.88 | title | — | — | type-set |
| 17 | `10005779808569` | אוברול בייבי מניה דגם חן | `type-set` | 0.88 | handle | gender-girl | handle | type-set, gender-girl, occ-seasonal |
| 18 | `9179155693881` | אוברול אלגנט דגם עומרי | `type-romper` | 0.88 | title | — | — | type-romper |
| 19 | `9096606908729` | אוברול ארוך | `type-romper` | 0.88 | title | gender-neutral | existing_tag | type-romper, gender-neutral, occ-gift, occ-everyday |
| 20 | `9096599994681` | אוברול ארוך עם רוכסן | `type-romper` | 0.88 | title | gender-neutral | existing_tag | type-romper, gender-neutral, occ-gift, occ-everyday |
| 21 | `9678573240633` | אוברול אריה מתוק דגם שמר | `type-romper` | 0.88 | handle | gender-boy | handle | type-romper, gender-boy |
| 22 | `10026520445241` | אוברול בייבי מניה דגם חן | `type-romper` | 0.88 | title | — | — | type-romper |
| 23 | `9858268430649` | אוברול גינס מהמם דגם רוית | `type-romper` | 0.88 | handle | gender-girl | handle | type-romper, gender-girl |
| 24 | `9731768713529` | מעיל אופנתי לבנות – דגם שיראל | `type-coat` | 0.90 | title | gender-girl | title | type-coat, gender-girl, occ-gift, occ-everyday |
| 25 | `9673730359609` | מעיל חורף צמר דגם שנאל | `type-coat` | 0.90 | title | gender-girl | handle | type-coat, gender-girl, occ-gift, occ-seasonal |
| 26 | `9688976228665` | מעיל קורדרוי מחמם מאוד דגם אליה | `type-coat` | 0.90 | title | gender-boy | handle | type-coat, gender-boy, occ-gift, occ-seasonal |
| 27 | `9179141308729` | כובע בייסבול דובוני לתינוקות מעוצב ומהמם עשוי | `type-hat` | 0.92 | title | gender-girl | title | type-hat, gender-girl |
| 28 | `9606864666937` | כובע בייסבול רך לתינוק | `type-hat` | 0.92 | title | gender-girl | handle | type-hat, gender-girl |
| 29 | `10024854847801` | כובע צמר מתנה | `type-hat` | 0.92 | title | — | — | type-hat, occ-gift |
| 30 | `9179140915513` | כובע קייצי רך ונעים מכותנה מתאים לתנוקות בגיל | `type-hat` | 0.92 | title | — | — | type-hat |

---

## 5. Source Trace — Top 10 Candidates

### [1] 9607363592505 — סנדלי קיץ וינטג'

**status:** active  
**current_tags (5):** `baby-gift`, `baby-sandals`, `newborn-clothing`, `summer-baby-wear`, `vintage-baby`  
**proposed_tags:** `type-dress`, `gender-girl`, `occ-gift`, `occ-seasonal`  

**type:** `type-dress` ← handle (conf=0.90)  
**gender:** `gender-girl` ← handle (conf=0.90)  
**occ:** `occ-gift` ← title/existing_tag  
**occ:** `occ-seasonal` ← title/existing_tag  
**forbidden_check:** PASS  
**allowed_values_check:** PASS  
**verdict:** SAFE_FOR_PHASE7C  

---

### [2] 9607363559737 — סנדלים אופנתיים לתינוקות צעד ראשון

**status:** active  
**current_tags (5):** `baby-gift`, `baby-sandals`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing`  
**proposed_tags:** `type-dress`, `gender-girl`, `occ-gift`, `occ-everyday`  

**type:** `type-dress` ← handle (conf=0.90)  
**gender:** `gender-girl` ← handle (conf=0.90)  
**occ:** `occ-gift` ← title/existing_tag  
**occ:** `occ-everyday` ← title/existing_tag  
**forbidden_check:** PASS  
**allowed_values_check:** PASS  
**verdict:** SAFE_FOR_PHASE7C  

---

### [3] 9606694142265 — שמלת אירועים אלגנטית לתינוקת

**status:** active  
**current_tags (0):** ``  
**proposed_tags:** `type-dress`, `gender-girl`  

**type:** `type-dress` ← handle (conf=0.90)  
**gender:** `gender-girl` ← handle (conf=0.90)  
**forbidden_check:** PASS  
**allowed_values_check:** PASS  
**verdict:** SAFE_FOR_PHASE7C  

---

### [4] 9606690111801 — שמלת בסגנון אמריקאי לבנות

**status:** active  
**current_tags (0):** ``  
**proposed_tags:** `type-dress`, `gender-girl`  

**type:** `type-dress` ← handle (conf=0.90)  
**gender:** `gender-girl` ← title (conf=0.90)  
**forbidden_check:** PASS  
**allowed_values_check:** PASS  
**verdict:** SAFE_FOR_PHASE7C  

---

### [5] 9892620927289 — שמלת וי פסים דגם יהלי

**status:** active  
**current_tags (0):** ``  
**proposed_tags:** `type-dress`, `gender-girl`  

**type:** `type-dress` ← handle (conf=0.90)  
**gender:** `gender-girl` ← handle (conf=0.90)  
**forbidden_check:** PASS  
**allowed_values_check:** PASS  
**verdict:** SAFE_FOR_PHASE7C  

---

### [6] 9179134132537 — שמלת טוטו נסיכותית - אלין

**status:** active  
**current_tags (0):** ``  
**proposed_tags:** `type-dress`  

**type:** `type-dress` ← title (conf=0.90)  
**forbidden_check:** PASS  
**allowed_values_check:** PASS  
**verdict:** SAFE_FOR_PHASE7C  

---

### [7] 9179152482617 — בגד גוף אלגנטי - מייקל

**status:** active  
**current_tags (0):** ``  
**proposed_tags:** `type-bodysuit`  

**type:** `type-bodysuit` ← title (conf=0.90)  
**forbidden_check:** PASS  
**allowed_values_check:** PASS  
**verdict:** SAFE_FOR_PHASE7C  

---

### [8] 9179168964921 — בגד גוף כיווצים אלגנטי - נטלי

**status:** active  
**current_tags (0):** ``  
**proposed_tags:** `type-bodysuit`  

**type:** `type-bodysuit` ← title (conf=0.90)  
**forbidden_check:** PASS  
**allowed_values_check:** PASS  
**verdict:** SAFE_FOR_PHASE7C  

---

### [9] 9096607301945 — בגד גוף פליז שרוולים ארוכים ופונפונים

**status:** active  
**current_tags (6):** `baby-bodysuit`, `baby-gift`, `fleece-baby`, `neutral-baby-outfit`, `newborn-clothing`, `winter-baby-wear`  
**proposed_tags:** `type-bodysuit`, `gender-neutral`, `occ-gift`, `occ-seasonal`  

**type:** `type-bodysuit` ← title (conf=0.90)  
**gender:** `gender-neutral` ← existing_tag (conf=0.88)  
**occ:** `occ-gift` ← title/existing_tag  
**occ:** `occ-seasonal` ← title/existing_tag  
**forbidden_check:** PASS  
**allowed_values_check:** PASS  
**verdict:** SAFE_FOR_PHASE7C  

---

### [10] 9179172733241 — בגד גוף פסים אלגנטי - ריף

**status:** active  
**current_tags (0):** ``  
**proposed_tags:** `type-bodysuit`  

**type:** `type-bodysuit` ← title (conf=0.90)  
**forbidden_check:** PASS  
**allowed_values_check:** PASS  
**verdict:** SAFE_FOR_PHASE7C  

---

## 6. Safety Checks

| Check | Result |
|-------|--------|
| No age-* tags | ✅ PASS |
| No multiple type-* | ✅ PASS |
| No gender collision | ✅ PASS |
| No forbidden tags | ✅ PASS |
| No archived products | ✅ PASS (active filter applied) |
| No already-tagged included | ✅ PASS (type-* filter applied) |
| No EU shoe size | ✅ PASS (blocked at classifier) |
| No Shopify writes | ✅ PASS — GET only |

---

## 7. Blockers

| Blocker | Status |
|---------|--------|
| EU Shoe Size mapping | ⛔ OPEN — type-shoes/sandals/sneakers blocked |
| REVIEW_ONLY pool | ⏳ manual review required before inclusion |
| Phase 8H Visual UX Polish | ⏳ open — לא חוסם Phase 7C |

---

## 8. Shopify Writes

**NONE.** כל הפעולות בשלב זה היו GET בלבד. אין PUT/POST/DELETE.

---

## 9. T3 Approval Requirements

לפני batch live, נדרש T3 approval מאייל עם:  
- אישור batch size (מומלץ: 20 מוצרים ראשונים)  
- אישור type mix  
- אישור QA Contract פעיל  

---

## 10. Verdict

**READY_FOR_PHASE7C_T3_APPROVAL**

✅ 30 SAFE candidates מוכנים לbatch live.
כל safety checks עברו. אין age-* tags. אין type collision. אין gender collision.
הצעד הבא: T3 approval מאייל → Phase 7C live batch (עד 20 מוצרים ראשונים).

---

*Report generated by scripts/phase7c_tagging_expansion_plan.py*