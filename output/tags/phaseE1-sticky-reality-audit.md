# Phase E1 — Sticky Add-to-Cart Reality Audit
**Date:** 2026-05-10 | **Mode:** READ-ONLY
**STICKY_SCOPE:** all_products (two distinct root causes)
**ROOT_CAUSE_CONFIDENCE:** HIGH (EasySleep/Tempio) / MEDIUM (clothing — behavioral)

---

## Template Audit

| Template | Has Sticky | Main-Product | Enabled | form__buttons in DOM | Verdict |
|----------|-----------|-------------|---------|---------------------|---------|
| product.json | ✅ | `main` | ✅ | ✅ | LIKELY_WORKING |
| product.clothing.json | ✅ | `main` | ✅ | ✅ | HTML_CORRECT_BEHAVIOR_UNKNOWN |
| product.shoes.json | ✅ | `main` | ✅ | ✅ | LIKELY_WORKING |
| product.accessories.json | ✅ | `main` | ✅ | ✅ | LIKELY_WORKING |
| product.reborn.json | ✅ | `main` | ✅ | ✅ | LIKELY_WORKING |
| product.easy-sleep.json | ✅ | `main` | ❌ | ❌ | BROKEN_MAIN_PRODUCT_DISABLED |
| product.tempio.json | ✅ | `main` | ❌ | ❌ | BROKEN_MAIN_PRODUCT_DISABLED |
| product.test-template.json | ✅ | `main` | ✅ | ✅ | LIKELY_WORKING |
| product.test.json | ❌ | `main` | ✅ | ✅ | BROKEN_NO_SECTION |

---

## Storefront HTML Check

### Check v1 — INCONCLUSIVE
Product returned by API was archived (HTTP 404). Results invalid.

### Check v2 — DEFINITIVE (live published clothing product)
**Product:** חליפת תחרה פרחונית מורן (`חליפת-תחרה-פרחונית-מורן`)
**Template suffix:** clothing | **HTTP:** 200 ✅

| Check | Result |
|-------|--------|
| `bm-sticky-bar` in HTML | ✅ YES |
| `.product-form__buttons` in HTML | ✅ YES |
| `product-form` in HTML | ✅ YES |
| `IntersectionObserver` in HTML | ✅ YES |
| Sticky starts `aria-hidden="true"` | ✅ YES (correct initial state) |

**Conclusion:** HTML structure is CORRECT on live clothing product. Sticky is NOT broken due to missing selector or template disable on clothing. Broken for a behavioral reason.

---

## Root Cause Analysis by Group

### Group A — EasySleep + Tempio (CONFIRMED BROKEN — structural)
`main-product` section has `"disabled": true` in template JSON.
`.product-form__buttons` not rendered → `querySelector` returns null → early return → sticky never activates.
**Fix:** T3 — enable main-product section on both templates.

### Group B — Clothing / Shoes / Accessories / Reborn / Default (BEHAVIORAL — needs T2 investigation)
HTML structure confirmed correct. Sticky broken on mobile per Ayal's real-world test.
Structural root cause: RULED OUT.

**Behavioral hypotheses:**
1. Mobile viewport short: `.product-form__buttons` never fully exits viewport → IntersectionObserver never fires with `isIntersecting=false` → sticky stays hidden permanently
2. z-index conflict: Dawn sticky header, cart drawer, or cookie banner sits above sticky bar even when triggered (z-index:999 may not be enough)
3. iOS Safari IntersectionObserver edge case: `threshold:0` fires once on init but not on subsequent scroll events
4. Dawn native component interference: Dawn's built-in cart or sticky header conflicts with custom sticky bar

### Group C — product.test.json (CONFIRMED — no section)
bm-sticky-bar section completely absent. Not a live product template, low priority.

---

## Recommended Fix Options

| Tier | Fix | Scope |
|------|-----|-------|
| T1 | Add bm-sticky-bar to product.test.json | product.test.json only |
| T2 | Mobile DevTools: check IntersectionObserver callback, z-index, iOS Safari behavior; adjust threshold or add JS scroll fallback | Group B — all behaviorally broken templates |
| T3 | Enable main-product section on product.easy-sleep.json + product.tempio.json | Group A — EasySleep + Tempio |

**Next action required:** Open browser DevTools on mobile for `חליפת-תחרה-פרחונית-מורן` → check:
- Console errors
- Whether IntersectionObserver callback fires when scrolling
- Whether sticky bar z-index is covered by another element
- Whether `.product-form__buttons` is always in viewport (page too short)

---

## show_rating
No review metafields found. `show_rating` left `false` on both featured-collection sections. No change.
