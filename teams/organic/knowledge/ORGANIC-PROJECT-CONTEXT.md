# Project Context — צוות אורגני

> קרא קובץ זה בתחילת כל שיחה הקשורה לצוות אורגני.

---

## זהות הפרויקט

| שדה | ערך |
|-----|-----|
| שם הצוות | צוות אורגני |
| מטרה | תגיות Shopify + מחקר מילות מפתח + אסטרטגיית אשכולות + כתיבת מאמרי בלוג SEO/AEO/BOFU |
| Knowledge Base | `BabyMania-AI-Agents-Docs/ORGANIC-CONTENT-KNOWLEDGE.md` |
| Topic Hub Map | `BabyMania-AI-Agents-Docs/TOPIC-HUBS-KNOWLEDGE.md` — 7 hubs מאושרים |
| חנות (myshopify) | `a2756c-c0.myshopify.com` |
| חנות (ציבורי) | `babymania-il.com` |
| API Version | 2024-10 |

---

## מבנה הקבצים

```
C:\Projects\baby-mania-agent\
├── 10-organic-lead/
│   ├── organic-orchestrator.py          # technical runner (fetch/push/verify)
│   └── organic-strategy-controller.py  # strategic decision layer
├── .claude/
│   └── agents/
│       ├── 01-organic-tag-generator.md
│       ├── 02-organic-keyword-research.md
│       ├── 03-organic-blog-strategist.md
│       ├── 04-organic-blog-writer.md
│       ├── 05-organic-search-demand-validator.md
│       ├── 06-organic-content-prioritizer.md
│       ├── 07-organic-content-mapper.md
│       ├── 08-organic-article-linker.md
│       ├── 09-organic-product-linker.md
│       └── 10-organic-link-qa.md
├── shared/
│   └── product-context/
│       └── {pid}.yaml            # context YAML (משותף עם צוות דף מוצר)
└── output/
    └── stage-outputs/
        ├── {pid}_organic_tags.json      # פלט סוכן 01
        ├── {pid}_keyword_research.json  # פלט סוכן 02
        ├── {pid}_blog_strategy.json     # פלט סוכן 03
        ├── {pid}_search_demand.json     # פלט סוכן 05
        ├── {pid}_organic_strategy_decision.json  # פלט strategy-controller
        ├── {pid}_content_priority.json          # פלט סוכן 06
        ├── {pid}_blog_article_{N}.html  # פלט סוכן 04 (N=1-5)
        ├── {pid}_article_link_suggestions.json   # פלט סוכן 08 — הצעות קישורי מאמרים
        ├── {pid}_product_link_suggestions.json   # פלט סוכן 09 — הצעות קישורי מוצרים
        └── {pid}_internal_link_validation.json   # פלט סוכן 10 — אימות קישורים
└── site-map/
    └── internal_content_map.json     # פלט סוכן 07 — מפת תוכן האתר
```

---

## חוזה קבצי Stage (File Contract)

| קובץ | כותב | קורא |
|------|------|------|
| `{pid}.yaml` | צוות דף מוצר (agent 01) / organic fetch | organic-tag-generator |
| `{pid}_fabric_story.txt` | צוות דף מוצר (agent 02) | organic-tag-generator (אופציונלי) |
| `{pid}_benefits.txt` | צוות דף מוצר (agent 03) | organic-tag-generator (אופציונלי) |
| `{pid}_organic_tags.json` | organic-tag-generator | organic push |
| `{pid}_keyword_research.json` | organic-keyword-research | blog-strategist (03) / SEO planning |
| `{pid}_blog_strategy.json` | organic-blog-strategist | search-demand-validator (05) / blog-writer (04) |
| `{pid}_search_demand.json` | organic-search-demand-validator | strategy-controller |
| `{pid}_organic_strategy_decision.json` | organic-strategy-controller | content-prioritizer (06) — go/no-go gate |
| `{pid}_content_priority.json` | organic-content-prioritizer | blog-writer (04) + internal-link-builder (07) |
| `{pid}_blog_article_{N}.html` | organic-blog-writer | content-mapper (07) + article-linker (08) + product-linker (09) / Shopify blog upload |
| `internal_content_map.json` | organic-content-mapper (07) | article-linker (08) + product-linker (09) + link-qa (10) |
| `{pid}_article_link_suggestions.json` | organic-article-linker (08) | link-qa (10) / link injection (ידני / עתידי) |
| `{pid}_product_link_suggestions.json` | organic-product-linker (09) | link-qa (10) / link injection (ידני / עתידי) |
| `{pid}_internal_link_validation.json` | organic-link-qa (10) | pipeline go/no-go for publishing |
| `prompts/blog-template-structure.md` | extracted from article 680573141305 | blog-writer (04) — HTML layout reference |

---

## פורמט פלט — blog_strategy.json

