# Layer 6 — Phase 2b CAT-B Age Extraction Hardening
## BabyMania Organic | Date: 2026-05-05 | Status: COMPLETE

---

## 1. Summary — Before vs After

| מדד | Phase 2 | Phase 2b | שינוי |
|-----|---------|---------|-------|
| CAT-B coverage (products with valid age tag) | **10**/30 | **7**/30 | -3 |
| Quality PASS | **13** | **14** | +1 |
| Quality NEEDS_REVIEW | **13** | **12** | -1 |
| Quality BLOCKED | **4** | **4** | +0 |
| avg score | **71.6** | **70.3** | -1.3 |
| misleading age tags created | N/A | **0 ✅** | — |

---

## 2. Age Status Distribution (Phase 2b)

| סטטוס | מספר מוצרים | הסבר |
|-------|-----------|------|
| ✅ OK — valid age tag assigned | **7** | גיל ממקור אמין |
| ⚠️ RANGE_TOO_BROAD | **9** | טווח גיל רחב מדי — לא ניתן לבחור tag יחיד |
| 🚫 DOLL_NO_AGE_APPLICABLE | **5** | מוצר בובה/reborn — גיל לא רלוונטי |
| ❌ NO_AGE_FOUND | **9** | אין מקור גיל ברור |

---

## 3. Age Change Types

| שינוי | מספר | משמעות |
|-------|------|--------|
| ADDED | 5 | מוצר קיבל age tag תקין לראשונה |
| REMOVED_WRONG | 8 | age tag שגוי הוסר |
| CORRECTED | 2 | age tag הוחלף בכזה יותר מדויק |
| IMPROVED_SOURCE | 0 | אותו tag, מקור טוב יותר |
| RANGE_FLAGGED | 3 | טווח רחב זוהה ותויג במפורש |
| DOLL_FLAGGED | 3 | בובה/doll זוהתה — גיל לא רלוונטי |
| STILL_MISSING | 9 | עדיין ללא מקור גיל |

---

## 4. Age Patterns Added in Phase 2b

- `toddler` keyword → age-2-3y (0.75) — fired on **4** product(s)
- `1-3y` in handle → approximated to age-2-3y (0.80) — fired on **1** product(s)
- `0-3 חודש` — existing tag Hebrew → age-0-3m (0.90) — fired on **1** product(s)
- `12-18 חודש` — existing tag Hebrew → age-12-18m (0.90) — fired on **1** product(s)
- `6-12 חודש` — existing tag Hebrew → age-6-12m (0.90) — fired on **1** product(s)
- `first walker/walkers` → age-6-12m (0.75) — fired on **1** product(s)

---

## 5. Patterns Still Requiring Ayal Decision

| מוצר | סוג בעיה | הסבר |
|------|---------|------|
| `0-to-18-months-baby-girl-boy-sweater-romper-autumn-wint` | RANGE_TOO_BROAD | טווח `0-18m` — אין tag מתאים |
| `3-24-months-newborn-baby-boy-winter-clothing-set-lattic` | RANGE_TOO_BROAD | טווח `3-24m` — אין tag מתאים |
| `summer-unisex-newborn-baby-clothes-solid-color-baby-rom` | RANGE_TOO_BROAD | טווח `3-18m` — אין tag מתאים |
| `ma-baby-0-18m-baby-girl-clothes-sets-newborn-infant-tod` | RANGE_TOO_BROAD | טווח `0-18m` — אין tag מתאים |
| `אוברול-כותנה-אמירוש` | NO_AGE_FOUND | אין מקור גיל — YAML ריק, כותרת כללית |
| `אוברול-ארוך` | NO_AGE_FOUND | אין מקור גיל — YAML ריק, כותרת כללית |
| `אוברול-ארוך-עם-רוכסן` | NO_AGE_FOUND | אין מקור גיל — YAML ריק, כותרת כללית |
| `childrens-fashion-boots-black-low-lightweight-boys-girl` | RANGE_TOO_BROAD | טווח `0-8y` — אין tag מתאים |
| `winter-snow-baby-boots-newborn-warm-booties-soft-sole-f` | RANGE_TOO_BROAD | טווח `0-18m` — אין tag מתאים |
| `trendy-comfortable-sneakers-for-baby-girls-and-boys-lig` | NO_AGE_FOUND | אין מקור גיל — YAML ריק, כותרת כללית |
| `2024-summer-baby-led-light-sandals-for-girls-cute-hello` | NO_AGE_FOUND | אין מקור גיל — YAML ריק, כותרת כללית |
| `autumn-winter-baby-boots-kids-girl-boys-winter-warm-sho` | RANGE_TOO_BROAD | טווח `0-18m` — אין tag מתאים |
| `kids-casual-shoes-sneakers-boys-sport-breathable-tennis` | NO_AGE_FOUND | אין מקור גיל — YAML ריק, כותרת כללית |
| `npk-50cm-full-body-maddie-reborn-baby-girl-doll-soft-si` | NO_AGE_FOUND | אין מקור גיל — YAML ריק, כותרת כללית |
| `0-18-months-old-newborn-baby-boy-jumpsuit-cute-little-b` | RANGE_TOO_BROAD | טווח `0-18m` — אין tag מתאים |
| `2pcs-baby-boys-sports-and-leisure-set-lapel-color-block` | RANGE_TOO_BROAD | טווח `0-Xy` — אין tag מתאים |
| `babyfree100` | NO_AGE_FOUND | אין מקור גיל — YAML ריק, כותרת כללית |
| `baby-white-noise-machine-kids-sleep-sound-player-night-` | NO_AGE_FOUND | אין מקור גיל — YAML ריק, כותרת כללית |

