# Layer 7 — Phase 7A Diverse Rollout Candidates
**תאריך:** 2026-05-04
**Phase:** 7A — Dry Run — DRY RUN ONLY — אין כתיבה ל-Shopify

---

## 1. מצב מערכת

| פרמטר | ערך |
|-------|-----|
| Phase 6 batch 1+2 | COMPLETE — PASS |
| Shopify live | YES — **5 products** (C3, C2, C4, C5, C1) |
| כל 5 מוצרים חיים | type-romper בלבד |
| Phase 7A | DRY RUN |
| collections | NOT OPEN |
| Mega Menu | NO |
| כתיבה ל-Shopify | NO |

---

## 2. למה לא collections עדיין

| סיבה | פרטים |
|------|-------|
| 5 מוצרים חיים בלבד (1.3% מהinventory) | Phase 7 (50+) נדרש לפני Phase 8 |
| כל 5 מוצרים = type-romper | אין גיוון — collection = לא ערך ללקוח |
| spec דורש Phase 7 לפני Phase 8 | Collections = downstream phase |
| navigation עם item אחד | UX confusion |

**target לפני collections:** 50+ מוצרים מ-4+ סוגים שונים.

---

## 3. מועמדים — 20 מוצרים

| # | product_id | כותרת | type | verdict | score |
|---|-----------|-------|------|---------|-------|
| 1 | 9179166671161 | בגד גוף שמלה ג׳ינס מכותנה - הרפר | type-bodysuit | SAFE_FOR_PHASE7A | 95.0 |
| 2 | 9606694437177 | חליפת פולו קצרה סרוגה לתינוקות | type-set | SAFE_FOR_PHASE7A | 85.0 |
| 3 | 9731768746297 | סט בגדי תינוקות גינס ושמלה דגם טליה | type-dress | SAFE_FOR_PHASE7A | 85.0 |
| 4 | 9607363559737 | סנדלים אופנתיים לתינוקות צעד ראשון | type-sandals | REVIEW_ONLY | 85.0 |
| 5 | 9179165753657 | בגד גוף כותנה טטרה - פריחת האביב | type-bodysuit | REVIEW_ONLY | 75.0 |
| 6 | 9179168964921 | בגד גוף כיווצים אלגנטי - נטלי | type-bodysuit | REVIEW_ONLY | 70.0 |
| 7 | 9179152154937 | בגד גוף מלמלות - קיטי | type-bodysuit | REVIEW_ONLY | 70.0 |
| 8 | 9179167129913 | בגד גוף מלמלות וכיווצים פרחוני - שיילי | type-bodysuit | REVIEW_ONLY | 70.0 |
| 9 | 9874906382649 | בגד גוף פו הדוב דגם לירון | type-bodysuit | SAFE_FOR_PHASE7A | 100.0 |
| 10 | 9688885985593 | אוברול פיל מתוק דגם נאיה | type-romper | SAFE_FOR_PHASE7A | 100.0 |
| 11 | 9688934973753 | אוברול פיל פסים דגם ליאו | type-romper | SAFE_FOR_PHASE7A | 95.0 |
| 12 | 9874906546489 | חליפת דובי  מלאה בסטייל דגם מאור | type-set | SAFE_FOR_PHASE7A | 100.0 |
| 13 | 9688660377913 | חליפת קואלה דגם שני | type-set | SAFE_FOR_PHASE7A | 100.0 |
| 14 | 9688976326969 | חליפה דוב מופתע דגם ליאל | type-set | SAFE_FOR_PHASE7A | 100.0 |
| 15 | 9688964989241 | חליפה דוב מקסימה דגם אריאל | type-set | SAFE_FOR_PHASE7A | 100.0 |
| 16 | 9688674566457 | חליפה לבנים דגם אימרי | type-set | SAFE_FOR_PHASE7A | 100.0 |
| 17 | 9688976294201 | חליפה מהממת רקמת דובי חמוד דגם אלי | type-set | SAFE_FOR_PHASE7A | 100.0 |
| 18 | 10190523302201 | Children’s Summer New Arrival Boys’ Regular S | type-set | SAFE_FOR_PHASE7A | 100.0 |
| 19 | 10190523203897 | Boys Khaki Letter Print Half Zip Hooded 2Pcs  | type-set | REVIEW_ONLY | 80.0 |
| 20 | 10190523138361 | Boys' summer white striped short-sleeved shor | type-set | SAFE_FOR_PHASE7A | 100.0 |

---

## 4. פילוח לפי סוג מוצר

