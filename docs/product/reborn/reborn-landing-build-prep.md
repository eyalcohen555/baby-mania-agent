# Reborn Landing Page Build Prep

**תפקיד:** מסמך הכנה לבנייה — דף נחיתה ריבורן
**נוצר:** 2026-04-26
**כפוף ל:** `docs/product/reborn/REBORN-MASTER-PROMPT.md` → `BABYMANIA-MASTER-PROMPT.md`

---

## Status

Build prep only — no live Shopify.
לא לגעת ב-theme live.
לא לעשות push לקוד.
לא לפרסם דף.
לא לכתוב קופי סופי.
לא לנעול FAQ.

---

## 1. Build Scope

דף נחיתה ריבורן כללי — קטגוריה בלבד.

**בסקופ:**
- דף נחיתה כללי לקטגוריית ריבורן

**מחוץ לסקופ:**
- דפי מוצר בודדים
- בלוג / תוכן אורגני
- דף בית
- Shopify live
- theme קוד
- push לכל remote

---

## 2. Approved Page Flow

9 סקשנים מאושרים — סדר נעול:

| # | שם | תפקיד פסיכולוגי |
|---|---|---|
| 1 | HERO | פתיחת החלום |
| 2 | פתיחת אמון | הורדת פחד מאכזבה |
| 3 | למה לא הכי יקרה | הורדת התנגדות מחיר |
| 4 | הסבר סוגי גוף | בחירה נכונה — ביטול אנקסייטי |
| 5 | חוויית משחק וטיפול | ערך רגשי — הצדקת הרכישה |
| 6 | לקוחות שרכשו מספרים | הוכחה חברתית |
| 7 | שער קטגוריות ריבורן | מעבר למוצר |
| 8 | FAQ | הורדת חסם אחרון |
| 9 | CTA סופי | פעולה |

**הערה:**
FAQ pending — לא נעול עד אחרי first page draft.
שאלות ייבחרו רק אחרי שרואים מה הסקשנים עונים בפועל — FAQ = שכבת השלמה, לא כפילות.

---

## 3. Section Implementation Strategy

---

### סקשן 1 — HERO

- **שימוש בסקשן קיים:** כן — Dawn `image-banner` / `hero` section קיים. להתאים לריבורן.
- **התאמות נדרשות:** תמונה, כותרת, תת-כותרת, CTA label.
- **סקשן חדש:** לא.
- **Assets חסרים:**
  - [ ] תמונת Hero — כמה בובות ריבורן על ספה (AI generated / אמיתית — ממתין להחלטת אייל)
- **חסם לפני build:** תמונת Hero חסרה + החלטת אייל: AI מותר להציג כתמונת מוצר?

---

### סקשן 2 — פתיחת אמון

- **שימוש בסקשן קיים:** כן — בדוק קיום `bm-store-features.liquid` או trust card בסקשני ביגוד. להתאים.
- **התאמות נדרשות:** Trust Promise visual card + Trust Strip icons.
- **סקשן חדש:** לא.
- **Assets חסרים:**
  - [ ] Trust badge visual design (צורה, גודל, איקון — לא מוגדר)
  - [ ] מספרים אמיתיים לאייקונים (כמה ביקורות? זמן משלוח בפועל?)
  - [ ] החלטת אייל: מדיניות החזרה סופית (14 יום? 30 יום? מי משלם משלוח?)
- **חסם לפני build:** מספרי Trust לא מאומתים. מדיניות החזרה לא נעולה.

---

### סקשן 3 — למה לא הכי יקרה

- **שימוש בסקשן קיים:** כן — סקשן טקסט + תמונה (image-with-text / Dawn `image-with-text`). להתאים.
- **התאמות נדרשות:** טקסט Positioning, תמונת ליווי.
- **סקשן חדש:** לא.
- **Assets חסרים:**
  - [ ] תמונה לסקשן — lifestyle / בובה + ילדה / אינפוגרפיקה קטנה
- **חסם לפני build:** אין. טקסט Positioning מאושר לתכנון. תמונה נדרשת אך לא חוסמת spec.

---

### סקשן 4 — הסבר סוגי גוף

