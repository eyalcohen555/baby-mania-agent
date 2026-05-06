# Phase 7C Live Batch 3 — Verify Report

**Date:** 2026-05-06  
**T3 approval:** Ayal approved Phase 7C Live Batch 3  
**Shopify writes:** 20 products PUT  
**Total selected:** 20  
**Written:** 20  
**Rollback triggered:** NO  

---

## QA Table — All Products (11 Checks)

| # | product_id | title | before | +new | after | forbidden | allowed | missing | removed | age | title_chg | status | verdict |
|---|-----------|-------|--------|------|-------|-----------|---------|---------|---------|-----|-----------|--------|--------|
| 1 | `9864947827001` | אוברול חגיגי דגם אנה | 1 | +2 | 3 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 2 | `9179136426297` | שמלת ורדים חגיגית אלגנטית מל | 0 | +1 | 1 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 3 | `9179151794489` | שמלת טול חגיגית - אוריאן | 0 | +1 | 1 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 4 | `9179137048889` | שמלת כותנה חגיגית - אלין | 0 | +1 | 1 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 5 | `9179147829561` | שמלת כותנה קיצית עם טקסטורה  | 0 | +1 | 1 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 6 | `9687596663097` | אוברול סריג מתוק לתינוקות דג | 1 | +2 | 3 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 7 | `9724813443385` | אוברול סריג פסים דגם רפאל | 1 | +2 | 3 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 8 | `9179138457913` | אוברול קיצי מתוק סטייל קז'וא | 0 | +1 | 1 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 9 | `9673732292921` | חליפה 3 חלקים מבית בייבי מני | 6 | +2 | 8 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 10 | `9179156742457` | חליפה מסוגננת פרחונית - מיקה | 0 | +1 | 1 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 11 | `9858268430649` | אוברול גינס מהמם דגם רוית | 1 | +2 | 3 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 12 | `9179176141113` | אוברול דובונים מכותנה - ליאו | 1 | +1 | 2 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 13 | `9179161231673` | אוברול כותנה קיצי - נועה | 1 | +1 | 2 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 14 | `10005779743033` | אוברול לתינוקות דגם סטייסי | 1 | +2 | 3 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 15 | `9096607138105` | אוברול מכופתרת | 5 | +1 | 6 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 16 | `9688965087545` | אוברול דוב מתוק דגם אייל | 1 | +2 | 3 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 17 | `9719189635385` | אוברול דובי אם רגלית דגם אור | 1 | +2 | 3 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 18 | `9717957525817` | אוברול דובי דגם דניאל | 1 | +2 | 3 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 19 | `10005779841337` | אוברול חורפי לתינוקות דגם אנ | 1 | +2 | 3 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |
| 20 | `9688885952825` | חליפה מכנס וחולצה לבנות דגם  | 6 | +2 | 8 | ✅ | ✅ | ✅ | ✅ | ✅ | NO | active | ✅ PASS |

---

## Per-Product Detail

### 9864947827001 — אוברול חגיגי דגם אנה

**status_before:** `active`  
**source_trace:** type matched 'dress' in handle (conf=0.90); gender matched 'girl' in handle (conf=0.90)  
**before_tags (1):** `אוברול`  
**proposed_new_tags:** `type-dress, gender-girl`  
**final_tags_before_write (3):** `gender-girl, type-dress, אוברול`  
**after_tags (3):** `gender-girl, type-dress, אוברול`  
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

### 9179136426297 — שמלת ורדים חגיגית אלגנטית מלאה בסטייל - קיילי

**status_before:** `active`  
**source_trace:** type matched 'שמלת' in title (conf=0.90)  
**before_tags (0):** ``  
**proposed_new_tags:** `type-dress`  
**final_tags_before_write (1):** `type-dress`  
**after_tags (1):** `type-dress`  
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

### 9179151794489 — שמלת טול חגיגית - אוריאן

**status_before:** `active`  
**source_trace:** type matched 'שמלת' in title (conf=0.90)  
**before_tags (0):** ``  
**proposed_new_tags:** `type-dress`  
**final_tags_before_write (1):** `type-dress`  
**after_tags (1):** `type-dress`  
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

