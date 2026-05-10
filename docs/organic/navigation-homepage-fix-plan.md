# Navigation + Homepage Quick Wins — Fix Plan
**Phase:** E (Planning) | **Mode:** READ-ONLY / T0 | **Date:** 2026-05-10
**Status:** NAVIGATION_HOMEPAGE_FIX_PLAN_READY
**Input source:** phaseD-homepage-ux-technical-audit.json + phaseD_index.json + theme assets API

---

## Task 1 — Current Navigation Map (17 Top-Level Items)

Data from Shopify GQL menus query (Phase D Task 8):

| Pos | Item | Issue | Recommendation |
|-----|------|-------|---------------|
| 1 | בגדי תינוקות | Parent OK — has 5 correct sub-items | KEEP — rename to "ביגוד" or leave |
| 2 | נעליים | Stand-alone, no sub-menu | KEEP — add sub-menu for categories |
| 3 | שמיכות עיטוף ושקי שינה | Too long — truncates on mobile | RENAME → "שינה" + move items to sub-menu |
| 4 | המיוחדים שלנו | Vague — unclear to customers | RENAME or REMOVE — merge into ביגוד |
| 5 | קיץ 2026 | Seasonal — will be stale | HOLD seasonal logic (see Task 3) |
| 6 | מארזי מתנה | Phase A fix ✅ → /collections/מארזי-מתנה | KEEP — rename to "מתנות לתינוק" if shorter |
| 7–16 | (10 additional items) | No grouping — flat overload | CONSOLIDATE into parent items |
| 17 | יצירת קשר | Not discoverable at position 17 on mobile | MOVE to footer + About sub-menu |

**Root cause of overload:** 17 items = near-impossible mobile UX. Industry standard: 5–8 top-level items.

---

## Task 2 — Proposed Premium Navigation (5–7 Top-Level Items)

```
BabyMania Navigation (Proposed)
├── ביגוד               [parent — HTTP]
│   ├── בנות            → /collections/בגדי-בנות
│   ├── בנים            → /collections/בגדי-בנים
│   ├── סטים            → /collections/סטים
│   ├── סרבלים          → /collections/סרבלים
│   └── כל הבגדים       → /collections/all-clothing
│
├── נעליים              [parent — HTTP]
│   ├── כל הנעליים      → /collections/נעליים
│   └── (sub-collections if exist)
│
├── שינה ואביזרים       [parent — HTTP]
│   ├── שמיכות עיטוף    → /collections/שמיכות-עיטוף
│   ├── שקי שינה        → /collections/שקי-שינה
│   └── EasySleep       → /products/™easysleep-...
│
├── מתנות               → /collections/מארזי-מתנה  [direct link]
│
├── מבצעים / חדש        → /collections/sale OR seasonal (see Task 3)
│
└── אודות               [parent — HTTP]
    ├── על BabyMania    → /pages/about
    └── יצירת קשר      → /pages/contact
```

**Result:** 5–6 top-level items. Mobile-friendly. Logical grouping.

---

## Task 3 — Seasonal & Age-Based Handling

### Current problems:
- `קיץ 2026` is hardcoded top-level nav — becomes stale, requires manual menu edit each season
- No age-based entry: 0–6m / 6–12m / 1–3y navigation is missing

### Recommendation:

**Seasonal (T1 — settings, no code):**
- Replace `קיץ 2026` with permanent `מבצעים` → link to sale/clearance smart collection
- OR rename to seasonal smart collection that Shopify manages automatically
- **Do not hardcode year** in menu label

**Age-based (HOLD — future phase):**
- Option: Add "גיל התינוק" parent item with 0-6m / 6-12m / 1-3y sub-items
- Requires product tagging by age range to populate collections
- **Scope:** T3 — requires smart collection creation + product tag audit
- **Decision:** HOLD for Phase F (product taxonomy cleanup)

---

## Task 4 — Homepage Quick Wins

