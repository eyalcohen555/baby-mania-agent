# חוזה Metafields — דף מוצר ריבורן
**טרמינל 6 | BabyMania | ריבורן בלבד**
**תאריך:** 2026-05-24
**סטטוס:** טיוטה — לא לביצוע בשופיפיי

---

## 1. מטרת החוזה

להגדיר בדיוק אילו שדות דינמיים נדרשים כדי להמיר את
`output/pages/reborn-landing/levi-reborn-product-v2.html`
לתבנית Liquid לשופיפיי שתעבוד עבור **כל דגמי הריבורן**,
כך שכל מקום שמוזכר שם הבובה או מחירה יתעדכן אוטומטית לפי המוצר.

**כלל עקרוני:** שם הבובה ומחיר הבובה — חייבים להיות דינמיים בכל סקשן.

---

## 2. Product Fields רגילים — לא צריכים metafield

אלה קיימים ב-Shopify מהקופסה:

| שדה | Liquid | שימוש בדף |
|---|---|---|
| מחיר מכירה | `product.price \| money` | S1, S2, S15, S17, Sticky |
| מחיר מקורי | `product.compare_at_price \| money` | S1, S17 |
| כותרת מוצר (ארוכה) | `product.title` | Sticky Bar (truncate: 45), `<title>` |
| תמונות | `product.images` | Hero gallery (עתידי) |
| וריאנטים | `product.variants` | S2 Bundle, Sticky |
| URL | `product.url` / `product.handle` | קישורים פנימיים |

**שים לב:** `product.title` של לוי הוא:
`"בובת ריבורן אמיתית – מגע מציאותי שמפתח רגישות ואהבה אצל ילדים מבית בייבי מניה"`
— זה **לא** שם התצוגה בדף. לכן נדרש metafield נפרד לשם קצר.

---

## 3. Metafields נדרשים — רשימה מינימלית

### קבוצה 1 — זהות דגם: `namespace: reborn_doll`

| key | type | חובה | משתנה בין דגמים |
|---|---|---|---|
| `hebrew_name` | `single_line_text_field` | **חובה** | כן |
| `model_label` | `single_line_text_field` | **חובה** | כן |

### קבוצה 2 — מפרט דגם: `namespace: reborn_specs`

| key | type | חובה | משתנה בין דגמים |
|---|---|---|---|
| `size_cm` | `single_line_text_field` | **חובה** | כן |
| `source_note` | `single_line_text_field` | רשות | לא תמיד |

### קבוצה 3 — קופי דגם: `namespace: reborn_copy`

| key | type | חובה | משתנה בין דגמים |
|---|---|---|---|
| `hero_subtitle` | `multi_line_text_field` | **חובה** | כן |

### קבוצה 4 — FAQ: `namespace: baby_mania`

| key | type | חובה | משתנה בין דגמים |
|---|---|---|---|
| `faq` | `json` | רשות שלב 1 | חלקית |

---

## 4. טבלת שימוש לפי סקשנים

