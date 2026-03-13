# Teams Index — אינדקס הצוותות

> רשימת כל הצוותות הפעילים והמתוכננים בפרויקט BabyMania AI Agents.

---

## צוותות פעילים (Active Teams)

### צוות 01 — צוות דף מוצר כללי

| שדה | ערך |
|-----|-----|
| **שם** | צוות דף מוצר כללי |
| **סטטוס** | ✅ פעיל |
| **זהות** | `TEAM-IDENTITY.md` |
| **הקשר** | `PROJECT-CONTEXT.md` |
| **כלל הפעלה** | `SYSTEM-STARTUP-RULE.md` |
| **פקודות** | `TEAM-COMMANDS.md` |

**תחומי אחריות:**
- Pipeline מלא: fetch → AI stages → push (+ Handle Safety Rule) → verify → audit
- סוכנים 00–07
- ביגוד בלבד, עברית, Active products only
- חנות: `a2756c-c0.myshopify.com`
- Handle Safety Rule: resolve אוטומטי ל-ASCII handle לפני push (מונע Shopify 422)

**קבצים שבבעלות הצוות:**
```
C:\Projects\baby-mania-agent\
├── 00-team-lead\orchestrator.py
├── .claude\agents\01–07
├── scripts\run-pipeline.py
├── prompts\*.md
├── templates\product.json
├── shared\business-rules.md
└── output\stage-outputs\*
```

---

### צוות 02 — צוות אורגני

| שדה | ערך |
|-----|-----|
| **שם** | צוות אורגני |
| **סטטוס** | ✅ פעיל |
| **זהות** | `ORGANIC-TEAM-IDENTITY.md` |
| **הקשר** | `ORGANIC-PROJECT-CONTEXT.md` |
| **פקודות** | `ORGANIC-TEAM-COMMANDS.md` |

**תחומי אחריות:**
- Pipeline: fetch → 01+02 (parallel) → 03 → 05 → strategy-controller → 06 → 04 (conditional) → **07 content-mapper → 08+09 (parallel) → 10 link-qa** → push tags → verify
- סוכנים: 01-tag-generator, 02-keyword-research, 03-blog-strategist, 04-blog-writer, 05-search-demand-validator, 06-content-prioritizer, **07-content-mapper, 08-article-linker, 09-product-linker, 10-link-qa** (Internal Linking Sub-Team)
- תגיות Shopify + מחקר מילות מפתח + אסטרטגיית אשכולות + כתיבת מאמרי בלוג SEO/AEO/BOFU
- לא משנה body_html / templates / template_suffix
- חנות: `a2756c-c0.myshopify.com`
- **Knowledge Base:** `ORGANIC-CONTENT-KNOWLEDGE.md` — כללי כתיבה, SEO, המרה, אשכולות, שכבות תוכן TOFU/AEO/BOFU
- **Topic Hub Map:** `TOPIC-HUBS-KNOWLEDGE.md` — 7 hubs מאושרים: keyword intent → hub mapping → cluster position → article creation
- **Content Layers:** כל מאמר מסווג — `tofu` (discovery) / `aeo` (answer engine) / `bofu` (commercial intent)

**קבצים שבבעלות הצוות:**
```
C:\Projects\baby-mania-agent\
├── 10-organic-lead\organic-orchestrator.py          # technical runner
├── 10-organic-lead\organic-strategy-controller.py   # strategic decision layer
└── .claude\agents\
    ├── 01-organic-tag-generator.md
    ├── 02-organic-keyword-research.md      ← upgraded: intent-first, hidden-diamond, Google-style phrasing
    ├── 03-organic-blog-strategist.md       ← upgraded: cluster thinking, pillar/supporting, content_type
    ├── 04-organic-blog-writer.md           ← upgraded: PPT intro, TACT ending, SEO rules, TOFU/AEO/BOFU structure
    ├── 05-organic-search-demand-validator.md ← upgraded: intent fit, SERP signals, hidden diamond flag
    ├── 06-organic-content-prioritizer.md   ← upgraded: Money→Support→Authority, editorial roadmap
    ├── 07-organic-content-mapper.md        ← Internal Linking Sub-Team: מיפוי מבנה תוכן, סיווג דפים, דפים יתומים
    ├── 08-organic-article-linker.md       ← Internal Linking Sub-Team: הצעות קישורים פנימיים במאמרים
    ├── 09-organic-product-linker.md       ← Internal Linking Sub-Team: קישורים טבעיים מאמר→מוצר
    └── 10-organic-link-qa.md              ← Internal Linking Sub-Team: אימות PASS/WARNING/FAIL

BabyMania-AI-Agents-Docs\ORGANIC-CONTENT-KNOWLEDGE.md  ← KNOWLEDGE BASE — כללי כתיבה, SEO, המרה
BabyMania-AI-Agents-Docs\TOPIC-HUBS-KNOWLEDGE.md       ← מפת אשכולות — 7 hubs + מוצרים + תורי מאמרים
BabyMania-AI-Agents-Docs\ORGANIC-FUTURE-AGENTS.md      ← future planning
prompts\blog-template-structure.md
output\stage-outputs\{pid}_organic_tags.json
output\stage-outputs\{pid}_keyword_research.json
output\stage-outputs\{pid}_blog_strategy.json
output\stage-outputs\{pid}_search_demand.json
output\stage-outputs\{pid}_organic_strategy_decision.json
output\stage-outputs\{pid}_content_priority.json
output\stage-outputs\{pid}_blog_article_{N}.html
output\stage-outputs\{pid}_article_link_suggestions.json
output\stage-outputs\{pid}_product_link_suggestions.json
output\stage-outputs\{pid}_internal_link_validation.json
output\site-map\internal_content_map.json
```