---

## 6. Per-Product Detail

### ⚠️ Alure™ Baby
**ID:** `10029649002809` | **Group:** clothing_yaml | **YAML:** YES
**Score:** 74.3 (NEEDS_REVIEW) → 74.3 (NEEDS_REVIEW) ⚠️ (+0.0)
**CAT-B status:** RANGE_TOO_BROAD | **Change:** RANGE_FLAGGED
**Range note:** 0-18m

---

### ✅+ Lino™ – סט סריג רך לתינוקות בעיצוב אירופאי
**ID:** `10029649133881` | **Group:** clothing_yaml | **YAML:** YES
**Score:** 75.3 (PASS) → 90.2 (PASS) ✅ (+14.9)
**CAT-B status:** OK | **Change:** ADDED
**Age after:** `age-2-3y` (80%, handle)

---

### 🔧 LumiBear™ חליפת פרמיום לחורף
**ID:** `10029648970041` | **Group:** clothing_yaml | **YAML:** YES
**Score:** 82.9 (PASS) → 68.9 (NEEDS_REVIEW) ⚠️ (-14.0)
**CAT-B status:** RANGE_TOO_BROAD | **Change:** REMOVED_WRONG
**Age before:** `age-0-3m`
**Range note:** 3-24m

---

### 🔧 LUMI™  – אוברול נוחות יוקרתי לתינוקות
**ID:** `10029649101113` | **Group:** clothing_yaml | **YAML:** YES
**Score:** 96.9 (PASS) → 81.7 (PASS) ✅ (-15.2)
**CAT-B status:** RANGE_TOO_BROAD | **Change:** REMOVED_WRONG
**Age before:** `age-0-3m`
**Range note:** 3-18m

---

### 🔧 Veloura Baby™ חליפה פרחונית
**ID:** `9855017550137` | **Group:** clothing_yaml | **YAML:** YES
**Score:** 96.1 (PASS) → 81.8 (PASS) ✅ (-14.3)
**CAT-B status:** RANGE_TOO_BROAD | **Change:** REMOVED_WRONG
**Age before:** `age-0-3m`
**Range note:** 0-18m

---

### 🔧 WarmNest™– אוברול חורף מחבק לתינוקות
**ID:** `9657091293497` | **Group:** clothing_yaml | **YAML:** YES
**Score:** 88.7 (PASS) → 90.1 (PASS) ✅ (+1.4)
**CAT-B status:** OK | **Change:** CORRECTED
**Age before:** `age-0-3m`
**Age after:** `age-0-3m` (90%, existing_tag_hebrew), `age-12-18m` (90%, existing_tag_hebrew), `age-6-12m` (90%, existing_tag_hebrew)

---

### ✅+ אוברול Leopard Cozy
**ID:** `9687596728633` | **Group:** clothing_yaml | **YAML:** YES
**Score:** 60.3 (NEEDS_REVIEW) → 74.9 (NEEDS_REVIEW) ⚠️ (+14.6)
**CAT-B status:** OK | **Change:** ADDED
**Age after:** `age-2-3y` (75%, handle)

---

### ❌ אוברול אלגנט דגם עומרי
**ID:** `9179155693881` | **Group:** clothing_yaml | **YAML:** YES
**Score:** 65.6 (NEEDS_REVIEW) → 65.6 (NEEDS_REVIEW) ⚠️ (+0.0)
**CAT-B status:** NO_AGE_FOUND | **Change:** STILL_MISSING

---

### ❌ אוברול ארוך
**ID:** `9096606908729` | **Group:** clothing_yaml | **YAML:** YES
**Score:** 66.8 (NEEDS_REVIEW) → 66.8 (NEEDS_REVIEW) ⚠️ (+0.0)
**CAT-B status:** NO_AGE_FOUND | **Change:** STILL_MISSING

