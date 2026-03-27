task_id: 20260327-024529
---
Both fixes applied:

**source-of-truth.md** — Fixed watchdog CLI defaults from `--warn 60 --stuck 180` to `--warn 120 --stuck 300` (matches actual code in `watchdog.py` lines 37-38).

**management-index.md** — Added 12 missing entries:
- 6 bridge runtime files (`runtime-state.md`, `watchdog-report.md`, `next-task.md`, `last-result.md`, `task-log.md`, `telegram-response.md`)
- `telegram-channel-design.md`
- New "Team Lead & Watchdog" section with `team_lead.py`, `watchdog.py`, `approval-policy.md`, `team-lead-agent-design.md`, `team-lead-input-model.md`

**Verification summary:**
- Watchdog code defaults: `WARN=120s`, `STUCK=300s`, `POLL=30s` — all now correctly documented
- `start-bridge.bat` uses `--daemon` only (no overrides) — code defaults are the runtime values
- `runtime-state.md` and `status.md` task IDs match (`20260327-024413`) — bridge is consistent
- `watchdog-report.md` is stale from previous task (`20260327-023815`) — expected, since watchdog only writes when warn threshold exceeded