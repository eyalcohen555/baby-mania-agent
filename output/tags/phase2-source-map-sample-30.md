# Layer 6 — Phase 2 Source Mapping Sample
## BabyMania Organic | Date: 2026-05-05 | Status: COMPLETE

---

## 1. Sample Summary

| מדד | ערך |
|-----|-----|
| סה"כ מוצרים בsample | **30** |
| clothing + YAML | **10** |
| shoes + YAML | **10** |
| reborn / toys (YAML_GAP) | **5** |
| YAML_GAP clothing | **5** |
| Quality PASS | **13** |
| Quality NEEDS_REVIEW | **13** |
| Quality BLOCKED | **4** |

---

## 2. Source Mapping Per Product

### [CLOTHING_YAML] Alure™ Baby
**ID:** `10029649002809` | **Handle:** `0-to-18-months-baby-girl-boy-sweater-romper-autumn-winter-cl`
**Group:** clothing_yaml | **YAML:** HAS_YAML | **Score:** 74.3 ⚠️ NEEDS_REVIEW

**Current tags:**
_(none)_

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-romper` | CAT-A | 90% | `handle` |
| `season-winter` | CAT-C | 85% | `body` |
| `occ-everyday` | CAT-E | 60% | `type_default` |
| `gender-unisex` | CAT-F | 85% | `title` |
| `style-striped` | CAT-G | 80% | `handle` |

**Missing required:** CAT-B

---

### [CLOTHING_YAML] Lino™ – סט סריג רך לתינוקות בעיצוב אירופאי
**ID:** `10029649133881` | **Handle:** `toddler-baby-boys-clothes-fall-outfit-striped-crew-neck-long`
**Group:** clothing_yaml | **YAML:** HAS_YAML | **Score:** 75.3 ✅ PASS

**Current tags:**
`baby-gift`, `baby-knit-set`, `baby-shower-gift`, `european-baby-style`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing`, `soft-knit`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-set` | CAT-A | 90% | `handle` |
| `season-spring-fall` | CAT-C | 85% | `body` |
| `occ-everyday` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 90% | `existing_tag` |
| `style-casual` | CAT-G | 80% | `handle` |

**Missing required:** CAT-B

---

### [CLOTHING_YAML] LumiBear™ חליפת פרמיום לחורף
**ID:** `10029648970041` | **Handle:** `3-24-months-newborn-baby-boy-winter-clothing-set-lattice-plu`
**Group:** clothing_yaml | **YAML:** HAS_YAML | **Score:** 82.9 ✅ PASS

**Current tags:**
`baby-gift`, `baby-shower-gift`, `baby-suit`, `neutral-baby-outfit`, `newborn-clothing`, `winter-baby-wear`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-romper` | CAT-A | 90% | `handle` |
| `age-0-3m` | CAT-B | 60% | `title_heuristic` |
| `season-winter` | CAT-C | 85% | `body` |
| `occ-everyday` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 90% | `existing_tag` |

---

### [CLOTHING_YAML] LUMI™  – אוברול נוחות יוקרתי לתינוקות
**ID:** `10029649101113` | **Handle:** `summer-unisex-newborn-baby-clothes-solid-color-baby-rompers-`
**Group:** clothing_yaml | **YAML:** HAS_YAML | **Score:** 96.9 ✅ PASS

**Current tags:**
`אוברול`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-romper` | CAT-A | 90% | `handle` |
| `age-0-3m` | CAT-B | 90% | `title_regex` |
| `season-summer` | CAT-C | 85% | `body` |
| `fabric-cotton` | CAT-D | 80% | `yaml_desc` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 85% | `title` |
| `style-elegant` | CAT-G | 80% | `handle` |

---

### [CLOTHING_YAML] Veloura Baby™ חליפה פרחונית
**ID:** `9855017550137` | **Handle:** `ma-baby-0-18m-baby-girl-clothes-sets-newborn-infant-toddler-`
**Group:** clothing_yaml | **YAML:** HAS_YAML | **Score:** 96.1 ✅ PASS

**Current tags:**
`baby-gift`, `baby-shower-gift`, `baby-suit`, `everyday-baby-wear`, `floral-baby`, `newborn-clothing`, `soft-knit`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-romper` | CAT-A | 90% | `handle` |
| `age-0-3m` | CAT-B | 60% | `title_heuristic` |
| `season-summer` | CAT-C | 85% | `body` |
| `occ-beach` | CAT-E | 80% | `title` |
| `occ-everyday` | CAT-E | 80% | `title` |
| `gender-girl` | CAT-F | 90% | `title` |
| `style-elegant` | CAT-G | 80% | `handle` |

