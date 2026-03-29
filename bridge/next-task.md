TASK: SHOES FULL CONTROLLED ROLLOUT
TASK_ID: 20260329-shoes-rollout-001
APPROVAL_TIER: T3
LAYER: 5
BLOCKER: נעליים עברו proof + controlled batch + verify-contract fix — מוכן ל-rollout מלא

ACTION:
בצע rollout מלא של נעליים לפי התוכנית הבאה. אל תחזור למשתמש בין מוצרים אלא אם פגעת ב-STOP condition.

---

OWNER APPROVAL MODEL:
- התוכנית מאושרת לנעליים בלבד
- אל תשאל שוב בין מוצרים אלא אם יש STOP condition
- אם מופיע policy conflict מעבר לscope זה — עצור ודווח

---

STAGE 0 — PRECHECK
מטרה: אמת שהמערכת בטוחה לrollout לאחר תיקון verify-contract

פעולה:
1. הרץ push + verify על PID 9615669100857
2. אמת:
   - ctx מכיל product_template_type: shoes
   - verify קורא category = shoes
   - verify required_keys = 3
   - המוצר נשאר LIVE

החלטה:
- PASS → המשך ל-STAGE 1
- FAIL → עצור ודווח

---

STAGE 1 — BUILD ROLLOUT LIST
מטרה: בנה רשימת מוצרים שנותרו לrollout

פעולה:
1. אסוף כל מוצרים שה-shoes path רלוונטי להם
2. אל תכלול:
   - 9940751417657
   - 9606764200249
   - 9607363592505
   - 9615669100857
3. הצג את הרשימה עם ספירה לפני הביצוע

החלטה:
- אם הרשימה ריקה → קפוץ ל-STAGE 5
- אחרת המשך

---

STAGE 2 — CONTROLLED ROLLOUT LOOP
מטרה: הרץ כל מוצר נעליים שנותר דרך ה-orchestrator המלא

לכל PID:
1. אמת שהמוצר מזוהה כ-shoes
2. הרץ pipeline מלא דרך orchestrator
3. הפק כל stage outputs
4. validator
5. publisher
6. push
7. verify
8. אמת LIVE

לאחר כל PID סווג:
- PASS
- OUTPUT FAIL
- DATA FAIL
- LOGIC FAIL
- VERIFY/SHOPIFY CONTRACT FAIL

ALLOWED SELF-HANDLING (ללא חזרה למשתמש):
A. OUTPUT FAIL בלבד — פעם אחת לכל PID:
   - הרץ מחדש מהstage הנכון אם כשל הוא output-level בלבד
   - מקסימום rerun אחד לכל PID
   - אסור תיקון טקסט ידני
   - אסור שינויי קוד

B. DATA FAIL בלבד — פעם אחת לכל PID:
   - הרץ מחדש מstage 01 אם ה-context ישן או חסר
   - מקסימום refresh אחד לכל PID
   - אסור שינויי קוד

NOT ALLOWED TO SELF-FIX:
- שינויי orchestrator / config / validator / agent / theme / Shopify structure
- כל bug שפוגע ביותר מ-PID אחד באותה צורה
- כל false-positive verify pattern

STOP CONDITIONS:
- LOGIC FAIL → עצור מיד
- VERIFY/SHOPIFY CONTRACT FAIL → עצור מיד
- אותו failure class על 2 מוצרים או יותר → עצור מיד (SYSTEMIC)

---

STAGE 3 — SYSTEMIC CHECKPOINTS
מטרה: זיהוי bugs חוזרים לפני שמתפשטים

תדירות: אחרי כל 5 PIDs שהושלמו
בדוק:
1. pattern of failure חוזר?
2. חולשה חוזרת ב-validator?
3. mismatch חוזר ב-verify?
4. state stale חוזר?
5. false-positive PASS חשד?

החלטה:
- נקי → המשך
- pattern חוזר → עצור מיד (SYSTEMIC)

---

STAGE 4 — ROLLOUT COMPLETION CHECK
בדוק:
1. כל PIDs שנותרו עובדו
2. אין FAIL לא פתור
3. אין PID שדולג
4. verify רץ עם required_keys אמיתיים
5. אין false-positive verify שנותר

החלטה:
- הכל תקין → המשך ל-STAGE 5
- אחרת → עצור ודווח על הפער המדויק

---

STAGE 5 — DOCUMENTATION LOCK
עדכן:
1. BABYMANIA-MASTER-PROMPT.md — סעיף shoes בלבד:
   - סטטוס rollout לאחר ריצה מלאה
   - האם shoes הושלם במלואו
   - כל blocker שנשאר
   - milestone מדויק שהושג

2. docs/product/shoes-journal.md — הוסף entry:
   - סיכום ריצת rollout
   - ספירות
   - סיבת עצירה אם נעצר
   - ממצא systemic אם יש

---

FILES_ALLOWED:
- 00-team-lead/orchestrator.py (read-only during rollout)
- shared/product-context/*.yaml
- output/stage-outputs/*
- logs/audits/*
- BABYMANIA-MASTER-PROMPT.md (לעדכון STAGE 5 בלבד)
- docs/product/shoes-journal.md (לעדכון STAGE 5 בלבד)
- teams/product/agents/* (read-only)
- 00-team-lead/config.yaml (read-only)

FILES_FORBIDDEN:
- teams/organic/**
- bridge/**
- theme_assets/**
- scripts/telegram_bot.py
- כל קובץ clothing שאינו שיתופי

RULES:
- orchestrator אמיתי בלבד
- shoes path אמיתי בלבד
- אסור לתקן output ידנית
- אסור לדלג שלבים
- ראיות בלבד
- עצור על systemic failure
- עדכן master ו-journal אחרי milestone

EXPECTED:
SYSTEM STATE
ROLLOUT STATE
QUEUE SIZE
PROCESSED COUNT
PASSED COUNT
FAILED COUNT
SKIPPED COUNT

PER PID RESULTS:
- PID / stage reached / validator / publisher / verify / LIVE / rerun used / failure class

SYSTEMIC CHECKPOINT RESULTS
ISSUES FOUND (OUTPUT / DATA / LOGIC / VERIFY / SHOPIFY / SYSTEMIC)
RISK LEVEL
NEXT STEP

ALSO INCLUDE:
- STAGE 0 RESULT: PASS / FAIL
- FULL ROLLOUT RESULT: PASS / FAIL / STOPPED
- ORCHESTRATOR USED: YES / NO
- SHOES PATH USED: YES / NO
- VERIFY CONTRACT STABLE: YES / NO
- MASTER UPDATED: YES / NO
- JOURNAL UPDATED: YES / NO
- EXACT STOP REASON (if stopped)
