---
name: babymania-master
description: |
  תיעוד מקיף של פרויקט Baby Mania Agent.
  כל סוכן שקורא קובץ זה מבין את הפרויקט המלא — החנות, הארכיטקטורה,
  ה-Metafields, פקודות העבודה, ובעיות ידועות.
  טען קובץ זה לפני כל משימה שקשורה לחנות BabyMania.
---

# BabyMania Master Skill
> תיעוד מלא של הפרויקט | עדכון אחרון: מרץ 2026

---

## 1. פרטי החנות

| שדה | ערך |
|-----|-----|
| **שם החנות** | BabyMania |
| **דומיין ציבורי** | babymania-il.com |
| **Shopify URL** | a2756c-c0.myshopify.com |
| **תמה פעילה** | Dawn (Shopify Free Theme) — Shopify OS 2.0 |
| **API Version** | 2024-10 |
| **שוק** | ישראל — עברית RTL בלבד |
| **קהל יעד** | הורים 25–40, בעיקר אמהות |
| **מוצרים פעילים** | 500+ בגדי תינוקות |
| **טווח מחירים** | 99–400 ₪ |
| **ספק** | AliExpress / CJ Dropshipping (סינית) |
| **פרסום** | Meta (פייסבוק + אינסטגרם) |

### מיקום הטוקן

```
קובץ ראשי: C:\Projects\baby-mania-agent\.env
  SHOPIFY_SHOP_URL=a2756c-c0.myshopify.com
  SHOPIFY_CLIENT_ID=...
  SHOPIFY_CLIENT_SECRET=...
  GEMINI_API_KEY=...

קובץ טוקן מאובטח: C:\Users\3024e\Desktop\shopify-token\.env
  SHOPIFY_CLIENT_ID=...
  SHOPIFY_CLIENT_SECRET=...
  SHOPIFY_ACCESS_TOKEN=...
```

**אימות:** OAuth `client_credentials` flow — טוקן תקף ~24 שעות, מתחדש אוטומטית
(ראה `shopify_client.py:_get_access_token()`).
**חוק ברזל:** אסור לכלול keys בפלטים, commits, או קבצים שמועלים.

---

## 2. ארכיטקטורת הסקשנים

### מיקום קבצים

```
C:\Projects\baby-mania-agent\
├── theme/
│   ├── templates/
│   │   └── product.json          ← רשימת + סדר הסקשנים
│   ├── assets/
│   │   └── bm-store.css          ← כל CSS המשותף (CSS variables + classes)
│   └── sections/
│       ├── bm-store-fabric.liquid
│       ├── bm-store-benefits.liquid
│       ├── bm-store-sizes.liquid
│       ├── bm-store-care.liquid
│       ├── bm-store-faq.liquid
│       ├── bm-store-urgency.liquid
│       └── bm-store-contact.liquid
├── config/
│   └── settings.py               ← METAFIELD_NAMESPACE, TEMPLATE_SECTIONS, SECTION_METAFIELD_MAP
├── templates/
│   ├── product-page-template.html  ← תבנית HTML מלאה (Jinja2 preview)
│   └── product_page.html           ← תבנית Jinja2 להרצת ה-agent
├── main.py                       ← נקודת כניסה, CLI
├── shopify_client.py             ← API client (get/update products)
├── gemini_client.py              ← Gemini — תיאורים, יתרונות, תמונות
├── page_builder.py               ← מרכיב HTML מנתוני מוצר
├── output/
│   ├── pages/                    ← HTML מוכן לפני העלאה
│   └── *.html                    ← preview לפי product_id
└── shared_memory.md              ← זיכרון משותף לכל הסוכנים
```

### 8 סקשני Shopify (product.json — לפי סדר)

| # | שם סקשן | תיאור | Metafield |
|---|---------|-------|-----------|
| 1 | `main` | `main-product` — hero, title, price, cart | — |
| 2 | `fabric` | `bm-store-fabric` — סיפור הבד | `baby_mania.fabric_story` |
| 3 | `benefits` | `bm-store-benefits` — יתרונות 6 כרטיסים | `baby_mania.benefits` |
| 4 | `sizes` | `bm-store-sizes` — מדריך מידות accordion | variants + `baby_mania.size_guide_url` |
| 5 | `care` | `bm-store-care` — מפרט + הוראות כביסה | `baby_mania.care_instructions` |
| 6 | `faq` | `bm-store-faq` — שאלות נפוצות accordion | `baby_mania.faq` |
| 7 | `urgency` | `bm-store-urgency` — פס מלאי | `baby_mania.stock_level` + `baby_mania.units_left` |
| 8 | `contact` | `bm-store-contact` — CTA + WhatsApp | `baby_mania.whatsapp_number` + `baby_mania.whatsapp_message` |

