# BabyMania — Source of Truth
**תפקיד:** הגדרה חד-משמעית של מי הוא מקור האמת לכל תחום.
**כלל:** כאשר יש ספק — קובץ זה מכריע.

---

## מקורות אמת פעילים

### מערכת כללית
| תחום | מקור אמת | הערה |
|------|-----------|------|
| מצב כולל / snapshot | `BABYMANIA-MASTER-PROMPT.md` | v1.2+ — עדכון אחרי milestones |
| ארכיטקטורת pipeline | `CATEGORY-ARCHITECTURE-DECISION.md` | v1.0 — עדכון אחרי שינוי ארכיטקטורי |
| הרצת pipeline | `00-team-lead/orchestrator.py` | single entry point — אסור להריץ agents ישירות |
| config מטאפילדים + stages | `00-team-lead/config.yaml` | source of truth לstages ולmetafields |
| template sections mapping | `config/settings.py` | source of truth לsection→metafield |

### Bridge
| תחום | מקור אמת |
|------|-----------|
| משימה נוכחית | `bridge/next-task.md` |
| תוצאה אחרונה | `bridge/last-result.md` |
| מצב live | `bridge/status.md` |
| כללי ביצוע | `bridge/EXECUTION_RULES.md` |
| פורמט משימה | `bridge/task-format.md` |
| היסטוריית bridge | `docs/operations/bridge-operations-journal.md` |

### Product Pipeline
| תחום | מקור אמת |
|------|-----------|
| agent prompts | `.claude/agents/*.md` |
| stage outputs | `output/stage-outputs/` |
| product context | `shared/product-context/*.yaml` |
| shoes status | `docs/product/shoes-journal.md` |
| clothing status | `docs/product/clothing-journal.md` |
| infrastructure decisions | `docs/product/infrastructure-journal.md` |

### Organic
| תחום | מקור אמת |
|------|-----------|
| HUB registry (live) | `teams/organic/hub-registry.json` |
| organic pipeline agents | `teams/organic/agents/` |
| organic knowledge | `teams/organic/knowledge/` |
| organic history | `docs/organic/organic-journal.md` |

---

## DEPRECATED — לא לסמוך עליהם

| קובץ | מצב | הוחלף ע"י |
|------|-----|------------|
| `next-task.md` (root) | DEPRECATED | `bridge/next-task.md` |
| `last-result.md` (root) | DEPRECATED | `bridge/last-result.md` |
| `shared_memory.md` | HISTORICAL | `BABYMANIA-MASTER-PROMPT.md` |
| `NIGHT_EXECUTION_PLAN.md` | HISTORICAL / REFERENCE ONLY | `docs/organic/organic-journal.md` |

---

## כלל סכסוך בין קבצים

```
אם קובץ A וקובץ B סותרים —
  1. בדוק תאריך עדכון
  2. קובץ מהרשימה הזו = מנצח
  3. אם שניהם בטבלה — journal > master (יותר עדכני)
  4. אם עדיין ספק — עצור ושאל אייל
```
