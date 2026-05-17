task_id: 20260517-230355
---
STAGE_VERDICT: **FAIL**

EVIDENCE:
- 7 articles checked × 8 qa_contract criteria = 56 checks total. **54/56 passed.**
- **Pillar, C1, C2, C3, C4:** 8/8 PASS each (C3 has a soft warning — only 1 blog-to-blog internal link; product link makes total 2, so passes).
- **C5 (Travel):** 7/8 — only **1 image placeholder** (line 19). Criterion 4 requires ≥2.
- **C6 (Dad carrier):** 7/8 — only **1 image placeholder** (line 19). Criterion 4 requires ≥2.
- No inline `style=`, no `<video>`, no `<iframe>` anywhere. All FAQs in 5–7 range. Hebrew clean. Product bridges present in all 7. FAQPage JSON-LD schema present in all 7.
- Full per-article matrix written to `output/organic/hub14-baby-carrier/hub14-qa-report.md`.

SYSTEM STATE:
- `output/organic/hub14-baby-carrier/hub14-qa-report.md` created.
- HUB-14 production state: 5/7 articles publish-ready on QA grounds; 2 articles (C5, C6) need +1 image each before re-QA.
- Pre-publish reminder logged: all `alt-placeholder-X` URLs across all 7 articles must be swapped for real Shopify CDN URLs before publish gate (informational, not a B4-QA blocker per contract wording).
- Stage cannot advance to B5 (publish) per `next_on_fail: B4` loop until C5 and C6 are fixed and re-checked.

```
ARTICLES_QA_PASS: 5/7
QA_VERDICT: FAIL
```