> **כלל חשוב:** כל סקשן קורא קודם מ-Metafield. אם ריק — נופל אוטומטית על `section.settings` (ערכי ברירת מחדל מה-Shopify customizer).

### ערכת הצבעים המלאה

| משתנה CSS | ערך | שימוש |
|-----------|-----|--------|
| `--bm-bg` | `#FFFDF9` | רקע דף |
| `--bm-text` | `#1A1A1A` | טקסט ראשי |
| `--bm-brand-green` | `#2F7D32` | CTA, כפתורים |
| `--bm-brand-green-dark` | `#1B5E20` | hover, gradient |
| `--bm-accent-light` | `#E8F5E9` | רקע hover, פריטים פעילים |
| `--bm-cream` | `#FFF8F2` | רקע כרטיסים |
| `--bm-warm-beige` | `#F5EFE6` | רקע אייקונים |
| `--bm-gold-soft` | `#D4A853` | קו קישוט מתחת לכותרות |
| `--bm-muted` | `#757575` | טקסט משני |
| `--bm-border` | `#E7E2DA` | גבולות |
| `--bm-urgent` | `#C62828` | מלאי אזל |
| `--bm-card-shadow` | `0 2px 12px rgba(0,0,0,0.06)` | צל כרטיסים |
| `--bm-card-radius` | `14px` | רדיוס כרטיסים |

> כל CSS מרוכז ב-`theme/assets/bm-store.css`. כל סקשן מייבא: `{{ 'bm-store.css' | asset_url | stylesheet_tag }}`

### פונטים

- **Heebo** (Google Fonts) — RTL, עברית מלאה
- Import: `https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800&display=swap`
- `font-family: 'Heebo', sans-serif` על ה-body

---

## 3. Metafields

**Namespace:** `baby_mania`

### כל ה-keys עם סכמה

| Key | סוג | סקשן שקורא | תיאור |
|-----|-----|-------------|-------|
| `fabric_story` | JSON object | `bm-store-fabric` | `{ "title": "", "dream": "", "body": "", "tags": "tag1,tag2" }` |
| `benefits` | JSON array | `bm-store-benefits` | `[{ "icon": "🌿", "title": "", "desc": "", "chain": "" }]` |
| `size_guide_url` | string (URL) | `bm-store-sizes` | קישור למדריך מידות חיצוני (אופציונלי) |
| `care_instructions` | JSON object | `bm-store-care` | `{ "material": "", "closure": "", "items": [{ "icon": "30°", "text": "" }] }` |
| `faq` | JSON array | `bm-store-faq` | `[{ "question": "", "answer": "" }]` |
| `stock_level` | string | `bm-store-urgency` | `"low"` \| `"in_stock"` \| `"out_of_stock"` |
| `units_left` | integer | `bm-store-urgency` | מספר יחידות שנותרו (אופציונלי, מוצג כש-`stock_level = "low"`) |
| `subtitle` | string | `product-hero` | כותרת משנה מתחת לשם המוצר |
| `badge_text` | string | `product-hero` | תווית על התמונה (NEW / SALE) |
| `available_colors` | JSON array | `color-selector` | רשימת צבעים |
| `color_images` | JSON object | `color-selector` | `{ "צבע": "url" }` |
| `available_sizes` | JSON array | `size-selector` | מידות לפי SKU |
| `gallery_images` | JSON array | `product-gallery` | URLs לתמונות נוספות |
| `material` | string | `product-details` | הרכב בד |
| `country_of_origin` | string | `product-details` | ארץ ייצור |
| `whatsapp_number` | string | `bm-store-contact`, `whatsapp-button` | ספרות בלבד, e.g. `"972501234567"` |
| `whatsapp_message` | string | `bm-store-contact`, `whatsapp-button` | הודעת פתיחה (pre-filled) |
| `related_product_ids` | JSON array | `related-products` | IDs של מוצרים קשורים |

### מיפוי סקשן ← Metafield key(s)

```python
# config/settings.py — SECTION_METAFIELD_MAP
{
  "bm-store-fabric":   ["baby_mania.fabric_story"],
  "bm-store-benefits": ["baby_mania.benefits"],
  "bm-store-sizes":    ["baby_mania.size_guide_url"],
  "bm-store-care":     ["baby_mania.care_instructions"],
  "bm-store-faq":      ["baby_mania.faq"],
  "bm-store-urgency":  ["baby_mania.stock_level", "baby_mania.units_left"],
  "bm-store-contact":  ["baby_mania.whatsapp_number", "baby_mania.whatsapp_message"],
}
```

