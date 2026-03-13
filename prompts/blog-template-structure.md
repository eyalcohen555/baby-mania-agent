# Blog HTML Template Structure — BabyMania
# Presentation Spec v1.0 — LOCKED 2026-03-10
#
# ARCHITECTURE CHANGE (v1.0):
# - Hero is rendered by main-article.liquid — NOT in body_html
# - All CSS styling is served from assets/bm-blog-premium.css
# - body_html must contain semantic HTML classes only — NO <style> blocks, NO inline styles
# - Writers must NOT generate <style> tags or style="" attributes

---

## ⛔ ARCHITECTURE RULES — READ BEFORE WRITING

| Rule | Requirement |
|------|-------------|
| **Hero** | Rendered by `main-article.liquid` — NEVER write hero HTML in body_html |
| **CSS** | All styling from `assets/bm-blog-premium.css` — NEVER write `<style>` blocks |
| **Inline styles** | `style=""` attributes are FORBIDDEN everywhere in body_html |
| **Semantic classes** | Use only the approved class list below — no invented classes |
| **Hero fallback** | If no featured image: theme renders text-only hero — do NOT fall back to raw Dawn header |

---

## Styling Architecture

All visual presentation is handled by:
```
assets/bm-blog-premium.css
```

Design tokens (for reference only — do not hard-code in HTML):

| Token | Value |
|-------|-------|
| `--cream` | `#FAF7F4` |
| `--warm` | `#F2EBE2` |
| `--brown` | `#8B5E3C` |
| `--dark` | `#1E1510` |
| `--text` | `#3A2E25` |
| `--muted` | `#9A8878` |
| `--accent` | `#C4876A` |
| `--green` | `#6B9970` |
| `--radius` | `18px` |

Font: **Heebo** (weights: 300, 400, 500, 700, 800, 900) — loaded by theme, not by article.

---

## Required Block Order (body_html)

The hero is NOT part of body_html. Start body_html from the Intro Box.

```
body_html content order:
1.  .intro-box          ← article hook, PPT formula
2.  .quick-answer       ← optional, AEO articles only
3.  .toc                ← table of contents with anchor links
4.  .article-body       ← all H2 sections, images, callouts
    ├── [image 1]       ← figure.article-image — before or at H2-1 (REQUIRED)
    ├── H2 sections     ← 3–5 sections with id anchors
    ├── .tip-box        ← at least one per article
    ├── .warning-box    ← optional
    ├── [image 2]       ← figure.article-image — before or at H2-3 (REQUIRED)
    └── .product-mention ← 1–2 product cards (min 1, max 2)
5.  .cta-banner         ← required, links to product or collection
6.  #faq                ← required, 3–5 <details> + JSON-LD schema
7.  .article-tags       ← tag pills
```

---

## Block Specifications

### 1. INTRO BOX
- Class: `.intro-box`
- Contains: 1 paragraph (PPT formula: Preview + Proof + Transition)
- No heading inside the intro-box
- 3–5 sentences maximum

### 2. QUICK ANSWER BOX (optional)
- Class: `.quick-answer`
- Use only for `article_type: "aeo"` or tofu articles with a single focused question
- Do NOT use in BOFU articles
- Contains: `<strong>תשובה קצרה:</strong>` + 40–60 words

### 3. TABLE OF CONTENTS
- Class: `.toc`
- Contains: `.toc-title` + ordered list with anchor `<a href="#section-id">` links
- Every H2 in the article must have a matching TOC entry

### 4. ARTICLE BODY
- Class: `.article-body`
- Wraps all content sections
- `dir="rtl"` must be present on `.article-body` or on a parent wrapper

#### 4a. H2 Section Headings
- Each H2 must have an `id` attribute for TOC anchor linking
- No `style=""` on H2 — styling via bm-blog-premium.css

#### 4b. Content Paragraphs
- Standard `<p>` elements, max 3 sentences each

#### 4c. Bullet Lists
- `<ul>` with `<li>` items — RTL-aware (no `padding-left` without `padding-right`)

#### 4d. H3 Sub-headings
- Brown color via CSS class, smaller than H2

#### 4e. Tip Box
- Class: `.tip-box`
- Green left border, light green background (from bm-blog-premium.css)
- Contains: icon span (💡/✅) + paragraph

#### 4f. Warning Box
- Class: `.warning-box`
- Accent left border, light orange background
- Contains: icon span (⚠️) + paragraph

#### 4g. Note Box (new — Spec v1.0)
- Class: `.note-box`
- Neutral informational callout

#### 4h. Image Grid
- Class: `.img-grid`
- 2-column grid (single column on mobile via bm-blog-premium.css)
- Each image must have alt text in Hebrew

