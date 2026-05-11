task_id: 20260511-185041
---
STAGE_VERDICT: PASS

EVIDENCE:
- Plan written to `output/navigation/navigation-fix-plan.md` (read-only deliverable, no theme/menu writes).
- Source data captured at `output/navigation/current-menus-raw.json` (5 menus, 17 items in main-menu).
- All required sections present: PROPOSED_STRUCTURE (6 top-level parents, depth 2), ITEMS_TO_REMOVE (5), ITEMS_TO_ADD (6), URL_CHANGES (12 slug changes + footer), TIER_REQUIRED: T3, AYAL_APPROVAL: YES.
- Files touched: only `output/navigation/*` (allowed). No edits to `bridge/next-task.md`, `templates/*.json`, `sections/*.liquid`, `.env`.

SYSTEM STATE:
- Menus snapshot saved (rollback source).
- Navigation fix plan staged and awaiting Ayal T3 approval before any Shopify menu/slug write.
- Hard dependency flagged: shoe sub-collections (`/collections/shoes/*`) cannot be wired until the tagging track (`tagging-continuation-from-issue-3-001`) completes.
- Next executable step (post-approval): hardcoded-URL audit across `templates/*.json`, `sections/*.liquid`, blog HTML, and external surfaces (Meta feed, Klaviyo, GMC) before any slug change.