# Organic Article QA Rules — BabyMania Pipeline
# Version 3.0 — Presentation Spec Lock (2026-03-10)
#
# This file is the SINGLE SOURCE OF TRUTH for all organic article quality rules.
# Referenced by: Agent 04 (blog-writer), Agent 10 (link-qa), publish scripts.
# Do not bypass these rules. They exist because each was violated in production.
#
# v3.0 CHANGES: Rules 8–9 added (Presentation Spec Lock).
# Rule 2 updated: figure/figcaption required. Rule 4 updated: max product mentions.
# Rule 7 checklist extended to 15 checks.

---

## RULE 1 — HEBREW TITLE ENFORCEMENT

**Status: LOCKED — violated in HUB-1 first cycle (all 4 titles were English)**

Every article title MUST be in natural Hebrew.

### Requirements
- The `<h1>` tag and the Shopify `title` field must be in Hebrew
- Titles must read naturally to Israeli parents — not translated literally from English
- The target keyword must appear in the title in natural Hebrew phrasing
- No English words in the title (product names like "EasySleep™" are permitted as proper nouns)

### Approved title patterns by content_type

| content_type | Hebrew pattern |
|-------------|----------------|
| `how-to` | "איך [לעשות X] — [הבטחה קצרה]" |
| `listicle` | "[N] דברים שכדאי לדעת על [נושא]" |
| `review` | "[X] לעומת [Y]: מה עדיף לתינוק שלך?" |
| `aeo` | "האם [שאלה]? [תשובה קצרה ב-3 מילים]" |
| `bofu` | "[נושא ההחלטה]: מה לבדוק לפני הקנייה?" |

### Forbidden
- English titles (FAIL)
- Titles that are direct translations of English phrases (WARNING)
- Titles over 70 characters (WARNING — GSC truncation)

---

## RULE 2 — IMAGE REQUIREMENT

**Status: LOCKED — violated in HUB-1 (C1, C2, C4 had 1 image instead of 2)**
**Updated v3.0: figure/figcaption structure now required.**

Every article must contain exactly 2 images minimum.

### Required image HTML structure ⛔
```html
<figure class="article-image">
  <img src="https://cdn.shopify.com/..." alt="תיאור בעברית — keyword">
  <figcaption>כיתוב תחת התמונה</figcaption>
</figure>
```
- `<img>` must be wrapped in `<figure class="article-image">`
- `<figcaption>` is required — never omit
- No `style=""` on any image element
- Images inside `.img-grid` may use bare `<img>` without `<figure>`

### Placement rules
| Image | Position |
|-------|----------|
| Image 1 | Before or at the first H2 |
| Image 2 | Before or at the third H2 |

### Image source priority
1. Product images from Shopify CDN (`cdn.shopify.com`) — hub's product bridge
2. Other store product images relevant to the article topic
3. Trusted royalty-free stock source — only if no product image is available and the image is contextually relevant
4. If no suitable image available — **omit the `<img>` entirely** (never use placeholder or invented src)

### Section relevance rule ⛔ NEW
- Every image must contextually support the H2 section it appears in
- Do not reuse a product image in an unrelated section

### Alt text rules
- Alt text must be in **Hebrew**
- Must be descriptive and specific — describe what is actually shown in the image
- Must include the target keyword naturally where relevant
- Format: `[what is shown] — [context or keyword]`
- Example: `"תינוק לבוש בפיג'מה חמה לשינה בחורף — לבוש לשינה בטוח"`
- **Forbidden:** empty alt, English-only alt, generic alt
- **Generic alt text examples that are FORBIDDEN:** `"תמונת תינוק"`, `"baby image"`, `"מוצר"`, `"תמונה"`, `"product image"`, `"תינוק"`
- Generic alt detected → WARNING (Agent 10 Check 10)

### Verification
An article with fewer than 2 `<img>` tags MUST NOT be published.
An image without `<figure class="article-image">` wrapper → WARNING (does not block publish but must be fixed).

---

## RULE 3 — HEBREW LANGUAGE POLISH

**Status: LOCKED — violated in HUB-1 (machine-like phrasing detected post-publish)**

### Required polish pass
Before finalizing the HTML, scan the full body for these patterns and replace them:

| Unnatural (machine-like) | Natural Israeli Hebrew |
|--------------------------|------------------------|
| `על מנת ל` | `כדי ל` |
| `על מנת שה` | `כדי שה` |
| `הורים המחפשים` | `הורים שמחפשים` |
| `תינוקות הסובלים` | `תינוקות שסובלים` |
| `כפי שניתן לראות` | `כפי שרואים` |
| `יש לציין כי` | `חשוב לדעת:` |
| `בנוסף לכך,` | `בנוסף,` |
| `לאור האמור` | `לכן` |
| `ניתן לומר` | `אפשר לומר` |
| `בהתאם לכך,` | `בהתאם,` |

