# Phase 7C — Batch 10 Plan (READ-ONLY)

**Generated:** 2026-05-07T12:48:59.081938+00:00
**Mode:** READ_ONLY_PLANNING
**Shopify Writes:** NONE
**Auth:** client_credentials OAuth (מאסטר פרומפט v5.0 — כלל הרשאה עדכני)

---

## סטטוס Phase 7C אחרי Batch 9

| פרמטר | ערך |
|-------|-----|
| Total active products | 393 |
| Written batches 1–9 | 166 |
| Already typed (type-* in Shopify) | 51 |
| **SAFE candidates remaining** | **12** |
| Blocked / no source trace | 164 |
| Selected for Batch 10 | 12 |

### Blocked breakdown

| סיבה | מספר |
|------|------|
| NO_TYPE_SOURCE_TRACE | 86 |
| SHOE_KEYWORD | 62 |
| FALSE_POSITIVE | 16 |

---

## Safety Checks — כל מועמד עבר את כל הבדיקות

| Check | Status |
|-------|--------|
| אין age-* tags | ✅ |
| אין type collision | ✅ |
| אין gender collision | ✅ |
| אין forbidden tags | ✅ |
| אין shoes/sandals/sneakers | ✅ |
| אין EU shoe size | ✅ |
| אין REVIEW_ONLY | ✅ |
| אין RANGE_TOO_BROAD | ✅ |
| יש source_trace (conf ≥ 0.88) | ✅ |

---

## מוצרים נבחרים לBatch 10

**סה"כ:** 12 מוצרים | כולם: type-set

| # | product_id | title | proposed_new_tags | type_source | gender_source | source_trace |
|---|-----------|-------|-------------------|-------------|---------------|-------------|
| 1 | `9873511022905` | בגד ים לבבות דגם מאיה | `type-set, gender-girl` | handle='set' | handle=girl | type matched 'set' in handle (conf=0.88); gender matched 'gi |
| 2 | `9606822265145` | יחידת קומות לאחסון אבקת פורמולה | `type-set` | handle='pcs' | -=- | type matched 'pcs' in handle (conf=0.88) |
| 3 | `9605662245177` | מארז טטרה מיוחד לתינוקות | `type-set` | handle='set' | -=- | type matched 'set' in handle (conf=0.88) |
| 4 | `9605662343481` | מברשות לניקוי הבקבוקים | `type-set` | handle='set' | -=- | type matched 'set' in handle (conf=0.88) |
| 5 | `9605662212409` | סט טטרה הדפס לתינוק | `type-set` | title='סט' | -=- | type matched 'סט' in title (conf=0.88) |
| 6 | `9096636825913` | סט לתינוק עד 3 חודשים - מארז מתנה מפנק | `type-set` | title='סט' | -=- | type matched 'סט' in title (conf=0.88) |
| 7 | `9096628732217` | סט שמיכות עטיפה פרחוני | `type-set` | title='סט' | -=- | type matched 'סט' in title (conf=0.88) |
| 8 | `9894032539961` | ספינר לתינקות 3 חלקים | `type-set, gender-boy` | handle='set' | handle=boy | type matched 'set' in handle (conf=0.88); gender matched 'bo |
| 9 | `9605887689017` | סרבל קיצי לתינוקות | `type-set, gender-neutral` | handle='set' | existing_tag=neutral-baby-outfit | type matched 'set' in handle (conf=0.88); gender matched 'ne |
| 10 | `9605441945913` | רצועת בטן לאחר לידה | `type-set` | handle='set' | -=- | type matched 'set' in handle (conf=0.88) |
| 11 | `9839248769337` | שירותים ניידים לילדים מבית בייבי מניה | `type-set` | handle='pcs' | -=- | type matched 'pcs' in handle (conf=0.88) |
| 12 | `9687563338041` | שלוש  סטים של עונת מעבר מבית בייבי מניה | `type-set, gender-girl` | title='סטים' | handle=girl | type matched 'סטים' in title (conf=0.88); gender matched 'gi |

---

## פירוט מלא לכל מוצר

