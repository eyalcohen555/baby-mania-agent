TASK: ייצוב פרוטוקול ה-Bridge
LAYER: 1
BLOCKER: שכבת האוטומציה לא יציבה — הלולאה נופלת, next-task לא תמיד נצרך, last-result לא תמיד זמין בזמן

ACTION:
  1. קרא את:
     - bridge/github-bridge.py
     - bridge/EXECUTION_RULES.md
  2. אמת את פרוטוקול העבודה בפועל:
     - קריאת next-task.md
     - ביצוע משימה
     - כתיבת last-result.md
     - commit + push
     - ניקוי next-task.md
  3. תקן רק מה שחיוני כדי להבטיח:
     - פורמט משימה יחיד וקבוע
     - last-result נכתב לפני ניקוי משימה
     - יש אינדיקציה ברורה אם הלולאה חיה/נפלה
  4. אל תיגע ב-product agents
  5. אל תיגע ב-Shopify
  6. אל תיגע ב-clothing
  7. אל תיגע ב-sections/theme
  8. אם נדרש שינוי ארכיטקטוני גדול — עצור ודווח, אל תחליט לבד

FILES_ALLOWED:
  - bridge/github-bridge.py
  - bridge/EXECUTION_RULES.md
  - bridge/*
  - מסמכי תיעוד רלוונטיים בלבד

FILES_FORBIDDEN:
  - config.yaml
  - orchestrator.py
  - Shopify
  - sections
  - theme
  - clothing files
  - product agents

EXPECTED:
SYSTEM STATE / CHANGES MADE / FILES UPDATED / RISK LEVEL / NEXT STEP