| סקשן | קבוע / דינמי | שדות דרושים | hardcoded בשלב 1? |
|---|---|---|---|
| `<title>` + `<meta>` | דינמי | `reborn_doll.hebrew_name` + `reborn_specs.size_cm` | ❌ חייב dynamic |
| **S1 Hero** — prod-name | דינמי | `reborn_doll.model_label` + `reborn_specs.size_cm` | ❌ |
| **S1 Hero** — img alt | דינמי | `reborn_doll.model_label` + `reborn_specs.size_cm` | ❌ |
| **S1 Hero** — subtitle | דינמי | `reborn_copy.hero_subtitle` | ❌ |
| **S1 Hero** — מחיר | דינמי | `product.price` / `product.compare_at_price` | ❌ |
| **S1 Hero** — trust bar | קבוע | — | ✅ |
| **S2 Bundle** — מחיר בסיס | דינמי | `product.price` | ❌ |
| **S2 Bundle** — חבילות 2/3 | קבוע (לוגיקה קבועה) | — | ✅ לשלב 1 |
| **S3 Trust** | קבוע | — | ✅ |
| **S4 Problem** | קבוע | — | ✅ |
| **S5 Agitation** | קבוע | — | ✅ |
| **S7 Research** | קבוע | — | ✅ |
| **S7.5 Video** | אסט קבוע לשלב 1 | — | ✅ לשלב 1 |
| **S8 Benefits** | קבוע | — | ✅ |
| **S9 Before/After** | אסט | — | ✅ לשלב 1 |
| **S10 Outcomes** | קבוע | — | ✅ |
| **S11 Social Proof** | דינמי חלקי | `reborn_doll.hebrew_name` | ❌ ("בחרו בלוי") |
| **S13 Stats** — גודל | דינמי | `reborn_specs.size_cm` | ❌ |
| **S13/14 Who For** | קבוע | — | ✅ |
| **S15 Price** | דינמי | `product.price` | ❌ |
| **S16 FAQ** | דינמי חלקי | `reborn_doll.hebrew_name` / `baby_mania.faq` | ✅ לשלב 1 |
| **S17 Final CTA** — כותרת | קבועה | — | ✅ |
| **S17 Final CTA** — כפתור | דינמי | `reborn_doll.model_label` | ❌ ("אני רוצה את בובת לוי") |
| **S17 Final CTA** — מחיר | דינמי | `product.price` / `product.compare_at_price` | ❌ |
| **Sticky Bar** | דינמי | `product.title` / `product.price` | ❌ |
| **Nav / Footer** | קבוע | — | ✅ |

---

## 5. פירוט מלא לכל Metafield

### `reborn_doll.hebrew_name`
- **namespace:** `reborn_doll`
- **key:** `hebrew_name`
- **type:** `single_line_text_field`
- **דוגמה ללוי:** `לוי`
- **חובה:** כן
- **משתנה:** כן — כל דגם שם אחר
- **סקשנים:** S1 (alt), S11 ("בחרו בלוי"), S16 FAQ ("בובת לוי"), `<title>`
- **hardcoded שלב 1:** ❌ — חוסם המרה ל-Liquid

### `reborn_doll.model_label`
- **namespace:** `reborn_doll`
- **key:** `model_label`
- **type:** `single_line_text_field`
- **דוגמה ללוי:** `בובת ריבורן לוי`
- **חובה:** כן
- **משתנה:** כן
- **סקשנים:** S1 prod-name, S17 כפתור CTA ("כן, אני רוצה את בובת ריבורן לוי")
- **hardcoded שלב 1:** ❌ — חוסם המרה ל-Liquid

### `reborn_specs.size_cm`
- **namespace:** `reborn_specs`
- **key:** `size_cm`
- **type:** `single_line_text_field`
- **דוגמה ללוי:** `46 ס״מ`
- **חובה:** כן
- **משתנה:** כן — 33/46/50/60 ס"מ
- **סקשנים:** S1 prod-name, S1 img alt, S1 hero-sub, S13 stat chip, `<title>`
- **hardcoded שלב 1:** ❌ — חוסם המרה ל-Liquid
- **הערה:** ערך לוי = 46 ס"מ לפי החלטת אייל (Ali=17-18in). לא 48 ולא 49.

### `reborn_specs.source_note`
- **namespace:** `reborn_specs`
- **key:** `source_note`
- **type:** `single_line_text_field`
- **דוגמה ללוי:** `לפי נתוני ספק`
- **חובה:** רשות
- **משתנה:** לא תמיד
- **סקשנים:** Tooltip / הסבר קטן ליד הגודל (אם יוחלט להוסיף)
- **hardcoded שלב 1:** ✅ — לא חוסם

### `reborn_copy.hero_subtitle`
- **namespace:** `reborn_copy`
- **key:** `hero_subtitle`
- **type:** `multi_line_text_field`
- **דוגמה ללוי:** `בובת ריבורן לוי נראית ומרגישה כמו תינוק אמיתי: 46 ס״מ, מגע רך, הבעה עדינה, בקבוק ומוצץ מגנטי באריזה.`
- **חובה:** כן
- **משתנה:** כן — כל דגם טקסט שונה
- **סקשנים:** S1 hero-sub
- **hardcoded שלב 1:** ❌ — חוסם המרה ל-Liquid

