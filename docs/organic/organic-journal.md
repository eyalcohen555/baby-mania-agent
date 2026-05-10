# Organic Content Journal
**תחום:** מערכת תוכן אורגני — HUBs, pipeline, agents, GSC
**עדכון:** אחרי כל HUB חדש, שינוי pipeline, או milestone אורגני

---

## [2026-05-10] Phase E1b Sticky Behavioral Debug — PHASEE1B_STICKY_ROOT_CAUSE_READY
Mode: READ-ONLY + PATCH PLAN | T2 plan only — no live writes
Action: Deep storefront HTML analysis + byte-offset verification of DOM timing bug
Files created:
  - docs/organic/phaseE1b-sticky-behavioral-debug.md
  - output/tags/phaseE1b-sticky-behavioral-debug.json
  - output/tags/phaseE1b-sticky-proposed-patch.md
Status: PHASEE1B_STICKY_ROOT_CAUSE_READY — awaiting T2 approval to apply

ROOT CAUSE CONFIRMED:
  bm-sticky-bar.liquid inline <script> (no defer) runs at char 80,957 in HTML.
  main-product section renders at char 137,957 (57,000 chars later).
  querySelector('.product-form__buttons') = null → if (!target) return → early exit.
  IntersectionObserver NEVER created → sticky permanently hidden on all products.
  NOT a CSS/z-index/iOS/viewport issue — pure DOM timing bug.

RULED OUT: CSS conflict (live bm-store-main-overrides.liquid has no sticky CSS),
  duplicate ID (only 1 id=bm-sticky-bar in live HTML), z-index, iOS safe-area,
  short viewport.

PROPOSED FIX (T2 — not applied):
  Option A: Wrap observer in initStickyObserver(), add readyState check +
  DOMContentLoaded listener. 8 lines changed, no HTML/CSS/schema changes.
  threshold: 0.1 (was 0).

EASYSLEEP/TEMPIO: Still need separate T3 fix (main-product disabled — different issue).

---

## [2026-05-10] Phase E1 Homepage Quick Wins — PHASEE1_HOMEPAGE_QUICK_WINS_PASS
Mode: LIVE | T1 approved | Theme: 183668179257 | Template: templates/index.json
Action: 6 T1 changes applied to homepage template
Files created:
  - docs/organic/phaseE1-homepage-quick-wins-report.md
  - output/tags/phaseE1-homepage-quick-wins-backup.json
  - output/tags/phaseE1-homepage-quick-wins-dry-run.md/json
  - output/tags/phaseE1-homepage-quick-wins-rollback-plan.md
  - output/tags/phaseE1-homepage-quick-wins-verify.md/json
  - output/tags/phaseE1-sticky-reality-audit.md/json
  - scripts/phaseE1_homepage_quick_wins.py
Status: PHASEE1_HOMEPAGE_QUICK_WINS_PASS — all 6 writes PASS

Homepage changes (all verified PASS):
  E1-1a: featured_collection products_to_show 25 → 8
  E1-1b: featured_collection_FXYxk4 products_to_show 25 → 8
  E1-2:  image_banner_WY4jhi disabled (blank section removed from render)
  E1-3:  rich_text_bWQ9mf disabled (empty heading removed)
  E1-4:  rich_text_xKGEmA heading "הנמכרים ביותר" → "מוצר השבוע"
  E1-5:  bm-trust-badges section added after hero (4 badges: משלוח/תשלום/החזרות/שירות)
  E1-6:  show_rating — NO CHANGE (no product reviews found)

Sticky audit (READ-ONLY):
  - product.clothing.json: HTML CORRECT — bm-sticky-bar ✅, .product-form__buttons ✅, IntersectionObserver ✅
  - Clothing sticky broken on mobile = BEHAVIORAL root cause (NOT structural) — T2 DevTools investigation needed
  - EasySleep + Tempio: BROKEN — main-product section disabled → .product-form__buttons not in DOM — T3 fix needed
  - product.test.json: BROKEN — no bm-sticky-bar section

---

## [2026-05-10] Phase E Navigation + Homepage Fix Plan — READ-ONLY COMPLETE
Mode: READ-ONLY | T0 | No Shopify writes | No theme writes
Action: Full fix plan for navigation restructure + homepage quick wins, based on Phase D audit
Files created:
  - docs/organic/navigation-homepage-fix-plan.md
  - output/tags/navigation-homepage-fix-plan.json
Status: NAVIGATION_HOMEPAGE_FIX_PLAN_READY

Key findings:
- Navigation: 17 top-level items → proposed 6-item premium structure (T1)
- Seasonal: Replace hardcoded קיץ 2026 with permanent מבצעים label (T1)
- Hero: bm-video-hero has no heading/CTA schema — fix via Liquid edit (T2)
- Homepage T1 wins: reduce products_to_show 25→8, add bm-trust-badges, rename dup heading, disable 2 empty sections
- Sticky bar root cause: .product-form__buttons = null on EasySleep + Tempio (main-product disabled in templates)
- Fix: Enable main-product section on product.easy-sleep.json + product.tempio.json (T3)
- Execution order: E1 (T1 homepage) → E2 (T1 nav) → E3 (T2 hero) → E4 (T3 structural)

---

## [2026-05-10] Phase D Homepage UX Technical Audit — READ-ONLY COMPLETE
Mode: READ-ONLY | T0 | No Shopify writes | No theme writes | No product writes
Action: Full structural audit of homepage — 8 tasks completed
Files created:
  - docs/organic/phaseD-homepage-ux-technical-audit.md
  - output/tags/phaseD-homepage-ux-technical-audit.json
  - output/tags/phaseD_index.json (raw homepage template for reference)
Status: PHASED_HOMEPAGE_UX_TECHNICAL_AUDIT_READY

