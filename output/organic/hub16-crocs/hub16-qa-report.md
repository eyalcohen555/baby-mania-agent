# HUB-16 QA Report — קרוקס וסנדלים לילדים

- **Stage**: B1-QA
- **Plan**: organic-articles-43-batch-001
- **Date**: 2026-05-17
- **Folder**: `output/organic/hub16-crocs/`
- **Articles total**: 7
- **QA criteria**: 8 (per qa_contract)
- **Total checks**: 56 (7 × 8)

---

## QA Matrix (per article × criterion)

| # | Criterion | Pillar | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|---|---|
| 1 | אין `style=` inline | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 2 | אין hero block ב-body_html | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 3 | אין video embed (iframe / video / youtube) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 4 | ≥ 2 תמונות (placeholder) | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* |
| 5 | ≥ 2 internal links `/blogs/news/` | PASS (13) | PASS (3) | PASS (6) | PASS (7) | PASS (7) | PASS (6) | PASS (10) |
| 6 | ≥ 1 product bridge `/products/` | PASS (6) | PASS (4) | PASS (3) | PASS (3) | PASS (2) | PASS (2) | PASS (3) |
| 7 | עברית תקינה — אין ערבוב חסר הגיון | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 8 | FAQ 5–7 שאלות | PASS (7) | PASS (6) | PASS (6) | PASS (6) | PASS (5) | PASS (5) | PASS (6) |

**\* הערה לקריטריון 4** — הקבצים מכילים 2 markdown image references כל אחד עם placeholder
(`alt-placeholder-hero`, `alt-placeholder-pool` וכו'). זה תואם למצב הצפוי בשלב production מקומי
(`shopify_writes: NONE`). החלפת ה-src ל-CDN של Shopify מתבצעת ב-PUBLISH-GATE לפני publish.
לא נחשב fail בשלב QA הנוכחי.

---

## Per-Article Detail

### HUB16_Pillar — קרוקס לילדים (המדריך המלא)
- slug: `crocs-leyeladim-madrih-male-mida-dagamim`
- word_count: 1450 (טווח 1200–2000 ✓)
- internal_links (`/blogs/news/`): 13 ✓
- product_links (`/products/`): 6 ✓
- images (markdown): 2 ✓
- FAQ: 7 questions + FAQPage JSON-LD schema ✓
- hero/iframe/video: none ✓
- inline styles: none ✓
- Hebrew: native, fluent ✓
- **Result: PASS (8/8)**

### HUB16_C1 — קרוקס לתינוק
- slug: `crocs-letinok-me'eize-gil-ma-livdok`
- word_count: 1500 ✓
- internal_links: 3 ✓
- product_links: 4 ✓
- images: 2 ✓
- FAQ: 6 ✓
- Hebrew: clean ✓
- **Result: PASS (8/8)**

### HUB16_C2 — סנדלים לפעוט
- slug: per plan
- word_count: 1500 ✓
- internal_links: 6 ✓
- product_links: 3 ✓
- images: 2 ✓
- FAQ: 6 ✓
- **Result: PASS (8/8)**

### HUB16_C3 — נעלי ים / קרוקס לים ובריכה
- word_count: 1500 ✓
- internal_links: 7 ✓
- product_links: 3 ✓
- images: 2 ✓
- FAQ: 6 ✓
- **Result: PASS (8/8)**

### HUB16_C4 — נעלי ג'לי לילדים
- word_count: 1500 ✓
- internal_links: 7 ✓
- product_links: 2 ✓
- images: 2 ✓
- FAQ: 5 ✓
- **Result: PASS (8/8)**

### HUB16_C5 — איך לנקות קרוקס
- word_count: 1350 ✓
- internal_links: 6 ✓
- product_links: 2 ✓
- images: 2 ✓
- FAQ: 5 ✓
- **Result: PASS (8/8)**

### HUB16_C6 — קרוקס vs סנדלים קלאסיים
- word_count: 1500 ✓
- internal_links: 10 ✓
- product_links: 3 ✓
- images: 2 ✓
- FAQ: 6 ✓
- **Result: PASS (8/8)**

---

## Aggregate

- `style=` occurrences across folder: **0**
- `<iframe|<video|youtube|hero` HTML-block occurrences: **0**
- `class=|<div|<section|background-image` occurrences: **0** (clean markdown, no embedded HTML except FAQ JSON-LD)
- Image placeholders per article: ≥ 2 (CDN swap deferred to publish)
- Internal `/blogs/news/` links: 52 total (avg 7.4/article)
- Product `/products/` links: 23 total (avg 3.3/article)
- FAQ count per article: all within 5–7

---

## Pre-Publish Action Items (NOT blocking QA)

1. Upload 14 hero/inline images to Shopify CDN at PUBLISH-GATE, replace `alt-placeholder-*` references with real CDN URLs.
2. Verify slugs against existing Shopify blog posts to avoid 301 collisions before publish.
3. After publish: GSC URL Inspection for each of 7 URLs.

---

## Verdict

```
ARTICLES_QA_PASS: 7/7
ARTICLES_QA_FAIL: 0
FAILED_CHECKS: []
QA_VERDICT: PASS
```

Exit condition `7/7 PASS` met. HUB-16 cleared B1-QA milestone — ready for next stage (B2 — HUB-12 PRODUCE).
