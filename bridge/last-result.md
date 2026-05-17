task_id: 20260517-201610
---
STAGE_VERDICT: FAIL

EVIDENCE:
- 64 checks executed (8 articles × 8 criteria). Report saved at `output/organic/batch-001-ext-qa-report.md`.
- ARTICLES_QA_PASS: 5/8 — HUB1_C5, HUB3_C5, HUB3_C6, HUB7_C6, HUB8_C6
- ARTICLES_QA_FAIL: 3/8 — HUB1_C6, HUB2_C6, HUB4_C5
- FAILED_CHECKS: all three fail on the same criterion #4 (only 1 image placeholder; contract requires ≥2). All other 7 checks (no inline styles / no hero / no video / internal links / product bridge / valid Hebrew / FAQ 5-7) pass on 100% of articles.
- Systemic note: zero actual Shopify CDN URLs in any article — expected at this stage (CDN URLs inserted at publish, not at local-markdown stage). Check #4 was evaluated as "≥2 image placeholders / image-slots reserved".

SYSTEM STATE:
- Stage A4-QA result: **FAIL** (5/8 pass)
- Per plan `next_on_fail: A1` — return to article-writing stage to add a second image placeholder to HUB1_C6, HUB2_C6, HUB4_C5, then re-run A4-QA. Fix is mechanical (one `![alt](placeholder)` block per file).
- 5 passing articles are unchanged and remain valid.
- Conductor cannot advance to B1 (HUB-16 production) until A4-QA = PASS (milestone gate).
- No Shopify writes. No bridge mutations. Only file written: `output/organic/batch-001-ext-qa-report.md`.