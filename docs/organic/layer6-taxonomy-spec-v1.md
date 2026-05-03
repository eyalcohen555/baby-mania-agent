# Layer 6 — Taxonomy Specification v1.0
## BabyMania | Phase 1 — Planning Only | Created: 2026-05-03
### Status: WAITING AYAL REVIEW — לא מורשה לביצוע Shopify עד אישור

---

> **חובה:** קובץ זה הוא מסמך תכנון בלבד.
> אין שינויים ב-Shopify עד שאייל מאשר Phase 1 ומאשר Phase 6 (T3).

---

## 1. SYSTEM STATE

| פרמטר | ערך |
|-------|-----|
| Phase 0 | ✅ COMPLETE (2026-04-29) |
| Pre-Phase-1 Cleanup | ✅ COMPLETE (2026-05-03) — CL-1/CL-3 |
| Verified inventory scope | **393 active products** |
| YAML coverage | **269/393 (68.4%)** |
| YAML_GAP | **124 active products — ללא YAML** |
| Tag field נבחר | **Native Shopify tags** |
| Phase 1 type | Planning only |
| Shopify live | **NO** |
| Phase 1 status | CREATED — WAITING AYAL REVIEW |
| Layer 6 execution | NOT OPEN |

---

## 2. TAG ARCHITECTURE — 3 רמות

כל תג Layer 6 קיים בשלוש רמות מושגיות. שלושתן מיוצגות ע"י native Shopify tag אחד בפועל.

```
LEVEL 1 — Internal Tag (Shopify native tag, admin-only readable)
  Format: {category-prefix}-{value}
  Example: type-romper | age-0-3m | season-summer | fabric-cotton
           occ-gift | gender-girl | style-elegant

LEVEL 2 — Collection Tag (same native tag drives Smart Collection)
  Shopify Smart Collection condition: tag = type-romper
  Collection handle: collection-type-romper → /collections/rompers

LEVEL 3 — Customer Label (Hebrew, displayed in storefront navigation)
  Mapped from native tag in Liquid / navigation config
  Example: type-romper → "אוברולים" | age-0-3m → "0-3 חודשים"
  Hebrew labels are NOT a separate Shopify field — they are a UI mapping layer
```

### כלל ה-3 רמות:
> כל native tag שנוסף חייב לקבל תיעוד ב-3 הרמות לפני Phase 6.
> תג שיש לו Level 1 בלבד = לא מוכן ל-Smart Collections.
> Level 3 Hebrew labels ייבנו ב-Phase 9 (Navigation Planning).

---

## 3. CAT-A — Product Type

**מטרה:** לתאר מה המוצר הוא — לא מה הוא עשוי ממנו, לא למי, לא באיזו עונה.

**Prefix:** `type-`

| internal_tag | customer_label_he | collection_slug | required | confidence_min |
|-------------|-------------------|----------------|---------|---------------|
| type-romper | אוברול | type-romper | חובה | 0.90 |
| type-bodysuit | בגד גוף | type-bodysuit | חובה | 0.90 |
| type-dress | שמלה | type-dress | חובה | 0.90 |
| type-set | סט | type-set | חובה | 0.90 |
| type-pants | מכנסיים | type-pants | חובה | 0.85 |
| type-top | חולצה | type-top | חובה | 0.85 |
| type-hat | כובע | type-hat | חובה | 0.90 |
| type-swimwear | בגד ים | type-swimwear | חובה | 0.90 |
| type-shoes | נעליים | type-shoes | חובה | 0.95 |
| type-sandals | סנדלים | type-sandals | חובה | 0.95 |
| type-sneakers | סניקרס | type-sneakers | חובה | 0.95 |
| type-boots | מגפיים | type-boots | חובה | 0.95 |
| type-coat | מעיל | type-coat | חובה | 0.90 |
| type-reborn-doll | בובת ריבורן | type-reborn-doll | חובה | 0.99 |
| type-toy | צעצוע | type-toy | חובה | 0.85 |
| type-accessory | אביזר | type-accessory | חובה | 0.80 |
| type-swimming-ring | מצוף שחייה | type-swimming-ring | חובה | 0.95 |
| type-unknown | — | — | fallback | 0.00 |

**allowed_sources (CAT-A):**
- Shopify `title` — מילות מפתח ישירות: "אוברול", "שמלה", "סט", "כובע", "נעל", "סנדל", "בגד גוף", "מגף", "מעיל", "בגד ים", "מצוף", "בובת ריבורן"
- Shopify `handle` — transliterated keywords: "ovarole", "smlot", "naal", "kova", "bgad-yam"
- Shopify current `tags` — existing valid tags: "baby-romper", "baby-dress", "baby-set", "baby-shoes", "baby-sneakers", "baby-sandals", "baby-boots", "baby-hat", "baby-coat", "baby-bodysuit", "אוברול", "סט"
- YAML `product_type` field
- Shopify `product_type` field