### 4A — Hero: No Text or Primary CTA (HIGH PRIORITY)

**Current state:** bm-video-hero schema has NO heading/subtitle/main CTA fields. Two category nav buttons only.
**Root cause:** Section was built as pure media — schema intentionally minimal.

| Option | Action | Tier | Effort |
|--------|--------|------|--------|
| A | Add heading+subtitle+main_btn fields to bm-video-hero schema + Liquid render | T2 | 1–2h |
| B | Enable disabled image_banner_xt8BGU section (double-hero workaround) | T1 | 15min |
| C | Add bm-store-hero.liquid section (exists in theme) above current hero | T1 | 15min |

**Recommended: Option A (T2)** — cleanest result. Edit `sections/bm-video-hero.liquid`:
- Add schema fields: `heading` (text), `subheading` (text), `cta_label` (text), `cta_url` (url)
- Render overlay div with heading + primary CTA button in Liquid
- Keep existing 2 nav CTAs (בנות/בנים)

### 4B — Duplicate Heading "הנמכרים ביותר" (LOW — aesthetic)

**Current state:** Heading "הנמכרים ביותר" appears in both rich_text_xKGEmA (pos 6) and rich_text_itPixN (pos 8).
**Fix:** Rename `rich_text_xKGEmA` heading to specific product name (e.g., "מוצר השבוע" or the actual product).
**Tier:** T1 — Shopify Customize → change text only.

### 4C — Trust Signals Missing (MEDIUM PRIORITY)

**Current state:** bm-trust-badges.liquid EXISTS in theme but is NOT in homepage template.
**Fix:** Add section via Shopify Customize → drag bm-trust-badges.liquid to position 2 (after Hero).
**Tier:** T1 — no code. Configure 4–6 trust badges:
- משלוח מהיר (delivery time)
- תשלום מאובטח (secure payment)
- מדיניות החזרות (returns)
- שירות לקוחות (support)

**Also:** Enable `show_rating: true` in both featured-collection sections → zero code, T1.

### 4D — Performance: Product Card Overload (MEDIUM PRIORITY)

**Current state:** Both featured-collection sections use `products_to_show: 25` → ~50 product images load on homepage.
**Fix:** Reduce `products_to_show` from 25 → 8 on both sections.
**Tier:** T1 — Shopify Customize slider.
**Estimated improvement:** Remove ~34 images from initial render.

### 4E — Cleanup: Empty/Blank Sections (LOW — quick)

| Section | Issue | Fix | Tier |
|---------|-------|-----|------|
| `rich_text_bWQ9mf` (pos 17) | Empty heading — no content | Disable or delete | T1 |
| `image_banner_WY4jhi` (pos 15) | All blocks disabled — loads image but renders nothing | Disable | T1 |

---

## Task 5 — Full T-Tier Classification

| Item | Fix Description | Tier | Scope |
|------|----------------|------|-------|
| Navigation restructure (17 → 6 items) | Shopify Admin → Navigation → Edit menu | T1 | HIGH |
| Rename קיץ 2026 → מבצעים | Shopify Admin → Navigation | T1 | MEDIUM |
| Hero heading/CTA | Edit bm-video-hero.liquid schema + Liquid | T2 | HIGH |
| Rename duplicate heading rich_text_xKGEmA | Shopify Customize → change text | T1 | LOW |
| Add bm-trust-badges.liquid to homepage | Shopify Customize → add section | T1 | MEDIUM |
| Enable show_rating on featured-collection | Shopify Customize → toggle | T1 | LOW |
| Reduce products_to_show 25→8 (both sections) | Shopify Customize → slider | T1 | MEDIUM |
| Disable image_banner_WY4jhi (blank section) | Shopify Customize → disable | T1 | LOW |
| Disable rich_text_bWQ9mf (empty section) | Shopify Customize → disable | T1 | LOW |
| Sticky bar fix — EasySleep/Tempio (see Task 7) | Enable main-product section on those templates | T3 | HIGH |
| Age-based navigation (0-6m/6-12m/1-3y) | Smart collections + product tagging | T3 | HOLD |
| Subscription text (English) | Admin → Apps → find/configure app | T3 | HIGH |

