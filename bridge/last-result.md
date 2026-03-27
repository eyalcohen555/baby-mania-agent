task_id: 20260327-023647
round: 1
---
Done. Updated `docs/management/source-of-truth.md` to match Master Prompt v2.0. Key changes:

1. **Team Lead routing** — added dedicated section with `teams/team-lead/team_lead.py` as source of truth (replaces old `00-team-lead/orchestrator.py`)
2. **Approval Tiers routing rule** — added T0–T3 table with bridge behavior
3. **Bridge section expanded** — added runtime-state.md, task-log.md, telegram-response.md, watchdog-report.md
4. **Agent paths fixed** — `teams/product/agents/` and `teams/organic/agents/` (not `.claude/agents/`)
5. **Product context fixed** — `shared/product-context/*.yaml` (not `output/stage-outputs/`)
6. **DEPRECATED section expanded** — added old orchestrator.py, config.yaml, .claude/agents/, output/stage-outputs/
7. **Added missing sections** — Theme Assets, Shopify Config, management docs table
