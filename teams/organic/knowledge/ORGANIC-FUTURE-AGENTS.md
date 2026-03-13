# ORGANIC-FUTURE-AGENTS.md
# BabyMania Organic Team — Future Agent Planning

> This document maps the organic content playbook into future system components.
> These agents are NOT yet implemented. This is a planning document only.
> Source: ORGANIC-CONTENT-KNOWLEDGE.md
> Created: 2026-03-09

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Implemented and active |
| 🔲 | Planned — not yet built |

---

## Currently Active Agents (Reference)

| Agent | Role |
|-------|------|
| 01-organic-tag-generator ✅ | Shopify tag taxonomy and discovery |
| 02-organic-keyword-research ✅ | Keyword research (intent-driven) |
| 03-organic-blog-strategist ✅ | Cluster-based topic strategy |
| 04-organic-blog-writer ✅ | Article writing (HTML, SEO, conversion) |
| 05-organic-search-demand-validator ✅ | Demand scoring and validation |
| 06-organic-content-prioritizer ✅ | Editorial roadmap and queue |

---

## Future Agents — Planned

---

### 07 — product-seo-builder 🔲

**Purpose:**
Build SEO metadata for product pages — separate from blog content.

**Playbook source:** ORGANIC-CONTENT-KNOWLEDGE.md — Section 4 (SEO Rules), Section 8 (Pre-Publish Checklist)

**Responsibilities:**
- Write SEO title for each product page (under 60 chars, keyword-first)
- Write meta description (under 155 chars, keyword + CTA)
- Generate product slug (keyword-based, hyphenated, no stopwords)
- Suggest alt text for all product images
- Validate keyword placement in product description

**Inputs:**
- `shared/product-context/{pid}.yaml`
- `output/stage-outputs/{pid}_keyword_research.json`

**Output:**
- `output/stage-outputs/{pid}_product_seo.json`

**Key rules from playbook:**
- Keyword in title, first sentence of description, slug
- One primary keyword per product page
- Alt text: descriptive + keyword when natural
- No keyword stuffing
- Meta description must include a soft CTA

**Not in scope:**
- Does not write body_html
- Does not modify Shopify directly (push via orchestrator)

---

### 08 — internal-link-builder 🔲

**Purpose:**
Build and maintain the internal link graph across all published blog articles and product pages.

**Playbook source:** ORGANIC-CONTENT-KNOWLEDGE.md — Section 4 (Internal Links), Section 6 (Content Cluster Strategy)

**Responsibilities:**
- Scan all published blog articles and product pages
- Identify where internal links are missing or could be strengthened
- Suggest anchor text and link targets for each article
- Map the cluster hierarchy (pillar → supporting → product pages)
- Detect orphaned articles (no internal links pointing to them)

**Inputs:**
- `output/stage-outputs/{pid}_blog_article_*.html` (all articles)
- `output/stage-outputs/{pid}_content_priority.json`
- `output/stage-outputs/{pid}_keyword_research.json`

**Output:**
- `output/link-map/internal_link_recommendations.json`

**Key rules from playbook:**
- Pillar pages must receive links from all supporting articles in the cluster
- Supporting articles link back to pillar
- Anchor text must be descriptive — never "click here" or "read more"
- 2–4 internal links per article minimum
- Product collection pages should receive links from money and support articles

**Not in scope:**
- Does not modify HTML files directly
- Does not push to Shopify

---

### 09 — topic-cluster-builder 🔲

**Purpose:**
Architect and expand topical clusters across the entire blog.
Think at the site level — not the product level.

**Playbook source:** ORGANIC-CONTENT-KNOWLEDGE.md — Section 6 (Content Cluster Strategy), Section 7 (Competitor Analysis Rules)

**Responsibilities:**
- Map all existing blog articles into topical hubs
- Identify gaps in each cluster (missing pillar? missing supporting topics?)
- Suggest cluster expansion topics based on PAA and SERP analysis
- Prioritize which clusters to build next (by business value + demand)
- Detect competitor cluster weaknesses (AI slop, thin coverage, missing FAQ)