**forbidden_inference (CAT-A):**
- ❌ לא להסיק `type-set` אם רק יש "plus" בכותרת
- ❌ לא להסיק `type-swimwear` אם יש "blue" או "summer" בלבד
- ❌ לא להסיק `type-reborn-doll` בלי מילת מפתח מפורשת בכותרת/YAML
- ❌ לא להסיק `type-hat` מתמונה בלבד

---

## 4. CAT-B — Age Group

**מטרה:** לתאר לאיזה גיל המוצר מתאים — מהמקור בלבד.

**Prefix:** `age-`

| internal_tag | customer_label_he | collection_slug | required | confidence_min |
|-------------|-------------------|----------------|---------|---------------|
| age-0-3m | 0-3 חודשים | age-0-3m | חובה | 0.85 |
| age-3-6m | 3-6 חודשים | age-3-6m | חובה | 0.85 |
| age-6-12m | 6-12 חודשים | age-6-12m | חובה | 0.85 |
| age-12-18m | 12-18 חודשים | age-12-18m | חובה | 0.85 |
| age-18-24m | 18-24 חודשים | age-18-24m | חובה | 0.85 |
| age-2-3y | 2-3 שנים | age-2-3y | חובה | 0.85 |
| age-3-5y | 3-5 שנים | age-3-5y | חובה | 0.85 |
| age-0-6m | 0-6 חודשים (טווח מאוחד) | age-0-6m | חובה | 0.85 |
| age-newborn | יילוד | age-newborn | חובה | 0.90 |
| age-unknown | — | — | fallback | 0.00 |

**הערה על age-0-6m:** כאשר מוצר מתאים ל-0-3 וגם 3-6 ניתן להשתמש בשניהם, או ב-age-0-6m אם מוצהר כך.

**allowed_sources (CAT-B):**
- Shopify `title` — "0-3", "3-6", "6-12", "12-18", "18-24", "2-3", "newborn", "יילוד", "חודשים"
- Shopify `description` — טווחי גיל מפורשים
- Shopify current `tags` — "0-3 חודש", "3-6 חודש", "6-12 חודש", "12-18 חודש", "18-24 חודש", "2-3 שנים", "newborn", "toddler"
- YAML `age_range` field
- Shopify variant `option` — אם יש size chart שמפנה לגיל

**forbidden_inference (CAT-B):**
- ❌ לא להסיק גיל ממחיר (מוצר יקר ≠ יילוד)
- ❌ לא להסיק גיל מתמונה בלבד (תינוק בתמונה ≠ גיל מוגדר)
- ❌ לא להסיק גיל מ"mini" בלבד
- ❌ "newborn" בכותרת כללית ≠ age-0-3m אוטומטית — חייב להיות מוצהר

**שים לב:** `18-24M` (existing tag) ← ממיר ל-`age-18-24m`. `3-6M6-9M` (malformed, 1 product) ← **אין להמיר** — tag זה אינו source תקין.

---

## 5. CAT-C — Season

**מטרה:** לתאר לאיזו עונה המוצר מתאים.

**Prefix:** `season-`

| internal_tag | customer_label_he | collection_slug | required | confidence_min |
|-------------|-------------------|----------------|---------|---------------|
| season-summer | קיץ | season-summer | חובה | 0.85 |
| season-winter | חורף | season-winter | חובה | 0.85 |
| season-spring-fall | אביב/סתיו | season-spring-fall | חובה | 0.80 |
| season-all | כל עונה | season-all | חובה | 0.80 |
| season-unknown | — | — | fallback | 0.00 |

**allowed_sources (CAT-C):**
- Shopify `title` — "קיץ", "חורף", "אביב", "סתיו", "summer", "winter", "spring"
- Shopify `handle` — "kayts", "khoref", "summer", "winter"
- Shopify current `tags` — "summer-baby-wear", "winter-baby-wear", "spring-baby-wear", "autumn-baby-wear", "חורף"
- YAML `season` or `use_season` field
- Product type context: swimwear → season-summer (HIGH confidence)
- Product type context: fleece/coat → season-winter (HIGH confidence)

**forbidden_inference (CAT-C):**
- ❌ לא להסיק קיץ מצבע לבן בלבד
- ❌ לא להסיק חורף מצבע כהה בלבד
- ❌ לא להסיק עונה ממחיר
- ✅ מותר: swimwear → season-summer אם type-swimwear כבר נקבע ממקור ברור

