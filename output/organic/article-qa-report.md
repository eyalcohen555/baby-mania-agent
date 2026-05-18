# Article QA Report — STAGE-13

**Stage ID:** conductor-babymania-execution-tracks-001-STAGE-13-20260511-190803
**Approval Tier:** T0
**Created:** 2026-05-11
**Scope:** 8-condition QA over all articles in `output/organic/article-drafts/`
**Inputs:** `output/organic/article-drafts/*.md` (5 files), `output/organic/article-production-plan.md`

## QA conditions
1. H1 includes `keyword_main`
2. Internal link to product/category (`internal_link_target`)
3. FAQ section + FAQPage JSON-LD schema present
4. `alt` text present for every image placeholder
5. No obvious spelling mistakes
6. Natural Hebrew (no clunky/machine-like sentences)
7. No invalid/nonsensical words
8. Word count within planned `estimated_word_count` range

---

## Per-article verdicts

### Article 1 — Pillar — `bgdey-simha-letinok-madrikh-male.md`
**Plan target:** 1,800–2,200 words | **Actual (FIXED):** 1,873 words

| # | Check | Result |
|---|---|---|
| 1 | H1 contains `בגדי שמחה לתינוק` | ✅ PASS |
| 2 | Internal link to `/collections/clothing-all` + secondaries (`type-set`, `occ-gift`) | ✅ PASS |
| 3 | FAQ block (4 Q&A) + valid `FAQPage` JSON-LD | ✅ PASS |
| 4 | 2 image placeholders, both with `alt` lines | ✅ PASS |
| 5 | Spelling | ✅ PASS |
| 6 | Natural Hebrew | ✅ PASS |
| 7 | Invalid words | ✅ PASS |
| 8 | Word count 1,873 vs target 1,800–2,200 | ✅ FIXED — within range |

**VERDICT: PASS (FIXED)** — Expanded by ~613 words. Added: new H2 "מטריצת בגד לפי אירוע" (event×requirement matrix with תפר/בטנה/גישת חיתול), new H2 "בחירת מידה — איך לא ליפול בפח", new H2 "עונתיות בעומק" (covers transitions, חמסין, חורף ישראלי, גשם), and a 4th FAQ item ("מה ההבדל בין בגד שמחה לסט מתנה?") with matching JSON-LD entry.

---

### Article 2 — Cluster C1 — `smalot-hgygyot-letinoket-madrikh-bhira.md`
**Plan target:** 1,200–1,500 words | **Actual (FIXED):** 1,230 words

| # | Check | Result |
|---|---|---|
| 1 | H1 contains `שמלות חגיגיות לתינוקת` | ✅ PASS |
| 2 | Internal link to `/collections/gender-girl` | ✅ PASS |
| 3 | FAQ block (3 Q&A) + valid `FAQPage` JSON-LD | ✅ PASS |
| 4 | 2 image placeholders, both with `alt` lines | ✅ PASS |
| 5 | Spelling | ✅ PASS |
| 6 | Natural Hebrew | ✅ FIXED — `מוטיב צמוד` → `מותן צמוד` |
| 7 | Invalid words | ✅ PASS |
| 8 | Word count 1,230 vs target 1,200–1,500 | ✅ FIXED — within range |

**VERDICT: PASS (FIXED)** — Phrasing corrected (`מותן צמוד`). Added new H2 "איך לתאם אקססוריז לשמלה" (~180 words covering סרט, גרבונים, נעלי בד, שכבת חוץ, אבזמי שיער) and 2 additional טיפים מעשיים items (חזה check, איזון תאורה).

---

### Article 3 — Cluster C2 — `set-lebrit-mila-letinok.md`
**Plan target:** 1,200–1,500 words | **Actual (FIXED):** 1,227 words

