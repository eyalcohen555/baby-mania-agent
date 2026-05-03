# Layer 6 — Phase 5 Human Review Pack

**תאריך:** 2026-05-03  
**מוכן עבור:** אייל — בדיקה ידנית לפני כל שינוי חי  
**מקור:** Phase 4 Dry Run (59 מוצרים)

---

## SYSTEM STATE

| שדה | ערך |
|---|---|
| שלב | Phase 4 COMPLETE → Phase 5 Human Review |
| מוצרים שנבדקו ב-Dry Run | 59 |
| PASS | 30 |
| NEEDS_REVIEW | 29 |
| BLOCKED | 0 |
| ציון איכות ממוצע | 77.7 |
| שינויים חיים בשופיפיי | **NO** |
| Phase 6 | **NOT OPEN** |

---

## איך לבדוק

**מה זה Native Tag?**  
תג פנימי באנגלית שנכנס לשופיפיי. הלקוח לא רואה אותו ישירות.  
דוגמה: `type-romper`, `age-0-3m`, `gender-girl`

**מה זה תווית לקוח?**  
מה שיוצג בתפריט הניווט / פילטר ללקוח.  
דוגמה: אוברולים, 0-3 חודשים, בנות

**איך לסמן:**
- **APPROVE** — התגיות נכונות, ניתן להמשיך לשלב הבא
- **APPROVE_WITH_NOTE** — נכון בערך, יש הסתייגות קטנה לרשום (לדוגמה: גיל חסר אבל המוצר ברור)
- **FAIL** — תגית שגויה, מטעה, או חסרה משהו קריטי — לא לאשר

**כללים חשובים:**
- אם מגדר הוסק מצבע (ורוד = בנות, כחול = בנים) — סמן **FAIL**. המערכת אסור שתסיק מגדר מצבע.
- אם חסר גיל אבל המוצר ברור לאייל — אפשר APPROVE_WITH_NOTE עם הגיל הנכון.
- אם תפריט עלול להטעות לקוח — סמן **FAIL**.
- ⚠️ = נקודה שצריכה תשומת לב מיוחדת

---

## REVIEW ITEMS

---

### מוצר 1 — ✅ PASS טוב (clothing_yaml)

- **product_id:** 9874906349881
- **title:** אוברול ג'ינס מתוק מבית בייבי מניה דגם זוהר
- **handle:** baby-summer-clothing-denim-rompers-toddler-newborn-baby-boys-girls-sleeveless-button-pocket-rompers-jumpsuits-casual-outfits
- **product_group:** clothing_yaml
- **status:** PASS
- **quality_score:** 96.6
- **current_tags (קיים בשופיפיי):** אוברול
- **proposed_native_tags:** `type-romper`, `age-newborn`, `season-summer`, `fabric-denim`, `occ-everyday`, `gender-girl`, `style-casual`
- **customer_labels_he:** אוברולים | יילוד | קיץ | ג'ינס | יומיומי | בנות | קז'ואל
- **blocked_tags:** —

**missing / review reason:** כל 7 קטגוריות נמצאו. מקורות ברורים. דוגמה מלאה לתיוג תקין.

**למה המערכת הציעה את התגיות:**
- `type-romper` — תג קיים "אוברול" הוצב למפה
- `age-newborn` — ה-handle מכיל "newborn" — זיהוי ישיר
- `season-summer` — הכותרת מכילה "summer"
- `fabric-denim` — הכותרת מכילה "denim"
- `occ-everyday` — ברירת מחדל לסוג אוברול
- `gender-girl` — ה-handle מכיל "girls" (לא מצבע)
- `style-casual` — ה-handle מכיל "casual"

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-romper` = אוברולים — נכון?
- [ ] גיל: `age-newborn` מ-"newborn" בה-handle — נכון?
- [ ] עונה: `season-summer` מ-"summer" בכותרת — נכון?
- [ ] בד/חומר: `fabric-denim` = ג'ינס — נכון?
- [ ] מגדר: `gender-girl` מ-"girls" בה-handle, לא מצבע — נכון?
- [ ] תווית עברית: "אוברולים | יילוד | קיץ | ג'ינס | בנות" — מתאים לתפריט?
- [ ] המוצר לא ייכנס לקטגוריה שגויה

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 2 — ✅ PASS טוב (clothing_yaml) — ⚠️ גיל: toddler vs infant בה-handle

- **product_id:** 9688660312377
- **title:** אוברול ג'ינס דגם אתי
- **handle:** babys-stylish-ruffled-ripped-denim-long-sleeve-belted-romper-toddler-infant-girls-button-down-bodysuit-for-spring-fall-outdoor-wear
- **product_group:** clothing_yaml
- **status:** PASS
- **quality_score:** 96.2
- **current_tags:** אוברול
- **proposed_native_tags:** `type-romper`, `age-2-3y`, `season-spring-fall`, `fabric-denim`, `occ-everyday`, `gender-girl`, `style-modern`
- **customer_labels_he:** אוברולים | 2-3 שנים | אביב/סתיו | ג'ינס | יומיומי | בנות | מודרני
- **blocked_tags:** —

**missing / review reason:** ה-handle מכיל גם "toddler" (= 2-3y) וגם "infant" (= תינוק). המערכת בחרה "toddler" ונתנה age-2-3y. אם המוצר מיועד לתינוק, הגיל שגוי.

**למה המערכת הציעה את התגיות:**
- `type-romper` — תג קיים "אוברול"
- `age-2-3y` — ה-handle מכיל "toddler" → הסקת גיל 2-3y (גבר על "infant")
- `season-spring-fall` — ה-handle מכיל "spring-fall"
- `fabric-denim` — הכותרת מכילה "denim"
- `gender-girl` — ה-handle מכיל "girls"
- `style-modern` — התיאור מכיל מילות סגנון

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-romper` = אוברולים — נכון?
- [ ] גיל: המוצר מיועד ל-2-3y (toddler) או לתינוק (infant)? — **לבדוק בשופיפיי**
- [ ] עונה: `season-spring-fall` — נכון לאוברול ג'ינס ארוך?
- [ ] בד/חומר: `fabric-denim` — נכון?
- [ ] מגדר: `gender-girl` מ-"girls" בה-handle — נכון?
- [ ] תווית עברית: "2-3 שנים" לעומת "תינוק" — מה נכון לתפריט?
- [ ] המוצר לא ייכנס לקטגוריה שגויה

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 3 — ✅ PASS טוב (shoes_yaml) — ⚠️ תג קיים "newborn-clothing" מול גיל מוצע 6-12m

