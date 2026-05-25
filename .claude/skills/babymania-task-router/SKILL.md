---
name: babymania-task-router
description: מחליט מה לעשות עם כל משימה ב-BabyMania — איזה mode, bridge ידני או Conductor plan, מה הצעד הבא. הפעל בקבלת כל בקשת משימה חדשה, כשיש ספק איך לגשת, כשהמשתמש שולח פקודה ללא mode מפורש, לפני כל ביצוע. טריגרים: "תתכנן", "תרוץ", "תבדוק", "תפעיל", "איך לגשת", "מה לעשות", "כיצד", "תתחיל", "תיצור plan", "מה קודם", כל בקשת משימה ללא mode מפורש. עובד לפי docs/management/chat-to-automation-operating-protocol.md.
allowed-tools: Read, Grep, Glob
---

# babymania-task-router — ניתוב משימות BabyMania

## מתי להשתמש

- כל קבלת משימה חדשה ללא `MODE:` מפורש
- כשמתלבטים בין bridge ידני לבין Conductor plan
- לפני הרצת כל קוד, script, או פקודה ל-Shopify
- כשהמשתמש שואל "מה לעשות" / "איך לגשת" / "מה קודם"

## מתי לא להשתמש

- כשהמשתמש ציין `MODE:` מפורש בבקשה ואין סתירה
- כשהמשימה T0 בלבד (קריאה, audit) — פשוט תבצע
- כשכבר ניתבת משימה זו באותו סשן

## 7 שאלות חובה לפני כל פקודה

לפי `docs/management/chat-to-automation-operating-protocol.md`:

```
1. מה המטרה העסקית?
   → מה אנחנו רוצים להשיג? מה הבעיה שפותרים?

2. איזה צוות / תחום?
   → organic / product-clothing / product-shoes / automation / shopify-live

3. מה המצב הנוכחי?
   → קרא BABYMANIA-MASTER-PROMPT.md + journal רלוונטי
   → בדוק: branch, conductor-state, bridge status

4. האם זו משימה אחת פשוטה או workflow רב-שלבי?
   → משימה אחת → bridge ידני
   → 2+ שלבים תלויים → Conductor plan

5. האם ניתן לטפל בזה דרך אוטומציה?
   → אם כן — צור plan YAML

6. מה יכול להשתבש?
   → הגדר fail_conditions לכל שלב

7. היכן חייב אייל לאשר?
   → T3 / merge / full automation / RISK HIGH
```

**חוק:** לא לדלג על שאלות 1–3 לפני ביצוע.

## הגדרת Modes

| Mode | מה כולל | מתי לבחור |
|------|---------|-----------|
| `AUDIT` | קריאה בלבד, אין שינויים | T0 — בדיקות, state check |
| `PLAN` | יצירת plan YAML בלבד | לפני כל ביצוע בעל 2+ שלבים |
| `DRY-RUN` | הרצת conductor עם `--dry-run` | לאחר יצירת plan, לפני live run |
| `CONTROLLED-EXECUTION` | הרצה אחת מבוקרת של plan | אחרי dry-run PASS |
| `REPORT` | תיעוד תוצאה בלבד | לאחר PASS של plan |

## טבלת החלטה — Bridge ידני או Conductor plan

| מצב | גישה |
|-----|------|
| פעולה אחת, ללא תלות | bridge ידני (next-task.md) |
| אין routing מותנה | bridge ידני |
| 2+ שלבים תלויים | Conductor plan |
| audit → fix → retest flow | Conductor plan |
| output של שלב קובע את הבא | Conductor plan |
| risk נגיעה בקבצים מחוץ לscope | Conductor plan + Codex review |
| ספק | plan. תמיד עדיף plan על copy-paste ידני |

## כללי אישור לפי Tier

| Tier | משמעות | מי מאשר |
|------|--------|---------|
| T0 | read-only, audit | אוטומטי |
| T1 | שינויים בטוחים | אוטומטי |
| T2 | שינויים משמעותיים | Claude מנתח, Team Lead בודק |
| T3 | Shopify live / bulk / ארכיטקטורה | **אייל חובה — STOP** |

## פורמט פלט חובה

```
BUSINESS GOAL:     [מה רוצים להשיג]
DOMAIN:            [organic / product / automation / shopify]
CURRENT STATE:     [בדוק מ-MASTER + journal]
TASK TYPE:         [משימה אחת / workflow רב-שלבי]
MODE:              [AUDIT / PLAN / DRY-RUN / CONTROLLED-EXECUTION / REPORT]
APPROVAL TIER:     [T0 / T1 / T2 / T3]
AYAL_APPROVAL:     [YES — נדרש / NO — לא נדרש]
NEXT EXACT STEP:   [פעולה אחת, ברורה, עם scope מוגדר]
RISK IF WRONG:     [מה יכול להשתבש]
```

## קבצי מקור שחובה לקרוא

- `docs/management/chat-to-automation-operating-protocol.md` — הפרוטוקול המלא
- `BABYMANIA-MASTER-PROMPT.md` — מצב נוכחי + approval tiers

## קבצים שמותר לקרוא

- `docs/management/conductor-plan-format.md` — לפני יצירת plan
- `docs/management/codex-automation-role.md` — לפני Codex review
- `bridge/conductor-state.md` — לבדיקת מצב bridge לפני ריצה

## פעולות אסורות

- להריץ plan בלי dry-run קודם
- לכתוב ל-Shopify בלי T3 ואישור אייל
- לפרש "Codex APPROVED" כ"אייל אישר" — לא אותו דבר
- לדלג על שאלות 1–3 לפני ביצוע
- להפעיל full automation בלי אישור מפורש מאייל

## חוקי BabyMania

- Full automation: NO — ממתין לאישור נפרד מאייל.
- Controlled daily use: YES (T1 plans עם dry-run לפני).
- כל T3 → STOP → אייל.
- ספק → plan. ספק על plan → Codex review.

## טעויות נפוצות למניעה

- לשלוח פקודה ל-Claude לפני שהבנת את המטרה העסקית.
- ליצור plan ענקי עם stages לא ברורים.
- לבחור bridge ידני כשיש 3+ שלבים תלויים — יוצר copy-paste.
- לבחור Conductor plan לפעולה פשוטה אחת — אוברקיל.
- לדלג על dry-run "כי הplan נראה טוב" — אסור.