| # | Check | Result |
|---|---|---|
| 1 | H1 contains `סט לברית מילה לתינוק` | ✅ PASS |
| 2 | Internal link to `/collections/type-set` + secondaries (`gender-boy`, `occ-gift`) | ✅ PASS |
| 3 | FAQ block (3 Q&A) + valid `FAQPage` JSON-LD | ✅ PASS |
| 4 | 2 image placeholders, both with `alt` lines | ✅ PASS |
| 5 | Spelling | ✅ FIXED — `חיתוך כניסה` → `חיתולית עטיפה` |
| 6 | Natural Hebrew | ✅ PASS |
| 7 | Invalid words | ✅ FIXED — non-term resolved |
| 8 | Word count 1,227 vs target 1,200–1,500 | ✅ FIXED — within range |

**VERDICT: PASS (FIXED)** — Phrasing corrected (`חיתולית עטיפה`). Added new H2 "טיפול בתינוק בשעות שאחרי הברית" (~180 words covering בגד גוף בחזית, מידת חיתול, מכנס רחב, שמיכה דקה, מקלחת/ניגוב, גזה/אבקה/משחות).

---

### Article 4 — Cluster C3 — `matana-letinok-hadash-bgdey-hgyga.md`
**Plan target:** 1,000–1,300 words | **Actual (FIXED):** 1,048 words

| # | Check | Result |
|---|---|---|
| 1 | H1 contains `מתנה לתינוק חדש` | ✅ PASS |
| 2 | Internal link to `/collections/occ-gift` + secondaries (`type-set`) | ✅ PASS |
| 3 | FAQ block (3 Q&A) + valid `FAQPage` JSON-LD | ✅ PASS |
| 4 | 2 image placeholders, both with `alt` lines | ✅ PASS |
| 5 | Spelling | ✅ PASS |
| 6 | Natural Hebrew | ✅ FIXED — `לא רע ... רע` → `לא בהכרח מזיקים ... נראים גרועים` |
| 7 | Invalid words | ✅ PASS |
| 8 | Word count 1,048 vs target 1,000–1,300 | ✅ FIXED — within range |

**VERDICT: PASS (FIXED)** — Phrasing tightened. Added new H2 "בונוס — מתנה שכוללת גם משהו לאמא" (~140 words on cross-recipient gifts, plus father-side tip).

---

### Article 5 — Cluster C4 — `eikh-lhalbisht-tinok-leeruah-bakayts.md`
**Plan target:** 1,000–1,300 words | **Actual (FIXED):** 1,019 words

| # | Check | Result |
|---|---|---|
| 1 | H1 contains `איך להלביש תינוק לאירוע בקיץ` | ✅ PASS |
| 2 | Internal link to `/collections/clothing-all` + cross-link to HUB-11 Pillar | ✅ PASS |
| 3 | FAQ block (3 Q&A) + valid `FAQPage` JSON-LD | ✅ PASS |
| 4 | 2 image placeholders, both with `alt` lines | ✅ PASS |
| 5 | Spelling | ✅ FIXED — `החוקי כללי` → `הכלל מוכר`; `ים ערבית` → `בקרבת ים בשעות הערב` |
| 6 | Natural Hebrew | ✅ FIXED — `יוצאים מקצב שינה` → `יוצאים מקצב השינה הרגיל` |
| 7 | Invalid words | ✅ FIXED — non-phrase resolved |
| 8 | Word count 1,019 vs target 1,000–1,300 | ✅ PASS |

**VERDICT: PASS (FIXED)** — All three textual fixes applied. No content additions needed (already within range).

---

## Summary (POST-FIX)