### 1. בגד ים לבבות דגם מאיה
- **PID:** `9873511022905`
- **Handle:** `patpat-valentines-day-hyper-tactile-cute-bow-baby-girl-swims`
- **Current tags (0):** none
- **Proposed new tags:** type-set, gender-girl
- **Type:** `type-set` | source=`handle` kw=`set` conf=0.88
- **Gender:** `gender-girl` | source=`handle` kw=`girl` conf=0.9
- **Source trace:** type matched 'set' in handle (conf=0.88); gender matched 'girl' in handle (conf=0.90)
- **Risk:** LOW
- **Safety flags:** none
- **Final tags after merge:** gender-girl, type-set

### 2. יחידת קומות לאחסון אבקת פורמולה
- **PID:** `9606822265145`
- **Handle:** `3pcs-4pcs-baby-formula-milk-storage-infant-toddler-portable-`
- **Current tags (0):** none
- **Proposed new tags:** type-set
- **Type:** `type-set` | source=`handle` kw=`pcs` conf=0.88
- **Gender:** `none` | source=`-` kw=`-` conf=0.0
- **Source trace:** type matched 'pcs' in handle (conf=0.88)
- **Risk:** LOW
- **Safety flags:** none
- **Final tags after merge:** type-set

### 3. מארז טטרה מיוחד לתינוקות
- **PID:** `9605662245177`
- **Handle:** `happyflute-new-print-5pcs-set-60-60cm-soft-muslin-swaddle-fe`
- **Current tags (0):** none
- **Proposed new tags:** type-set
- **Type:** `type-set` | source=`handle` kw=`set` conf=0.88
- **Gender:** `none` | source=`-` kw=`-` conf=0.0
- **Source trace:** type matched 'set' in handle (conf=0.88)
- **Risk:** LOW
- **Safety flags:** none
- **Final tags after merge:** type-set

### 4. מברשות לניקוי הבקבוקים
- **PID:** `9605662343481`
- **Handle:** `3-in-1-baby-bottle-brush-set-lone-handle-silicone-bottle-and`
- **Current tags (0):** none
- **Proposed new tags:** type-set
- **Type:** `type-set` | source=`handle` kw=`set` conf=0.88
- **Gender:** `none` | source=`-` kw=`-` conf=0.0
- **Source trace:** type matched 'set' in handle (conf=0.88)
- **Risk:** LOW
- **Safety flags:** none
- **Final tags after merge:** type-set

### 5. סט טטרה הדפס לתינוק
- **PID:** `9605662212409`
- **Handle:** `elinfant-5pcs-gift-set-bamboo-cotton-muslin-bib-burp-cloth-1`
- **Current tags (0):** none
- **Proposed new tags:** type-set
- **Type:** `type-set` | source=`title` kw=`סט` conf=0.88
- **Gender:** `none` | source=`-` kw=`-` conf=0.0
- **Source trace:** type matched 'סט' in title (conf=0.88)
- **Risk:** LOW
- **Safety flags:** none
- **Final tags after merge:** type-set

### 6. סט לתינוק עד 3 חודשים - מארז מתנה מפנק
- **PID:** `9096636825913`
- **Handle:** `סט-לתינוק-עד-3-חודשים-מארז-מתנה-מפנק`
- **Current tags (0):** none
- **Proposed new tags:** type-set
- **Type:** `type-set` | source=`title` kw=`סט` conf=0.88
- **Gender:** `none` | source=`-` kw=`-` conf=0.0
- **Source trace:** type matched 'סט' in title (conf=0.88)
- **Risk:** LOW
- **Safety flags:** none
- **Final tags after merge:** type-set

### 7. סט שמיכות עטיפה פרחוני
- **PID:** `9096628732217`
- **Handle:** `סט-שמיכות-עטיפה-פרחוני`
- **Current tags (0):** none
- **Proposed new tags:** type-set
- **Type:** `type-set` | source=`title` kw=`סט` conf=0.88
- **Gender:** `none` | source=`-` kw=`-` conf=0.0
- **Source trace:** type matched 'סט' in title (conf=0.88)
- **Risk:** LOW
- **Safety flags:** none
- **Final tags after merge:** type-set

