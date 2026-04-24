# BabyMania — Management Index
**תפקיד:** מפת כל מסמכי הניהול. נקודת כניסה ראשונה לכל מסמך בפרויקט.
**עדכון:** בכל פעם שמסמך חדש נוצר או מסמך ישן הופך deprecated.

---

## מסמכי שליטה עליונים

| קובץ | תפקיד | סטטוס |
|------|--------|--------|
| `BABYMANIA-MASTER-PROMPT.md` | חוקה. snapshot מצב. חוקי עבודה. | ✅ ACTIVE |
| `CATEGORY-ARCHITECTURE-DECISION.md` | ארכיטקטורת pipeline — thinking/writing/validation | ✅ ACTIVE REFERENCE |
| `docs/management/source-of-truth.md` | מי הוא מקור האמת לכל תחום | ✅ ACTIVE |
| `docs/management/update-policy.md` | מתי לעדכן master / journals | ✅ ACTIVE |

---

## יומני תחומים (Journals)

| קובץ | תחום | עדכון |
|------|------|--------|
| `docs/management/management-journal.md` | ניהול — החלטות רחבות, שינויי workflow | שוטף |
| `docs/operations/bridge-operations-journal.md` | Bridge — runtime, singleton, path, scheduler | ✅ CLOSED |
| `docs/product/shoes-journal.md` | Shoes — blockers, pipeline, rollout | שוטף |
| `docs/product/clothing-journal.md` | Clothing — production status, issues | שוטף |
| `docs/product/infrastructure-journal.md` | Infrastructure — orchestrator, config, routing | שוטף |
| `docs/product/reborn/REBORN-MASTER-PROMPT.md` | Reborn — שליטה + חוקים + כפיפות למאסטר | PLANNING |
| `docs/product/reborn/reborn-product-page-state.md` | Reborn — מצב תפעולי + כיוון מאושר | שוטף |
| `docs/product/reborn/reborn-task-checklist.md` | Reborn — צ'ק ליסט שלבים (PHASE 1–9) | שוטף |
| `docs/product/reborn/reborn-first-summary-report.md` | Reborn — דוח מחקר שוק ראשון (reference input בלבד) | REFERENCE |
| `docs/organic/organic-journal.md` | Organic — HUBs, content pipeline | שוטף |
| `docs/organic/מצב-הפרויקט-האורגני.md` | **Organic state תפעולי** — checklist + layer state | **חובה לקרוא לפני משימה אורגנית** |

---

## מסמכי Bridge (Operational)

| קובץ | תפקיד |
|------|--------|
| `bridge/EXECUTION_RULES.md` | כללי ביצוע חובה לכל משימה |
| `bridge/task-format.md` | פורמט רשמי למשימה ותוצאה |
| `bridge/status.md` | מצב live של ה-bridge (מנוהל אוטומטית) |
| `bridge/runtime-state.md` | מצב Team Lead — stage / round / verdict |
| `bridge/watchdog-report.md` | דוח Watchdog — suspected_stuck, reminder |
| `bridge/next-task.md` | משימה נוכחית (GPT כותב) |
| `bridge/last-result.md` | תוצאה אחרונה (Claude כותב) |
| `bridge/task-log.md` | לוג משימות (append-only) |
| `bridge/telegram-response.md` | תגובת Telegram bot |
| `docs/operations/bridge-runtime-status.md` | הסבר איך לקרוא את מצב ה-bridge |
| `docs/operations/telegram-channel-design.md` | עיצוב ערוץ Telegram |

---

## Team Lead & Watchdog

| קובץ | תפקיד |
|------|--------|
| `teams/team-lead/team_lead.py` | Team Lead agent — ניתוב, ניתוח output, verdict |
| `teams/team-lead/watchdog.py` | Watchdog daemon — מוניטור stuck, Telegram reminder |
| `docs/management/approval-policy.md` | מדיניות אישורים T0–T3 |
| `docs/management/team-lead-agent-design.md` | עיצוב Team Lead agent |
| `docs/management/team-lead-input-model.md` | מודל קלט Team Lead |
| `docs/management/conductor-plan-format.md` | פורמט רשמי לתוכניות execution רב-שלביות (YAML spec) |

---

## קבצים היסטוריים (לא לעדכן)

| קובץ | סיבה |
|------|------|
| `shared_memory.md` | עיצוב מוקדם — לפני הpipeline הנוכחי. לא רלוונטי. |
| `NIGHT_EXECUTION_PLAN.md` | תוכנית אורגנית היסטורית — בוצעה חלקית. |

---

## חוקי ניהול בסיסיים

1. **master prompt = חוקה** — לא journal, לא מחסן היסטוריה
2. **כל תחום = journal משלו** — לא דוחסים הכל ל-master
3. **source-of-truth.md = נקודת פתרון סכסוכים** — כשיש ספק, שם יש תשובה
4. **לפני handoff/chat חדש** — חובה לעדכן next-step בjournal הרלוונטי
