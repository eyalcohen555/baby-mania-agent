# BUILD-PLAN — תבנית דף מוצר דרופשיפינג
## מקור אמת לבנייה | Baby Mania

## עקרון על
תבנית-על אחת (17 סקשנים) מבוססת שלד ריבורן המוכח, מותאמת למוצרי-בעיה.
כל מוצר חדש = brief + תמונות + 3 variants בשופיפיי -> דף מוכן.

## מנגנון Bundle (נעול)
- זיהוי variants לפי POSITION: 1=יחידה, 2=זוג, 3=שלישייה
- שמות variants חופשיים למכירה (לדוגמה "זוג מדחומים")
- מסירים את שכבת ה-IDs הקשיחים (סביב L626-631 בקובץ המקור)
- כלל יחיד למוצר חדש: ליצור variants בסדר 1/2/3 בשופיפיי

## טבלת 17 הסקשנים
| # | סקשן | מצב בריבורן | פעולה |
|---|------|-------------|-------|
| 1 | Hero | קיים דינמי L494 | placeholders טקסט |
| 2 | Bundle | IDs קשיחים | להסיר IDs, position-based |
| 3 | Trust Badges | קיים L651 | placeholders |
| 4 | כותרת בעיה | חלש | להעצים PAS |
| 5 | העמקת בעיה | חלש | להעצים שפת לקוח |
| 6 | תמונת בעיה | חסר | לבנות |
| 7 | מחקרים | קיים L877 | placeholders |
| 8 | לפני/אחרי | קיים L1070 | placeholders |
| 9 | פתרון | קיים L1004 | placeholders |
| 10 | מוצר בפעולה | קיים L1080 | placeholders |
| 11 | mid-CTA | חסר | לבנות |
| 12 | סטטיסטיקות | חסר | לבנות |
| 13 | ביקורות | קיים L1126 | placeholders |
| 14 | למי מתאים | קיים L1231 | placeholders |
| 15 | התנגדויות/מחיר | קיים L1343 | placeholders |
| 16 | FAQ | קיים L1384 | placeholders |
| 17 | CTA סופי | קיים L1490 | placeholders |

## Placeholders — טקסט
PRODUCT_NAME, HERO_TITLE, HERO_SUBTITLE, PROBLEM_HOOK, PROBLEM_AGITATION,
RESEARCH_1/2/3, SOLUTION_TITLE, BENEFITS, REVIEWS, WHOFOR_CARDS,
OBJECTIONS, FAQ_ITEMS, FINAL_CTA, STATS

## Placeholders — מדיה
תמונות (10): IMG_HERO(אוטומטי), IMG_S2_BUNDLE, IMG_S3_TRUST, IMG_S6_PROBLEM,
IMG_S8_BEFORE_AFTER, IMG_S9_SOLUTION, IMG_S14_CARD_1..4
וידאו (3): VID_PROBLEM (סקשן 4-6), VID_DEMO (סקשן 9-10), VID_UGC (סקשן 13)

## סדר ביצוע
1. BUILD-PLAN.md + commit (מקור אמת)
2. תקן Bundle (הסר IDs קשיחים, position-based)
3. de-Rebornify (placeholders)
4. בנה S6 + S11 + S12
5. העצם S4 + S5 (PAS)
6. README + PLACEHOLDERS-MAP
7. QA + commit
8. בדיקת מוצר ראשון (Tempio) ב-DUPE

## כללי עבודה
- אחרי כל שלב: commit + עדכון ARCHITECTURE.md
- בדיקה ב-DUPE לפני LIVE תמיד
- לא לשנות תוכנית ללא אישור מפורש
