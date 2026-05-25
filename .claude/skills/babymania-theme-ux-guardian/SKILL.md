---
name: babymania-theme-ux-guardian
description: שומר על UX, המרה ואמון בכל שינוי ויזואלי ב-BabyMania. הפעל לפני כל שינוי הנוגע לדף הבית, navigation, hero section, CTA, trust badges, sticky bar, mobile layout, קומפוננטות ויזואליות, או כל שינוי שמשנה את מה שהמשתמש רואה. טריגרים: "homepage", "דף בית", "navigation", "תפריט", "hero", "CTA", "mobile", "trust badges", "UX", "CVR", "sticky", "section", "layout", "עיצוב", "תבנית", "ויזואלי", "index.json", "כפתור". כל שינוי ויזואלי עובר דרך סקיל זה.
allowed-tools: Read, Grep, Glob
---

# babymania-theme-ux-guardian — שומר UX ודף בית

## מתי להשתמש

- לפני כל שינוי ב-`templates/index.json` (דף הבית)
- לפני כל שינוי ב-navigation / תפריט ראשי
- לפני הוספת / שינוי section ויזואלי (hero, banner, trust badges, featured collection)
- לפני שינויי CTA — טקסט, צבע, מיקום
- לפני כל שינוי שמשפיע על mobile layout
- לפני שינוי ב-sticky add-to-cart

## מתי לא להשתמש

- שינויים ב-backend בלבד (metafields, SEO tags) — לא נוגע ב-UI
- תיקון JS פנימי שלא משנה מה שהמשתמש רואה
- audit read-only ללא שינוי

## עקרונות ה-UX Guardian

### 1. אין עיצוב לשם יופי
כל שינוי ויזואלי חייב לענות על: "זה מגדיל קנייה / אמון / בהירות?"
אם התשובה אינה ברורה — אל תשנה.

### 2. לא להעמיס על דף הבית
- דף הבית = מסנן, לא קטלוג
- מקסימום 8 מוצרים ב-featured collection (לא 25)
- אין sections ריקים / blank
- אין כפילויות (2 sections עם אותה כותרת)

### 3. מובייל קודם
- כל שינוי — בדוק ב-mobile ראשון (הקהל הוא בעיקר אמהות במובייל)
- sticky bar חייב לעבוד ב-mobile (בדוק `initStickyObserver` בHTML)
- כפתורים: מינימום 44px גובה
- טקסט: מינימום 16px

### 4. CTA — כלל 3 שניות
המבקר חייב לראות CTA ברור בתוך 3 שניות, ללא גלילה.
כל שינוי שמזיז CTA למטה = CVR regression.

### 5. אמון ומפלס ביטחון
- Trust badges גלויים לפני CTA
- משלוח חינם / אחריות / החזרות — גלויים above the fold
- אין הסרת trust signals קיימות

### 6. Navigation — כלל שמרנות
- אין שינוי בתפריט ראשי בלי אישור T3 מאייל
- אין פתיחת Mega Menu בלי אישור מפורש
- שינוי URL של קולקציה = בדוק קישורים קיימים

### 7. EasySleep / Tempio — חסום
**אסור לגעת ב-`product.easy-sleep.json` ו-`product.tempio.json` בלי אישור מפורש.**
לחיפוש: הוסף לכל שינוי תבנית — האם הוא נוגע ב-EasySleep / Tempio?

## פורמט פלט חובה

```
UX CHANGE:         [מה מתכוונים לשנות]
BUSINESS GOAL:     [איך זה משרת קנייה / אמון / בהירות]
MOBILE_FIRST:      CHECKED / NOT_CHECKED
ABOVE_FOLD:        AFFECTED / NOT AFFECTED — [פרטים]
CTA_IMPACT:        POSITIVE / NEGATIVE / NEUTRAL — [פרטים]
TRUST_IMPACT:      MAINTAINED / DEGRADED — [פרטים]
NAVIGATION:        UNCHANGED / CHANGED (T3 נדרש) — [פרטים]
HOMEPAGE_LOAD:     [כמה sections, כמה מוצרים ב-featured]
EASYSLEEP_TEMPIO:  NOT AFFECTED / AFFECTED — STOP
VERDICT:           UX_GUARDIAN_PASS / UX_GUARDIAN_FAIL
BLOCKING_ISSUES:   [רשימה, אחרת NONE]
```

## קבצי מקור שחובה לקרוא

- `BABYMANIA-MASTER-PROMPT.md` — Theme Assets, מבנה Templates

## קבצים שמותר לקרוא

- `templates/index.json` — מבנה דף הבית
- `sections/bm-sticky-bar.liquid` — sticky bar (בדיקת initStickyObserver)
- `sections/bm-trust-badges.liquid` — trust badges
- `theme_assets/sections/` — sections קיימות

## פעולות אסורות

- לשנות navigation ראשי בלי T3 ואישור אייל
- לפתוח Mega Menu בלי אישור מפורש
- לגעת ב-EasySleep / Tempio בלי אישור
- להוסיף sections ריקים / blank לדף הבית
- להעלות products_to_show מעל 8 ב-featured collection
- לשנות CTA בלי לבדוק CVR impact

## חוקי BabyMania רלוונטיים

- Theme ID: `183668179257` | Shop: `a2756c-c0.myshopify.com`
- כל שינוי theme = T2 לפחות. שינוי navigation = T3.
- sticky bar תוקן ב-Phase E1c (DOM timing fix) — לא לשבור את `initStickyObserver`.
- trust badges הוספו ב-Phase E1 — לא לסיר אותם.
- products_to_show הוכנסו ל-8 ב-E1 — לא להחזיר ל-25.

## טעויות נפוצות למניעה

- לשנות layout בגלל ש"זה נראה טוב" — בלי לבדוק CVR impact.
- לבדוק desktop בלבד ולשכוח mobile — הקהל הוא בעיקר mobile.
- לפתוח Mega Menu "כי זה נוח" — שינוי ארכיטקטוני שדורש T3.
- לשנות נתיב קולקציה בלי לבדוק קישורים קיימים — 404s.
- להסיר trust badges "כי הם לא יפים" — פוגע בהמרה.
