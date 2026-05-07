# Phase 7C — Batch 10 Business Audit (READ-ONLY)

**Generated:** 2026-05-07
**Mode:** BUSINESS_AUDIT — READ-ONLY, אין כתיבה ל-Shopify
**Auditor:** manual business logic review per BabyMania category rules
**Source:** output/tags/phase7c-batch10-plan.json

---

## סיכום ממצאים

| מדד | ערך |
|-----|-----|
| מוצרים שנבחרו ב-Batch 10 | 12 |
| APPROVE_FOR_BATCH10 | **1** |
| REJECT_FALSE_POSITIVE | **9** |
| MOVE_TO_REVIEW_ONLY | **2** |
| אחוז false positives | **75%** |

**VERDICT: `READY_FOR_REVISED_PHASE7C_BATCH10_PLAN`**
(batch מקורי מבוטל — נדרש plan מחודש עם 1 מוצר בלבד, + 2 review ידני)

---

## כלל עסקי מחמיר (הזכורון)

`type-set` מותר **רק** אם המוצר הוא:
- סט בגדים לתינוק / ילד
- מארז בגדי תינוק
- סט אביזרי ביגוד (כגון: רומפר + כובע + כריות)
- מארז מתנה המכיל בגדי תינוק

`type-set` **אסור** אם המילה set/pcs/סט מופיעה טכנית בלבד וגוף המוצר הוא:
- בגד ים / חלק ים
- טקסטיל / טטרה / שמיכה / עטיפה
- מברשות ניקוי / ציוד היגיינה
- אחסון פורמולה / מיכל אוכל
- צעצוע אמבטיה
- ציוד לידה לאם (postpartum)
- שירותים ניידים / potty

---

## טבלת Audit לכל מוצר

| # | product_id | title | proposed_tag | source_trace | business_fit | decision | reason |
|---|-----------|-------|-------------|-------------|-------------|---------|--------|
| 1 | 9873511022905 | בגד ים לבבות דגם מאיה | type-set | 'set' in handle | ❌ לא | REJECT_FALSE_POSITIVE | "בגד ים" = בגד ים/שחייה. handle: swimsuit-set. "set" טכני של ביגוד ים, לא סט בגדים. |
| 2 | 9606822265145 | יחידת קומות לאחסון אבקת פורמולה | type-set | 'pcs' in handle | ❌ לא | REJECT_FALSE_POSITIVE | אחסון אבקת פורמולה — ציוד להכנת בקבוק, לא בגד ולא סט בגדים. |
| 3 | 9605662245177 | מארז טטרה מיוחד לתינוקות | type-set | 'set' in handle | ❌ לא | REJECT_FALSE_POSITIVE | "טטרה" = בדי muslin/swaddle. אף שיש "מארז", זהו סט טקסטיל ולא סט בגדים לאוסף סטים. |
| 4 | 9605662343481 | מברשות לניקוי הבקבוקים | type-set | 'set' in handle | ❌ לא | REJECT_FALSE_POSITIVE | "מברשות ניקוי בקבוקים" = ציוד היגיינה. bottle-brush-set. אין קשר לסט בגדים. |
| 5 | 9605662212409 | סט טטרה הדפס לתינוק | type-set | 'סט' in title | ❌ לא | REJECT_FALSE_POSITIVE | "סט טטרה" = סט בדי muslin/bib/burp-cloth. טקסטיל ולא ביגוד. |
| 6 | 9096636825913 | סט לתינוק עד 3 חודשים - מארז מתנה מפנק | type-set | 'סט' in title | ⚠️ לא ברור | MOVE_TO_REVIEW_ONLY | Title מרמז על מארז מתנה לתינוק 0-3 חודשים — אפשרי שמכיל בגדים, אפשרי שמכיל אביזרים מעורבים. Handle עברי בלבד — לא ניתן לקבוע תוכן. נדרש בדיקה ידנית. |
| 7 | 9096628732217 | סט שמיכות עטיפה פרחוני | type-set | 'סט' in title | ❌ לא | REJECT_FALSE_POSITIVE | "סט שמיכות עטיפה" = שמיכות/עטיפות. Handle עברי. טקסטיל ולא ביגוד. |
| 8 | 9894032539961 | ספינר לתינקות 3 חלקים | type-set | 'set' in handle | ❌ לא | REJECT_FALSE_POSITIVE | "ספינר לאמבטיה" = צעצועי אמבטיה. handle: bath-toys-spinner-suction-cup-rattles. אין קשר לסט בגדים. |
| 9 | 9605887689017 | סרבל קיצי לתינוקות | type-set | 'set' in handle | ⚠️ לא ברור | MOVE_TO_REVIEW_ONLY | Handle: "rompers-headband-set" — ייתכן שזה סרבל + ריבון (2 פריטים = סט ביגוד). אבל ייתכן שה-type הנכון הוא type-romper ולא type-set. נדרש בדיקה ידנית לפי תמונה + תיאור. |
| 10 | 9605441945913 | רצועת בטן לאחר לידה | type-set | 'set' in handle | ❌ לא | REJECT_FALSE_POSITIVE | "רצועת בטן לאחר לידה" = ציוד postpartum לאם. handle: corset-postpartum-belly-band. לא מוצר תינוק ולא ביגוד תינוק. |
| 11 | 9839248769337 | שירותים ניידים לילדים מבית בייבי מניה | type-set | 'pcs' in handle | ❌ לא | REJECT_FALSE_POSITIVE | "שירותים ניידים" = portable potty / toilet. handle: folding-toilet-portable-child-travel-potty. אין קשר לסט בגדים. |
| 12 | 9687563338041 | שלוש סטים של עונת מעבר מבית בייבי מניה | type-set | 'סטים' in title | ✅ כן | APPROVE_FOR_BATCH10 | Title: "שלוש סטים של עונת מעבר" — ריבוי סטי בגדים. Handle: "girls-3pcs-spring-fall-outfit-set" — 3-piece outfit set for girls, spring/fall. מוצר ביגוד ברור + source trace כפול (title + handle). |

