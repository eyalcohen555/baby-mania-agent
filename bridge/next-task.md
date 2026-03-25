TASK: BRIDGE GITHUB ROUNDTRIP TEST
LAYER: 1
BLOCKER: צריך להוכיח שהזרימה GitHub → local Claude → GitHub עובדת
ACTION: בצע בדיקת קריאה בלבד על קבצי ה-bridge והחזר PASS קצר
FILES_ALLOWED:
- bridge/task-format.md
- bridge/EXECUTION_RULES.md
- bridge/status.md
- bridge/last-result.md
FILES_FORBIDDEN:
- teams/product/**
- teams/organic/**
- Shopify
- agents
- pipeline logic
- shoes
- clothing
RULES:
- קריאה בלבד
- לא לשנות שום קובץ
EXPECTED:
SYSTEM STATE
PRODUCT STATE
ISSUES FOUND
RISK LEVEL
NEXT STEP

בסוף להחזיר גם:
- TASK_ID: GITHUB-ROUNDTRIP-TEST
- STATUS: PASS / FAIL
- FILES_UPDATED: none
- IS GITHUB BRIDGE ROUNDTRIP WORKING: YES / NO