- **product_id:** 9615375565113
- **title:** נעל אלגנטית צעד ראשון לבנות
- **handle:** girls-mary-jane-shoes-children-solid-color-bow-round-toe-bow-2024-new-kids-fashion-soft-moccasin-shoes-baby-first-walker-shoes
- **product_group:** shoes_yaml
- **status:** PASS
- **quality_score:** 95.4
- **current_tags (קיים בשופיפיי):** baby-gift, baby-shoes, elegant-baby, everyday-baby-wear, girls-clothing, **newborn-clothing**
- **proposed_native_tags:** `type-shoes`, `age-6-12m`, `season-unknown`, `occ-gift`, `occ-special-event`, `occ-everyday`, `occ-first-step`, `gender-girl`, `style-elegant`
- **customer_labels_he:** נעליים | **6-12 חודשים** | מתנה | אירוע מיוחד | יומיומי | צעד ראשון | בנות | אלגנטי
- **blocked_tags:** —

**missing / review reason:** בשופיפיי יש תג "newborn-clothing" (= יילוד, 0-3m), אבל המערכת מציעה age-6-12m כי ה-handle מכיל "first-walker". נעלי צעד ראשון בדרך כלל מיועדות ל-6-12m. יש סתירה — איזה גיל נכון?

**למה המערכת הציעה את התגיות:**
- `type-shoes` — תג קיים "baby-shoes"
- `age-6-12m` — ה-handle מכיל "first-walker" → הסקת גיל 6-12m (⚠️ מנוגד ל-"newborn-clothing")
- `season-unknown` — אין מקור לעונה, נעל כל-עונתית
- `occ-gift`, `occ-special-event` — תג קיים "baby-gift", "elegant-baby"
- `occ-first-step` — הכותרת מכילה "צעד ראשון"
- `gender-girl` — תג קיים "girls-clothing"
- `style-elegant` — תג קיים "elegant-baby"

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-shoes` = נעליים — נכון?
- [ ] גיל: "newborn-clothing" קיים בשופיפיי VS "first-walker" = 6-12m — **איזה נכון?**
- [ ] עונה: `season-unknown` לנעל — האם לא לתת עונה?
- [ ] בד/חומר: אין fabric tag — האם חסר?
- [ ] מגדר: `gender-girl` מ-"girls-clothing" — נכון?
- [ ] תווית עברית: "6-12 חודשים | צעד ראשון | בנות | אלגנטי" — מתאים לתפריט?
- [ ] המוצר לא ייכנס לקטגוריה שגויה (newborn vs 6-12m עלול לגרום לבלבול לקוח)

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 4 — ✅ PASS טוב (shoes_yaml) — ⚠️ handle מכיל "0-to-3-years-old"

- **product_id:** 9606764462393
- **title:** נעל קז'ואל במיוחד לתינוקות
- **handle:** baby-toddler-shoes-four-seasons-shoes-0-to-3-years-old-baby-shoes-soft-bottom-non-slip-girls-boys-mesh-breathable-single-shoes
- **product_group:** shoes_yaml
- **status:** PASS
- **quality_score:** 94.5
- **current_tags:** baby-gift, baby-shoes, everyday-baby-wear, **neutral-baby-outfit**, newborn-clothing
- **proposed_native_tags:** `type-shoes`, `age-2-3y`, `season-unknown`, `occ-gift`, `occ-everyday`, `gender-neutral`, `style-casual`
- **customer_labels_he:** נעליים | 2-3 שנים | מתנה | יומיומי | ניוטרלי | קז'ואל
- **blocked_tags:** —

**missing / review reason:** ה-handle מכיל "0-to-3-years-old" (טווח של 3 שנים — בדרך כלל חסום). המערכת מצאה "toddler" קודם ונתנה age-2-3y ללא חסימה. גם "four-seasons-shoes" בה-handle = כל-עונה → season-unknown נכון.

**למה המערכת הציעה את התגיות:**
- `type-shoes` — תג קיים "baby-shoes"
- `age-2-3y` — "baby-toddler" בה-handle → toddler_heuristic (⚠️ handle גם מכיל "0-to-3-years-old")
- `season-unknown` — "four-seasons" → לא לייחס עונה
- `occ-gift` — תג קיים "baby-gift"
- `occ-everyday` — תג קיים "everyday-baby-wear"
- `gender-neutral` — תג קיים "neutral-baby-outfit" (מקור אמין)
- `style-casual` — הכותרת מכילה "קז'ואל"

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-shoes` — נכון?
- [ ] גיל: handle מכיל "0-to-3-years-old" אבל המערכת נתנה age-2-3y — **האם 2-3y נכון, או שיש לחסום גיל לגמרי?**
- [ ] עונה: `season-unknown` ל"four-seasons" — נכון?
- [ ] מגדר: `gender-neutral` מ-"neutral-baby-outfit" (תג קיים) — נכון?
- [ ] תווית עברית: "נעליים | 2-3 שנים | ניוטרלי" — מתאים לתפריט?
- [ ] האם המוצר יופיע רק תחת "2-3 שנים" בעוד שהנעל מיועדת ל-0-3y?

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 5 — ✅ PASS טוב (yaml_gap) — ⚠️ אין YAML, כל המקורות מ-title/handle

