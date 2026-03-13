# זהות הצוות — צוות אורגני

> קובץ זה מגדיר את זהות צוות האורגני, תפקידיו, והסוכנים המרכיבים אותו.

---

## שם הצוות

**צוות אורגני**

---

## משימת הצוות (Mission)

שיפור הגילוי האורגני וסיווג SEO של מוצרי חנות BabyMania ב-Shopify.
הצוות מקבל מוצר עם context קיים ומייצר תגיות Shopify נקיות, מחקר מילות מפתח, אסטרטגיית תוכן באשכולות, ומאמרי בלוג SEO לפי playbook אורגני מלא.

**זרימת העבודה:** keyword intent → topic hubs → cluster logic → content prioritization → article creation

**שכבות תוכן (Content Layers):** המערכת מייצרת שלושה סוגי תוכן:

| שכבה | מטרה | article_type |
|------|------|-------------|
| **TOFU** — Discovery/SEO | גילוי אורגני, חינוך הורים | `tofu` |
| **AEO** — Answer Engine | תשובות ישירות ל-AI Overviews, PAA, Snippets | `aeo` |
| **BOFU** — Commercial Intent | השוואות, המלצות, קרוב לרכישה | `bofu` |

**Knowledge Base:** כל הסוכנים עוקבים אחרי שני קבצים:

| קובץ | תפקיד |
|------|--------|
| `BabyMania-AI-Agents-Docs/ORGANIC-CONTENT-KNOWLEDGE.md` | כללי כתיבה, SEO, המרה, אשכולות, **שכבות תוכן** |
| `BabyMania-AI-Agents-Docs/TOPIC-HUBS-KNOWLEDGE.md` | 7 ה-hubs המאושרים — מיפוי כל נושא ל-hub, pillar, ומוצרים |

---

## היקף פעולה (Scope)

| פרמטר | ערך |
|-------|-----|
| קטגוריה | **ביגוד בלבד** — Clothing Only |
| סטטוס מוצר | **Active בלבד** — לא טיוטות |
| שפת תגיות | **אנגלית** (lowercase, hyphen format) |
| חנות | `a2756c-c0.myshopify.com` |

---

## סוכני הצוות (Agents)

| # | שם הסוכן | סוג | תפקיד |
|---|---------|-----|--------|
| 01 | organic-tag-generator | Claude Code (AI) | יצירת 6–10 תגיות Shopify לגילוי אורגני |
| 02 | organic-keyword-research | Claude Code (AI) | מחקר מילות מפתח אורגניות מבוסס כוונת הורים |
| 03 | organic-blog-strategist | Claude Code (AI) | חשיבת אשכולות — pillar vs supporting, סיווג content_type, שיוך topic_hub, סיווג article_type (tofu/aeo/bofu) |
| 04 | organic-blog-writer | Claude Code (AI) | כתיבת מאמרי בלוג HTML — מסתגל למבנה לפי article_type: TOFU/AEO/BOFU |
| 05 | organic-search-demand-validator | Claude Code (AI) | הערכת ביקוש + search intent + hidden diamond + SERP signals + hub_strengthening_value |
| 06 | organic-content-prioritizer | Claude Code (AI) | מפת דרכים עריכתית — Money → Support → Authority, cluster_position, hub priority order |
| | | | |
| | **--- Internal Linking Sub-Team ---** | | |
| 07 | organic-content-mapper | Claude Code (AI) | מיפוי מבנה תוכן האתר — סיווג דפים, זיהוי אשכולות, גילוי דפים יתומים |
| 08 | organic-article-linker | Claude Code (AI) | הצעת קישורים פנימיים הקשריים בתוך מאמרים — anchor text, pillar links, cluster links |
| 09 | organic-product-linker | Claude Code (AI) | מציאת הזדמנויות טבעיות לקישור מאמרים לדפי מוצר |
| 10 | organic-link-qa | Claude Code (AI) | אימות מבנה הקישורים לפני פרסום — PASS / WARNING / FAIL |

> **הבדל מצוות דף מוצר כללי:** צוות אורגני לא משנה תוכן, templates, או body_html.
> הוא מעדכן **רק** את שדה `tags` של המוצר ב-Shopify, ומייצר מחקר SEO לשימוש עתידי.

---

## זרימת ה-Pipeline

