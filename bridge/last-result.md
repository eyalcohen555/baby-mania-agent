task_id: 20260511-184840
---
Plan written. No theme files touched, no `templates/index.json` modified, no push.

---

**STAGE_VERDICT:** PASS

**EVIDENCE:**
- `output/homepage/homepage-fixes-plan.md` created (single new file, only allowed output target).
- TRUST_BADGES_FIX section: includes layout/style/position decision (content-only fix, section CSS unchanged), full proposed JSON block for `bm_trust_badges_E1_2026` with 4 distinct icons (🚚🔒↩️💬) and real Hebrew descriptions replacing the leaked `"-"` defaults, plus optional Liquid hardening. `TIER_REQUIRED: T2`, `AYAL_APPROVAL: YES`.
- HERO_FIX section: new Hebrew copy (eyebrow + headline + subheadline), CTA text + primary/secondary visual spec, full proposed Liquid markup + schema additions + CSS rewrite for `sections/bm-video-hero.liquid`, plus mobile hero height reduction `100vh → 78vh` to address MEDIUM finding #5. `TIER_REQUIRED: T2`, `AYAL_APPROVAL: YES`.
- MOBILE_CHECK section: per-requirement audit table (tap target ≥ 44px → 48px met; body text ≥ 16px → flagged one `clamp(15px,…)` to lift to `clamp(16px,…)` before T2; trust strip above-the-fold verified on iPhone 14 / SE / Galaxy S22), plus a 6-step post-deploy mobile QA checklist.
- No writes to `bridge/next-task.md`, `templates/index.json`, `sections/*.liquid`, or `.env`. No push performed.

**SYSTEM STATE:**
- STAGE-7 plan artifact present at `output/homepage/homepage-fixes-plan.md` and ready for Ayal review.
- Source audit (`output/homepage/homepage-audit.md`) read-only consulted; unchanged.
- Live theme `183668179257` and `templates/index.json` on shop `a2756c-c0.myshopify.com` untouched.
- T2/Ayal approval required before any code in this plan can be executed against the live theme. LOW findings #6/#7/#8 from the audit remain deferred to a later stage.