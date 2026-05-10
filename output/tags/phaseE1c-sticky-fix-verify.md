# Phase E1c — Verify Report
**Date:** 2026-05-10 | **Overall:** FAIL

| Product | Template | HTTP | Sticky | form__buttons | initObserver | DOMContent | readyState | threshold 0.1 | old gone | Verdict |
|---------|----------|------|--------|---------------|-------------|------------|------------|--------------|----------|---------|
| חליפת-תחרה-פרחונית-מורן | clothing | 200 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **PASS** |
| newborn-baby-winter-jacket-warm-hoo | clothing | 404 | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | **FAIL** |

## EasySleep / Tempio
Not tested here — `main-product` section is disabled on these templates.
Sticky will still not appear. Requires separate T3 fix (enable main-product).