- **product_id:** 10190523302201
- **title:** Children's Summer New Arrival Boys' Regular Striped Teddy Bear Short T-Shirt and Shorts Two-Piece Set
- **handle:** children-s-summer-new-arrival-boys-regular-striped-teddy-bear-short-t-shirt-and-shorts-casual-sport-two-piece-set
- **product_group:** yaml_gap
- **status:** PASS
- **quality_score:** 96.3
- **current_tags:** (ריק — אין תגים בשופיפיי)
- **proposed_native_tags:** `type-set`, `age-3-6m`, `season-summer`, `fabric-knit`, `occ-everyday`, `gender-boy`, `style-striped`
- **customer_labels_he:** סטים | 3-6 חודשים | קיץ | סריג | יומיומי | בנים | פסים
- **blocked_tags:** —

**missing / review reason:** אין YAML, אין תגים קיימים. כל המקורות מ-title/handle/body בלבד. מקור הגיל (age-3-6m) מצוין כ-"yaml_desc" אבל למוצר אין קובץ YAML — ייתכן שהגיל הגיע מהתיאור בשופיפיי. נדרש אימות ידני.

**למה המערכת הציעה את התגיות:**
- `type-set` — הכותרת מכילה "Two-Piece Set"
- `age-3-6m` — מהתיאור (body_html) — ⚠️ נדרש אימות, מקור לא ברור
- `season-summer` — הכותרת מכילה "Summer"
- `fabric-knit` — הכותרת מכילה "Knitted"
- `occ-everyday` — ברירת מחדל לסט
- `gender-boy` — הכותרת מכילה "Boys'"
- `style-striped` — הכותרת מכילה "Striped"

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-set` = סטים — נכון?
- [ ] גיל: `age-3-6m` — **לבדוק בפועל בשופיפיי, המקור לא ברור**
- [ ] עונה: `season-summer` — נכון?
- [ ] בד/חומר: `fabric-knit` = סריג — נכון לסט קיץ?
- [ ] מגדר: `gender-boy` — נכון?
- [ ] תווית עברית: "סטים | 3-6 חודשים | קיץ | בנים | פסים" — מתאים לתפריט?
- [ ] המוצר לא ייכנס לקטגוריה שגויה

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 6 — 🔶 NEEDS_REVIEW — NO_AGE_FOUND, handle קצר

- **product_id:** 9688934940985
- **title:** אוברול בייבי לתינוק – Baby Bear Cozy Set
- **handle:** baby-bear-cozy-set
- **product_group:** clothing_yaml
- **status:** NEEDS_REVIEW
- **quality_score:** 59.1
- **current_tags:** אוברול
- **proposed_native_tags:** `type-romper`, `season-unknown`, `occ-everyday`, `gender-unknown`
- **customer_labels_he:** אוברולים | יומיומי
- **blocked_tags:** —

**missing / review reason:** ה-handle קצר מאוד — "baby-bear-cozy-set". אין מידע גיל, מגדר, עונה, או בד. ציון נמוך: 59.1. כל 4 התגיות מגיעות מברירת מחדל בלבד.

**למה המערכת הציעה את התגיות:**
- `type-romper` — תג קיים "אוברול"
- `season-unknown` — ברירת מחדל (אין מקור)
- `occ-everyday` — ברירת מחדל לאוברול
- `gender-unknown` — ברירת מחדל (אין מקור)

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-romper` — נכון? (ייתכן שזה "set" ולא "romper")
- [ ] גיל: חסר לחלוטין — מה גיל "Baby Bear Cozy Set"? לבדוק בשופיפיי
- [ ] עונה: "cozy" מרמז חורף/בד רך — האם `season-winter`?
- [ ] בד/חומר: אין fabric — האם יש פרטי בד בשופיפיי?
- [ ] מגדר: gender-unknown — לבדוק בשופיפיי
- [ ] תווית עברית: רק "אוברולים | יומיומי" — האם מספיק לתפריט?
- [ ] לסמן לצורך העשרת YAML ידנית

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 7 — 🔶 NEEDS_REVIEW — NO_AGE_FOUND, handle עברי