### `baby_mania.faq`
- **namespace:** `baby_mania`
- **key:** `faq`
- **type:** `json`
- **דוגמה ללוי:** (ראה סעיף 6 למטה)
- **חובה:** רשות לשלב 1
- **משתנה:** חלקית — שאלות כלליות קבועות, תשובות ספציפיות משתנות
- **סקשנים:** S16 FAQ
- **hardcoded שלב 1:** ✅ — ניתן להשאיר hardcoded בגרסה הראשונה

---

## 6. דוגמת ערכים ללוי — PID 9689589383481

```json
{
  "reborn_doll": {
    "hebrew_name": "לוי",
    "model_label": "בובת ריבורן לוי"
  },
  "reborn_specs": {
    "size_cm": "46 ס״מ",
    "source_note": "לפי נתוני ספק"
  },
  "reborn_copy": {
    "hero_subtitle": "בובת ריבורן לוי נראית ומרגישה כמו תינוק אמיתי: 46 ס״מ, מגע רך, הבעה עדינה, בקבוק ומוצץ מגנטי באריזה."
  },
  "product_fields": {
    "title": "בובת ריבורן אמיתית – מגע מציאותי שמפתח רגישות ואהבה אצל ילדים מבית בייבי מניה",
    "price": "299.00",
    "compare_at_price": "399.00",
    "variants_count": 3,
    "variants": ["בד", "סיליקון ילדה", "סיליקון ילד"]
  }
}
```

**FAQ ללוי (baby_mania.faq) — טיוטה:**
```json
[
  {
    "q": "מאיזה גיל מתאים המוצר?",
    "a": "בובת לוי מתאימה מגיל 3 ומעלה. היא מורכבת מחומרים בטוחים ועמידים, ללא חלקים קטנים. לילדות מגיל 3–12 היא מספקת חוויית משחק עשירה ומפתחת."
  },
  {
    "q": "מה ההבדל בין גרסת הבד לגרסת הסיליקון?",
    "a": "בגרסת הבד — ראש וגפיים מסיליקון, גוף בד. קלה יותר, רכה יותר, לא מתאימה לרחיצה. בגרסת הסיליקון — כל הגוף סיליקון מלא, מתאים לרחיצה. שתי הגרסאות מגיעות עם בקבוק ומוצץ מגנטי."
  },
  {
    "q": "האם ניתן לרחוץ את הבובה?",
    "a": "גרסת הסיליקון המלאה — כן, מתאים לרחיצה. גרסת הבד — לא. ניתן לנגב בעדינות במטלית לחה בסבון עדין ומים פושרים."
  },
  {
    "q": "מה כלול באריזה?",
    "a": "הבובה מגיעה עם: בקבוק, מוצץ מגנטי, תעודת לידה, חיתול, כובע ובגדים. הכל כלול — אין צורך לקנות בנפרד."
  },
  {
    "q": "מהי מדיניות ההחזרה?",
    "a": "אנו מציעים החזרה תוך 14 יום מיום הקבלה, ללא שאלות. המוצר צריך להיות באריזתו המקורית ובמצב תקין. החזר כספי מלא יינתן תוך 5–7 ימי עסקים."
  }
]
```

---

## 7. שדות שלא נכנסים לחוזה כרגע

לפי החלטת אייל — לא חוסמים ולא נדרשים לשלב הראשון:

| שדה | סיבה |
|---|---|
| סוג שיער | UNKNOWN לכל המוצרים |
| צבע עיניים | UNKNOWN לכל המוצרים |
| אביזרים כלולים | UNKNOWN מ-Ali, ידוע רק ללוי מספק ישיר |
| בגדים כלולים | UNKNOWN מ-Ali |
| רחיץ / לא רחיץ | UNKNOWN מ-Ali, ידוע רק ללוי |
| גיל מומלץ | UNKNOWN |
| CE / EN71 | לא מאומת |
| משקל | UNKNOWN לכל המוצרים |
| model_story | עדיין לא מוגדר לשום דגם |
| unique_differentiator | לא חוסם שלב 1 |