---

## 6. CAT-D — Fabric / Material

**מטרה:** לתאר מאיזה חומר עשוי המוצר — רק אם מוצהר במפורש.

**Prefix:** `fabric-`

| internal_tag | customer_label_he | collection_slug | required | confidence_min |
|-------------|-------------------|----------------|---------|---------------|
| fabric-cotton | כותנה | fabric-cotton | מומלץ | 0.90 |
| fabric-linen | פשתן | fabric-linen | מומלץ | 0.90 |
| fabric-muslin | מוסלין | fabric-muslin | מומלץ | 0.90 |
| fabric-knit | סריג | fabric-knit | מומלץ | 0.85 |
| fabric-fleece | פליז | fabric-fleece | מומלץ | 0.90 |
| fabric-denim | ג'ינס | fabric-denim | מומלץ | 0.90 |
| fabric-polyester | פוליאסטר | fabric-polyester | מומלץ | 0.85 |
| fabric-faux-fur | פרווה מלאכותית | fabric-faux-fur | מומלץ | 0.90 |
| fabric-corduroy | קורדרוי | fabric-corduroy | מומלץ | 0.90 |
| fabric-velvet | קטיפה | fabric-velvet | מומלץ | 0.90 |
| fabric-waffle-knit | סריג וופל | fabric-waffle-knit | מומלץ | 0.85 |
| fabric-silicone | סיליקון | fabric-silicone | מומלץ | 0.95 |
| fabric-body | גוף בד (ריבורן) | fabric-body | מומלץ | 0.95 |
| fabric-unknown | — | — | fallback | 0.00 |

**allowed_sources (CAT-D):**
- Shopify `title` — "כותנה", "פשתן", "מוסלין", "פליז", "ג'ינס", "cotton", "linen", "fleece", "denim"
- Shopify `description` — פירוט חומר מפורש
- Shopify current `tags` — "cotton-baby", "linen-baby", "fleece-baby", "denim-baby", "faux-fur-baby", "corduroy-baby", "velvet-baby", "waffle-knit"
- YAML `fabric_type` field ← **המקור החזק ביותר**

**forbidden_inference (CAT-D):**
- ❌ **אסור להסיק חומר מתמונה** — גם אם נראה ממשי
- ❌ לא להסיק כותנה מ"soft" בלבד
- ❌ לא להסיק פשתן מ"natural look" בלבד
- ❌ לא להסיק polyester מ"sporty" בלבד
- ❌ **YAML_GAP products** — ללא YAML אסור לתת fabric tag אלא אם כתוב מפורשות בכותרת/תיאור

---

## 7. CAT-E — Occasion / Use Case

**מטרה:** לתאר לאיזה שימוש המוצר מיועד.

**Prefix:** `occ-`

| internal_tag | customer_label_he | collection_slug | required | confidence_min |
|-------------|-------------------|----------------|---------|---------------|
| occ-everyday | יומיומי | occ-everyday | מומלץ | 0.80 |
| occ-gift | מתנה | occ-gift | מומלץ | 0.85 |
| occ-baby-shower | מקלחת תינוק | occ-baby-shower | מומלץ | 0.85 |
| occ-beach | חוף / בריכה | occ-beach | מומלץ | 0.85 |
| occ-sleep | שינה | occ-sleep | מומלץ | 0.85 |
| occ-special-event | אירוע מיוחד | occ-special-event | מומלץ | 0.85 |
| occ-photoshoot | צילום | occ-photoshoot | מומלץ | 0.85 |
| occ-first-step | צעד ראשון | occ-first-step | מומלץ | 0.90 |
| occ-water-play | משחק במים | occ-water-play | מומלץ | 0.85 |
| occ-calming | הרגעה (ריבורן) | occ-calming | מומלץ | 0.90 |
| occ-unknown | — | — | fallback | 0.00 |

**allowed_sources (CAT-E):**
- Shopify `title` — "מתנה", "אירוע", "צילום", "שינה", "gift", "event", "sleep"
- Shopify `description` — שימוש מוצהר
- Shopify current `tags` — "baby-gift", "gift", "baby-shower-gift", "special-occasion-baby", "everyday-baby-wear", "sleepwear-baby"
- YAML `use_case` field
- Product type context: type-swimwear → occ-beach (HIGH confidence)
- Product type context: type-reborn-doll → occ-calming (HIGH confidence)

