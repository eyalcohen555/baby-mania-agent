task_id: 20260511-133635
---
STAGE_VERDICT: **FAIL**

EVIDENCE:
- `product_type=Shoes` → `count_product_type_Shoes = 0` (no products in the store use this product_type)
- `tag=נעליים` → returned 600 products, but this is the full catalog, not a real filter result
- Sanity control: `tag=__no_such_tag_control__` → `count = 600` (same as `count_all`)
- Sanity control: `tag=baby-shoes` (a tag that demonstrably exists on real products) → `count = 600` as well
- Conclusion: Shopify's `tag=` query-string filter is **silently ignored** by this API context (likely a scope/permission limitation of the client_credentials app on this store). The prescribed two-filter strategy cannot produce a shoes-only list.
- Local-side scan of the merged response by shoe-related tag keywords (`baby-shoes`, `baby-sneakers`, `baby-sandals`, `baby-boots`, `נעליים`, etc.) found 47 actual shoe products embedded in the 600 returned items.
- Output written to `output/tags/shoes-products-raw.json` with full diagnostics, verdict, warning, and the merged product summaries (so the next stage has data to work with without being misled).
- SHOPIFY_WRITES: NONE — verified read-only throughout (only `GET /products.json` and `GET /products/count.json`).

FILES TOUCHED:
- `scripts/fetch_shoes_products.py` (new)
- `output/tags/shoes-products-raw.json` (new)

SYSTEM STATE:
- The current shoes inventory cannot be discovered through `product_type=Shoes` or `tag=נעליים` in this Shopify API context. Real shoe products are tagged with English keys (`baby-shoes`, `baby-sneakers`, `baby-sandals`, `baby-boots`) and need a different discovery strategy — e.g., fetch full catalog and filter locally on those tags, or query `/products/count.json` with `product_type` variations, or curate a known shoes collection. STAGE-5 must redefine the discovery filter before any tagging work proceeds.

EXACT NEXT STEP: redefine STAGE-4 discovery filter (or add STAGE-4b) to: (a) page all products once and filter locally on the known shoe tags, or (b) build a Shopify collection of shoes and pull `/collections/{id}/products.json` instead of `tag=`.