# KNOWN ANOMALIES REGISTRY

**גרסה:** v1
**תאריך יצירה:** 2026-04-19
**עדכון אחרון:** 2026-04-19

---

## STATUS

פעיל

---

## PURPOSE

המסמך מרכז חריגים ידועים שחייבים להיות מוחרגים או מטופלים לפני generation / bundle / push / closure.

המטרה: למנוע גילוי חוזר של אותה בעיה בכל ריצה חדשה.

---

## RULE

כל חריג ידוע חייב להופיע כאן **לפני** כל rollout או recovery רלוונטי.

bundle לא יכול לכלול PID שמופיע ברשימה זו — אלא אם כן שונה סטטוסו לאחר החלטה ניהולית מפורשת.

---

## REGISTRY

---

### ANOMALY-001

#### PID
`9881362759993`

#### PRODUCT
מנורת לילה להירדמות

#### CATEGORY
anomaly / non-clothing product

#### DETECTED IN
Layer 4 GEO

#### WHY BLOCKED
המוצר נכנס בטעות לסקופ clothing / GEO למרות שאינו מוצר clothing תקין למסלול זה.

#### AFFECTED LAYERS
- Layer 4

#### EXCLUDE RULE
יש להחריג את PID `9881362759993` מכל bundle / push / recovery שרצים על clothing GEO — עד החלטה ניהולית מפורשת אחרת.

#### LIVE STATUS
לא נכתב אליו GEO ב-live — **מאומת** (management-journal.md, 2026-04-19)

#### REOPEN CONDITION
רק אחרי:
1. אימות סיווג מוצר נכון
2. החלטה ניהולית מפורשת של אייל
3. בדיקה שהמוצר שייך למסלול המתאים

#### OWNER
אייל

#### LAST VERIFIED
2026-04-19

---

## ADDING NEW ANOMALIES

לפני הוספת חריג חדש, לבדוק:
- האם יש evidence (ראיה) מתועדת — log / journal / live check?
- האם ה-PID מזוהה בוודאות?
- האם הסיבה ברורה ומנוסחת?

**אין להוסיף חריג חלקי או מבוסס-השערה.**

פורמט חובה לכל רשומה חדשה: ANOMALY-NNN + כל שדות החובה לעיל.

---

*KNOWN ANOMALIES REGISTRY — BabyMania Layer 4 — P1-S2 / AUTOMATION-HARDENING-PLAN v1*