---

### [CLOTHING_YAML] WarmNest™– אוברול חורף מחבק לתינוקות
**ID:** `9657091293497` | **Handle:** `newborn-baby-winter-jacket-warm-hooded-infant-romper-thicken`
**Group:** clothing_yaml | **YAML:** HAS_YAML | **Score:** 88.7 ✅ PASS

**Current tags:**
`0-3 חודש`, `12-18 חודש`, `6-12 חודש`, `אוברול`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-romper` | CAT-A | 90% | `handle` |
| `age-0-3m` | CAT-B | 60% | `title_heuristic` |
| `season-winter` | CAT-C | 85% | `body` |
| `occ-everyday` | CAT-E | 60% | `type_default` |
| `gender-unisex` | CAT-F | 85% | `title` |
| `style-cartoon` | CAT-G | 80% | `handle` |

---

### [CLOTHING_YAML] אוברול Leopard Cozy
**ID:** `9687596728633` | **Handle:** `babys-casual-leopard-pattern-long-sleeve-romper-hairband-tod`
**Group:** clothing_yaml | **YAML:** HAS_YAML | **Score:** 60.3 ⚠️ NEEDS_REVIEW

**Current tags:**
`אוברול`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-romper` | CAT-A | 90% | `handle` |
| `occ-everyday` | CAT-E | 80% | `title` |
| `gender-girl` | CAT-F | 90% | `title` |
| `style-casual` | CAT-G | 80% | `handle` |

**Missing required:** CAT-C, CAT-B

---

### [CLOTHING_YAML] אוברול אלגנט דגם עומרי
**ID:** `9179155693881` | **Handle:** `אוברול-כותנה-אמירוש`
**Group:** clothing_yaml | **YAML:** HAS_YAML | **Score:** 65.6 ⚠️ NEEDS_REVIEW

**Current tags:**
`אוברול`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-romper` | CAT-A | 90% | `title` |
| `fabric-cotton` | CAT-D | 80% | `yaml_desc` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 60% | `default_unisex` |

**Missing required:** CAT-C, CAT-B

---

### [CLOTHING_YAML] אוברול ארוך
**ID:** `9096606908729` | **Handle:** `אוברול-ארוך`
**Group:** clothing_yaml | **YAML:** HAS_YAML | **Score:** 66.8 ⚠️ NEEDS_REVIEW

**Current tags:**
`baby-gift`, `baby-overall`, `cotton-baby`, `everyday-wear`, `long-sleeve-baby`, `neutral-baby-outfit`, `newborn-clothing`, `sleepwear-baby`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-romper` | CAT-A | 90% | `title` |
| `fabric-cotton` | CAT-D | 80% | `yaml_desc` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 90% | `existing_tag` |

**Missing required:** CAT-C, CAT-B

---

### [CLOTHING_YAML] אוברול ארוך עם רוכסן
**ID:** `9096599994681` | **Handle:** `אוברול-ארוך-עם-רוכסן`
**Group:** clothing_yaml | **YAML:** HAS_YAML | **Score:** 60.3 ⚠️ NEEDS_REVIEW