### 8. ספינר לתינקות 3 חלקים
- **PID:** `9894032539961`
- **Handle:** `3pcs-set-baby-bath-toys-funny-bathing-sucker-spinner-suction`
- **Current tags (0):** none
- **Proposed new tags:** type-set, gender-boy
- **Type:** `type-set` | source=`handle` kw=`set` conf=0.88
- **Gender:** `gender-boy` | source=`handle` kw=`boy` conf=0.9
- **Source trace:** type matched 'set' in handle (conf=0.88); gender matched 'boy' in handle (conf=0.90)
- **Risk:** LOW
- **Safety flags:** none
- **Final tags after merge:** gender-boy, type-set

### 9. סרבל קיצי לתינוקות
- **PID:** `9605887689017`
- **Handle:** `babys-clothes-summer-jumpsuit-outfit-solid-color-ruched-todd`
- **Current tags (5):** baby-gift, baby-romper, neutral-baby-outfit, newborn-clothing, summer-baby-wear
- **Proposed new tags:** type-set, gender-neutral
- **Type:** `type-set` | source=`handle` kw=`set` conf=0.88
- **Gender:** `gender-neutral` | source=`existing_tag` kw=`neutral-baby-outfit` conf=0.88
- **Source trace:** type matched 'set' in handle (conf=0.88); gender matched 'neutral-baby-outfit' in existing_tag (conf=0.88)
- **Risk:** LOW
- **Safety flags:** none
- **Final tags after merge:** baby-gift, baby-romper, gender-neutral, neutral-baby-outfit, newborn-clothing, summer-baby-wear, type-set

### 10. רצועת בטן לאחר לידה
- **PID:** `9605441945913`
- **Handle:** `3in1-corset-postpartum-belly-band-pregnant-women-tummy-belly`
- **Current tags (0):** none
- **Proposed new tags:** type-set
- **Type:** `type-set` | source=`handle` kw=`set` conf=0.88
- **Gender:** `none` | source=`-` kw=`-` conf=0.0
- **Source trace:** type matched 'set' in handle (conf=0.88)
- **Risk:** LOW
- **Safety flags:** none
- **Final tags after merge:** type-set

### 11. שירותים ניידים לילדים מבית בייבי מניה
- **PID:** `9839248769337`
- **Handle:** `10pcs-folding-toilet-portable-child-travel-potty-for-adults-`
- **Current tags (0):** none
- **Proposed new tags:** type-set
- **Type:** `type-set` | source=`handle` kw=`pcs` conf=0.88
- **Gender:** `none` | source=`-` kw=`-` conf=0.0
- **Source trace:** type matched 'pcs' in handle (conf=0.88)
- **Risk:** LOW
- **Safety flags:** none
- **Final tags after merge:** type-set

### 12. שלוש  סטים של עונת מעבר מבית בייבי מניה
- **PID:** `9687563338041`
- **Handle:** `girls-3pcs-spring-fall-outfit-set-comfy-long-sleeve-tops-wit`
- **Current tags (0):** none
- **Proposed new tags:** type-set, gender-girl
- **Type:** `type-set` | source=`title` kw=`סטים` conf=0.88
- **Gender:** `gender-girl` | source=`handle` kw=`girl` conf=0.9
- **Source trace:** type matched 'סטים' in title (conf=0.88); gender matched 'girl' in handle (conf=0.90)
- **Risk:** LOW
- **Safety flags:** none
- **Final tags after merge:** gender-girl, type-set

---

## QA Contract Pre-Checks (לפני T3)

```
[ ] גיבוי JSON נוצר לפני כתיבה
[ ] dry run PASS לכל 12 מוצרים
[ ] T3 approval התקבל במפורש מאייל
[ ] אין collections / navigation בתוכנית
[ ] אין REVIEW_ONLY
[ ] אין EU shoe sizes
[ ] אין gender inferred from color
[ ] batch ≤ 20 ✓ (12 מוצרים)
[ ] OAuth smoke test PASS לפני ריצה
```

---

**VERDICT:** `READY_FOR_PHASE7C_BATCH10_T3_APPROVAL`

*קובץ זה הוא READ-ONLY PLAN. אין כתיבה ל-Shopify. נדרש T3 approval לפני ביצוע.*