- **שימוש בסקשן קיים:** כן — `bm-store-features.liquid` או columns/feature row. להתאים לשני סוגי גוף.
- **התאמות נדרשות:** 2 כרטיסים: Fabric type / Silicone type — תיאור קצר + תמונה לכל סוג.
- **סקשן חדש:** לא.
- **Assets חסרים:**
  - [ ] תמונה לגוף בד
  - [ ] תמונה לגוף סיליקון
  - [ ] החלטת אייל: שורות קצרות (2) לכל סוג, או טבלת השוואה?
- **חסם לפני build:** תמונות חסרות. החלטת פורמט (שורות / טבלה) חסרה.

---

### סקשן 5 — חוויית משחק וטיפול

- **שימוש בסקשן קיים:** כן — image-with-text / rich-text. להתאים.
- **התאמות נדרשות:** טקסט + תמונת lifestyle.
- **סקשן חדש:** לא.
- **Assets חסרים:**
  - [ ] תמונת lifestyle — בובה בסביבה ביתית / ילדה משחקת
- **חסם לפני build:** אין. תמונה נדרשת אך לא חוסמת spec.

---

### סקשן 6 — לקוחות שרכשו מספרים

- **שימוש בסקשן קיים:** לא — אין סקשן וידאו מתאים קיים.
- **סקשן חדש:** כן — **Reborn Video Review Cards**.
  - מאושר כרעיון תכנוני בלבד.
  - **לא לכתוב קוד לפני spec מאושר מאייל.**
- **Spec requirements (ידוע):**
  - כרטיסים configurable
  - וידאו 9:16 אנכי + טקסט ביקורת + שם/תווית + כפתור play
  - Mobile-first, lazy load, לא autoplay כבד
- **Assets חסרים:**
  - [ ] בחירת 4 ביקורות AliExpress מתוך 40 (Phase 2 בדוח)
  - [ ] 4 קטעי וידאו קצרים (CapCut) — 5–10 שניות כל אחד
  - [ ] תמונות/קטעי המחשה עם בובות
- **חסם לפני build:** spec לא מאושר. אסור לכתוב קוד. videos לא קיימים.

---

### סקשן 7 — שער קטגוריות ריבורן

- **שימוש בסקשן קיים:** כן — product grid / collection list / `featured-collection`. להתאים.
- **התאמות נדרשות:** גריד עם 6 בובות — תמונה + שם עברי + מחיר + כפתור.
- **סקשן חדש:** לא.
- **Assets חסרים:**
  - [ ] שמות עבריים לכל 6 בובות (לא נקבעו)
  - [ ] לינקים לדפי מוצר של 6 בובות
  - [ ] תמונות מוצר לכל בובה (לא סטוק — אמיתיות)
- **חסם לפני build:** שמות עבריים לא נעולים. תמונות מוצר תלויות ב-PHASE 5.

---

### סקשן 8 — FAQ

- **שימוש בסקשן קיים:** כן — `bm-store-accordion.liquid` / Dawn accordion. להתאים.
- **התאמות נדרשות:** שאלות ותשובות + שורת מייל מתחת לאקורדיון.
- **סקשן חדש:** לא.
- **Assets חסרים:**
  - [ ] תשובות סופיות לשאלות (חסומות עד first page draft + PHASE 5)
  - [ ] החלטת אייל: מדיניות החזרה סופית (נדרש לשאלה 4)
- **חסם לפני build:** ראה סקשן 6 — FAQ Handling.

---

### סקשן 9 — CTA סופי

- **שימוש בסקשן קיים:** כן — **לשימוש בסקשן יצירת קשר קיים (כמו בביגוד)**. להתאים לריבורן.
- **התאמות נדרשות:** כותרת CTA, כפתור ראשי, מייל.
- **סקשן חדש:** לא.
- **Assets חסרים:**
  - [ ] החלטת אייל: CTA מקשר ל-collection page, או חזרה לגריד הבובות בדף?
- **חסם לפני build:** החלטת יעד ה-CTA חסרה.

---

## 4. Visual Build Rules

- **Mobile first** — כל סקשן מתוכנן למובייל תחילה
- **RTL** — עברית, כיוון ימין לשמאל
- **BabyMania brand palette only** — לא להוסיף צבעים שאינם בפלטה המאושרת
- **Visual rhythm:** תמונה → טקסט → תמונה → טקסט — אסור שני סקשני טקסט רצופים
- **No heavy autoplay** — וידאו: הפעלה בלחיצה בלבד
- **No text-heavy sections** — כל סקשן חייב asset ויזואלי לפחות אחד
- **No new colors** — חסומים: `#2C2C2C`, `#FAFAF8`, `#4A7C59`, `#F5EDE3`
- **No new sections without Eyal approval** — חריג יחיד: Reborn Video Review Cards (spec בלבד)

