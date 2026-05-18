# HUB-13 Water Shoes QA Report — Stage B3-QA

**Plan:** organic-articles-43-batch-001
**Stage:** B3-QA
**Task ID:** conductor-organic-articles-43-batch-001-B3-QA-20260517-220612
**Date:** 2026-05-17
**Tier:** T0

---

## QA Contract (8 criteria × 7 articles = 56 checks)

| # | Criterion |
|---|---|
| 1 | אין inline styles (`style=`) |
| 2 | אין hero ב-body_html |
| 3 | אין video embed |
| 4 | מינימום 2 תמונות / image slots (CDN Shopify swapped at publish) |
| 5 | מינימום 2 internal links |
| 6 | קיים product bridge (לפחות קישור מוצר/קולקציה אחד) |
| 7 | עברית תקינה — אין ערבוב שפות חסר הגיון |
| 8 | FAQ קיים — 5-7 שאלות |

**Note on criterion 4:** Source `.md` files use `![alt](alt-placeholder-*)` image slots. Real Shopify CDN URLs are swapped in by the publisher in stage B-publish. Criterion 4 is evaluated as "≥ 2 image slots present" — consistent with the precedent in `output/organic/batch-001-ext-qa-report.md` (A4-QA, 2026-05-17).

---

## Per-Article Results

### 1. HUB13_Pillar — `naalei-mayim-leyeladim-madrih-male-brekha-yam`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | grep `style=` → 0 hits |
| 2. no hero block | PASS | Markdown-only; no `<section class="hero">`, no HTML hero block |
| 3. no video embed | PASS | No `<iframe>`, `<video>`, YouTube |
| 4. ≥2 image slots | PASS | 2 (`alt-placeholder-hero`, `alt-placeholder-beach`) |
| 5. ≥2 internal links | PASS | 9 internal (HUB-6 Pillar, HUB-6-C3, HUB-11-C3, HUB-11-C6, HUB-16-P, HUB-16-C3, HUB-13-C1, HUB-13-C2, HUB-13-C3) |
| 6. product bridge | PASS | 3 product links (water-shoes, EVA crocs, summer sandals) |
| 7. valid Hebrew | PASS | Hebrew throughout; English terms (Aqua Shoes, Foam Clogs, mesh, EVA, UPF, SPF) used in proper context |
| 8. FAQ 5-7 | PASS | 7 questions in body + matching JSON-LD `FAQPage` schema |
**Verdict: 8/8 PASS**

### 2. HUB13_C1 — `naalei-mayim-letinok-me'eize-gil`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | grep `style=` → 0 hits |
| 2. no hero block | PASS | — |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 3 (`alt-placeholder-1`, `-2`, `-3`) |
| 5. ≥2 internal links | PASS | 3 internal (HUB-13-Pillar, HUB-6-C1, HUB-11-C6) |
| 6. product bridge | PASS | `/products/1-4t-baby-sandals-summer-breathable-air-mesh...` |
| 7. valid Hebrew | PASS | Hebrew; English (aqua socks, mesh) in context |
| 8. FAQ 5-7 | PASS | 5 questions + matching JSON-LD |
**Verdict: 8/8 PASS**

### 3. HUB13_C2 — `kafkafim-lapautot-layam-velabreykha`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | grep `style=` → 0 hits |
| 2. no hero block | PASS | — |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 2 (`alt-placeholder-1`, `-2`) |
| 5. ≥2 internal links | PASS | 2 internal (HUB-13-Pillar, HUB-16-Pillar) |
| 6. product bridge | PASS | `/products/childrens-sandals-summer-casual-eva-...` |
| 7. valid Hebrew | PASS | Hebrew; English (EVA, PVC, flip-flops, Croslite) in context |
| 8. FAQ 5-7 | PASS | 6 questions + matching JSON-LD |
**Verdict: 8/8 PASS**

### 4. HUB13_C3 — `naalei-yam-anti-hahlaka-leyeladim`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | grep `style=` → 0 hits |
| 2. no hero block | PASS | — |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 3 (`alt-placeholder-1`, `-2`, `-3`) |
| 5. ≥2 internal links | PASS | 2 internal (HUB-13-Pillar, HUB-6-C3) |
| 6. product bridge | PASS | `/products/1-4t-baby-sandals-summer-breathable-air-mesh...` |
| 7. valid Hebrew | PASS | Hebrew; English (TPR, PVC, EVA, anti-slip, Croslite, mesh) in context |
| 8. FAQ 5-7 | PASS | 6 questions + matching JSON-LD |
**Verdict: 8/8 PASS**

