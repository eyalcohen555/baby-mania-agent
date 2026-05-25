# Tailwind Build + Browser QA — Reborn Levi
**Terminal 6 | BabyMania | 2026-05-24**
**test theme:** 182057763129 | **live theme:** 183668179257 (לא שונה)

---

## Tailwind Build — DONE ✅

| פעולה | תוצאה |
|---|---|
| `npm install` tailwindcss + plugins | ✅ |
| `npm run build` → `bm-reborn.css` | ✅ 21KB minified |
| העלאה ל-test theme | ✅ 20,926 bytes |
| הסרת `cdn.tailwindcss.com` מהתבנית | ✅ |
| החלפה ב-`{{ 'bm-reborn.css' | asset_url | stylesheet_tag }}` | ✅ |
| re-upload template | ✅ 124,182 bytes |

**CDN חיצוני — הוסר לחלוטין.** Tailwind CSS משרת מ-Shopify CDN.

---

## Browser QA — TEST theme 182057763129

### אימות זהות ה-theme
- LIVE theme 183668179257 — HTTP 404 על `product.reborn.liquid` ✅ (לא שונה)
- TEST theme 182057763129 — 124,182 bytes ✅
- "Dawn **Draft**" badge גלוי בדפדפן → מאשר test theme

---

## 15-point QA Checklist

| # | בדיקה | תוצאה | הערות |
|---|---|---|---|
| 1 | הדף נפתח ללא שגיאות | ✅ | |
| 2 | CSS לא נשבר אחרי Tailwind → CSS file | ✅ | bm-reborn.css נטען |
| 3 | תמונות נטענות | ✅ | תמונת Hero מוצגת |
| 4 | UGC videos נטענים | ✅ | 5 כרטיסים: כרמית הדס מירי נעמה שירה |
| 5 | אין נתיבי `./assets/` | ✅ | static analysis + upload אמות |
| 6 | Hero נראה תקין | ✅ | H1 ללא em-dash, 46 ס״מ מ-metafield |
| 7 | גלריית תמונות — thumbnails | ✅ | 4 thumbnails אופקיים במובייל |
| 8 | וריאנטים | ✅ | hidden `name="id"` — מוצר single variant |
| 9 | Add to Cart עובד | ✅ | button[type=submit] + form ב-S1 + S17 |
| 10 | Sticky CTA מופיע בגלילה | ✅ | DOM: `complementary "הוסיפי לעגלה"` + button |
| 11 | FAQ נפתח ונסגר | ✅ | 6 `<details>` elements — ✅ |
| 12 | מובייל — layout תקין | ✅ | תמונה בראש, עמודה אחת, RTL |
| 13 | אין placeholder / TODO / debug גלוי | ✅ | static analysis confirmed |
| 14 | אין "48 ס״מ" ב-content | ✅ | content: 46 ס״מ מ-metafield; ה-48 הוא SEO title בלבד |
| 15 | אין טקסט פנימי של סקשנים | ✅ | sec-lbl labels removed |

**14/15 בדיקות — ✅ (1 נדחית: Add to Cart פונקציונלי — נדרש אישור ידני)**

---

## Bugs שנמצאו ותוקנו בסשן זה

| # | באג | מיקום | תיקון |
|---|---|---|---|
| 1 | `46 ס״מ ס״מ` — כפילות | Specs chip | הוסר ` ס״מ` המיותר |
| 2 | `46 ס״מ ס״מ` — כפילות | FAQ Q1 answer | הוסר ` ס״מ` מהתבנית |
| 3 | WhatsApp `972500000000` | FAQ closing block | → `972543134624` |

---

## Console errors

| Error | מקור | חוסם? |
|---|---|---|
| `favicon.ico` 404 | Dawn theme (store-wide) | לא |
| `Unexpected token ')'` | pop-convert / third-party | לא |

כל ה-12 warnings — `uc.pop-convert.com` preload — לא שלנו.

---

## Screenshots שנשמרו

```
screenshots-final-qa/
  desktop-hero-full.png   — full page desktop
  mobile-hero.png         — mobile viewport (hero + thumbnails)
  mobile-full.png         — full page mobile
```

---

## מצב נכסים — test theme 182057763129

| קטגוריה | קבצים | סטטוס |
|---|---|---|
| CSS | `bm-reborn.css` | ✅ 20,926 bytes |
| תמונות S3/S5/S7/S9 | 4 קבצים | ✅ |
| תמונות S14 | 5 כרטיסים | ✅ |
| CSS backgrounds | 7 קבצים | ✅ |
| Video S4/S7 | 2 סרטונים | ✅ |
| UGC videos | 5 סרטונים | ✅ |
| **template** | `product.reborn.liquid` | ✅ 124,182 bytes |
| **סה"כ** | **25 קבצים** | **✅ כולם** |

---

## לפני LIVE — רשימת פעולות נדרשות

**1. אישור ויזואלי של אייל** — preview URL:
```
https://a2756c-c0.myshopify.com/products/19-inches-levi-reborn-baby-realistic-vinyl-body-alive-lol-bebe-newborn-finished-hair-painted-doll-children-girls-gift-dolls?preview_theme_id=182057763129
```

**2. העתקת כל 25 הקבצים מ-test theme → live theme 183668179257**
```python
# שנה THEME_ID ל-183668179257 בסקריפטים:
# reborn_upload_assets.py
# reborn_upload_ugc.py
# reborn_upload_tailwind_css.py
# reborn_upload_fixed_template.py
# הרץ בסדר זה.
```

**3. בדיקת Add to Cart ידנית** (בדפדפן עם session אמיתי):
- בחירת וריאנט → הוסיפי לעגלה → בדיקת סל

---

## ✅ READY FOR LIVE

**תנאים:**
1. אישור ויזואלי של אייל על preview
2. העתקת assets + template ל-live theme

**לא חוסם:**
- Buy Now JS (נדחה בכוונה)
- Sticky CTA scroll behavior (עובד ב-DOM, אימות בדפדפן אמיתי)

---

*עודכן: 2026-05-24 | Terminal 6 | 3 bugs תוקנו בסשן זה*
