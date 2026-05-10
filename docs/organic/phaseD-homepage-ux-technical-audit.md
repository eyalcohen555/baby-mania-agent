# Phase D — Homepage UX Technical Audit

**Date:** 2026-05-10  
**Mode:** READ-ONLY — T0 — No Shopify writes  
**Theme:** Copy of Dawn new (ID: 183668179257)  
**Template audited:** `templates/index.json`  
**Verdict:** PHASED_HOMEPAGE_UX_TECHNICAL_AUDIT_READY  

---

## Task 1 — Homepage Structure

**Template:** `templates/index.json` (22,074 chars)  
**Theme name:** Copy of Dawn new  
**Theme ID:** 183668179257  

### Section Order (17 sections)

| Pos | Section ID | Type | Name / Role | Status |
|-----|-----------|------|-------------|--------|
| 1 | `bm_video_hero_CRzC6Q` | `bm-video-hero` | Hero — 2 desktop videos (split) + 1 mobile video | ACTIVE |
| 2 | `custom_liquid_BzKyFU` | `custom-liquid` | Spacer div (32px height) | ACTIVE |
| 3 | `image_banner_xt8BGU` | `image-banner` | Image banner with heading/text/buttons blocks | **DISABLED** |
| 4 | `collection_list_YdPRgD` | `collection-list` | 5-collection grid tiles (בגדי-בנות/בנים/נעליים/חורף/מארזי-מתנה) | ACTIVE |
| 5 | `featured_product_xPjepJ` | `featured-product` | EasySleep product feature | ACTIVE |
| 6 | `rich_text_xKGEmA` | `rich-text` | Heading: "הנמכרים ביותר" | ACTIVE |
| 7 | `featured_product_9bffYN` | `featured-product` | Projector lamp product | ACTIVE |
| 8 | `rich_text_itPixN` | `rich-text` | Heading: "הנמכרים ביותר" + בובת לוטרה text | **DUPLICATE HEADING** |
| 9 | `featured_product_wKn6ej` | `featured-product` | Baby winter romper product | ACTIVE |
| 10 | `rich_text_RhHHWN` | `rich-text` | "ברוכים הבאים ל - baby mania" welcome text | ACTIVE |
| 11 | `custom_liquid_dqnD4Q` | `custom-liquid` | Embedded video (external CDN - non-Shopify) | ACTIVE |
| 12 | `featured_collection` | `featured-collection` | "בגדי תינוקות" — collection בגדי-חורף, 25 products | ACTIVE |
| 13 | `featured_collection_FXYxk4` | `featured-collection` | "קולקציות ילדים מדהימות" — collection נעליים, 25 products | ACTIVE |
| 14 | `17615407419d9e24f1` | `_blocks` | Testimonials carousel (3 reviews, AI-generated block) | ACTIVE |
| 15 | `image_banner_WY4jhi` | `image-banner` | Image banner — all text blocks disabled | ACTIVE (blank) |
| 16 | `rich_text_NMeQkb` | `rich-text` | "קצת עלינו" — store story text | ACTIVE |
| 17 | `rich_text_bWQ9mf` | `rich-text` | Empty heading — no content | ACTIVE (blank) |

---

## Task 2 — Hero / Video / CTA

### ROOT_CAUSE

```
HERO_SECTION: bm-video-hero (sections/bm-video-hero.liquid)
SECTION_TYPE: Custom built — NOT Dawn slideshow/hero

ISSUE_1: NO HEADLINE SUPPORT
  The bm-video-hero schema contains only:
    - video_desktop, image_desktop (fallback)
    - video_desktop_2, image_desktop_2 (second cell, optional)
    - video_mobile
    - btn1_text, btn1_link
    - btn2_text, btn2_link
  NO heading, subheading, title, or overlay text field exists in the schema.
  The section was designed as a pure media display with minimal navigation buttons.
  ROOT CAUSE: Section missing heading/subtitle settings by design.

ISSUE_2: LAYOUT IS SPLIT, NOT CAROUSEL
  When video_desktop_2 is set (current config), the section renders:
    - Desktop: two videos SIDE BY SIDE in a CSS grid (1fr 1fr), 72vh tall
    - Mobile: one full-100vh video
  There is NO carousel/slider — the 2 desktop videos play simultaneously.
  The perception of "3 videos" is because there are also 2 autoplay desktop videos
  + 1 autoplay mobile video + 1 custom-liquid CDN video lower on the page.

ISSUE_3: CTA EXISTS BUT IS MINIMAL
  Two buttons DO render (btn1="בגדי בנות", btn2="בגדי בנים") — overlaid bottom-center.
  These are category navigation links, not a primary purchase CTA.
  Missing: "ראה את כל המוצרים" / "קנייה עכשיו" / "כל הקולקציות" main CTA button.
  Missing: Any visible headline to explain what the store sells.
```