- **product_id:** 10026520445241
- **title:** אוברול בייבי מניה דגם חן
- **handle:** אוברול-בייבי-מניה-דגם-חן-מתנה
- **product_group:** clothing_yaml
- **status:** NEEDS_REVIEW
- **quality_score:** 78.8
- **current_tags:** אוברול
- **proposed_native_tags:** `type-romper`, `season-summer`, `fabric-cotton`, `occ-gift`, `gender-unknown`, `style-modern`
- **customer_labels_he:** אוברולים | קיץ | כותנה | מתנה | מודרני
- **blocked_tags:** —

**missing / review reason:** handle בעברית — אין מידע גיל. גם מגדר חסר. ה-handle מכיל "מתנה" → occ-gift נכון. עונה ובד מגיעים מהתיאור. המוצר עשוי להיות ניוטרלי.

**למה המערכת הציעה את התגיות:**
- `type-romper` — תג קיים "אוברול"
- `season-summer` — התיאור (body_html) מכיל מילת קיץ
- `fabric-cotton` — התיאור מכיל כותנה
- `occ-gift` — ה-handle העברי מכיל "מתנה"
- `gender-unknown` — ברירת מחדל, אין מקור מגדרי
- `style-modern` — התיאור מכיל מילות סגנון

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-romper` — נכון?
- [ ] גיל: חסר — מה הגיל של "דגם חן"? לבדוק בשופיפיי
- [ ] עונה: `season-summer` מהתיאור — נכון?
- [ ] בד/חומר: `fabric-cotton` מהתיאור — נכון?
- [ ] מגדר: gender-unknown — לבנות? לבנים? ניוטרלי?
- [ ] תווית עברית: חסרות תווית גיל ומגדר — האם מוצר יופיע בפילטר בלי אלה?
- [ ] לסמן לצורך העשרת YAML

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 8 — 🔶 NEEDS_REVIEW — NO_AGE_FOUND, נעל קיץ

- **product_id:** 9607363232057
- **title:** נעל הלו קיטי עם אורות לילדות
- **handle:** 2024-summer-baby-led-light-sandals-for-girls-cute-hello-kitty-childrens-casual-shoes-anti-slip-kids-beach-shoes-outdoor-shoes
- **product_group:** shoes_yaml
- **status:** NEEDS_REVIEW
- **quality_score:** 82.4
- **current_tags:** baby-gift, baby-shoes, everyday-baby-wear, girls-clothing, kids-clothing, neutral-baby-outfit
- **proposed_native_tags:** `type-shoes`, `season-summer`, `occ-gift`, `occ-everyday`, `gender-girl`, `style-casual`
- **customer_labels_he:** נעליים | קיץ | מתנה | יומיומי | בנות | קז'ואל
- **blocked_tags:** —

**missing / review reason:** תגים קיימים "baby" ו-"kids" נותנים טווח רחב ולא גיל ספציפי. ה-handle מכיל "sandals" אבל type-shoes הוצע. אין גיל.

**למה המערכת הציעה את התגיות:**
- `type-shoes` — תג קיים "baby-shoes"
- `season-summer` — ה-handle מכיל "summer"
- `occ-gift` — תג קיים "baby-gift"
- `occ-everyday` — תג קיים "everyday-baby-wear"
- `gender-girl` — תג קיים "girls-clothing"
- `style-casual` — ה-handle מכיל "casual"

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-shoes` — נכון? (**handle מכיל "sandals" — האם `type-sandals` נכון יותר?**)
- [ ] גיל: חסר — "hello kitty" + "kids" — מה הגיל המשוער? לבדוק בשופיפיי
- [ ] עונה: `season-summer` — נכון?
- [ ] מגדר: `gender-girl` מ-"girls-clothing" — נכון?
- [ ] תווית עברית: חסרת גיל בתפריט — האם בעיה?
- [ ] type-shoes vs type-sandals — מה המדיניות לנעל קיץ עם "sandals" בה-handle?

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 9 — 🔶 NEEDS_REVIEW — NO_AGE_FOUND, מידע מינימלי

