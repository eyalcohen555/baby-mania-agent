task_id: 20260511-190807
---
QA report written to `output/organic/article-qa-report.md`.

---

**STAGE_VERDICT: FAIL**

**EVIDENCE:**
- 5 articles QA'd against 8 conditions each.
- All 5 pass structural checks (H1+keyword_main, internal link to live collection, FAQ+FAQPage JSON-LD schema, alt text on every image placeholder).
- 1 FAIL: Pillar `bgdey-simha-letinok-madrikh-male` is 1,260 words vs planned 1,800–2,200 (30% under floor). Must be expanded — Pillar depth is structural for HUB-12 authority.
- 4 WARN: C1 (987/1,200–1,500, 18% short), C2 (1,051/1,200–1,500, 12% short + `חיתוך כניסה` phrasing), C3 (937/1,000–1,300, 6% short), C4 (1,058 PASS on word count but 3 textual fixes: `החוקי כללי`, `ים ערבית`, `יוצאים מקצב שינה`).
- 0 PASS.

**ARTICLES_QA:** 5 | **PASS_COUNT:** 0 | **WARN_COUNT:** 4 | **FAIL_COUNT:** 1
**QA_REPORT:** `output/organic/article-qa-report.md`

**SYSTEM STATE:** HUB-12 article drafts (5 files) exist and are structurally complete (links, schema, alt, H1). Content depth is below plan across the board. Publishing gated on (a) Pillar expansion to ≥1,800 words, (b) cluster expansions to floor, (c) minor textual fixes on C2 and C4, plus the prior HUB-11 GSC submission gate noted in the production plan.