### RECOMMENDED_FIX (do not apply yet)

```
OPTION A — Quick, settings only (no Liquid edit):
  Add section bm-store-hero.liquid (already in theme) to the page with heading + CTA.
  Place it between sections 1 and 3, or replace bm-video-hero.

OPTION B — Schema edit (requires Liquid change, theme file write):
  Add heading, subtitle, and main_btn settings to bm-video-hero schema.
  Render heading overlay above the btn1/btn2 buttons.
  This is a minor Liquid edit (~10 lines).

OPTION C — Enable the disabled image_banner_xt8BGU:
  image_banner_xt8BGU (section 3) already has heading/text/buttons configured.
  Currently "disabled: true". Enabling it would add a second hero below the video.
  Trade-off: two hero sections back-to-back may look clunky.

RECOMMENDED: Option B (minor schema + Liquid edit on bm-video-hero) — cleanest solution.
  Scope: T2 — theme file write, needs approval.
```

---

## Task 3 — Subscription / Deferred Purchase Text

### SOURCE ANALYSIS

```
SOURCE_TYPE: THIRD-PARTY APP (most probable) or SHOPIFY PURCHASE OPTIONS RESIDUE

Evidence gathered:
  ✅ Selling plan groups via REST:   0 groups found
  ✅ Selling plan groups via GQL:    0 groups found
  ✅ EasySleep variant SPAs:         0 (no selling_plan_allocations on any variant)
  ✅ snippets/price.liquid:          NO deferred/subscription/recurring text
  ✅ snippets/buy-buttons.liquid:    NO deferred/subscription/recurring text
  ✅ locales/he.json:                NO "deferred"/"subscription"/"recurring" strings
  ✅ locales/en.default.json:        NO "deferred"/"subscription"/"recurring" strings
  ✅ featured-product.liquid:        NO subscription rendering logic
  ❌ Script tags:                    403 (read_script_tags scope missing — cannot verify)
  ❌ Installed apps list:            404 (scope not available)

Implication:
  The text is NOT from the Dawn theme's native Liquid code.
  The text is NOT from any configured selling plan group.
  The text IS likely injected by:
    A) A third-party subscription app (e.g., Appstle, ReCharge, Bold, Skio, Seal)
       that was installed and may still be active or left residual data.
    B) Shopify's native "Purchase options" feature if it was enabled
       then disabled — orphaned UI text from a prior configuration.
    C) A script tag or theme app extension not readable with current API scopes.
```

### AFFECTED_SECTIONS
```
Likely renders in: featured-product sections on homepage (buy-buttons area)
                   main-product.liquid on product detail pages
May appear in:    cart drawer / cart page (Shopify purchase option disclosure)
```

### RISK
```
HIGH — The text "This item is a deferred, subscription, or recurring purchase..."
appears in English in a Hebrew store. This:
  - Confuses Hebrew-speaking customers
  - Creates the impression the product requires a subscription
  - Reduces trust and may cause cart abandonment
```

### RECOMMENDED_FIX (do not apply yet)
```
STEP 1: Open Shopify Admin → Apps → check if any subscription app is installed.
STEP 2: If app found → configure it to hide disclosure text for non-subscription products,
        or uninstall if subscriptions are not needed.
STEP 3: Open Shopify Admin → Settings → Purchase options → disable if not used.
STEP 4: If no app and no purchase options enabled → check Script Tags via admin
        (Settings → Notifications or Script Editor app).
STEP 5: Consider adding hide CSS to theme if app cannot be configured:
        .selling-plan-form__text { display: none; }
        (Last resort — verify with Ayal before any write.)
```

---

## Task 4 — Duplicate "הנמכרים ביותר"

