TASK: בצע 5 שינויים מדויקים ב-02b-shoes-thinking
LAYER: 2
BLOCKER: הקובץ .claude/agents/02b-shoes-thinking.md מוגן, לכן השינוי חייב להתבצע דרך ה-bridge

ACTION:
  1. קרא את:
     C:/Projects/baby-mania-agent/.claude/agents/02b-shoes-thinking.md
  2. בצע רק את 5 השינויים הבאים, ולא שום שינוי אחר:
     א. הסר את שורת ה-DESIGN מהקובץ
     ב. הסר כל שורה שמכילה את הטקסט: "טרם הפך לסוכן"
     ג. אם יש תנאי שעוצר הרצה כאשר _intelligence.json חסר — בטל את העצירה
     ד. הוסף fallback ברור: אם _intelligence.json חסר → המשך עם context.yaml בלבד
     ה. סמן במפורש degraded_mode=true במסלול ה-fallback
  3. שמור את כל שאר הקובץ ללא שינוי
  4. אל תריץ את הסוכן
  5. אל תיגע בשום קובץ אחר

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
  - כל קובץ אחר מלבד 02b-shoes-thinking.md

RULES:
  - שינוי מינימלי בלבד
  - אין refactor
  - אין formatting changes
  - אין שינוי שמות שדות מעבר למה שנדרש
  - אם אחד מ-5 השינויים לא ניתן לביצוע בלי לשנות קבצים נוספים — עצור ודווח, אל תאלתר

EXPECTED:
SYSTEM STATE / CHANGES MADE / FILES UPDATED / RISK LEVEL / NEXT STEP
