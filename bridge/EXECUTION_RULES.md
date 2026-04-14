# EXECUTION RULES — חובה בכל פקודה

## בדיקת Approval Tier (חובה לפני כל פעולה)
- זהה את ה-APPROVAL_TIER מהמשימה (T0/T1/T2/T3)
- אם T3 ואין אישור אייל מפורש — עצור ודווח `AWAITING_APPROVAL`
- אם T2 — בצע + הרץ validator + דווח RISK LEVEL
- אם T0/T1 — בצע כרגיל
- אם אין APPROVAL_TIER — חשב לפי מטריצת ההחלטה ב-`docs/management/approval-policy.md`
- ראה מסמך מלא: `docs/management/approval-policy.md`

## סדר שלבים
- לפני כל פעולה — בדוק שהקלט הנדרש קיים
- אם קלט חסר — עצור ודווח MISSING_INPUT
- לא מדלגים על שלב גם אם נראה פשוט

## סנכרון בין סוכנים
- לפני הרצת סוכן — בדוק שהסוכן שלפניו סיים ויצר output
- אם output חסר — עצור ודווח PREVIOUS_STAGE_INCOMPLETE
- לא מריצים שני סוכנים במקביל אלא אם צוין במפורש

## בדיקה לפני ביצוע
- קרא את הקובץ הרלוונטי לפני שאתה עורך אותו
- אחרי עריכה — הדפס הוכחה מתוך הקובץ שהשינוי בוצע
- אם אין הוכחה — כתוב FAIL

## פורמט דיווח חובה
SYSTEM STATE
CHANGES MADE
FILES UPDATED
RISK LEVEL
NEXT STEP

## כללי עצירה
- אם קובץ לא נמצא — עצור ודווח FILE_NOT_FOUND
- אם הוראה לא ברורה — עצור ושאל
- אם יש סתירה בין קבצים — עצור ודווח CONFLICT
- לא ממשיכים לשלב הבא כשיש FAIL פתוח

## אסור בהחלט
- לבצע audit במקום edit כשביקשו edit
- להחזיר PASS בלי הוכחה מהקובץ
- לגעת בקבצים מחוץ לscope של המשימה
- להציע שלבים נוספים מחוץ למשימה הנוכחית

## משימות אורגניות — כלל STATE חובה

**כשמשימה כוללת `DOMAIN: ORGANIC` (או מתייחסת ל-HUBs / blog / organic pipeline):**

### לפני ביצוע
1. קרא: `docs/organic/מצב-הפרויקט-האורגני.md`
2. זהה את השכבה הפעילה הנוכחית (CURRENT_LAYER)
3. זהה את הפריט הפתוח הראשון (NEXT_OPEN_ITEM)
4. ודא שהמשימה הנוכחית מתאימה לפריט הפתוח — לא לשלב שלאחריו

### כלל שכבות
- אסור לדלג שכבה — גם אם היא נראית פשוטה
- אסור לפתוח item חדש אם יש item פתוח קודם באותה שכבה
- אם יש mismatch בין `BABYMANIA-MASTER-PROMPT.md` לבין `מצב-הפרויקט-האורגני.md`:
  state doc התפעולי קובע לביצוע השוטף — לא לפנות ל-master לצורך החלטות ביצוע

### בלוק STATE_CHECK — חובה בתחילת כל output אורגני
```
STATE FILE READ: YES
CURRENT LAYER: [מספר שכבה — לדוגמה: LAYER 2b]
NEXT OPEN ITEM: [הפריט הפתוח הראשון לפי state doc]
WHY THIS TASK NOW: [למה משימה זו עכשיו — לא אחרת]
WHAT IS BLOCKED AFTER THIS: [מה ייפתח / מה עדיין חסום אחרי המשימה הזו]
```

אם לא ניתן למלא את הבלוק הזה — עצור ודווח `ORGANIC_STATE_UNRESOLVED`.

---

## פורמט פקודה חובה (מ-bridge/next-task.md)
> **הערה:** Team Lead = Claude Code session המבצע. הפקודה מגיעה דרך bridge/next-task.md (נכתב ע"י GPT/אייל), לא מ-agent נפרד.

SCOPE: [שם המשימה המדויקת]
INPUT REQUIRED: [קבצים שחייבים להיות קיימים]
OUTPUT EXPECTED: [מה צריך להיווצר]
DO NOT TOUCH: [קבצים שאסור לגעת בהם]

---

## חוקים מערכתיים — לקחים מ-LAYER 3

> נוצרו: 2026-04-14 | מקור: ביצוע plan `layer3-product-seo-aeo-priority-001` (18 stages)

### 1. Generation stage — batch size
- אם stage צפוי לעבור 300–400 שניות, לא להריץ כיחידה אחת
- לבצע batch split מראש (12–15 מוצרים לבאץ')
- לא לחכות ל-timeout כדי לגלות את זה

### 2. Draft coverage gate לפני live push
- אין לבצע live push אם draft coverage קטן מ-100%
- `publisher.json` אינו תחליף ל-`seo_draft.json`
- כל מוצר target חייב `seo_draft.json` תקין לפני write ל-live

### 3. SKIP_EXISTING — חובה בכל generation stage
- כל generation stage עתידי חייב לדעת לדלג על draft קיים ותקין
- retry / resume בלי `skip_existing` נחשב recovery חלש

### 4. Post-fail classification
- אחרי FAIL של generation צריך לבדוק:
  - האם נוצרו קבצים בפועל
  - כמה נוצרו
  - האם זה logic fail אמיתי או structural timeout
- לא להניח שכל FAIL אומר אפס תוצאה

### 5. Pre-live field map verification
- לפני כתיבה ל-Shopify live חייב להיות אימות לשדות היעד
- במקרה SEO:
  - `global.title_tag`
  - `global.description_tag`
- לא להמשיך ל-live בלי field map verified

### 6. Live verify — שער חובה
- PASS של write לא מספיק
- חייב verify חי אחרי כל push
- אין לסגור שכבה בלי live verify אמיתי

### 7. Recovery principle — סדר פעולות
- אם הבעיה ב-input חסר, לא מתקנים ב-live ישירות
- סדר חובה: השלמת drafts חסרים → re-push → live verify

### 8. Runtime rule — Python path
- להשתמש בנתיב Python המלא: `C:/Users/3024e/AppData/Local/Python/pythoncore-3.14-64/python.exe`
- לא להשתמש ב-WindowsApps python stub
- שימוש ב-stub גורם ל-double-process / false duplicate detection ב-conductor

### 9. Scope rule — recovery ממוקד
- בזמן recovery אסור לגעת במוצרים שכבר עברו verify
- recovery חייב להיות ממוקד רק על failed / missing subset

### 10. Documentation rule — לקחים בכתב
- כל recovery משמעותי חייב להיכנס ל-state/journal
- לא להשאיר לקחים רק בצ'אט
