# Phase A — Live Issues Fix Report

**Date:** 2026-05-10  
**T3 Approval:** Ayal — 2026-05-10  
**Mode:** live  
**Verdict:** PHASEA_LIVE_ISSUES_FIX_PASS  

---

## Summary of Fixes

| Fix | Item | Action | Result |
|-----|------|--------|--------|
| A1 | Pajama product PID 9606694306105 | Remove gender-girl, add gender-neutral, fix title | PASS |
| A2 | Navigation "מתנות לתינוק" | Change destination → /collections/מארזי-מתנה | PASS |
| A3 | occ-gift Smart Collection (526691860793) | Rename title from "מתנות לתינוק" to "בגדים שמתאימים למתנה" | PASS |
| A4 | PID 9096636825913 | Add occ-gift tag (was empty) | PASS |
| A5 | PID 9605887689017 | Read-only status check — no writes | READ_ONLY_COMPLETE |

---

## A1 — Pajama Product (PID 9606694306105)

**Handle:** cartoon-pajamas-suits-childrens-baby-boys-girls-spring-autumn-sleepwear-home-clothes-cotton-autumn-long-trousers-kids-pijamas

**Issue:** Title was corrupted (Hebrew encoding failure from previous session). gender-girl tag was present instead of gender-neutral.

**Fix applied:**
- Title: corrupted → `סט פיג'מה ארוכה לילדים`
- Tags: removed `gender-girl`, added `gender-neutral`

**Post-verify:**
- title_correct: ✅
- gender_girl_absent: ✅
- gender_neutral_present: ✅
- no_age_tags: ✅

---

## A2 — Navigation Fix

**Issue:** Main menu item "מתנות לתינוק" pointed to `/collections/occ-gift` (internal Smart Collection handle). Should point to `/collections/מארזי-מתנה` (Custom Collection, publicly branded).

**Fix applied:**
- menuUpdate GraphQL mutation on gid://shopify/Menu/250909851961
- "מתנות לתינוק" resourceId changed from `gid://shopify/Collection/526691860793` to `gid://shopify/Collection/471568646457`
- All 17 other menu items preserved intact

**Post-verify:**
- gifts_found: ✅
- gifts_url_is_matanat: ✅ (URL `/collections/%D7%9E%D7%90%D7%A8%D7%96%D7%99-%D7%9E%D7%AA%D7%A0%D7%94` = `/collections/מארזי-מתנה` percent-encoded)
- not_occ_gift_url: ✅
- bagdei_sub_intact: ✅ (5 sub-items in "בגדי תינוקות" preserved)
- item_count_17: ✅

---

## A3 — occ-gift Collection Title

**Issue:** Smart Collection "occ-gift" had title "מתנות לתינוק" which was misleading (same as the menu item that now points elsewhere).

**Fix applied:**
- Title: `מתנות לתינוק` → `בגדים שמתאימים למתנה`
- Handle: occ-gift (unchanged — Smart Collection rules/URL preserved)

**Post-verify:**
- handle_unchanged: ✅ (occ-gift)
- url_200: ✅ (/collections/occ-gift still resolves)
- title_not_misleading: ✅

---

## A4 — PID 9096636825913

**Title:** סט לתינוק עד 3 חודשים - מארז מתנה מפנק

**Issue:** Product had 0 tags — missing occ-gift tag to appear in the occ-gift Smart Collection.

**Fix applied:**
- Added `occ-gift` tag

**Post-verify:**
- occ_gift_present: ✅
- type_set_absent: ✅
- type_romper_absent: ✅
- product_accessible: ✅ (status=active)

---

## A5 — PID 9605887689017 (Read-Only)

**Title:** סרבל קיצי לתינוקות  
**Status:** active  
**Published:** 2024-08-20  
**Tags:** baby-gift, baby-romper, neutral-baby-outfit, newborn-clothing, summer-baby-wear  
**Shopify writes:** NONE  

**Findings:**
- REVIEW_ONLY — no type-* tags (manual classification needed)
- REVIEW_ONLY — no gender-* tags (manual classification needed)
- REVIEW_ONLY — occ-gift tag absent (needs manual review)

No action taken. All notes for future review only.

---

## Output Files

| File | Description |
|------|-------------|
| `output/tags/phaseA-live-fix-backup.json` | Pre-write backup of all 5 items |
| `output/tags/phaseA-live-fix-dry-run.md/json` | Dry-run plan |
| `output/tags/phaseA-live-fix-rollback-plan.md/json` | Rollback instructions |
| `output/tags/phaseA-live-fix-verify.md/json` | Post-write verification |
| `output/tags/phaseA-product-9605887689017-readonly-report.md/json` | A5 read-only report |
| `scripts/phaseA_live_fix.py` | Execution script (dry-run + live mode) |
