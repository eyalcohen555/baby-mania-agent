# Phase E1c — Rollback Plan
**Date:** 2026-05-10

## How to Rollback

Restore original `sections/bm-sticky-bar.liquid` from backup:
1. Read `output/tags/phaseE1c-sticky-fix-backup.json`
2. Extract `.source` field
3. PUT to theme 183668179257 asset `sections/bm-sticky-bar.liquid`

The change is JS-only. Rolling back restores the original inline script behavior.
Backup saved: `output/tags/phaseE1c-sticky-fix-backup.json`