Key findings:
- Template: templates/index.json | Theme: Copy of Dawn new (183668179257) | 17 sections
- Hero: bm-video-hero — 2 videos split side-by-side (NOT carousel), NO heading support in schema, 2 nav CTAs only
- Duplicate heading: "הנמכרים ביותר" appears in rich_text_xKGEmA + rich_text_itPixN (positions 6 and 8)
- Subscription text: NOT from theme Liquid/locale files, NOT from selling plans (0 groups), source = third-party app (script_tags/apps inaccessible via current API scope)
- Performance: 4 videos (3 simultaneous on desktop), ~53 product cards, ~65 images, lazy loading only partial
- Trust signals: bm-trust-badges.liquid EXISTS in theme but NOT on homepage — needs placement only (T1)
- EasySleep: PID 10085913231673, options דגם (450/300מ"ל) + צבע (White/Brown) = valid real variants, no subscriptions
- Navigation (post Phase A): 17 top-level items, gifts link = /collections/מארזי-מתנה ✅, structure documented as UX debt
- Testimonials section IS on homepage (position 14) — but delivery/payment/returns signals missing

---

## [2026-05-10] Phase A Live Issues Fix — PHASEA_LIVE_ISSUES_FIX_PASS
Mode: LIVE | T3 approval: Ayal — 2026-05-10
Action: 4 targeted fixes applied (A1 pajama, A2 navigation, A3 occ-gift title, A4 missing tag)
Files created:
  - docs/organic/phaseA-live-issues-fix-report.md
  - output/tags/phaseA-live-fix-backup.json
  - output/tags/phaseA-live-fix-dry-run.md/json
  - output/tags/phaseA-live-fix-rollback-plan.md/json
  - output/tags/phaseA-live-fix-verify.md/json
  - output/tags/phaseA-product-9605887689017-readonly-report.md/json
  - scripts/phaseA_live_fix.py
Status: PHASEA_LIVE_ISSUES_FIX_PASS — all 4 writes PASS, A5 READ_ONLY_COMPLETE

Changes:
- A1: PID 9606694306105 — title fixed (encoding corruption → "סט פיג'מה ארוכה לילדים"), gender-girl→gender-neutral
- A2: main-menu "מתנות לתינוק" → /collections/מארזי-מתנה (was /collections/occ-gift)
- A3: occ-gift collection title: "מתנות לתינוק" → "בגדים שמתאימים למתנה" (handle unchanged)
- A4: PID 9096636825913 — occ-gift tag added (was empty)
- A5: PID 9605887689017 — read-only check, REVIEW_ONLY findings, no writes

---

## [2026-05-10] Tag Taxonomy Expansion — READ-ONLY Planning
Mode: PLANNING_ONLY | No Shopify writes
Action: Full tag taxonomy expansion proposal created
Files created:
  - docs/organic/tag-taxonomy-expansion-proposal.md
  - output/tags/tag-taxonomy-expansion-audit.json
  - output/tags/shoes-taxonomy-proposal.md
  - output/tags/shoes-image-review-spec.md
  - output/tags/review-only-triage-plan.md
  - output/tags/future-smart-collections-proposal.md
Status: PROPOSAL_READY — awaiting approval before any live writes

Key findings:
- 218 products already live-tagged (clothing: type-* + gender-* + occ-*)
- ~133 REVIEW_ONLY products pending manual triage
- ~65 shoe products blocked (pending EU size mapping decision + taxonomy approval)
- 6 Smart Collections live (gender-girl/boy, type-set/romper, occ-gift, clothing-all)
- Shoe taxonomy proposed: 7 tags (sneakers/sandals/boots/first-step/elegant/soft-sole/review-only)
- Image review agent spec defined (input/output schema + vision prompt)
- REVIEW_ONLY triage plan: 5 categories + batch workflow (20/batch)
- Future collections roadmap: 13 candidates, summer-2024 handle assessed
- No Shopify writes performed

---

## DATE: 2026-05-08
## TASK: Layer 6 Closure Audit
## SCOPE: READ-ONLY — Full Tag System + Navigation Foundation closure audit
## WHAT CHANGED:
- Layer 6 Closure Audit performed. 10/10 closure checks PASS
- Confirmed: 218 products live-tagged, SAFE pool exhausted, 6 Smart Collections exist
- Confirmed: main-menu updated (Phase 8F, 17 items), no open rollbacks, no age-* tags
- QA Contract (layer7-live-tagging-qa-contract.md v1.0) active throughout all Phase 7B+ batches
- Batch 10 false positive lessons documented (7 keyword gap categories)
- Backlog formally defined: REVIEW_ONLY / shoes / EU-size / FP-hardening / Phase 8H
- verdict: LAYER6_COMPLETE_SAFE_SYSTEM_CLOSED
## FILES CREATED:
- docs/organic/layer6-closure-report.md
- output/tags/layer6-closure-audit.json
## DOCS UPDATED:
- docs/organic/מצב-הפרויקט-האורגני.md (v5.20)
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- Layer 6 officially closed. No Shopify changes.
- Next work: REVIEW_ONLY pool manual review OR EU size mapping OR new HUB planning
## OPEN ISSUES (backlog, not blockers):
- REVIEW_ONLY ~133 products: manual Shopify admin review required
- 2 Batch-10 REVIEW_ONLY PIDs: 9096636825913, 9605887689017
- Shoes/sandals: blocked until EU size mapping
- EU size mapping: blocked until Ayal approval
- FP keyword hardening: update FALSE_POSITIVE_KW list in scanner
- Phase 8H: Navigation Visual UX Polish (future)
## NEXT STEP: Ayal to decide: REVIEW_ONLY pool review / EU size mapping / new HUB

---

## DATE: 2026-05-07
## TASK: Layer 7 Phase 7C — Batch 10 Revised Live Write
## SCOPE: Layer 7 — Shopify live tag write (1 product, post business audit)
## WHAT CHANGED:
- Batch 10 Revised live write executed: 1/1 PASS (PHASE7C_LIVE_BATCH10_REVISED_PASS)
- Business audit of 12 batch10 candidates: 1 APPROVE / 9 REJECT_FALSE_POSITIVE / 2 REVIEW_ONLY
- False positive rate 75% — scan keyword gaps documented (swimsuit, brush, potty, postpartum, formula, שמיכות)
- PUT HTTP 200 + GET verify PASS. 11/11 QA checks PASS
- PID 9687563338041 (שלוש סטים של עונת מעבר): type-set + gender-girl written
- 0 products excluded. 0 Hebrew month normalizations. 0 rollback
- Shopify live total: 218 products
## FILES TOUCHED:
- output/tags/phase7c-batch10-plan.json (READ-ONLY plan)
- output/tags/phase7c-batch10-business-audit.json (audit)
- output/tags/phase7c-batch10-business-audit.md
- output/tags/phase7c-batch10-revised-plan.json
- output/tags/phase7c-batch10-revised-plan.md
- output/tags/phase7c-live-batch10-revised-backup.json
- output/tags/phase7c-live-batch10-revised-dry-run.json
- output/tags/phase7c-live-batch10-revised-dry-run.md
- output/tags/phase7c-live-batch10-revised-rollback-plan.md
- output/tags/phase7c-live-batch10-revised-verify.json
- output/tags/phase7c-live-batch10-revised-verify.md
- docs/organic/מצב-הפרויקט-האורגני.md (v5.19)
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- PID 9687563338041 now has type-set + gender-girl tags
- Shopify live tagged products: 218 (was 217)
- Phase 7C Batch 10 pool exhausted — all SAFE candidates processed
## OPEN ISSUES:
- 2 REVIEW_ONLY products (9096636825913, 9605887689017): require manual Shopify admin review
- EU Shoe Size mapping: blocked until Ayal approves
- REVIEW_ONLY 133 products: blocked until manual review
- False positive keyword list needs update before next scan
## NEXT STEP: REVIEW_ONLY pool manual review OR new scan with updated false-positive list

---

## DATE: 2026-05-07
## TASK: Layer 7 Phase 7C — Batch 9 Live Write
## SCOPE: Layer 7 — Shopify live tag write (20 products)
## WHAT CHANGED:
- Batch 9 live write executed: 20/20 PASS (PHASE7C_LIVE_BATCH9_PASS)
- DRY_RUN_PASS → PHASE7C_LIVE_BATCH9_PASS → POST_VERIFY_PASS — all 20/20
- 0 products excluded (no shoe titles; sweater 10011383202105 not in plan)
- types: set:20 only
- Hebrew month normalization: 1 product (9688955978041: 3 tags — 6-12/12-18/18-24 חודש→חודשים)
- Shopify live total: 217 products
- Auth fix: static SHOPIFY_ACCESS_TOKEN expired — switched to client_credentials OAuth flow
- Scripts: phase7c_live_batch9.py + phase7c_live_batch9_verify.py (use _fetch_oauth_token())
## FILES TOUCHED:
- scripts/phase7c_live_batch9.py (created, OAuth client_credentials flow)
- scripts/phase7c_live_batch9_verify.py (created)
- scripts/phase7c_batch9_plan.py (created in prior session)
- output/tags/phase7c-live-batch9-backup.json
- output/tags/phase7c-live-batch9-dry-run.json
- output/tags/phase7c-live-batch9-dry-run.md
- output/tags/phase7c-live-batch9-rollback-plan.md
- output/tags/phase7c-live-batch9-verify.json
- output/tags/phase7c-live-batch9-verify.md
- output/tags/shopify-auth-flow-audit.json
- output/tags/shopify-auth-flow-audit.md
- docs/organic/מצב-הפרויקט-האורגני.md (v5.18, includes batch9 plan + live)
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- 20 Shopify products now have type-set (and gender/occ where applicable) tags
- Shopify live tagged products: 217 (was 197)
## OPEN ISSUES:
- Phase 7C Batch 10+: ~4 SAFE candidates remaining (type-set only), T3 approval needed
- EU Shoe Size mapping: blocked until Ayal approves
- REVIEW_ONLY 135 products: blocked until manual review
## NEXT STEP: Phase 7C Batch 10 planning or REVIEW_ONLY pool review

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Batch 9 Planning (READ-ONLY)
## SCOPE: Layer 7 — plan only, no Shopify writes
## WHAT CHANGED:
- Batch 9 plan created: 20 candidates selected (READY_FOR_PHASE7C_BATCH9_T3_APPROVAL)
- already_written_batch12345678=146 excluded; t3_excluded=1 (sweater 10011383202105)
- types: set:20 only (all other pools exhausted)
- false_positive_blkd=11 (added שמיכ/ספינר blockers + סניקרס to shoe keywords)
- 1 product needs Hebrew month normalization (9688955978041: 3 singular tags)
- All 20 safety checks PASS; Shopify writes: NONE
- Shopify live total unchanged: 197 products
## FILES TOUCHED:
- scripts/phase7c_batch9_plan.py (created)
- output/tags/phase7c-batch9-plan.md (created)
- output/tags/phase7c-batch9-plan.json (created)
- docs/organic/מצב-הפרויקט-האורגני.md (v5.17)
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- 0 Shopify writes — read-only planning pass
- Next: T3 approval from Ayal → Batch 9 live write
## OPEN ISSUES:
- Phase 7C Batch 9 live: ~24 SAFE candidates remaining (type-set only), T3 approval needed
- EU Shoe Size mapping: blocked until Ayal approves
- REVIEW_ONLY 135 products: blocked until manual review
## NEXT STEP: T3 approval → Phase 7C Live Batch 9

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Batch 8 Live Write
## SCOPE: Layer 7 — Shopify live tag write (20 products)
## WHAT CHANGED:
- Batch 8 live write executed: 20/20 PASS (PHASE7C_LIVE_BATCH8_PASS)
- DRY_RUN_PASS → PHASE7C_LIVE_BATCH8_PASS → POST_VERIFY_PASS — all 20/20
- 0 products excluded (no shoe titles; sweater 10011383202105 not in plan)
- types: set:20 only
- 0 Hebrew month normalizations needed
- Shopify live total: 197 products
- New flag added: --exclude-product-id in live scripts
- Scripts: phase7c_live_batch8.py + phase7c_live_batch8_verify.py
## FILES TOUCHED:
- scripts/phase7c_live_batch8.py (created, added --exclude-product-id flag)
- scripts/phase7c_live_batch8_verify.py (created)
- output/tags/phase7c-live-batch8-backup.json
- output/tags/phase7c-live-batch8-dry-run.json
- output/tags/phase7c-live-batch8-dry-run.md
- output/tags/phase7c-live-batch8-rollback-plan.md
- output/tags/phase7c-live-batch8-verify.json
- output/tags/phase7c-live-batch8-verify.md
- docs/organic/מצב-הפרויקט-האורגני.md (v5.16, includes batch8 plan + live)
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- 20 Shopify products now have type-set (and gender/occ where applicable) tags
- Shopify live tagged products: 197 (was 177)
## OPEN ISSUES:
- Phase 7C Batch 9+: ~27 SAFE candidates remaining (type-set only), T3 approval needed
- EU Shoe Size mapping: blocked until Ayal approves
- REVIEW_ONLY 135 products: blocked until manual review
## NEXT STEP: Phase 7C Batch 9 planning (T3 approval needed)

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Batch 8 Plan (READ-ONLY)
## SCOPE: Layer 7 — READ-ONLY planning, no Shopify writes
## WHAT CHANGED:
- Batch 8 plan created: 20 SAFE type-set candidates selected
- already_written_batch1234567=126 (19 batch7 PIDs added to exclusion list)
- t3_excluded=1: sweater 10011383202105 (requires explicit re-approval)
- false_positive_blkd expanded to 9: added 'טטרה' blocker (muslin bib sets)
- 0 products need Hebrew month normalization
- SAFE candidates in pool: 47 (type-set only, other pools exhausted)
- All 20 candidates: type-set only
- All safety checks PASS: no age-*, no type collision, no gender collision, no forbidden tags
- Verdict: READY_FOR_PHASE7C_BATCH8_T3_APPROVAL
## FILES TOUCHED:
- scripts/phase7c_batch8_plan.py (created)
- output/tags/phase7c-batch8-plan.md (created)
- output/tags/phase7c-batch8-plan.json (created)
- docs/organic/מצב-הפרויקט-האורגני.md (v5.15)
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- No Shopify changes (GET only)
- Shopify live tagged products: 177 (unchanged)
## OPEN ISSUES:
- Phase 7C Batch 8+: 47 SAFE candidates remaining (type-set only), T3 approval needed
- EU Shoe Size mapping: blocked until Ayal approves
- REVIEW_ONLY 135 products: blocked until manual review
## NEXT STEP: Phase 7C Batch 8 live write (T3 approval needed from Ayal)

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Batch 7 Live Write
## SCOPE: Layer 7 — Shopify live tag write (19 products)
## WHAT CHANGED:
- Batch 7 live write executed: 19/19 PASS (PHASE7C_LIVE_BATCH7_PASS)
- DRY_RUN_PASS → PHASE7C_LIVE_BATCH7_PASS → POST_VERIFY_PASS — all 19/19
- 1 product excluded per T3: סוודר סרוג לתינוקות (10011383202105) — not a set outfit
- types: set:19 only
- Hebrew month normalization: 1 product (9179173617977) — 4 singular tags normalized
  (0-3 חודש, 3-6 חודש, 6-12 חודש, 12-18 חודש → חודשים)
- Shopify live total: 177 products
- New flag added: --exclude-title in live scripts
- Scripts: phase7c_live_batch7.py + phase7c_live_batch7_verify.py
## FILES TOUCHED:
- scripts/phase7c_live_batch7.py (created, added --exclude-title flag)
- scripts/phase7c_live_batch7_verify.py (created)
- output/tags/phase7c-live-batch7-backup.json
- output/tags/phase7c-live-batch7-dry-run.json
- output/tags/phase7c-live-batch7-dry-run.md
- output/tags/phase7c-live-batch7-rollback-plan.md
- output/tags/phase7c-live-batch7-verify.json
- output/tags/phase7c-live-batch7-verify.md
- docs/organic/מצב-הפרויקט-האורגני.md (v5.14, includes batch7 plan + live)
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- 19 Shopify products now have type/gender tags
- Shopify live tagged products: 177 (was 158)
## OPEN ISSUES:
- Phase 7C Batch 8+: ~48 SAFE candidates remaining (type-set only), T3 approval needed
- EU Shoe Size mapping: blocked until Ayal approves
- REVIEW_ONLY 135 products: blocked until manual review
## NEXT STEP: Phase 7C Batch 8 planning (T3 approval needed)

---

## JOURNAL TEMPLATE

```
## DATE: YYYY-MM-DD
## TASK: שם המשימה
## SCOPE: organic component
## WHAT CHANGED:
## FILES TOUCHED:
## SYSTEM IMPACT:
## OPEN ISSUES:
## NEXT STEP:
```

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Batch 7 READ-ONLY Planning
## SCOPE: Layer 7 — READ-ONLY planning — no Shopify writes
## WHAT CHANGED:
- Batch 7 plan created: 20 SAFE candidates selected (set:20 — all other types exhausted)
- Expanded NOT_SET_TITLE_KW blockers: added כובע/יחידת/מארז/מברשות/מתלה/ניקוי
- 8 false-positive products blocked (was 1 prev. batches)
- 107 already-written PIDs (batch1/2/3/4/5/6) explicitly excluded
- 68 SAFE new candidates in pool
- 1 product needs Hebrew month normalization: 9179173617977 (4 singular tags)
- All safety checks PASS: 0 flags, 0 age-* tags, 0 type collision, 0 overlap with prev batches
## FILES TOUCHED:
- scripts/phase7c_batch7_plan.py (created, expanded NOT_SET_TITLE_KW)
- output/tags/phase7c-batch7-plan.json
- output/tags/phase7c-batch7-plan.md
- docs/organic/מצב-הפרויקט-האורגני.md (v5.13)
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- No Shopify writes — planning only
## OPEN ISSUES:
- Phase 7C Batch 7 T3 approval needed from Ayal before live write
- ~48 SAFE candidates remaining after batch7 selection (all type-set)
- 1 product (9179173617977) needs Hebrew month normalization in live stage
## NEXT STEP: T3 approval from Ayal → Phase 7C Batch 7 live write

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Batch 6 Live Write
## SCOPE: Layer 7 — Shopify live tag write (20 products)
## WHAT CHANGED:
- Batch 6 live write executed: 20/20 PASS (PHASE7C_LIVE_BATCH6_PASS)
- DRY_RUN_PASS → PHASE7C_LIVE_BATCH6_PASS → POST_VERIFY_PASS — all 20/20
- types: dress:4, set:16
- 0 Hebrew month normalizations needed
- Shopify live total: 158 products
- Scripts: phase7c_live_batch6.py + phase7c_live_batch6_verify.py
- Output files: output/tags/phase7c-live-batch6-*.json/md
## FILES TOUCHED:
- scripts/phase7c_live_batch6.py (executed)
- scripts/phase7c_live_batch6_verify.py (executed)
- output/tags/phase7c-live-batch6-backup.json
- output/tags/phase7c-live-batch6-dry-run.json
- output/tags/phase7c-live-batch6-dry-run.md
- output/tags/phase7c-live-batch6-rollback-plan.md
- output/tags/phase7c-live-batch6-verify.json
- output/tags/phase7c-live-batch6-verify.md
- docs/organic/מצב-הפרויקט-האורגני.md (v5.12)
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- 20 Shopify products now have type/gender tags
- Shopify live tagged products: 158 (was 138)
## OPEN ISSUES:
- Phase 7C Batch 7+: ~75 SAFE candidates remaining (mostly type-set), T3 approval needed
- EU Shoe Size mapping: blocked until Ayal approves
- REVIEW_ONLY 135 products: blocked until manual review
## NEXT STEP: Phase 7C Batch 7 planning (T3 approval needed)

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Batch 6 READ-ONLY Planning
## SCOPE: Layer 7 — READ-ONLY planning — no Shopify writes
## WHAT CHANGED:
- Batch 6 plan created: 20 SAFE candidates selected (dress:4, set:16, romper:0, bodysuit:0)
- romper + bodysuit pools fully exhausted — only dress and set remain in SAFE pool
- 87 already-written PIDs (batch1/2/3/4/5) explicitly excluded
- 95 SAFE new candidates in pool; 0 need Hebrew month normalization
- All safety checks PASS: 0 flags, 0 age-* tags, 0 type collision, 0 overlap with prev batches
## FILES TOUCHED:
- scripts/phase7c_batch6_plan.py (created)
- output/tags/phase7c-batch6-plan.json
- output/tags/phase7c-batch6-plan.md
- docs/organic/מצב-הפרויקט-האורגני.md (v5.11)
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- No Shopify writes — planning only
## OPEN ISSUES:
- Phase 7C Batch 6 T3 approval needed from Ayal before live write
- ~75 SAFE candidates remaining after batch6 selection (mostly set)
## NEXT STEP: T3 approval from Ayal → Phase 7C Batch 6 live write

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Batch 5 Live Write
## SCOPE: Layer 7 — Shopify live tag write (20 products)
## WHAT CHANGED:
- Batch 5 live write executed: 20/20 PASS (PHASE7C_LIVE_BATCH5_PASS)
- DRY_RUN_PASS → PHASE7C_LIVE_BATCH5_PASS → POST_VERIFY_PASS — all 20/20
- types: dress:5, set:6, romper:4, bodysuit:5
- 0 Hebrew month normalizations needed (all products already had plural or no month tags)
- Shopify live total: 138 products
- Scripts: phase7c_live_batch5.py + phase7c_live_batch5_verify.py
- Output files: output/tags/phase7c-live-batch5-*.json/md
## FILES TOUCHED:
- scripts/phase7c_live_batch5.py (executed)
- scripts/phase7c_live_batch5_verify.py (executed)
- output/tags/phase7c-live-batch5-backup.json
- output/tags/phase7c-live-batch5-dry-run.json
- output/tags/phase7c-live-batch5-dry-run.md
- output/tags/phase7c-live-batch5-rollback-plan.md
- output/tags/phase7c-live-batch5-verify.json
- output/tags/phase7c-live-batch5-verify.md
- docs/organic/מצב-הפרויקט-האורגני.md (v5.10)
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- 20 Shopify products now have type/gender tags
- Shopify live tagged products: 138 (was 118)
## OPEN ISSUES:
- Phase 7C Batch 6+: ~95 SAFE candidates remaining, T3 approval needed
- EU Shoe Size mapping: blocked until Ayal approves
- REVIEW_ONLY 135 products: blocked until manual review
## NEXT STEP: Phase 7C Batch 6 planning (T3 approval needed)

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Batch 5 READ-ONLY Planning
## SCOPE: Layer 7 — READ-ONLY planning — no Shopify writes
## WHAT CHANGED:
- Batch 5 plan created: 20 SAFE candidates selected (dress:5, set:6, romper:4, bodysuit:5)
- romper pool had only 4 remaining candidates after batch1/2/3/4 — round-robin fill gave extra set slot
- 67 already-written PIDs (batch1/2/3/4) explicitly excluded
- 115 SAFE new candidates in pool; 0 need Hebrew month normalization
- All safety checks PASS: 0 flags, 0 age-* tags, 0 type collision, 0 overlap with prev batches
## FILES TOUCHED:
- scripts/phase7c_batch5_plan.py (created)
- output/tags/phase7c-batch5-plan.md (created)
- output/tags/phase7c-batch5-plan.json (created)
- docs/organic/מצב-הפרויקט-האורגני.md (v5.9)
## SYSTEM IMPACT: READ-ONLY — no Shopify writes
## OPEN ISSUES: awaiting T3 approval from Ayal before batch5 live write
## NEXT STEP: T3 approval → Phase 7C Batch 5 live write

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Live Batch 4 (T3 approved)
## SCOPE: Layer 7 — live Shopify tag writes + Hebrew month normalization
## WHAT CHANGED:
- 20 products tagged live: dress:5, set:5, romper:5, bodysuit:5
- DRY_RUN_PASS (20/20) → PHASE7C_LIVE_BATCH4_PASS (20/20) → POST_VERIFY_PASS (20/20)
- Hebrew month normalization applied on 2 products:
  9179173191993: 5 tags normalized (0-3/3-6/6-12/12-18/18-24 חודש → חודשים)
  9688955912505: 3 tags normalized (6-12/12-18/18-24 חודש → חודשים)
- PUT HTTP 200 + GET verify PASS per product; אין rollback; אין age-* tags
- Shopify live tagged total: 98 → 118 products
## FILES TOUCHED:
- scripts/phase7c_live_batch4.py (created)
- scripts/phase7c_live_batch4_verify.py (created)
- output/tags/phase7c-live-batch4-backup.json
- output/tags/phase7c-live-batch4-dry-run.json / .md
- output/tags/phase7c-live-batch4-rollback-plan.md
- output/tags/phase7c-live-batch4-verify.json / .md (post_verify appended)
- docs/organic/מצב-הפרויקט-האורגני.md (v5.8)
## SYSTEM IMPACT: 20 Shopify products tagged; 8 Hebrew month tags normalized
## OPEN ISSUES: ~95 SAFE candidates remain; Phase 7C Batch 5 needs T3 approval
## NEXT STEP: Phase 7C Batch 5 planning (T3 approval required)

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Batch 4 READ-ONLY Planning
## SCOPE: Layer 7 — READ-ONLY planning — no Shopify writes
## WHAT CHANGED:
- Batch 4 plan created: 20 SAFE candidates selected (dress:5, set:5, romper:5, bodysuit:5)
- 47 already-written PIDs (batch1/2/3) explicitly excluded via hardcoded list
- 135 SAFE new candidates in pool; round-robin selection used
- All safety checks PASS: 0 flags, 0 age-* tags, 0 type collision, 0 overlap with batch1/2/3
## FILES TOUCHED:
- scripts/phase7c_batch4_plan.py (created)
- output/tags/phase7c-batch4-plan.md (created)
- output/tags/phase7c-batch4-plan.json (created)
- docs/organic/מצב-הפרויקט-האורגני.md (v5.7)
## SYSTEM IMPACT: READ-ONLY — no Shopify writes
## OPEN ISSUES: awaiting T3 approval from Ayal before batch4 live write
## NEXT STEP: T3 approval → Phase 7C Batch 4 live write

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Live Batch 3 (T3 approved)
## SCOPE: Layer 7 — live Shopify tag writes
## WHAT CHANGED:
- 20 products tagged live: dress:5, set:5, romper:5, bodysuit:5
- DRY_RUN_PASS (20/20) → PHASE7C_LIVE_BATCH3_PASS (20/20) → POST_VERIFY_PASS (20/20)
- PUT HTTP 200 + GET verify PASS per product; אין rollback; אין age-* tags
- Shopify live tagged total: 78 → 98 products
## FILES TOUCHED:
- scripts/phase7c_live_batch3.py (created)
- scripts/phase7c_live_batch3_verify.py (created)
- output/tags/phase7c-live-batch3-backup.json
- output/tags/phase7c-live-batch3-dry-run.json / .md
- output/tags/phase7c-live-batch3-rollback-plan.md
- output/tags/phase7c-live-batch3-verify.json / .md (post_verify appended)
- docs/organic/מצב-הפרויקט-האורגני.md (v5.6)
## SYSTEM IMPACT: 20 Shopify products now carry Layer 7 taxonomy tags
## OPEN ISSUES: ~160 SAFE candidates remain; Phase 7C Batch 4 needs T3 approval
## NEXT STEP: Phase 7C Batch 4 planning (T3 approval required)

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Batch 3 READ-ONLY Planning
## SCOPE: Layer 7 — READ-ONLY planning — no Shopify writes
## WHAT CHANGED:
- scripts/phase7c_batch3_plan.py created — balanced round-robin selector (5 per type)
- 20 candidates selected from remaining SAFE pool: dress:5, set:5, romper:5, bodysuit:5
- 1 false-positive blocked: "בגד ים" (swimwear) matched type-set via "set" in handle → NOT_SET_TITLE_KW
- "suit"→type-set blocked when title contains "אוברול" (romper title, not a set product)
- Short Hebrew keyword "סט" uses word-boundary matching to avoid substring false-positives (e.g. "סטייסי")
- All 20 candidates passed batch-level safety checks (age-*/type-collision/gender-collision/forbidden)
- Shopify writes: NONE
- verdict: READY_FOR_PHASE7C_BATCH3_T3_APPROVAL
## FILES TOUCHED:
- scripts/phase7c_batch3_plan.py (new)
- output/tags/phase7c-batch3-plan.md (new)
- output/tags/phase7c-batch3-plan.json (new)
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- No Shopify state change
- Batch 3 plan ready for T3 review
## OPEN ISSUES:
- EU Shoe Size mapping — חסום עד אישור אייל
- REVIEW_ONLY 135 products — manual review required
## NEXT STEP:
- T3 approval מאייל → Phase 7C Batch 3 live write (max 20 products)

---

## DATE: 2026-05-06
## TASK: Layer 7 Phase 7C — Long Run Tagging Completion Plan
## SCOPE: Layer 7 — READ-ONLY planning — no Shopify writes
## WHAT CHANGED:
- Long run tagging completion plan generated from existing JSON state files
- Current state: 78 products live tagged, ~180 SAFE candidates remaining (207 total − 27 written)
- REVIEW_ONLY: 135 products (excluded, manual review required)
- Blocked: shoes/sandals/sneakers (EU-size mapping approval required)
- Recommended strategy: max 20 per batch, T3 approval per batch
- Batch order: dress/set/romper/bodysuit → remaining clothing → REVIEW_ONLY after review → shoes after EU-size
- Shopify writes: NONE
- verdict: READY_FOR_PHASE7C_LONG_RUN_REVIEW
## FILES TOUCHED:
- output/tags/phase7c-long-run-tagging-plan.md (new)
- output/tags/phase7c-long-run-tagging-plan.json (new)
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Plan document available for T3 approval review
- No Shopify state change
## OPEN ISSUES:
- EU Shoe Size mapping — חסום עד אישור אייל
- REVIEW_ONLY 135 products — manual review required
## NEXT STEP:
- T3 approval מאייל → Phase 7C Batch 3 READ-ONLY plan → Batch 3 live

---

## DATE: 2026-05-05
## TASK: Layer 7 Phase 7C — Live Batch 2 — hat + coat (T3 approved by Ayal)
## SCOPE: Layer 7 — Live tag write — 7 products (hat:4, coat:3) — Shopify PUT + verify
## WHAT CHANGED:
- 7 products tagged in Shopify live (PUT HTTP 200 + GET verify PASS per product)
- 4 false-positive products excluded: מגבת (towel), תיק (bag), משפך (funnel) matched "כובע" keyword but are not hats — false-positive blocker added to classifier
- types written: hat:4, coat:3
- gender written: girl:5, boy:1, none:1
- occ tags written: occ-gift×5, occ-everyday×1, occ-seasonal×2
- post-run verify: 7/7 PASS (GET re-check)
- rollback: NOT triggered
- Shopify live: YES (78 products total, up from 71)
- false-positive blocker (NOT_HAT_TITLE_KW) added to batch2 classifier script
## FILES TOUCHED:
- scripts/phase7c_live_batch2.py
- scripts/phase7c_live_batch2_verify.py
- output/tags/phase7c-live-batch2-backup.json
- output/tags/phase7c-live-batch2-dry-run.md
- output/tags/phase7c-live-batch2-dry-run.json
- output/tags/phase7c-live-batch2-rollback-plan.md
- output/tags/phase7c-live-batch2-verify.md
- output/tags/phase7c-live-batch2-verify.json
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Shopify live tagged products: 78 (was 71)
- type-hat: 4 new products now tagged
- type-coat: 3 new products now tagged
- false-positive blocker established for future hat/coat batches
## OPEN ISSUES:
- EU Shoe Size mapping — חסום עד אישור אייל
- REVIEW_ONLY 135 products — manual review required
- remaining SAFE pool ~180 products — needs T3 re-approval for Batch 3
## NEXT STEP:
- T3 re-approval מאייל → Phase 7C Batch 3 (remaining dress/set/romper/bodysuit from SAFE pool)

---

## DATE: 2026-05-05
## TASK: Layer 7 Phase 7C — Live Batch 1 (T3 approved by Ayal)
## SCOPE: Layer 7 — Live tag write — 20 products — Shopify PUT + verify
## WHAT CHANGED:
- 20 products tagged in Shopify live (PUT HTTP 200 + GET verify PASS per product)
- 2 products excluded by shoe title keyword (סנדלי קיץ, סנדלים אופנתיים)
- types written: dress:4, bodysuit:5, set:6, romper:5
- gender written: girl:6, boy:5, neutral:2, none:7
- occ tags written: occ-gift×5, occ-everyday×4, occ-seasonal×5
- post-run verify: 20/20 PASS (GET re-check)
- rollback: NOT triggered
- Shopify live: YES (71 products total, up from 51)
- no age-* tags, no type collision, no gender collision, no forbidden tags
## FILES TOUCHED:
- scripts/phase7c_live_batch1.py
- scripts/phase7c_live_batch1_verify.py
- output/tags/phase7c-live-batch1-backup.json
- output/tags/phase7c-live-batch1-dry-run.md
- output/tags/phase7c-live-batch1-dry-run.json
- output/tags/phase7c-live-batch1-rollback-plan.md
- output/tags/phase7c-live-batch1-verify.md
- output/tags/phase7c-live-batch1-verify.json
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Shopify live tagged products: 71 (was 51)
- Smart Collections now include 20 additional products
- SAFE candidates remaining: ~187
## OPEN ISSUES:
- EU Shoe Size mapping — חסום עד אישור אייל
- REVIEW_ONLY 135 products — manual review required
## NEXT STEP:
- T3 re-approval מאייל → Phase 7C Batch 2 (hat + coat candidates)

---

## DATE: 2026-05-05
## TASK: Layer 7 Phase 7C — Tagging Expansion Planning (READ-ONLY)
## SCOPE: Layer 7 — Product classification + batch planning — no Shopify writes
## WHAT CHANGED:
- 393 מוצרים פעילים נסרקו ב-Shopify
- כבר מתויגים (type-*): 51 | SAFE candidates: 207 | REVIEW_ONLY: 135 | REJECT: 0
- recommended batch: 30 מוצרים — dress:6, set:6, romper:6, bodysuit:5, hat:4, coat:3
- gender breakdown: girl:12, no-gender:10, boy:5, neutral:3
- כל safety checks PASS (no age-*, no type collision, no gender collision, no EU shoe size)
- Shopify writes: NONE (GET-only)
- verdict: READY_FOR_PHASE7C_T3_APPROVAL
## FILES TOUCHED:
- scripts/phase7c_tagging_expansion_plan.py
- output/tags/phase7c-tagging-expansion-plan.md
- output/tags/phase7c-tagging-expansion-plan.json
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Phase 7 pipeline ממשיך לאחר Phase 8 Navigation Pipeline COMPLETE
- blocker פתוח: EU Shoe Size mapping (type-shoes/sandals/sneakers)
- REVIEW_ONLY pool (135) ממתין לסקירה ידנית לפני הכללה
## OPEN ISSUES:
- EU Shoe Size mapping — חסום עד אישור אייל
- REVIEW_ONLY 135 products — manual review required
## NEXT STEP:
- T3 approval מאייל → Phase 7C live batch (עד 20 מוצרים ראשונים)

---

## DATE: 2026-05-05
## TASK: Layer 8 Phase 8G — Navigation Post-Live Monitor (READ-ONLY)
## SCOPE: Layer 8 — Post-live monitoring — no Shopify writes
## WHAT CHANGED:
- 15/15 checks PASS — navigation technical state confirmed stable
- main-menu: 17 top-level items, GID unchanged (gid://shopify/Menu/250909851961)
- 'בגדי תינוקות' קיים עם 5 תתי פריטים: סטים/סרבלים/בגדי בנות/בגדי בנים/כל הבגדים
- 'מתנות לתינוק' קיים כפריט ראשי → /collections/occ-gift
- 3 legacy items absent from top-level
- כל 6 URLs → HTTP 200
- כל 6 Smart Collections קיימות (count=6)
- clothing-all: 51 מוצרים
- אין Mega Menu, אין שינוי collections/products/tags/theme
- Shopify writes: NONE (GET-only)
## FILES TOUCHED:
- scripts/phase8g_navigation_monitor.py
- output/tags/phase8g-navigation-post-live-monitor.md
- output/tags/phase8g-navigation-post-live-monitor.json
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Phase 8 Navigation Pipeline: COMPLETE
- Backlog פתוח: Phase 8H — Navigation Visual UX Polish (עתידי, לא חוסם)
## OPEN ISSUES:
- Phase 8H — Visual UX Polish (עיצוב/סידור התפריט) — עתידי בלבד
## NEXT STEP:
- Phase 8H (עתידי) — Visual QA + UX Polish — לפי החלטת אייל

---

## DATE: 2026-05-05
## TASK: Layer 8 Phase 8F — Main Menu Navigation Update LIVE (T3 approved)
## SCOPE: Layer 8 — GraphQL menuUpdate on main-menu — 1 mutation write
## WHAT CHANGED:
- main-menu עודכן דרך GraphQL menuUpdate:
  - לפני: 18 פריטים | אחרי: 17 פריטים
  - נוסף 'בגדי תינוקות' כפריט ראשי עם 5 תתי פריטים:
    1. סטים → /collections/type-set
    2. סרבלים → /collections/type-romper
    3. בגדי בנות → /collections/gender-girl
    4. בגדי בנים → /collections/gender-boy
    5. כל הבגדים → /collections/clothing-all
  - נוסף 'מתנות לתינוק' → /collections/occ-gift כפריט ראשי נפרד
  - הוסרו מניווט בלבד: 'בגדי בנות', 'בגדי בנים', 'מארזי מתנה' (collections לא נמחקו)
- 16/16 verify checks PASS
- backup שמור: output/tags/phase8f-main-menu-prewrite-backup.json
## FILES TOUCHED:
- scripts/phase8f_navigation_live.py
- output/tags/phase8f-main-menu-prewrite-backup.json
- output/tags/phase8f-navigation-live-verify.md
- output/tags/phase8f-navigation-live-verify.json
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Shopify Navigation: 1 GraphQL menuUpdate on gid://shopify/Menu/250909851961
- אין שינוי collections, אין שינוי products, אין שינוי tags, אין שינוי theme
- אין Mega Menu
## OPEN ISSUES:
- Visual QA ידני — מומלץ לוודא תצוגה בדפדפן (desktop + mobile)
## NEXT STEP:
- Visual QA ידני על main-menu בדפדפן
- שלב הבא לפי תוכנית: Phase 8G (אם מוגדר) — post-live monitor

---

## DATE: 2026-05-05
## TASK: Layer 8 Phase 8E-4 — clothing-all Smart Collection LIVE CREATE (T3 approved)
## SCOPE: Layer 8 — Shopify Smart Collection create — 1 POST write
## WHAT CHANGED:
- Smart Collection clothing-all נוצרה ב-Shopify live
  - id=526700020025, handle=clothing-all, title=כל בגדי התינוקות
  - disjunctive=true (OR logic), sort_order=best-selling, published=true
  - 4 rules: type-set / type-romper / type-dress / type-bodysuit
  - SEO: title_tag + description_tag metafields הוגדרו
- 16/16 verify checks PASS:
  - exists, handle, title, published, sort_order, disjunctive, rules(4), rule_count(4)
  - product_count=51 (in range 48–54), url HTTP 200
  - seo_title present, seo_desc present
  - no extra collections (6 total as expected)
  - main-menu GID unchanged (gid://shopify/Menu/250909851961)
  - product tags unchanged
- backup שמור: output/tags/phase8e4-clothing-all-precreate-backup.json
- verify MD: output/tags/phase8e4-clothing-all-live-verify.md
- verify JSON: output/tags/phase8e4-clothing-all-live-verify.json
- Smart Collections live: 6 (5 Phase 8C + 1 Phase 8E-4)
## FILES TOUCHED:
- scripts/phase8e4_clothing_all_live.py
- output/tags/phase8e4-clothing-all-precreate-backup.json
- output/tags/phase8e4-clothing-all-live-verify.md
- output/tags/phase8e4-clothing-all-live-verify.json
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Shopify: 1 Smart Collection POST — clothing-all (id=526700020025)
- Smart Collections live: 6 total
- אין שינוי Navigation, אין שינוי products/tags
## OPEN ISSUES:
- Phase 8F עדיין ממתין לT3 approval מאייל לפני mutation
## NEXT STEP:
- T3 approval מאייל לPhase 8F
- Phase 8F: menuUpdate mutation → הוסף `בגדי תינוקות` עם 6 sub-items (כולל clothing-all) → verify

---

## DATE: 2026-05-05
## TASK: Layer 8 Phase 8E — Navigation Dry Run (read-only, no mutation)
## SCOPE: Layer 8 — Navigation dry run — NO Shopify writes, NO mutation
## WHAT CHANGED:
- main-menu נקרא דרך GraphQL: GID=gid://shopify/Menu/250909851961, 18 items, title="תפריט"
- 3 overlaps ישנים מסומנים remove_from_navigation_candidate:
  - 'בגדי בנות' → /collections/בגדי-בנות (resourceId=482519155001)
  - 'בגדי בנים' → /collections/בגדי-בנים (resourceId=482519187769)
  - 'מארזי מתנה' → /collections/מארזי-מתנה (resourceId=471568646457)
- כל 5 URLs חדשים מחזירים HTTP 200
- mutations נמצאו: menuCreate, menuUpdate, menuDelete
- מבנה מוצע: `בגדי תינוקות` עם 5 sub-items (gender-girl/boy, type-set/romper, occ-gift)
- snapshot שמור ב: output/tags/phase8e-navigation-dryrun.json
- אין שינוי Navigation, אין Mega Menu, אין שינוי products/tags
## FILES TOUCHED:
- output/tags/phase8e-navigation-dryrun.md
- output/tags/phase8e-navigation-dryrun.json
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Phase 8E COMPLETE — READY_FOR_PHASE8F_T3_APPROVAL
- Shopify: אין שינוי (0 writes, 0 mutations)
- Navigation: לא שונה
## OPEN ISSUES:
- Phase 8F עדיין ממתין לT3 approval מאייל לפני mutation
- write_online_store_navigation scope עדיין נדרש לbiצוע mutation
  → GraphQL menuUpdate ידרוש את הscope הזה
## NEXT STEP:
- T3 approval מאייל לPhase 8F
- Phase 8F: menuUpdate mutation → הוסף `בגדי תינוקות` עם 5 sub-items + הסר overlaps מניווט → verify → rollback אם נדרש

---

## DATE: 2026-05-05
## TASK: Layer 8 Phase 8E — Navigation Endpoint Diagnosis + Scope Blocker Resolved
## SCOPE: Layer 8 — Navigation scope investigation — NO Shopify writes
## WHAT CHANGED:
- Phase 8E scope blocker resolved — לא ע"י תיקון REST scope, אלא ע"י גילוי שGraphQL עובד
- GraphQL Admin API `menus(first:5)` query: HTTP 200 ✅ — 5 menus נמצאו
- Menus שנמצאו: main-menu, footer, link-list, link-list-1, customer-account-main-menu
- REST `/menus.json` (2024-10 + 2026-01 + 2023-10): עדיין HTTP 403 (scope חסר)
- GraphQL עובד — לא נדרש scope נוסף לקריאה (אבל mutations עדיין ידרשו `online_store_navigation`)
- Token חדש הופק: suffix `0e9e` — Desktop .env עודכן
- אין שינוי Navigation
- אין Mega Menu
## FILES TOUCHED:
- output/tags/phase8e-navigation-endpoint-diagnosis.md
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- READY_FOR_PHASE8E_NAVIGATION_DRYRUN — Phase 8E dry run אפשרי
- Shopify: אין שינוי (0 writes)
- Navigation: לא שונה
- GraphQL path confirmed: backup + dry run + write יעשו דרך GraphQL mutations
## OPEN ISSUES:
- Phase 8E Dry Run עדיין ממתין לT3 approval מאייל לפני write
- GraphQL mutations (`menuCreate` / `menuUpdate`) יעלו error אם `write_online_store_navigation` חסר
  → לבדוק בdry run לפני T3
## NEXT STEP:
- Phase 8E Dry Run: GET main-menu → הצג מבנה חדש מוצע → T3 approval → write (GraphQL) → verify → rollback אם צריך

---

## DATE: 2026-05-05
## TASK: Layer 8 Phase 8D — Navigation Planning (read-only)
## SCOPE: Layer 8 — Navigation planning — NO Shopify writes
## WHAT CHANGED:
- Phase 8D תכנון ניווט נוצר: output/tags/phase8d-navigation-planning.md
- נקראו collections קיימות: 5 smart (Phase 8C) + 18 custom
- ממצא קריטי: 3 custom collections ישנות חופפות לsmarts (בגדי-בנות, בגדי-בנים, מארזי-מתנה)
- ממצא קריטי: Token חסר scope `write_navigation` — blocker לPhase 8E
- header.liquid: תמיכה בdropdown + mega
- המלצה: Option A — simple dropdown תחת "בגדי תינוקות", 5 sub-items
- Mega Menu: לא מומלץ עכשיו (רק 5 collections)
- type-dress/type-bodysuit: נשארות בחוץ
## FILES TOUCHED:
- output/tags/phase8d-navigation-planning.md
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Phase 8D COMPLETE — READY_FOR_PHASE8E_NAVIGATION_DRYRUN
- Shopify: אין שינוי (0 writes)
- Navigation: לא שונה
## OPEN ISSUES:
- ⚠️ BLOCKER Phase 8E: token חסר scope `write_navigation`
  → אייל צריך להוסיף scope ב-Custom App → regenerate token → עדכן .env
  → OR: עדכון ידני ב-Shopify Admin → Navigation
- 3 custom collections ישנות חופפות — לנהל בPhase 8E (הסרה מניווט, לא מחיקה)
## NEXT STEP:
- פתרון blocker write_navigation scope — אישור אייל
- Phase 8E: backup nav → dry run → T3 → write nav → verify → rollback אם צריך

---

## DATE: 2026-05-05
## TASK: Layer 8 Phase 8C — Create 5 Smart Collections LIVE (T3 approved by Ayal)
## SCOPE: Layer 8 — Shopify Smart Collections — LIVE WRITE — PHASE8C_PASS
## WHAT CHANGED:
- 5 Smart Collections נוצרו ב-Shopify live
- gender-girl (id=526691729721): 20/20 מוצרים — PASS
- gender-boy (id=526691762489): 19/19 מוצרים — PASS
- type-set (id=526691795257): 18/18 מוצרים — PASS
- type-romper (id=526691828025): 16/16 מוצרים — PASS
- occ-gift (id=526691860793): 14/14 מוצרים — PASS
- לא נוצרו: type-dress, type-bodysuit (כמפורש באישור T3)
- 11 QA checks עברו לכל collection
- גיבוי לפני יצירה: output/tags/phase8c-smart-collections-backup.json
- verify MD: output/tags/phase8c-smart-collections-live-verify.md
## FILES TOUCHED:
- scripts/phase8c_create_collections.py
- output/tags/phase8c-smart-collections-backup.json
- output/tags/phase8c-smart-collections-live-verify.md
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Smart Collections live: 0 → 5
- rollback: לא הופעל (0 failures)
- product tags: ללא שינוי (collections only)
## OPEN ISSUES:
- Mega Menu / navigation wiring — Phase 8D (pending אישור)
- type-dress + type-bodysuit: pending growth (7B+ batches) before safe to create
## NEXT STEP:
- Phase 8D: wire collections to navigation/Mega Menu (T3 required)

---

## DATE: 2026-05-05
## TASK: Layer 8 Phase 8B — Collections Dry Run (7 collections, 0 blocked)
## SCOPE: Layer 8 — collections planning — NO Shopify writes
## WHAT CHANGED:
- Phase 8B dry run מלא לכל 51 מוצרים
- 7 collections נבדקו: gender-girl(20), gender-boy(19), type-set(18), type-romper(16), occ-gift(14), type-dress(9), type-bodysuit(8)
- כל 7 collections עברו קריטריוני חסימה
- 2 collections עם SEO caveat: type-dress(9), type-bodysuit(8)
- output: phase8b-collections-dryrun.md + phase8b-collections-dryrun.json
- אין כתיבה ל-Shopify
## FILES TOUCHED:
- output/tags/phase8b-collections-dryrun.md
- output/tags/phase8b-collections-dryrun.json
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Phase 8B COMPLETE — READY_FOR_PHASE8C_T3_APPROVAL
- Shopify: אין שינוי (0 writes)
- Collections live: 0 (unchanged)
## OPEN ISSUES:
- T3 approval מאייל נדרש לפני Phase 8C
- type-dress: 9 products — SEO thin, recommend growing to 12+ in Phase 7C
- type-bodysuit: 8 products — HIGH SEO risk, consider growing or merging
## NEXT STEP:
- שלח Phase 8B report לאייל לאישור T3
- Phase 8C: create 7 Smart Collections in Shopify (T3 required)

---

## DATE: 2026-05-05
## TASK: Layer 8 Phase 8A — Collections Navigation Plan
## SCOPE: Layer 8 — collections planning — NO Shopify writes
## WHAT CHANGED:
- Phase 8A plan נוצר: output/tags/phase8a-collections-navigation-plan.md
- ניתוח 51 מוצרים, 7 collections recommended, navigation structure proposed
## FILES TOUCHED:
- output/tags/phase8a-collections-navigation-plan.md
## SYSTEM IMPACT: Phase 8A COMPLETE

---

## DATE: 2026-05-05
## TASK: Layer 7 Phase 7B — Live Batch 2 (12 מוצרים — PASS 12/12)
## SCOPE: Layer 7 — live Shopify tag write — PHASE7B_LIVE_BATCH2_PASS
## WHAT CHANGED:
- 12 מוצרים קיבלו tags Layer 6/7 ב-Shopify live
- כל 12 PUT HTTP 200 + GET verify PASS
- merge בלבד (אין מחיקות): final = sorted(set(current) | set(proposed))
- סוגים: 1 bodysuit + 3 dress + 4 romper + 4 set
- גיבוי JSON נשמר: output/tags/phase7b-live-batch2-tags-backup.json
- verify MD נשמר: output/tags/phase7b-live-batch2-verify.md
- בחירה: מיני dry-run — 193 SAFE candidates → 12 נבחרו (max 4/type)
## FILES TOUCHED:
- output/tags/phase7b-live-batch2-tags-backup.json
- output/tags/phase7b-live-batch2-verify.md
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Shopify live tagged products: 39 → 51
- יעד Phase 8 הושג: 51 מוצרים מ-4+ סוגים (bodysuit/dress/romper/set)
- rollback: לא הופעל (0 failures)
## OPEN ISSUES:
- EU shoes: עדיין חסום
- Phase 8 collections: eligible for PLANNING — T3 approval נדרש לפני live
## NEXT STEP:
- Phase 8 planning: collections/navigation — T3 approval נדרש לפני live

---

## DATE: 2026-05-04
## TASK: Layer 7 Phase 7B — Live Batch 1 (20 מוצרים — PASS 20/20)
## SCOPE: Layer 7 — live Shopify tag write — PHASE7B_LIVE_BATCH1_PASS
## WHAT CHANGED:
- 20 מוצרים קיבלו tags Layer 6/7 ב-Shopify live
- כל 20 PUT HTTP 200 + GET verify PASS
- merge בלבד (אין מחיקות): final = sorted(set(current) | set(proposed))
- סוגים: 5 dress + 5 bodysuit + 5 set + 5 romper
- backup JSON נשמר: output/tags/phase7b-live-batch1-tags-backup.json
- verify MD נשמר: output/tags/phase7b-live-batch1-verify.md
## FILES TOUCHED:
- output/tags/phase7b-live-batch1-tags-backup.json
- output/tags/phase7b-live-batch1-verify.md
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- Shopify live tagged products: 19 → 39
- rollback: לא הופעל (0 failures)
## OPEN ISSUES:
- Phase 8 collections BLOCKED — need 50+ products (now 39, need 11+ more)
- Phase 7B Batch 2: 11+ מוצרים נוספים לפני Phase 8
## NEXT STEP:
- Phase 7B Batch 2 — 11+ מוצרים נוספים מ-pool של 202 SAFE candidates

---

## DATE: 2026-05-04
## TASK: Layer 7 Phase 7B — Dry Run re-confirm (374/222/108/44 — consistent)
## SCOPE: Layer 7 — dry run only — אין כתיבה ל-Shopify
## WHAT CHANGED:
- dry run רץ שנית על 374 מוצרים (אימות תוצאות קודמות)
- תוצאות עקביות: 222 SAFE | 108 REVIEW_ONLY | 44 REJECT
- output files זהים — phase7b-dryrun-candidates.md/.json בgit ללא שינוי
- recommended batch: 20 מוצרים (5 dress + 5 bodysuit + 5 set + 5 romper) — מאושר
## FILES TOUCHED:
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- אין שינוי. Shopify live = 19 מוצרים.
## OPEN ISSUES:
- ממתין לאישור T3 מאייל לפני live batch
- EU shoes: עדיין חסום
## NEXT STEP:
- Phase 7B live batch — T3 approval from Ayal → write to Shopify
- IDs recommended: 9606691324217, 9895864369465, 9892557848889, 9179146256697, 9606694175033, 10190522908985, 9179165753657, 9179154612537, 9179152154937, 9179167129913, 10190522941753, 10190523203897, 10190523105593, 10190523236665, 10190522843449, 10029649101113, 9657091293497, 9687596728633, 10029649002809, 10029648970041

---

## DATE: 2026-05-04
## TASK: Layer 7 Phase 7B — Dry Run (374 מועמדים, 222 SAFE)
## SCOPE: Layer 7 — dry run only — אין כתיבה ל-Shopify
## WHAT CHANGED:
- dry run רץ על 374 active products untapped (מתוך 393 total)
- 222 SAFE_FOR_PHASE7B | 108 REVIEW_ONLY | 44 REJECT
- תוקנו 3 misclassifications מ-handle: 2 נעליים + 1 אוברול שסומנו כ-dress בגלל "dress" בhandle
- classifier: הוסרה בדיקת "dress" בhandle (היתה רחבה מדי) → נשמרו רק "smlat"/"smla"
- recommended batch: 20 מוצרים מ-4 סוגים (5 dress + 5 bodysuit + 5 set + 5 romper)
- verdict: READY_FOR_PHASE7B_T3_APPROVAL
## FILES TOUCHED:
- output/tags/phase7b-dryrun-candidates.json
- output/tags/phase7b-dryrun-candidates.md
- scripts/phase7b_dryrun.py
- scripts/phase7b_build_report.py
- scripts/phase7b_patch_report.py
- docs/organic/organic-journal.md
## SYSTEM IMPACT:
- pool: 222 SAFE candidates (type-set:97 | type-romper:56 | type-dress:27 | type-shoes:14 | type-bodysuit:9 | type-hat:7 | type-sandals:4 | type-swimwear:3 | type-coat:3 | other:2)
- recommended batch ready for T3 approval: 9606691324217, 9895864369465, 9892557848889, 9179146256697, 9606694175033, 10190522908985, 9179165753657, 9179154612537, 9179152154937, 9179167129913, 10190522941753, 10190523203897, 10190523105593, 10190523236665, 10190522843449, 10029649101113, 9657091293497, 9687596728633, 10029649002809, 10029648970041
- אין כתיבה ל-Shopify. Shopify live עדיין 19 מוצרים.
## OPEN ISSUES:
- EU shoe sizes — עדיין אין מיפוי מאושר (type-shoes/sandals = 18 blocked products)
- handle-based type: 2 romper products בbatch עם handle-only source (לבדיקה T3)
- Phase 8 collections: חסום — אחרי batch יהיו 39 (עוד 11 חסרים ל-50)
## NEXT STEP:
- Phase 7B live batch — לאחר T3 approval מאייל
- batch 1: עד 20 מוצרים מ-4 סוגים (recommended list בדוח)
- batch 2 לאחר מכן: עוד 11+ כדי להגיע ל-50+

---

## DATE: 2026-05-04
## TASK: Layer 7 Phase 7A — Batch 2 Live (4 מוצרים SAFE שנותרו)
## SCOPE: Layer 7 — Shopify live tag write — 4 products
## WHAT CHANGED:
- Phase 7A batch 2 בוצע — T3 approval מאייל התקבל
- 4 מוצרים קיבלו תגיות Layer 6/7 חיות (2 type-set, 2 type-romper)
- גיבוי נוצר לפני הכתיבה: output/tags/phase7a-batch2-tags-backup.json
- כל 4 מוצרים עברו verify PASS (PUT 200 + GET confirm)
- Shopify live: YES — 19 products total (15 קודמים + 4 batch 2)
- אין age-* tags. אין rollback.
## FILES TOUCHED:
- output/tags/phase7a-batch2-tags-backup.json
- output/tags/phase7a-batch2-live-verify.md
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- 9606694437177 (חליפת פולו קצרה): type-set, season-summer, fabric-knit, gender-neutral, style-striped
- 9688885985593 (אוברול פיל מתוק): type-romper, size-3-6m, size-6-9m, size-newborn, season-spring-fall, gender-girl
- 9688934973753 (אוברול פיל פסים): type-romper, size-0-3m..12-18m, style-striped
- 10190523138361 (Boys summer striped set): type-set, size-3y, season-summer, gender-boy, style-striped
## OPEN ISSUES:
- EU shoe sizes — אין מיפוי מאושר עדיין
- 6 REVIEW_ONLY ממתינים לבדיקה ידנית (phase7a-diverse-rollout-candidates.md)
## NEXT STEP:
- Phase 7B — candidate expansion toward 50+ products from 4+ types
- target: 50+ מוצרים מ-4+ סוגים לפני Phase 8 (collections)

---

## DATE: 2026-05-04
## TASK: Layer 7 Phase 7A — Batch 1 Live (10 מוצרים מגוונים)
## SCOPE: Layer 7 — Shopify live tag write — 10 products diverse types
## WHAT CHANGED:
- Phase 7A batch 1 בוצע — T3 approval מאייל התקבל
- 10 מוצרים קיבלו תגיות Layer 6/7 חיות (type-dress, type-bodysuit, type-set)
- גיבוי נוצר לפני הכתיבה: output/tags/phase7a-batch1-tags-backup.json
- כל 10 מוצרים עברו verify PASS (PUT 200 + GET confirm)
- Shopify live: YES — 15 products total (5 Phase6 + 10 Phase7A)
- אין age-* tags. אין rollback.
## FILES TOUCHED:
- output/tags/phase7a-batch1-tags-backup.json
- output/tags/phase7a-batch1-live-verify.md
- scripts/tags/run_phase7a_batch1_live.py
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- 9731768746297 (סט בגדי תינוקות גינס ושמלה): type-dress, season-summer, fabric-denim, gender-girl
- 9179166671161 (בגד גוף שמלה ג׳ינס): type-bodysuit, size-12-18m, size-3-6m, fabric-cotton
- 9874906382649 (בגד גוף פו הדוב): type-bodysuit, size-0-3m..18-24m, season-summer, fabric-cotton, gender-girl, style-teddy
- 9874906546489 (חליפת דובי): type-set, size-3-6m/9-12m, season-spring-fall, gender-boy, style-teddy
- 9688660377913 (חליפת קואלה): type-set, size-0-3m..18-24m, season-spring-fall, gender-girl, style-casual
- 9688976326969 (חליפה דוב מופתע): type-set, size-0-3m..12-18m, gender-boy, style-casual
- 9688964989241 (חליפה דוב מקסימה): type-set, size-9-12m, season-winter, fabric-polyester, gender-boy, style-teddy
- 9688674566457 (חליפה לבנים): type-set, size-0-3m/3-6m/12-18m/18-24m, gender-boy, style-casual
- 9688976294201 (חליפה רקמת דובי): type-set, size-6-9m..18-24m, season-winter, gender-boy, style-casual
- 10190523302201 (Boys Summer Set): type-set, size-3-6m..18-24m, season-summer, gender-boy, style-casual
## OPEN ISSUES:
- EU shoe sizes — אין מיפוי מאושר עדיין
- 4 SAFE_FOR_PHASE7A נותרו ל-batch הבא (9606694437177, 9688885985593, 9688934973753, 10190523138361)
- 6 REVIEW_ONLY ממתינים לבדיקה ידנית
## NEXT STEP:
- post-live monitor ל-15 מוצרים
- batch נוסף Phase 7A (4 נותרים SAFE)
- target: 50+ מוצרים מ-4+ סוגים לפני Phase 8 (collections)

---

## DATE: 2026-05-04
## TASK: Layer 6 Phase 6 — Batch 2 Live (C5, C1)
## SCOPE: Layer 6 — Shopify live tag write — 2 products
## WHAT CHANGED:
- Phase 6 batch 2 בוצע — T3 approval מאייל התקבל
- C5 (9687579033913) + C1 (9688932909369) קיבלו תגיות Layer 6 חיות
- גיבוי נוצר לפני הכתיבה: output/tags/phase6-batch2-tags-backup.json
- שני המוצרים עברו verify PASS
- Shopify live: YES (5 products total: C3, C2, C4, C5, C1)
- אין age-* tags. אין rollback.
## FILES TOUCHED:
- output/tags/phase6-batch2-tags-backup.json
- output/tags/phase6-batch2-live-verify.md
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- C5 (9687579033913): type-romper, size-0-3m/3-6m/6-9m/9-12m/12-18m, season-winter, fabric-cotton, gender-girl
- C1 (9688932909369): type-romper, size-0-3m/3-6m/6-9m/9-12m, gender-boy, style-casual
## OPEN ISSUES:
- EU shoe sizes (C6, C8) — אין מיפוי מאושר
- Phase 7+ (collections/navigation) ממתין לאישור נפרד
## NEXT STEP:
- review results + consider collections/navigation planning only after explicit approval

---

## DATE: 2026-05-04
## TASK: Layer 6 Phase 6 — Small Live Batch 1 (C3, C2, C4)
## SCOPE: Layer 6 — Shopify live tag write — 3 products
## WHAT CHANGED:
- Phase 6 batch 1 בוצע — T3 approval מאייל התקבל
- 3 מוצרים קיבלו תגיות Layer 6 חיות: C3, C2, C4
- גיבוי נוצר לפני הכתיבה: output/tags/phase6-small-batch-tags-backup.json
- כל 3 מוצרים עברו verify מלא אחרי כתיבה — PASS
- Shopify live: YES (3 products only)
- אין age-* tags. אין rollback נדרש.
## FILES TOUCHED:
- output/tags/phase6-small-batch-tags-backup.json
- output/tags/phase6-small-batch-live-verify.md
- docs/organic/organic-journal.md
- docs/organic/מצב-הפרויקט-האורגני.md
## SYSTEM IMPACT:
- C3 (9688660312377): type-romper, size-3-6m/6-9m/9-12m/12-18m, season-spring-fall, fabric-denim, gender-girl
- C2 (9874906349881): type-romper, size-3-6m/6-9m/9-12m, season-summer, fabric-denim, gender-neutral, style-casual
- C4 (9895864205625): type-romper, size-0-3m/3-6m/9-12m/12-18m, fabric-denim, gender-neutral, style-casual
## OPEN ISSUES:
- EU shoe sizes (C6, C8) — אין מיפוי מאושר
- batch שני (C5, C1) ממתין לאישור נוסף
## NEXT STEP:
- monitor Shopify analytics 48-72 שעות
- batch שני רק אחרי אישור נוסף מאייל

---

## DATE: 2026-05-03
## TASK: Layer 6 Phase 5d — Rerun after Phase 5b/5c logic updates
## SCOPE: Layer 6 — validation rerun, no Shopify writes
## WHAT CHANGED:
- הרצה חוזרת על 59 מוצרים עם לוגיקה מעודכנת Phase 5b/5c
- type-sleep-soother מזוהה לפני type-reborn-doll ב-CAT-A (מוצר 13 תוקן)
- Phase 5b: CAT-B פטור לסוגים שאינם ביגוד/נעליים (NON_AGE_TYPES)
- מוצר 13 (פיל נושם): type-reborn-doll → type-sleep-soother, score 79.8→95.1
- Avg quality score: 77.7 → 82.3 (+4.6 — Phase 5b counts CAT-B as present for exempt types)
- PASS/NEEDS_REVIEW: 30/29 (ללא שינוי בחלוקה — לא נמצאו products עם YAML שמטיפוס non-age)
- BLOCKED: 0 (ללא שינוי)
- taxonomy gaps: 0 (ללא שינוי)
- Phase5b_exempt: 0 (כי מוצרי reborn_toys הם yaml_gap, exempt דרך YAML_GAP לא Phase5b)
- sleep_soother_count: 1 ✅
## FILES TOUCHED:
- scripts/tags/run_layer6_phase5d_rerun.py (new)
- output/tags/phase5d-rerun-sample-59.json (new)
- output/tags/phase5d-rerun-report.json (new)
- output/tags/phase5d-rerun-report.md (new)
- output/tags/phase5d-rerun-comparison.md (new)
## SYSTEM IMPACT:
- Layer 6 Phase 5d CREATED — WAITING AYAL REVIEW
- Shopify live: NO
- Phase 6 NOT OPEN
- ממוצע quality score שיפור: 77.7 → 82.3
## OPEN ISSUES:
- D1 NO_AGE_FOUND: ~18 clothing/shoes — עדיין ממתין
- D2 RANGE_TOO_BROAD: 4 מוצרים — עדיין ממתין
- Phase 6 candidates: 5+ מוצרים זמינים (PASS + score>=80 + no yaml_gap)
## NEXT STEP: Phase 5d Ayal Review ← WAITING

---

## DATE: 2026-05-03
## TASK: Layer 6 Phase 5b — CAT-B Rule Update
## SCOPE: Layer 6 — logic update, no Shopify writes
## WHAT CHANGED:
- כלל מחייב חדש: CAT-B (age) נדרש רק לביגוד/נעליים
- לא נדרש age לצעצועים/ריבורן/אביזרים/type-unknown
- עודכן scripts/tags/layer6_validate_tags.py: _catb_exempt + NON_AGE_TYPES + CLOTHING_SHOES_TYPES
- נוספו type-bath-accessory + type-plush-toy לרשימת ערכים מותרים (CAT-A)
- עודכנו phase5 docs: מוצרים 10/12/13 + D1 + D3 (החלטה סופית)
- D3 החלטה סופית: A — אין age לריבורן/צעצועים. C בעתיד אם מפורש.
- NO_AGE_FOUND אמיתי: ~18 clothing/shoes (לא 31)
## FILES TOUCHED:
- scripts/tags/layer6_validate_tags.py (updated: Phase 5b CAT-B rule)
- output/tags/phase5-human-review-pack.md (updated: Phase 5b section + products 10/12/13 + D1/D3)
- output/tags/phase5-human-review-pack.json (updated: D1/D3 + items 10/12/13 + phase5b_rule)
- output/tags/phase5-human-review-summary.md (updated: risks + D3 decided)
## SYSTEM IMPACT:
- Layer 6 Phase 5b CREATED — WAITING AYAL REVIEW
- Shopify live: NO
- Phase 6 NOT OPEN
## OPEN ISSUES:
- D1 NO_AGE_FOUND: ~18 clothing/shoes — עדיין ממתין
- D2 RANGE_TOO_BROAD: 4 מוצרים — עדיין ממתין
- type-reborn-doll לפיל פלאש — classification rule לתיקון
## NEXT STEP: Phase 5 Ayal Review ← WAITING

---

## DATE: 2026-05-03
## TASK: Layer 6 Phase 5 — Human Review Pack
## SCOPE: Layer 6 — review documentation, read-only (no Shopify writes)
## WHAT CHANGED:
- נוצרה חבילת בדיקה ידנית מ-Phase 4 Dry Run עבור אייל
- 15 מוצרים נבחרו לבדיקה: 5 PASS + 5 NO_AGE_FOUND + 3 YAML_GAP + 2 RANGE_BROAD/edge
- זוהו 5 ממצאים חשובים: type-reborn-doll שגוי (פיל פלאש), ניגוד גיל נעל מוצר 3, טווח רחב מוצר 4, מדחום type-unknown, NO_AGE_FOUND×31
- נוצרה טבלת Menu Label Review (16 תוויות)
- נוצרו 4 Open Decisions: D1 NO_AGE_FOUND / D2 RANGE_TOO_BROAD / D3 Doll Age / D4 Phase 6 readiness
## FILES TOUCHED:
- output/tags/phase5-human-review-pack.md (new)
- output/tags/phase5-human-review-pack.json (new)
- output/tags/phase5-human-review-summary.md (new)
## SYSTEM IMPACT:
- Layer 6 Phase 5 CREATED — WAITING AYAL REVIEW
- Shopify live: NO — review/documentation only
- Phase 6 NOT OPEN
## OPEN ISSUES:
- type-reborn-doll שגוי על פיל פלאש (מוצר 13) — classification rule דורש תיקון
- NO_AGE_FOUND×31 — החלטת D1 נדרשת
- RANGE_TOO_BROAD×4 — החלטת D2 נדרשת
- מדחום (type-unknown) — האם שייך ל-Layer 6? החלטת אייל נדרשת
## NEXT STEP: Phase 6 Small Live Batch — רק לאחר Ayal VERDICT על Phase 5

---

## DATE: 2026-05-03
## TASK: Layer 6 Phase 4 — Dry Run (59 products)
## SCOPE: Layer 6 — full tag extraction pipeline, read-only (no Shopify writes)
## WHAT CHANGED:
- הורץ Phase 4 Dry Run על 59 מוצרים: 20 clothing_yaml + 15 shoes_yaml + 9 reborn_toys + 10 yaml_gap + 5 edge_cases
- 7 extractors (CAT-A עד CAT-G) עם Phase 3b normalization inline (ללא gender-unisex, ללא type-doll, ללא fallback)
- הורצו 8 validation gates על כל מוצר
- Phase 4 PASS criteria: כל 8 קריטריונים עברו ✅
- תוצאות: PASS 30/59 (50.8%) | NEEDS_REVIEW 29/59 (49.2%) | BLOCKED 0/59 (0%)
- Avg quality score: 77.7 | RANGE_TOO_BROAD: 4 | NO_AGE_FOUND: 31 | doll_no_age: 9
- gate fails: CATEGORY_COVERAGE 26 | QUALITY_SCORE 17 (נובע מ-CATEGORY_COVERAGE)
- אין taxonomy gaps חדשים — כל טאגים עברו ALLOWED_VALUE
## FILES TOUCHED:
- scripts/tags/run_layer6_phase4_dryrun.py (new)
- output/tags/phase4-dryrun-sample-60.json (new)
- output/tags/phase4-dryrun-report.json (new)
- output/tags/phase4-dryrun-report.md (new)
- output/tags/phase4-dryrun-customer-labels-preview.md (new)
## SYSTEM IMPACT:
- Layer 6 Phase 4 CREATED — WAITING AYAL REVIEW
- Shopify live: NO — read-only analysis only
- Phase 5 NOT OPEN
## OPEN ISSUES:
- NO_AGE_FOUND×31: רוב reborn_toys (doll_no_age=9) + yaml_gap — החלטה נדרשת
- RANGE_TOO_BROAD×4: טווח גיל רחב מדי — נדרשת אסטרטגיה
- NEEDS_REVIEW×29: בעיקר CATEGORY_COVERAGE (CAT-B חסר) — מחכה לאישור
## NEXT STEP: Phase 5 — לאחר Ayal review על Phase 4

---

## DATE: 2026-05-03
## TASK: Layer 6 Phase 3b — Taxonomy & Source Normalization
## SCOPE: Layer 6 — taxonomy normalization, read-only (no Shopify writes)
## WHAT CHANGED:
- תוקנו taxonomy gaps שהתגלו ב-Phase 3 לפני Phase 4 Dry Run
- gender-unisex×18: explicit src → gender-neutral (13), deprecated src → gender-unknown (5)
- type-doll×5: reborn context → type-reborn-doll (4), no reborn → type-toy (1: BABY MANIA)
- type-other×2: → type-unknown (src=category_default)
- occ-sport×2, occ-holiday×1, style-cartoon×1: → BLOCKED (TAXONOMY_GAP)
- default_unisex/fallback deprecated sources: → category_default
- הורצו 8 gates מחדש: ALLOWED_VALUE 24 fail → 0 fail | SOURCE_TRACEABLE 6 fail → 0 fail
- Overall PASS: 3/30 → 12/30 | negative tests: 10/10 ✅
## FILES TOUCHED:
- scripts/tags/run_layer6_phase3_gates.py (updated: --phase3b mode added)
- output/tags/phase3b-normalized-source-map-sample-30.json (new)
- output/tags/phase3b-validation-gates-report.json (new)
- output/tags/phase3b-validation-gates-report.md (new)
## SYSTEM IMPACT:
- Layer 6 Phase 3b CREATED — WAITING AYAL REVIEW
- Shopify live: NO — read-only analysis only
- Phase 4 NOT OPEN
## OPEN ISSUES:
- CATEGORY_COVERAGE 17 fail: RANGE_TOO_BROAD×9, NO_AGE_FOUND×9 — structural, needs decision
- DUPLICATE_CONFLICT 1 fail: WarmNest multi-age (3 tags) — CAT-B single vs multi-value decision
- QUALITY_SCORE 13 fail: כולם נובעים מ-CATEGORY_COVERAGE בלבד (לא נפרדים)
## NEXT STEP: Phase 4 Dry Run — לאחר Ayal review על Phase 3b

---

## DATE: 2026-05-03
## TASK: Layer 6 Phase 3 — Validation Gates
## SCOPE: Layer 6 — 8 validation gates, read-only analysis
## WHAT CHANGED:
- נוצרו scripts/tags/layer6_validate_tags.py (8 gates) + scripts/tags/run_layer6_phase3_gates.py
- הורצו 8 gates על 30 המוצרים מ-Phase 2b + 10 negative test cases
- נוצרו output/tags/phase3-validation-gates-report.json + .md
- כל 10 negative tests עברו verification ✅
- ממצאים עיקריים: ALLOWED_VALUE 24/30 fail (taxonomy gaps) | SOURCE_TRACEABLE 6/30 fail (deprecated sources)
- Taxonomy gaps שהתגלו: gender-unisex×18, type-doll×5, occ-sport×2, type-other×2, style-cartoon×1, occ-holiday×1
## FILES TOUCHED:
- scripts/tags/layer6_validate_tags.py (new)
- scripts/tags/run_layer6_phase3_gates.py (new)
- output/tags/phase3-negative-test-cases.json (new)
- output/tags/phase3-validation-gates-report.json (new)
- output/tags/phase3-validation-gates-report.md (new)
## SYSTEM IMPACT:
- Layer 6 Phase 3 COMPLETE — validation gates ready
- Overall PASS (כל 8 gates): 3/30 — נמוך עקב taxonomy gaps מ-Phase 2
- Shopify live: NO — read-only analysis only
## OPEN ISSUES:
- Taxonomy gaps דורשים תיקון לפני Phase 4: gender-unisex→gender-neutral, type-doll→type-reborn-doll
- Sources deprecated: default_unisex, fallback — Phase 4 code חייב להשתמש ב-VALID_SOURCES בלבד
- 9 RANGE_TOO_BROAD + 9 NO_AGE_FOUND — ממתינים להחלטת אייל
## NEXT STEP: Phase 4 Dry Run — לאחר Ayal review על Phase 3

---

## DATE: 2026-05-05
## TASK: Layer 6 Phase 2b — CAT-B Age Extraction Hardening
## SCOPE: Layer 6 — age mapping hardening, read-only
## WHAT CHANGED:
- שיפור מיפוי CAT-B age group על אותם 30 מוצרים של Phase 2
- נוצרו output/tags/phase2b-age-hardening-sample-30.json + .md
- הוסרו 8 age tags שגויים (age-0-3m הוסק מטעות מטווחים רחבים / מוצרי reborn)
- נוספו 5 age tags לגיטימיים חדשים (toddler→2-3y, 1-3y, first-walker, Hebrew tags)
- תוקנו 2 age tags (WarmNest: Hebrew tags; נעל חורף מחממת: toddler→2-3y)
- RANGE_TOO_BROAD: 9 מוצרים תויגו במפורש (0-18m, 3-24m, 0-8y וכו')
- DOLL_NO_AGE_APPLICABLE: 5 מוצרי reborn/בובה — גיל לא רלוונטי
- no misleading age tags: YES ✅
## FILES TOUCHED:
- output/tags/phase2b-age-hardening-sample-30.json (new)
- output/tags/phase2b-age-hardening-sample-30.md (new)
## SYSTEM IMPACT:
- CAT-B valid coverage: 10→7 (פחות אבל מדויק)
- PASS: 13→14 | NEEDS_REVIEW: 13→12 | BLOCKED: 4→4 | avg: 71.6→70.3
- Shopify live: NO — read-only analysis only
## OPEN ISSUES:
- D1: legacy tags coexistence — confirmed (no migration)
- 9 מוצרים עם RANGE_TOO_BROAD — ממתינים להחלטת אייל על טיפול
- 9 מוצרים NO_AGE_FOUND — title/YAML ללא מידע גיל
## NEXT STEP: Phase 3 Validation Gates — לאחר Ayal review על Phase 2b

---

## DATE: 2026-05-05
## TASK: Layer 6 Phase 2 — Source Mapping Sample (30 products)
## SCOPE: Layer 6 — source mapping, read-only
## WHAT CHANGED:
- נוצרו output/tags/phase2-source-map-sample-30.json + .md
- 30 מוצרים: 10 clothing+YAML, 10 shoes+YAML, 5 reborn_gap, 5 YAML_GAP
- Quality: PASS=13, NEEDS_REVIEW=13, BLOCKED=4 | avg score=71.6
- CAT-B (age) נמוך (10/30) — titles לא תמיד מציינים גיל מפורש
- CAT-D (fabric) 3/30 — yaml_fabric ריק ברוב המוצרים, כצפוי מ-Phase 1 spec
## FILES TOUCHED:
- output/tags/phase2-source-map-sample-30.json (new)
- output/tags/phase2-source-map-sample-30.md (new)
- scripts/layer6-phase2-source-map.py (new)
## SYSTEM IMPACT:
- Layer 6 Phase 2 COMPLETE — source map sample ready for Ayal review
- Shopify live: NO — read-only analysis only
## OPEN ISSUES:
- D1: legacy tags migration vs coexistence — ממתין לאייל
- D2: 3-6M6-9M (1 product) — ממתין לאישור
- D3: 124 YAML_GAP — timeline לא מוגדר
- CAT-B coverage נמוכה — שיפור age extraction אפשרי ב-Phase 3
## NEXT STEP: Phase 3 Validation Gates — לאחר Ayal review על Phase 2

---

## DATE: 2026-05-03
## TASK: Layer 6 Phase 1 — Taxonomy Spec created
## SCOPE: Layer 6 — taxonomy planning only
## WHAT CHANGED:
- נוצר docs/organic/layer6-taxonomy-spec-v1.md
- 7 קטגוריות (CAT-A עד CAT-G), 61 allowed values
- Native Shopify tags policy, YAML_GAP policy, forbidden tags
- Phase 1 = planning only — אין Shopify write
## FILES TOUCHED:
- docs/organic/layer6-taxonomy-spec-v1.md (new)
## SYSTEM IMPACT:
- Layer 6 Phase 1 Taxonomy Spec CREATED — WAITING AYAL REVIEW
- Layer 6 execution NOT OPEN
- Shopify live: NO
## OPEN ISSUES:
- D1: legacy tags migration vs coexistence — ממתין לאייל
- D2: 3-6M6-9M (1 product) — ממתין לאישור
- D3: 124 YAML_GAP — timeline לא מוגדר
## NEXT STEP: Phase 2 Source Mapping — לאחר אישור אייל על Phase 1

---

## DATE: 2026-05-03
## TASK: Layer 6 Pre-Phase-1 Tag Cleanup — CL-1/CL-3
## SCOPE: Layer 6 — tag system prep
## WHAT CHANGED:
- הוסרו תגיות `Copy AI` (75 מוצרים) ו-`All categories` (3 מוצרים) מ-Shopify
- CL-2 (garbled Hebrew) = 0 — Phase 0 report היה שגוי, התגיות תקינות
- 76 מוצרים עודכנו בהצלחה — 0 שגיאות
- Verify: 76/76 PASS — כל תג תקין נשמר
## FILES TOUCHED:
- output/tags/pre-phase1-cleanup-backup.json
- output/tags/pre-phase1-cleanup-dryrun.json / .md
- output/tags/pre-phase1-cleanup-verify.json / .md
- output/tags/phase0-audit-report.md (הוסף סעיף 12)
## SYSTEM IMPACT:
- Shopify: 76 מוצרים נקיים מתגיות spurious
- Layer 6 Phase 0: COMPLETE + Cleanup COMPLETE
## OPEN ISSUES:
- A2: בחירת tag field (Native vs Metafields) — ממתין לאייל
- A3: אישור פתיחת Phase 1 (Taxonomy Spec) — ממתין לאייל
- A4: 124 active products ללא YAML — החלטה ממתינה
## NEXT STEP: Phase 1 Taxonomy Spec — לאחר אישור אייל

---

## מצב נוכחי (2026-03-25)

| HUB | נושא | מאמרים | סטטוס | GSC |
|-----|------|---------|--------|-----|
| HUB-1 | Baby Sleep | 5 | ✅ LIVE | ✅ |
| HUB-2 | Newborn Clothing | 6 | ✅ LIVE | ✅ |
| HUB-3 | Baby Bath | 5 | ✅ LIVE | ✅ |
| HUB-4 | Sensitive Skin | 5 | ✅ LIVE | ✅ |
| HUB-5 | Baby Gifts | 7 | ✅ LIVE | ✅ |
| HUB-6 | נעלי תינוק | 7 | ✅ LIVE | ⏳ GSC pending |
| HUB-7 | בטיחות תינוק | 6 | ✅ LIVE | ⏳ GSC pending |
| HUB-8 | — | — | ⏳ לא התחיל | — |

**Pipeline:** `11-topic-researcher → 03-blog-strategist → 04-blog-writer → 08-article-linker → publish`

---

## DATE: 2026-04-29
## TASK: Second-terminal live findings sync — GSC, redirects, SEO quality, billing, collections
## SCOPE: organic — documentation sync only. אין publishing, אין Shopify live, אין Layer 6.

## WHAT WAS CHECKED:
- Sitemap.xml (הוגש 21.4) + Google indexing status
- GSC indexing status per HUB (HUB-9 / HUB-10 / HUB-11)
- 301 redirects validation
- Google Cloud billing status + GSC service account
- Collection meta update (15 קולקציות)
- Product SEO quality (10-product report vs. Chozen + Shilav)
- Layer 3/4 quality audit — ציון 5.25/10
- GSC SEO opportunities (4 זיהויים)
- Duplicate content: בגדי-חורף-1
- Security: GSC verification token לא בשימוש

## LIVE FINDINGS:
| ממצא | סטטוס |
|------|--------|
| Sitemap.xml הוגש ל-GSC (2026-04-21) | ✅ — 460 דפים זוהו |
| HUB-9 GSC indexing | ✅ 7/7 submitted to index |
| HUB-10 GSC indexing | ⏳ 5/7 submitted (Pillar+C1-C4) — C5-C6 טרם |
| 53 redirects 301 הועלו ל-Shopify | ✅ validation 5/5 PASS |
| 311 דפי 404 הוגשו ל-GSC לאימות | ✅ |
| 15 קולקציות מטא עודכנו ב-Shopify | ✅ validation 5/5 PASS |
| 1/5 קולקציות הוגשה ל-GSC | ⏳ 4 נותרות |
| 10-product meta report נוצר | ✅ לא בוצע שינוי |
| Pink Noise article research | ✅ future idea only |

## INFRASTRUCTURE BLOCKERS:
| בלוק | סיבה | פעולה |
|------|------|--------|
| Google Cloud billing | Mastercard 0400 rejected — account terminated | אייל: חידוש |
| GSC service account | gsc-access@babymania-001 לא Owner ב-GSC | אייל: GSC Settings |
| ⇒ submit_gsc.py | לא אוטומטי עד שנפתרים | — |

## QUALITY FINDING:
- Layer 3/4 technically COMPLETE — ציון 5.25/10 vs. מתחרים (Chozen, Shilav)
- 244 כותרות מועמדות לשיפור — prompt קיים, לא בוצע
- 4 הזדמנויות GSC SEO זוהו — לא נפתחה עבודה
- תועד ב: docs/organic/seo-quality-backlog-2026-04-29.md
- Layer 3/4 סטטוס: COMPLETE טכנית — לא השתנה

## OPEN (פעולות אייל בלבד):
| פריט | עדיפות |
|------|--------|
| Google Cloud billing renewal | HIGH |
| Service account → GSC Owner | HIGH |
| HUB-10 GSC C5-C6 Manual Request Indexing | MEDIUM |
| HUB-11 GSC C2-C6 Manual Request Indexing | MEDIUM |
| 4 collections GSC indexing | MEDIUM |
| Duplicate content "בגדי-חורף-1" — מיזוג vs. תוכן ייחודי | MEDIUM |
| GSC verification token cleanup | LOW |

## NOT DOING NOW:
- לא מבצעים שיפור 244 כותרות (backlog only)
- לא פותחים B-03 / HUB חדש (ממתין לאישור אייל)
- לא פותחים Layer 6 (NOT OPEN)
- לא מריצים GSC automation (חסום)

## FILES TOUCHED:
- docs/organic/organic-journal.md (this entry)
- docs/organic/מצב-הפרויקט-האורגני.md (GSC status + open actions + sections 8+10+11)
- BABYMANIA-MASTER-PROMPT.md (HUB table + quality/blockers note)
- docs/organic/seo-quality-backlog-2026-04-29.md (CREATED)

## NEXT STEP:
אייל: חדש Google Cloud billing + הוסף service account כ-Owner ב-GSC.
לאחר מכן: Manual Request Indexing לHUB-10 C5-C6 + HUB-11 C2-C6 ב-GSC UI.

---

## DATE: 2026-04-29
## TASK: Layer 5 Gap Map Planning — הכרזת סגירה רשמית
## SCOPE: organic — Layer 5 Gap Map Planning closure declaration, documentation only

## WHAT CHANGED:
- **`docs/organic/layer5-gap-map-backlog.md`** — v1.3 → v1.4 | Gap Map Planning: CLOSED ✅
- **`docs/organic/מצב-הפרויקט-האורגני.md`** — Layer 5 status עודכן
- **`BABYMANIA-MASTER-PROMPT.md`** — Layer snapshot עודכן

## CLOSURE DECLARATION:
Layer 5 Gap Map Planning הוכרז סגור רשמית (2026-04-29).

| פרמטר | ערך |
|-------|-----|
| Gap Map items | 12 (G-01–G-12) |
| Backlog items | 12 (B-01–B-12) |
| DONE | 2: B-01 HUB-11 (7 מאמרים live), B-02 Post-HUB Linking Audit |
| WAITING | 10: B-03–B-12 |
| BLOCKED | 0 |
| Execution backlog | ACTIVE — פתוח לבחירה עתידית |
| Layer 6 | NOT OPEN |

## OPEN ACTIONS (לא חלק מסגירה זו):
- GSC C2-C6 Manual Indexing Request — פעולת אייל ב-GSC UI
- Product→Article live implementation (16 מוצרים) — ממתין T1 approval
- B-03 selection — ממתין אישור אייל (UNBLOCKED)
- G-12 reverse-index rebuild — MEDIUM priority, future execution

## NEXT STEP:
Layer 5 execution ממשיך. בחירת B-03 דורשת אישור אייל.
Layer 6 Opening Audit — משימה נפרדת, לא בוצעה.

---

## DATE: 2026-04-29
## TASK: Layer 5 — G-12/B-12 נוסף + הכנה לסגירת Gap Map Planning
## SCOPE: organic — Layer 5 Gap Map completion, documentation only

## WHAT CHANGED:
- **`docs/organic/layer5-gap-map-backlog.md`** — v1.2 → v1.3
  - G-12 נוסף: product-reverse-index.json rebuild v2.0 (System gap)
  - B-12 נוסף: MEDIUM priority, WAITING
  - סעיף 3a חדש: Layer 5 closure preparation summary
  - Gap Map: 12 גאפים | Backlog: 12 פריטים

## G-12 DETAILS:
- type: System gap
- gap: product-reverse-index.json v1.2 מכסה HUB-1–8 בלבד (25 מוצרים)
- missing: HUB-9 (Reborn), HUB-10 (Reborn Benefits), HUB-11 (Summer Clothing) — לא כלולים
- future scope: rebuild v2.0 לכלול ~50+ מוצרים נוספים, אימות מול internal_content_map v5.9+
- execution: NOT NOW — backlog item MEDIUM priority

## LAYER 5 STATUS:
- Gap Map Planning: READY FOR CLOSURE DECLARATION (לא סגור עדיין)
- Gap Map: 12 gaps (G-01–G-12) — כל קטגוריות הפערים הידועות מכוסות
- Backlog: 12 items (B-01–B-12) | DONE: 2 | WAITING: 10
- Layer 5 execution ממשיך (B-03 unblocked, ממתין לאישור אייל)

## NEXT STEP:
- Layer 5 Formal Closure Declaration — משימה נפרדת (T1 approval)
- B-03 selection — ממתין לאישור אייל

---

## DATE: 2026-04-29
## TASK: Layer 5 Gap Map — Future Product Gaps נוספו (B-09, B-10, B-11)
## SCOPE: organic — Layer 5 Gap Map completion, documentation only

## WHAT CHANGED:
- **`docs/organic/layer5-gap-map-backlog.md`** — v1.1 → v1.2
  - Gap Map: הוספו G-09 / G-10 / G-11 (Future Product Gaps)
  - Backlog: הוספו B-09 / B-10 / B-11
  - סעיף 3b חדש: Future Product Gaps מדיניות + פירוט לפי פריט

## FUTURE PRODUCT GAPS ADDED:
| פריט | קטגוריה | עדיפות |
|------|---------|--------|
| B-09 (G-09) | אביזרים לבובת ריבורן | HIGH |
| B-10 (G-10) | רחפן משחק | MEDIUM-HIGH |
| B-11 (G-11) | רובוט AI לילדים TOYA | HIGH |

## CONSTRAINTS:
- אין מוצרים live — אלה מוצרים מתוכננים בלבד
- ביצוע כל פריט מותנה ב-T1 approval + product data
- לא מעורבבים עם orphan products קיימים

## NEXT STEP:
- Layer 5 Gap Map Completion Audit — לאחר הוספת Future Gaps
- B-03 — בגדי שמחה / שמלות חגיגיות (UNBLOCKED — ממתין לאישור אייל)

---

## DATE: 2026-04-29
## TASK: B-02 — Post-HUB-11 Linking Audit COMPLETE + Product→Article Plan
## SCOPE: organic — HUB-11 post-publish audit, product mapping

## WHAT CHANGED:
- **B-02 סגור** — Post-HUB-11 Linking Audit הושלם
- **`docs/organic/hub11-product-to-article-plan.md` נוצר** — 16 מוצרים ממופו לעמודי מאמר HUB-11
- **`docs/organic/layer5-gap-map-backlog.md`** — B-02 סטטוס ⏳ WAITING → ✅ COMPLETE, B-03 UNBLOCKED

## AUDIT RESULTS SUMMARY:
| בדיקה | תוצאה |
|-------|-------|
| Article → Product | ✅ PASS — product_mention בכל 7 מאמרים |
| Product → Article | ✅ MAPPED — 16 מוצרים (ממתין T1 implementation) |
| Article → Article | ✅ PASS — cross-links תקינים |
| Hub → Hub | ✅ חלקי — 4 cross-hub links אומתו HTTP 200 |
| HTTP 200 verify | ✅ כל 7 URLs תקינים |
| GSC indexing | ⏳ PENDING — C2-C6 (פעולת אייל) |

## PRODUCT→ARTICLE MAPPING:
- C4 — שמלות קיץ: 5 מוצרים
- C2 — בגד ים: 3 מוצרים
- C5 — חליפת פשתן: 3 מוצרים
- C1 — הלבשת קיץ: 2 מוצרים
- C3 — כובע שמש: 1 מוצר
- C6 — בריכה: 1 מוצר
- Pillar: 1 מוצר

## WARNINGS:
- W-01: Pillar לא מקשר ל-C1–C6 (T1 נפרד)
- W-02: Pillar לא מקשר ל-HUB-5 (T1 נפרד)

## OPEN ACTIONS (פעולת אייל):
- GSC Manual Request Indexing — C2–C6 (5 URLs)
- T1 approval לפני Product→Article implementation ב-Shopify

## NEXT STEP:
- B-03 UNBLOCKED — בגדי שמחה / שמלות חגיגיות (אישור אייל לפני פתיחה)

---

## DATE: 2026-04-29
## TASK: Layer 5 Gap Map Backlog + Post-HUB Rule — תכנון ותיעוד
## SCOPE: organic — Layer 5 planning, no publishing

## WHAT CHANGED:
- **`docs/organic/layer5-gap-map-backlog.md` נוצר** — Gap Map מלא, Backlog ממוין (B-01–B-08), Post-HUB Linking Audit rule מוגדר
- **BABYMANIA-MASTER-PROMPT.md** — v4.8: Layer 5 FROZEN→OPEN, HUB-11 COMPLETE, map reference נוסף
- **`מצב-הפרויקט-האורגני.md`** — v2.7: Gap Map reference, Post-HUB rule, Layer 5 OPEN
- **`organic-journal.md`** — entry זה נוסף

## GAP MAP SUMMARY:
- 8 גאפים מזוהים (G-01–G-08)
- 8 פריטי Backlog (B-01–B-08)
- B-01 (HUB-11) = COMPLETE
- B-02 (Post-HUB-11 Audit) = WAITING — הבא

## POST-HUB RULE:
מוגדר ומחייב: HUB לא "סגור" עד שPost-HUB Linking Audit (Article→Product, Product→Article, Article→Article, Hub→Hub, HTTP 200, GSC) נסגר.

## NEXT STEP:
- B-02 — Post-HUB-11 Linking Audit (mapping בלבד, לא live edit)
- GSC Manual Indexing Request לC2-C6 — פעולת אייל

---

## DATE: 2026-04-29
## TASK: HUB-11 C2-C6 BATCH — כתיבה, QA, פרסום ואימות
## SCOPE: organic — HUB-11 C2–C6 batch publish (5 articles)

## WHAT CHANGED:
- **HUB-11 C2 נכתב ופורסם** — "בגד ים לתינוקת — איך לבחור, מה לבדוק ואיזה קרם הגנה להשתמש" | article_id: 686727070009 | HTTP 201+200 ✓
- **HUB-11 C3 נכתב ופורסם** — "כובע שמש לתינוק — למה זה חובה וכיצד לבחור נכון" | article_id: 686727528761 | HTTP 201+200 ✓
- **HUB-11 C4 נכתב ופורסם** — "שמלות קיץ לתינוקת — הדגמים הכי נוחים לחום הישראלי" | article_id: 686727790905 | HTTP 201+200 ✓
- **HUB-11 C5 נכתב ופורסם** — "חליפת פשתן לתינוק — היתרונות, איך לבחור ומתי ללבוש" | article_id: 686728216889 | HTTP 201+200 ✓
- **HUB-11 C6 נכתב ופורסם** — "בריכה עם תינוק — בטיחות, ציוד ושעות מומלצות" | article_id: 686728479033 | HTTP 201+200 ✓
- **QA כל 5 מאמרים** — 16/16 בדיקות PASS לכל מאמר | no style blocks, no hero, 2× figure.article-image

## URLS LIVE:
- C2: https://www.babymania-il.com/blogs/news/bgad-yam-letineket-eikh-livkhor-ma-livdok-ukrem-haganah
- C3: https://www.babymania-il.com/blogs/news/kovah-shemesh-letinok-lama-zeh-hova-vekheytsad-livkhor-nakhon
- C4: https://www.babymania-il.com/blogs/news/smlot-kayts-letineket-hadgamim-yoter-nonhim-lahom-hayisraeli
- C5: https://www.babymania-il.com/blogs/news/khalifat-pishtan-letinok-hayitronot-eikh-livkhor-umatay-lilbosh
- C6: https://www.babymania-il.com/blogs/news/brekha-im-tinok-bitakhon-tsiyud-ushahot-hamumlatsot

## SYSTEM IMPACT:
- מאמרים live: 68 (63 + C2 + C3 + C4 + C5 + C6)
- HUB-11: 7/7 COMPLETE
- hub-registry.json: HUB-11 status → complete
- internal_content_map.json: v5.9 עם כל 7 מאמרי HUB-11

## NEXT STEP (פעולת אייל):
- GSC Manual Request Indexing לכל 5 URLs: C2–C6

---

## DATE: 2026-04-29
## TASK: HUB-11 C1 — כתיבה, QA, פרסום ואימות
## SCOPE: organic — HUB-11 C1 article publish

## WHAT CHANGED:
- **HUB-11 C1 נכתב** — "איך להלביש תינוק בקיץ — המדריך לפי גיל, חום ושעות היום"
- **QA עבר** — 16/16 בדיקות PASS | tip-box×2, warning-box×1, pull-quote×1, product-mention×2, FAQ×4, JSON-LD ✓
- **פורסם ל-Shopify** — POST HTTP 201 | article_id: 686705443129 | blog_id: 109164036409
- **URL אומת** — HTTP 200 ✓
- Internal links: → HUB-11 Pillar ✓ | → HUB-7-C3 (overheating) ✓

## ARTICLE DETAILS:
- Title: איך להלביש תינוק בקיץ — המדריך לפי גיל, חום ושעות היום
- URL: https://www.babymania-il.com/blogs/news/eikh-lhalbisht-tinok-bakayts-madrikh-lfi-gil-khom-ushaot
- article_id: 686705443129
- Products: סרבל קיצי (9605887689017) + חליפת קיץ 1977 (9179159888185)

## SYSTEM IMPACT:
- מאמרים live: 63 (61 + Pillar + C1)
- HUB-11: 2/7 live

## NEXT STEP:
- T1 — HUB-11 C2 בתור

---

## DATE: 2026-04-28
## TASK: HUB-11 Pillar — כתיבה, QA, פרסום ואימות
## SCOPE: organic — HUB-11 Pillar article publish

## WHAT CHANGED:
- **HUB-11 Pillar נכתב** — 4 H2 sections, ~1,700 מילים, Presentation Spec v3.0 LOCKED
- **QA עבר** — tip-box×2, warning-box×1, pull-quote×1, product-mention×2, FAQ×4, JSON-LD ✓
- **פורסם ל-Shopify** — POST HTTP 201 | article_id: 686702362937 | blog_id: 109164036409
- **URL אומת** — HTTP 200 ✓

## FILES TOUCHED:
- `output/hub11-summer-clothing/HUB11_Pillar_blog_article.html` — מאמר Pillar (NEW)
- `output/hub11-summer-clothing/HUB11_Pillar_PUBLISH_RESULT.json` — publish result (NEW)
- `publish_hub11_pillar.py` — publish script (NEW)
- `teams/organic/hub-registry.json` — HUB-11-Pillar status: planned → live, article_id + live_url נוספו

## ARTICLE DETAILS:
- Title: בגדי קיץ לתינוק — המדריך המלא: מה ללבוש, מה לקחת לים ואיך לבחור נכון
- URL: https://www.babymania-il.com/blogs/news/bgdey-kayts-letinok-madrikh-male-ma-lilbosh-ma-lakakhat-layam
- article_id: 686702362937
- Target keyword: בגדי קיץ לתינוק
- Products: שמלת שמש (9605887590713) + סט Breeze™ (10025300853049)

## SYSTEM IMPACT:
- HUBs live: 10 | מאמרים live: 62 (61 + Pillar HUB-11)
- HUB-11 Pillar: LIVE 2026-04-28

## OPEN ISSUES:
- [ ] GSC Manual Request Indexing — HUB-11 Pillar URL
- [ ] HUB-11 C1-C6 — נשאר 6 מאמרים להשלמת HUB

## NEXT STEP:
- T1 — כתיבת HUB-11 C1: איך להלביש תינוק בקיץ
- GSC Request Indexing לאחר C1-C6 live

---

## DATE: 2026-04-28
## TASK: HUB-11 — רישום רשמי — Layer 5
## SCOPE: organic — HUB-11 planning registration

## WHAT CHANGED:
- HUB-11 נרשם רשמית ב-hub-registry.json כ-**בגדי קיץ לתינוק**
- Layer 5 נפתח רשמית (אישור אייל 2026-04-28) לאחר Gap Map Audit PASS + HUB Selection Audit PASS
- 7 מאמרים מתוכננים: Pillar + C1-C6
- 17+ מוצרים orphan ימופו לתוכן תומך

## HUB-11 PLAN:
- Pillar: בגדי קיץ לתינוק — המדריך המלא
- C1: איך להלביש תינוק בקיץ
- C2: בגד ים לתינוקת — איך לבחור
- C3: כובע שמש לתינוק — למה זה חובה
- C4: שמלות קיץ לתינוקת — מה ההבדל
- C5: חליפת פשתן לתינוק — למה הבחירה הכי חכמה
- C6: בריכה עם תינוק — הציוד שצריך

## FILES TOUCHED:
- `teams/organic/hub-registry.json` — HUB-11 entry נוסף, next_hub עודכן
- `docs/organic/מצב-הפרויקט-האורגני.md` — HUB-11 row נוסף לטבלה, section 5 עודכן
- `docs/organic/organic-journal.md` — entry זה
- `BABYMANIA-MASTER-PROMPT.md` — HUBs table עודכן

## SYSTEM IMPACT:
- HUBs registered: 11 | HUBs live: 10 | מאמרים live: 61
- hub-registry: next_hub = HUB-11 PLANNED
- Layer 5: OPEN — Gap Map PASS → HUB Selection PASS → Registration PASS

## OPEN ISSUES:
- [ ] GSC Manual Request Indexing — 7 URLs HUB-10 (ידני ב-GSC UI)
- [ ] HUB-11 article generation — T1 task הבא

## NEXT STEP:
- T1 — כתיבת Pillar HUB-11 (agent pipeline: 11 → 03 → 04 → 08 → publish)
- לאחר Pillar LIVE: C1 בראשית, לפי writing_order

---

## DATE: 2026-04-28
## TASK: HUB-10 C6 — live polish
## SCOPE: organic — C6 article post-publish fix

## WHAT CHANGED:
- שגיאת כתיב: "עקבות" → "עקביות" (חסרה אות י) — תוקנה ב-Shopify live
- תמונת featured/hero: null → Sc65457105edf484ab6d358f635cf3d31V.webp (CDN HTTP 200)
- Shopify PUT: HTTP 200 | article 686682571065 | body_len 12015 | published_at ללא שינוי
- API GET verify: typo_fixed ✓ | old_typo_gone ✓ | no_hero_inline_style ✓

## FILES TOUCHED:
- `output/hub10-reborn-benefits/HUB10_C6_blog_article.html` (typo fixed local)
- `output/hub10-reborn-benefits/HUB10_C6_POLISH_RESULT.json` (result log — new)

## SYSTEM IMPACT:
- C6 live: כתיב מתוקן, featured image מוגדר — תמונות גוף ללא שינוי (img1+img2 HTTP 200)

## OPEN ISSUES: none — polish complete
## NEXT STEP:
- GSC Manual Request Indexing — 7 URLs של HUB-10 (ידני ב-GSC UI)
- HUB-11: בחירת נושא (TBD)

---

## DATE: 2026-04-28
## TASK: HUB-10 — סגירה תיעודית — ALL LIVE
## SCOPE: organic — HUB-10 closure docs

## WHAT CHANGED:
- HUB-10 נסגר: 7 מאמרים ALL LIVE ב-2026-04-28
- internal_content_map.json עודכן → v5.7 (61 מאמרים)
- hub-registry.json: status planned → published, clusters array הוסף
- GSC: pending_manual_request — נדרש Manual Request Indexing ידני ב-GSC UI

## LIVE ARTICLES:
| מאמר | article_id | handle | published_at |
|---|---|---|---|
| Pillar | 686621098297 | yitronot-bobat-reborn-leyladim-regshiyim-chevratiyim-histapdutiyim | 2026-04-28T10:18:19+03:00 |
| C1 | 686651507001 | bobat-reborn-intelignatzia-regshit-mishak | 2026-04-28T12:42:34+03:00 |
| C2 | 686673527097 | reborn-bitachon-chevrati-yeladim-mehussim | 2026-04-28T13:47:28+03:00 |
| C3 | 686676443449 | gil-matim-lebobat-reborn | 2026-04-28T13:56:00+03:00 |
| C4 | 686676541753 | bobat-reborn-empathia-yeladim | 2026-04-28T14:02:06+03:00 |
| C5 | 686678147385 | bobat-reborn-yeled-ragish | 2026-04-28T14:13:47+03:00 |
| C6 | 686682571065 | reborn-achrayut-yeladim | 2026-04-28T14:27:38+03:00 |

## FILES TOUCHED:
- `docs/organic/organic-journal.md` (this entry)
- `docs/organic/מצב-הפרויקט-האורגני.md` (HUB-10 row → ALL LIVE, totals updated)
- `teams/organic/hub-registry.json` (HUB-10 status → published, clusters added)

## SYSTEM IMPACT:
- HUBs live: 10 | מאמרים live: 61
- internal_content_map: v5.7
- hub-registry: last_published = HUB-10 ALL LIVE, next_hub = HUB-11 (TBD)

## OPEN ISSUES:
- [ ] GSC Manual Request Indexing — נדרש ידנית ב-GSC UI עבור 7 URLs של HUB-10

## NEXT STEP:
- GSC UI → Request Indexing לכל 7 URLs של HUB-10
- HUB-11: בחירת נושא (TBD)

---

## DATE: 2026-04-28
## TASK: HUB-10 — הגדרת נושא + תכנון רשמי
## SCOPE: organic — HUB-10 direction decision

## WHAT CHANGED:
- HUB-10 הוגדר רשמית כ-**יתרונות בובת הריבורן לילדים**
- "רשימת קניות לתינוק" נדחה לצמיתות — החנות לא מוכרת ציוד כללי (עריסות, עגלות וכד')
- הרחבת topical authority על ריבורן — ממשיכה מ-HUB-9 לעומק פסיכולוגי/התפתחותי

## DECISION RATIONALE:
- HUB-9 כבר מכסה: בחירה, ביגוד, מתנה, טיפול, השוואה, גיל
- מה שחסר (ומה שהורה מהסס מחפש): **למה הריבורן טוב לילד שלי?**
- keywords חדשים: "בובת ריבורן אינטליגנציה רגשית", "ריבורן ביטחון עצמי", "גיל מתאים לבובת ריבורן"
- product bridge: 6 PIDs ריבורן קיימים → CTA: /search?q=ריבורן
- cross-links: ↔ HUB-9 Pillar + HUB-9 C1 + HUB-9 C5

## APPROVED PLAN:
- Pillar: "בובת ריבורן לילדים — יתרונות רגשיים, חברתיים והתפתחותיים"
- C1: בובת ריבורן ואינטליגנציה רגשית — מה פסיכולוגים אומרים [PRIORITY]
- C2: ריבורן וביטחון חברתי — איך הבובה עוזרת לילדים מהוססים
- C3: מאיזה גיל בובת ריבורן מתאימה — מדריך לפי שלב התפתחותי
- C4: בובת ריבורן ואמפתיה — ילדים שלומדים לדאוג לאחרים
- C5: בובת ריבורן לילד רגיש — למה זה עובד
- C6: ריבורן ואחריות — מה הבובה מלמדת ילדים

## FILES TOUCHED:
- `teams/organic/hub-registry.json` (HUB-10 added)
- `docs/organic/מצב-הפרויקט-האורגני.md` (HUB-10 table + LAYER 10 + next step)
- `docs/organic/organic-journal.md` (this entry)

## BLOCKERS BEFORE WRITING:
- [ ] תקן agent 04: מחק PART A hero מ-body_html (מתנגש עם QA Rule 9)
- [ ] עדכן internal_content_map.json → v5.0 עם HUB-9 Pillar + C1-C6

## OPEN ISSUES: none — planning complete
## NEXT STEP: תקן blockers → כתוב HUB-10 Pillar

---

## DATE: 2026-04-23
## TASK: HUB-9 Clusters C1-C6 פרסום
## SCOPE: organic — HUB-9 Reborn cluster content

## WHAT CHANGED:
- C2 (בגדי ריבורן) — article_id 686018724153, LIVE
- C1 (איך לבחור בובת ריבורן) — article_id 686018756921, LIVE
- C3 (ריבורן כמתנה) — article_id 686018789689, LIVE
- C4 (טיפול בריבורן) — article_id 686018822457, LIVE
- C5 (ריבורן לילדים vs. אספנים) — article_id 686018855225, LIVE
- C6 (השוואת ריבורן) — article_id 686018887993, LIVE
- Pillar + C1-C6: [CLUSTER-URL:Cx] + [HUB-2-PILLAR-URL] placeholders resolved, PUT back to Shopify

## FILES TOUCHED:
- `output/hub9-reborn/HUB9_Pillar_blog_article.html` (placeholders resolved)
- `output/hub9-reborn/HUB9_C1_blog_article.html` through `HUB9_C6_blog_article.html`
- `teams/organic/hub-registry.json` (C1-C6 added, next_hub=HUB-10)
- `docs/organic/מצב-הפרויקט-האורגני.md` (HUB-9 row updated)
- `docs/organic/organic-journal.md` (this entry)
- `docs/management/management-journal.md`

## SYSTEM IMPACT:
- HUB-9 fully complete: 7 articles LIVE (Pillar + 6 Clusters)
- Internal links resolved — no dead placeholders in Shopify content
- Total live articles: 54

## OPEN ISSUES: GSC Manual Request Indexing pending (C1-C6) — requires GSC UI
## NEXT STEP: HUB-10

---

## DATE: 2026-04-20
## TASK: GSC integration + submit HUB-8 + HUB-9
## SCOPE: organic — post-publish GSC flow

## WHAT CHANGED:
- `scripts/submit_gsc.py` נוצר ושוכתב — URL Inspection API (webmasters scope)
- **API CAPABILITY PROVEN:** inspection_only — `urlInspection.index()` contains only `inspect`. No `requestIndexing` method exists anywhere in Search Console API v1.
- post-publish flow עודכן: publish → verify → GSC inspect (script) → Request Indexing (GSC UI, ידני) → docs
- ניסיון submit ל-HUB-8 + HUB-9 Pillar — נחסם 403 Forbidden

## GSC RUN RESULT:
- HUB-8 Pillar: **no_access** — 403 Forbidden
- HUB-9 Pillar: **no_access** — 403 Forbidden

## ROOT CAUSE:
Service account `gsc-access@babymania-001.iam.gserviceaccount.com` אינו מורשה על property `babymania-il.com` ב-GSC.
הסקריפט תקין — הבעיה היא הרשאת GSC בלבד.

## FIX REQUIRED:
GSC → babymania-il.com → Settings → Users and permissions → Add user:
`gsc-access@babymania-001.iam.gserviceaccount.com` → Owner

## FILES TOUCHED:
- `scripts/submit_gsc.py` (new)
- `docs/organic/מצב-הפרויקט-האורגני.md` (post-publish flow + GSC blocker)
- `docs/organic/organic-journal.md`

## OPEN ISSUES:
- [ ] Add service account as Owner in GSC → then re-run `python scripts/submit_gsc.py <url>`

## NEXT STEP:
- הוסף service account ל-GSC → הרץ שוב את הסקריפט עבור HUB-8 + HUB-9

---

## DATE: 2026-04-20
## TASK: HUB-9 Pillar PUBLISH + GSC manual Request Indexing complete — HUB-8 + HUB-9
## SCOPE: organic — publish, GSC post-publish flow complete

## WHAT CHANGED:
- HUB-9 Pillar פורסם ל-Shopify: article_id=685558825273, published_at=2026-04-20T11:16:25+03:00
- `scripts/submit_gsc.py` שוכתב ל-URL Inspection API — הוכח: inspection only, ללא request indexing
- HUB-8 + HUB-9: inspection רץ (result: unknown) → Manual Request Indexing בוצע ב-GSC UI
- gsc_status עודכן ל-`gsc_manual_requested` בshub-registry.json + כל מסמכי המקור
- Pipeline line עודכן: `11 → 03 → 04 → 08 → publish → verify → GSC inspect → manual Request Indexing → docs update`

## GSC RESULT (2026-04-20):
- HUB-8 (6 URLs): result=unknown → Manual Request Indexing completed
- HUB-9 Pillar (1 URL): result=unknown → Manual Request Indexing completed

## FILES TOUCHED:
- `publish_hub9_pillar.py` (new)
- `output/hub9-reborn/HUB9_Pillar_blog_article.html` (2 fixes: FAQ id, CTA href)
- `scripts/submit_gsc.py` (rewritten — URL Inspection API)
- `teams/organic/hub-registry.json` (HUB-9 pillar added, gsc_status → gsc_manual_requested)
- `docs/organic/מצב-הפרויקט-האורגני.md` (HUB-8 + HUB-9 GSC column)
- `BABYMANIA-MASTER-PROMPT.md` (pipeline + HUBs table GSC column)
- `docs/management/update-policy.md` (Post-Publish Flow, status table)

## SYSTEM STATE:
- HUBs LIVE: 9 (HUB-1 through HUB-9 Pillar)
- מאמרים live: 48
- HUB-8: published + gsc_manual_requested ✅
- HUB-9: Pillar published + gsc_manual_requested ✅ | C1-C6 pending

## OPEN ISSUES:
- [ ] HUB-9 Clusters C1-C6 — כתיבה + פרסום (C2 עדיפות: בגדי ריבורן pos 1.5)
- [ ] [CLUSTER-URL:C1-C6] placeholders ב-Pillar — יעודכנו כשהקלאסטרים יפורסמו
- [ ] HUB-6 + HUB-7 Manual Request Indexing — נדחה (לא דחוף)

## NEXT STEP:
- HUB-9 C2 "בגדי ריבורן" — כתיבה + פרסום (C2 = priority, pos 1.5)

---

## DATE: 2026-04-20
## TASK: HUB-9 — בחירת נושא + הגדרה רשמית
## SCOPE: organic — HUB-9 direction decision

## WHAT CHANGED:
- HUB-9 הוגדר רשמית כ-**בובת ריבורן** — שינוי מכיוון קודם "רשימת קניות לתינוק"
- hub-registry.json עודכן: HUB-9 סטטוס "planned", Pillar + 6 clusters מוגדרים
- מצב-הפרויקט-האורגני.md עודכן: HUB-9 מופיע בטבלה ובסעיף LAYER 2b

## DECISION RATIONALE:
- Reborn = קטגוריה #1 בחנות לפי GSC: בובת ריבורן pos 2.7, בגדי ריבורן pos 1.5
- 6 מוצרי Reborn קיימים עם SEO Layer 3 מלא — ללא HUB תומך כלל
- Shopping checklist (pos 36) נדחה ל-HUB-10

## APPROVED PLAN:
- Pillar: "בובת ריבורן — המדריך המלא: מה זה, איך לבחור ולמי זה מתאים"
- C1: איך לבחור בובת ריבורן — מדריך לרוכש הראשון
- C2: בגדי ריבורן — מה לובשים ואיפה מוצאים [PRIORITY — pos 1.5]
- C3: בובת ריבורן כמתנה — מי זה מתאים לו ומה לבקש
- C4: איך לטפל בבובת ריבורן — שמירה, ניקוי, אחסון
- C5: ריבורן לילדים vs. ריבורן לאספנים — מה ההבדל
- C6: השוואת בובות ריבורן — מידות, חומרים, מחירים

## FILES TOUCHED:
- `teams/organic/hub-registry.json` (v2.0 → HUB-9 added)
- `docs/organic/מצב-הפרויקט-האורגני.md` (v2.5 → HUB-9 table + LAYER 2b)

## SYSTEM IMPACT:
- HUB-9 מוגדר ומתועד — ממתין ל-execution plan

## OPEN ISSUES:
- [x] execution plan לכתיבת Pillar HUB-9 Reborn — הושלם
- [x] כתיבת Pillar HUB-9 Reborn — הושלמה 2026-04-20
- [ ] QA + cluster links resolution ([CLUSTER-URL:C1–C6])
- [x] image placeholders resolution — הושלם 2026-04-20

## NEXT STEP:
- QA על ה-Pillar + אישור לפרסום

---

## DATE: 2026-04-20
## TASK: HUB-9 Reborn Pillar — פרסום
## SCOPE: organic — HUB-9 pillar publish

## WHAT CHANGED:
- `output/hub9-reborn/HUB9_Pillar_blog_article.html` פורסם ל-Shopify blog
- article_id: 685558825273
- handle: bobat-reborn-madrih-male-ma-ze-ech-livhor
- url: https://babymania-il.com/blogs/news/bobat-reborn-madrih-male-ma-ze-ech-livhor
- published_at: 2026-04-20T11:16:25+03:00

## FILES TOUCHED:
- `teams/organic/hub-registry.json` (status: planned → published, pillar object added)
- `docs/organic/organic-journal.md`
- `docs/organic/מצב-הפרויקט-האורגני.md`
- `publish_hub9_pillar.py` (new — single-use publish script)

## SYSTEM IMPACT:
- HUB-9 Pillar LIVE — 8 HUBs now published
- cluster C1-C6 remain pending (placeholders [CLUSTER-URL:Cx] in article)

## OPEN ISSUES:
- [ ] GSC indexing HUB-9 Pillar — pending (not executed yet)
- [ ] Cluster C1-C6 writing + publishing
- [ ] Resolve [CLUSTER-URL:C1-C6] internal links after clusters go live

## NEXT STEP:
- GSC: submit HUB-8 + HUB-9 Pillar for indexing

---

## DATE: 2026-04-20
## TASK: HUB-9 Reborn Pillar — כתיבה
## SCOPE: organic — HUB-9 pillar article

## WHAT CHANGED:
- `output/hub9-reborn/HUB9_Pillar_blog_article.html` — נכתב, READY_FOR_REVIEW
- hub-registry.json: pillar_file + pillar_status הוסף

## ARTICLE METADATA:
- כותרת: "בובת ריבורן — המדריך המלא: מה זה, איך לבחור ולמי זה מתאים"
- handle מוצע: bobat-reborn-madrih-male-ma-ze-ech-livhor
- keyword ראשי: "בובת ריבורן" (pos 2.7)
- ~2100 מילים, 8 sections, 7 product cards, 5 FAQ, cluster nav מלא

## KEYWORD OWNERSHIP:
- Pillar: "בובת ריבורן", "ריבורן מה זה", חומרים/מידות ✅
- C2: S5 teaser 2 שורות + link בלבד ✅
- C1/C5: teasers בלבד ✅
- C6: טבלת השוואה ללא מחירים/ranking ✅

## FILES TOUCHED:
- `output/hub9-reborn/HUB9_Pillar_blog_article.html` (new)
- `teams/organic/hub-registry.json`
- `docs/organic/organic-journal.md`

## NEXT STEP:
- QA על ה-Pillar לפני publish

---

## DATE: 2026-04-14
## TASK: LAYER 3 — Product SEO/AEO complete + route-a closure
## SCOPE: organic — product SEO layer, plan execution, live push

## WHAT CHANGED:
- Plan `layer3-product-seo-aeo-priority-001` הושלם — 18 stages, PASS
- 244 מוצרים עודכנו live ב-Shopify: `global.title_tag` + `global.description_tag`
  - Reborn dolls: 6 | Baby shoes: 13 | Clothing: 219 | Accessories: 6
- route-a נסגר: shoes rollout + LAYER 2 (Product↔Blog) + LAYER 3 (SEO/AEO)
- LAYER 2 נסגר (2026-04-13) — clothing + shoes, 66 מוצרים LIVE

## OPERATIONAL NOTES:
- STAGE-7 (shoes gen): נכשל פעמיים בגלל rate limit, עבר בריצה שלישית
- STAGE-9 (clothing gen): timeout פעמיים, recovery ידני 5 batches (B1-B5) — 115 drafts
- STAGE-11 (accessories gen): timeout, recovery micro-task בודד (babysleep-pro)
- STAGE-16 (live verify): 29 failures → גילוי 124 missing drafts → generation recovery (B1-B5) → re-push → 244/244 PASS
- No theme changes. No YAML changes.

## FILES TOUCHED:
- `bridge/conductor-state.md`
- `output/stage-outputs/*_seo_draft.json` (244 files)
- `docs/organic/מצב-הפרויקט-האורגני.md`
- `BABYMANIA-MASTER-PROMPT.md` (v3.0)

## SYSTEM IMPACT:
- 244 מוצרים BabyMania עם SEO title + meta description live
- READY_FOR_LAYER_4 = YES

## OPEN ISSUES:
- [ ] GSC confirmation HUB-6 + HUB-7 + HUB-8
- [ ] GSC backlog — PLANNED ONLY

## NEXT STEP:
- LAYER 4 — GEO (AI answers: Perplexity, ChatGPT, Gemini)

---

## DATE: 2026-03-25
## TASK: HUB-7 פרסום
## SCOPE: organic — HUB-7 בטיחות תינוק

## WHAT CHANGED:
- HUB-7 (בטיחות תינוק) פורסם — 6 מאמרים
- internal linking בוצע

## FILES TOUCHED:
- `teams/organic/hub-registry.json` (עודכן)

## SYSTEM IMPACT:
- 7 HUBs live, GSC ב-HUB-6/7 ב-indexing

## OPEN ISSUES:
- [ ] HUB-8 — נושא טרם נבחר
- [ ] GSC confirmation HUB-6 + HUB-7

## NEXT STEP:
- בחירת נושא HUB-8
- מעקב GSC על HUB-6 + HUB-7

---

## DATE: 2026-03-24
## TASK: HUB-6 פרסום
## SCOPE: organic — HUB-6 נעלי תינוק

## WHAT CHANGED:
- HUB-6 (נעלי תינוק) פורסם — 7 מאמרים

## FILES TOUCHED:
- `teams/organic/hub-registry.json`

## SYSTEM IMPACT:
- cross-link בין HUB-6 (אורגני) לshoes pipeline (מוצר)

## OPEN ISSUES: GSC indexing pending
## NEXT STEP: HUB-7

---

## DATE: 2026-03-20
## TASK: HUB-5 פרסום
## SCOPE: organic — HUB-5 Baby Gifts

## WHAT CHANGED:
- HUB-5 (Baby Gifts) פורסם — 7 מאמרים
- מוצרי מתנה מחוברים: Lino™ set, LUMI™ romper

## FILES TOUCHED:
- `teams/organic/hub-registry.json`

## SYSTEM IMPACT: GSC confirmed ✅
## OPEN ISSUES: none
## NEXT STEP: HUB-6

---

## REFERENCE: NIGHT_EXECUTION_PLAN.md (Historical)
קובץ `NIGHT_EXECUTION_PLAN.md` ב-root מכיל תוכנית ביקורת אורגנית מ-6 שלבים.
**סטטוס:** היסטורי — בוצע חלקית. לא לעדכן.
**להמשיך מ-PHASE 4 ואילך** אם נדרש audit אורגני נוסף.
