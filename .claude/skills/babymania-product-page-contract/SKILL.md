---
name: babymania-product-page-contract
description: שומר על חוזה דף המוצר של BabyMania — benefits, accordion, FAQ, מבנה, עומק, חזרתיות. הפעל לפני כל בדיקה, שינוי, או audit של דף מוצר. טריגרים: "product page", "benefits", "accordion", "FAQ", "PDP", "page audit", "shoes", "clothing", "metafields", "דף מוצר", "יתרונות", "שאלות נפוצות", "section", "validator", "בדיקת מוצר", "publish product", "content quality". גם מופעל לפני live push של דף מוצר.
allowed-tools: Read, Grep, Glob
---

# babymania-product-page-contract — חוזה דף מוצר

## מתי להשתמש

- לפני בדיקה / שינוי / פרסום של דף מוצר
- כשיש בעיה בבenefits, accordion, או FAQ
- כשמתכוננים לpull request / live write של content מוצר
- לפני הרצת batch של product page agents
- כשצריך לבדוק repetition / quality / conversion impact

## מתי לא להשתמש

- שינויי theme (sections, CSS) — שייך ל-UX Guardian
- עדכוני SEO fields בלבד (title_tag, description_tag) — שייך ל-Organic SEO Guardian
- שינויים ב-navigation — שייך ל-UX Guardian

## אבחון שכבה לפני הכל

לפני כל תיקון — זהה את שכבת הבעיה:

| שכבה | סוג בעיה | מה לעשות |
|------|---------|---------|
| **DATA** | נתוני מוצר חסרים / שגויים (YAML, specs) | תקן מקור הנתונים |
| **LOGIC** | agent נותן output שגוי — לוגיקה שגויה | תקן agent prompt / logic |
| **OUTPUT** | הטקסט שנוצר לא טוב — ניסוח, עברית | תקן output בלבד |
| **WORKFLOW** | pipeline לא מחובר נכון | תקן pipeline routing |

**כלל ברזל:** לא לתקן OUTPUT אם הבעיה בLOGIC.
"שפר את הניסוח" בלי לתקן מה שגרם לניסוח הרע = patch ולא fix.

## חוזה benefits (יתרונות)

| כלל | תיאור |
|-----|-------|
| **Signal קצר** | כל benefit = signal אחד. מבנה: [feature] → [parent outcome] |
| **Parent outcome** | מה ההורה מרוויח — לא מה המוצר עושה |
| **לא הסבר** | benefits אינם מקום להסברים ארוכים |
| **אין חזרות** | כל benefit שונה מהאחר |
| **Specific** | "בד כותנה 100% — שינה ללא הזעה" ✅ / "בד איכותי" ❌ |
| **מקסימום 5** | עדיף 3 חזקים על 7 חלשים |

## חוזה accordion (הרחבה)

| כלל | תיאור |
|-----|-------|
| **מעמיק** | accordion מרחיב מה שbenefits הציגו |
| **לא חוזר** | אסור לחזור על מה שכבר כתוב ב-benefits |
| **מבנה** | כל section = נושא אחד (חומרים, גדלים, טיפול) |
| **RTL** | כל הטקסט RTL, dir="rtl" |
| **עברית טבעית** | לא תרגום מכונה |

## חוזה FAQ (שאלות נפוצות)

| כלל | תיאור |
|-----|-------|
| **התנגדויות** | FAQ = תשובות להתנגדויות לקנייה, לא חזרה על benefits |
| **לא כופל** | אסור לחזור על מה שב-benefits ו-accordion |
| **שאלות אמיתיות** | "האם המידה מדויקת?" / "כמה זמן משלוח?" |
| **Trust** | תשובות שמגדילות אמון |
| **Schema** | חייב `FAQPage` JSON-LD schema |

## בדיקת חזרתיות (Repetition Check)

חפש:
- אותה מילה / phrase בbenefits + accordion + FAQ
- אותה תועלת מוצגת פעמיים
- כותרות דומות בshoeaccordion sections

**כלל:** אם המשתמש יכול לדלג על חלק אחד ולא להפסיד מידע — יש חזרה.

## Conversion Impact Check

לפני live push:
- האם benefits מעלים רצון לקנות?
- האם FAQ מסיר חסמים לקנייה?
- האם accordion מונע שאלות שמאטות החלטה?

## פורמט פלט חובה

```
PRODUCT:             [handle / PID]
CATEGORY:            clothing / shoes / accessories / reborn
LAYER DIAGNOSIS:     DATA / LOGIC / OUTPUT / WORKFLOW
BENEFITS CHECK:      PASS / FAIL — [מה בדיוק לא תקין]
ACCORDION CHECK:     PASS / FAIL — [חזרתיות? עומק?]
FAQ CHECK:           PASS / FAIL — [התנגדויות מכוסות?]
REPETITION FOUND:    YES — [מה חוזר] / NO
PARENT_OUTCOME:      PRESENT / MISSING
FAQ_SCHEMA:          PRESENT / MISSING
LIVE_VERIFY_DONE:    YES / NO
VERDICT:             PRODUCT_CONTRACT_PASS / PRODUCT_CONTRACT_FAIL
BLOCKING_ISSUES:     [רשימה, אחרת NONE]
```

## קבצי מקור שחובה לקרוא

- `BABYMANIA-MASTER-PROMPT.md` — pipeline, agent list

## קבצים שמותר לקרוא

- `teams/product/agents/` — agent files (03-benefits, 04-faq, 04b-shoes-accordion)
- `shared/product-context/<pid>.yaml` — נתוני מוצר ספציפי
- `theme_assets/sections/bm-store-benefits.liquid` — benefits section
- `theme_assets/sections/bm-shoes-accordion.liquid` — accordion section
- `theme_assets/sections/bm-store-faq.liquid` — FAQ section

## פעולות אסורות

- לתקן OUTPUT בלי לאבחן את שכבת הבעיה
- לפרסם live בלי verify (HTTP 200 + content check)
- לדחוף benefits עם חזרות על מוצרים שונים
- לכתוב FAQ שחוזר על benefits במקום לפתור התנגדויות
- לכתוב "מוצר איכותי" בלי פרטים ספציפיים

## חוקי BabyMania

- Pipeline: `01 → 02b → [02/03b/04b/04c/05] → 06 → 07 → 09`
- Shoes pipeline: `03b → 04b → 04c → 07-shopify-publisher`
- Clothing pipeline: `02 → 03 → 04 → 05 → 06 → 07`
- לא לגעת בביגוד בפרודקשן בלי אישור
- כל push לשופיפיי = T2 לפחות, verify חובה

## טעויות נפוצות למניעה

- "תיקון ניסוח" כש-agent נותן output גנרי — הבעיה בLOGIC, לא בOUTPUT.
- לפרסם benefits של נעליים על מוצר ביגוד — pipeline שגוי.
- לשכוח לעדכן FAQ schema JSON-LD — ריך-סניפט יחסר בGoogle.
- לכתוב 7 benefits חלשים במקום 3 חזקים — פחות = יותר.
- לפרסם בלי verify HTTP 200 — מוצר אחד נכשל בפרסום יכול לא להיות מורגש בלי verify.
