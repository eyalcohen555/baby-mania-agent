# Phase E1 — Homepage Quick Wins Report
**Date:** 2026-05-10 | **Mode:** LIVE | **Tier:** T1
**Verdict:** PHASEE1_HOMEPAGE_QUICK_WINS_PASS
**Theme:** Copy of Dawn new (183668179257) | **Template:** templates/index.json

---

## Changes Applied

| ID | Section | Change | Verify |
|----|---------|--------|--------|
| E1-1a | `featured_collection` | products_to_show: 25 → 8 | **PASS** |
| E1-1b | `featured_collection_FXYxk4` | products_to_show: 25 → 8 | **PASS** |
| E1-2 | `image_banner_WY4jhi` | disabled: false → true | **PASS** |
| E1-3 | `rich_text_bWQ9mf` | disabled: false → true | **PASS** |
| E1-4 | `rich_text_xKGEmA` | heading: "הנמכרים ביותר" → "מוצר השבוע" | **PASS** |
| E1-5 | `bm_trust_badges_E1_2026` | New section added (after hero, block_type=badge, 4 badges) | **PASS** |
| E1-6 | show_rating | NO CHANGE — no reviews found | SKIP_OK |

All 6 live writes verified PASS. Template written to Shopify via PUT themes/183668179257/assets.json.

---

## Trust Badges (E1-5)
Schema: `bm-trust-badges.liquid` found — block_type=`badge`, text_field=`title`.
Section `bm_trust_badges_E1_2026` inserted after hero section `bm_video_hero_CRzC6Q`.
4 badges configured:
- משלוח מהיר לכל הארץ
- תשלום מאובטח
- החזרות עד 14 יום
- שירות לקוחות אישי

---

## show_rating (E1-6)
Product metafields API: 0 review fields found. `show_rating` left `false` on both featured-collection sections.
Action required: once reviews confirmed (app installed, reviews imported), toggle show_rating via Shopify Customize (T1).

---

## Sticky Add-to-Cart Audit (Part B)

**STICKY_SCOPE:** all_products (two distinct root causes)

### Group A — EasySleep + Tempio: BROKEN — STRUCTURAL
Root cause: `main-product` section has `"disabled": true` in template JSON → `.product-form__buttons` not in DOM → IntersectionObserver target = null → sticky never activates.
Fix: T3 — enable main-product section on `product.easy-sleep.json` + `product.tempio.json`.

### Group B — Clothing + other standard templates: BROKEN — BEHAVIORAL
Storefront HTML check on live clothing product (`חליפת-תחרה-פרחונית-מורן`, template=clothing, HTTP 200):
- `bm-sticky-bar` in HTML: ✅
- `.product-form__buttons` in HTML: ✅
- `IntersectionObserver` in HTML: ✅
- Sticky starts `aria-hidden="true"`: ✅

**Structural root cause: RULED OUT.** Sticky broken on mobile for behavioral reason.

Behavioral hypotheses (require T2 DevTools investigation):
1. Mobile viewport: page short enough → `.product-form__buttons` never exits viewport → IntersectionObserver fires `isIntersecting=true` always → sticky stays hidden
2. z-index conflict: sticky z-index:999 covered by Dawn header, cart drawer, or cookie banner
3. iOS Safari IntersectionObserver edge case with threshold:0
4. Dawn native sticky/cart interference

**Next action:** Developer to open mobile DevTools on a live clothing product and check IntersectionObserver callback behavior.

### Group C — product.test.json: BROKEN — NO SECTION
bm-sticky-bar section absent. Not a live template, low priority.

---

## Files Created
- `output/tags/phaseE1-homepage-quick-wins-backup.json`
- `output/tags/phaseE1-homepage-quick-wins-dry-run.json/.md`
- `output/tags/phaseE1-homepage-quick-wins-rollback-plan.md`
- `output/tags/phaseE1-homepage-quick-wins-verify.json/.md`
- `output/tags/phaseE1-sticky-reality-audit.json/.md`
- `docs/organic/phaseE1-homepage-quick-wins-report.md`
