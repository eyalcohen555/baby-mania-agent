TASK: Final E2E test — write checkpoint file
LAYER: 1
APPROVAL_TIER: T3
BLOCKER: none
ACTION: כתוב לקובץ bridge/e2e-final.txt את הטקסט הבא בדיוק:
FINAL_E2E: PASS
TIMESTAMP: כתוב את השעה הנוכחית בפורמט YYYY-MM-DD HH:MM:SS
FILES_ALLOWED: bridge/e2e-final.txt
FILES_FORBIDDEN: Shopify, config.yaml, teams/product/**, teams/organic/**, bridge/status.md, bridge/runtime-state.md
RULES:
- כתוב את הקובץ בדיוק לפי ה-ACTION
- אל תעשה שום דבר נוסף
- החזר STATUS: PASS ואת נתיב הקובץ שנכתב
EXPECTED: bridge/e2e-final.txt קיים עם FINAL_E2E: PASS + TIMESTAMP