---

## פירוט לכל REJECT

### 1. בגד ים לבבות דגם מאיה (9873511022905)
- **עבר safety בסריקה כי:** "set" ב-handle התאים טכנית לtype-set
- **הבעיה:** "בגד ים" = swimwear. ה-"set" ב-`swimsuit-set` מתאר קומפוזיציה של בגד ים (למשל: חלק עליון + תחתית), לא סט בגדים לאוסף "סטים"
- **FALSE_POSITIVE_KW שהחמיץ:** "swimsuit" לא היה ב-keyword list (היה "swimwear")

### 2. יחידת קומות לאחסון אבקת פורמולה (9606822265145)
- **עבר safety בסריקה כי:** "pcs" ב-handle (3pcs/4pcs)
- **הבעיה:** מוצר אחסון אבקת פורמולה — לא ביגוד, לא אביזר ביגוד

### 3. מארז טטרה מיוחד לתינוקות (9605662245177)
- **עבר safety בסריקה כי:** "set" ב-handle, "מארז" לא היה ב-false-positive keywords
- **הבעיה:** "טטרה" / muslin-swaddle — טקסטיל, לא ביגוד. "מארז" בלבד אינו מספיק

### 4. מברשות לניקוי הבקבוקים (9605662343481)
- **עבר safety בסריקה כי:** "set" ב-handle (bottle-brush-set)
- **הבעיה:** מברשות ניקוי בקבוקים — ציוד היגיינה. המילה "מברשות" לא הייתה ב-false-positive list

### 5. סט טטרה הדפס לתינוק (9605662212409)
- **עבר safety בסריקה כי:** "סט" ב-title
- **הבעיה:** "סט טטרה" — "טטרה" הייתה ב-false-positive list אבל רק בעברית גולמית, לא כ-prefix לצירוף "סט טטרה"

### 7. סט שמיכות עטיפה פרחוני (9096628732217)
- **עבר safety בסריקה כי:** "סט" ב-title, handle עברי ולא נסרק ל-false-positives
- **הבעיה:** "שמיכות עטיפה" = blankets. "שמיכה" הייתה ב-false-positive list אבל בצורת יחיד בלבד