| type | מוצרים בbatch זה | מוצרים חיים |
|------|----------------|------------|
| type-romper | 2 | 5 |
| type-dress | 1 | 0 |
| type-set | 10 | 0 |
| type-bodysuit | 6 | 0 |
| type-sandals | 1 | 0 |

---

## 5. פרטים לכל מוצר

### 9179166671161 — בגד גוף שמלה ג׳ינס מכותנה - הרפר
**type:** type-bodysuit | **score:** 95.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** True
**size_status:** OK
**proposed tags (4):** `type-bodysuit, size-12-18m, size-3-6m, fabric-cotton`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-bodysuit | title | keyword | 0.88 |
| size-12-18m | existing_tag_hebrew | heb_tag | 0.9 |
| size-3-6m | existing_tag_hebrew | heb_tag | 0.9 |
| fabric-cotton | title | keyword | 0.9 |

### 9606694437177 — חליפת פולו קצרה סרוגה לתינוקות
**type:** type-set | **score:** 85.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** True
**size_status:** NO_SIZE_FOUND
**proposed tags (5):** `type-set, season-summer, fabric-knit, gender-neutral, style-striped`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-set | existing_tag | tag_map | 0.88 |
| season-summer | title_handle | keyword | 0.88 |
| fabric-knit | existing_tag | keyword | 0.9 |
| gender-neutral | existing_tag | tag_map | 0.9 |
| style-striped | title | keyword | 0.82 |

### 9731768746297 — סט בגדי תינוקות גינס ושמלה דגם טליה
**type:** type-dress | **score:** 85.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** True
**size_status:** NO_SIZE_FOUND
**proposed tags (4):** `type-dress, season-summer, fabric-denim, gender-girl`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-dress | title | keyword | 0.9 |
| season-summer | title_handle | keyword | 0.88 |
| fabric-denim | title | keyword | 0.9 |
| gender-girl | handle | keyword | 0.9 |

### 9607363559737 — סנדלים אופנתיים לתינוקות צעד ראשון
**type:** type-sandals | **score:** 85.0 | **verdict:** `REVIEW_ONLY` | **has_yaml:** True
**reason:** size range too broad
**size_status:** RANGE_TOO_BROAD
**proposed tags (3):** `type-sandals, season-summer, gender-neutral`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-sandals | existing_tag | tag_map | 0.88 |
| season-summer | title_handle | keyword | 0.88 |
| gender-neutral | existing_tag | tag_map | 0.9 |

### 9179165753657 — בגד גוף כותנה טטרה - פריחת האביב
**type:** type-bodysuit | **score:** 75.0 | **verdict:** `REVIEW_ONLY` | **has_yaml:** True
**reason:** score 75.0 < 85 minimum
**size_status:** NO_SIZE_FOUND
**proposed tags (3):** `type-bodysuit, season-spring-fall, fabric-cotton`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-bodysuit | title | keyword | 0.88 |
| season-spring-fall | title_handle | keyword | 0.82 |
| fabric-cotton | title | keyword | 0.9 |

### 9179168964921 — בגד גוף כיווצים אלגנטי - נטלי
**type:** type-bodysuit | **score:** 70.0 | **verdict:** `REVIEW_ONLY` | **has_yaml:** True
**reason:** score 70.0 < 85 minimum
**size_status:** NO_SIZE_FOUND
**proposed tags (2):** `type-bodysuit, style-elegant`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-bodysuit | title | keyword | 0.88 |
| style-elegant | title | keyword | 0.82 |

### 9179152154937 — בגד גוף מלמלות - קיטי
**type:** type-bodysuit | **score:** 70.0 | **verdict:** `REVIEW_ONLY` | **has_yaml:** True
**reason:** score 70.0 < 85 minimum
**size_status:** NO_SIZE_FOUND
**proposed tags (1):** `type-bodysuit`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-bodysuit | title | keyword | 0.88 |

### 9179167129913 — בגד גוף מלמלות וכיווצים פרחוני - שיילי
**type:** type-bodysuit | **score:** 70.0 | **verdict:** `REVIEW_ONLY` | **has_yaml:** True
**reason:** score 70.0 < 85 minimum
**size_status:** NO_SIZE_FOUND
**proposed tags (2):** `type-bodysuit, style-floral`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-bodysuit | title | keyword | 0.88 |
| style-floral | title | keyword | 0.82 |

