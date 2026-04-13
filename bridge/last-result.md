task_id: 20260413-144959
---
Now I have the full audit. Here's the report:

---

## STAGE-2 AUDIT REPORT — Shoes Product ↔ Blog Readiness

### SYSTEM STATE

LAYER 2 is partially complete. Clothing Product ↔ Blog is live and working. Shoes Product ↔ Blog is **data-ready but not deployed**.

### FILES CHECKED

| File | Location | Status |
|------|----------|--------|
| `product.shoes.json` | Live Shopify theme + `theme_assets/templates/` | **Missing `bm-product-blog` section** |
| `product.clothing.json` | Live Shopify theme | **Has `bm-product-blog` section** ✅ |
| `bm-product-blog.liquid` | Live Shopify theme `sections/` | **Exists on live** ✅ |
| `product-reverse-index.json` | `output/site-map/` | **13 shoe products mapped to 7 unique HUB-6 articles** ✅ |
| `bm-product-blog.liquid` (local) | `theme_assets/`, downloads sections | **Not found locally** |

### HOW `bm-product-blog.liquid` WORKS

The section uses a **`case/when` on `product.handle`** to hardcode article slug assignments. Currently it only has clothing/bath product handles. For shoes, it needs:

1. **13 new `{% when %}` cases** — one per shoe product handle, mapping to HUB-6 article slugs
2. **7 new slug → Hebrew title/description entries** in both the Item 1 and Item 2 lookup tables
3. **A shoes fallback group** in the fallback logic (currently fallback only covers winter/denim/gifting/everyday clothing)

### MISSING OR BLOCKING ITEMS

| # | Item | Severity | What's Needed |
|---|------|----------|---------------|
| 1 | **Shoe handles not in `bm-product-blog.liquid` case/when** | BLOCKING | Add 13 shoe product handles with their HUB-6 article slugs |
| 2 | **HUB-6 slug → Hebrew title/desc lookup missing** | BLOCKING | Add 7 HUB-6 article entries to both Item 1 and Item 2 lookup tables |
| 3 | **Shoes fallback group missing** | BLOCKING | Add fallback for shoe products not in reverse-index (e.g., title contains "נעל"/"shoes") |
| 4 | **`product.shoes.json` missing `bm-product-blog` section** | BLOCKING | Add section entry to shoes template (on live Shopify) |
| 5 | **Local copy of `bm-product-blog.liquid` missing** | NON-BLOCKING | State doc says it's on live only; local file not tracked |

### EXACT FILES NEEDED FOR FIX

1. **`sections/bm-product-blog.liquid`** (on Shopify live theme) — Add:
   - 13 shoe `{% when %}` handle → slug mappings
   - 7 HUB-6 slug → Hebrew title/description entries (both Item 1 & Item 2 tables)
   - Shoes fallback group in fallback logic

2. **`templates/product.shoes.json`** (on Shopify live theme) — Add:
   - `"bm-product-blog": { "type": "bm-product-blog", "settings": {} }` section
   - Insert in order between `bm_accordion` and `bm_urgency`

### 7 HUB-6 ARTICLE SLUGS TO ADD

| Slug | Cluster |
|------|---------|
| `bchira-naale-tinok-madrih-male` | HUB-6-Pillar |
| `naal-tsaad-rishon-ma-kol-horeh-tzarich-ladaat` | HUB-6-C1 |
| `solya-gmisha-naale-yeladim-mah-hahevdel` | HUB-6-C2 |
| `mida-nachon-naale-yeladim-kacha-memdim-babayit` | HUB-6-C3 |
| `naale-gan-yeladim-mah-kday-ladaat` | HUB-6-C4 |
| `matay-lechahlif-naale-yeled-hassimanim` | HUB-6-C5 |
| `chomrim-noshmim-naale-tinoket-mah-levakesh` | HUB-6-C6 |

### RISK ASSESSMENT

- **Low risk** — The section architecture is proven (live on clothing). Shoes rollout is additive — no changes to existing clothing logic.
- The `case/when` pattern is well-established and understood.
- No architectural changes needed — just data additions.

---

**STAGE_VERDICT: PASS**

**EVIDENCE:** All components for shoes Product ↔ Blog rollout are identified. The section (`bm-product-blog.liquid`) exists on live and works for clothing. The reverse-index has all 13 shoe products mapped. The gap is precisely scoped: 2 files need updating (section Liquid + shoes template JSON) with specific, enumerable additions.

**SYSTEM STATE:** LAYER 2 shoes rollout is data-ready. Fix requires adding shoe handles + HUB-6 slugs to `bm-product-blog.liquid` and adding the section to `product.shoes.json`. Both changes are local-testable before live deployment.