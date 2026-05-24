# טיוטת ערכי Metafields — לוי בלבד
**PID:** 9689589383481
**תאריך:** 2026-05-24
**סטטוס:** טיוטה — לא לכתיבה לשופיפיי עדיין

---

## ערכים מוכנים לכתיבה (לאחר אישור)

### namespace: `reborn_doll`

| key | ערך | הערה |
|---|---|---|
| `hebrew_name` | `לוי` | שם קצר לתצוגה |
| `model_label` | `בובת ריבורן לוי` | לכפתורי CTA וכותרות |

### namespace: `reborn_specs`

| key | ערך | הערה |
|---|---|---|
| `size_cm` | `46 ס״מ` | החלטת אייל — Ali=17-18 inches |
| `source_note` | `לפי נתוני ספק` | הסבר לפער בין 49cm ל-46cm |

### namespace: `reborn_copy`

| key | ערך | הערה |
|---|---|---|
| `hero_subtitle` | `בובת ריבורן לוי נראית ומרגישה כמו תינוק אמיתי: 46 ס״מ, מגע רך, הבעה עדינה, בקבוק ומוצץ מגנטי באריזה.` | פסקת hero — S1 |

### namespace: `baby_mania` (רשות שלב 1)

| key | ערך | הערה |
|---|---|---|
| `faq` | ראה JSON למטה | 5 שאלות מותאמות לריבורן/לוי |

---

## baby_mania.faq — JSON מלא

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

## Liquid שימוש — מפת הזרקה

```liquid
{# S1 hero-prod-name #}
{{ product.metafields.reborn_doll.model_label }} {{ product.metafields.reborn_specs.size_cm }}

{# S1 hero-sub #}
{{ product.metafields.reborn_copy.hero_subtitle }}

{# S1 price #}
{{ product.price | money }} / {{ product.compare_at_price | money }}

{# S11 headline #}
אמהות כבר בחרו ב{{ product.metafields.reborn_doll.hebrew_name }}

{# S13 stat #}
{{ product.metafields.reborn_specs.size_cm }}

{# S17 CTA button #}
כן, אני רוצה את {{ product.metafields.reborn_doll.model_label }}

{# S17 price #}
{{ product.price | money }} / {{ product.compare_at_price | money }}

{# <title> #}
{{ product.metafields.reborn_doll.model_label }} {{ product.metafields.reborn_specs.size_cm }} | Baby Mania
```

---

*לא לכתוב לשופיפיי לפני אישור אייל.*