### 9874906382649 — בגד גוף פו הדוב דגם לירון
**type:** type-bodysuit | **score:** 100.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** True
**size_status:** OK
**proposed tags (11):** `type-bodysuit, size-18-24m, size-0-3m, size-9-12m, size-12-18m, size-3-6m, size-6-9m, season-summer, fabric-cotton, gender-girl, style-teddy`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-bodysuit | existing_tag | tag_map | 0.88 |
| size-18-24m | variant | variant_option | 0.95 |
| size-0-3m | variant | variant_option | 0.95 |
| size-9-12m | variant | variant_option | 0.95 |
| size-12-18m | variant | variant_option | 0.95 |
| size-3-6m | variant | variant_option | 0.95 |
| size-6-9m | variant | variant_option | 0.95 |
| season-summer | title_handle | keyword | 0.88 |
| fabric-cotton | existing_tag | keyword | 0.9 |
| gender-girl | handle | keyword | 0.9 |
| style-teddy | existing_tag | keyword | 0.82 |

### 9688885985593 — אוברול פיל מתוק דגם נאיה
**type:** type-romper | **score:** 100.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** True
**size_status:** OK
**proposed tags (6):** `type-romper, size-3-6m, size-6-9m, size-newborn, season-spring-fall, gender-girl`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-romper | existing_tag | tag_map | 0.88 |
| size-3-6m | variant | variant_option | 0.95 |
| size-6-9m | variant | variant_option | 0.95 |
| size-newborn | variant | variant_option | 0.95 |
| season-spring-fall | title_handle | keyword | 0.82 |
| gender-girl | handle | keyword | 0.9 |

### 9688934973753 — אוברול פיל פסים דגם ליאו
**type:** type-romper | **score:** 95.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** True
**size_status:** OK
**proposed tags (7):** `type-romper, size-0-3m, size-3-6m, size-6-9m, size-9-12m, size-12-18m, style-striped`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-romper | existing_tag | tag_map | 0.88 |
| size-0-3m | variant | variant_option | 0.95 |
| size-3-6m | variant | variant_option | 0.95 |
| size-6-9m | variant | variant_option | 0.95 |
| size-9-12m | variant | variant_option | 0.95 |
| size-12-18m | variant | variant_option | 0.95 |
| style-striped | title | keyword | 0.82 |

### 9874906546489 — חליפת דובי  מלאה בסטייל דגם מאור
**type:** type-set | **score:** 100.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** True
**size_status:** OK
**proposed tags (6):** `type-set, size-3-6m, size-9-12m, season-spring-fall, gender-boy, style-teddy`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-set | existing_tag | tag_map | 0.88 |
| size-3-6m | variant | variant_option | 0.95 |
| size-9-12m | variant | variant_option | 0.95 |
| season-spring-fall | title_handle | keyword | 0.82 |
| gender-boy | handle | keyword | 0.9 |
| style-teddy | existing_tag | keyword | 0.82 |

### 9688660377913 — חליפת קואלה דגם שני
**type:** type-set | **score:** 100.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** True
**size_status:** OK
**proposed tags (10):** `type-set, size-0-3m, size-3-6m, size-6-9m, size-9-12m, size-12-18m, size-18-24m, season-spring-fall, gender-girl, style-casual`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-set | existing_tag | tag_map | 0.88 |
| size-0-3m | variant | variant_option | 0.95 |
| size-3-6m | variant | variant_option | 0.95 |
| size-6-9m | variant | variant_option | 0.95 |
| size-9-12m | variant | variant_option | 0.95 |
| size-12-18m | variant | variant_option | 0.95 |
| size-18-24m | variant | variant_option | 0.95 |
| season-spring-fall | title_handle | keyword | 0.82 |
| gender-girl | handle | keyword | 0.9 |
| style-casual | title | keyword | 0.82 |

### 9688976326969 — חליפה דוב מופתע דגם ליאל
**type:** type-set | **score:** 100.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** True
**size_status:** OK
**proposed tags (8):** `type-set, size-0-3m, size-3-6m, size-6-9m, size-9-12m, size-12-18m, gender-boy, style-casual`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-set | existing_tag | tag_map | 0.88 |
| size-0-3m | variant | variant_option | 0.95 |
| size-3-6m | variant | variant_option | 0.95 |
| size-6-9m | variant | variant_option | 0.95 |
| size-9-12m | variant | variant_option | 0.95 |
| size-12-18m | variant | variant_option | 0.95 |
| gender-boy | handle | keyword | 0.9 |
| style-casual | title | keyword | 0.82 |

