# Baby Clothing Writing Library

Purpose: provide non-generic phrasing for baby clothing product pages.
Writers must select and adapt sentences from this library instead of generating generic text.

---

## BENEFITS LIBRARY

> **⚠️ Anchors only — NOT final benefit output.**
> All entries below are layer 1–2 fragments (feature or child benefit).
> Before using any entry as a final benefit card, complete it to layer 3:
> add an explicit parent outcome — what changes in the parent's day.
>
> Example of required completion:
> Library entry: `"נוח לזחילה ולתנועה חופשית"` (layer 2 — child benefit)
> Final benefit card: `"נוח לזחילה ולתנועה חופשית — אתה לא עוצר אותו כל הזמן"` (layer 3 — parent outcome added)

Use short real-life advantages (as anchors for layer-3 completion):

- לבישה מהירה גם כשהתינוק עייף
- סט מוכן בלי לחפש אביזרים נוספים
- נוח לזחילה ולתנועה חופשית
- מתאים ליום בבית או לביקור קצר
- קל להלבשה גם לתינוק שמתפתל
- לבוש נוח לשגרה היומיומית
- מאפשר לתינוק לנוע בנוחות
- פריט נוח שמלבישים שוב ושוב
- פתרון לבוש פשוט ומהיר
- מתאים למשחק, שינה וטיול קצר
- נוח גם לזמן בטן
- לבוש רך לשעות ארוכות

---

## FABRIC STORY LIBRARY

Fabric section should be short and calm.

- בגד נעים ללבישה יומיומית.
- נוח לתינוק מהלבישה הראשונה.
- מתאים לשגרה בבית או ליציאה קצרה.
- פריט פשוט ונעים ליום יום.
- נוחות שמרגישים מיד כשמלבישים.
- לבוש רגוע שמתאים לשעות ארוכות.

---

## FABRIC STORY RULE

Fabric sections must always be written as a short narrative.

### Visual structure (as displayed on product page)

```
[כותרת רגשית — מבוססת יתרון]

| [פסקה 1 — תחושת הבד על התינוק. מה קורה כשהתינוק לא מגרד, לא מתעורר מחיכוך.]

[פסקה 2 — פרטי החומר + עמידות + מה זה נותן להורה]

[TAG PILL] | [TAG PILL] | [TAG PILL]
```

### Field mapping

| שדה | תוכן |
|-----|------|
| `fabric_title` | כותרת רגשית — לא שם הבד, אלא יתרון ("הבגד שגורם לתינוק להירגע – ולהורה לנשום") |
| `fabric_paragraph_1` | תחושת הבד על העור — מה קורה כשהבד לא מגרד, לא חוכך, לא מפריע |
| `fabric_paragraph_2` | פרטי הבד (אם ידועים) + עמידות + השקט שזה נותן להורה |
| `fabric_tags` | 3 גלולות קצרות: הרכב / סוג הבד / תחושה (כל גלולה: עד 4 מילים) |

### Rules

1. **Paragraph 1** — רגשי, מתאר את חוויית התינוק.
2. **Paragraph 2** — עובדתי+רגשי, מסביר את הבד ומסיים ביתרון להורה.
3. **Tags** — גלולות, לא bullet list. לפחות 2, עד 4.
4. **Never** output a bullet list for the story paragraphs.
5. **Fabric length target:** 60–90 words total.

### TAG COMPOSITION RULE

תגית הרכב בד (כגון "100% כותנה", "כותנה סרוגה") — **מותרת רק אם המידע קיים במוצר עצמו.**

| מצב | תגית מותרת |
|-----|------------|
| `fabric_type` = "כותנה סרוגה" | ✅ `כותנה סרוגה` |
| `fabric_type` = "100% cotton" | ✅ `100% כותנה` |
| אין `fabric_type` ואין רמז | ❌ אסור לכתוב הרכב — השתמש ב-benefit tag |

**benefit tags לשימוש כשאין מידע הרכב:**

