---
name: babymania-state-loader
description: טוען מצב מינימלי של מערכת BabyMania לפי סוג משימה. הפעל תמיד בפתיחת סשן חדש, כאשר המשתמש אומר "מה המצב", "תבדוק מצב", "state", "מצב פרויקט", "מה קרה", "היכן אנחנו", "תסכם", "summary", "session פתוח", או לפני כל תכנון משימה ללא הקשר. לא לטעון את כל הפרויקט — רק קבצי עוגן לפי סוג המשימה.
allowed-tools: Read, Grep, Glob, Bash
---

# babymania-state-loader — טוען מצב מינימלי

## מתי להשתמש

- בפתיחת כל סשן BabyMania (חובה לפני תכנון)
- כשהמשתמש מבקש "מה המצב" / "state" / "מצב פרויקט"
- לפני יצירת plan חדש, לפני הרצת script, לפני כל שינוי
- כשאין הקשר ברור מהשיחה

## מתי לא להשתמש

- כשכבר טענת מצב באותו סשן (אל תקרא שוב)
- כשהמשתמש ציין `MODE:` מפורש עם קבצים ספציפיים לקרוא
- כשהמשימה קצרה ומיידית ולא צריכה הקשר מוקדם

## קבצי מקור — חובה בכל סוג משימה

- `BABYMANIA-MASTER-PROMPT.md` — snapshot מצב הפרויקט (חובה תמיד)

## קבצי מקור — לפי סוג משימה (קרא רק הרלוונטיים)

| סוג משימה | קבצים לקרוא (בנוסף ל-MASTER) |
|-----------|------------------------------|
| אורגני — HUBs, בלוגים, SEO | `docs/organic/מצב-הפרויקט-האורגני.md` + `docs/organic/organic-journal.md` |
| מוצרי ביגוד | `docs/product/clothing-journal.md` |
| מוצרי נעליים | `docs/product/shoes-journal.md` |
| אוטומציה / bridge | `bridge/status.md` + `bridge/conductor-state.md` |
| ניהול / הנחיות | `docs/management/source-of-truth.md` |
| כתיבה ל-Shopify | `docs/management/approval-policy.md` |

**כלל:** קרא לכל היותר 3 קבצים (מעבר ל-MASTER). אם אינך בטוח בסוג — שאל את המשתמש.

## קבצים שאסור לקרוא

- `output/` — אסור אלא אם המשתמש ביקש מפורשות
- `output/stage-outputs/` — גדול מדי, לא נדרש לסקירת מצב
- `theme-live/` — אסור בלי צורך ספציפי
- `shared/product-context/` — אל תסרוק (294 קבצים)
- סקריפטים גדולים של כתיבה לשופיפיי — אל תקרא בלי בקשה

## פורמט פלט חובה

```
SYSTEM STATE:    [תיאור קצר — מה עובד, מה תקוע]
BRANCH:          [שם branch — בדרך כלל main]
CONDUCTOR STATE: [idle / running / blocked / done / unknown]
BRIDGE STATUS:   [idle / running / waiting_response / unknown]
DOMAIN:          [organic / product-clothing / product-shoes / automation / shopify-live]
LAST MILESTONE:  [milestone אחרון לפי journal]
OPEN BLOCKERS:   [blockers פתוחים אם יש, אחרת NONE]
READY TO PLAN:   YES / NO
REASON:          [אם NO — למה]
```

## חוקי BabyMania

- GitHub = מקור האמת. אם יש divergence בין local לבין GitHub — GitHub מנצח.
- אל תקרא יותר מ-4 קבצים לסקירת מצב רגילה.
- ריפו ראשי: `eyalcohen555/baby-mania-agent`. `baby-mania-shoes` = reference בלבד.
- אין "בערך מוכן". יש READY TO PLAN: YES או NO.

## טעויות נפוצות למניעה

- לקרוא את כל `output/` כ"הכנה" — מיותר ואיטי.
- לדווח מצב בלי לקרוא `BABYMANIA-MASTER-PROMPT.md` — אסור.
- לטעון מצב פעמיים באותו סשן — מבזבז context.
- לדווח `READY TO PLAN: YES` בלי לבדוק `bridge/conductor-state.md` — עלול לגרום לריצה כפולה.
- לדווח על status של `easy-sleep` / `tempio` כ"מוכנים" — הם T3 נפרד.
