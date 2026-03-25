TASK: הפוך 02b-shoes-thinking ל-runnable בלבד
LAYER: 2
BLOCKER: 02b-shoes-thinking מסומן DESIGN ואינו runnable

ACTION:
  1. קרא את:
     C:/Projects/baby-mania-agent/.claude/agents/02b-shoes-thinking.md
  2. הסר רק חסימות DESIGN:
     - כל שורה עם DESIGN
     - כל שורה עם "טרם הפך לסוכן"
  3. אם יש ניסוח שעוצר הרצה רק כי _intelligence.json חסר:
     החלף אותו ל-fallback ברור:
     אם _intelligence.json חסר → המשך עם context.yaml בלבד
     וסמן degraded_mode=true
  4. אל תריץ את הסוכן
  5. אל תבדוק מוצרים
  6. אל תיגע ב-config.yaml
  7. אל תיגע ב-orchestrator.py
  8. אל תיגע ב-.github/workflows
  9. שמור את כל שאר הקובץ ללא שינוי

FILES_ALLOWED:
  - .claude/agents/02b-shoes-thinking.md

FILES_FORBIDDEN:
  - config.yaml
  - orchestrator.py
  - .github/workflows/*
  - Shopify
  - sections
  - theme
  - clothing files

EXPECTED:
SYSTEM STATE / CHANGES MADE / FILES UPDATED / RISK LEVEL / NEXT STEP