### 8. ספינר לתינקות 3 חלקים (9894032539961)
- **עבר safety בסריקה כי:** "set" ב-handle
- **הבעיה:** "ספינר" / "צעצועי אמבטיה" — לא היה ב-false-positive list

### 10. רצועת בטן לאחר לידה (9605441945913)
- **עבר safety בסריקה כי:** "set" ב-handle (3in1...strap-body-shaper)
- **הבעיה:** מוצר postpartum לאם — לא מוצר תינוק בכלל

### 11. שירותים ניידים לילדים (9839248769337)
- **עבר safety בסריקה כי:** "pcs" ב-handle (10pcs-folding-toilet)
- **הבעיה:** potty / portable toilet — "שירותים" לא היה ב-false-positive list

---

## לקחים — כשלי הסריקה האוטומטית

| כשל | תיאור | תיקון נדרש |
|-----|-------|-----------|
| swimsuit≠swimwear | "swimsuit" לא היה ב-keyword list, רק "swimwear" | הוסף: swimsuit, בגד-ים |
| מברשות | לא היה ב-false-positive list | הוסף: brush, מברשות |
| ספינר/צעצוע | לא היה ב-false-positive list | הוסף: toy, spinner, potty, toilet, potty, urinal |
| פורמולה | לא היה ב-false-positive list | הוסף: formula, powder, storage, container |
| postpartum | לא היה ב-false-positive list | הוסף: postpartum, belly-band, corset |
| שמיכות (plural) | רק "שמיכה" (יחיד) היה ב-list | הוסף: שמיכות |
| "סט" עם false product | "סט" בtitle לא מספיק ללא בדיקת product category | נדרש: semantic check על title — "סט + [קטגוריית ביגוד]" |

---

## REVIEW_ONLY — נדרש בדיקה ידנית

### PID 9096636825913 — "סט לתינוק עד 3 חודשים - מארז מתנה מפנק"
- Handle עברי בלבד — לא ניתן לקבוע תוכן
- ייתכן: מארז מתנה עם בגדים → APPROVE
- ייתכן: מארז מתנה עם אביזרים מעורבים → REJECT
- **פעולה נדרשת:** בדיקה ידנית ב-Shopify admin — ראה תמונות + תיאור

### PID 9605887689017 — "סרבל קיצי לתינוקות"
- Handle: "rompers-headband-set" — ייתכן סרבל + ריבון (= סט ביגוד) 
- ייתכן: type-romper עם headband bonus → type-set APPROVE
- ייתכן: type-romper בלבד, ה-headband חלק מהמוצר → type-romper REJECT מ-type-set
- **פעולה נדרשת:** בדיקה ידנית — כמה חלקים יש במוצר?

---

## APPROVE — מוצר אחד

### PID 9687563338041 — "שלוש סטים של עונת מעבר מבית בייבי מניה"
- ✅ Title: "שלוש סטים של עונת מעבר" — ביגוד מובהק
- ✅ Handle: "girls-3pcs-spring-fall-outfit-set" — outfit set לבנות
- ✅ Gender: girl (מ-handle)
- ✅ אין false-positive flags
- ✅ Source trace כפול: title + handle
- proposed_new_tags: `type-set`, `gender-girl`

---

## המלצה

**Batch 10 המקורי (12 מוצרים) — בטל לחלוטין.**

נדרש:
1. צור REVISED plan עם PID 9687563338041 בלבד (1 מוצר)
2. בדיקה ידנית ל-2 מוצרי REVIEW_ONLY לפני הכנסתם לבatch עתידי
3. עדכן false-positive keyword list בסקריפט הסריקה (ראה טבלת לקחים)
4. ה-SAFE pool של Phase 7C הגיע לסופו — לאחר Batch 10 המחודש, שארית הבלתי-מוגנים נדרשת לaudit ידני

---

*דוח זה הוא READ-ONLY. אין כתיבה ל-Shopify. Batch 10 המקורי לא בוצע.*