---

## Task 6 — Phased Execution Order

### Phase E1 — T1 Quick Wins (Shopify Customize only — no approvals needed)
1. Reduce products_to_show 25→8 on both featured-collection sections
2. Disable image_banner_WY4jhi (blank)
3. Disable rich_text_bWQ9mf (empty)
4. Add bm-trust-badges.liquid after hero — configure 4 badges
5. Enable show_rating on featured-collection sections
6. Rename rich_text_xKGEmA heading (remove duplicate)

### Phase E2 — T1 Navigation Restructure (Shopify Admin → Navigation)
7. Restructure main menu: 17 items → 5–6 items per Task 2 proposal
8. Rename seasonal item (קיץ 2026 → מבצעים)
9. Move יצירת קשר to footer / About sub-menu

### Phase E3 — T2 Hero Enhancement (theme Liquid edit, needs T2 approval)
10. Edit bm-video-hero.liquid: add heading/subtitle/CTA schema fields
11. Test desktop + mobile overlay rendering

### Phase E4 — T3 Structural + App Fixes (needs T3 approval)
12. Fix sticky bar: enable main-product section on product.easy-sleep.json + product.tempio.json
13. Identify + configure subscription text app (Admin → Apps)

---

## Task 7 — Sticky Add-to-Cart Mobile Root Cause Analysis

### Root Cause
**File:** `sections/bm-sticky-bar.liquid` lines 113–114:
```javascript
var target = document.querySelector('.product-form__buttons');
if (!target) return;  // early return — sticky never activates
```

The sticky bar works by observing `.product-form__buttons` (the Add-to-Cart button container). If this element is absent from the DOM, the IntersectionObserver is never created and the sticky bar stays hidden forever.

### Affected Templates

| Template | Issue | Impact |
|----------|-------|--------|
| `product.easy-sleep.json` | `main-product` section has `"disabled": true` → no product form in DOM → `.product-form__buttons` = null | EasySleep sticky bar NEVER shows |
| `product.tempio.json` | Same: `"disabled": true` on main-product | Tempio sticky bar NEVER shows |
| `product.test.json` | `bm-sticky-bar` section is completely absent from template | No sticky bar at all |

All other templates (product.json, product.clothing.json, product.shoes.json, etc.) have bm-sticky-bar present AND main-product enabled → sticky bar works correctly.

### Recommended Fix

**Fix A — T3 (preferred):** Enable main-product section on the affected templates.
- In `product.easy-sleep.json`: remove `"disabled": true` from main-product section OR set `"disabled": false`
- In `product.tempio.json`: same
- Effect: standard product form renders → `.product-form__buttons` exists → sticky bar activates
- Risk: Must verify EasySleep custom layout still works after enabling main-product (may need to re-disable blocks within main-product that conflict with bm-store-hero or other custom sections)

**Fix B — T2 (fallback):** Add fallback selector in bm-sticky-bar.liquid.
- Edit line 113: `var target = document.querySelector('.product-form__buttons, .product-form, form[action="/cart/add"]');`
- Less clean but handles edge cases without template changes

**Decision:** Fix A (T3) preferred — addresses root cause. Fix B if EasySleep template structure is too complex to re-enable main-product without breaking layout.

---

## Summary

| Category | Quick wins available | Tier required | Est. time |
|----------|---------------------|--------------|-----------|
| Homepage cleanup | 5 items | T1 | 30 min |
| Navigation restructure | 17→6 items | T1 | 45 min |
| Trust signals | Add 1 section | T1 | 15 min |
| Hero CTA | Schema + Liquid edit | T2 | 1–2h |
| Sticky bar fix | Enable main-product | T3 | 30 min |
| Subscription text | Admin app config | T3 | variable |