### 9688964989241 — חליפה דוב מקסימה דגם אריאל
**type:** type-set | **score:** 100.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** True
**size_status:** OK
**proposed tags (6):** `type-set, size-9-12m, season-winter, fabric-polyester, gender-boy, style-teddy`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-set | existing_tag | tag_map | 0.88 |
| size-9-12m | variant | variant_option | 0.95 |
| season-winter | title_handle | keyword | 0.85 |
| fabric-polyester | title | keyword | 0.9 |
| gender-boy | handle | keyword | 0.9 |
| style-teddy | existing_tag | keyword | 0.82 |

### 9688674566457 — חליפה לבנים דגם אימרי
**type:** type-set | **score:** 100.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** True
**size_status:** OK
**proposed tags (7):** `type-set, size-0-3m, size-3-6m, size-12-18m, size-18-24m, gender-boy, style-casual`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-set | existing_tag | tag_map | 0.88 |
| size-0-3m | variant | variant_option | 0.95 |
| size-3-6m | variant | variant_option | 0.95 |
| size-12-18m | variant | variant_option | 0.95 |
| size-18-24m | variant | variant_option | 0.95 |
| gender-boy | existing_tag | tag_map | 0.9 |
| style-casual | title | keyword | 0.82 |

### 9688976294201 — חליפה מהממת רקמת דובי חמוד דגם אלי
**type:** type-set | **score:** 100.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** True
**size_status:** OK
**proposed tags (8):** `type-set, size-6-9m, size-9-12m, size-12-18m, size-18-24m, season-winter, gender-boy, style-casual`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-set | existing_tag | tag_map | 0.88 |
| size-6-9m | variant | variant_option | 0.95 |
| size-9-12m | variant | variant_option | 0.95 |
| size-12-18m | variant | variant_option | 0.95 |
| size-18-24m | variant | variant_option | 0.95 |
| season-winter | title_handle | keyword | 0.85 |
| gender-boy | handle | keyword | 0.9 |
| style-casual | title | keyword | 0.82 |

### 10190523302201 — Children’s Summer New Arrival Boys’ Regular Striped Teddy Bear Short T-Shirt and Shorts Casual Sport Two-Piece Set
**type:** type-set | **score:** 100.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** False
**size_status:** OK
**proposed tags (9):** `type-set, size-18-24m, size-9-12m, size-12-18m, size-3-6m, size-6-9m, season-summer, gender-boy, style-casual`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-set | title | keyword | 0.85 |
| size-18-24m | variant | variant_option | 0.95 |
| size-9-12m | variant | variant_option | 0.95 |
| size-12-18m | variant | variant_option | 0.95 |
| size-3-6m | variant | variant_option | 0.95 |
| size-6-9m | variant | variant_option | 0.95 |
| season-summer | title_handle | keyword | 0.88 |
| gender-boy | title | keyword | 0.9 |
| style-casual | title | keyword | 0.82 |

### 10190523203897 — Boys Khaki Letter Print Half Zip Hooded 2Pcs Summer Set, Short Sleeve Hoodie + Shorts, Kids Casual Outfit 3-12Y
**type:** type-set | **score:** 80.0 | **verdict:** `REVIEW_ONLY` | **has_yaml:** False
**reason:** score 80.0 < 85 minimum
**size_status:** NO_SIZE_FOUND
**proposed tags (4):** `type-set, season-summer, gender-boy, style-casual`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-set | title | keyword | 0.85 |
| season-summer | title_handle | keyword | 0.88 |
| gender-boy | title | keyword | 0.9 |
| style-casual | title | keyword | 0.82 |

### 10190523138361 — Boys' summer white striped short-sleeved shorts with pockets, fashionable two-piece set, suitable for children over 3 years old
**type:** type-set | **score:** 100.0 | **verdict:** `SAFE_FOR_PHASE7A` | **has_yaml:** False
**size_status:** OK
**proposed tags (5):** `type-set, size-3y, season-summer, gender-boy, style-striped`

**source trace:**
| tag | source | rule | conf |
|-----|--------|------|------|
| type-set | title | keyword | 0.85 |
| size-3y | title | regex_narrow | 0.88 |
| season-summer | title_handle | keyword | 0.88 |
| gender-boy | title | keyword | 0.9 |
| style-striped | title | keyword | 0.82 |

---

## 6. רשימת SAFE_FOR_PHASE7A

