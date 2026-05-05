# Phase 7C Live Batch 2 — Verify Report (hat + coat)

**Date:** 2026-05-05  
**T3 approval:** Ayal approved Phase 7C Live Batch 2 — hat + coat only  
**Shopify writes:** 7 products PUT  
**Written:** 7 / 7  
**Rollback triggered:** NO  

---

## QA Table

| # | product_id | title | type | before | +new | after | forbidden | miss_new | removed | age | title_chg | status | verdict |
|---|-----------|-------|------|--------|------|-------|-----------|---------|---------|-----|-----------|--------|--------|
| 1 | `9179141308729` | כובע בייסבול דובוני לתינוקות | `type-hat` | 0 | +2 | 2 | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 2 | `9606864666937` | כובע בייסבול רך לתינוק | `type-hat` | 0 | +2 | 2 | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 3 | `10024854847801` | כובע צמר מתנה | `type-hat` | 1 | +2 | 3 | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 4 | `9179140915513` | כובע קייצי רך ונעים מכותנה מ | `type-hat` | 0 | +1 | 1 | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 5 | `9731768713529` | מעיל אופנתי לבנות – דגם שירא | `type-coat` | 6 | +4 | 10 | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 6 | `9673730359609` | מעיל חורף צמר דגם שנאל | `type-coat` | 5 | +4 | 9 | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 7 | `9688976228665` | מעיל קורדרוי מחמם מאוד דגם א | `type-coat` | 6 | +4 | 10 | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |

---

## Per-Product Detail

### 9179141308729 — כובע בייסבול דובוני לתינוקות מעוצב ומהמם עשוי מכותנה, מתאים לבנים ולבנות בגילאי 3-12 חודשים

**status_before:** `active`  
**before_tags (0):** ``  
**proposed_new_tags:** `type-hat, gender-girl`  
**final_tags_before_write (2):** `gender-girl, type-hat`  
**after_tags (2):** `gender-girl, type-hat`  
**missing_new_tags:** `none`  
**removed_old_tags:** `none`  
**unexpected_tags:** `none`  
**allowed_values_check:** `PASS`  
**forbidden_tags_check:** `PASS`  
**age_tags_check:** `PASS`  
**title_changed:** `NO`  
**status_after:** `active`  
**rollback_needed:** `NO`  
**final_verdict:** `PASS`  

### 9606864666937 — כובע בייסבול רך לתינוק

**status_before:** `active`  
**before_tags (0):** ``  
**proposed_new_tags:** `type-hat, gender-girl`  
**final_tags_before_write (2):** `gender-girl, type-hat`  
**after_tags (2):** `gender-girl, type-hat`  
**missing_new_tags:** `none`  
**removed_old_tags:** `none`  
**unexpected_tags:** `none`  
**allowed_values_check:** `PASS`  
**forbidden_tags_check:** `PASS`  
**age_tags_check:** `PASS`  
**title_changed:** `NO`  
**status_after:** `active`  
**rollback_needed:** `NO`  
**final_verdict:** `PASS`  

### 10024854847801 — כובע צמר מתנה

**status_before:** `active`  
**before_tags (1):** `gift`  
**proposed_new_tags:** `type-hat, occ-gift`  
**final_tags_before_write (3):** `gift, occ-gift, type-hat`  
**after_tags (3):** `gift, occ-gift, type-hat`  
**missing_new_tags:** `none`  
**removed_old_tags:** `none`  
**unexpected_tags:** `none`  
**allowed_values_check:** `PASS`  
**forbidden_tags_check:** `PASS`  
**age_tags_check:** `PASS`  
**title_changed:** `NO`  
**status_after:** `active`  
**rollback_needed:** `NO`  
**final_verdict:** `PASS`  

### 9179140915513 — כובע קייצי רך ונעים מכותנה מתאים לתנוקות בגילאי 0-12 חודשים

