---
name: babymania-cvr-checklist
description: בדיקת CVR לפני פרסום כל שינוי ב-BabyMania. הפעל לפני פרסום sections, templates, product pages, homepage, navigation, landing pages, עדכוני sticky bar, trust badges, CTA, ניווט. טריגרים: "לפרסם", "להעלות", "publish", "deploy", "go live", "push to shopify", "שינוי ב-homepage", "שינוי ב-template", "שינוי ב-section", "כתיבה חיה", "T2 write", "T3 write", כל שינוי שמשפיע על עמוד מוצר, דף ראשי, ניווט. מחזיר CVR_PASS או CVR_FAIL עם בעיות חוסמות ספציפיות.
allowed-tools: Read, Grep, Glob
---

# babymania-cvr-checklist — בדיקת המרה לפני פרסום

## מתי להשתמש

- לפני כל כתיבה חיה לשופיפיי שמשפיעה על UI
- לפני פרסום section חדש / שינוי קיים
- לפני שינוי ב-navigation, homepage, product page, landing page
- לפני הפעלת T2 / T3 write

## מתי לא להשתמש

- שינויים שלא נוגעים ב-UI (metafields טהורים, SEO tags ב-backend)
- שינויי גיבוי / rollback — לא נדרש CVR check לפני restore

## 8 בדיקות CVR חובה

### בדיקה 1 — מסר ברור מעל הקיפול (Above the Fold)
- יש כותרת H1 ברורה עם תועלת, לא רק שם מוצר?
- יש תמונה מוצר ברורה בטעינה ראשונה?
- אין תוכן גדול שדוחף את המסר הראשי למטה?
- **FAIL אם:** הכותרת גנרית / המוצר לא ברור ב-mobile בלי לגלול.

### בדיקה 2 — CTA ברור
- יש כפתור "הוסף לסל" / "לקנייה" ברור?
- הצבע מנוגד לרקע (לא אפור על לבן)?
- הטקסט פעיל ("הוסף לסל" ולא "מוצר")?
- Sticky add-to-cart פעיל ב-mobile (initStickyObserver קיים ב-HTML)?
- **FAIL אם:** CTA נחבא / לא בולט / sticky לא עובד ב-mobile.

### בדיקה 3 — אמון וביטחון (Trust Signals)
- יש ביקורות / דירוג?
- יש אחריות / החזר כספי / משלוח חינם?
- Trust badges גלויים לפני ATC?
- **FAIL אם:** אין שום trust signal לפני כפתור הקנייה.

### בדיקה 4 — מובייל
- גודל טקסט קריא (minimum 16px)?
- כפתורים לחיצים (minimum 44px)?
- אין overflow אופקי?
- Sticky bar לא מסתיר תוכן חיוני?
- **FAIL אם:** שינוי שובר layout ב-mobile.

### בדיקה 5 — עברית טבעית
- אין תרגום מילולי מאנגלית?
- RTL תקין — `dir="rtl"` מוגדר?
- אין superlatives לא מבוססים ("הטוב בעולם")?
- **FAIL אם:** קופי נשמע כמו תרגום מכונה.

### בדיקה 6 — ניווט לא מבלבל
- אין קישורים שבורים?
- ניווט ראשי לא השתנה בלי אישור?
- **FAIL אם:** ניווט ראשי השתנה ללא אישור / קישורים שבורים.

### בדיקה 7 — אין קופי גנרי
- אין "מוצר איכותי לתינוקות" ללא פרטים?
- יש תועלות ספציפיות (לא features בלבד)?
- **FAIL אם:** קופי יכול להתאים לכל חנות תינוקות בעולם.

### בדיקה 8 — אין שינוי שפוגע בהמרה
- הוסרה trust signal קיימת?
- CTA הוזז למטה?
- נוסף תוכן ארוך לפני ATC?
- **FAIL אם:** שינוי הוסיף friction לדרך לקנייה.

## פורמט פלט חובה

```
CVR CHECK: [תיאור השינוי הנבדק]
---
בדיקה 1 — above fold:    PASS / FAIL — [פרטים אם FAIL]
בדיקה 2 — CTA:           PASS / FAIL — [פרטים אם FAIL]
בדיקה 3 — trust signals: PASS / FAIL — [פרטים אם FAIL]
בדיקה 4 — mobile:        PASS / FAIL — [פרטים אם FAIL]
בדיקה 5 — עברית:         PASS / FAIL — [פרטים אם FAIL]
בדיקה 6 — navigation:    PASS / FAIL — [פרטים אם FAIL]
בדיקה 7 — generic copy:  PASS / FAIL — [פרטים אם FAIL]
בדיקה 8 — no regression: PASS / FAIL — [פרטים אם FAIL]
---
BLOCKING_ISSUES: [רשימה, אחרת NONE]
VERDICT: CVR_PASS / CVR_FAIL
```

## מה לעשות כאשר CVR_FAIL

- אל תפרסם עד שכל blocking issue נפתר
- עבור כל בדיקה שנכשלה — הגדר תיקון ספציפי
- הרץ CVR check שוב אחרי תיקון
- אם אי-ודאות — שאל אייל לפני פרסום

## קבצי מקור שמותר לקרוא

- section file רלוונטי ב-`sections/*.liquid`
- template JSON רלוונטי ב-`templates/*.json`
- `theme_assets/sections/bm-sticky-bar.liquid` — לבדיקת sticky bar

## פעולות אסורות

- לאשר CVR_PASS בלי לבדוק mobile (בדיקה 4)
- לאשר CVR_PASS בלי לקרוא את הטקסט בעברית (בדיקה 5)
- לדלג על הchecklist "כי השינוי קטן"
- לפרסם אחרי CVR_FAIL בלי תיקון

## חוקי BabyMania

- אין "בערך טוב" — יש CVR_PASS או CVR_FAIL.
- לא לגעת ב-navigation ראשי בלי אישור אייל (T3).
- EasySleep / Tempio — T3 נפרד, לא נבדק כאן.
- sticky bar — חייב לעבוד ב-mobile (initStickyObserver קיים בHTML אחרי תיקון E1c).

## טעויות נפוצות למניעה

- לבדוק CVR רק על desktop ולשכוח mobile — הקהל הוא בעיקר אמהות במובייל.
- לאשר "trust signals OK" בלי לבדוק שהן גלויות לפני ATC.
- לא לבדוק RTL כשמוסיפים section חדש — dir="rtl" חובה.
- לשכוח שהstickybar תוקן ב-E1c — לוודא initStickyObserver קיים.