**Current tags:**
`baby-gift`, `baby-overall`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-romper` | CAT-A | 90% | `title` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 90% | `existing_tag` |

**Missing required:** CAT-C, CAT-B

---

### [SHOES_YAML] מגפי חורף לילדות דגם לין
**ID:** `9607363625273` | **Handle:** `kids-boots-for-girls-winter-warm-shoes-for-children-fur-boot`
**Group:** shoes_yaml | **YAML:** HAS_YAML | **Score:** 75.3 ✅ PASS

**Current tags:**
`baby-boots`, `baby-gift`, `girls-clothing`, `kids-clothing`, `neutral-baby-outfit`, `winter-baby-wear`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-shoes` | CAT-A | 90% | `handle` |
| `season-winter` | CAT-C | 85% | `body` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-girl` | CAT-F | 90% | `existing_tag` |

**Missing required:** CAT-B

---

### [SHOES_YAML] מגפי חורף נוצצים עם כוכבים
**ID:** `9615669461305` | **Handle:** `childrens-fashion-boots-black-low-lightweight-boys-girls-tod`
**Group:** shoes_yaml | **YAML:** HAS_YAML | **Score:** 75.3 ✅ PASS

**Current tags:**
`baby-boots`, `baby-gift`, `neutral-baby-outfit`, `newborn-clothing`, `winter-baby-wear`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-shoes` | CAT-A | 90% | `handle` |
| `season-winter` | CAT-C | 85% | `title` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 90% | `existing_tag` |

**Missing required:** CAT-B

---

### [SHOES_YAML] מגפי חורף צעד ראשון
**ID:** `9615375794489` | **Handle:** `winter-snow-baby-boots-newborn-warm-booties-soft-sole-first-`
**Group:** shoes_yaml | **YAML:** HAS_YAML | **Score:** 89.5 ✅ PASS

**Current tags:**
`baby-boots`, `baby-gift`, `neutral-baby-outfit`, `newborn-clothing`, `winter-baby-wear`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-shoes` | CAT-A | 90% | `handle` |
| `age-0-3m` | CAT-B | 60% | `title_heuristic` |
| `season-winter` | CAT-C | 85% | `body` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 90% | `existing_tag` |

---

### [SHOES_YAML] נעל אולסטאר צעד ראשון לתינוק
**ID:** `9607365132601` | **Handle:** `trendy-comfortable-sneakers-for-baby-girls-and-boys-lightwei`
**Group:** shoes_yaml | **YAML:** HAS_YAML | **Score:** 60.3 ⚠️ NEEDS_REVIEW

**Current tags:**
`baby-gift`, `baby-set`, `baby-shower-gift`, `everyday-baby-wear`, `neutral-baby-outfit`, `newborn-clothing`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-shoes` | CAT-A | 90% | `handle` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 90% | `existing_tag` |

**Missing required:** CAT-C, CAT-B

---

### [SHOES_YAML] נעל אופנתית אלגנטית לתינוק
**ID:** `9607363756345` | **Handle:** `baby-panda-sneakers-toddler-fashion-sports-shoes-for-boys-gi`
**Group:** shoes_yaml | **YAML:** HAS_YAML | **Score:** 66.6 ⚠️ NEEDS_REVIEW