### 5. HUB13_C4 — `bgad-yam-livanot-tinokot-upf50-bchira`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | grep `style=` → 0 hits |
| 2. no hero block | PASS | — |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 3 (`alt-placeholder-1`, `-2`, `-3`) |
| 5. ≥2 internal links | PASS | 2 internal (HUB-13-Pillar, HUB-11-C2) |
| 6. product bridge | PASS | `/products/baby-swimsuit` |
| 7. valid Hebrew | PASS | Hebrew; English (UPF50, SPF, UVA, UVB, AS/NZ 4399, EN 13758) in proper context |
| 8. FAQ 5-7 | PASS | 6 questions + matching JSON-LD |
**Verdict: 8/8 PASS**

### 6. HUB13_C5 — `bgad-yam-livanim-tinokot-mah-amid-yoter`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | grep `style=` → 0 hits |
| 2. no hero block | PASS | — |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 2 (`alt-placeholder-1`, `-2`) |
| 5. ≥2 internal links | PASS | 2 internal (HUB-13-Pillar, HUB-11-Pillar) |
| 6. product bridge | PASS | `/products/baby-boy-swim-set` |
| 7. valid Hebrew | PASS | Hebrew; English (rashguard, UPF) in context |
| 8. FAQ 5-7 | PASS | 6 questions + matching JSON-LD |
**Verdict: 8/8 PASS**

### 7. HUB13_C6 — `tsiyud-hof-letinok-reshima-mele'a`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | grep `style=` → 0 hits |
| 2. no hero block | PASS | — |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 2 (`alt-placeholder-1`, `-2`) |
| 5. ≥2 internal links | PASS | 4 internal (HUB-13-Pillar, HUB-11-C6, HUB-5-Pillar, HUB-11-C3) |
| 6. product bridge | PASS | 2 product links (`/products/baby-beach-essentials`, water-shoes) |
| 7. valid Hebrew | PASS | Hebrew; English (pop-up, UPF, SPF, swim diaper, squeeze) in context |
| 8. FAQ 5-7 | PASS | 6 questions + matching JSON-LD |
**Verdict: 8/8 PASS**

---

## Content Overlap Check vs HUB-11-C2

**HUB-11-C2** (LIVE, source: hub-registry.json)
- Title: *בגד ים לתינוקת — איך לבחור, מה לבדוק ואיזה קרם הגנה להשתמש*
- Keyword: `בגד ים לתינוקת`
- Intent: commercial (general buying guide + sunscreen guidance)

**HUB-13-C4** (new this batch)
- Title: *בגד ים לבנות תינוקות — UPF50 ובחירה נכונה*
- Keyword: `בגד ים לבנות תינוקות`
- Intent: commercial_educational (UPF50 fabric deep-dive)

**Overlap analysis:**
- Same topic family (baby girl swimwear) — but different long-tail keywords (`בגד ים לתינוקת` singular vs `בגד ים לבנות תינוקות` plural+gender)
- HUB-11-C2 = general buying guide (cuts, sizes, sunscreen). HUB-13-C4 = single-angle deep-dive on UPF50 (UPF vs SPF, AS/NZ 4399, EN 13758, fabric density tests, color vs weave). No section repeats HUB-11-C2's general guidance.
- HUB-13-C4 explicitly internal-links to HUB-11-C2 as the complementary general guide.

**Cannibalization risk:** LOW. Distinct keyword targets, complementary angles, mutual linking. Search engines should split them.

**HUB-13-C5** (`בגד ים לבנים תינוקות`) is for baby boys — no overlap with HUB-11-C2 (girls).

**CONTENT_OVERLAP:** **WARNING** — same family but distinct angle, sufficient differentiation.

---

## Summary

| Metric | Value |
|---|---|
| Articles checked | 7 |
| Checks per article | 8 |
| Total checks | 56 |
| Checks PASSED | 56 |
| Checks FAILED | 0 |
| Articles PASS | 7/7 |
| Articles FAIL | 0 |

**ARTICLES_QA_PASS:** 7/7
**ARTICLES_QA_FAIL:** 0
**FAILED_CHECKS:** [] (none)
**CONTENT_OVERLAP:** WARNING (HUB-13-C4 vs HUB-11-C2 — same topic family, distinct angles, mutual linking — LOW cannibalization risk)
**QA_VERDICT:** **PASS**

---

## Notes for Publisher (downstream B-publish)

- All 7 articles use `alt-placeholder-*` image slots — swap to Shopify CDN URLs before publish.
- Slug `naalei-mayim-letinok-me'eize-gil` contains an apostrophe — verify Shopify handle compatibility (may need to be stripped to `naalei-mayim-letinok-meeize-gil` or hyphenated).
- HUB-13-Pillar references `kafkafim-lapautot-layam-velabreykha` and `naalei-yam-anti-hahlaka-leyeladim` — confirm both slugs publish before Pillar so internal links resolve.
- HUB-13-C6 links `/products/baby-beach-essentials` and HUB-13-C5 links `/products/baby-boy-swim-set` — verify these handles exist in Shopify before publish; if not, swap to existing equivalents.
- Publish order per plan: Pillar → C1 → C2 → C3 → C4 → C5 → C6.

**Exit condition met:** 7/7 PASS → next stage = next per Conductor plan.
