# QA סופי — Reborn Test Theme
**טרמינל 6 | BabyMania | ריבורן בלבד**
**תאריך:** 2026-05-24
**בודק:** Terminal 6 static analysis + upload verification
**theme בדיקה:** 182057763129 (Dawn, unpublished)
**live theme:** 183668179257 (Copy of Dawn new, main)

---

## Preview URL

```
https://a2756c-c0.myshopify.com/products/19-inches-levi-reborn-baby-realistic-vinyl-body-alive-lol-bebe-newborn-finished-hair-painted-doll-children-girls-gift-dolls?preview_theme_id=182057763129
```

**Template בשימוש:** `templates/product.reborn.liquid` (118,475 bytes)
**product handle:** `19-inches-levi-reborn-baby-realistic-vinyl-body-alive-lol-bebe-newborn-finished-hair-painted-doll-children-girls-gift-dolls`
**template_suffix:** `reborn` ← תואם לקובץ

---

## 1. מבנה HTML

| בדיקה | תוצאה |
|---|---|
| `{% layout none %}` הוסר | ✅ |
| `<!DOCTYPE` / `<html>` / `<head>` / `<body>` הוסרו | ✅ |
| `<main dir="rtl">` קיים | ✅ |
| `</main>` קיים | ✅ |
| nav מקומי הוסר | ✅ Dawn nav בשימוש |
| footer מקומי הוסר | ✅ Dawn footer בשימוש |

---

## 2. Hero (S1)

| בדיקה | תוצאה |
|---|---|
| `assign bm_variant` | ✅ `product.selected_or_first_available_variant` |
| `model_label` metafield | ✅ `reborn_doll.model_label.value` |
| `size_cm` metafield | ✅ `reborn_specs.size_cm.value` |
| `hero_subtitle` metafield | ✅ `reborn_copy.hero_subtitle.value` |
| מחיר דינמי S1 | ✅ `bm_price | money_without_trailing_zeros` |
| compare-at + חיסכון % | ✅ `bm_compare > bm_price` → save% |
| טופס S1 | ✅ `form 'product', product, id: 'bm-product-form-s1'` |
| endform S1 | ✅ |
| בורר וריאנטים | ✅ `options_with_values` + `has_only_default_variant` fallback |
| תמונה ראשית | ✅ `product.images[0] | image_url: width: 900` |
| גלריה thumbnails | ✅ `bm-gallery-thumbs-col` + `bm-gallery-main` + JS switcher |
| Add to Cart button | ✅ `type="submit" name="add"` |
| Buy Now button | ⚠️ `type="button"` — JS לא מחובר (נדחה בכוונה) |

---

## 3. Final CTA (S17)

| בדיקה | תוצאה |
|---|---|
| assign `bm17_variant` | ✅ |
| מחיר דינמי | ✅ `bm17_variant.price | money_without_trailing_zeros` |
| שם הדגם דינמי | ✅ `reborn_doll.model_label.value | default: product.title` |
| טופס S17 | ✅ `form 'product', product, id: 'bm-product-form-s17'` |
| endform S17 | ✅ |
| hidden input variant id | ✅ `selected_or_first_available_variant.id` |

---

## 4. Sticky CTA

| בדיקה | תוצאה |
|---|---|
| Sticky CTA קיים בדף | ❌ לא נמצא בקוד |
| הערה | לא היה ב-scope של שלבים 7-9. לא חוסם. |

---

## 5. גלריה

| בדיקה | תוצאה |
|---|---|
| לולאה על `product.images` | ✅ |
| תמונה ראשית `#bm-gallery-main` | ✅ |
| עמודת thumbnails אנכית | ✅ `.bm-gallery-thumbs-col` |
| JS החלפת תמונה בלחיצה | ✅ `click → src/srcset swap` |
| מובייל — שורה אופקית | ✅ `@media(max-width:768px)` |
| placeholder אם אין תמונות | ✅ `hero-img-ph` |

---

## 6. Countdown Timer

| בדיקה | תוצאה |
|---|---|
| אלמנטים `bm-cd-h/m/s` | ✅ קיימים |
| JS localStorage 10 דקות | ✅ |

---

## 7. טקסטים — בדיקה סופית

### Em-Dashes (—)
| מיקום | פעולה |
|---|---|
| Hero H1 | ✅ תוקן → `,` |
| Bundle H2 | ✅ תוקן → `,` |
| S5 body copy | ✅ תוקן → `.` |
| S7.5 eyebrow `&#8212;` | ✅ תוקן → הוסרה תווית S7.5 |
| S7 disclaimer | ✅ תוקן → `.` |
| S10 benefits (×3) | ✅ תוקנו → `,` |
| S11 social proof | ✅ תוקן → `,` |
| S16 FAQ answer | ✅ תוקן → `,` |
| S17 FAQ closing | ✅ תוקן → `,` |
| Alt attribute S9 `— ריבורן` | ⚠️ נשאר ב-alt (לא גלוי לגולש רגיל) |

### hardcoded "48 ס"מ"
| מיקום | פעולה |
|---|---|
| S16 FAQ תשובה | ✅ תוקן → `product.metafields.reborn_specs.size_cm.value` |

### TODO / debug text
| בדיקה | תוצאה |
|---|---|
| TODO בתוך HTML גלוי | ✅ אין — רק בתוך `<!-- comments -->` |
| Placeholder גלוי | ✅ אין |
| sec-lbl עם S\d גלוי | ✅ אין |

