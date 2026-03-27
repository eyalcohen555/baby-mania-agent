task_id: 20260327-021009
round: 1
---
File looks correct. Here's a summary of all changes made:

**BABYMANIA-MASTER-PROMPT.md v1.2 → v2.0**

Changes made to match the real system:

1. **Roles section** — Added Team Lead (`team_lead.py`) and Watchdog (`watchdog.py`) as real system actors with their actual verdicts (PASS/RETRY/BLOCKED/FAILED_EMPTY/etc.)

2. **Documents table** — Added 3 missing docs: `approval-policy.md`, `team-lead-agent-design.md`, `team-lead-input-model.md`, `telegram-channel-design.md`

3. **Directory structure** — Added full real tree showing `bridge/`, `teams/`, `shared/` (234 product contexts), `knowledge/`, `prompts/`, `theme_assets/` with actual file counts

4. **Bridge section** — Completely rewritten:
   - Local daemon is now primary (was "fallback"), with polling interval (4s), singleton lock, approval tier parsing
   - Added Telegram integration flow (needs_response → telegram-response.md → re-run)
   - Added startup flow (start-bridge.bat → watchdog + bridge)
   - Added all 11 bridge files (was 5)
   - Added Approval Tiers table (T0–T3) with bridge behavior
   - Added Team Lead and Watchdog sections with real CLI usage

5. **Product agents** — Fixed to match actual 17 files in `teams/product/agents/`: removed phantom `01c`, `02b-clothing-thinking`, `02b-shoes-thinking`, `09-page-validator`; added `04-shoes-validator`, `08-section-expert`, `ad-script-writer`, `product-page-builder`, `seo-specialist`, `winning-product-scout`

6. **Organic agents** — Added full table of all 13 agents in `teams/organic/agents/` (was missing entirely). Added hub-registry.json reference

7. **Theme assets** — Added organized table of all 20 Liquid sections (clothing/shoes/blog/shared) + templates

8. **Shoes status** — Simplified to current state (removed stale commit hashes and closed items)

9. **Task format** — Added mandatory `APPROVAL_TIER` field

10. **Security rules** — Added rule #8 (no Shopify MCP), added Shopify Config block with shop URL, theme ID, token path, metafields namespace, sections path
