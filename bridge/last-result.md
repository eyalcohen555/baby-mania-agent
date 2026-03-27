task_id: 20260327-020454
round: 1
---
Now I have a complete picture. Here's the audit:

---

# MASTER PROMPT + SYSTEM DOCS SYNC AUDIT

## SYSTEM STATE: Multiple desync issues found

---

### 1. CRITICAL — `babymania-master.md` (skill file) is stale / V1-centric

| Issue | Detail |
|-------|--------|
| **Shop URL wrong** | `babymania-master.md` §6 commands use `babymania-il.myshopify.com` — actual shop is `a2756c-c0.myshopify.com` (CLAUDE.md is correct) |
| **theme/ directory doesn't exist** | `babymania-master.md` §2 documents `theme/sections/*.liquid` — no `theme/` dir exists in repo. Sections are at `C:\Users\3024e\Downloads\קלוד קוד\sections\` per CLAUDE.md |
| **fabric_story metafield schema outdated** | Skill says `fabric_story` = single JSON object `{title, dream, body, tags}`. Actual `settings.py` maps to 5 separate keys: `fabric_title`, `fabric_body`, `fabric_body_2`, `fabric_highlight`, `fabric_tags` |
| **8 sections → 12 sections** | Skill lists 8 sections. Actual `TEMPLATE_SECTIONS` in `settings.py` has 12 (added: `bm-sticky-bar`, `bm-store-main-overrides`, `bm-store-hero`, `bm-store-banner`, `related-products`) |
| **V1 commands still prominent** | §5-6 show `main.py` commands as primary workflow. Master prompt correctly marks these LEGACY but skill file does not |
| **SECTION_METAFIELD_MAP outdated** | Skill shows old simplified map. Actual `settings.py` has `bm-store-hero` mapping + expanded fabric keys |
| **Missing hero metafield keys** | Skill lists `subtitle`, `badge_text` but actual config uses `hero_eyebrow`, `hero_headline`, `hero_subheadline` |

### 2. MEDIUM — Master Prompt vs Actual State

| Issue | Detail |
|-------|--------|
| **Agent paths inconsistent** | Master prompt says `00-team-lead/orchestrator.py` — file exists there. But `source-of-truth.md` says agents at `.claude/agents/*.md`. Actual agents are **dual-located**: both `.claude/agents/` and `teams/product/agents/`. No doc clarifies which is canonical |
| **Shoes agents incomplete in master** | Master lists `02b-shoes-thinking` but actual repo also has `04-shoes-validator.md` (in `teams/product/agents/`) which is NOT listed in the agent table |
| **content-editor-agent missing from master** | `.claude/agents/content-editor-agent.md` exists but not listed in master prompt agent table |
| **Organic pipeline numbering mismatch** | Master says pipeline is `11 → 03 → 04 → 08 → publish`. Actual organic agents: 01-tag, 02-keyword, 03-strategist, 04-writer, 05-demand, 06-prioritizer, 07-mapper, 08-linker, 09-product-linker, 10-link-qa, 10.5-content-qa, 11-topic, 12-hub-planner. Pipeline numbering doesn't match |

### 3. LOW — source-of-truth.md gaps

| Issue | Detail |
|-------|--------|
| **Missing from source-of-truth** | `teams/team-lead/team_lead.py`, `teams/team-lead/watchdog.py` — not documented anywhere |
| **New bridge files undocumented** | `bridge/checkpoint.md`, `bridge/telegram-response.md`, `bridge/watchdog-report.md`, `bridge/runtime-state.md`, `bridge/task-log.md` — none in any doc |
| **New docs undocumented** | `docs/management/approval-policy.md`, `docs/management/team-lead-agent-design.md`, `docs/management/team-lead-input-model.md`, `docs/operations/telegram-channel-design.md` — not in management-index.md |
| **EXECUTION_RULES references approval-policy.md** | This file exists but isn't in any index |

### 4. LOW — CLAUDE.md vs Memory

| Issue | Detail |
|-------|--------|
| **Memory says store URL = `babymania-il.myshopify.com`** | CLAUDE.md correctly says `a2756c-c0.myshopify.com`. Memory file is wrong |

---

## ROOT CAUSE
- System evolved (V1→V2, new agents, new bridge features) but `babymania-master.md` skill file was not updated alongside
- New operational files (watchdog, telegram, approval-policy) added without updating indexes
- Agent dual-location (`.claude/agents/` + `teams/`) never formally documented

## PRIORITY FIX ORDER

1. **Fix `babymania-master.md`** — shop URL, remove theme/ references, update section list + metafield schema, mark V1 sections clearly
2. **Update `management-index.md`** — add 4 missing docs
3. **Update `source-of-truth.md`** — add bridge new files, teams/team-lead, approval-policy
4. **Fix master prompt agent table** — add shoes-validator, content-editor-agent
5. **Fix memory MEMORY.md** — correct store URL
6. **Clarify agent canonical location** — `.claude/agents/` vs `teams/*/agents/`

Want me to proceed with fixes? I recommend starting with items 1-2 (most impactful).
