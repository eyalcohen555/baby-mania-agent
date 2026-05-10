# Phase E1b — Sticky Add-to-Cart Behavioral Debug
**Date:** 2026-05-10 | **Mode:** READ-ONLY + PATCH PLAN
**Tier:** T2 (patch plan only — not applied)
**Verdict:** PHASEE1B_STICKY_ROOT_CAUSE_READY

---

## Executive Summary

The sticky add-to-cart bar is **permanently broken on all clothing/standard product pages**. The root cause is a **DOM timing bug**: the `bm-sticky-bar.liquid` inline script runs before `main-product` renders, finds no `.product-form__buttons`, and exits early. The IntersectionObserver is never created. The bar stays `aria-hidden="true"` forever.

This is not a z-index, CSS, viewport, or iOS issue. It is a simple timing bug with a clean two-line fix.

---

## Task 1 — bm-sticky-bar.liquid Analysis

### Current Logic (from live Shopify — confirmed via storefront HTML)

```javascript
(function () {
    var bar    = document.getElementById('bm-sticky-bar');
    var stickyBtn = document.getElementById('bm-sticky-add-btn');
    var stickyPrice = document.getElementById('bm-sticky-price');
    if (!bar || !stickyBtn) return;

    // ← CRITICAL LINE
    var target = document.querySelector('.product-form__buttons');
    if (!target) return;   // ← exits here on every product page

    new IntersectionObserver(
        function (entries) {
            bar.setAttribute('aria-hidden', entries[0].isIntersecting ? 'true' : 'false');
        },
        { threshold: 0 }
    ).observe(target);

    // … price sync, click proxy …
}());
```

### Failure Analysis

| Item | Value | Issue |
|------|-------|-------|
| Script type | `<script>` (no defer, no module, no async) | Runs immediately inline |
| Script position in HTML | char 80,957 | Parsed early — section is pos 1 |
| `.product-form__buttons` DOM position | char 137,957 | 57,000 chars LATER (main-product pos 3) |
| `DOMContentLoaded` fallback | NONE | No recovery from early exit |
| Early exit on null target | `if (!target) return;` | Fires on EVERY product page |

### POSSIBLE_FAILURE_POINTS (all confirmed, not hypothetical)

1. **DOM timing**: Script runs at section position 1, `main-product` at position 3 → target null
2. **No fallback**: No `DOMContentLoaded`, no `readyState` check, no retry
3. **Strict null check**: `if (!target) return` — no soft degradation
4. **Observer never created**: `new IntersectionObserver(...)` line is never reached

### MOST_LIKELY_ROOT_CAUSE

```
Section order: bm_sticky_bar (pos 1) → bm_main_overrides (pos 2) → main (pos 3)
Script runs at pos 1 as inline (non-deferred) → .product-form__buttons = null at that moment
→ early return → observer never created → sticky permanently hidden
```

### CONFIDENCE: HIGH (verified by storefront HTML byte-offset analysis)

---

## Task 2 — CSS / z-index Analysis

### CSS from live bm-sticky-bar.liquid

```css
.bm-sticky-bar {
    position: fixed;
    bottom: 0; right: 0; left: 0;
    z-index: 999;
    transform: translateY(100%);   /* hidden by default */
    transition: transform 0.3s ease;
    pointer-events: none;
}
.bm-sticky-bar[aria-hidden="false"] {
    transform: translateY(0);      /* shows when aria-hidden="false" */
    pointer-events: auto;
}
```

### CSS_CONFLICTS_FOUND: NONE

- Live `bm-store-main-overrides.liquid` comment confirms: *"Sticky bar removed — handled exclusively by sections/bm-sticky-bar.liquid"*
- No `#bm-sticky-bar` CSS with higher specificity in live theme
- No conflicting `display: none` or `visibility: hidden` rules found
- `z-index: 999` — acceptable, no higher-z elements confirmed blocking it

### Z_INDEX_MAP (relevant fixed elements)

