task_id: 20260327-023815
round: 1
---
Done. Changes made to `source-of-truth.md`:

1. **Management table** — added `management-index.md` and `management-journal.md`
2. **Bridge table** — added `.github/workflows/claude-bridge.yml`, `bridge-runtime-status.md`, `telegram-channel-design.md`
3. **Team Lead routing rule** — updated to match master prompt: CLI syntax (`team_lead.py --task ... [--dry-run]`), full verdict list, `stage / round / verdict` in runtime-state
4. **Watchdog block** — added full spec (`--daemon`, `--warn 60`, `--stuck 180`, behavior)
5. **Startup block** — added `start-bridge.bat` flow (watchdog + bridge)
6. **Product Pipeline table** — added `knowledge/copywriting/`, `prompts/`, `shared/knowledge/`, `shared/schemas/`
