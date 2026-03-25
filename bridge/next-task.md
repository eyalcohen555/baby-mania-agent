TASK: הוסף shoes stages ל-config.yaml
LAYER: 4
BLOCKER: config.yaml לא כולל את שלבי ה-shoes pipeline
ACTION:
  1. קרא את config.yaml
  2. בדוק מה כתוב תחת clothing stages
  3. הוסף shoes stages במבנה זהה
  4. עצור ודווח לפני שמירה — הצג את השינוי המדויק לאישור
FILES_ALLOWED: config.yaml
FILES_FORBIDDEN: orchestrator.py, Shopify, sections, clothing files, agents
EXPECTED: SYSTEM STATE / PROPOSED CHANGES / RISK LEVEL
