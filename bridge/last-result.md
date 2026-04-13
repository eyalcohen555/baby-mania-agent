task_id: 20260413-160144
---
3 `case` blocks and 3 `endcase` blocks — balanced. 

Now let me update the conductor state to report the result:

---

## SYSTEM STATE

- `bm-product-blog.liquid` section already exists and is live on Shopify (in `baby-mania-theme` repo)
- `product.clothing.json` already includes `bm-product-blog` section — working in production
- `product.shoes.json` was **missing** the `bm-product-blog` section
- The section's Liquid logic had **no shoes handles** and **no shoes fallback** — only clothing mappings

## CHANGES MADE

1. **`theme_assets/templates/product.shoes.json`** (local agent repo)
   - Added `bm-product-blog` section definition with settings
   - Added `bm-product-blog` to order array (position: after `bm_accordion`, before `bm_urgency`)

2. **`baby-mania-theme/shopify-theme/templates/product.shoes.json`** (theme repo)
   - Added `bm-product-blog` section definition with settings
   - Added `bm-product-blog` to order array (after `main`, before `related-products`)

3. **`baby-mania-theme/shopify-theme/sections/bm-product-blog.liquid`** (theme repo)
   - Added 13 shoes product handle → article slug mappings in the `{% case product.handle %}` block
   - Each shoe product gets its specific HUB-6 article + pillar as second article
   - Added shoes fallback logic (handles containing "shoe", "sneaker", "sandal", "boot", "walker") → routes to HUB-6 pillar + C1
   - Added 7 HUB-6 article slug → Hebrew title/description mappings in both Item 1 and Item 2 case blocks

## FILES UPDATED

| File | Repo | Change |
|------|------|--------|
| `theme_assets/templates/product.shoes.json` | baby-mania-agent | Added section + order entry |
| `shopify-theme/templates/product.shoes.json` | baby-mania-theme | Added section + order entry |
| `shopify-theme/sections/bm-product-blog.liquid` | baby-mania-theme | Added 13 handle mappings + shoes fallback + 7 slug→title mappings |

## RISK LEVEL

**LOW** — All changes are additive. No existing clothing logic was modified. The section already renders with a blank check (`{% if bm_pb_1_title != blank %}`), so shoes products that don't match will simply show nothing. JSON validated. Liquid tags balanced (3 case / 3 endcase).

---

**STAGE_VERDICT: PASS**

**EVIDENCE:** 
- Local shoes template now includes `bm-product-blog` section in both repos
- 13 shoe product handles mapped to specific HUB-6 articles from reverse-index v1.2
- Shoes fallback logic covers unmapped shoe products via handle keyword detection
- All 7 HUB-6 article slugs have Hebrew title + description in both item-1 and item-2 case blocks
- No changes to Shopify live (template not pushed yet)
- No changes to clothing path — all additions are new `{% when %}` cases

**SYSTEM STATE:** Shoes Product ↔ Blog local fix complete. Ready for STAGE-4 (local retest) before live deployment.