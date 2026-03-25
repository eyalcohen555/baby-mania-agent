TASK: audit shoes blocker in orchestrator.py
LAYER: 4
BLOCKER: orchestrator.py לא shoes-aware

ACTION:
  1. קרא בלבד:
     - 00-team-lead/orchestrator.py
     - 00-team-lead/config.yaml
  2. זהה במדויק איפה ה-orchestrator hardcoded ל-clothing
  3. זהה מה חסר כדי לתמוך ב-shoes runtime
  4. החזר הצעת שינוי מינימלית בלבד:
     - אילו בלוקים צריך לשנות
     - מה מטרת כל שינוי
     - האם זה שינוי ממוקד או ארכיטקטוני
  5. אל תשנה שום קובץ
  6. אל תריץ pipeline
  7. אל תיגע ב-Shopify

FILES_ALLOWED:
  - 00-team-lead/orchestrator.py
  - 00-team-lead/config.yaml

FILES_FORBIDDEN:
  - Shopify
  - sections
  - theme
  - clothing files
  - agents
  - publisher
  - validator

EXPECTED:
SYSTEM STATE / PRODUCT STATE / ISSUES FOUND / RISK LEVEL / NEXT STEP
