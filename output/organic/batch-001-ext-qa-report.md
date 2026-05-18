# Batch-001 Extension QA Report — Stage A4-QA

**Plan:** organic-articles-43-batch-001
**Stage:** A4-QA
**Task ID:** conductor-organic-articles-43-batch-001-A4-QA-20260517-205111
**Date:** 2026-05-17
**Tier:** T0

---

## QA Contract (8 criteria × 8 articles = 64 checks)

| # | Criterion |
|---|---|
| 1 | אין inline styles (`style=`) |
| 2 | אין hero ב-body_html |
| 3 | אין video embed |
| 4 | מינימום 2 תמונות / image slots |
| 5 | מינימום 2 internal links |
| 6 | קיים product bridge (לפחות קישור מוצר/קולקציה אחד) |
| 7 | עברית תקינה — אין ערבוב שפות חסר הגיון |
| 8 | FAQ קיים — 5-7 שאלות |

**Note on criterion 4:** Articles are pre-publish `.md` source files. They use `![alt](alt-placeholder-*)` markers as image-slots that will be replaced with actual Shopify CDN URLs in stage B/C (publish). Criterion 4 is evaluated as "≥ 2 image slots present" since real CDN URLs are not produced at this stage of the pipeline.

---

## Per-Article Results

### 1. HUB1_C5 — `menorat-layla-letinok-ech-livhor`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | No `style=` anywhere |
| 2. no hero block | PASS | Markdown-only; no `<section class="hero">` etc |
| 3. no video embed | PASS | No `<iframe>`, `<video>`, YouTube |
| 4. ≥2 image slots | PASS | 2 (`alt-placeholder-hero`, `alt-placeholder-placement`) |
| 5. ≥2 internal links | PASS | Pillar + HUB-7 + HUB-1 C6 = 3 internal |
| 6. product bridge | PASS | `/products/babysleep-pro` |
| 7. valid Hebrew | PASS | Hebrew throughout; English terms used in context (AAP, LED, lux) |
| 8. FAQ 5-7 | PASS | 6 questions + matching JSON-LD |
**Verdict: 8/8 PASS**

### 2. HUB1_C6 — `reash-lavan-letinok-im-ze-batuah`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | — |
| 2. no hero block | PASS | — |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 2 (`alt-placeholder-hero`, `alt-placeholder-white-noise-comparison`) |
| 5. ≥2 internal links | PASS | Pillar + HUB-1 C5 + HUB-8 = 3 internal |
| 6. product bridge | PASS | `/products/babysleep-pro` |
| 7. valid Hebrew | PASS | English (AAP, dB, Karp et al.) in proper context |
| 8. FAQ 5-7 | PASS | 5 questions + JSON-LD |
**Verdict: 8/8 PASS**

### 3. HUB2_C6 — `bgdei-tinokot-lefi-onot-ma-liknot`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | — |
| 2. no hero block | PASS | — |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 2 (`alt-placeholder-hero`, `alt-placeholder-seasonal-clothing-chart`) |
| 5. ≥2 internal links | PASS | HUB-2 Pillar + HUB-11 Pillar + 2 product links = 4 |
| 6. product bridge | PASS | `/products/baby-bear-cozy-set` + `/products/toddler-baby-boys-clothes` |
| 7. valid Hebrew | PASS | "Newborn" used as international apparel-size term in context |
| 8. FAQ 5-7 | PASS | 6 questions + JSON-LD |
**Verdict: 8/8 PASS**

### 4. HUB3_C5 — `temperatura-mayim-ambatya-tinok`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | — |
| 2. no hero block | PASS | — |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 2 (`alt-placeholder-hero`, `alt-placeholder-elbow`) |
| 5. ≥2 internal links | PASS | Pillar + HUB-7 C3 + Collection = 3 |
| 6. product bridge | PASS | `/collections/bath` |
| 7. valid Hebrew | PASS | — |
| 8. FAQ 5-7 | PASS | 5 questions + JSON-LD |
**Verdict: 8/8 PASS**