**forbidden_inference (CAT-E):**
- ❌ לא להסיק occ-gift מ"beautiful" בלבד
- ❌ לא להסיק occ-special-event מ"elegant" בלבד
- ❌ לא להסיק occ-sleep ממוצר בצבע כהה
- ❌ לא להסיק occ-beach ממוצר קיצי שאינו swimwear/swimming accessory

---

## 8. CAT-F — Gender

**מטרה:** לתאר לאיזה מגדר המוצר מיועד — אם מוצהר.

**Prefix:** `gender-`

| internal_tag | customer_label_he | collection_slug | required | confidence_min |
|-------------|-------------------|----------------|---------|---------------|
| gender-girl | בנות | gender-girl | חובה | 0.90 |
| gender-boy | בנים | gender-boy | חובה | 0.90 |
| gender-neutral | ניוטרלי | gender-neutral | חובה | 0.85 |
| gender-unknown | — | — | fallback | 0.00 |

**allowed_sources (CAT-F):**
- Shopify `title` — "בנות", "בנים", "ניוטרלי", "girl", "boy", "girls", "boys", "unisex"
- Shopify `handle` — "girl", "boy", "banim", "banot"
- Shopify current `tags` — "girls-clothing", "boys-clothing", "neutral-baby-outfit"
- YAML `gender` field
- Shopify `description` — ציון מגדר מפורש

**forbidden_inference (CAT-F):**
- ❌ **אסור להסיק מגדר מצבע** — ורוד ≠ בנות, כחול ≠ בנים
- ❌ לא להסיק מגדר מ"pretty" / "cute" / "handsome" בלבד
- ❌ לא להסיק מגדר מהדפס (פרחים ≠ בנות, מכוניות ≠ בנים) — אלא אם מוצהר
- ✅ אם לא ברור — gender-unknown ולא gender-neutral
- **הבחנה:** gender-neutral = מוצהר במפורש כמתאים לשניהם. gender-unknown = לא ידוע.

---

## 9. CAT-G — Style

**מטרה:** לתאר את הסגנון החזותי/אסתטי של המוצר — רק ממקור מילולי.

**Prefix:** `style-`

| internal_tag | customer_label_he | collection_slug | required | confidence_min |
|-------------|-------------------|----------------|---------|---------------|
| style-elegant | אלגנטי | style-elegant | מומלץ | 0.80 |
| style-casual | קז'ואל | style-casual | מומלץ | 0.80 |
| style-vintage | וינטאג' | style-vintage | מומלץ | 0.85 |
| style-sporty | ספורטיבי | style-sporty | מומלץ | 0.80 |
| style-floral | פרחוני | style-floral | מומלץ | 0.85 |
| style-animal-print | הדפס חיות | style-animal-print | מומלץ | 0.85 |
| style-teddy | דובי | style-teddy | מומלץ | 0.85 |
| style-european | אירופאי | style-european | מומלץ | 0.80 |
| style-unicorn | חד-קרן | style-unicorn | מומלץ | 0.85 |
| style-striped | פסים | style-striped | מומלץ | 0.85 |
| style-modern | מודרני | style-modern | מומלץ | 0.75 |
| style-unknown | — | — | fallback | 0.00 |

**allowed_sources (CAT-G):**
- Shopify `title` — "אלגנטי", "פרחוני", "וינטאג'", "sporty", "vintage", "floral", "elegant"
- Shopify `handle` — "vintage", "elegant", "floral"
- Shopify current `tags` — "elegant-baby", "sporty-baby", "vintage-baby", "floral-baby", "bear-print-baby", "animal-print-baby", "elephant-print-baby", "leopard-baby", "unicorn-baby", "striped-baby", "european-baby-style", "denim-style-baby"
- Shopify `description` — תיאור סגנון מפורש
- YAML `style` field

**forbidden_inference (CAT-G):**
- ❌ לא להסיק style-elegant אם רק "special" בכותרת
- ❌ לא להסיק style-vintage מ"retro" בלבד
- ❌ style-casual ≠ ברירת מחדל — רק אם מוצהר

---

## 10. SOURCE RULES — כללים מלאים

### 10.1 היררכיית אמינות מקורות

| מקור | אמינות | הערות |
|------|--------|-------|
| YAML field (**חזק**) | HIGH | YAML = מסמך אמת מוסמך לפי מוצר |
| Shopify title | HIGH | מוצהר ישיר — אמין לרוב הקטגוריות |
| Shopify handle | MEDIUM-HIGH | משקף כותרת, לא תמיד מלא |
| Shopify current tags | MEDIUM | תגיות קיימות = evidence, לא proof |
| Shopify description | MEDIUM | יש לבדוק שלא נוסף על-ידי AI בלבד |
| Shopify product_type | MEDIUM | לא תמיד מאוכלס ב-BabyMania |
| collection membership | MEDIUM | מחייב בדיקה שה-collection אינה ידנית בלבד |
| Image alt text | LOW | לא להשתמש כ-sole source |