**Current tags:**
`baby-gift`, `baby-shoes`, `elegant-baby`, `everyday-baby-wear`, `newborn-clothing`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-shoes` | CAT-A | 90% | `handle` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 85% | `title` |
| `style-elegant` | CAT-G | 80% | `title` |

**Missing required:** CAT-C, CAT-B

---

### [SHOES_YAML] נעל אלגנטית צעד ראשון לבנות
**ID:** `9615375565113` | **Handle:** `girls-mary-jane-shoes-children-solid-color-bow-round-toe-bow`
**Group:** shoes_yaml | **YAML:** HAS_YAML | **Score:** 66.8 ⚠️ NEEDS_REVIEW

**Current tags:**
`baby-gift`, `baby-shoes`, `elegant-baby`, `everyday-baby-wear`, `girls-clothing`, `newborn-clothing`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-shoes` | CAT-A | 90% | `handle` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-girl` | CAT-F | 90% | `existing_tag` |
| `style-elegant` | CAT-G | 80% | `title` |

**Missing required:** CAT-C, CAT-B

---

### [SHOES_YAML] נעל הלו קיטי עם אורות לילדות
**ID:** `9607363232057` | **Handle:** `2024-summer-baby-led-light-sandals-for-girls-cute-hello-kitt`
**Group:** shoes_yaml | **YAML:** HAS_YAML | **Score:** 81.8 ✅ PASS

**Current tags:**
`baby-gift`, `baby-shoes`, `everyday-baby-wear`, `girls-clothing`, `kids-clothing`, `neutral-baby-outfit`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-shoes` | CAT-A | 90% | `handle` |
| `season-summer` | CAT-C | 85% | `body` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-girl` | CAT-F | 90% | `existing_tag` |
| `style-casual` | CAT-G | 80% | `handle` |

**Missing required:** CAT-B

---

### [SHOES_YAML] נעל חורף מחממת ואלגנטית צעד ראשון
**ID:** `9615376023865` | **Handle:** `2023-winter-snow-baby-boots-multiple-colors-warm-fluff-balls`
**Group:** shoes_yaml | **YAML:** HAS_YAML | **Score:** 95.3 ✅ PASS

**Current tags:**
`baby-gift`, `baby-shoes`, `elegant-baby`, `newborn-clothing`, `winter-baby-wear`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-shoes` | CAT-A | 90% | `handle` |
| `age-0-3m` | CAT-B | 60% | `title_heuristic` |
| `season-winter` | CAT-C | 85% | `body` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 60% | `default_unisex` |
| `style-elegant` | CAT-G | 80% | `title` |

---

### [SHOES_YAML] נעל חורף צעד ראשון אופנתיות
**ID:** `9615376089401` | **Handle:** `autumn-winter-baby-boots-kids-girl-boys-winter-warm-shoes-so`
**Group:** shoes_yaml | **YAML:** HAS_YAML | **Score:** 89.5 ✅ PASS

**Current tags:**
`baby-gift`, `baby-shoes`, `neutral-baby-outfit`, `newborn-clothing`, `winter-baby-wear`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-shoes` | CAT-A | 90% | `handle` |
| `age-0-3m` | CAT-B | 60% | `title_heuristic` |
| `season-winter` | CAT-C | 85% | `body` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 90% | `existing_tag` |

---

### [SHOES_YAML] נעל ספורט קז'ואל נוחה לתינוק
**ID:** `9607363461433` | **Handle:** `kids-casual-shoes-sneakers-boys-sport-breathable-tennis-snea`
**Group:** shoes_yaml | **YAML:** HAS_YAML | **Score:** 81.7 ✅ PASS

**Current tags:**
`baby-gift`, `baby-shoes`, `everyday-baby-wear`, `newborn-clothing`, `sporty-baby`

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-shoes` | CAT-A | 90% | `handle` |
| `season-spring-fall` | CAT-C | 85% | `body` |
| `occ-special-event` | CAT-E | 80% | `title` |
| `occ-beach` | CAT-E | 80% | `title` |
| `gender-unisex` | CAT-F | 85% | `title` |
| `style-casual` | CAT-G | 80% | `handle` |

**Missing required:** CAT-B

---

### [REBORN_GAP] 46CM Finished Reborn Baby Doll Felicia Newborn Open Blue Eyes Doll Soft Hand-Roo
**ID:** `10190522810681` | **Handle:** `46cm-finished-reborn-baby-doll-felicia-newborn-open-blue-eye`
**Group:** reborn_gap | **YAML:** YAML_GAP | **Score:** 73.1 ⚠️ NEEDS_REVIEW

**Current tags:**
_(none)_

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-doll` | CAT-A | 90% | `title` |
| `age-0-3m` | CAT-B | 60% | `title_heuristic` |
| `occ-gift` | CAT-E | 80% | `title` |
| `occ-sport` | CAT-E | 80% | `body` |
| `gender-unisex` | CAT-F | 60% | `default_unisex` |

**Blocked tags:**
- `fabric-*` — BLOCKED:yaml_gap_no_explicit_source

**Missing required:** CAT-C

---

### [REBORN_GAP] 50CM  Whole Silicone Vinyl Reborn Doll 20 Inch Girl Painted Newborn Baby Doll Wi
**ID:** `10190523040057` | **Handle:** `50cm-whole-silicone-vinyl-reborn-doll-20-inch-girl-painted-n`
**Group:** reborn_gap | **YAML:** YAML_GAP | **Score:** 74.3 ⚠️ NEEDS_REVIEW

**Current tags:**
_(none)_

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-set` | CAT-A | 90% | `body` |
| `age-0-3m` | CAT-B | 60% | `title_heuristic` |
| `occ-gift` | CAT-E | 80% | `title` |
| `occ-holiday` | CAT-E | 80% | `title` |
| `gender-girl` | CAT-F | 90% | `title` |