**Inputs:**
- All `{pid}_blog_strategy.json` files
- All `{pid}_content_priority.json` files
- All `{pid}_keyword_research.json` files

**Output:**
- `output/cluster-map/topic_cluster_architecture.json`

**Key rules from playbook:**
- Each cluster = 1 pillar + 2–3 supporting + optional authority articles
- Never expand a cluster before the pillar is published and ranking
- Hidden diamond topics = highest expansion priority
- Competitor URL gaps = cluster expansion opportunities

**Not in scope:**
- Does not write articles
- Does not push to Shopify

---

### 10 — promotion-agent 🔲

**Purpose:**
Plan the post-publish promotion strategy for each blog article.
Organic traffic takes time — promotion accelerates initial traction.

**Playbook source:** ORGANIC-CONTENT-KNOWLEDGE.md — Section 1 (Trust and Authority)

**Responsibilities:**
- For each published article, generate a promotion plan:
  - Social media post suggestions (Facebook, Instagram — parent-focused)
  - Email newsletter excerpt
  - WhatsApp group content suggestion (for parent communities)
  - Pinterest pin description (visual content for parenting boards)
- Identify republish or update opportunities for existing articles

**Inputs:**
- `output/stage-outputs/{pid}_blog_article_*.html`
- `output/stage-outputs/{pid}_blog_strategy.json`

**Output:**
- `output/promotion/{pid}_article_promotion_plan.json`

**Key rules from playbook:**
- Promotion copy must match the article's informational tone — not ad copy
- Social posts lead with value, not with product
- Pinterest descriptions should use long-tail keyword phrasing
- No fake urgency in promotion copy

**Not in scope:**
- Does not post to social media directly
- Does not modify articles

---

### 11 — monitoring-agent 🔲

**Purpose:**
Track the performance of published blog articles and surface refresh opportunities.

**Playbook source:** ORGANIC-CONTENT-KNOWLEDGE.md — Sections 7 (Competitor Analysis), 8 (Pre-Publish Checklist)

**Responsibilities:**
- Monitor which articles have been published (tracking file)
- Flag articles older than 6 months for review
- Detect when a competitor has updated their article on the same keyword
- Suggest article refresh: new FAQ items, updated product mentions, new internal links
- Identify articles that should be merged (thin content) or expanded (good ranking, low CTR)

**Inputs:**
- `output/stage-outputs/{pid}_blog_article_*.html`
- `output/monitoring/published_articles_index.json`

**Output:**
- `output/monitoring/content_refresh_queue.json`

**Key rules from playbook:**
- Content refresh priority: articles ranking on page 2–3 for target keyword
- Refresh = update intro, add FAQ, add internal links, update product mentions
- Do not rewrite articles that are already ranking on page 1
- AI slop competitor updates = refresh opportunity (their weakened content = our advantage)

**Not in scope:**
- Does not rewrite articles directly
- Does not push to Shopify

---

## Implementation Order Recommendation

When ready to build these agents, implement in this order:

1. **07-product-seo-builder** — Highest immediate business value. Product SEO gaps are costing rankings today.
2. **08-internal-link-builder** — Second highest value. Internal links are free ranking signals.
3. **09-topic-cluster-builder** — After 5+ articles exist per cluster. Needs content to map.
4. **11-monitoring-agent** — After 10+ articles published. Needs published content to monitor.
5. **10-promotion-agent** — Lowest urgency. Organic is a long game; promotion accelerates but is not blocking.

---

## Shared Dependencies (all future agents)

All future agents will share:
- `ORGANIC-CONTENT-KNOWLEDGE.md` as the governing strategic reference
- `shared/product-context/{pid}.yaml` as product data source
- `output/stage-outputs/` as the data pipeline
- Shopify API credentials from `.env` (for agents that need to read published data)

---

*This document is a planning reference only.*
*Do not implement these agents until the current 6 active agents are fully tested and stable.*