### DUPLICATE_SOURCE
```
Two separate rich-text sections have identical heading "הנמכרים ביותר":

Section A: rich_text_xKGEmA (position 6)
  - Type: rich-text
  - Blocks: heading "הנמכרים ביותר" (h2) only — no text
  - Introduces: featured_product_9bffYN (starry-sky projector lamp, position 7)

Section B: rich_text_itPixN (position 8)
  - Type: rich-text
  - Blocks: text "בובת לוטרה נושמת לתינוקות... עכשיו ב 50% הנחה" + heading "הנמכרים ביותר" (h2)
  - NOTE: heading block AFTER the text block (heading renders second visually)
  - Introduces: featured_product_wKn6ej (baby winter romper set, position 9)
```

### SECTION_IDS
```
rich_text_xKGEmA
rich_text_itPixN
```

### RECOMMENDED_RENAME_OR_REMOVE
```
OPTION A: Rename rich_text_xKGEmA heading → "המוצר הנבחר" or "מוצר השבוע"
          (No text content change, just heading text)
OPTION B: Rename based on the product: "מקרן כוכבים קסום"
OPTION C: Remove the heading block from rich_text_itPixN and keep only the text
          (the rich_text_itPixN heading is positioned AFTER the text anyway — odd UX)
Easiest fix: Option A — settings-only change in Shopify Customize.
Scope: T1 — theme content edit, no code change.
```

### RISK
```
LOW — Aesthetic/UX issue. Customers see "הנמכרים ביותר" twice in close proximity.
No functional impact. Easy to fix.
```

---

## Task 5 — Homepage Performance / Load Audit

### VIDEOS_COUNT
```
4 videos total on homepage:
  1. bm-video-hero desktop cell 1 (autoplay, loop, muted) — hero left panel
  2. bm-video-hero desktop cell 2 (autoplay, loop, muted) — hero right panel
  3. bm-video-hero mobile (autoplay, loop, muted) — shown on mobile only
  4. custom_liquid_dqnD4Q — external CDN video (https://cdn.shopify.com/videos/...),
     autoplay, loop, muted (inline <video> tag, NOT deferred)

Desktop renders simultaneously: 3 videos (2 hero + 1 CDN)
Mobile renders simultaneously: 2 videos (1 hero + 1 CDN)
```

### GIFS_COUNT
```
Cannot confirm from Liquid code alone — collection tile images are set in Shopify admin.
The 5 collection tiles (collection_list_YdPRgD) may include animated GIFs.
Requires storefront render or Shopify admin image inspection to confirm.
Estimate: 0–5 GIFs.
```

### PRODUCT_CARDS_ESTIMATE
```
featured_product_xPjepJ:   1 product card (EasySleep)
featured_product_9bffYN:   1 product card (projector lamp)
featured_product_wKn6ej:   1 product card (baby winter romper)
featured_collection:       up to 25 product cards (בגדי-חורף, products_to_show=25)
featured_collection_FXYxk4: up to 25 product cards (נעליים, products_to_show=25)
TOTAL ESTIMATE: ~53 product cards (with sliders on mobile = not all visible at once)
```

### IMAGES_ESTIMATE
```
Hero section:          2 desktop image fallbacks + 1 mobile = 3 (videos load instead)
Collection list:       5 collection tiles
Featured collections:  25 + 25 = 50 product card images
Featured products:     3 product images (1 each)
Image banners:         2 (one disabled, one blank)
Testimonials:          3 avatar placeholders
TOTAL ESTIMATE: ~60–65 images
```

### LAZY_LOADING_PRESENT
```
PARTIAL:
  ✅ bm-video-hero image fallbacks: loading="lazy" on <img> elements
  ✅ Dawn product cards (featured-collection): Dawn uses native lazy loading on card images
  ❌ bm-video-hero desktop videos: autoplay on page load — NOT deferred
  ❌ bm-video-hero mobile video: autoplay on page load — NOT deferred
  ❌ custom_liquid_dqnD4Q CDN video: inline <video autoplay> — NOT deferred
  ❌ collection_list_YdPRgD tiles: no explicit lazy on collection card images
```