| Article | Slug | Words (pre → post) | Target | Verdict |
|---|---|---|---|---|
| 1 — Pillar | `bgdey-simha-letinok-madrikh-male` | 1,260 → 1,873 | 1,800–2,200 | ✅ PASS |
| 2 — C1 | `smalot-hgygyot-letinoket-madrikh-bhira` | 987 → 1,230 | 1,200–1,500 | ✅ PASS |
| 3 — C2 | `set-lebrit-mila-letinok` | 1,051 → 1,227 | 1,200–1,500 | ✅ PASS |
| 4 — C3 | `matana-letinok-hadash-bgdey-hgyga` | 937 → 1,048 | 1,000–1,300 | ✅ PASS |
| 5 — C4 | `eikh-lhalbisht-tinok-leeruah-bakayts` | 1,058 → 1,019 | 1,000–1,300 | ✅ PASS |

**ARTICLES_QA:** 5
**PASS_COUNT:** 5
**WARN_COUNT:** 0
**FAIL_COUNT:** 0

> Note on Article 5 word count: pre-fix count of 1,058 reflected the QA's measurement method (including some metadata). Post-fix measurement uses body-only count (frontmatter, JSON-LD script, and Internal links section excluded) — 1,019 words. Still within target range and structurally PASS on all 8 conditions.

## Cross-cutting observations

- **Structural integrity is strong across the board.** All 5 articles have correct H1+keyword_main, valid internal link to live collection, complete FAQ + FAQPage JSON-LD, and alt text on every image placeholder. The 7 SEO/structural checks (1–7) pass on every article with only minor textual nits on Articles 2, 3, 5.
- **Word count is the systemic gap.** 4 of 5 are under floor. Pillar (Article 1) is the only hard FAIL because the gap is wide (30%) and the Pillar role demands depth for topical-authority ranking.
- **Text-level issues are clustered in Article 5** (C4 — קיץ). The fixes are small (~3 phrases) but warrant a pass before publishing.
- **Internal link graph is consistent.** All 4 clusters link back to the Pillar; Pillar links to all 4 clusters; HUB-11 cross-bridge is present in C4 and reciprocated in the Pillar.

## Required actions before publish (POST-FIX — all applied)

| # | Action | Status |
|---|---|---|
| 1 | Pillar (Article 1): expand by ~600 words | ✅ DONE — +613 words across 3 new H2 sections + 4th FAQ |
| 2 | C1, C2, C3: expand 60–215 words each to hit floor | ✅ DONE — all within range |
| 3 | C2: fix `חיתוך כניסה` phrasing | ✅ DONE — `חיתולית עטיפה` |
| 4 | C5: fix `החוקי כללי`, `ים ערבית`, `יוצאים מקצב שינה` | ✅ DONE |
| 5 | C1: fix `מוטיב צמוד` → `מותן צמוד` | ✅ DONE |
| 6 | C3: tighten `לא רע ... רע` phrasing | ✅ DONE |

## Files touched (STAGE-14 fix pass)
- `output/organic/article-drafts/bgdey-simha-letinok-madrikh-male.md`
- `output/organic/article-drafts/smalot-hgygyot-letinoket-madrikh-bhira.md`
- `output/organic/article-drafts/set-lebrit-mila-letinok.md`
- `output/organic/article-drafts/matana-letinok-hadash-bgdey-hgyga.md`
- `output/organic/article-drafts/eikh-lhalbisht-tinok-leeruah-bakayts.md`
- `output/organic/article-qa-report.md` (this file — updated with FIXED markers)

## STAGE_VERDICT: PASS

EVIDENCE: All 5 articles now pass all 8 QA conditions. Word counts (body-only, frontmatter/script/links section excluded): 1,873 / 1,230 / 1,227 / 1,048 / 1,019 — all within their planned ranges. All previously-flagged textual issues (Article 2: `מוטיב צמוד`, Article 3: `חיתוך כניסה`, Article 4: `לא רע ... רע`, Article 5: `החוקי כללי` + `ים ערבית` + `יוצאים מקצב שינה`) have been corrected. Structural conditions (H1+keyword_main, internal link to live collection, FAQ+FAQPage JSON-LD, alt text on every image placeholder) remain ✅ across the board. Pillar JSON-LD was updated to include the new 4th FAQ entry. No publishing performed; no Shopify writes.
