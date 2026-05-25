---
name: babymania-organic-article-production
description: מנחה ייצור מאמרים אורגניים ב-BabyMania — תכנון, כתיבה, תמונות, QA, פרסום. טריגרים: "מאמר חדש", "article", "blog", "organic write", "תכנון תוכן", "כתיבת בלוג", "QA מאמר", "פרסום מאמר".
allowed-tools: Read, Grep, Glob
---

# babymania-organic-article-production — זרימת ייצור מאמרים אורגניים

זרימת ייצור מאמר אורגני מקצה לקצה. **8 שלבים — אין דילוגים.**

---

## מתי להשתמש

- ייצור מאמר אורגני חדש (TOFU / AEO / BOFU)
- כתיבת מאמר בלוג חדש לאחר תכנון HUB
- הכנה לפרסום מאמר ב-Shopify Blog
- QA סופי למאמר לפני אישור Ayal
- פרסום מאמר אורגני שכבר עבר QA
- verify לאחר פרסום (HTTP 200 + content check)
- בקשת אינדוקס ידנית ב-GSC

## מתי לא להשתמש

- שינוי בתוכן מאמר קיים שלא דורש זרימת ייצור (תיקון טייפו → ערוך ישירות)
- תכנון HUB ברמה גבוהה (זה שייך ל-hub-planner)
- מחקר מילות מפתח גולמי (זה שייך ל-organic-keyword-research)
- שינויי SEO ברמת מוצר (זה שייך ל-seo-specialist)
- שינויים ב-navigation / homepage / theme

## פעולות אסורות

- ❌ פרסום ללא Ayal sign-off
- ❌ פרסום ללא 8/8 QA PASS
- ❌ דילוג על pipeline 04→10.5→10
- ❌ בקשת אינדוקס דרך GSC API (manual UI בלבד)
- ❌ שינוי `bridge/next-task.md` או `.env`
- ❌ כתיבה ב-Shopify Blog API לפני שלב 6
- ❌ יצירת מאמר ללא `target_product_handle` (חייב גשר למוצר)

---

## הזרימה — 8 שלבים

### שלב 1 — תכנון (Planning)

לפני כתיבת מילה אחת, מלא בלוק תכנון:

```yaml
planning:
  keyword_main:          # מילת המפתח הראשית (1)
  keyword_secondary:     # 2-4 מילות מפתח משניות
  target_product_handle: # handle של המוצר היעד (חובה — גשר מסחרי)
  business_value:        # מה המאמר עושה לעסק? (traffic / authority / conversion)
  seo_rationale:         # למה זה נושא מנצח? (demand + intent + gap)
```

**ולידציות:**
- `keyword_main` ≠ ריק וקיים בפועל (חיפוש אמיתי, לא נושא תיאורטי)
- `target_product_handle` קיים ב-Shopify
- `business_value` חייב להיות אחד מ: discovery / answer-engine / commercial
- `seo_rationale` ≥ 2 משפטים

**אם חסר אחד מהשדות — STOP. אל תתחיל לכתוב.**

---

### שלב 2 — כתיבה (Writing)

מבנה חובה לכל מאמר:

```
H1 (חובה — חייב להכיל keyword_main)
  ├── פתיח (hook + intent match) — 80-120 מילים
  ├── H2 #1 — sub-topic ראשי
  ├── H2 #2 — sub-topic משלים
  ├── H2 #3 — sub-topic מעמיק / השוואה
  ├── H2 — CTA section (גשר למוצר target_product_handle)
  └── H2 — FAQ (3-6 שאלות) + FAQPage JSON-LD schema
```

**דרישות תוכן:**
- H1 — keyword_main חייב להופיע (טבעי, לא stuffing)
- כל H2 — 150-300 מילים, מינימום keyword_secondary אחד מתאים
- CTA — לינק פנימי ל-`/products/{target_product_handle}` עם anchor טבעי
- FAQ — שאלות אמיתיות מהורים (לא הומצאו)
- FAQPage JSON-LD — תקין, mapping של כל שאלה/תשובה
- Alt text placeholders — `[IMG_ALT_{n}: תיאור בעברית]` לכל תמונה צפויה
- Internal links — מינימום 2 (אחד למוצר, אחד למאמר אחר באותו HUB אם קיים)