`רך למגע` | `נעים ללבישה` | `נוחות יומיומית` | `גזרה מחבקת` | `קל להלבשה` | `נוח לתנועה`

### Example (from real product — LumiBear knitted cotton)

```
fabric_title: הבגד שגורם לתינוק להירגע – ולהורה לנשום
fabric_paragraph_1: בגד שנוח על העור עושה הבדל אמיתי. כשהתינוק לא מגרד, לא מתעורר בגלל חיכוך ולא מתנגד להלבשה, גם ההורה נושם לרווחה.
fabric_paragraph_2: הכותנה הסרוגה עוברת תהליך סינון שמסלק סיבים קצרים ולא אחידים. התוצאה היא בד חלק, עשיר ורך במיוחד שלא מתגרד עם הזמן. כשהתינוק נוח בבגד שלו, גם אתם נרגעים — ואפשר לחשוב על הדברים שחשובים באמת.
fabric_tags: 100% כותנה | כותנה סרוגה | רך במיוחד לעור תינוק
```

---

## FABRIC NAMING POLICY

If `fabric_type` exists in the product data — use the real material name.

Examples:
- כותנה סרוגה
- סריג כותנה
- כותנה אורגנית

If `fabric_type` does NOT exist — use the default fallback:

> **"בד סרוג"**

Never invent fabric materials.

Forbidden examples (unless they appear in product data):
- 100% cotton
- organic cotton
- temperature regulating

---

## ICON POLICY — BABY CLOTHING

Icons support emotional buying triggers.
Parents buy comfort and safety, not technical specs.

If material specs exist → icons may reference them.

If specs do NOT exist → use benefit icons:

- רך ונעים למגע
- נוח לתנועה
- קל להלבשה
- מתאים לשימוש יומי

Never invent technical claims.

---

## CARE INSTRUCTIONS STANDARD

All baby clothing products must include a washing instructions accordion.

### Section name (exact)

```
הוראות כביסה — לחצו לפתיחה
```

### Display rules

- Accordion collapsed by default
- Maximum 5 rows — no more, no less
- Icons must match standard ISO laundry symbols

### Standard 5 rows (default set)

| icon_type | card_title | card_text |
|-----------|------------|-----------|
| `wash_60` | כביסה עד 60° | בגד עמיד — נשמר כחדש אחרי כביסות חוזרות |
| `no_tumble_dry` | ייבוש טבעי מומלץ | שומר על הצורה המקורית ומאריך את חיי הבגד |
| `no_bleach` | שמירה על הצבע | הסיבים עמידים — ללא צורך בחומרי הלבנה |
| `iron` | גיהוץ עדין אם נחוץ | חום נמוך מספיק לשמירת הבד |
| `sun_dry` | ייבוש טבעי באוויר | שומר על הצורה והצבע לאורך זמן |

### Override rule

If `fabric_type` is **empty** (`fabric_known = false`) → replace `wash_60` with `hand_wash` only.
All other 4 rows remain standard.

---

## EMOTIONAL MOMENTS

Use real parenting situations.

- נוח גם להלבשה מהירה באמצע הלילה.
- כשצריך להלביש תינוק מהר — זה פשוט עובד.
- פתרון לבוש קל להורים עסוקים.
- מתאים לרגעים הקטנים של היום.
- לבוש פשוט שעושה את העבודה.

---

## CARE ADVANTAGE PHRASING

Never use warning language.
Convert instructions into advantages.

Instead of:
"לא להלבין"

Write:
"שומר על הסיבים גם בלי חומרי הלבנה"

Examples:

- כביסה עדינה שומרת על הרכות
- ייבוש טבעי שומר על הצבע
- טיפול פשוט שמתאים לשגרה
- קל לשמור עליו גם אחרי הרבה כביסות
- תחזוקה קלה לאורך זמן

---

## BENEFIT STRUCTURE RULE

Every benefit must follow this structure:

Feature → Practical advantage → Real-life result

Example:

Feature:
כובע וכפפות

Advantage:
סט מוכן

Result:
לא צריך לחפש אביזרים נוספים
