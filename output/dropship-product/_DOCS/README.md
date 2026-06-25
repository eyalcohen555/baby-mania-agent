# Dropship Product Page Template

## How to Use

1. Copy `_TEMPLATE/product-page-template.liquid` into `output/<product-name>/`
2. Fill in all `{{PLACEHOLDER}}` tokens using the brief
3. Replace media paths (IMG_*, VID_*) with real CDN/asset URLs
4. Push to DUPE theme (187183563065) for QA
5. QA pass (11-point checklist) -> push to LIVE (183668179257)

## Variant Order Rule

| Variant Position | Meaning |
|---|---|
| 1 — first variant | Single unit |
| 2 — second variant | Pair / duo |
| 3 — third variant | Trio / triple pack |

The bundle form (`#bm-bundle-form`) reads `product.variants[0/1/2]` in this order.
Always create Shopify variants matching this order.

## Fill Brief -> Replace -> Push Workflow

```
brief.md -> sed/manual replace all {{ PLACEHOLDER }} in liquid -> git add -> push DUPE -> QA checklist -> push LIVE
```

## Section Map

| Section | data-section | Purpose |
|---|---|---|
| S1 | 1 | Hero + add-to-cart |
| S2 | 2 | Bundle selector |
| S3 | 3 | Trust bar |
| S4 | 4 | Problem hook |
| S5 | 5 | Problem agitation |
| S6 | 6 | Problem image |
| S11b | 11b | Mid-page CTA |
| S7 | 7 | Research social proof |
| S7.5 | 7.5 | Video demo |
| S8 | 8 | Benefits (what it builds) |
| S9 | 9 | Before/after image |
| S10 | 10 | Outcome for parent |
| S11 | 11 | Reviews / social proof CTA |
| S12 | 12 | Key stats |
| S13 | 13 | Who it's for (cards) |
| S15 | 15 | Price objections |
| S16 | 16 | FAQ |
| S17 | 17 | Final CTA |
