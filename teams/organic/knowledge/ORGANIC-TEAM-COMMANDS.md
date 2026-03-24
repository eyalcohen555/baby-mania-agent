# Organic Team Commands — פקודות צוות אורגני

> כל הפקודות מורצות מ: `C:\Projects\baby-mania-agent\`

> **Knowledge Base:** כל הסוכנים עוקבים אחרי שני קבצים:
> - `BabyMania-AI-Agents-Docs/ORGANIC-CONTENT-KNOWLEDGE.md` — כללי כתיבה, SEO, אשכולות, המרה, **שכבות תוכן (TOFU/AEO/BOFU)**
> - `BabyMania-AI-Agents-Docs/TOPIC-HUBS-KNOWLEDGE.md` — 7 ה-hubs המאושרים: מיפוי נושאים, pillar pages, מוצרים מקושרים
>
> **זרימת העבודה:** keyword intent → topic hub mapping → cluster logic → **article_type (tofu/aeo/bofu)** → content prioritization → article creation
>
> **שכבות תוכן:** TOFU = discovery/SEO | AEO = answer engine (snippets, PAA, AI Overviews) | BOFU = commercial intent

---

## Orchestrator Commands (Technical Runner)

נקודת הכניסה: `10-organic-lead/organic-orchestrator.py`

```bash
# Fetch — שליפת מוצר (או שימוש ב-context קיים)
python 10-organic-lead/organic-orchestrator.py fetch PRODUCT_ID

# Push — עדכון tags ב-Shopify
python 10-organic-lead/organic-orchestrator.py push PRODUCT_ID

# Verify — אימות שהתגיות נשמרו
python 10-organic-lead/organic-orchestrator.py verify PRODUCT_ID

# Batch — הרצה על מספר מוצרים
python 10-organic-lead/organic-orchestrator.py batch ID1 ID2 ID3
```

---

## Strategy Controller Commands (Decision Layer)

נקודת הכניסה: `10-organic-lead/organic-strategy-controller.py`

```bash
# Decide — הערכה אסטרטגית של מוצר (האם לכתוב מאמר? מה לתעדף?)
python 10-organic-lead/organic-strategy-controller.py decide PRODUCT_ID

# Check — הצגת החלטה קיימת בלי הערכה מחדש
python 10-organic-lead/organic-strategy-controller.py check PRODUCT_ID

# Batch — הערכה של מספר מוצרים + סיכום (proceed/skip/blocked)
python 10-organic-lead/organic-strategy-controller.py batch ID1 ID2 ID3
```

---

## Flow מלא — מוצר בודד

```bash
cd C:/Projects/baby-mania-agent

# שלב 1: וודא שקיים context (אם המוצר כבר עבר fetch בצוות הראשי — דלג)
python 10-organic-lead/organic-orchestrator.py fetch 9999999999999

# שלב 2: הרץ סוכנים ב-Claude Code
#   Agent 01 → output/stage-outputs/{pid}_organic_tags.json      ┐ parallel
#   Agent 02 → output/stage-outputs/{pid}_keyword_research.json  ┘
#   Agent 03 → output/stage-outputs/{pid}_blog_strategy.json     (serial, after 02)
#   Agent 05 → output/stage-outputs/{pid}_search_demand.json     (serial, after 02+03)

# שלב 3: הרץ Strategy Controller — החלטה אם להמשיך לכתיבת מאמר
python 10-organic-lead/organic-strategy-controller.py decide 9999999999999
# → פלט: output/stage-outputs/{pid}_organic_strategy_decision.json
# → אם should_create_blog_article=true → המשך לשלב 4
# → אם false → עצור כאן (tags כבר נדחפים בנפרד)

# שלב 4: הרץ Content Prioritizer — תור ביצוע מדורג (איזה מאמר ראשון?)
#   Agent 06 → output/stage-outputs/{pid}_content_priority.json
# → recommended_now = המאמר הבא לכתיבה
# → content_queue = כל התור המדורג

# שלב 5: כתוב מאמר (רק אם Strategy Controller אישר!)
#   Agent 04 → output/stage-outputs/{pid}_blog_article_{N}.html
# → כתוב לפי recommended_now או top-ranked content_queue item

# שלב 5.5: Internal Linking Sub-Team (אחרי כתיבת המאמר)

#   Agent 07 (Content Mapper) → output/site-map/internal_content_map.json
# → מיפוי מבנה תוכן האתר — סיווג דפים, אשכולות, דפים יתומים

#   Agent 08 (Article Linker) → output/stage-outputs/{pid}_article_link_suggestions.json  ┐ parallel
#   Agent 09 (Product Linker) → output/stage-outputs/{pid}_product_link_suggestions.json  ┘
# → 08: הצעות קישורים פנימיים בתוך המאמר (anchor text, pillar, cluster)
# → 09: הצעות קישורים למוצרים (max 2, natural context, no aggressive CTA)