---

## 5. Assets Needed Before Real Build

### תמונות
- [ ] Hero AI image — כמה בובות ריבורן על ספה (ממתין להחלטת אייל)
- [ ] תמונות lifestyle — בובה בסביבה ביתית / ילדה משחקת
- [ ] תמונות מוצר לכל 6 בובות (אמיתיות — לא סטוק)
- [ ] תמונה לגוף בד (סקשן 4)
- [ ] תמונה לגוף סיליקון (סקשן 4)

### וידאו וביקורות
- [ ] 4 ביקורות נבחרות מ-40 ביקורות AliExpress (Phase 2 בדוח)
- [ ] 4 קטעי וידאו קצרים (CapCut) — 5–10 שניות כל אחד
- [ ] תמונות/קטעי המחשה עם בובות לסקשן 6

### קישורים ומוצרים
- [ ] לינקים לדפי מוצר של כל 6 בובות
- [ ] שמות עבריים לכל 6 בובות
- [ ] קישור לקולקציית ריבורן / catalog

### החלטות תלויות אייל
- [ ] מדיניות החזרות סופית (14 יום? 30 יום? מי משלם?)
- [ ] מספרים אמיתיים ל-Trust Strip (ביקורות, זמן משלוח)
- [ ] החלטת AI image: מותר להציג כתמונת מוצר?
- [ ] פורמט סקשן 4: שורות קצרות או טבלת השוואה?
- [ ] יעד CTA הסופי: collection page או גריד בדף?
- [ ] URL לדף הנחיתה (עברית אם בטוח טכנית)

### מייל (מאושר)
- babymania.israel@gmail.com

---

## 6. FAQ Handling

FAQ is intentionally not locked at this stage.

**Reason:**
FAQ must not duplicate content already answered by earlier sections.
Only after a first page draft exists — when we can see what sections 1–7 actually say — can FAQ questions be selected.

**Selection criteria (after first draft):**
- What questions remain unanswered after reading sections 1–7?
- Not product-specific (product FAQ → individual product pages)
- Not already answered by Section 2 / 3 / 4 / 5
- Max 4 questions + contact line

**Contact line (approved):**
"לא מצאתם תשובה? כתבו לנו: babymania.israel@gmail.com"
— מופיע כשורת טקסט קטנה מתחת לאקורדיון, לא כשאלת FAQ.

**Status:** Placeholder — pending first page draft.

---

## 7. Next Build Task Recommendation

שלושה מסלולים אפשריים — לאישור אייל:

**A. Map existing sections for reuse**
סרוק את קבצי ה-theme הקיימים (sections/, snippets/) ומפה אילו סקשנים קיימים יכולים לשמש כל אחד מ-9 הסקשנים. פלט: טבלה — סקשן → קובץ קיים → רמת התאמה נדרשת.
→ עבודה: תיעוד בלבד. לא נוגעים ב-live.

**B. Prepare technical spec for Reborn Video Review Cards**
כתוב spec מוגמר לסקשן החדש היחיד המאושר: כרטיסי וידאו ביקורות. פלט: מסמך spec עם: HTML structure, data schema, JS behavior, Liquid variables, mobile/performance requirements.
→ עבודה: מסמך בלבד. לא קוד live.

**C. Prepare non-live page template draft**
בנה skeleton HTML/Liquid בקובץ לוקלי — לא ב-theme live — עם 9 הסקשנים כ-placeholders. מאפשר לראות visual rhythm לפני כל build.
→ עבודה: קובץ לוקלי בלבד. לא push, לא theme.

**המלצה:**
A → B → C בסדר הזה.
A מוכרח לפני כל build (למנוע בנייה מיותרת מאפס).
B מוכרח לפני קוד לסקשן 6.
C אפשרי במקביל ל-B.

---

*Build prep only — לא קופי סופי. אין לפרסם לפני אישור אייל + PHASE 5 + PHASE 6.*
*כפוף ל-REBORN-MASTER-PROMPT.md ו-BABYMANIA-MASTER-PROMPT.md בכל עת.*