### MAIN_PERFORMANCE_RISKS
```
RISK_1 (HIGH): 3 simultaneous autoplay videos on desktop page load.
  Video downloads start immediately; no deferral or intersection observer.
  Mobile data users and slow connections hit immediately.

RISK_2 (MEDIUM): featured-collection products_to_show=25 × 2 sections = 50 product images.
  Even with lazy loading, this means 50 image srcs must be resolved.
  On mobile (2 cols), many are visible immediately and download eagerly.

RISK_3 (MEDIUM): External CDN video in custom_liquid_dqnD4Q.
  URL: https://cdn.shopify.com/videos/... (it IS Shopify CDN, good)
  BUT: inline <video> with autoplay — plays immediately, no poster/deferral.

RISK_4 (LOW): image_banner_WY4jhi renders with all blocks disabled but still loads its image.
  Image: White_Beige_Baby_Product_Online_Shopping_Discount... PNG.
  Wasted image download.

RISK_5 (LOW): rich_text_bWQ9mf renders with empty heading — wasted DOM and CSS render.
```

### QUICK_WINS (do not apply yet)
```
1. Reduce products_to_show: 25 → 8–12 on both featured-collection sections (T1, settings only)
2. Remove/disable rich_text_bWQ9mf (empty section) — settings only (T1)
3. Add poster attribute + play-on-scroll to custom_liquid CDN video (T2, Liquid edit)
4. Disable image_banner_WY4jhi (T1, settings only)
5. Consider reducing bm-video-hero to 1 desktop video (no split) for mobile-first perf (T2)
```

---

## Task 6 — Trust Signals

### TRUST_SECTIONS_FOUND
```
SECTION FOUND IN THEME — NOT on homepage:
  ✅ sections/bm-trust-badges.liquid — RTL, configurable icon+title+desc grid
     Supports: multiple columns, card background, border/shadow, icon emoji, Hebrew text
     NOT in templates/index.json → Not shown on homepage

SECTION FOUND IN THEME — NOT on homepage:
  ✅ sections/bm-store-benefits.liquid — 6-card product benefits grid (20,576 chars)
     Purpose: product advantages (fabric, quality, etc.) — not purchase-trust signals
     NOT in templates/index.json

PARTIALLY PRESENT on homepage:
  ✅ Section 14 (17615407419d9e24f1) — _blocks testimonials:
     3 customer reviews with names and "Happy Customer/Verified Buyer" labels
     Auto-playing carousel at 5s intervals — IS on homepage
     This IS a trust signal (social proof), but only social proof. Not delivery/payment.
```

### CAN_ENABLE_WITH_SETTINGS
```
YES — bm-trust-badges.liquid exists in theme and can be added via Shopify Admin → Customize → Add section.
No code change needed. Only content configuration (icons, text).
Scope: T1 — settings only.
```

### NEEDS_NEW_SECTION
```
NO — The section already exists. It needs placement only.
```

### MISSING TRUST SIGNALS (not on homepage)
```
❌ משלוח חינם / זמן משלוח
❌ תשלום מאובטח (only in footer)
❌ מדיניות החזרות
❌ שירות לקוחות / אחריות
❌ Product star ratings (show_rating: false in both featured-collection sections)
❌ Payment method icons (footer only)
```

### RECOMMENDED_PLACEMENT
```
Add bm-trust-badges.liquid between sections:
  After position 4 (collection_list_YdPRgD) — before first featured-product
  OR directly after Hero (position 1) for immediate trust on landing.
Configure badges: 🚚 משלוח מהיר | 🔒 תשלום מאובטח | 🔄 החזרות קלות | 💬 שירות לקוחות | ⭐ ביקורות אמיתיות
```

---

## Task 7 — EasySleep Product Audit