**Blocked tags:**
- `fabric-*` — BLOCKED:yaml_gap_no_explicit_source

**Missing required:** CAT-C

---

### [REBORN_GAP] NPK 46CM Meadow Reborn Baby Doll - Soft Touch 3D Skin Hand Painted Multiple Laye
**ID:** `10190522777913` | **Handle:** `npk-46cm-meadow-reborn-baby-doll-soft-touch-3d-skin-hand-pai`
**Group:** reborn_gap | **YAML:** YAML_GAP | **Score:** 45.0 ❌ BLOCKED

**Current tags:**
_(none)_

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-doll` | CAT-A | 90% | `title` |
| `gender-unisex` | CAT-F | 60% | `default_unisex` |

**Blocked tags:**
- `fabric-*` — BLOCKED:yaml_gap_no_explicit_source

**Missing required:** CAT-C, CAT-B

---

### [REBORN_GAP] NPK 50CM Full Body Maddie Reborn Baby Girl Doll - Soft Silicone Lifelike Touch G
**ID:** `10190523072825` | **Handle:** `npk-50cm-full-body-maddie-reborn-baby-girl-doll-soft-silicon`
**Group:** reborn_gap | **YAML:** YAML_GAP | **Score:** 48.0 ❌ BLOCKED

**Current tags:**
_(none)_

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-doll` | CAT-A | 90% | `title` |
| `gender-girl` | CAT-F | 90% | `title` |

**Blocked tags:**
- `fabric-*` — BLOCKED:yaml_gap_no_explicit_source

**Missing required:** CAT-C, CAT-B

---

### [REBORN_GAP] Open Mouth 33cm Pascale Full Body Silicone Reborn Girl Doll With Painted Skin Wa
**ID:** `10190523007289` | **Handle:** `open-mouth-33cm-pascale-full-body-silicone-reborn-girl-doll-`
**Group:** reborn_gap | **YAML:** YAML_GAP | **Score:** 48.0 ❌ BLOCKED

**Current tags:**
_(none)_

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-doll` | CAT-A | 90% | `title` |
| `gender-girl` | CAT-F | 90% | `title` |

**Blocked tags:**
- `fabric-*` — BLOCKED:yaml_gap_no_explicit_source

**Missing required:** CAT-C, CAT-B

---

### [GAP_CLOTHING] 0-18 Months old Newborn Baby boy Jumpsuit Cute Little Bear Short sleeved Jumpsui
**ID:** `10190523334969` | **Handle:** `0-18-months-old-newborn-baby-boy-jumpsuit-cute-little-bear-s`
**Group:** gap_clothing | **YAML:** YAML_GAP | **Score:** 89.5 ✅ PASS

**Current tags:**
_(none)_

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-romper` | CAT-A | 90% | `body` |
| `age-0-3m` | CAT-B | 60% | `title_heuristic` |
| `season-summer` | CAT-C | 85% | `title` |
| `occ-special-event` | CAT-E | 80% | `body` |
| `occ-everyday` | CAT-E | 80% | `body` |
| `gender-boy` | CAT-F | 90% | `title` |

**Blocked tags:**
- `fabric-*` — BLOCKED:yaml_gap_no_explicit_source

---

### [GAP_CLOTHING] 2Pcs Baby Boys' Sports and Leisure Set lapel Color blocked Short Sleeves and Sho
**ID:** `10190522941753` | **Handle:** `2pcs-baby-boys-sports-and-leisure-set-lapel-color-blocked-sh`
**Group:** gap_clothing | **YAML:** YAML_GAP | **Score:** 68.9 ⚠️ NEEDS_REVIEW