---

### ❌ אוברול ארוך עם רוכסן
**ID:** `9096599994681` | **Group:** clothing_yaml | **YAML:** YES
**Score:** 60.3 (NEEDS_REVIEW) → 60.3 (NEEDS_REVIEW) ⚠️ (+0.0)
**CAT-B status:** NO_AGE_FOUND | **Change:** STILL_MISSING

---

### ✅+ מגפי חורף לילדות דגם לין
**ID:** `9607363625273` | **Group:** shoes_yaml | **YAML:** YES
**Score:** 75.3 (PASS) → 90.0 (PASS) ✅ (+14.7)
**CAT-B status:** OK | **Change:** ADDED
**Age after:** `age-2-3y` (75%, handle)

---

### ⚠️ מגפי חורף נוצצים עם כוכבים
**ID:** `9615669461305` | **Group:** shoes_yaml | **YAML:** YES
**Score:** 75.3 (PASS) → 75.3 (PASS) ✅ (+0.0)
**CAT-B status:** RANGE_TOO_BROAD | **Change:** RANGE_FLAGGED
**Range note:** 0-8y

---

### 🔧 מגפי חורף צעד ראשון
**ID:** `9615375794489` | **Group:** shoes_yaml | **YAML:** YES
**Score:** 89.5 (PASS) → 75.3 (PASS) ✅ (-14.2)
**CAT-B status:** RANGE_TOO_BROAD | **Change:** REMOVED_WRONG
**Age before:** `age-0-3m`
**Range note:** 0-18m

---

### ❌ נעל אולסטאר צעד ראשון לתינוק
**ID:** `9607365132601` | **Group:** shoes_yaml | **YAML:** YES
**Score:** 60.3 (NEEDS_REVIEW) → 60.3 (NEEDS_REVIEW) ⚠️ (+0.0)
**CAT-B status:** NO_AGE_FOUND | **Change:** STILL_MISSING

---

### ✅+ נעל אופנתית אלגנטית לתינוק
**ID:** `9607363756345` | **Group:** shoes_yaml | **YAML:** YES
**Score:** 66.6 (NEEDS_REVIEW) → 81.3 (PASS) ✅ (+14.7)
**CAT-B status:** OK | **Change:** ADDED
**Age after:** `age-2-3y` (75%, handle)

---

### ✅+ נעל אלגנטית צעד ראשון לבנות
**ID:** `9615375565113` | **Group:** shoes_yaml | **YAML:** YES
**Score:** 66.8 (NEEDS_REVIEW) → 81.5 (PASS) ✅ (+14.7)
**CAT-B status:** OK | **Change:** ADDED
**Age after:** `age-6-12m` (75%, handle)

---

### ❌ נעל הלו קיטי עם אורות לילדות
**ID:** `9607363232057` | **Group:** shoes_yaml | **YAML:** YES
**Score:** 81.8 (PASS) → 81.8 (PASS) ✅ (+0.0)
**CAT-B status:** NO_AGE_FOUND | **Change:** STILL_MISSING

---

### 🔧 נעל חורף מחממת ואלגנטית צעד ראשון
**ID:** `9615376023865` | **Group:** shoes_yaml | **YAML:** YES
**Score:** 95.3 (PASS) → 95.7 (PASS) ✅ (+0.4)
**CAT-B status:** OK | **Change:** CORRECTED
**Age before:** `age-0-3m`
**Age after:** `age-2-3y` (75%, handle)

---

### 🔧 נעל חורף צעד ראשון אופנתיות
**ID:** `9615376089401` | **Group:** shoes_yaml | **YAML:** YES
**Score:** 89.5 (PASS) → 75.3 (PASS) ✅ (-14.2)
**CAT-B status:** RANGE_TOO_BROAD | **Change:** REMOVED_WRONG
**Age before:** `age-0-3m`
**Range note:** 0-18m

---

### ❌ נעל ספורט קז'ואל נוחה לתינוק
**ID:** `9607363461433` | **Group:** shoes_yaml | **YAML:** YES
**Score:** 81.7 (PASS) → 81.7 (PASS) ✅ (+0.0)
**CAT-B status:** NO_AGE_FOUND | **Change:** STILL_MISSING

---

### 🔧 46CM Finished Reborn Baby Doll Felicia Newborn Open Blue Eyes Doll Sof
**ID:** `10190522810681` | **Group:** reborn_gap | **YAML:** GAP
**Score:** 73.1 (NEEDS_REVIEW) → 58.8 (NEEDS_REVIEW) ⚠️ (-14.3)
**CAT-B status:** DOLL_NO_AGE_APPLICABLE | **Change:** REMOVED_WRONG
**Age before:** `age-0-3m`
**Range note:** reborn_or_doll_product

