# Shoes Tag Taxonomy Proposal — BabyMania

**תאריך:** 2026-05-10  
**מצב:** READ-ONLY PLANNING — אין כתיבות Shopify  
**מבוסס על:** Layer 6 closure backlog, shoes-journal.md, Phase 7C long-run plan

---

## 1. רקע

~65 מוצרי נעליים חסומים מתיוג מאז Phase 7C Batch 1 (2026-05-05).  
חסימה: "shoe_blocked" — keyword match על כותרות כגון: נעל, נעליים, סנדל, סנדלים, סניקרס, boot, sandal, sneaker, כפכף, בלרינה, first-walkers.

**מטרת מסמך זה:** לספק taxonomy מלא לנעליים כדי שתהיה תשתית לסיווג ידני + image review בשלב הבא.

---

## 2. תגים מוצעים

### shoes-sneakers

**שם עברי לתצוגה:** סניקרס  
**הגדרה:** נעל ספורט או קז'ואל עם סוליה קשה/גומי, גפה בד או עור — לתינוק/פעוט.  
**Visual cues לimage review:** לייס או סקוץ', גפה בד, גומי בסוליה, סוליה מעוצבת.  
**דוגמאות מוצרים:**
- "Baby Sneakers Spring Summer Boys Girls Soft Sole"
- "Anti-Slip Soft Sole First Walkers Infant Lightweight Shoes" (אם גפה סגורה + גומי)

**מתאים ל-multi-tag עם:** `shoes-soft-sole`, `shoes-first-step`

---

### shoes-sandals

**שם עברי לתצוגה:** סנדלים  
**הגדרה:** נעל פתוחה — חשיפת בהונות או עקב — בעיקר לקיץ.  
**Visual cues:** רצועות, בוהן גלוי, עקב פתוח, בד/עור/סינטטי.  
**דוגמאות:**
- "Baby Sandals Summer Breathable Air Mesh"
- כפכפי בד לתינוק, סנדל עם רצועות

**מתאים ל-multi-tag עם:** `shoes-first-step`, `shoes-soft-sole`

---

### shoes-boots

**שם עברי לתצוגה:** מגפיים  
**הגדרה:** מגף לרגל או לקרסול — מכסה את הקרסול לפחות.  
**Visual cues:** גפה גבוהה, רוכסן/כפתור/גומי, עור/בד עבה.  
**דוגמאות:**
- מגפוני חורף לתינוק
- בוטים לאירוע

**מתאים ל-multi-tag עם:** `shoes-elegant`

---

### shoes-first-step

**שם עברי לתצוגה:** נעלי צעד ראשון  
**הגדרה:** עיצוב ייעודי לתינוק שרק מתחיל ללכת — סוליה גמישה, תמיכה בקרסול, קל משקל.  
**Visual cues:** סוליה רכה/גמישה, גודל מיני, עיצוב תומך.  
**keyword hints:** "first-walkers", "first step", "צעד ראשון", "infant"  
**גיל אינדיקטיבי:** 0–18 חודשים (אינדיקציה בלבד — לא תג גיל)

**מתאים ל-multi-tag עם:** `shoes-soft-sole`, `shoes-sneakers`, `shoes-sandals`

---

### shoes-elegant

**שם עברי לתצוגה:** נעליים אלגנטיות  
**הגדרה:** נעל לאירוע, שמחה, ברית — לא לשימוש יומיומי.  
**Visual cues:** עור/לכה, פפיון, עיטור, צבע לבן/שמפניה/שחור, עקב נמוך.  
**keyword hints:** "elegant", "formal", "party", "אלגנטי", "לאירוע"

**מתאים ל-multi-tag עם:** `shoes-boots`, `occ-brit`, `occ-event`

---

### shoes-soft-sole

**שם עברי לתצוגה:** סוליה רכה  
**הגדרה:** סוליה רכה ומתאימה לזחילה או צעדים ראשונים — לא סוליה קשה.  
**Visual cues:** סוליה מגומי דק, עיטורים מגומי נגד החלקה, גמישות גלויה.  
**keyword hints:** "soft sole", "anti-slip soft", "סוליה רכה"

**מתאים ל-multi-tag עם:** `shoes-first-step`, `shoes-sneakers`, `shoes-sandals`

---

### shoes-review-only

**שם עברי לתצוגה:** ממתין לבדיקה  
**הגדרה:** מוצר שלא ניתן לסווג ללא ראיית תמונה — כותרת לא מספקת.  
**שימוש:** Internal only. לא Smart Collection.  
**תנאי:** confidence LOW מ-image review agent.

---

## 3. תגים שלא ליצור

| תג | סיבה |
|---|---|
| `shoes-doll` | אין עדות לקטגוריה נפרדת של נעלי בובה בחנות |
| `shoes-eu-22`, `shoes-size-22`, `shoes-22` | NEVER TAG BY SIZE — מדיניות קשיחה |
| `shoes-age-0m`, `shoes-age-12m` | NEVER TAG BY AGE — מדיניות קשיחה |
| `shoes-crocs` | שם מותג — לא קטגוריה taxonomy |
| `shoes-winter`, `shoes-summer` | חפיפה עם season-* (לא בסקופ) |

---

## 4. עץ החלטה — תיוג נעל

```
מוצר נעל →
  ├── האם סוליה רכה? → shoes-soft-sole (+)
  ├── האם מיועד לצעד ראשון? → shoes-first-step (+)
  ├── האם נעל פתוחה/סנדל? → shoes-sandals
  ├── האם מגף (מכסה קרסול)? → shoes-boots
  ├── האם ספורטיבי/קז'ואל עם סוליה קשה? → shoes-sneakers
  ├── האם אלגנטי/לאירוע? → shoes-elegant
  └── לא ברור מכותרת → shoes-review-only → image review
```

**חוק multi-tag:** אם מוצר עומד בשניים → שניהם. מקסימום 3 תגי shoes- למוצר.

---

## 5. כללי image review

- **HIGH confidence:** ממצאים ברורים מתמונה → כלול בbatch planning
- **MEDIUM confidence:** צריך בדיקה נוספת → shoes-review-only זמני
- **LOW confidence:** shoes-review-only קבוע → human review

**אסור לתייג לפי:**
- גודל EU/cm המצוין בכותרת בלבד
- גיל "0-6m" בלבד ללא ראיה לסוג הנעל
- שם מותג בלבד

---

## 6. מצב נוכחי ורמות חסימה

| רמה | סטטוס | מה נדרש |
|---|---|---|
| Taxonomy approved | PENDING | אישור אייל על מסמך זה |
| Image review agent | NOT BUILT | spec ב-shoes-image-review-spec.md |
| EU size mapping decision | PENDING | החלטת אייל — מה לעשות עם גדלים בכותרות |
| Live write T3 | BLOCKED | עד שכל שלבים לעיל הושלמו |

---

*מסמך זה הוא הצעה בלבד. אין כתיבות Shopify ללא אישור T3 מאייל.*