#   Agent 10 (Link QA) → output/stage-outputs/{pid}_internal_link_validation.json
# → אימות: PASS / WARNING / FAIL — לפני פרסום
# → בודק: 404, anchor text, density, pillar link, cluster link, duplicates
# → FAIL חוסם פרסום (hard gate דרך qa_gate.py)

#   Agent 10.5 (Content Reviewer) → output/stage-outputs/{pid}_content_review.json
# → REVIEWER ONLY — לא gate, לא מחובר ל-qa_gate.py
# → בודק בדיוק 2 נושאים: (1) איכות כותרת, (2) איכות intro-box (PPT)
# → תוצאה: PASS / WARN — WARN דורש החלטה אנושית, לא עוצר פרסום אוטומטית
# → מריצים לפי שיקול דעת, לא חובה בכל HUB

# שלב 6: Push tags ל-Shopify
python 10-organic-lead/organic-orchestrator.py push 9999999999999

# שלב 7: Verify
python 10-organic-lead/organic-orchestrator.py verify 9999999999999
```

---

## בדיקות מהירות (Quick Checks)

```bash
# רשימת organic_tags.json קיימים
ls output/stage-outputs/*_organic_tags.json

# רשימת keyword_research.json קיימים
ls output/stage-outputs/*_keyword_research.json

# רשימת blog_strategy.json קיימים
ls output/stage-outputs/*_blog_strategy.json

# בדיקת תגיות של מוצר ספציפי
cat output/stage-outputs/PRODUCT_ID_organic_tags.json

# בדיקת מחקר מילות מפתח של מוצר
cat output/stage-outputs/PRODUCT_ID_keyword_research.json

# בדיקת אסטרטגיית בלוג של מוצר
cat output/stage-outputs/PRODUCT_ID_blog_strategy.json

# בדיקת הערכת ביקוש אורגני של מוצר
cat output/stage-outputs/PRODUCT_ID_search_demand.json

# בדיקת החלטה אסטרטגית של מוצר
cat output/stage-outputs/PRODUCT_ID_organic_strategy_decision.json

# בדיקת תור תעדוף תוכן
cat output/stage-outputs/PRODUCT_ID_content_priority.json

# בדיקת מפת תוכן האתר (Content Mapper)
cat output/site-map/internal_content_map.json

# בדיקת הצעות קישורי מאמרים (Article Linker)
cat output/stage-outputs/PRODUCT_ID_article_link_suggestions.json

# בדיקת הצעות קישורי מוצרים (Product Linker)
cat output/stage-outputs/PRODUCT_ID_product_link_suggestions.json

# בדיקת אימות קישורים (Link QA — hard gate)
cat output/stage-outputs/PRODUCT_ID_internal_link_validation.json

# בדיקת סקירת תוכן (Content Reviewer — reviewer only, לא gate)
cat output/stage-outputs/PRODUCT_ID_content_review.json

# בדיקת החלטה מהירה (בלי הערכה מחדש)
python 10-organic-lead/organic-strategy-controller.py check PRODUCT_ID

# בדיקת tags נוכחיים של מוצר ב-Shopify
python 10-organic-lead/organic-orchestrator.py verify PRODUCT_ID
```

---

## Pipeline States

| State | מה זה אומר |
|-------|-----------|
| `fetched` | context YAML קיים (fetch או שימוש בקיים) |
| `tags_generated` | agent 01 כתב organic_tags.json |
| `keywords_generated` | agent 02 כתב keyword_research.json |
| `blog_strategy_generated` | agent 03 כתב blog_strategy.json |
| `search_demand_evaluated` | agent 05 כתב search_demand.json |
| `strategy_decided` | strategy-controller כתב organic_strategy_decision.json |
| `content_prioritized` | agent 06 כתב content_priority.json |
| `article_written` | agent 04 כתב blog_article_{N}.html |
| `content_mapped` | agent 07 כתב internal_content_map.json — מפת תוכן האתר |
| `article_links_suggested` | agent 08 כתב article_link_suggestions.json |
| `product_links_suggested` | agent 09 כתב product_link_suggestions.json |
| `links_validated` | agent 10 כתב internal_link_validation.json — PASS/WARNING/FAIL (hard gate) |
| `content_reviewed` | agent 10.5 כתב content_review.json — PASS/WARN (reviewer only, לא חוסם) |
| `tags_pushed` | tags עודכנו ב-Shopify |
| `tags_verified` | אומת שהתגיות נשמרו נכון |
| `failed` | כישלון בשלב כלשהו |

---

## Verify Checks (2 בדיקות)

| # | בדיקה | מה נבדק |
|---|-------|---------|
| 1 | tags_exist | המוצר ב-Shopify מכיל tags לא ריקים |
| 2 | tags_match | התגיות ב-Shopify תואמות ל-organic_tags.json |

---

## מה לא לעשות

- אסור לשנות `body_html` — זה בתחום צוות דף מוצר כללי
- אסור לשנות `template_suffix` — זה בתחום צוות דף מוצר כללי
- אסור תגיות בעברית — Shopify tags חייבים להיות באנגלית
- אסור להריץ push בלי organic_tags.json קיים