### Tone guidelines
- Write as a knowledgeable parent speaking to another parent — not as a content system
- Sentences: short and clear. Max 3 sentences per paragraph (enforced in B.3)
- No formal / bureaucratic phrasing
- No Anglicisms when a Hebrew word exists

### Forbidden phrases (auto-FAIL in QA)
- "חשוב מאוד לציין ש..."
- "כפי שאמרנו לעיל..."
- "לסיכום, ברור מאליו ש..."
- "שאלה מצוינת!"
- Any phrase that sounds like a translated prompt response

---

## RULE 4 — CTA LANGUAGE VALIDATION

**Status: LOCKED — weak CTAs found in HUB-1 ("לפרטים", "לצפייה ב-EasySleep")**

### Allowed CTAs only — no other phrasing permitted

| CTA button | Use case |
|-----------|----------|
| `לעמוד המוצר` | Product card — ONE button per card only |
| `לצפייה במוצר` | Product card — ONE button per card only |
| `לקריאה נוספת` | Internal article link |
| `למדריך המלא` | Link to pillar article |

> **RULE 4a — ONE CTA per product card (LOCKED 2026-03-10)**
> Each `.product-mention` card must contain **exactly one** `<a class="product-btn">`.
> Using both `לעמוד המוצר` AND `לצפייה במוצר` in the same card is **FORBIDDEN** — auto-FAIL.
> Use `לצפייה במוצר` as the default. Only use `לעמוד המוצר` if the HUB spec explicitly requires it.
> The `product-btn--secondary` CSS class must NOT appear in any article HTML.

> **RULE 4b — PRODUCT MENTION COUNT LIMITS (LOCKED v3.0)**
> Minimum: 1 product bridge per article (either a `.product-mention` card OR a `.cta-banner` that links to a product).
> Maximum: 2 `.product-mention` cards per article. More than 2 → **auto-FAIL**.
> The `.cta-banner` product link does NOT count against the 2-card maximum.

### Forbidden CTAs (auto-FAIL)
- `לפרטים` — too vague
- `לפרטים ורכישה` — too transactional
- `לצפייה ב-EasySleep™` — weak verb
- `לרכישה — ₪319` — price in CTA is pushy
- `המדריך המלא →` — arrow suffix not standard
- `קנו עכשיו` / `רכשו עכשיו` — fake urgency
- `לחצו כאן` / `לחץ כאן` — generic
- Two CTA buttons in a single `.product-mention` card — always forbidden

### Verification
Search the HTML for any button, `.cta-btn`, `.product-btn`, or `<a class=` element.
Every button text must match one of the 4 approved CTAs exactly.
Each `.product-mention` must contain exactly 1 `.product-btn` element — fail if 2 or more.

---

## RULE 5 — INTERNAL LINK VALIDATION

**Status: LOCKED — staged/deferred links were found live in HUB-1 C1 and C4 at publish**

### Pre-publish link requirements
1. Every `<a href>` pointing to a BabyMania blog URL must resolve to a **live, published article**
2. Staged anchor text (link-ready text written without `<a>` tags) is permitted in the article body during draft — but must be wrapped with `<a>` tags **before** or **at** publish time
3. No `href=""` or `href="#"` internal links allowed
4. No links to `babymania-il.com/blogs/news/` URLs that do not exist in `internal_content_map.json` with status `"published"`

### Deferred link rule
If a target article is not yet written (deferred cluster):
- Do NOT add a placeholder `<a>` tag
- Write the anchor text as link-ready plain text (per B.7)
- Record the deferred link in `article_link_suggestions.json` with `"status": "deferred"`
- Activate the `<a>` tag only after the target article is published

### HTTP verification
Before publishing, every internal URL must return HTTP 200.
If HTTP check fails → mark link as `"status": "broken"` in the QA report → FAIL.

---

## RULE 6 — RTL STRUCTURE CHECK

**Status: LOCKED — RTL rendering issues observed in HUB-1 lists and tables**

### Requirements
- Root `<html>` or `<body>` must have `dir="rtl"` OR the `.page-wrap` CSS must include `direction: rtl`
- All `<table>` elements: `dir="rtl"` or `text-align: right` on `<th>` and `<td>`
- All `<ul>` and `<ol>` lists: no `padding-left` without matching `padding-right`; use RTL-aware padding
- No inline `style="float:left"` on text containers (images may float, text must not)
- No `text-align: left` in `.article-body` — use `text-align: right` or `text-align: start`