```
fetch (Python) — שליפת מוצר (או שימוש ב-context קיים)
    ↓
01 organic-tag-generator      →  {pid}_organic_tags.json      ┐
02 organic-keyword-research   →  {pid}_keyword_research.json  ┘ parallel
    ↓
03 organic-blog-strategist    →  {pid}_blog_strategy.json       serial (תלוי ב-02)
    ↓
05 organic-search-demand-validator → {pid}_search_demand.json    serial (תלוי ב-02+03)
    ↓
organic-strategy-controller (Python) → {pid}_organic_strategy_decision.json
    ↓                                   (gate: should_create_blog_article?)
06 organic-content-prioritizer → {pid}_content_priority.json     תור ביצוע מדורג
    ↓
04 organic-blog-writer        →  {pid}_blog_article_{N}.html    רק אם should_create=true
    ↓
07 organic-content-mapper     →  internal_content_map.json       מיפוי מבנה תוכן האתר
    ↓
08 organic-article-linker     →  {pid}_article_link_suggestions.json  ┐ parallel
09 organic-product-linker     →  {pid}_product_link_suggestions.json  ┘
    ↓
10 organic-link-qa            →  {pid}_internal_link_validation.json  אימות PASS/WARNING/FAIL
    ↓
push (Python) — עדכון tags בלבד ב-Shopify API
    ↓
verify (Python) — אימות שהתגיות נשמרו
```

> **הערה:** סוכנים 01 ו-02 רצים במקביל. סוכן 03 רץ אחרי 02 (תלוי ב-keyword_research.json).
> **חשוב:** סוכן 04 (blog-writer) רץ **רק** אם ה-strategy-controller החליט `should_create_blog_article: true`.
> **חשוב — Internal Linking Sub-Team:**
> - סוכן 07 (content-mapper) רץ אחרי 04 — דורש את כל תוכן האתר למיפוי.
> - סוכנים 08 (article-linker) ו-09 (product-linker) רצים **במקביל** — דורשים את ה-HTML מ-04 + content_map מ-07.
> - סוכן 10 (link-qa) רץ **אחרון** — מאמת את כל הקישורים לפני פרסום.

---

## שכבות הניהול (Management Layers)

| שכבה | קובץ | תפקיד |
|------|------|--------|
| Technical Runner | `10-organic-lead/organic-orchestrator.py` | הרצת fetch/push/verify — שכבה טכנית |
| Strategic Controller | `10-organic-lead/organic-strategy-controller.py` | החלטת go/no-go — האם בכלל שווה לכתוב תוכן |
| Content Prioritizer | `06-organic-content-prioritizer` (Claude Code agent) | תור ביצוע — מה לכתוב ראשון, מה אחרי, מה לדחות |

> ה-orchestrator הוא הידיים. ה-strategy-controller שואל "האם?". ה-content-prioritizer שואל "מה ובאיזה סדר?".

---

## מיקום קבצי הסוכנים

```
C:\Projects\baby-mania-agent\.claude\agents\
├── 01-organic-tag-generator.md
├── 02-organic-keyword-research.md
├── 03-organic-blog-strategist.md
├── 04-organic-blog-writer.md
├── 05-organic-search-demand-validator.md
├── 06-organic-content-prioritizer.md
├── 07-organic-content-mapper.md
├── 08-organic-article-linker.md
├── 09-organic-product-linker.md
└── 10-organic-link-qa.md
```

---

## תלויות בצוותים אחרים

| תלות | פירוט |
|------|-------|
| צוות דף מוצר כללי | משתמש ב-context YAML וב-stage outputs (fabric_story, benefits) כקלט |
| תשתית משותפת | Shopify client, `.env`, orchestrator base |

> **חוק:** צוות אורגני לא משנה שום קובץ של צוות דף מוצר כללי.

---

## סוכנים עתידיים (מתוכננים)

> פרטים מלאים: `BabyMania-AI-Agents-Docs/ORGANIC-FUTURE-AGENTS.md`

| # | שם | תפקיד |
|---|----|--------|
| 11 | product-seo-builder | SEO title, meta description, slug, alt text לדפי מוצר |
| 12 | topic-cluster-builder | ארכיטקטורת אשכולות ברמת האתר — גילוי פערים והרחבה |
| 13 | promotion-agent | תוכנית קידום post-publish (social, email, WhatsApp) |
| 14 | monitoring-agent | מעקב ביצועי מאמרים + זיהוי הזדמנויות refresh |