### 9179137048889 — שמלת כותנה חגיגית - אלין

**status_before:** `active`  
**source_trace:** type matched 'שמלת' in title (conf=0.90)  
**before_tags (0):** ``  
**proposed_new_tags:** `type-dress`  
**final_tags_before_write (1):** `type-dress`  
**after_tags (1):** `type-dress`  
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

### 9179147829561 — שמלת כותנה קיצית עם טקסטורה - יעל

**status_before:** `active`  
**source_trace:** type matched 'שמלת' in title (conf=0.90)  
**before_tags (0):** ``  
**proposed_new_tags:** `type-dress`  
**final_tags_before_write (1):** `type-dress`  
**after_tags (1):** `type-dress`  
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

### 9687596663097 — אוברול סריג מתוק לתינוקות דגם שוהם

**status_before:** `active`  
**source_trace:** type matched 'set' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90)  
**before_tags (1):** `אוברול`  
**proposed_new_tags:** `type-set, gender-girl`  
**final_tags_before_write (3):** `gender-girl, type-set, אוברול`  
**after_tags (3):** `gender-girl, type-set, אוברול`  
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

### 9724813443385 — אוברול סריג פסים דגם רפאל

**status_before:** `active`  
**source_trace:** type matched 'outfit' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90)  
**before_tags (1):** `אוברול`  
**proposed_new_tags:** `type-set, gender-girl`  
**final_tags_before_write (3):** `gender-girl, type-set, אוברול`  
**after_tags (3):** `gender-girl, type-set, אוברול`  
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

### 9179138457913 — אוברול קיצי מתוק סטייל קז'ואל - יואבי

**status_before:** `active`  
**source_trace:** type matched 'סט' in handle (conf=0.88)  
**before_tags (0):** ``  
**proposed_new_tags:** `type-set`  
**final_tags_before_write (1):** `type-set`  
**after_tags (1):** `type-set`  
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

### 9673732292921 — חליפה 3 חלקים מבית בייבי מניה דגם אריאל

**status_before:** `active`  
**source_trace:** type matched 'חליפה' in title (conf=0.88); gender matched 'girl' in handle (conf=0.90)  
**before_tags (6):** `baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, neutral-baby-outfit, newborn-clothing`  
**proposed_new_tags:** `type-set, gender-girl`  
**final_tags_before_write (8):** `baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, gender-girl, neutral-baby-outfit, newborn-clothing, type-set`  
**after_tags (8):** `baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, gender-girl, neutral-baby-outfit, newborn-clothing, type-set`  
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

### 9179156742457 — חליפה מסוגננת פרחונית - מיקה

**status_before:** `active`  
**source_trace:** type matched 'חליפה' in title (conf=0.88)  
**before_tags (0):** ``  
**proposed_new_tags:** `type-set`  
**final_tags_before_write (1):** `type-set`  
**after_tags (1):** `type-set`  
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

### 9858268430649 — אוברול גינס מהמם דגם רוית

**status_before:** `active`  
**source_trace:** type matched 'romper' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90)  
**before_tags (1):** `אוברול`  
**proposed_new_tags:** `type-romper, gender-girl`  
**final_tags_before_write (3):** `gender-girl, type-romper, אוברול`  
**after_tags (3):** `gender-girl, type-romper, אוברול`  
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

### 9179176141113 — אוברול דובונים מכותנה - ליאור

**status_before:** `active`  
**source_trace:** type matched 'אוברול' in title (conf=0.88)  
**before_tags (1):** `אוברול`  
**proposed_new_tags:** `type-romper`  
**final_tags_before_write (2):** `type-romper, אוברול`  
**after_tags (2):** `type-romper, אוברול`  
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

### 9179161231673 — אוברול כותנה קיצי - נועה

**status_before:** `active`  
**source_trace:** type matched 'אוברול' in title (conf=0.88)  
**before_tags (1):** `אוברול`  
**proposed_new_tags:** `type-romper`  
**final_tags_before_write (2):** `type-romper, אוברול`  
**after_tags (2):** `type-romper, אוברול`  
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