```json
{
  "product_id": "9688934940985",
  "product_handle": "baby-bear-cozy-set",
  "source_keyword_file": "9688934940985_keyword_research.json",
  "blog_topics": [
    {
      "title": "What Clothes Does a Newborn Really Need?",
      "target_keyword": "what clothes does a newborn need",
      "content_type": "listicle",
      "article_role": "pillar",
      "article_type": "tofu",
      "topic_hub": "HUB-2: Newborn Clothing",
      "related_pillar": "How Many Clothes Does a Newborn Really Need",
      "product_bridge_relevance": "baby outfits, bodysuits, baby sets",
      "search_intent": "First-time parents preparing clothing for a newborn baby.",
      "why_this_article_matters": "Strong organic traffic potential, naturally leads to recommending newborn clothing products.",
      "internal_link_potential": "Can link to: HUB-2 pillar, HUB-4 fabric articles, product collection pages"
    }
  ],
  "topic_count": 5,
  "generated_at": "2026-03-09T15:00:00Z"
}
```

> **הערה:** blog_strategy.json לא נדחף ל-Shopify — הוא משמש לתכנון תוכן בלוג עתידי.

---

## פורמט פלט — keyword_research.json

```json
{
  "product_id": "9688934940985",
  "product_handle": "baby-bear-cozy-set",
  "primary_keyword": "newborn baby clothes",
  "secondary_keywords": [
    "soft baby clothing",
    "newborn outfit",
    "baby romper set",
    "infant clothing gift",
    "organic baby wear"
  ],
  "long_tail_keywords": [
    "soft winter clothes for newborn baby",
    "what to dress newborn in winter",
    "comfortable baby outfit for cold weather",
    "best baby romper for sensitive skin",
    "cute newborn coming home outfit"
  ],
  "search_intent": "Parent looking for warm, comfortable winter clothing for their newborn",
  "customer_problem": "Parents worry about keeping their baby warm without overheating",
  "commercial_relevance": "High commercial intent — parents searching for winter baby clothing are ready to buy",
  "hidden_diamond_opportunity": "how to dress a newborn for cold nights — strong PAA demand, weak competitor coverage",
  "suggested_topic_hub": "HUB-2: Newborn Clothing",
  "possible_new_hub_candidate": false,
  "generated_at": "2026-03-09T15:00:00Z"
}
```

> **הערה:** keyword_research.json לא נדחף ל-Shopify — הוא משמש כמסד נתונים למחקר SEO, תכנון בלוג, וקישור פנימי.

---

## פורמט פלט — organic_tags.json

```json
{
  "product_id": "9688934940985",
  "product_handle": "baby-bear-cozy-set",
  "shopify_tags": [
    "baby-set",
    "cozy-baby-outfit",
    "winter-baby-clothes",
    "newborn-gift",
    "soft-baby-fabric",
    "neutral-baby-outfit",
    "baby-bear-style",
    "everyday-baby-wear"
  ],
  "tag_count": 8,
  "generated_at": "2026-03-09T15:00:00Z"
}
```

---

## פורמט פלט — organic_strategy_decision.json

```json
{
  "product_id": "9688934940985",
  "should_create_blog_article": true,
  "recommended_first_article": {
    "title": "What Clothes Does a Newborn Really Need?",
    "target_keyword": "what clothes does a newborn need"
  },
  "priority_tier": "money",
  "next_best_action": "write_article",
  "confidence_level": "high",
  "business_value": "high",
  "blocking_issues": [],
  "reasoning_summary": "Composite score: 0.78 | Strong demand, clear parent relevance, high product fit.",
  "evaluation_method": "heuristic-estimated",
  "scores": {
    "composite": 0.78,
    "avg_demand": 8.2,
    "parent_search_relevance": 2.8,
    "commercial_relevance": 2.5,
    "product_fit": 2.7,
    "cluster_value": 2.3
  },
  "decided_at": "2026-03-09T16:00:00Z"
}
```

> **חשוב:** blog-writer (04) רץ **רק** אם `should_create_blog_article: true` ו-`next_best_action: "write_article"`.

| שדה | ערכים אפשריים |
|-----|--------------|
| `priority_tier` | `money` / `support` / `authority` / `skip` |
| `next_best_action` | `write_article` / `improve_keywords` / `improve_demand_validation` / `wait_for_data` / `skip_topic` / `product_seo_next` |
| `confidence_level` | `low` / `medium` / `high` |
| `business_value` | `low` / `medium` / `high` |

---

## כללי תגיות

| כלל | ערך |
|-----|-----|
| שפה | אנגלית בלבד |
| פורמט | lowercase, hyphen-separated |
| כמות | 6–10 תגיות למוצר |
| כפילויות | אסור |
| תגיות שיווקיות | אסור (`best-baby`, `premium-quality`) |
| המצאת חומרים | אסור — רק מה שמופיע בנתונים |

---

## Shopify API — עדכון תגיות

```
PUT /admin/api/2024-10/products/{pid}.json
Body: {"product": {"tags": "tag1,tag2,tag3"}}
```

> **חשוב:** שדה `tags` ב-Shopify הוא string אחד מופרד בפסיקים, לא array.
> ה-push stage ממיר את ה-array ל-comma-separated string.

---

## Handle Safety Rule

חל גם על צוות אורגני — כל פעולה שמשתמשת ב-handle חייבת לעבור resolve:
1. `product_handle` — אם ASCII-safe
2. `template_suffix_current` — fallback
3. `product_id` — last resort

> אמנם ב-organic push לא משתמשים ב-handle ל-template, אבל ה-rule עדיין חל על לוגים ואימות.
