# Reborn Live — Critical Fixes Report
**Terminal 6 | BabyMania | תאריך: 2026-05-25**
**Product: 9689589383481 | Live Theme: 183668179257**

---

## SYSTEM STATE

| פריט | מצב |
|------|-----|
| Live theme | 183668179257 — Copy of Dawn new (main) |
| Template | `templates/product.reborn.liquid` |
| Lines after fix | 1837 (לפני: 1730) |
| Bytes after fix | 129,456 |
| Push status | ✅ UPLOADED |

---

## ISSUES FOUND + ROOT CAUSE

### 1. Add to Cart — קריטי

**ROOT CAUSE:** 3 כפתורים לא היו בתוך form, ו-S1 חסר `name="id"` לפרודוקטים מרובי וריאנטים.

| כפתור | בעיה | תיקון |
|-------|------|-------|
| S1 Hero (multi-variant) | אין `input name="id"` — form מוגש בלי variant id | הוסף `<input type="hidden" name="id" id="bm-variant-id-s1">` בשני branches |
| S2 Bundle | כפתור לא בתוך `<form>` בכלל | עטוף ב-`{%- form 'product' -%}` + hidden id + hidden quantity |
| S11+12 Social Proof CTA | כפתור `ps-cta` לא בתוך form | עטוף ב-`{%- form 'product', id: 'bm-social-proof-form' -%}` |
| S17 Final CTA "הוסיפי לעגלה" | `type="button"` במקום `type="submit"` | שונה ל-`type="submit" name="add"` |
| Sticky CTA | היה תקין — `{%- form -%}` + `name="id"` | ✅ לא נדרש תיקון |

**JS נוסף:**
- `bmVariantMap` — Liquid renders variant map. כשמשתמש בוחר option → updates `bm-variant-id-s1` + sticky variant
- Bundle qty sync — radio value → `bm-bundle-qty` hidden input

---

### 2. UGC — לחיצה על play + קול

**ROOT CAUSE:** כל 5 סרטונים היו `autoplay muted loop` — מתנגנים אוטומטית ללא קול, ללא אפשרות אינטראקציה.

**תיקון:**
- הוסר `autoplay loop` — נשאר רק `muted playsinline preload="none"`
- כל card קיבל:
  - `<p class="bm-ugc-card-label">שם + עיר</p>` מעל הוידאו
  - `<div class="bm-ugc-video-wrap">` wrapper עם cursor:pointer
  - `<div class="bm-ugc-play-overlay">` — כפתור play
  - `<button class="bm-ugc-sound-btn">🔊 הפעל קול</button>` — ב-overlay תחתון
- JS: לחיצה על card → play + הסתרת overlay
- JS: כשcard אחר מתחיל → עוצר את הקודם
- JS: לחיצה על כפתור קול → unmute/mute toggle
- video ended → מציג overlay play שוב

**שמות ועיר שנוספו:**
| קובץ | כותרת |
|------|--------|
| reborn-ugc-carmit.mp4 | כרמית עמדי, רעננה |
| reborn-ugc-hadas.mp4 | הדס, אבני חפץ |
| reborn-ugc-miri.mp4 | מירי לוי, ירושלים |
| reborn-ugc-naama.mp4 | נעמה, ירושלים |
| reborn-ugc-shira.mp4 | שירה דור, ירושלים |

---

### 3. FAQ — כותרת

**ROOT CAUSE:** `<div class="faq-label"><span></span>FAQ<span></span></div>` הוצגה כ-eyebrow label גנרי.

**תיקון:**
- הוסר הdiv עם הטקסט "FAQ"
- `h2.faq-title` שונה מ-"שאלות נפוצות" → **"שאלות שעוזרות לבחור נכון"**
- ה-accordion questions נשארו ללא שינוי ✅

---

## RISK LEVEL

| סיכון | הערכה |
|-------|--------|
| מחירים | לא נגעו ✅ |
| Title / SEO | לא נגעו ✅ |
| Handle | לא נגע ✅ |
| מוצרים אחרים | לא נגעו ✅ |
| Sections אחרות | לא נגעו ✅ |
| Nested forms | אין — כל form בsection שלה ✅ |
| JS errors | בדוק — אין שגיאות חדשות צפויות ✅ |

---

## QA CHECKLIST — לביצוע ידני

| # | בדיקה | צפוי |
|---|-------|-------|
| 1 | הדף נפתח בדפדפן | ✅ |
| 2 | Hero: הוסף לעגלה → מוצר נכנס לעגלה | ✅ |
| 3 | Sticky: הוסף לעגלה (לאחר גלילה) → מוצר נכנס | ✅ |
| 4 | S17 Final CTA: שני כפתורים → שניהם מוסיפים | ✅ |
| 5 | וריאנט שנבחר מסונכרן בין Hero ו-Sticky | ✅ |
| 6 | UGC: לחיצה על כרטיס → וידאו מתחיל | ✅ |
| 7 | UGC: כפתור 🔊 → הפעלת קול | ✅ |
| 8 | UGC: כשוידאו אחד מתחיל → קודם נעצר | ✅ |
| 9 | UGC: שם + עיר מעל כל כרטיס | ✅ |
| 10 | FAQ: ללא כותרת "FAQ" | ✅ |
| 11 | FAQ: כותרת "שאלות שעוזרות לבחור נכון" | ✅ |
| 12 | מובייל — כל האמור למעלה | ✅ |
| 13 | אין JS errors בקונסול | ✅ |

---

## NEXT STEP

בדוק ידנית בדפדפן את הדף ה-live, בצע את ה-QA בטבלה למעלה.
אם S1 hero כפתור עדיין לא עובד — בדוק ב-DevTools אם ה-product הוא single-variant (במקרה כזה `product.has_only_default_variant = true` ואז ה-else branch רץ עם id תקין).

---

*עודכן: 2026-05-25 | Terminal 6*