| product_id | כותרת | type | score |
|-----------|-------|------|-------|
| 9179166671161 | בגד גוף שמלה ג׳ינס מכותנה - הרפר | type-bodysuit | 95.0 |
| 9606694437177 | חליפת פולו קצרה סרוגה לתינוקות | type-set | 85.0 |
| 9731768746297 | סט בגדי תינוקות גינס ושמלה דגם טליה | type-dress | 85.0 |
| 9874906382649 | בגד גוף פו הדוב דגם לירון | type-bodysuit | 100.0 |
| 9688885985593 | אוברול פיל מתוק דגם נאיה | type-romper | 100.0 |
| 9688934973753 | אוברול פיל פסים דגם ליאו | type-romper | 95.0 |
| 9874906546489 | חליפת דובי  מלאה בסטייל דגם מאור | type-set | 100.0 |
| 9688660377913 | חליפת קואלה דגם שני | type-set | 100.0 |
| 9688976326969 | חליפה דוב מופתע דגם ליאל | type-set | 100.0 |
| 9688964989241 | חליפה דוב מקסימה דגם אריאל | type-set | 100.0 |
| 9688674566457 | חליפה לבנים דגם אימרי | type-set | 100.0 |
| 9688976294201 | חליפה מהממת רקמת דובי חמוד דגם אלי | type-set | 100.0 |
| 10190523302201 | Children’s Summer New Arrival Boys’ Regular Stripe | type-set | 100.0 |
| 10190523138361 | Boys' summer white striped short-sleeved shorts wi | type-set | 100.0 |

---

## 7. בדיקת גיוון

| בדיקה | תוצאה |
|-------|-------|
| מספר SAFE_FOR_PHASE7A | 14 |
| סוגי מוצר ב-SAFE | 4 (type-dress, type-romper, type-set, type-bodysuit) |
| לפחות 10 SAFE מגוונים | כן ✅ |

---

## 8. המלצת batch חי ראשון של Phase 7A

**כלל:** לא 20 מוצרים live בבת אחת — batch של 10 בלבד.

| המלצה | פרטים |
|-------|-------|
| גודל batch | 10 מוצרים (לא 20) |
| עדיפות | SAFE_FOR_PHASE7A בלבד |
| גיוון | לפחות 3 סוגים שונים בbatch |
| כלל | 1 מוצר בכל פעם עם verify |

**batch מומלץ (10 הראשונים):**

| # | product_id | כותרת | type | score |
|---|-----------|-------|------|-------|
| 1 | 9874906382649 | בגד גוף פו הדוב דגם לירון | type-bodysuit | 100.0 |
| 2 | 9688885985593 | אוברול פיל מתוק דגם נאיה | type-romper | 100.0 |
| 3 | 9874906546489 | חליפת דובי  מלאה בסטייל דגם מאור | type-set | 100.0 |
| 4 | 9688660377913 | חליפת קואלה דגם שני | type-set | 100.0 |
| 5 | 9688976326969 | חליפה דוב מופתע דגם ליאל | type-set | 100.0 |
| 6 | 9688964989241 | חליפה דוב מקסימה דגם אריאל | type-set | 100.0 |
| 7 | 9688674566457 | חליפה לבנים דגם אימרי | type-set | 100.0 |
| 8 | 9688976294201 | חליפה מהממת רקמת דובי חמוד דגם אלי | type-set | 100.0 |
| 9 | 10190523302201 | Children’s Summer New Arrival Boys’ Regular S | type-set | 100.0 |
| 10 | 10190523138361 | Boys' summer white striped short-sleeved shor | type-set | 100.0 |

---

## 9. Backup / Verify / Rollback Plan

| שלב | תיאור |
|-----|-------|
| גיבוי | GET tags לכל מוצר → שמור JSON לפני כל כתיבה |
| כתיבה | PUT tags אחד בכל פעם (merge: current + new) |
| verify | GET אחרי כל PUT — בדוק כל tag קיים, אין age-*, title לא השתנה |
| rollback | אם verify נכשל → PUT tags מקוריות מהגיבוי |
| מוצר פגוע | עצור batch, rollback מיידי |

---

## 10. Verdict סופי

**READY_FOR_PHASE7A_T3_APPROVAL**

| בדיקה | תוצאה |
|-------|-------|
| SAFE_FOR_PHASE7A | 14 |
| REVIEW_ONLY | 6 |
| REJECT | 0 |
| גיוון סוגים ב-SAFE | 4 סוגים |
| לפחות 10 SAFE | כן ✅ |
| כתיבה ל-Shopify | **NO** |
| collections נוצרו | **NO** |
| Mega Menu נוצר | **NO** |

---

*Phase 7A dry run only — אין שינויים ב-Shopify. כל ביצוע מותנה ב-T3 approval.*
