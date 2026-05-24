# סטטוס Dawn Template Prep — שלב 8
**טרמינל 6 | BabyMania | ריבורן בלבד**
**עדכון:** 2026-05-24
**מוצר בדיקה:** PID 9689589383481 (לוי)

---

## 1. קבצים שנוצרו

| קובץ | שורות | מצב |
|---|---|---|
| `output/theme-test/sections/bm-reborn-product-page.liquid` | 1608 | ✅ נוצר |
| `output/theme-test/templates/product.reborn-test.json` | 12 | ✅ נוצר |
| `output/pages/reborn-landing/levi-reborn-product-liquid-draft.liquid` | 1636 | ✅ עודכן (פיקסים) |
| `output/pages/reborn-landing/levi-reborn-product-v2.html` | 1586 | ✅ לא שונה |

---

## 2. מבנה Section

| אלמנט | מצב |
|---|---|
| `{% comment %}` header | ✅ |
| Google Fonts `<link>` | ✅ |
| Tailwind CDN `<script>` (test only) | ✅ |
| `tailwind.config` script block | ✅ |
| `{% stylesheet %}` — 429 שורות CSS | ✅ |
| תוכן `<main>` — כל S1–S17 | ✅ (1061 שורות) |
| `{% javascript %}` — trust bar + countdown | ✅ (49 שורות) |
| `{% schema %}` | ✅ |
| DOCTYPE / `<html>` / `<head>` / `<nav>` / `<footer>` | ✅ הוסרו |

---

## 3. Template JSON

```json
{
  "sections": {
    "main": {
      "type": "bm-reborn-product-page",
      "settings": {}
    }
  },
  "order": ["main"]
}
```

**שם section:** `bm-reborn-product-page`
לא שונה: `product.json` / `product.clothing.json` / `product.accessories.json`

---

## 4. שדות Liquid

| שדה | מצב |
|---|---|
| `product.selected_or_first_available_variant` | ✅ |
| `product.metafields.reborn_doll.model_label` | ✅ (S1, S17, title) |
| `product.metafields.reborn_copy.hero_subtitle` | ✅ (S1 sub) |
| `product.metafields.reborn_specs.size_cm` | ✅ (S1 prod-name, S13 stat, title) |
| `product.metafields.reborn_doll.hebrew_name` | ✅ (S11 headline) |
| `bm_variant.price | money_without_trailing_zeros` | ✅ (×4 — S1+S17) |
| `bm_compare > bm_price` → save% | ✅ |
| Fallback לכל metafield | ✅ `default: product.title` |
| variant selector (`options_with_values`) | ✅ |
| single-variant fallback (`has_only_default_variant`) | ✅ |

---

## 5. Add to Cart

| טופס | ID | מצב |
|---|---|---|
| S1 Hero | `bm-product-form-s1` | ✅ `{% form 'product', product %}` |
| S17 Final CTA | `bm-product-form-s17` | ✅ `{% form 'product', product %}` |
| endform count | 2/2 | ✅ |

---

## 6. Buy Now — נדחה

| | |
|---|---|
| מצב | TODO — לא מחובר |
| סיבה | דורש JS redirect לצ'קאאוט — לא בטוח לבנות ללא בדיקה בסביבה אמיתית |
| פתרון | לשלב 9: `window.location = '/checkout?...add=VARIANT_ID'` בלחיצה |
| כפתורים | S1: `btn-outline` / S17: `btn-outline-white` — נשארו כ-button type=button |

---

## 7. פיקסים שבוצעו (על liquid-draft + section)

| פיקס | מצב |
|---|---|
| S13 stat: "48 ס״מ" → `{{ product.metafields.reborn_specs.size_cm.value \| default: '46 ס״מ' }}` | ✅ |
| S11 H2: "+2,400 אמהות" → `אמהות כבר בחרו ב{{ hebrew_name }}` | ✅ |
| S1 review count: "(2,400 ביקורות)" → "ביקורות לקוחות" + TODO | ✅ |
| S11 rating: "4.9 מתוך 5" → "דירוג לקוחות" + TODO | ✅ |

---

## 8. מה עדיין hardcoded (בכוונה — מחוץ לתחולת שלב 8)

| מיקום | ערך | סיבה |
|---|---|---|
| S2 Bundle | ₪299 / ₪549 / ₪779 | מחכה להחלטת bundle API |
| S15 Price compare | 299 ₪ | סקשן static — לא תלוי PID |
| S16 FAQ | 5 שאלות | ממתין לשלב FAQ (baby_mania.faq) |
| S1 H1 | טקסט שיווקי | קופי קבוע — לא שם מוצר |
| trust bar | 14 יום / SSL / משלוח חינם | קבוע ברמת חנות |
| countdown | 10 דקות | קבוע |

---

## 9. בעיה טכנית אחת: Tailwind CDN

| | |
|---|---|
| מצב | CDN בתוך section — עובד לבדיקה |
| בעיה ב-production | CDN לא מותר ב-Dawn theme בצורה זו לפרודקשן |
| פתרון | לפני push ל-live: להעביר Tailwind לקובץ CSS compiled ב-`assets/` |
| השפעה על שלב 9 | לא חוסם בדיקה — חוסם רק push ל-production |

---

## 10. האם אפשר לעבור לשלב 9 (העלאה ל-theme test)?

**כמעט מוכן** — חסר:

- [ ] העלאת `sections/bm-reborn-product-page.liquid` ל-Shopify theme (draft/unpublished)
- [ ] העלאת `templates/product.reborn-test.json` ל-Shopify theme
- [ ] שינוי template_suffix של לוי ל-`reborn-test` (או בדיקה ב-theme preview)
- [ ] אישור אייל לפני שינוי template suffix

**לא חוסם את הבדיקה:**
- Buy Now (לא נדרש לבדיקת S1/S17)
- Tailwind CDN (עובד בבדיקה)
- S2/S15/S16 hardcoded (מחוץ לתחולה)