```
PRODUCT_ID:   10085913231673
TITLE:        ™EasySleep פתרון שינה יעיל  שמחליף כמה מוצרים
HANDLE:       ™easysleep-מערכת-שינה-חכמה-לתינוקות-לשינה-רגועה-ורציפה-מבית-babymania
STATUS:       active
PRODUCT_TYPE: (empty)
TAGS:         (empty)

OPTIONS:
  דגם: [450 מ"ל, 300 מ"ל]   ← Volume/capacity of the device (diffuser/humidifier)
  צבע: [White, Brown]        ← Color

VARIANTS (4):
  51657462841657 | 450 מ"ל / White  | ₪319.00
  51657462874425 | 450 מ"ל / Brown  | ₪329.00
  51657462776121 | 300 מ"ל / White  | ₪279.00
  51657462808889 | 300 מ"ל / Brown  | ₪289.00

SELLING_PLAN_GROUPS: 0 (no subscriptions)

ISSUE_FOUND:
  NOT a bug — The 450מ"ל / 300מ"ל options are REAL product capacity variants.
  The product is a baby sleep device (diffuser/humidifier type) with two model sizes.
  These options correctly differentiate product models at different price points.

  MINOR ISSUES (UX, not data errors):
  1. Color labels in English ("White", "Brown") in a Hebrew store — inconsistent UX
  2. product_type and tags are empty — product won't appear in tag-based collections
  3. Title has ™ trademark symbol — unusual in product title
  4. Handle starts with ™ symbol — could cause URL edge cases

RECOMMENDED_ACTION:
  1. (Optional) Translate color options: "White" → "לבן", "Brown" → "חום"
  2. (Optional) Add product_type and relevant tags for collection membership
  These are non-blocking UX improvements. No fix required now.
```

---

## Task 8 — Navigation Audit (Post Phase A)

```
MAIN_MENU_ITEM_COUNT: 17 top-level items

TOP_LEVEL_ITEMS:
  1.  [FRONTPAGE]  דף הבית
  2.  [HTTP]       בגדי תינוקות  →  # (5 sub-items)
       ├── [COLLECTION] סטים → /collections/type-set
       ├── [COLLECTION] סרבלים → /collections/type-romper
       ├── [COLLECTION] בגדי בנות → /collections/gender-girl
       ├── [COLLECTION] בגדי בנים → /collections/gender-boy
       └── [COLLECTION] כל הבגדים → /collections/clothing-all
  3.  [COLLECTION] מתנות לתינוק → /collections/מארזי-מתנה ✅ PHASE A FIXED
  4.  [COLLECTION] בגדי חורף
  5.  [COLLECTION] קיץ 2026
  6.  [CATALOG]    כל המוצרים → /collections/all
  7.  [COLLECTION] בובת ריבורן
  8.  [COLLECTION] מוצרי בטיחות
  9.  [COLLECTION] משחקים לתינוק
  10. [COLLECTION] נעלי ילדים
  11. [COLLECTION] שמיכות עיטוף ושקי שינה
  12. [COLLECTION] תיקי החתלה
  13. [COLLECTION] לידה ואביזרים נלווים
  14. [BLOG]       בלוג
  15. [COLLECTION] עיצוב וטקסטיל לחדרי ילדים
  16. [COLLECTION] המיוחדים שלנו
  17. [PAGE]       יצירת קשר

BAGDEI_TINOKOT_STATUS: ✅ Correct — parent HTTP item with 5 COLLECTION sub-items

GIFTS_LINK_STATUS: ✅ PASS — "מתנות לתינוק" → /collections/מארזי-מתנה (Phase A fix working)
  resourceId: gid://shopify/Collection/471568646457
  URL: /collections/%D7%9E%D7%90%D7%A8%D7%96%D7%99-%D7%9E%D7%AA%D7%A0%D7%94 (percent-encoded Hebrew, correct)

UX_RISK_NOTES:
  - 17 top-level items is excessive — industry standard for e-commerce: 5–8 top-level
  - "קיץ 2026" is a seasonal link — should be temporary/promotional, not permanent nav
  - "בובת ריבורן" is a very specific niche — debatable at top-level
  - "המיוחדים שלנו" is vague — unclear what category this is
  - "שמיכות עיטוף ושקי שינה" is very long — truncates on mobile
  - No grouping of non-clothing items into a sub-menu (unlike "בגדי תינוקות")
  - "יצירת קשר" at position 17 — not discoverable on mobile where menu scrolls
  This is documented as future UX debt — NOT to be fixed now.
```

---

## Files Created

| File | Path |
|------|------|
| Technical audit MD | `docs/organic/phaseD-homepage-ux-technical-audit.md` |
| Technical audit JSON | `output/tags/phaseD-homepage-ux-technical-audit.json` |
| Homepage template | `output/tags/phaseD_index.json` (raw, for reference) |