**Current tags:**
_(none)_

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-set` | CAT-A | 90% | `title` |
| `season-summer` | CAT-C | 85% | `title` |
| `occ-sport` | CAT-E | 80% | `body` |
| `gender-boy` | CAT-F | 90% | `title` |

**Blocked tags:**
- `fabric-*` — BLOCKED:yaml_gap_no_explicit_source

**Missing required:** CAT-B

---

### [GAP_CLOTHING] BABY MANIA™  בובה  נושמת מבית
**ID:** `9166992900409` | **Handle:** `babyz-בובת-לוטרה-נושמת`
**Group:** gap_clothing | **YAML:** YAML_GAP | **Score:** 54.0 ⚠️ NEEDS_REVIEW

**Current tags:**
_(none)_

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-doll` | CAT-A | 90% | `title` |
| `occ-beach` | CAT-E | 80% | `body` |
| `gender-girl` | CAT-F | 90% | `title` |

**Blocked tags:**
- `fabric-*` — BLOCKED:yaml_gap_no_explicit_source

**Missing required:** CAT-C, CAT-B

---

### [GAP_CLOTHING] Babyfree100
**ID:** `9839001633081` | **Handle:** `babyfree100`
**Group:** gap_clothing | **YAML:** YAML_GAP | **Score:** 41.0 ❌ BLOCKED

**Current tags:**
_(none)_

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-other` | CAT-A | 50% | `fallback` |
| `gender-unisex` | CAT-F | 60% | `default_unisex` |

**Blocked tags:**
- `fabric-*` — BLOCKED:yaml_gap_no_explicit_source

**Missing required:** CAT-C, CAT-B

---

### [GAP_CLOTHING] BabySleep Pro – רעש לבן ואור מרגיע לשינה עמוקה לתינוק
**ID:** `9839252472121` | **Handle:** `baby-white-noise-machine-kids-sleep-sound-player-night-light`
**Group:** gap_clothing | **YAML:** YAML_GAP | **Score:** 58.3 ⚠️ NEEDS_REVIEW

**Current tags:**
_(none)_

**Proposed tags:**
| Tag | Category | Confidence | Source |
|-----|---------|------------|--------|
| `type-other` | CAT-A | 50% | `fallback` |
| `occ-beach` | CAT-E | 80% | `body` |
| `gender-boy` | CAT-F | 90% | `title` |
| `style-casual` | CAT-G | 80% | `body` |

**Blocked tags:**
- `fabric-*` — BLOCKED:yaml_gap_no_explicit_source

**Missing required:** CAT-C, CAT-B

---

## 3. Taxonomy Coverage Analysis

| קטגוריה | כיסוי | % | Required |
|---------|-------|---|----------|
| Product Type (type-) | 30/30 | 100% | ✅ Required |
| Age Group (age-) | 10/30 | 33% | ✅ Required |
| Season (season-) | 15/30 | 50% | ✅ Required |
| Fabric (fabric-) | 3/30 | 10% | Recommended |
| Occasion (occ-) | 26/30 | 87% | Recommended |
| Gender (gender-) | 30/30 | 100% | ✅ Required |
| Style (style-) | 12/30 | 40% | Recommended |

---

## 4. Phase 2 Observations

- ממוצע quality score: **71.6** | PASS: 13 | NEEDS_REVIEW: 13 | BLOCKED: 4
- YAML_GAP fabric blocks: **10** מוצרים — CAT-D חסום ללא מקור מפורש בכותרת
- מוצרים עם טווח גיל מרובה: **0** — מוצרים 0-18M ו-0-24M מקבלים multiple age tags
- ללא season tag: **15** מוצרים — עונה לא ניתנת להסקה מהכותרת/תיאור

---

*Phase 2 Source Mapping Sample הורץ: 2026-05-05 | read-only source analysis | T0 | אין שינוי ב-Shopify*