---

## צוותות מתוכננים (Planned Teams — לא בנויים עדיין)

### צוות 03 — צוות SEO/AEO (מתוכנן)

| שדה | ערך |
|-----|-----|
| **שם** | צוות SEO/AEO |
| **סטטוס** | 🔲 מתוכנן |
| **תלויות** | דורש תוצאות Pipeline מצוות 01 |

**תחומי אחריות (מתוכנן):**
- Agent 08: seo-aeo-builder
- יצירת תוכן SEO ו-AEO לדפי מוצר
- מבנה שאלות/תשובות לגוגל

---

### צוות 04 — צוות Taxonomy & Tags (מתוכנן)

| שדה | ערך |
|-----|-----|
| **שם** | צוות Taxonomy & Tags |
| **סטטוס** | 🔲 מתוכנן |
| **תלויות** | דורש context YAML מצוות 01 |

**תחומי אחריות (מתוכנן):**
- Agent 09: taxonomy-tag-generator
- יצירת תגיות מוצר ו-taxonomy שיטתית
- שיוך קטגוריות Shopify

---

## מבנה תיקיות Teams Context

```
C:\Users\3024e\Downloads\קלוד קוד\BabyMania-AI-Agents-Docs\
├── TEAMS-INDEX.md                  ← קובץ זה
├── TEAM-IDENTITY.md                ← זהות צוות דף מוצר כללי
├── PROJECT-CONTEXT.md              ← הקשר מלא של הפרויקט
├── SYSTEM-STARTUP-RULE.md          ← כלל הטעינה החובה
├── TEAM-COMMANDS.md                ← פקודות ה-pipeline
├── ORGANIC-TEAM-IDENTITY.md        ← זהות צוות אורגני
├── ORGANIC-PROJECT-CONTEXT.md      ← הקשר צוות אורגני
├── ORGANIC-TEAM-COMMANDS.md        ← פקודות צוות אורגני
├── ORGANIC-CONTENT-KNOWLEDGE.md      ← KNOWLEDGE BASE — כללי כתיבה, SEO, המרה
├── TOPIC-HUBS-KNOWLEDGE.md           ← מפת אשכולות — 7 hubs + pillar + מוצרים + agent instructions
├── TOPIC-HUBS-QUICK-REFERENCE.md     ← סקירה מהירה — hub priority, pillar per hub, agent fields
└── ORGANIC-FUTURE-AGENTS.md          ← תכנון סוכנים עתידיים
```

---

## כיצד להוסיף צוות חדש

1. צור קובץ `TEAM-{NAME}-IDENTITY.md` עם: שם, משימה, סוכנים, scope
2. הוסף `TEAM-{NAME}-COMMANDS.md` עם פקודות ספציפיות לצוות
3. עדכן קובץ זה בטבלת "צוותות פעילים"
4. עדכן `PROJECT-CONTEXT.md` עם הסוכנים החדשים
5. הוסף את הצוות ל-`SYSTEM-STARTUP-RULE.md` אם הוא נטען אוטומטית

---

## טבלת סוכנים לפי צוות

| Agent # | שם | צוות |
|---------|-----|------|
| 00 | team-lead | צוות דף מוצר כללי |
| 01 | product-analyzer | צוות דף מוצר כללי |
| 02 | fabric-story-writer | צוות דף מוצר כללי |
| 03 | benefits-generator | צוות דף מוצר כללי |
| 04 | faq-builder | צוות דף מוצר כללי |
| 05 | care-instructions | צוות דף מוצר כללי |
| 06 | validator | צוות דף מוצר כללי |
| 07 | shopify-publisher | צוות דף מוצר כללי |
| 01-organic | organic-tag-generator | צוות אורגני |
| 02-organic | organic-keyword-research | צוות אורגני |
| 03-organic | organic-blog-strategist | צוות אורגני |
| 04-organic | organic-blog-writer | צוות אורגני |
| 05-organic | organic-search-demand-validator | צוות אורגני |
| 06-organic | organic-content-prioritizer | צוות אורגני |
| 07-organic | organic-content-mapper | צוות אורגני — Internal Linking Sub-Team |
| 08-organic | organic-article-linker | צוות אורגני — Internal Linking Sub-Team |
| 09-organic | organic-product-linker | צוות אורגני — Internal Linking Sub-Team |
| 10-organic | organic-link-qa | צוות אורגני — Internal Linking Sub-Team |
| 11 | seo-aeo-builder | צוות SEO/AEO *(מתוכנן)* |
| 12 | taxonomy-tag-generator | צוות Taxonomy & Tags *(מתוכנן)* |