### גישה ל-Metafield ב-Liquid

```liquid
{% assign value = product.metafields.baby_mania.fabric_story.value %}
{% if value != blank %}
  {% assign obj = value | parse_json %}
{% else %}
  {% assign obj = nil %}  {%- comment -%} → fallback to section.settings {%- endcomment -%}
{% endif %}
```

---

## 4. סינון מוצרים

### מוצרים שמעבדים

- **כל** מוצרי ביגוד תינוקות שה-status שלהם `active` בשופיפיי
- ברירת המחדל: `limit=10` בהרצה רגילה, עד `250` ב-REST API

### מוצרים לדילוג — כללים

| מצב | פעולה |
|-----|--------|
| `product.status != "active"` | דלג אוטומטית |
| `product.variants[0].price == 0` | דלג — מוצר שגוי |
| `product.title` מכיל "TEST" / "test" | דלג — מוצר בדיקה |
| `product.images` ריק | כתב warning, אל תדלג (body_html עדיין עולה) |
| מוצר שכבר עובד (body_html > 5000 chars ומכיל `bm-page`) | דלג — כבר עובד |

> **כלל ברזל:** לא מעבדים מוצר שאין לו וריאנטים עם option1 = מידה. לפני הרצת batch, בדוק שהמוצר אכן בגד תינוקות.

### לוגיקה מלאה לסינון batch

```python
def should_skip(product):
    if product.get("status") != "active":
        return True, "not active"
    if float(product.get("variants", [{}])[0].get("price", 0)) == 0:
        return True, "price=0"
    if "TEST" in product.get("title", "").upper():
        return True, "test product"
    body = product.get("body_html", "") or ""
    if len(body) > 5000 and "bm-page" in body:
        return True, "already processed"
    return False, None
```

---

## 5. תהליך עבודה מלא

### א. עדכון מוצר בודד

```
1. שלוף מוצר:    python main.py --product-id <ID> --dry-run
2. בדוק output/<ID>.html בדפדפן
3. אשר עם המשתמש: "האם לדחוף לשופיפיי?"
4. דחוף:         python main.py --product-id <ID>
```

### ב. הוספת סקשן חדש

```
1. צור קובץ:     theme/sections/bm-store-<name>.liquid
   - כלול: {{ 'bm-store.css' | asset_url | stylesheet_tag }}
   - כלול: {% schema %} עם name, settings, presets
   - לוגיקה: Metafield → parse_json → fallback to section.settings

2. עדכן product.json:
   theme/templates/product.json → הוסף entry ב-"sections" + ב-"order"

3. עדכן settings.py:
   TEMPLATE_SECTIONS → הוסף שם
   SECTION_METAFIELD_MAP → הוסף מיפוי

4. הוסף CSS אם צריך:
   theme/assets/bm-store.css → הוסף בלוק ב-section המתאים

5. בדוק ב-Shopify Theme Editor לפני העלאה
```

### ג. הרצה על batch של מוצרים

```
1. dry-run ראשון:  python main.py --all --limit 5 --dry-run
2. בדוק 5 דפים ב-output/
3. אשר עם המשתמש
4. הרצה מלאה:     python main.py --all --limit 50
5. מעקב: בדוק שה-output/ מלא ואין שגיאות בקונסול
```

---

## 6. פקודות מוכנות

### הרצה על 50 מוצרים

```bash
cd C:/Projects/baby-mania-agent
python main.py --all --limit 50
```

### הרצה על 50 מוצרים עם תמונות

```bash
python main.py --all --limit 50 --images
```

### Dry-run — 10 מוצרים (ללא העלאה לשופיפיי)

```bash
python main.py --all --limit 10 --dry-run
```

### מוצר בודד — dry-run

```bash
python main.py --product-id 9940751417657 --dry-run
```

### מוצר בודד — עם העלאה

```bash
python main.py --product-id 9940751417657
```

### בדיקת Metafields למוצר בודד (GraphQL)

```bash
# דרך Shopify Admin API — GraphQL
curl -s -X POST \
  "https://babymania-il.myshopify.com/admin/api/2024-10/graphql.json" \
  -H "X-Shopify-Access-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ product(id: \"gid://shopify/Product/9940751417657\") { metafields(namespace: \"baby_mania\", first: 20) { edges { node { key value type } } } } }"
  }'
```

