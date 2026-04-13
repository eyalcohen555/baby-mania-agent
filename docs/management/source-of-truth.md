# BabyMania — Source of Truth
**תפקיד:** הגדרה חד-משמעית של מי הוא מקור האמת לכל תחום.
**כלל:** כאשר יש ספק — קובץ זה מכריע.
**תואם ל:** BABYMANIA-MASTER-PROMPT v2.0 (2026-03-27)

---

## מקורות אמת פעילים

### מערכת כללית
| תחום | מקור אמת | הערה |
|------|-----------|------|
| מצב כולל / snapshot | `BABYMANIA-MASTER-PROMPT.md` | v2.0 — עדכון אחרי milestones |
| מי מקור האמת | `docs/management/source-of-truth.md` | הקובץ הזה |
| מפת כל המסמכים | `docs/management/management-index.md` | |
| מתי לעדכן מה | `docs/management/update-policy.md` | |
| החלטות ניהוליות רחבות | `docs/management/management-journal.md` | |
| מדיניות אישורים | `docs/management/approval-policy.md` | T0–T3 |
| עיצוב Team Lead | `docs/management/team-lead-agent-design.md` | |
| מודל קלט Team Lead | `docs/management/team-lead-input-model.md` | |

### Bridge — ערוץ תקשורת
| תחום | מקור אמת | הערה |
|------|-----------|------|
| משימה נוכחית | `bridge/next-task.md` | GPT כותב |
| תוצאה אחרונה | `bridge/last-result.md` | Claude כותב |
| מצב live | `bridge/status.md` | idle / running / waiting_response / done / failed |
| מצב Team Lead | `bridge/runtime-state.md` | stage / round / verdict |
| לוג משימות | `bridge/task-log.md` | append-only |
| תגובת Telegram | `bridge/telegram-response.md` | Telegram bot כותב |
| דוח stuck | `bridge/watchdog-report.md` | Watchdog כותב |
| singleton lock | `bridge/bridge.lock` | PID |
| כללי ביצוע | `bridge/EXECUTION_RULES.md` | |
| פורמט משימה | `bridge/task-format.md` | |
| GitHub Actions executor | `.github/workflows/claude-bridge.yml` | מסלול משני |
| היסטוריית bridge | `docs/operations/bridge-operations-journal.md` | |
| איך לקרוא מצב bridge live | `docs/operations/bridge-runtime-status.md` | |
| עיצוב ערוץ Telegram | `docs/operations/telegram-channel-design.md` | |

### Team Lead — שכבת ניתוב וניתוח
| תחום | מקור אמת | הערה |
|------|-----------|------|
| Team Lead agent | `teams/team-lead/team_lead.py` | מריץ worker, מנתח output, verdict |
| Watchdog | `teams/team-lead/watchdog.py` | מוניטור stuck, Telegram reminder |
| verdict state | `bridge/runtime-state.md` | PASS / RETRY / BLOCKED / FAILED |

**כלל ניתוב Team Lead:**
```
team_lead.py --task bridge/next-task.md [--dry-run]
  → קורא task packet
  → מריץ Claude Code (worker)
  → מנתח output → verdict:
      PASS / RETRY / BLOCKED / FAILED_EMPTY / FAILED_RATE_LIMIT / FALSE_SUCCESS / PARTIAL
  → כותב runtime-state.md (stage / round / verdict)
  → max 2 retries per task
```

**Watchdog:**
```
watchdog.py [--daemon] [--warn 120] [--stuck 300]
  → monitors runtime-state.md
  → detects suspected_stuck
  → writes watchdog-report.md
  → sends Telegram reminder (one per cycle)
```

**Startup:**
```
start-bridge.bat (Task Scheduler: logon trigger)
  → starts watchdog.py --daemon (background, polls כל 30s)
  → starts bridge.py (foreground, polls כל 4s)
```

### Approval Tiers — כלל ניתוב
| Tier | משמעות | bridge behavior |
|------|--------|----------------|
| T0 | read-only, audit | מריץ מיד |
| T1 | שינויים בטוחים | מריץ מיד |
| T2 | שינויים משמעותיים | מריץ מיד (Team Lead מנתח) |
| T3 | Shopify live / bulk / ארכיטקטורה | חוסם — AWAITING_APPROVAL |