### 10.2 כלל מינימום confidence

```
required tag + confidence < 0.85 → לא להוסיף → tag = *-unknown
optional tag + confidence < 0.80 → לא להוסיף → leave empty
confidence ≥ 0.90 → HIGH confidence → source traced and clear
```

### 10.3 מקורות אסורים — אסור בהחלט

| מה | למה |
|----|-----|
| צבע המוצר | צבע ≠ מגדר, עונה, סגנון |
| תמונת המוצר | לא מקור טקסטואלי — לא ניתן לאמת |
| מחיר | מחיר ≠ קטגוריה |
| vendor name | vendor ≠ product type |
| הנחה / "SALE" | פרטי שיווק ≠ taxonomy |
| GPT/AI inference | אסור להסיק בלי source trace מפורש |

---

## 11. YAML_GAP POLICY

**הגדרה:** 124 active products שאין להם קובץ YAML ב-`shared/product-context/`.

### 11.1 מה מותר ל-YAML_GAP products

| קטגוריה | מה מותר | מה אסור |
|---------|---------|---------|
| CAT-A (type) | ✅ מ-title + handle + existing tags | ❌ לא מ-image |
| CAT-B (age) | ✅ רק אם מוצהר בכותרת/תג קיים | ❌ לא מ-variant sizes בלבד |
| CAT-C (season) | ✅ מ-title + existing tags + type context | ❌ לא מ-color |
| CAT-D (fabric) | ❌ **אסור** אלא אם כתוב מפורשות בכותרת/תיאור | ❌ לא מ-image, לא מ-"looks soft" |
| CAT-E (occasion) | ✅ מ-title + existing tags בלבד | ❌ לא מ-price |
| CAT-F (gender) | ✅ מ-title + handle + existing tags | ❌ אסור מ-color |
| CAT-G (style) | ✅ רק מ-title + existing tags ברורים | ❌ לא inference |

### 11.2 source_status לmapping

```json
{
  "product_id": "...",
  "yaml_gap": true,
  "source_status": "limited",
  "missing_yaml": true,
  "allowed_tags": ["type-*", "gender-*", "season-* (from title/tags only)"],
  "blocked_tags": ["fabric-* (no title source)", "age-* (no explicit source)"]
}
```

### 11.3 Phase 6 (Live Batch) — YAML_GAP policy

> YAML_GAP products לא נכללים ב-Phase 6 pilot batch
> אלא אם יש source trace ברור ל-4 שדות חובה (type/age/season/gender)
> מ-title + handle + existing tags בלבד.

---

## 12. NATIVE SHOPIFY TAG POLICY

### 12.1 כלל הפורמט

```
Format: {prefix}-{value}
Examples: type-romper, age-0-3m, season-summer, fabric-cotton,
          occ-gift, gender-girl, style-elegant

Rules:
✅ lowercase always
✅ hyphens only — no spaces, no underscores
✅ English/Latin only — no Hebrew in native tags
✅ max 50 characters
✅ no colons (Shopify UI edge-case issues)
```

**למה אנגלית/slug ולא עברית ב-native tags:**
- קידוד UTF-8 בURL collections עלול לגרום לשגיאות
- Smart Collection conditions עובדות טוב יותר עם ASCII
- Hebrew labels יישמרו ב-Level 3 (UI mapping) — לא ב-native tag

### 12.2 מה אסור לעלות כ-native tag

| אסור | סיבה |
|------|------|
| `Copy AI` | spurious admin tag — removed in CL-1 |
| `All categories` | spurious admin tag — removed in CL-3 |
| `3-6M6-9M` | malformed merged value — לא source תקין |
| תגיות עם רווח שאינן slug | חוסמות Smart Collections |
| תגיות עם characters מיוחדים | URL encoding issues |
| תגיות ב-Hebrew כ-native tag | encoding edge-cases בCollections |
| תגיות ללא source trace | forbidden — מחייב G1-G4 לעבור |

### 12.3 תגיות קיימות תקינות — מה קורה אתן