### רשימת כל המוצרים (REST)

```bash
curl -s \
  "https://babymania-il.myshopify.com/admin/api/2024-10/products.json?limit=50&fields=id,title,status,body_html" \
  -H "X-Shopify-Access-Token: $TOKEN" | python -m json.tool
```

### העלאת קבצי theme ל-Shopify (Shopify CLI)

```bash
# חייב: npm install -g @shopify/cli
cd C:/Projects/baby-mania-agent/theme
shopify theme push --store babymania-il.myshopify.com
```

### העלאת קובץ section בודד

```bash
shopify theme push --only sections/bm-store-fabric.liquid --store babymania-il.myshopify.com
```

---

## 7. בעיות ידועות ופתרונות

| בעיה | סיבה | פתרון |
|------|-------|--------|
| `<style>` tags ב-body_html לא עובדים | שופיפיי מסנן `<style>` מה-body | **Inline CSS בלבד** ב-`body_html`. ב-Liquid sections — קובץ CSS נפרד ב-assets |
| Unicode output שבור בWindows console | encoding ברירת מחדל cp1255 | `main.py` כולר `reconfigure(encoding="utf-8")` בתחילה |
| טוקן Shopify פג תוך ~24 שעות | OAuth client_credentials | `shopify_client._get_access_token()` מתחדש אוטומטית בכל קריאה |
| `parse_json` ב-Liquid נכשל אם JSON לא תקין | Metafield עם ערך שגוי | תמיד בדוק Metafield ב-Admin לפני שדוחפים; שמור raw string בלי whitespace מיותר |
| גלריית תמונות לא מוצגת ב-Shopify | `product.images` לא נכלל ב-`body_html` | **לעולם** לא לבנות gallery בתוך body_html. זה role של הtheme (main-product section) |
| `section.id` conflicts ב-page עם אותו section פעמיים | Shopify מאפשר section אחד מסוג בודד בtemplate | כל ID element צמוד ל-`{{ section.id }}` כדי למנוע conflicts |
| Gemini מחזיר HTML עם Markdown code blocks | הפרומפט לא מדויק מספיק | כבר מתוקן בפרומפט: "החזר רק HTML נקי, בלי markdown, בלי בלוק קוד" |
| מוצר עם "One Size" — אין שורות בטבלת מידות | הלוגיקה מציגה רק מידות שבוריאנטים | הוסף בדיקה: אם variants == 1 ו-option1 == "One Size" → אל תציג טבלה |
| WhatsApp number format שגוי | ספרות עם `+` או `-` | Metafield `whatsapp_number` חייב ספרות בלבד: `972501234567` |

---

## 8. מודלים ו-AI

| מודל | שימוש | קובץ |
|------|-------|------|
| `gemini-2.5-flash` | תיאורי מוצר בעברית + יתרונות | `gemini_client.py` |
| `gemini-2.0-flash-preview-image-generation` | יצירת תמונות מוצר | `gemini_client.py` |

**כלל ברזל:** תמונות נוצרות רק עם `--images` flag. בלי הflag — מדלגים על שלב 3 בתהליך.

---

## 9. חוקים שאסור לשבור

1. **לא מפברקים מידע** — הרכב בד, תעודות, מפרט טכני — רק ממה שיש. אם חסר → שואלים את בעל החנות
2. **לא דוחפים לשופיפיי ללא אישור מפורש** — תמיד dry-run ראשון, תמיד שמירה ב-`output/` לפני
3. **לא נוגעים ב:** `title`, `variants`, `price`, `compare_at_price`, `tags`, `images`, `inventory`, `metafields` — רק `body_html`
4. **Inline CSS בלבד ב-body_html** — לא `<style>`, לא classes חיצוניות
5. **RTL עברית מלאה** — כל טקסט בעברית, `dir="rtl"`, פונט Heebo
6. **כל פלט נשמר תחילה ב-`output/`** — ריצה בטוחה, תמיד ניתן לחזור
7. **לא מעלים theme לשופיפיי ללא אישור** — המתן לאישור משתמש לפני כל `shopify theme push`

---

## 10. פקודת debug מהירה

```python
# בדוק שכל ה-imports תקינים
cd C:/Projects/baby-mania-agent
python -c "from config.settings import METAFIELD_NAMESPACE, TEMPLATE_SECTIONS, SECTION_METAFIELD_MAP; print('OK — namespace:', METAFIELD_NAMESPACE, '| sections:', len(TEMPLATE_SECTIONS))"
```

תוצאה צפויה:
```
OK — namespace: baby_mania | sections: 15
```
