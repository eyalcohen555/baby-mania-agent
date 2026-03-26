TASK: בדיקת מעגל question מלא
LAYER: 1
BLOCKER: חסר ערך לביצוע
ACTION: שאל שאלה אחת בלבד ב-bridge/last-result.md: "מה הערך לכתיבה בתוך test-question-output.txt?" ואז עצור. אל תיצור את הקובץ לפני שמתקבלת תשובה ב-bridge/telegram-response.md. אם קיימת תשובה עם content, כתוב את התוכן שקיבלת לתוך test-question-output.txt ועדכן את bridge/last-result.md שהמשימה הושלמה.
FILES_ALLOWED: bridge/last-result.md, bridge/telegram-response.md, test-question-output.txt
FILES_FORBIDDEN: כל קובץ אחר
RULES:
- אם אין תשובה ב-bridge/telegram-response.md, רק שאל ועצור
- השאלה חייבת להיות קצרה וברורה
- אל תכתוב test-question-output.txt לפני שיש תשובה
- אם יש תשובה, כתוב בדיוק את הערך שהתקבל בלי שינוי
EXPECTED: קודם מופיעה שאלה ב-last-result.md, ואחרי תשובה מטלגרם נוצר test-question-output.txt עם הערך שנשלח