תגיות ה-legacy הקיימות (baby-gift, newborn-clothing, everyday-baby-wear וכו') **אינן מוסרות** ב-Layer 6. הן ממשיכות לקיים. Layer 6 **מוסיף** תגיות structured בנוסף.

> החלטה: האם לשמור legacy tags לצד Layer 6 tags, או לבצע migration — תוחלט ב-Phase 5 (Ayal Review) לפני Phase 6.

---

## 13. BLOCKED / FORBIDDEN TAGS

| תג | סטטוס | סיבה |
|----|-------|------|
| `Copy AI` | FORBIDDEN | spurious — הוסר CL-1 |
| `All categories` | FORBIDDEN | admin tag — הוסר CL-3 |
| `kids-clothing` | REVIEW REQUIRED | too broad — לא מדויק מספיק לLayer 6 taxonomy |
| `3-6M6-9M` | MALFORMED | שתי ערכים ממוזגים — לא להשתמש כ-source |
| `9-18M` | NON-STANDARD | פורמט לא עקבי — לא layer 6 source |
| `18-24M` | NON-STANDARD | פורמט לא עקבי — ממיר ל-age-18-24m ב-Phase 4 |
| `תינוקות 0-3Y` | NON-STANDARD | ערבוב עברית+אנגלית+Y suffix — לא source |
| כל תג עם `?` / `�` | FORBIDDEN | garbled encoding — אם יימצא בעתיד |
| תגיות AI-generated ללא source | FORBIDDEN | G4: No Forbidden Inference |

---

## 14. ALLOWED VALUES — טבלה מלאה

| category | internal_tag | customer_label_he | collection_slug | required | confidence_min | example_product_signal |
|---------|-------------|-------------------|----------------|---------|---------------|----------------------|
| CAT-A | type-romper | אוברול | type-romper | חובה | 0.90 | title: "אוברול", tag: "אוברול"/"baby-romper" |
| CAT-A | type-bodysuit | בגד גוף | type-bodysuit | חובה | 0.90 | title: "בגד גוף", tag: "baby-bodysuit" |
| CAT-A | type-dress | שמלה | type-dress | חובה | 0.90 | title: "שמלה", tag: "baby-dress" |
| CAT-A | type-set | סט | type-set | חובה | 0.90 | title: "סט", tag: "baby-set"/"סט" |
| CAT-A | type-pants | מכנסיים | type-pants | חובה | 0.85 | title: "מכנסיים", tag: "baby-pants" |
| CAT-A | type-top | חולצה | type-top | חובה | 0.85 | title: "חולצה", tag: "baby-top" |
| CAT-A | type-hat | כובע | type-hat | חובה | 0.90 | title: "כובע", YAML: product_type=hat |
| CAT-A | type-swimwear | בגד ים | type-swimwear | חובה | 0.90 | title: "בגד ים", handle: "bgad-yam" |
| CAT-A | type-shoes | נעליים | type-shoes | חובה | 0.95 | title: "נעל", tag: "baby-shoes" |
| CAT-A | type-sandals | סנדלים | type-sandals | חובה | 0.95 | title: "סנדל", tag: "baby-sandals" |
| CAT-A | type-sneakers | סניקרס | type-sneakers | חובה | 0.95 | title: "סניקרס", tag: "baby-sneakers" |
| CAT-A | type-boots | מגפיים | type-boots | חובה | 0.95 | title: "מגף", tag: "baby-boots" |
| CAT-A | type-coat | מעיל | type-coat | חובה | 0.90 | title: "מעיל", tag: "baby-coat" |
| CAT-A | type-swimming-ring | מצוף שחייה | type-swimming-ring | חובה | 0.95 | title: "מצוף", handle: "swimming-ring" |
| CAT-A | type-reborn-doll | בובת ריבורן | type-reborn-doll | חובה | 0.99 | title: "ריבורן", YAML: product_type=reborn |
| CAT-A | type-toy | צעצוע | type-toy | חובה | 0.85 | title: "צעצוע", YAML: product_type=toy |
| CAT-A | type-accessory | אביזר | type-accessory | חובה | 0.80 | YAML: product_type=accessory |
| CAT-B | age-0-3m | 0-3 חודשים | age-0-3m | חובה | 0.85 | title/tag: "0-3", YAML age_range |
| CAT-B | age-3-6m | 3-6 חודשים | age-3-6m | חובה | 0.85 | title/tag: "3-6", YAML age_range |
| CAT-B | age-6-12m | 6-12 חודשים | age-6-12m | חובה | 0.85 | title/tag: "6-12", YAML age_range |
| CAT-B | age-12-18m | 12-18 חודשים | age-12-18m | חובה | 0.85 | title/tag: "12-18", YAML age_range |
| CAT-B | age-18-24m | 18-24 חודשים | age-18-24m | חובה | 0.85 | title/tag: "18-24", YAML age_range |
| CAT-B | age-2-3y | 2-3 שנים | age-2-3y | חובה | 0.85 | title/tag: "2-3 שנים", YAML age_range |
| CAT-B | age-3-5y | 3-5 שנים | age-3-5y | חובה | 0.85 | YAML age_range: 3-5y |
| CAT-B | age-newborn | יילוד | age-newborn | חובה | 0.90 | title: "יילוד"/"newborn", tag: "newborn" |
| CAT-B | age-0-6m | 0-6 חודשים | age-0-6m | חובה | 0.85 | YAML age_range: 0-6m |
| CAT-C | season-summer | קיץ | season-summer | חובה | 0.85 | title: "קיץ"/"summer", tag: "summer-baby-wear" |
| CAT-C | season-winter | חורף | season-winter | חובה | 0.85 | title: "חורף"/"winter", tag: "winter-baby-wear"/"חורף" |
| CAT-C | season-spring-fall | אביב/סתיו | season-spring-fall | חובה | 0.80 | tag: "spring-baby-wear"/"autumn-baby-wear" |
| CAT-C | season-all | כל עונה | season-all | חובה | 0.80 | YAML: season=all, bodysuit/accessories |
| CAT-D | fabric-cotton | כותנה | fabric-cotton | מומלץ | 0.90 | title: "כותנה"/"cotton", tag: "cotton-baby", YAML fabric_type |
| CAT-D | fabric-linen | פשתן | fabric-linen | מומלץ | 0.90 | title: "פשתן"/"linen", tag: "linen-baby", YAML fabric_type |
| CAT-D | fabric-muslin | מוסלין | fabric-muslin | מומלץ | 0.90 | title: "מוסלין"/"muslin", YAML fabric_type |
| CAT-D | fabric-knit | סריג | fabric-knit | מומלץ | 0.85 | tag: "soft-knit"/"baby-knit-set", YAML fabric_type |
| CAT-D | fabric-fleece | פליז | fabric-fleece | מומלץ | 0.90 | tag: "fleece-baby", title: "פליז", YAML fabric_type |
| CAT-D | fabric-denim | ג'ינס | fabric-denim | מומלץ | 0.90 | tag: "denim-baby", title: "ג'ינס"/"denim", YAML fabric_type |
| CAT-D | fabric-polyester | פוליאסטר | fabric-polyester | מומלץ | 0.85 | title: "פוליאסטר", YAML fabric_type |
| CAT-D | fabric-faux-fur | פרווה מלאכותית | fabric-faux-fur | מומלץ | 0.90 | tag: "faux-fur-baby", title: "פרווה", YAML fabric_type |
| CAT-D | fabric-corduroy | קורדרוי | fabric-corduroy | מומלץ | 0.90 | tag: "corduroy-baby", YAML fabric_type |
| CAT-D | fabric-velvet | קטיפה | fabric-velvet | מומלץ | 0.90 | tag: "velvet-baby", title: "קטיפה", YAML fabric_type |
| CAT-D | fabric-waffle-knit | סריג וופל | fabric-waffle-knit | מומלץ | 0.85 | tag: "waffle-knit", YAML fabric_type |
| CAT-E | occ-everyday | יומיומי | occ-everyday | מומלץ | 0.80 | tag: "everyday-baby-wear"/"everyday-wear" |
| CAT-E | occ-gift | מתנה | occ-gift | מומלץ | 0.85 | tag: "baby-gift"/"gift" |
| CAT-E | occ-baby-shower | מקלחת תינוק | occ-baby-shower | מומלץ | 0.85 | tag: "baby-shower-gift" |
| CAT-E | occ-beach | חוף / בריכה | occ-beach | מומלץ | 0.85 | type-swimwear + type-swimming-ring |
| CAT-E | occ-sleep | שינה | occ-sleep | מומלץ | 0.85 | tag: "sleepwear-baby", title: "שינה"/"sleep" |
| CAT-E | occ-special-event | אירוע מיוחד | occ-special-event | מומלץ | 0.85 | tag: "special-occasion-baby", title: "אירוע" |
| CAT-E | occ-calming | הרגעה | occ-calming | מומלץ | 0.90 | type-reborn-doll, YAML use_case=calming |
| CAT-E | occ-first-step | צעד ראשון | occ-first-step | מומלץ | 0.90 | type-shoes, YAML use_case=first-step |
| CAT-E | occ-water-play | משחק במים | occ-water-play | מומלץ | 0.85 | type-swimming-ring, title: "בריכה"/"ים" |
| CAT-F | gender-girl | בנות | gender-girl | חובה | 0.90 | title: "בנות", tag: "girls-clothing", YAML gender |
| CAT-F | gender-boy | בנים | gender-boy | חובה | 0.90 | title: "בנים", tag: "boys-clothing", YAML gender |
| CAT-F | gender-neutral | ניוטרלי | gender-neutral | חובה | 0.85 | tag: "neutral-baby-outfit", YAML gender=neutral, title: "ניוטרלי"/"unisex" |
| CAT-G | style-elegant | אלגנטי | style-elegant | מומלץ | 0.80 | tag: "elegant-baby", title: "אלגנטי" |
| CAT-G | style-casual | קז'ואל | style-casual | מומלץ | 0.80 | title: "קז'ואל"/"casual", YAML style |
| CAT-G | style-vintage | וינטאג' | style-vintage | מומלץ | 0.85 | title: "וינטאג'"/"vintage", tag: "vintage-baby", YAML style |
| CAT-G | style-sporty | ספורטיבי | style-sporty | מומלץ | 0.80 | tag: "sporty-baby", title: "ספורטיבי" |
| CAT-G | style-floral | פרחוני | style-floral | מומלץ | 0.85 | tag: "floral-baby", title: "פרחוני"/"floral" |
| CAT-G | style-animal-print | הדפס חיות | style-animal-print | מומלץ | 0.85 | tag: "animal-print-baby"/"elephant-print-baby"/"leopard-baby" |
| CAT-G | style-teddy | דובי | style-teddy | מומלץ | 0.85 | tag: "bear-print-baby", title: "דוב"/"bear" |
| CAT-G | style-european | אירופאי | style-european | מומלץ | 0.80 | tag: "european-baby-style", YAML style |
| CAT-G | style-unicorn | חד-קרן | style-unicorn | מומלץ | 0.85 | tag: "unicorn-baby", title: "חד-קרן"/"unicorn" |
| CAT-G | style-striped | פסים | style-striped | מומלץ | 0.85 | tag: "striped-baby", title: "פסים"/"striped" |
| CAT-G | style-modern | מודרני | style-modern | מומלץ | 0.75 | YAML style=modern, title: "מודרני" |

**סה"כ allowed values: 61 (לא כולל unknown fallbacks)**

---

## 15. PHASE 1 EXIT CONDITIONS

Phase 1 נחשב PASS רק כאשר **כל** הפריטים הבאים נכונים:

```
✅ כל 7 הקטגוריות (CAT-A עד CAT-G) מוגדרות
✅ לכל קטגוריה יש allowed values עם internal_tag
✅ לכל value יש customer_label_he
✅ לכל value יש allowed_sources מוגדר
✅ לכל value יש forbidden_inference מוגדר
✅ לכל value יש confidence_min
✅ YAML_GAP policy מוגדרת (סעיף 11)
✅ Native Shopify tag policy מוגדרת (סעיף 12)
✅ Blocked/Forbidden tags מתועדים (סעיף 13)
✅ אין Shopify write — Phase 1 planning only
✅ המסמך מוכן לאישור אייל
```

**מצב נוכחי:** כל 10 תנאים מתקיימים. **Phase 1 = PASS (planning) — WAITING AYAL REVIEW.**

---

## 16. LEGACY TAGS — מדיניות המשך

תגיות legacy קיימות (baby-gift, newborn-clothing, everyday-baby-wear, neutral-baby-outfit, summer-baby-wear, winter-baby-wear, girls-clothing, boys-clothing, cotton-baby, וכו'):

**מדיניות ברירת מחדל:**
> תגיות legacy **נשמרות** לצד תגיות Layer 6. לא מוסרות ב-Phase 6/7.
> ב-Phase 5 (Ayal Review) — אייל יחליט: migration מלא (מחליף) או coexistence (מוסיף).

---

## 17. OPEN DECISIONS — ממתינות לאייל

| # | שאלה | אפשרויות | עדיפות |
|---|------|---------|-------|
| D1 | Legacy tags: migration או coexistence? | A: מחליף legacy | B: מוסיף בנוסף | HIGH |
| D2 | `3-6M6-9M` (1 מוצר) — להסיר? | T1 קטן בנפרד | MEDIUM |
| D3 | 124 YAML_GAP — מתי לסגור? | Phase 2/3/later | MEDIUM |

---

## 18. היסטוריית גרסאות

| גרסה | תאריך | שינוי |
|------|-------|-------|
| v1.0 | 2026-05-03 | נוצר — Phase 1 Taxonomy Spec. 7 קטגוריות, 61 allowed values. |

---

*קובץ זה הוא מסמך תכנון בלבד. אין שינויים ב-Shopify עד Phase 6 (T3 approval).*