- **product_id:** 9179143569721
- **title:** נעל סנדל צעד ראשון מונעת החלקה – גמישה בטוחה ונוחה לתינוק דגם רוני
- **handle:** סנדל-אופנתי-נח-מונע-החלקה-רוני
- **product_group:** shoes_yaml
- **status:** NEEDS_REVIEW
- **quality_score:** 60.9
- **current_tags:** Copy AI
- **proposed_native_tags:** `type-sandals`, `season-unknown`, `occ-first-step`, `gender-unknown`
- **customer_labels_he:** סנדלים | צעד ראשון
- **blocked_tags:** —

**missing / review reason:** handle עברי קצר, תג קיים "Copy AI" בלבד. אין גיל, מגדר, עונה. מקורות מינימליים מהכותרת בלבד. ציון נמוך: 60.9. "צעד ראשון" מרמז לגיל 6-12m אבל המערכת לא כתבה גיל.

**למה המערכת הציעה את התגיות:**
- `type-sandals` — הכותרת מכילה "סנדל"
- `season-unknown` — ברירת מחדל, אין מקור
- `occ-first-step` — הכותרת מכילה "צעד ראשון"
- `gender-unknown` — ברירת מחדל, אין מקור

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-sandals` = סנדלים — נכון?
- [ ] גיל: "צעד ראשון" = בד"כ 6-12m — האם לאשר `age-6-12m` ידנית?
- [ ] עונה: אין עונה — האם לתת `season-summer` לסנדל?
- [ ] מגדר: gender-unknown — לבדוק בשופיפיי — לבנות? לבנים? ניוטרלי?
- [ ] תווית עברית: רק "סנדלים | צעד ראשון" — מספיק?
- [ ] לסמן לצורך העשרת YAML/מקורות

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 10 — 🔶 NEEDS_REVIEW — ⚠️ type-unknown — מדחום, לא ביגוד

- **product_id:** 10099941179705
- **title:** Tempio — מדחום חכם למקלחת בטוחה
- **handle:** led-display-household-water-shower-thermometer-5-85-flow-self-powered-water-thermometer-monitoring-baby-care-energy-smart-meter
- **product_group:** yaml_gap
- **status:** NEEDS_REVIEW
- **quality_score:** 54.7
- **current_tags:** (ריק)
- **proposed_native_tags:** `type-unknown`, `season-unknown`, `occ-everyday`, `gender-unknown`
- **customer_labels_he:** יומיומי
- **blocked_tags:** —

**missing / review reason:** ⚠️ **זה מדחום מים למקלחת — לא בגד, לא נעל, לא בובה.** המערכת נתנה type-unknown בצדק. ציון נמוך: 54.7. **שאלה מרכזית: האם מוצר כזה שייך למערכת Layer 6 Tag System בכלל?**

**למה המערכת הציעה את התגיות:**
- `type-unknown` — המערכת לא זיהתה סוג ביגוד/נעל/בובה — ברירת מחדל
- `season-unknown` — ברירת מחדל
- `occ-everyday` — ברירת מחדל
- `gender-unknown` — ברירת מחדל

**מה אייל צריך לבדוק:**
- [ ] האם מוצר זה שייך ל-Layer 6 Tag System בכלל?
- [ ] אם כן — מה type נכון? (אין קטגוריה "מוצרי תינוק / אביזרים" עדיין)
- [ ] אם לא — לסמן כ-**EXCLUDED** מ-Layer 6
- [ ] האם יש מוצרים דומים בחנות (מוצרי עזר, אלקטרוניקה לתינוק) שצריך טיפול?

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 11 — ✅ PASS (yaml_gap) — ⚠️ אין YAML, מקורות אנגלית בלבד

- **product_id:** 10190523105593
- **title:** Boys' Summer Knitted Set, Contrast Color Short-Sleeved With Pocket and Shorts Clothes Sets
- **handle:** boys-summer-knitted-set-contrast-color-short-sleeved-with-pocket-and-shorts-clothes-sets-children-comfort-soft-2-piece-set
- **product_group:** yaml_gap
- **status:** PASS
- **quality_score:** 96.1
- **current_tags:** (ריק — אין תגים בשופיפיי)
- **proposed_native_tags:** `type-set`, `age-2-3y`, `season-summer`, `fabric-knit`, `occ-everyday`, `gender-boy`, `style-casual`
- **customer_labels_he:** סטים | 2-3 שנים | קיץ | סריג | יומיומי | בנים | קז'ואל
- **blocked_tags:** —

**missing / review reason:** אין YAML, אין תגים קיימים. כל המקורות מ-title/handle/body. גיל age-2-3y מהתיאור — נדרש אימות. מוצר חדש?

**למה המערכת הציעה את התגיות:**
- `type-set` — הכותרת מכילה "2-piece Set"
- `age-2-3y` — מהתיאור (body_html) — נדרש אימות
- `season-summer` — הכותרת מכילה "Summer"
- `fabric-knit` — הכותרת מכילה "Knitted"
- `gender-boy` — הכותרת מכילה "Boys'"
- `style-casual` — התיאור מכיל casual

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-set` — נכון?
- [ ] גיל: `age-2-3y` — **לבדוק בתיאור המוצר בשופיפיי**
- [ ] עונה: `season-summer` — נכון?
- [ ] בד/חומר: `fabric-knit` = סריג — נכון?
- [ ] מגדר: `gender-boy` — נכון?
- [ ] תווית עברית: "סטים | 2-3 שנים | קיץ | בנים" — מתאים לתפריט?
- [ ] למה אין YAML? לבדוק אם מוצר חדש שדורש YAML

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 12 — ✅ PASS (yaml_gap) — ⚠️ type-toy, אין גיל, כותרת חצויה

