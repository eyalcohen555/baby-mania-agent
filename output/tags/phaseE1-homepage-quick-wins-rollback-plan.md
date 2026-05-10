# Phase E1 — Rollback Plan
**Date:** 2026-05-10 | **Mode:** LIVE

## Rollback Scope
All changes are to `templates/index.json` only (homepage template settings).
No Liquid/CSS/JS files were modified.

## How to Rollback

### Option A — Restore via API (preferred)
1. Read `output/tags/phaseE1-homepage-quick-wins-backup.json`
2. Extract the `template_value` field
3. PUT to theme 183668179257 asset `templates/index.json`

### Option B — Manual restore via Shopify Customize
Reverse each change individually:
- E1-1a/b: Restore products_to_show = 25 on both featured-collection sections
- E1-2: Re-enable image_banner_WY4jhi section
- E1-3: Re-enable rich_text_bWQ9mf section
- E1-4: Restore heading in rich_text_xKGEmA from "מוצר השבוע" → "הנמכרים ביותר"
- E1-5: Remove bm_trust_badges_E1_2026 section

## Backup
Backup saved: output/tags/phaseE1-homepage-quick-wins-backup.json
