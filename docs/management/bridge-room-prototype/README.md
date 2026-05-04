# Bridge Room V1 — Safe Prototype

**STATUS:** PROTOTYPES 1–3, 5–6 CLOSED — ALL PASSED  
**CLOSURE DOC:** [PROTOTYPE-CLOSURE.md](PROTOTYPE-CLOSURE.md)  
**APPROVAL TIER:** T1  
**LAYER:** 1  
**LAST UPDATED:** 2026-05-03

> **READY FOR SAFE NEXT DESIGN: YES**
> **READY FOR FULL IMPLEMENTATION: NO — Telegram/runtime integration not approved**

---

## Purpose

This directory is a fully isolated, mock-only prototype demonstrating the Bridge Room V1 loop.  
No files here connect to `bridge.py`, `scripts/`, `teams/`, or any live system.

---

## Roles

| Role | Actor | Responsibility |
|------|-------|----------------|
| Controller / Reviewer | Codex | Issues commands, reviews output, decides verdict |
| Executor | Claude | Receives commands, executes task, returns output |

---

## Scenario: AUDIT → RETEST

```
[Codex]  ──AUDIT command──►  outbox/claude-command.json
                                        │
                                   [Claude reads]
                                        │
                                        ▼
                            inbox/claude-output.json  ◄── Claude writes result
                                        │
                                   [Codex reviews]
                                        │
                                        ▼
                            codex-verdict.json  ◄── verdict: RETEST
                                        │
                              journal/stage-log.jsonl  ◄── full trace
```

### Stage Sequence

1. **INIT** — Room opens, state = `WAITING_COMMAND`
2. **AUDIT_ISSUED** — Codex writes command to `outbox/`
3. **AUDIT_IN_PROGRESS** — Claude picks up command, state = `EXECUTING`
4. **AUDIT_COMPLETE** — Claude writes result to `inbox/`, state = `AWAITING_VERDICT`
5. **VERDICT_ISSUED** — Codex writes verdict (`RETEST`) to `codex-verdict.json`
6. **RETEST_QUEUED** — Loop closes, ready for next cycle

---

## File Map

```
bridge-room-prototype/
├── README.md                  ← this file
├── plan.yaml                  ← scenario plan
├── room-state.json            ← current room state
├── outbox/
│   └── claude-command.json    ← Codex → Claude
├── inbox/
│   └── claude-output.json     ← Claude → Codex
├── codex-verdict.json         ← Codex verdict
└── journal/
    └── stage-log.jsonl        ← append-only event log
```

---

## Safety Constraints

- **DO NOT** connect to `bridge.py`
- **DO NOT** import or reference `scripts/`
- **DO NOT** push to git or Telegram
- **DO NOT** run as a live system
- All values are mock/documentation
- External review required before any runtime integration

---

## Prototype Closure

| | |
|-|-|
| Prototype #1 PASS | YES |
| Prototype #2 PASS | YES |
| Prototype #3 PASS | YES |
| Prototype #5 PASS | YES |
| Prototype #6 PASS | YES |
| Execution Pack v1 sandbox proof PASS | YES |
| Decision lifecycle + TOKEN_SAFE_STOP sandbox proof PASS | YES |
| Telegram integration approved | NO |
| Runtime integration approved | NO |
| Execution Pack runtime integration approved | NO |
| Ready for safe next design | YES |
| Ready for next sandbox design | YES |
| Ready for runtime integration | NO |
| Ready for full implementation | NO |

See [PROTOTYPE-CLOSURE.md](PROTOTYPE-CLOSURE.md) for full details.
