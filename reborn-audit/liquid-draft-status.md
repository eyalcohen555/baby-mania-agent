# סטטוס Liquid Draft — שלב 7
**טרמינל 6 | BabyMania | ריבורן בלבד**
**עדכון:** 2026-05-24
**קובץ בסיס:** `output/pages/reborn-landing/levi-reborn-product-v2.html` (1586 שורות)

---

## 1. קובץ שנוצר

`output/pages/reborn-landing/levi-reborn-product-liquid-draft.liquid` (1636 שורות)

הקובץ המקורי (`v2.html`) **לא שונה**.

---

## 2. מה הומר ל-Liquid

| מיקום | אלמנט | מצב |
|---|---|---|
| `<title>` | שם דגם + גודל | ✅ Liquid |
| S1 L509 | `bm_variant` assign | ✅ Liquid |
| S1 L510 | `bm_model` (model_label / fallback title) | ✅ Liquid |
| S1 L511 | `bm_size` (size_cm) | ✅ Liquid |
| S1 L512 | `bm_subtitle` (hero_subtitle / fallback description) | ✅ Liquid |
| S1 L513–516 | price, compare_at_price, save% | ✅ Liquid |
| S1 L525 | `hero-prod-name` | ✅ Liquid |
| S1 L527 | `hero-sub` | ✅ Liquid |
| S1 L530–536 | price row (money_without_trailing_zeros) | ✅ Liquid |
| S1 L541 | `{% form 'product', product, id: 'bm-product-form-s1' %}` | ✅ |
| S1 L541–564 | variant selector (options_with_values) | ✅ Liquid |
| S1 L604 | hero image (product.images[0] \| image_url) | ✅ Liquid |
| S17 L1510 | `bm17_variant` assign | ✅ Liquid |
| S17 L1520–1525 | price row (money_without_trailing_zeros, save%) | ✅ Liquid |
| S17 L1542 | `{% form 'product', product, id: 'bm-product-form-s17' %}` | ✅ |
| S17 L1544 | CTA button text (model_label / fallback title) | ✅ Liquid |

---

## 3. מה נשאר hardcoded (בכוונה)

| סקשן | אלמנט | סיבה |
|---|---|---|
| S2 Bundle | מחירים ₪299/₪549/₪779 | סקשן מחוץ לתחולת שלב 7 |
| S11 Social Proof | "+2,400 אמהות" / "4.9★" | ביקורות — נתונים מדומים, TODO נפרד |
| S13 Stat | "48 ס״מ" | S13 מחוץ לתחולת שלב 7 (צריך עדכון ל-46 ס״מ בשלב נפרד) |
| S15 Price compare | 299 ₪ | S15 מחוץ לתחולת שלב 7 |
| S16 FAQ | כל הטקסט | FAQ — שלב נפרד עם baby_mania.faq |
| S1 Hero H1 | טקסט שיווקי | קופי קבוע — לא שם מוצר |
| trust bar | טקסטים קבועים | לא תלוי מוצר |
| countdown JS | 10 דקות | לוגיקה קבועה |

---

## 4. Add to Cart

| טופס | מצב |
|---|---|
| S1 — `bm-product-form-s1` | ✅ מוכן — `{% form 'product', product %}` עם variant selector |
| S17 — `bm-product-form-s17` | ✅ מוכן — `{% form 'product', product %}` עם hidden id |
| "קני עכשיו" (S1) | TODO Stage 8 — צריך JS buy-now redirect לצ'קאאוט |
| כפתור שני S17 | TODO Stage 8 — JS dedup אם שני כפתורים באותו form |

---

## 5. Variants

| מצב | פירוט |
|---|---|
| ✅ דינמי | `product.options_with_values` + `product.has_only_default_variant` |
| fallback | אם מוצר ברירת מחדל — `<input type="hidden" name="id" value="{{ product.variants.first.id }}"/>` |
| לוי (PID 9689589383481) | ייתכן שיש variants של vinyl/silicone — selector יוצג אוטומטית |

---

## 6. Liquid Validation (בדיקה מקומית)

| בדיקה | תוצאה |
|---|---|
| `{% layout none %}` | ✅ |
| `bm_variant assign` | ✅ |
| `form 'product', product` | ✅ (×2) |
| `endform` | ✅ (×2 — L564, L1549) |
| `bm17_variant assign` | ✅ |
| `money_without_trailing_zeros` | ✅ |
| hardcoded "Reborn Baby Levi 48cm" | ✅ הוסר מ-S1 |
| ₪299 בS1/S17 | ✅ הוסר (נשאר רק ב-S2/S15 — כוונה) |

---

## 7. האם אפשר לעבור לשלב העלאה ל-theme test?

**כמעט** — נדרש לפני העלאה:

- [ ] להוסיף `{% section_tag %}` / להתאים ל-template structure של Dawn (sections JSON)
- [ ] לפתור TODO של "קני עכשיו" (JS buy-now) — Stage 8
- [ ] לאמת ב-Shopify Theme Editor עם `product: levi` כ-preview
- [ ] לבדוק שה-metafields מוצגים נכון ב-online store (לא רק ב-admin)

**בינתיים** — הקובץ מוכן לבדיקה ב-Shopify Theme Editor כ-draft template.

---

## 8. קבצים שנוצרו

| קובץ | תיאור |
|---|---|
| `output/pages/reborn-landing/levi-reborn-product-liquid-draft.liquid` | ✅ קובץ Liquid חדש |
| `output/pages/reborn-landing/levi-reborn-product-v2.html` | ✅ קובץ מקורי — לא שונה |
| `reborn-audit/liquid-draft-status.md` | ✅ מסמך זה |
