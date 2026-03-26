task_id: 20260326-130622
---
Done. Here's a summary of what was set up:

## מדיניות אישורים מדורגת — 4 Tiers

| Tier | מי מאשר | מתי |
|------|---------|-----|
| **T0** | אף אחד (auto) | קריאה, audit, validator, GET מ-Shopify |
| **T1** | GPT בלבד | output ביניים, journal, dry-run, writing agents |
| **T2** | GPT + validator | agent prompts, sections, pipeline בודד, git push |
| **T3** | **אייל חובה** | Shopify live, config/orchestrator, bulk >5, ביגוד production |

## קבצים שעודכנו:
1. **`docs/management/approval-policy.md`** — מסמך מלא (source of truth) עם מטריצת החלטה, escalation rules, מקרי קצה, דוגמאות, וחיבור ל-Bridge
2. **`BABYMANIA-MASTER-PROMPT.md`** — טבלת סיכום עם 4 tiers + כלל הסלמה
3. **`bridge/EXECUTION_RULES.md`** — הוספת בדיקת Tier כשלב ראשון חובה לפני כל פעולה
4. **`docs/management/management-index.md`** — עודכן ל-T0/T1/T2/T3