#### 4i. Single Article Image ⛔ REQUIRED FORMAT
```html
<figure class="article-image">
  <img src="https://cdn.shopify.com/..." alt="תיאור בעברית — keyword">
  <figcaption>כיתוב תחת התמונה</figcaption>
</figure>
```
- REQUIRED structure: `<figure>` wrapping `<img>` + `<figcaption>`
- Class must be `article-image` on the `<figure>` element
- Alt text: Hebrew, format `"[מה נראה] — [keyword]"` — must be descriptive and specific
- Alt text FORBIDDEN: empty, English-only, or generic (e.g., `"תמונת תינוק"`, `"baby image"`, `"מוצר"`)
- src: Shopify CDN preferred (`https://cdn.shopify.com/`) or trusted royalty-free stock source
- NO inline styles on `<figure>`, `<img>`, or `<figcaption>`
- Image MUST contextually support the H2 section it appears in — do not reuse an unrelated image

**Image placement requirements:**
| Image | Position |
|-------|----------|
| Image 1 | Before or at first H2 |
| Image 2 | Before or at third H2 |

#### 4j. Data Table (new — Spec v1.0)
- Class: `.data-table` on wrapping `<div>`, standard `<table>` inside
- `dir="rtl"` on table or wrapper

#### 4k. Checklist Summary (new — Spec v1.0)
- Class: `.checklist-summary`
- CSS grid layout for quantity-based checklists

#### 4l. Product Mention ⛔ REQUIRED FORMAT
```html
<div class="product-mention">
  <div class="product-info">
    <h3 class="product-name">שם המוצר</h3>
    <p class="product-price">₪XXX</p>
  </div>
  <a class="product-btn" href="https://babymania-il.com/products/{handle}">לצפייה במוצר</a>
</div>
```
- ONE `.product-btn` per card — NEVER two
- Minimum 1 product bridge per article (card OR cta-banner product link)
- Maximum 2 `.product-mention` cards per article
- Handle must be HTTP 200 verified before use

### 5. CTA BANNER ⛔ REQUIRED
- Class: `.cta-banner`
- Gradient background (from bm-blog-premium.css — do NOT inline)
- Contains: H3 title, paragraph, `.cta-buttons` group
- Buttons: `.cta-btn` (solid) + optionally `.cta-btn-outline` (outline)
- Must link to a product or collection

### 6. FAQ SECTION ⛔ REQUIRED
- ID: `#faq`
- Wrapper class: `.faq`
- Title: class `faq-title`
- Uses `<details>` + `<summary>` for collapsible Q&A
- 3–5 questions minimum
- Arrow indicator via bm-blog-premium.css ::after (do NOT add inline)

**JSON-LD schema — REQUIRED alongside FAQ HTML:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "שאלה ראשונה?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "תשובה ראשונה."
      }
    }
  ]
}
</script>
```
Every `<details>` question must have a matching entry in the JSON-LD schema.

### 7. ARTICLE TAGS
- Class: `.article-tags`
- Contains pill `.tag` elements
- 5–7 tags maximum

---

## Approved CSS Classes (bm-blog-premium.css)

Only these classes may appear in body_html. Do NOT invent new classes.

| Class | Purpose |
|-------|---------|
| `.intro-box` | Introduction paragraph box |
| `.quick-answer` | AEO direct answer box |
| `.toc` | Table of contents |
| `.toc-title` | TOC label |
| `.article-body` | Main article content wrapper |
| `.tip-box` | Green tip callout |
| `.warning-box` | Orange warning callout |
| `.note-box` | Neutral informational callout |
| `.img-grid` | 2-column image grid |
| `.article-image` | Single image figure wrapper |
| `.data-table` | Data table wrapper |
| `.checklist-summary` | CSS grid checklist |
| `.product-mention` | Product recommendation card |
| `.product-info` | Product info wrapper inside card |
| `.product-name` | Product name inside card |
| `.product-price` | Product price inside card |
| `.product-btn` | Product CTA link (pill button) |
| `.cta-banner` | Call-to-action banner section |
| `.cta-buttons` | Button group inside CTA banner |
| `.cta-btn` | Solid CTA button |
| `.cta-btn-outline` | Outline CTA button |
| `.faq` | FAQ section wrapper |
| `.faq-title` | FAQ section heading |
| `.article-tags` | Tag pills wrapper |
| `.tag` | Individual tag pill |

**FORBIDDEN in body_html:**
- `.hero`, `.hero-overlay`, `.hero-content`, `.hero-tag`, `.hero-video` — hero is in main-article.liquid
- `.page-wrap` — layout wrapper is in theme template, not body_html
- Any class not in the approved list above

---

## Responsive Behavior

Handled entirely by `assets/bm-blog-premium.css`. Writers do not need to write media queries.

Key breakpoints (for reference only):
```
@media (max-width: 600px):
  - Image grid: single column
  - CTA padding reduced
  - Article body padding reduced
```

---

## CHANGE LOG

| Date | Version | Change |
|------|---------|--------|
| 2026-03-10 | v1.1 — Image Source Policy | Trusted stock sources allowed alongside Shopify CDN; generic alt text forbidden; image must support section topic |
| 2026-03-10 | v1.0 — Presentation Spec Lock | Hero moved to main-article.liquid; CSS moved to bm-blog-premium.css; inline styles forbidden; figure/figcaption required; JSON-LD FAQ required; approved class list locked |
| — | v0.1 — initial | Extracted from article 680573141305 |