- **product_id:** 9839252406585
- **title:** 30 CM Cute Teddy Bear Hide and Seek Animated Stuffed Animal Talking Bear Shy Bear Best Birthday Gift for
- **handle:** 30-cm-cute-teddy-bear-hide-and-seek-animated-stuffed-animal-talking-bear-shy-bear-best-birthday-gift-for
- **product_group:** yaml_gap
- **status:** PASS
- **quality_score:** 76.1
- **current_tags:** (ריק)
- **proposed_native_tags:** `type-toy`, `season-unknown`, `fabric-fleece`, `occ-gift`, `gender-unknown`, `style-teddy`
- **customer_labels_he:** צעצועים | פליז | מתנה | דובי
- **blocked_tags:** —

**missing / review reason:** דובי צעצוע. אין גיל, מגדר, עונה. ציון 76.1 בגלל 3 קטגוריות חסרות. **הכותרת בשופיפיי חצויה** ("Birthday Gift for..." — חסר קצה). לבדוק.

**למה המערכת הציעה את התגיות:**
- `type-toy` — התיאור מכיל "toy" / "stuffed animal"
- `season-unknown` — ברירת מחדל
- `fabric-fleece` — התיאור מכיל fleece/plush
- `occ-gift` — הכותרת מכילה "Birthday Gift"
- `gender-unknown` — ברירת מחדל
- `style-teddy` — הכותרת מכילה "Teddy Bear"

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-toy` = צעצועים — נכון?
- [ ] גיל: חסר — מה הגיל המומלץ לדובי 30 ס"מ? (תינוק? ילד?)
- [ ] עונה: season-unknown לצעצוע — בסדר?
- [ ] בד/חומר: `fabric-fleece` = פליז — נכון לדובי?
- [ ] מגדר: gender-unknown — האם `gender-neutral` לדובי?
- [ ] **כותרת חצויה בשופיפיי** — לבדוק ולתקן

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 13 — ✅ PASS (reborn_toys, yaml_gap) — ⚠️⚠️ type-reborn-doll עלול להיות שגוי

- **product_id:** 9587715244345
- **title:** בובה נושמת פיל ועוד חיות מחמד
- **handle:** 4-modes-baby-breathing-soothing-elephant-plush-doll-toy-sleeping-companion-music-and-light-doll-sensory-stuffed-toy-kids-gift
- **product_group:** reborn_toys
- **status:** PASS
- **quality_score:** 79.8
- **current_tags:** (ריק)
- **proposed_native_tags:** `type-reborn-doll`, `season-winter`, `fabric-fleece`, `occ-calming`, `occ-gift`, `gender-unknown`, `style-animal-print`
- **customer_labels_he:** **בובות ריבורן** | חורף | פליז | הרגעה | מתנה | הדפס חיות
- **blocked_tags:** —

**⚠️ אזהרה:** מוצר זה הוא **פיל פלאש מרגיע** — לא בובת ריבורן! המערכת זיהתה "doll" בה-handle ושיבצה type-reborn-doll. הסיווג עלול להיות שגוי לחלוטין. גם season-winter הוסק מ"חומר" בצורה לא ברורה.

**missing / review reason:** type-reborn-doll הוסק מ-"doll" בה-handle. אבל המוצר הוא צעצוע פלאש מרגיע (פיל), לא ריבורן. season-winter מ"הסקת חומר" (fleece = חורף?) — לא ברור.

**למה המערכת הציעה את התגיות:**
- `type-reborn-doll` — ה-handle מכיל "doll" → מסווג כ-reborn_toys → type-reborn-doll
- `season-winter` — ה-handle מכיל חומר שהמערכת פירשה כחורף (fleece)
- `fabric-fleece` — הכותרת "פלאש" = fleece
- `occ-calming` — הסקה לפי סוג reborn_toys → הרגעה
- `occ-gift` — ה-handle מכיל "kids-gift"
- `style-animal-print` — הכותרת מכילה "פיל" = הדפס חיות

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-reborn-doll` = בובות ריבורן — **זה נכון? זה פיל פלאש ולא ריבורן!**
- [ ] אם לא — האם `type-toy` נכון יותר?
- [ ] גיל: DOLL_NO_AGE_APPLICABLE — נכון לצעצוע פלאש?
- [ ] עונה: `season-winter` מהסקת fleece — מתאים לפיל פלאש?
- [ ] **תווית: "בובות ריבורן" לפיל פלאש עלול להטעות לקוח!**
- [ ] לבדוק אם יש מוצרים דומים בחנות עם אותה בעיה

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 14 — ✅ PASS (clothing_yaml) — RANGE_TOO_BROAD, גיל חסום