**טון:**
- מומחה הורות — לא קופי-רייטר
- עברית טבעית — לא תרגום-מכונה
- בלי "במאמר זה נדבר על..." / "לסיכום"

---

### שלב 3 — תמונות (Images)

לכל תמונה במאמר, הגדר 3 שדות:

```yaml
image_n:
  prompt:      # אנגלית — לג'נרטור (Gemini / Midjourney / FLUX)
  alt_text:    # עברית — ל-HTML alt + SEO
  style_notes: # סגנון סקנדינבי — חובה
```

**Style notes — סקנדינבי קבוע:**
- צבעוניות: tones חמים-ניטרליים (beige, cream, dusty pink, sage green, off-white)
- תאורה: רכה, יום, חלון
- composition: נקייה, מינימליסטית, הרבה white space
- בלי: רעש ויזואלי, צבעים סטוריים, רקעים עמוסים, פילטרים אגרסיביים
- mood: שקט, חם, אותנטי

**Prompt structure (אנגלית):**
`{subject} + {action/composition} + {scandinavian style: soft natural light, muted warm tones, minimal, airy} + {camera: 50mm, shallow DoF} + {avoid: text, watermark, harsh shadows}`

**Alt text (עברית):**
- תיאורי, לא keyword-stuffed
- ≤ 125 תווים
- מכיל context (גיל תינוק / סצנה / רגש) — לא רק "תינוק לבן"

---

### שלב 4 — QA (8 תנאים — חייב 8/8 PASS)

| # | תנאי | קריטריון | PASS = |
|---|------|----------|--------|
| 1 | Keyword usage | keyword_main ב-H1 + פתיח + מינימום H2 אחד | YES |
| 2 | Internal link | מינימום 1 לינק למוצר target + 1 לינק רלוונטי נוסף | YES |
| 3 | Schema | FAQPage JSON-LD תקין, valid JSON, mapping מלא | YES |
| 4 | Alt text | כל תמונה עם alt בעברית, ≤125 תווים, לא ריק | YES |
| 5 | כתיב | אין שגיאות כתיב, ניקוד תקין במקומות נכונים בלבד | YES |
| 6 | עברית טבעית | זרימה אנושית, לא תרגום מכונה, לא ביטויים מלאכותיים | YES |
| 7 | מילים תקינות | אין מילים פיקטיביות / שגויות / שמות לא-קיימים | YES |
| 8 | Word count | TOFU: 800-1500, AEO: 600-1200, BOFU: 500-900 | YES |

**אם אפילו תנאי אחד = NO → STOP. תקן ובדוק שוב. אסור לעבור לשלב 5.**

---

### שלב 5 — אישור (Ayal Sign-Off)

**חובה לפני פרסום.**

הצג ל-Ayal:
- כותרת + slug + meta description
- 8/8 QA matrix מלא
- תצוגה מקדימה של תמונות + alt text
- internal links list
- FAQPage JSON-LD

**ממתין ל:** APPROVED מפורש מ-Ayal.

**אסור:**
- "אני מניח שזה בסדר" → לא
- "Ayal לא ענה — אני ממשיך" → לא
- שינויים אחרי אישור ללא re-approval

---

### שלב 6 — פרסום (Pipeline 04→10.5→10→publish)

הסדר קבוע — אסור לדלג:

```
04  → תכנון פרסום (slug, blog_id, tags, publish_date, meta)
10.5 → הכנת payload Shopify (HTML + schema + images uploaded)
10   → publish call ל-Shopify Blog API
```

**שלבים:**
1. `04` — וודא slug ייחודי, tags נכונים (taxonomy אורגני), meta_title + meta_description.
2. `10.5` — העלה תמונות, החלף alt placeholders, בנה final HTML + JSON-LD.
3. `10` — קריאת POST ל-Shopify Blog Articles API. שמור response.id.
4. בדוק status בתשובה = 201 / published.

**אם שלב נכשל — אל תמשיך לבא. תקן ופתח מחדש.**

---

### שלב 7 — Verify (HTTP 200 + Content Check)