| Element | z-index | Source |
|---------|---------|--------|
| `.bm-sticky-bar` | 999 | bm-sticky-bar.liquid |
| Dawn `.header-wrapper` (sticky) | typically 3–5 | Dawn theme |
| Dawn cart drawer | typically 100 | Dawn theme |
| No conflict found | — | — |

### LIKELY_VISIBILITY_ISSUE: NONE (CSS is correct — bar would show if `aria-hidden="false"` were set)

### RECOMMENDED_CSS_FIX_IF_NEEDED: NONE required — CSS is correct.

**Secondary note:** No `env(safe-area-inset-bottom)` padding. On iPhone with home indicator, the bar is 12px off the very bottom. Minor cosmetic issue, not the cause of "doesn't work."

---

## Task 3 — IntersectionObserver Behavior Analysis

### Observer Configuration

```javascript
new IntersectionObserver(fn, { threshold: 0 }).observe('.product-form__buttons')
```

**threshold: 0** means: fire callback when ANY pixel of target enters or exits viewport.
- `isIntersecting: true` → at least 1px of target is in viewport
- `isIntersecting: false` → target is completely outside viewport

### INTERSECTION_LOGIC_RISK

The observer configuration is **correct in principle** but has one edge case:
- `threshold: 0` only shows sticky when the entire button container is COMPLETELY gone from viewport
- If `.product-form__buttons` is partially visible (e.g., just 1px peeking), sticky stays hidden
- `threshold: 0.1` would show sticky when 90% of the button is gone — slightly better UX

### Triage of hypothetical root causes (all now ruled out)

| Hypothesis | Status | Reason |
|-----------|--------|--------|
| Button always in viewport (short page) | RULED OUT | This would only cause sticky to never show on short pages, not on all pages |
| z-index conflict | RULED OUT | No conflicting z-index found |
| iOS safe-area | RULED OUT | Minor cosmetic, not functional |
| Dawn IntersectionObserver interference | RULED OUT | No Dawn IO uses same target |
| CSS hiding sticky | RULED OUT | CSS is correct |
| **DOM timing — script before main-product** | **CONFIRMED ROOT CAUSE** | char 80,957 vs 137,957 |

### BETTER_TRIGGER_OPTIONS

All are better than current behavior (observer never created):

| Option | Mechanism | Pros | Cons |
|--------|-----------|------|------|
| DOMContentLoaded + readyState fix | Same IntersectionObserver, deferred | Minimal change, correct behavior | Requires understanding readyState |
| scrollY > threshold | `window.scroll` event | Simple | Always shows after scroll, even on desktop |
| getBoundingClientRect polling | requestAnimationFrame | Works always | Heavy on CPU |
| Hybrid: IO + scroll fallback | Both together | Most robust | More code |

**Recommended: DOMContentLoaded + readyState fix** — smallest change, correct behavior preserved.

---

## Task 4 — Proposed Patch (T2, NOT APPLIED)

### Option A — JS Timing Fix (RECOMMENDED)

Replace the `var target = ... if (!target) return;` block with a DOMContentLoaded-aware init:

**File to modify:** `sections/bm-sticky-bar.liquid`
**Change type:** JavaScript only — no HTML, no CSS, no schema changes
**Scope:** ~5 lines changed within the existing `(function () { ... }())` IIFE

```javascript
// BEFORE (broken):
var target = document.querySelector('.product-form__buttons');
if (!target) return;

new IntersectionObserver(
    function (entries) {
        bar.setAttribute('aria-hidden', entries[0].isIntersecting ? 'true' : 'false');
    },
    { threshold: 0 }
).observe(target);
```

```javascript
// AFTER (fix):
function initStickyObserver() {
    var target = document.querySelector('.product-form__buttons')
              || document.querySelector('.product-form__submit:not(#bm-sticky-add-btn)');
    if (!target) return;

    new IntersectionObserver(
        function (entries) {
            var vis = entries[0].isIntersecting;
            bar.setAttribute('aria-hidden', vis ? 'true' : 'false');
        },
        { threshold: 0.1 }
    ).observe(target);
}

// If DOM still loading (section renders before main-product) → wait for DOMContentLoaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStickyObserver);
} else {
    initStickyObserver();  // DOM already ready (safe fallback)
}
```