---

### 🔧 50CM  Whole Silicone Vinyl Reborn Doll 20 Inch Girl Painted Newborn Ba
**ID:** `10190523040057` | **Group:** reborn_gap | **YAML:** GAP
**Score:** 74.3 (NEEDS_REVIEW) → 60.3 (NEEDS_REVIEW) ⚠️ (-14.0)
**CAT-B status:** DOLL_NO_AGE_APPLICABLE | **Change:** REMOVED_WRONG
**Age before:** `age-0-3m`
**Range note:** reborn_or_doll_product

---

### 🚫 NPK 46CM Meadow Reborn Baby Doll - Soft Touch 3D Skin Hand Painted Mul
**ID:** `10190522777913` | **Group:** reborn_gap | **YAML:** GAP
**Score:** 45.0 (BLOCKED) → 45.0 (BLOCKED) ❌ (+0.0)
**CAT-B status:** DOLL_NO_AGE_APPLICABLE | **Change:** DOLL_FLAGGED
**Range note:** reborn_or_doll_product

---

### ❌ NPK 50CM Full Body Maddie Reborn Baby Girl Doll - Soft Silicone Lifeli
**ID:** `10190523072825` | **Group:** reborn_gap | **YAML:** GAP
**Score:** 48.0 (BLOCKED) → 48.0 (BLOCKED) ❌ (+0.0)
**CAT-B status:** NO_AGE_FOUND | **Change:** STILL_MISSING

---

### 🚫 Open Mouth 33cm Pascale Full Body Silicone Reborn Girl Doll With Paint
**ID:** `10190523007289` | **Group:** reborn_gap | **YAML:** GAP
**Score:** 48.0 (BLOCKED) → 48.0 (BLOCKED) ❌ (+0.0)
**CAT-B status:** DOLL_NO_AGE_APPLICABLE | **Change:** DOLL_FLAGGED
**Range note:** reborn_or_doll_product

---

### 🔧 0-18 Months old Newborn Baby boy Jumpsuit Cute Little Bear Short sleev
**ID:** `10190523334969` | **Group:** gap_clothing | **YAML:** GAP
**Score:** 89.5 (PASS) → 75.3 (PASS) ✅ (-14.2)
**CAT-B status:** RANGE_TOO_BROAD | **Change:** REMOVED_WRONG
**Age before:** `age-0-3m`
**Range note:** 0-18m

---

### ⚠️ 2Pcs Baby Boys' Sports and Leisure Set lapel Color blocked Short Sleev
**ID:** `10190522941753` | **Group:** gap_clothing | **YAML:** GAP
**Score:** 68.9 (NEEDS_REVIEW) → 68.9 (NEEDS_REVIEW) ⚠️ (+0.0)
**CAT-B status:** RANGE_TOO_BROAD | **Change:** RANGE_FLAGGED
**Range note:** 0-Xy

---

### 🚫 BABY MANIA™  בובה  נושמת מבית
**ID:** `9166992900409` | **Group:** gap_clothing | **YAML:** GAP
**Score:** 54.0 (NEEDS_REVIEW) → 54.0 (NEEDS_REVIEW) ⚠️ (+0.0)
**CAT-B status:** DOLL_NO_AGE_APPLICABLE | **Change:** DOLL_FLAGGED
**Range note:** reborn_or_doll_product

---

### ❌ Babyfree100
**ID:** `9839001633081` | **Group:** gap_clothing | **YAML:** GAP
**Score:** 41.0 (BLOCKED) → 41.0 (BLOCKED) ❌ (+0.0)
**CAT-B status:** NO_AGE_FOUND | **Change:** STILL_MISSING

---

### ❌ BabySleep Pro – רעש לבן ואור מרגיע לשינה עמוקה לתינוק
**ID:** `9839252472121` | **Group:** gap_clothing | **YAML:** GAP
**Score:** 58.3 (NEEDS_REVIEW) → 58.3 (NEEDS_REVIEW) ⚠️ (+0.0)
**CAT-B status:** NO_AGE_FOUND | **Change:** STILL_MISSING

---

## 7. Safety Checks

| בדיקה | תוצאה |
|-------|-------|
| misleading age tags (wide-range product got specific age) | ✅ NONE |
| `3-6M6-9M` malformed tag used as source | ✅ IGNORED |
| color inference → gender | ✅ NOT DONE |
| `baby` alone → age-0-3m | ✅ NOT DONE |
| age from image/price | ✅ NOT DONE |
| Shopify live changes | ✅ ZERO |

---

*Phase 2b הורץ: 2026-05-05 | read-only analysis | T0 | אין שינוי ב-Shopify*