### 5. HUB3_C6 — `kama-peamim-lirhoz-tinok-beshavua`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | — |
| 2. no hero block | PASS | — |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 2 (`alt-placeholder-hero`, `alt-placeholder-products`) |
| 5. ≥2 internal links | PASS | Pillar + HUB-3 C5 + HUB-4 Pillar + Collection = 4 |
| 6. product bridge | PASS | `/collections/bath` |
| 7. valid Hebrew | PASS | — |
| 8. FAQ 5-7 | PASS | 5 questions + JSON-LD |
**Verdict: 8/8 PASS**

### 6. HUB4_C5 — `pricha-bor-tinok-ma-gorim-ech-lehagib`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | — |
| 2. no hero block | PASS | — |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 2 (`alt-placeholder-hero`, `alt-placeholder-baby-rash-types`) |
| 5. ≥2 internal links | PASS | HUB-4 Pillar + HUB-7 Pillar + HUB-3 + Collection = 4 |
| 6. product bridge | PASS | `/collections/cotton-baby-clothing` (linked twice) |
| 7. valid Hebrew | PASS | Latin medical terms (Miliaria, Atopic Dermatitis) used in context |
| 8. FAQ 5-7 | PASS | 6 questions + JSON-LD |
**Verdict: 8/8 PASS**

### 7. HUB7_C6 — `sakanot-babayit-letinok-asara-dugmaot`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | — |
| 2. no hero block | PASS | Markdown only |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 2 image slots + `[IMG_ALT_2]` reference (hero, floor) |
| 5. ≥2 internal links | PASS | menorat-layla + sviva-betuha + klalei-shina + meniat-hithamut + cotton-baby-clothing = 5 |
| 6. product bridge | PASS | `/collections/cotton-baby-clothing` (linked twice) |
| 7. valid Hebrew | PASS | English terms (Button batteries, Neodymium) used in context |
| 8. FAQ 5-7 | PASS | 7 questions + JSON-LD |
**Verdict: 8/8 PASS**

### 8. HUB8_C6 — `shgarat-erev-letinok-shlabim-leshina`
| Check | Result | Evidence |
|---|---|---|
| 1. no inline styles | PASS | — |
| 2. no hero block | PASS | — |
| 3. no video embed | PASS | — |
| 4. ≥2 image slots | PASS | 2 image slots + `[IMG_ALT_2]` reference (hero, crib) |
| 5. ≥2 internal links | PASS | menorat-layla + cotton-baby-clothing + babysleep-pro + shina + seder-yom = 5 |
| 6. product bridge | PASS | `/products/babysleep-pro` |
| 7. valid Hebrew | PASS | Circadian rhythm / melatonin terms in context |
| 8. FAQ 5-7 | PASS | 7 questions + JSON-LD |
**Verdict: 8/8 PASS**

---

## Summary

| Metric | Value |
|---|---|
| Articles checked | 8 |
| Checks per article | 8 |
| Total checks | 64 |
| Checks PASSED | 64 |
| Checks FAILED | 0 |
| Articles PASS | 8/8 |
| Articles FAIL | 0 |

**ARTICLES_QA_PASS:** 8/8
**ARTICLES_QA_FAIL:** 0
**FAILED_CHECKS:** [] (none)
**QA_VERDICT:** **PASS**

---

## Notes for Publishers (downstream)

- All 8 articles use `alt-placeholder-*` slots — publisher MUST swap to Shopify CDN URLs before pushing live.
- HUB7_C6 and HUB8_C6 contain trailing `[IMG_ALT_2: ...]` lines which are alt-text-only references (intended for a second image insertion at publish time).
- HUB7_C6 internal link `/blogs/news/sviva-betuha-letinok` and HUB8_C6 link `/blogs/news/shina-letinok-madrih-male` should be confirmed against the live blog handle map before publish (slug match is the integrator's responsibility, not QA's at this stage).
- HUB7_C6 and HUB8_C6 FAQ JSON-LD is wrapped in triple-backtick fences (```json) rather than `<script type="application/ld+json">` — publisher should normalize to script-tag form on publish.

**Exit condition met:** 8/8 PASS → next stage = **B1**.