**status_before:** `active`  
**before_tags (0):** ``  
**proposed_new_tags:** `type-hat`  
**final_tags_before_write (1):** `type-hat`  
**after_tags (1):** `type-hat`  
**missing_new_tags:** `none`  
**removed_old_tags:** `none`  
**unexpected_tags:** `none`  
**allowed_values_check:** `PASS`  
**forbidden_tags_check:** `PASS`  
**age_tags_check:** `PASS`  
**title_changed:** `NO`  
**status_after:** `active`  
**rollback_needed:** `NO`  
**final_verdict:** `PASS`  

### 9731768713529 — מעיל אופנתי לבנות – דגם שיראל

**status_before:** `active`  
**before_tags (6):** `baby-coat, baby-gift, everyday-baby-wear, girls-clothing, neutral-baby-outfit, newborn-clothing`  
**proposed_new_tags:** `type-coat, gender-girl, occ-gift, occ-everyday`  
**final_tags_before_write (10):** `baby-coat, baby-gift, everyday-baby-wear, gender-girl, girls-clothing, neutral-baby-outfit, newborn-clothing, occ-everyday, occ-gift, type-coat`  
**after_tags (10):** `baby-coat, baby-gift, everyday-baby-wear, gender-girl, girls-clothing, neutral-baby-outfit, newborn-clothing, occ-everyday, occ-gift, type-coat`  
**missing_new_tags:** `none`  
**removed_old_tags:** `none`  
**unexpected_tags:** `none`  
**allowed_values_check:** `PASS`  
**forbidden_tags_check:** `PASS`  
**age_tags_check:** `PASS`  
**title_changed:** `NO`  
**status_after:** `active`  
**rollback_needed:** `NO`  
**final_verdict:** `PASS`  

### 9673730359609 — מעיל חורף צמר דגם שנאל

**status_before:** `active`  
**before_tags (5):** `baby-coat, baby-gift, neutral-baby-outfit, newborn-clothing, winter-baby-wear`  
**proposed_new_tags:** `type-coat, gender-girl, occ-gift, occ-seasonal`  
**final_tags_before_write (9):** `baby-coat, baby-gift, gender-girl, neutral-baby-outfit, newborn-clothing, occ-gift, occ-seasonal, type-coat, winter-baby-wear`  
**after_tags (9):** `baby-coat, baby-gift, gender-girl, neutral-baby-outfit, newborn-clothing, occ-gift, occ-seasonal, type-coat, winter-baby-wear`  
**missing_new_tags:** `none`  
**removed_old_tags:** `none`  
**unexpected_tags:** `none`  
**allowed_values_check:** `PASS`  
**forbidden_tags_check:** `PASS`  
**age_tags_check:** `PASS`  
**title_changed:** `NO`  
**status_after:** `active`  
**rollback_needed:** `NO`  
**final_verdict:** `PASS`  

### 9688976228665 — מעיל קורדרוי מחמם מאוד דגם אליה

**status_before:** `active`  
**before_tags (6):** `baby-coat, baby-gift, corduroy-baby, neutral-baby-outfit, newborn-clothing, winter-baby-wear`  
**proposed_new_tags:** `type-coat, gender-boy, occ-gift, occ-seasonal`  
**final_tags_before_write (10):** `baby-coat, baby-gift, corduroy-baby, gender-boy, neutral-baby-outfit, newborn-clothing, occ-gift, occ-seasonal, type-coat, winter-baby-wear`  
**after_tags (10):** `baby-coat, baby-gift, corduroy-baby, gender-boy, neutral-baby-outfit, newborn-clothing, occ-gift, occ-seasonal, type-coat, winter-baby-wear`  
**missing_new_tags:** `none`  
**removed_old_tags:** `none`  
**unexpected_tags:** `none`  
**allowed_values_check:** `PASS`  
**forbidden_tags_check:** `PASS`  
**age_tags_check:** `PASS`  
**title_changed:** `NO`  
**status_after:** `active`  
**rollback_needed:** `NO`  
**final_verdict:** `PASS`  

---

## Verdict

**PHASE7C_LIVE_BATCH2_PASS**

pass=7 | fail=0 | written=7