**Why this works:**
- `bm_sticky_bar` renders before `main-product` → when script runs, `readyState` is `'loading'`
- DOMContentLoaded fires after ALL sections render → `.product-form__buttons` exists
- `initStickyObserver()` runs → observer created → sticky activates on scroll

**Why the `.product-form__submit` fallback:**
- `.product-form__buttons` is the container div (more reliable)
- `.product-form__submit:not(#bm-sticky-add-btn)` is the actual button (fallback if container class changes)
- `threshold: 0.1` instead of `0` → shows sticky when 90% of button is gone (slightly better UX on partial scrolls)

### Option B — Always Show After Scroll (simpler)

Mobile-only scroll trigger instead of IntersectionObserver:

```javascript
// Mobile only (max-width 768px)
if (window.innerWidth <= 768) {
    var shown = false;
    window.addEventListener('scroll', function () {
        if (!shown && window.scrollY > 250) {
            bar.setAttribute('aria-hidden', 'false');
            shown = true;
        } else if (shown && window.scrollY <= 50) {
            bar.setAttribute('aria-hidden', 'true');
            shown = false;
        }
    }, { passive: true });
} else {
    // Desktop: keep IntersectionObserver approach (with timing fix)
    // ... (Option A code)
}
```

**Pros:** Trivial to implement, no timing issues.
**Cons:** Shows sticky even when ATC button is still visible (on long-scroll pages). Less precise UX.

### RECOMMENDATION: Option A

Option A fixes the root cause without changing behavior. The sticky will appear at exactly the right moment (when ATC button exits viewport), same as originally intended. Option B is a fallback if Option A causes unexpected issues.

---

## Task 5 — EasySleep / Tempio Special Templates

### SPECIAL_TEMPLATES_STATUS

| Template | Sticky bar section | Main-product | Status |
|----------|--------------------|--------------|--------|
| product.easy-sleep.json | ✅ present | `"disabled": true` | BROKEN — different root cause |
| product.tempio.json | ✅ present | `"disabled": true` | BROKEN — different root cause |

### Root cause for EasySleep/Tempio (separate from clothing):

Even with the Option A DOMContentLoaded fix, these templates will still be broken. At DOMContentLoaded:
- `document.querySelector('.product-form__buttons')` → null (main-product section is disabled → form not rendered)
- `document.querySelector('.product-form__submit:not(#bm-sticky-add-btn)')` → null
- `if (!target) return` → exits → observer never created

### T3_REQUIRED: YES

Fix for EasySleep/Tempio requires T3 approval:
- Enable the `main` (main-product) section in `product.easy-sleep.json` and `product.tempio.json`
- Verify the EasySleep/Tempio custom layout isn't broken by the re-enabled main section
- This is a template structure change, not a code change

### RISK_IF_ENABLE_MAIN_PRODUCT

Medium risk:
- EasySleep uses `bm-store-hero.liquid` which likely provides the product form. Enabling `main-product` might render TWO product forms (one from main-product, one from bm-store-hero).
- Need to check bm-store-hero.liquid schema to understand if it renders its own ATC.
- Safe path: enable main-product but disable specific blocks within it that would duplicate content (title, price, buttons that bm-store-hero already shows).

---

## Combined Scope Map

| Template group | Root cause | Fix tier | Notes |
|---------------|-----------|---------|-------|
| product.clothing.json + shoes + accessories + reborn + default | DOM timing — bm_sticky_bar renders before main | **T2** | Option A patch |
| product.easy-sleep.json + tempio.json | main-product disabled → no form buttons in DOM | **T3** | Enable main-product carefully |
| product.test.json | bm-sticky-bar section absent | **T1** | Add section via Customize |
| product.test-template.json | Template OK — sticky should work after T2 fix | — | No separate action needed |