### Verification check
Search the HTML for:
- `dir="rtl"` OR `direction: rtl` OR `direction:rtl` — must be present (FAIL if absent)
- `text-align: left` inside `.article-body` — FAIL if found
- `float: left` on paragraph containers — WARNING if found

---

## RULE 7 — PRE-PUBLISH QA CHECKLIST

**This checklist must be completed by Agent 10 (link-qa) before any article is published.**

| # | Check | Pass condition | Fail action |
|---|-------|---------------|-------------|
| 1 | **Title language** | Title is in Hebrew | Block publish |
| 2 | **Image count** | ≥ 2 `<img>` tags in body | Block publish |
| 3 | **Image placement** | `<figure class="article-image">` before H2-1 AND before H2-3 | Warning |
| 4 | **Alt text quality** | All alt texts in Hebrew, descriptive, non-generic | Warning |
| 5 | **Internal links live** | All href=blog URLs return HTTP 200 | Block publish |
| 6 | **No staged links** | No deferred links with `href=""` or `href="#"` | Block publish |
| 7 | **Product handle verified** | All `/products/{handle}` hrefs return HTTP 200 | Block publish |
| 8 | **CTA wording** | All buttons match approved list | Block publish |
| 9 | **RTL present** | `dir="rtl"` or `direction: rtl` found | Block publish |
| 10 | **No AI fluff** | No forbidden phrases (Rule 3 list) | Warning |
| 11 | **No fake urgency** | No "קנו עכשיו" / "מבצע מוגבל" | Block publish |
| 12 | **FAQ present** | ≥ 3 `<details>` blocks | Warning |
| 13 | **No inline styles** ⛔ v3.0 | No `style=""` attributes anywhere in body_html | Block publish |
| 14 | **No hero block** ⛔ v3.0 | No `.hero` / `.hero-overlay` / `<video` in body_html | Block publish |
| 15 | **Product mention count** ⛔ v3.0 | Exactly 1–2 `.product-mention` cards | Block publish |

**Overall result logic:**
- Any "Block publish" failure → `overall_result: "FAIL"` → article must not publish
- Only warnings → `overall_result: "WARNING"` → can publish, log for review
- All pass → `overall_result: "PASS"`

---

## AGENTS BOUND BY THESE RULES

| Agent | Rules applied |
|-------|--------------|
| `04-organic-blog-writer` | Rules 1, 2, 3, 4, 8, 9 (generation) |
| `08-organic-article-linker` | Rule 5 (link staging) |
| `09-organic-product-linker` | Rule 4, 5 (product CTA) |
| `10-organic-link-qa` | Rules 1–9 (full QA gate) |
| `publish_blog_articles.py` | Rule 5, 7 (HTTP verification before PUT) |

---

## RULE 8 — NO INLINE STYLES ⛔ NEW (v3.0)

**Status: LOCKED — Presentation Spec Lock 2026-03-10**

All visual styling is served from `assets/bm-blog-premium.css`.

### Requirements
- `style=""` attribute is FORBIDDEN on any HTML element in body_html
- This includes: `style="color:..."`, `style="margin:..."`, `style="text-align:..."`, etc.
- Exception: `dir="rtl"` is a semantic attribute — not a style — and is ALLOWED

### Verification
Search body_html for ` style="` (with space before style).
If found anywhere → **FAIL — Block publish**.

---

## RULE 9 — NO HERO BLOCK IN body_html ⛔ NEW (v3.0)

**Status: LOCKED — Presentation Spec Lock 2026-03-10**

The hero section is rendered by `main-article.liquid`. Writers must never include hero HTML.

### Requirements
- No `.hero` class in body_html
- No `.hero-overlay`, `.hero-content`, `.hero-tag`, `.page-wrap` classes in body_html
- No `<video` elements in body_html
- body_html starts from `.intro-box` — nothing before it

### Verification
Search body_html for: `class="hero"` OR `class="hero-overlay"` OR `<video` OR `class="page-wrap"`.
If found → **FAIL — Block publish**.

---

## CHANGE LOG

| Date | Change | Reason |
|------|--------|--------|
| 2026-03-10 | v3.1 — Image Source Policy | Rule 2 updated: trusted stock sources allowed; section relevance required; generic alt text explicitly forbidden; Rule 7 check 4 updated |
| 2026-03-10 | v3.0 — Presentation Spec Lock | Hero architecture change; CSS moved to bm-blog-premium.css; inline styles forbidden; figure/figcaption required; Rules 8–9 added; Rule 7 checklist extended to 15 items |
| 2026-03-10 | v2.1 — Rules 1–7 locked | HUB-1 manual QA cycle revealed systemic issues |
| — | v2.0 — original pipeline | Initial pipeline build |