לאחר publish:

1. **HTTP check:**
   - GET `https://a2756c-c0.myshopify.com/blogs/{blog_handle}/{article_slug}`
   - חייב להחזיר `200 OK`
   - אם 404/302/500 → FAIL → חקור (slug לא נשמר? blog לא published?)

2. **Content check:**
   - H1 קיים ונכון
   - keyword_main מופיע
   - FAQPage JSON-LD נטען ב-HTML הסופי
   - internal link ל-target_product_handle עובד (לא 404)
   - תמונות נטענות (HTTP 200 לכל src)

**שמור snapshot של verify ב-`output/organic/verify-{article_slug}.json`.**

---

### שלב 8 — GSC (Manual Request Indexing)

**חוק קריטי: דרך UI בלבד.**

- כניסה ל-Google Search Console (manual)
- URL Inspection → הדבק URL מלא של המאמר
- לחץ "Request Indexing"
- חכה לאישור "Indexing requested"

**אסור:**
- ❌ GSC API לבקשת אינדוקס (לא נתמך + הפרת ToS)
- ❌ scripts אוטומטיים
- ❌ submission דרך sitemap בלבד (חלש מדי לפריט בודד)

**רישום:**
- תאריך בקשת אינדוקס
- screenshot של GSC confirmation
- שמור ב-`output/organic/gsc-requests.md`

---

## טעויות נפוצות

### 1. דילוג על שלב 1 (תכנון)
"יש לי רעיון למאמר, אני מתחיל לכתוב" → STOP.
ללא keyword_main + target_product_handle = מאמר ללא ערך מסחרי.

### 2. FAQPage JSON-LD שבור
JSON לא valid, שאלה ללא תשובה, mainEntity חסר.
**תקן:** הרץ דרך Schema.org Validator לפני שלב 5.

### 3. Alt text זהה לכל התמונות
"תינוק" / "בגד תינוק" — לא עוזר ל-SEO, לא נגיש.
**תקן:** alt חייב להיות ייחודי + תיאורי.

### 4. internal link לתוכן שלא קיים
לינק ל-handle שטרם פורסם / נמחק → 404 → SEO damage.
**תקן:** בדוק כל לינק ב-verify (שלב 7).

### 5. פרסום ללא Ayal sign-off
"זה דחוף, אני מפרסם" → ביטול publish + restart.

### 6. בקשת אינדוקס דרך API
חסום על ידי Google + הפרת ToS. UI manual בלבד.

### 7. תרגום מכונה מ-AI ללא עריכה
"כדאי לזכור לנו ש..." / "במאמר זה אנו נחקור" → קופי גנרי.
**תקן:** עורך אנושי מעביר על כל מאמר.

### 8. word count שגוי לסוג המאמר
TOFU 400 מילים = רדוד. BOFU 2000 מילים = שחיקת intent.
**תקן:** התאם לסוג (TOFU/AEO/BOFU) לפי טבלה בשלב 4.

---

## קבצים רלוונטיים (read-only context)

- `docs/organic/מצב-הפרויקט-האורגני.md` — state doc (חובה לקרוא לפני התחלה)
- `output/organic/` — תיקיית פלט (planning, verify, gsc-requests)
- `agents/organic-blog-writer.md` — סוכן הכתיבה
- `agents/organic-keyword-research.md` — מחקר keywords
- `agents/hub-planner.md` — תכנון HUB

---

## פלט סופי לכל מאמר (לאחר 8/8)

```yaml
article_id: {shopify_article_id}
slug: {article_slug}
url: https://a2756c-c0.myshopify.com/blogs/{blog}/{slug}
keyword_main: {keyword}
target_product_handle: {handle}
qa_score: 8/8
ayal_signoff: APPROVED ({timestamp})
published_at: {iso_timestamp}
verify_http: 200
verify_content: PASS
gsc_request_status: REQUESTED ({date})
gsc_request_method: manual_ui
```

---

## חוק זהב

**8 שלבים. אין דילוגים. אין קיצורי דרך.**
מאמר אורגני שמדלג על שלב = liability ארוך טווח (SEO damage, indexing failure, ToS risk).
