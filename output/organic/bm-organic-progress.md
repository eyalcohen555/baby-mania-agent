# bm-organic Template Track — מצב ואופן עבודה
**נוצר:** 2026-06-06
**מסלול:** נפרד מ-43-article batch pipeline
**עדכון אחרון:** 2026-06-07
**סטטוס:** LIVE QA PASS + GSC submitted for 3 renewed articles

---

## 1. מהו bm-organic

`bm-organic` הוא מסלול Shopify OS2.0 למאמרים אורגניים שמטרתם לא רק להביא תנועה מגוגל, אלא להמיר למוצר.

כל מאמר במסלול מציג 7 sections בסדר קבוע:

```text
hero → trust-strip → quick-answer → article-body → product-card → cta-banner → faq
```

הלקח המרכזי: אין להשתמש ב-template JSON אחד משותף לכמה מאמרים, כי שינוי בתוכן ה-section דורס את כל המאמרים שמצביעים לאותו template.

הפתרון שבוצע: template suffix ייחודי לכל מאמר.

---

## 2. Theme IDs

| Role | ID | שם | אזהרה |
|------|----|----|-------|
| TEST (עבודה) | `187183563065` | Working/001 | עבודה ובדיקות |
| LIVE (ייצור) | `183668179257` | ORGINAL Dawn new | לגעת רק עם אישור מפורש |

BLOG_ID: `109164036409`

---

## 3. Template JSON Files

| קובץ | טסט | לייב | hero | מוצר | מחיר | sticky | FAQ |
|------|-----|------|------|------|------|--------|-----|
| `article.bm-organic-water.json` | PASS | PASS | PASS | PASS | ₪95 PASS | ₪95 PASS | PASS |
| `article.bm-organic-sneaker.json` | PASS | PASS | PASS | PASS | ₪111 PASS | ₪111 PASS | PASS |
| `article.bm-organic-pishtan.json` | PASS | PASS | PASS | PASS | ₪151 PASS | ₪151 PASS | PASS |

---

## 4. מאמרים חיים

| article_id | suffix לפני | suffix עכשיו | handle | body len |
|------------|-------------|--------------|--------|----------|
| `689095672121` | `bm-organic` | `bm-organic-water` | `naalei-mayim-letinok-meize-gil` | 4,004 |
| `682290053433` | `bm-organic` | `bm-organic-sneaker` | `naal-tsaad-rishon-ma-kol-horeh-tzarich-ladaat` | 4,774 |
| `686728216889` | `bm-organic` | `bm-organic-pishtan` | `khalifat-pishtan-letinok-hayitronot-eikh-livkhor-umatay-lilbosh` | 4,729 |

Live URLs:

```text
https://babymania-il.com/blogs/news/naalei-mayim-letinok-meize-gil
https://babymania-il.com/blogs/news/naal-tsaad-rishon-ma-kol-horeh-tzarich-ladaat
https://babymania-il.com/blogs/news/khalifat-pishtan-letinok-hayitronot-eikh-livkhor-umatay-lilbosh
```

---

## 5. QA Summary

| בדיקה | water | sneaker | pishtan |
|-------|-------|---------|---------|
| suffix_correct | PASS | PASS | PASS |
| tpl_on_live | PASS | PASS | PASS |
| hero_matches | PASS | PASS | PASS |
| product_matches | PASS | PASS | PASS |
| price_correct | PASS | PASS | PASS |
| sticky_cta_ok | PASS | PASS | PASS |
| faq_present | PASS | PASS | PASS |
| no_placeholder | PASS | PASS | PASS |
| body_no_jsonld | PASS | PASS | PASS |
| body_no_faq_sec | PASS | PASS | PASS |
| body_no_cta_div | PASS | PASS | PASS |
| sections_live (7/7) | PASS | PASS | PASS |
| no_old_suffix | PASS | PASS | PASS |
| סה"כ | 13/13 | 13/13 | 13/13 |

OVERALL QA: PASS

---

## 6. Risk Closure

| בדיקה | תוצאה |
|-------|--------|
| `article.bm-organic.json` קיים בלייב | EXISTS, ללא שימוש |
| מאמרים עם suffix ישן `bm-organic` | 0 |
| Section files בלייב | ALL 7 PRESENT |
| סיכון cross-contamination | NONE |

---

## 7. GSC Submission

כל 3 המאמרים הוגשו ידנית ל-GSC בתאריך 2026-06-07.

| # | handle | סטטוס לפני | פעולה |
|---|--------|------------|--------|
| 1 | `naal-tsaad-rishon-ma-kol-horeh-tzarich-ladaat` | ב-Google | הוגש לסריקה מחודשת |
| 2 | `khalifat-pishtan-letinok-hayitronot-eikh-livkhor-umatay-lilbosh` | לא ב-Google עדיין | הוגש לאינדקס ראשון |
| 3 | `naalei-mayim-letinok-meize-gil` | ב-Google | הוגש לסריקה מחודשת |

כל ה-3 קיבלו אישור GSC: `Indexing request received`.

Follow-up: לבדוק בעוד 3-7 ימים אם `khalifat-pishtan` נכנס לאינדקס.

Reference: `output/organic/bm-organic-gsc-submission-2026-06-07.md`

---

## 8. פריט פתוח קטן

במאמר `naalei-mayim-letinok-meize-gil` נשאר `intro-box` בגוף המאמר.

סטטוס: WARN בלבד, pre-existing, לא blocker.

כלל פעולה: לא לתקן עכשיו בלי backup, תוכנית ואישור, כי זה שינוי `body_html`.

---

## 9. Safety Checklist לפני שכפול למאמרים 4-6

```text
□ עובדים קודם ב-test theme
□ live theme רק עם אישור מפורש
□ backup body_html לפני כל שינוי
□ Hero מאושר ידנית מאייל בלבד
□ product קיים ב-Shopify + status active
□ מחיר נכון לפי variants בפועל
□ אין placeholders
□ כל 7 sections מוגדרים
□ template suffix ייחודי לכל מאמר
□ QA PASS לפני דיווח על השלמה
□ GSC ידני אחרי Live QA
```

---

## 10. השלב הבא

המסלול הראשון של 3 מאמרי bm-organic סגור תפעולית: live templates נפרדים, QA PASS, GSC submitted.

השלב הבא הוא audit ותכנון לפני ביצוע:

1. לבחור 5 מאמרים הבאים לפי פוטנציאל מכירה.
2. לבצע audit לשדות המטא של 3 משפחות מוצרים חזקות: בובת ריבורן, נעלי צעד ראשון, מנורת לילה / מנורת ארנב לילה.
3. לא לבצע כתיבה ל-Shopify לפני אישור.