---

## 8. ספירת מקומות שם הבובה ומחיר — לפי סקשן

### שם הבובה ("לוי" / `reborn_doll.hebrew_name` / `reborn_doll.model_label`)

| מיקום | טקסט נוכחי | שדה Liquid |
|---|---|---|
| `<title>` | `בובת ריבורן לוי 48 ס״מ \| Baby Mania` | `{{ product.metafields.reborn_doll.model_label }} {{ product.metafields.reborn_specs.size_cm }}` |
| S1 hero-prod-name | `Reborn Baby Levi 48cm` | `{{ product.metafields.reborn_doll.model_label }} {{ product.metafields.reborn_specs.size_cm }}` |
| S1 img alt | `בובת ריבורן לוי 48 ס״מ` | `{{ product.metafields.reborn_doll.model_label }} {{ product.metafields.reborn_specs.size_cm }}` |
| S1 hero-sub | `בובת ריבורן לוי נראית...` | `{{ product.metafields.reborn_copy.hero_subtitle }}` |
| S11 headline | `אמהות כבר בחרו בלוי` | `אמהות כבר בחרו ב{{ product.metafields.reborn_doll.hebrew_name }}` |
| S16 FAQ תשובה 1 | `בובת לוי מתאימה מגיל 3` | `{{ product.metafields.reborn_doll.model_label }} מתאימה מגיל 3` |
| S17 כפתור ראשי | `כן, אני רוצה את בובת לוי` | `כן, אני רוצה את {{ product.metafields.reborn_doll.model_label }}` |

### מחיר הבובה (`product.price` / `product.compare_at_price`)

| מיקום | טקסט נוכחי | שדה Liquid |
|---|---|---|
| S1 price-now | `₪299` | `{{ product.price \| money }}` |
| S1 price-old | `₪399` | `{{ product.compare_at_price \| money }}` |
| S1 hero-daily | `פחות מ-₪1 ליום` | hardcoded (לוגיקה) |
| S2 Bundle יחידה אחת | `₪299` | `{{ product.price \| money }}` |
| S15 מחיר | `299 ₪` | `{{ product.price \| money }}` |
| S17 finalcta-price-now | `₪299` | `{{ product.price \| money }}` |
| S17 finalcta-price-old | `₪399` | `{{ product.compare_at_price \| money }}` |
| Sticky Bar | `product.selected_or_first_available_variant.price` | `{{ product.selected_or_first_available_variant.price \| money }}` |

---

## 9. מה צריך לקרות בשלב הבא (המרה ל-Liquid)

**תנאים מוקדמים להמרה:**

1. ✅ חוזה metafields מאושר (מסמך זה)
2. ⬜ metafields נוצרו בשופיפיי Admin (namespace + key + type)
3. ⬜ ערכי לוי הוזנו ב-Admin (hebrew_name, model_label, size_cm, hero_subtitle)
4. ⬜ תמונות מוצר מוכנות ומועלות ל-Shopify CDN
5. ⬜ section schema מוגדר ב-Liquid (settings fallback לכל metafield)

**סדר המרה מומלץ:**

```
1. יצירת metafields ב-Admin (לא לכתוב קוד — רק UI)
2. המרת S1 Hero → Liquid (הכי הרבה שדות דינמיים)
3. המרת S17 Final CTA
4. המרת Sticky Bar
5. שאר הסקשנים (קבועים → העתק כ-HTML ב-Liquid)
```

**לא לבצע עדיין:**
- לא ליצור metafields בשופיפיי
- לא לכתוב לשופיפיי
- לא לדחוף theme

---

*מסמך זה: תכנון בלבד. אין כתיבה לשופיפיי.*