**APPROVAL_TIER חובה בכל משימה.** Bridge חוסם T3 אוטומטית.

### Product Pipeline
| תחום | מקור אמת | הערה |
|------|-----------|------|
| product agents | `teams/product/agents/` | 18 agents (01–09 + extras) |
| product context | `shared/product-context/*.yaml` | 294 product YAML files |
| shoes status | `docs/product/shoes-journal.md` | |
| clothing status | `docs/product/clothing-journal.md` | |
| infrastructure decisions | `docs/product/infrastructure-journal.md` | |
| template sections mapping | `config/settings.py` | section→metafield |
| brand voice + copywriting | `knowledge/copywriting/` | |
| agent prompts | `prompts/` | benefits, blog, faq, etc. |
| content-bank, writing-rules | `shared/knowledge/` | |
| data schemas | `shared/schemas/` | |

### Organic
| תחום | מקור אמת | הערה |
|------|-----------|------|
| **state תפעולי** | `docs/organic/מצב-הפרויקט-האורגני.md` | **חובה לקרוא לפני כל משימה אורגנית** |
| HUB registry (live) | `teams/organic/hub-registry.json` | v2.0 |
| site map מאמרים | `output/site-map/internal_content_map.json` | v4.0 — 47 clusters |
| product reverse index | `output/site-map/product-reverse-index.json` | v1.2 — 25/25 verified |
| organic agents | `teams/organic/agents/` | 13 agents (01–12) |
| organic knowledge | `teams/organic/knowledge/` | |
| organic history | `docs/organic/organic-journal.md` | |

**כלל קדימות אורגני:**
```
hub-registry.json          → source of truth לסטטוס HUBים
internal_content_map.json  → source of truth למיפוי מאמרים
מצב-הפרויקט-האורגני.md    → source of truth תפעולי — checklist + layer state
BABYMANIA-MASTER-PROMPT.md → snapshot ניהולי על בלבד
```

### Theme Assets
| תחום | מקור אמת | הערה |
|------|-----------|------|
| Liquid sections | `theme_assets/sections/` | 20 section files |
| templates | `theme_assets/templates/` | blog.json, product.shoes.json |

### Shopify Config
| תחום | מקור אמת |
|------|-----------|
| Shop | a2756c-c0.myshopify.com |
| Theme ID | 183668179257 |
| API version | 2024-10 |
| Token | `C:\Users\3024e\Desktop\shopify-token\.env` |
| Env ראשי | `C:\Projects\baby-mania-agent\.env` |
| Metafields namespace | baby_mania |
| Sections path | `C:\Users\3024e\Downloads\קלוד קוד\sections\` |

---

## DEPRECATED — לא לסמוך עליהם

| קובץ | מצב | הוחלף ע"י |
|------|-----|------------|
| `next-task.md` (root) | DEPRECATED | `bridge/next-task.md` |
| `last-result.md` (root) | DEPRECATED | `bridge/last-result.md` |
| `shared_memory.md` | HISTORICAL | `BABYMANIA-MASTER-PROMPT.md` |
| `NIGHT_EXECUTION_PLAN.md` | HISTORICAL / REFERENCE ONLY | `docs/organic/organic-journal.md` |
| `00-team-lead/orchestrator.py` | DEPRECATED | `teams/team-lead/team_lead.py` |
| `00-team-lead/config.yaml` | DEPRECATED | task packets via `bridge/next-task.md` |
| `.claude/agents/*.md` | DEPRECATED | `teams/product/agents/` + `teams/organic/agents/` |
| `output/stage-outputs/` | DEPRECATED | `shared/product-context/*.yaml` |

---

## כלל סכסוך בין קבצים

```
אם קובץ A וקובץ B סותרים —
  1. בדוק תאריך עדכון
  2. קובץ מהרשימה הזו = מנצח
  3. אם שניהם בטבלה — journal > master (יותר עדכני)
  4. אם עדיין ספק — עצור ושאל אייל
```