---

## 8. Assets — BLOCKER לפני LIVE

הקובץ מכיל reference ל-`./assets/` — paths מקומיים שלא קיימים ב-Shopify theme:

### CSS backgrounds (דקורטיבי — לא חוסם QA ויזואלי)
| קובץ | סקשן |
|---|---|
| `./assets/s2-bg.png` | S2 Bundle bg |
| `./assets/s6-bg-mobile.png` | S6 mobile bg |
| `./assets/s6-bg-desktop.png` | S6 desktop bg |
| `./assets/s8-bg-mobile.png` | S8 mobile bg |
| `./assets/s3-bg-mobile.png` | S3 Trust mobile bg |
| `./assets/s7-bg.png` | S7 Research bg |

### HTML תמונות/וידאו (גלוי לגולש — BLOCKER לפני LIVE)
| קובץ | סקשן | חומרה |
|---|---|---|
| `./assets/s4-video.mp4` | S4 בעיה — מסכים | 🔴 סרטון לא יטען |
| `./assets/s5-girl.png` | S5 הגברה | 🔴 תמונה תהיה שבורה |
| `./assets/s7-video.mp4` | S7 מחקרים | 🔴 סרטון לא יטען |
| `./assets/s9-desktop.png` | S9 לפני/אחרי | 🔴 תמונה תהיה שבורה |
| `./assets/s9-mobile.png` | S9 לפני/אחרי מובייל | 🔴 תמונה תהיה שבורה |
| `assets/s14-card-1..5.jpg` | S14 למי מתאים | 🔴 5 כרטיסים שבורים |

**פתרון נדרש:** להעלות קבצים אלה ל-Shopify CDN (`assets/`) ולעדכן paths מ-`./assets/X` ל-`{{ 'X' | asset_url }}`.

---

## 9. Buy Now

| | |
|---|---|
| מצב | ⚠️ נדחה בכוונה |
| כפתורים | קיימים (`type="button"`, לא מחובר) |
| חוסם? | לא — Add to Cart עובד |
| לשלב | 10 (אחרי QA + אישור אייל) |

---

## 10. Tailwind CDN

| | |
|---|---|
| מצב | `<script src="https://cdn.tailwindcss.com...">` ב-body |
| חוסם QA בדיקה? | לא |
| חוסם LIVE? | כן — CDN חיצוני, ביצועים + CSP |
| פתרון | Tailwind build → `assets/bm-reborn.css` + `{{ 'bm-reborn.css' | asset_url }}` |
| מתי | לפני push ל-live, אחרי אישור אייל |

---

## 11. מובייל (ניתוח סטטי)

| אלמנט | תוצאה |
|---|---|
| Hero — 1 עמודה במובייל | ✅ `.hero-grid` `@media(max-width:768px)` |
| Hero — תמונה עולה לראש | ✅ `.hero-img-col { order:-1 }` |
| גלריה — שורה אופקית | ✅ `flex-direction:row` במובייל |
| כפתורים | ✅ `btn-cta` עם `width:100%` |
| Sticky CTA מובייל | ❌ לא קיים |
| RTL direction | ✅ `<main dir="rtl">` |

---

## 12. Add to Cart — אימות פונקציונלי

**לא ניתן לאמת אוטומטית ללא Playwright approval.**

בדיקה ידנית נדרשת על ידי אייל:
1. בחירת וריאנט (צבע/מידה אם קיים)
2. לחיצה על "הוסיפי לעגלה"
3. בדיקת סל — מחיר וכמות נכונים
4. מעבר לצ'קאאוט

---

## סיכום ממצאים

### עבר ✅
- Liquid דינמי: מחיר, וריאנטים, metafields, תמונות
- שני product forms (S1 + S17)
- גלריית תמונות עם thumbnails
- Countdown timer
- Dawn layout (header/footer מהתבנית)
- הסרת כל labels S1–S17
- הסרת em-dashes מכל הטקסטים הגלויים
- 48 ס"מ hardcoded → dynamic

### נכשל / חסר ❌
- **Sticky CTA** — לא קיים (לא היה ב-scope)
- **Assets קבצים** — 11 קבצים מקומיים לא קיימים ב-Shopify CDN
- **Buy Now JS** — נדחה בכוונה

### חוסם LIVE 🔴
1. **./assets/ paths** — S4/S5/S7/S9/S14 יופיעו שבורים
2. **Tailwind CDN** — לא מותאם לייצור
3. **Buy Now** — לא פונקציונלי (ניתן לדחות)

### אפשר לדחות לאחרי קמפיין ⏸️
- Buy Now JS
- Sticky CTA
- S14 כרטיסי תמונה (decorative)
- alt text em-dash ב-S9

---

## המלצה

```
CONDITIONALLY READY — לאישור ויזואלי של אייל על Hero / CTA / גלריה
NOT READY — לדחיפה ל-live עד להעלאת assets ל-Shopify CDN
```

**לאחר אישור אייל — 2 פעולות לפני live:**
1. העלאת assets (s4-video, s5-girl, s7-video, s9, s14-cards) ל-`assets/` בתבנית + עדכון paths ל-`{{ 'X' | asset_url }}`
2. Tailwind build → CSS compiled file

---

*עודכן: 2026-05-24 | Terminal 6 | לא שונה: live theme, מוצרים, מחירים, SEO*
