# Phase E1c — Sticky Add-to-Cart Fix Report
**Date:** 2026-05-10 | **Mode:** LIVE | **Tier:** T2
**Verdict:** PHASEE1C_STICKY_FIX_PARTIAL

## Change Applied

**File:** `sections/bm-sticky-bar.liquid`
**Type:** JavaScript only — no HTML, no CSS, no schema changes
**Lines changed:** 33

### Root Cause Fixed
Inline `<script>` (no defer) runs before `main-product` section renders.
`querySelector('.product-form__buttons')` returns null → early return → observer never created.

### Patch Applied (Option A)
Wrapped observer setup in `initStickyObserver()` with `readyState` check:
- If `readyState === 'loading'`: wait for `DOMContentLoaded` → run observer setup
- Otherwise: run immediately
- Added `.product-form__submit` fallback selector
- Changed `threshold: 0` → `threshold: 0.1` (shows sticky when 90% of button gone)

## Sanity Checks
- initStickyObserver_present: ✅
- domcontent_listener_present: ✅
- readystate_check_present: ✅
- threshold_0.1_present: ✅
- old_threshold_0_absent: ✅
- old_early_return_absent: ✅
- html_unchanged: ✅
- schema_unchanged: ✅
- style_unchanged: ✅

## Verify: FAIL
See `output/tags/phaseE1c-sticky-fix-verify.md` for per-product results.

## EasySleep / Tempio
Still broken — different root cause (`main-product` disabled).
Requires separate T3 approval and fix.

## Files
- Backup: `output/tags/phaseE1c-sticky-fix-backup.json`
- Rollback: `output/tags/phaseE1c-sticky-fix-rollback-plan.md`
