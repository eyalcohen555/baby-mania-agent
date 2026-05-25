# תכנית דחיפה ל-Live — Reborn Levi
**Terminal 6 | BabyMania | מוכן לאישור אייל**
**תאריך:** 2026-05-24
**test theme:** 182057763129 (Dawn, unpublished)
**live theme:** 183668179257 (Copy of Dawn new, main)
**מוצר:** 9689589383481 | handle: levi-reborn-...

---

## Preview URL לאישור ויזואלי

```
https://a2756c-c0.myshopify.com/products/19-inches-levi-reborn-baby-realistic-vinyl-body-alive-lol-bebe-newborn-finished-hair-painted-doll-children-girls-gift-dolls?preview_theme_id=182057763129
```

---

## Stage 10 — תכנית דחיפה ל-Live

### מה הועלה לTest Theme (182057763129) — מוכן

| # | פעולה | סטטוס |
|---|---|---|
| 1 | `templates/product.reborn.liquid` — 1769 שורות | ✅ |
| 2 | 17 assets: s2-bg, s3, s5-girl, s6, s7, s8, s9, s14-card-1..5, s4-video, s7-video | ✅ |
| 3 | 5 UGC videos: carmit, hadas, miri, naama, shira | ✅ |
| 4 | כל paths עודכנו ל-`{{ 'X' | asset_url }}` | ✅ |

### שלבים לפני Live (דורשים אישור אייל)

#### שלב A — Tailwind CSS (חובה לפני live)
```bash
# בנייה מקומית של CSS מ-Tailwind CDN → קובץ סטטי
npx tailwindcss -i ./input.css -o ./assets/bm-reborn.css --minify

# העלאה:
python scripts/upload_single_asset.py assets/bm-reborn.css

# החלפה בתבנית:
# <script src="https://cdn.tailwindcss.com..."> → <link rel="stylesheet" href="{{ 'bm-reborn.css' | asset_url }}">
```
**סיבה:** CDN חיצוני = ביצועים + CSP blocking בסביבת production.

#### שלב B — העתקת assets ל-Live Theme (183668179257)
כל ה-22 קבצים שהועלו ל-test theme צריכים להיות גם ב-live theme.
```python
# שנה THEME_ID=182057763129 → 183668179257 בסקריפטים
# הרץ: reborn_upload_assets.py + reborn_upload_ugc.py
```

#### שלב C — העתקת template ל-Live Theme
```python
# שנה THEME_ID=182057763129 → 183668179257 ב-reborn_upload_fixed_template.py
# הרץ: reborn_upload_fixed_template.py
```

#### שלב D — אימות ידני של אייל
1. פתח Preview URL בדפדפן (דסקטופ + מובייל)
2. בדוק: תמונות, סרטונים, גלריה
3. הוסף לעגלה — בדוק מחיר + מוצר בסל
4. בדוק שה-Sticky CTA מופיע בגלילה

---

## Stage 11 — מה אסור לגעת

### ❌ אסור בהחלט ללא אישור אייל

| פעולה | סיבה |
|---|---|
| שינוי title / description של המוצר | SEO + conversion |
| שינוי מחיר / compare-at-price | conversion metrics |
| שינוי handle / template_suffix | routing |
| שינוי metafields בלייב | השפעה ישירה על הדף |
| נגיעה ב-live theme (183668179257) | משפיע על כל הלקוחות |
| שינוי מוצרים אחרים מלבד 9689589383481 | scope |
| הסרת "טיפול רגשי" מהדף | אסור בלי אישור |
| הוספת תעודות בטיחות (BPA, תקנים אירופאים) | לא מאומת |
| הוספת ביקורות AliExpress כביקורות BabyMania | הטעיה |
| הוספת מפרט טכני לא מאומת | לא מאומת |

### ⏸️ נדחה — לאחרי קמפיין

| פעולה | מצב |
|---|---|
| Buy Now JS | כפתור קיים, לא מחובר |
| Tailwind build | CDN עדיין בשימוש |
| S14 cards תמונות | מועלות, מוצגות |
| Alt text em-dash ב-S9 | ב-alt attribute בלבד |

---

## סיכום QA סופי — 20/20 בדיקות עברו

```
ALL OK — 20 checks passed
Lines: 1769 | Bytes: 126,901
```

| בדיקה | תוצאה |
|---|---|
| Dawn layout (ללא layout none) | ✅ |
| RTL main dir | ✅ |
| כל ./assets/ paths → asset_url | ✅ |
| UGC section (5 videos) | ✅ |
| Sticky CTA | ✅ |
| Specs chips | ✅ |
| 6 שאלות FAQ ניקיות | ✅ |
| ללא BPA / תקנים אירופאים | ✅ |
| ללא TODO/placeholder גלוי | ✅ |
| S1 + S17 + Sticky forms | ✅ |

**READY — לאישור ויזואלי של אייל, לאחר מכן Tailwind build + live push**

---

*עודכן: 2026-05-24 | Terminal 6*