- **product_id:** 10005779808569
- **title:** אוברול בייבי מניה דגם חן
- **handle:** autumn-baby-clothes-bodysuit-one-pieces-boys-girls-newborn-rompers-solid-color-100-cotton-0-24m-long-sleeve-loungewear-outfit
- **product_group:** clothing_yaml
- **status:** PASS
- **quality_score:** 81.5
- **current_tags:** 18-24M, 3-6M6-9M, 9-18M, אוברול, חורף, לבן, תינוקות 0-3Y
- **proposed_native_tags:** `type-romper`, `season-winter`, `fabric-cotton`, `occ-everyday`, `gender-girl`, `style-modern`
- **customer_labels_he:** אוברולים | חורף | כותנה | יומיומי | בנות | מודרני
- **blocked_tags:** גיל חסום — RANGE_TOO_BROAD (handle מכיל "0-24m")

**missing / review reason:** ה-handle מכיל "0-24m" (טווח 24 חודשים — רחב מדי). **המערכת חסמה את כל תגי הגיל.** תגי גדלים קיימים בשופיפיי: 3-6M, 9-18M, 18-24M — אלה גדלים, לא גילאים. PASS כי CAT-B פטור כאשר RANGE_TOO_BROAD.

**למה המערכת הציעה את התגיות:**
- `type-romper` — תג קיים "אוברול"
- `season-winter` — תג קיים "חורף"
- `fabric-cotton` — הכותרת מכילה "100-cotton"
- `occ-everyday` — ברירת מחדל
- `gender-girl` — ה-handle מכיל "girls"
- `style-modern` — התיאור מכיל סגנון מודרני
- **גיל חסום:** "0-24m" בה-handle → RANGE_TOO_BROAD → אין age tag

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-romper` — נכון?
- [ ] גיל: תגי גדל קיימים = 3-6M, 9-18M, 18-24M — **האם לתת כמה גילאים? או להשאיר בלי גיל?**
- [ ] עונה: `season-winter` מ-"חורף" קיים — נכון?
- [ ] בד/חומר: `fabric-cotton` — נכון?
- [ ] מגדר: `gender-girl` — נכון? (handle מכיל "boys-girls")
- [ ] תווית עברית: ללא גיל — האם המוצר יופיע בפילטר גיל?
- [ ] **החלטה D2:** אוברול 0-24m — לא לתת גיל? לפצל? tag רחב?

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

### מוצר 15 — 🔶 NEEDS_REVIEW — edge case, handle עברי קצר

- **product_id:** 9179152482617
- **title:** בגד גוף אלגנטי - מייקל
- **handle:** בגד-גוף-אלגנטי-מייקל
- **product_group:** edge_cases
- **status:** NEEDS_REVIEW
- **quality_score:** 67.5
- **current_tags:** Copy AI
- **proposed_native_tags:** `type-bodysuit`, `season-unknown`, `occ-everyday`, `gender-unknown`, `style-elegant`
- **customer_labels_he:** בגד גוף | יומיומי | אלגנטי
- **blocked_tags:** —

**missing / review reason:** handle עברי קצר "בגד-גוף-אלגנטי-מייקל". שם "מייקל" לא מספיק למגדר (המערכת לא מסיקה מגדר משמות — מדיניות נכונה). תג קיים "Copy AI" בלבד. חסר גיל, מגדר, עונה. נבחר כ-edge case בגלל handle עברי קצר.

**למה המערכת הציעה את התגיות:**
- `type-bodysuit` — הכותרת מכילה "בגד גוף"
- `season-unknown` — ברירת מחדל
- `occ-everyday` — ברירת מחדל
- `gender-unknown` — "מייקל" הוא שם בנים אבל המערכת לא מסיקה מגדר משמות בלבד (מדיניות נכונה)
- `style-elegant` — הכותרת מכילה "אלגנטי"

**מה אייל צריך לבדוק:**
- [ ] סוג מוצר: `type-bodysuit` = בגד גוף — נכון?
- [ ] גיל: חסר — מה גיל "בגד גוף אלגנטי מייקל"?
- [ ] עונה: season-unknown — נכון?
- [ ] מגדר: "מייקל" = שם בנים — האם לאשר `gender-boy` ידנית?
- [ ] תווית עברית: "בגד גוף | אלגנטי" — מספיק?
- [ ] לסמן לצורך העשרת YAML

**החלטת אייל:** `APPROVE / APPROVE_WITH_NOTE / FAIL`  
**הערת אייל:** _____________

---

## MENU LABEL REVIEW

בדיקת תוויות הניווט — האם כל תווית עברית מתאימה לתפריט ללקוח?

| internal_tag | customer_label_he | האם מתאים לתפריט | הערה |
|---|---|---|---|
| `type-romper` | אוברולים | [ ] | הופיע ב-Phase 4 ✓ |
| `type-dress` | שמלות | [ ] | **לא הופיע ב-Phase 4** — לבדוק בנפרד |
| `type-set` | סטים | [ ] | הופיע ב-Phase 4 ✓ |
| `type-shoes` | נעליים | [ ] | הופיע ב-Phase 4 ✓ |
| `type-sandals` | סנדלים | [ ] | הופיע ב-Phase 4 ✓ |
| `type-reborn-doll` | בובות ריבורן | [ ] | הופיע ✓ — ⚠️ ראה מוצר 13 (פיל פלאש!) |
| `season-summer` | קיץ | [ ] | ⚠️ "קיץ" או "בגדי קיץ"? לאחד |
| `season-winter` | חורף | [ ] | ⚠️ "חורף" או "בגדי חורף"? לאחד |
| `age-0-3m` | 0-3 חודשים | [ ] | **לא הופיע ב-Phase 4** — לבדוק בנפרד |
| `age-6-12m` | 6-12 חודשים | [ ] | הופיע ב-Phase 4 ✓ |
| `gender-boy` | בנים | [ ] | הופיע ב-Phase 4 ✓ |
| `gender-girl` | בנות | [ ] | הופיע ב-Phase 4 ✓ |
| `gender-neutral` | ניוטרלי | [ ] | ⚠️ "ניוטרלי" או "יוניסקס"? לאחד |
| `occ-gift` | מתנה | [ ] | הופיע ב-Phase 4 ✓ |
| `occ-first-step` | צעד ראשון | [ ] | הופיע ב-Phase 4 ✓ |
| `fabric-cotton` | כותנה | [ ] | הופיע ב-Phase 4 ✓ |

**שאלות פתוחות לתוויות:**
1. `season-summer` → "קיץ" או "בגדי קיץ"?
2. `season-winter` → "חורף" או "בגדי חורף"?
3. `gender-neutral` → "ניוטרלי" או "יוניסקס" או "יוניסקס / ניוטרלי"?
4. `occ-gift` → "מתנה" או "מתנות"?

---

## OPEN DECISIONS FOR AYAL

---

### D1 — NO_AGE_FOUND strategy

**הבעיה:** 31 מוצרים (52%) חסרים גיל — בעיקר נעליים + yaml_gap.

**אפשרויות:**
- **A.** לא להציג מוצרים כאלה בפילטר גיל עד שיש גיל מאומת
- **B.** להשתמש ב-`age-unknown` פנימי בלבד — לא יוצג לתפריט
- **C.** לפתוח משימת YAML enrichment בעתיד (מילוי ידני)

**המלצה:** B עכשיו, C בעתיד.

**החלטת אייל:** ___________

---

### D2 — RANGE_TOO_BROAD strategy

**הבעיה:** 4 מוצרים עם טווח גיל 0-24m ומעלה — גיל חסום.

**אפשרויות:**
- **A.** לא לתת תגית גיל (כפי שנעשה כעת)
- **B.** להוסיף tag רחב חדש בעתיד כמו `age-0-18m`
- **C.** לפצל לכמה תגיות גיל רק אם המקור מפורש

**המלצה:** A עכשיו, B רק אם אייל רוצה פילטרים רחבים.

**החלטת אייל:** ___________

---

### D3 — Reborn / dolls age

**הבעיה:** 9 מוצרי reborn/toys עם DOLL_NO_AGE_APPLICABLE — בובות ריבורן ללא גיל.

**אפשרויות:**
- **A.** בלי age tag (כפי שנעשה כעת)
- **B.** tag מיוחד כמו `age-not-applicable`
- **C.** להשתמש בגיל מומלץ רק אם כתוב במוצר במפורש

**המלצה:** A עכשיו, C בעתיד אם יש מקור.

**החלטת אייל:** ___________

---

### D4 — Phase 6 readiness

**השאלה:** האם לאחר review של 15 מוצרים ניתן להכין live batch קטן?

**אפשרויות:**
- **A.** כן, אם 12/15 מאושרים — להכין batch קטן (10-15 מוצרי PASS)
- **B.** לא, קודם לתקן taxonomy/source (לדוגמה: type-reborn-doll לפיל פלאש)
- **C.** לא, קודם להעשיר YAML לפחות ל-50% מה-NEEDS_REVIEW

**המלצה:** תלוי בתוצאות review זה.

**החלטת אייל:** ___________

---

## REVIEW VERDICT TEMPLATE

**מלא לאחר סיום הבדיקה:**

```
Ayal Review Result:
- reviewed_count: ___ / 15
- approved: ___
- approved_with_note: ___
- failed: ___
- major_pattern_found: YES / NO
  (אם YES — תאר את הדפוס:)
- can_proceed_to_phase6_small_live_batch: YES / NO
- notes:
```

---

*Phase 6 NOT OPEN — לא לבצע שום שינוי בשופיפיי לפני VERDICT.*