### 10005779743033 — אוברול לתינוקות דגם סטייסי

**status_before:** `active`  
**source_trace:** type matched 'romper' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90)  
**before_tags (1):** `אוברול`  
**proposed_new_tags:** `type-romper, gender-girl`  
**final_tags_before_write (3):** `gender-girl, type-romper, אוברול`  
**after_tags (3):** `gender-girl, type-romper, אוברול`  
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

### 9096607138105 — אוברול מכופתרת

**status_before:** `active`  
**source_trace:** type matched 'אוברול' in title (conf=0.88)  
**before_tags (5):** `baby-gift, baby-overall, everyday-baby-wear, neutral-baby-outfit, newborn-clothing`  
**proposed_new_tags:** `type-romper`  
**final_tags_before_write (6):** `baby-gift, baby-overall, everyday-baby-wear, neutral-baby-outfit, newborn-clothing, type-romper`  
**after_tags (6):** `baby-gift, baby-overall, everyday-baby-wear, neutral-baby-outfit, newborn-clothing, type-romper`  
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

### 9688965087545 — אוברול דוב מתוק דגם אייל

**status_before:** `active`  
**source_trace:** type matched 'bodysuit' in handle (conf=0.90); gender matched 'boy' in handle (conf=0.90)  
**before_tags (1):** `אוברול`  
**proposed_new_tags:** `type-bodysuit, gender-boy`  
**final_tags_before_write (3):** `gender-boy, type-bodysuit, אוברול`  
**after_tags (3):** `gender-boy, type-bodysuit, אוברול`  
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

### 9719189635385 — אוברול דובי אם רגלית דגם אוריאל

**status_before:** `active`  
**source_trace:** type matched 'bodysuit' in handle (conf=0.90); gender matched 'boy' in handle (conf=0.90)  
**before_tags (1):** `אוברול`  
**proposed_new_tags:** `type-bodysuit, gender-boy`  
**final_tags_before_write (3):** `gender-boy, type-bodysuit, אוברול`  
**after_tags (3):** `gender-boy, type-bodysuit, אוברול`  
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

### 9717957525817 — אוברול דובי דגם דניאל

**status_before:** `active`  
**source_trace:** type matched 'bodysuit' in handle (conf=0.90); gender matched 'girl' in handle (conf=0.90)  
**before_tags (1):** `אוברול`  
**proposed_new_tags:** `type-bodysuit, gender-girl`  
**final_tags_before_write (3):** `gender-girl, type-bodysuit, אוברול`  
**after_tags (3):** `gender-girl, type-bodysuit, אוברול`  
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

### 10005779841337 — אוברול חורפי לתינוקות דגם אנגל

**status_before:** `active`  
**source_trace:** type matched 'bodysuit' in handle (conf=0.90); gender matched 'girl' in handle (conf=0.90)  
**before_tags (1):** `אוברול`  
**proposed_new_tags:** `type-bodysuit, gender-girl`  
**final_tags_before_write (3):** `gender-girl, type-bodysuit, אוברול`  
**after_tags (3):** `gender-girl, type-bodysuit, אוברול`  
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

### 9688885952825 — חליפה מכנס וחולצה לבנות דגם אנה

**status_before:** `active`  
**source_trace:** type matched 'bodysuit' in handle (conf=0.90); gender matched 'בנות' in title (conf=0.90)  
**before_tags (6):** `baby-gift, baby-top, everyday-baby-wear, girls-clothing, neutral-baby-outfit, newborn-clothing`  
**proposed_new_tags:** `type-bodysuit, gender-girl`  
**final_tags_before_write (8):** `baby-gift, baby-top, everyday-baby-wear, gender-girl, girls-clothing, neutral-baby-outfit, newborn-clothing, type-bodysuit`  
**after_tags (8):** `baby-gift, baby-top, everyday-baby-wear, gender-girl, girls-clothing, neutral-baby-outfit, newborn-clothing, type-bodysuit`  
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

**PHASE7C_LIVE_BATCH3_PASS**

pass=20 | fail=0 | written=20
