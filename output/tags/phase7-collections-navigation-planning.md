# Layer 6/7 — Collections & Navigation Planning
**תאריך:** 2026-05-04
**Phase:** Post-Phase 6 Planning — תכנון בלבד
**READ-ONLY PLANNING — אין כתיבה ל-Shopify**

---

## 1. מצב מערכת נוכחי

| פרמטר | ערך |
|-------|-----|
| Phase 6 batch 1+2 | COMPLETE — PASS |
| Shopify live | YES — **5 products** (C3, C2, C4, C5, C1) |
| Phase 7 (full rollout) | NOT STARTED |
| Phase 8 (collections) | NOT OPEN |
| Phase 9 (navigation) | NOT OPEN |
| Phase 10 (Mega Menu) | NOT OPEN |
| age-* tags | 0 |
| collections קיימות | 0 |
| Mega Menu בנוי | NO |
| T3 approval לPhase 7 | PENDING |

**כלל הspec (section 8):** Collections הן downstream phase — לא לפני Phase 6/7.
**כלל הspec (section 2.2):** Mega Menu = Phase 10 בלבד.

---

## 2. רשימת 5 המוצרים החיים והתגיות שלהם

| candidate | product_id | כותרת | תגיות Layer 6 |
|-----------|-----------|-------|--------------|
| C3 | 9688660312377 | אוברול ג׳ינס דגם אתי | type-romper, size-3-6m/6-9m/9-12m/12-18m, season-spring-fall, fabric-denim, gender-girl |
| C2 | 9874906349881 | אוברול ג'ינס מתוק דגם זוהר | type-romper, size-3-6m/6-9m/9-12m, season-summer, fabric-denim, gender-neutral, style-casual |
| C4 | 9895864205625 | אוברול ג'ינס יוניסקס דגם שלו | type-romper, size-0-3m/3-6m/9-12m/12-18m, fabric-denim, gender-neutral, style-casual |
| C5 | 9687579033913 | אוברול לבבות דגם הילה | type-romper, size-0-3m/3-6m/6-9m/9-12m/12-18m, season-winter, fabric-cotton, gender-girl |
| C1 | 9688932909369 | אוברול אריה חמוד דגם שמר | type-romper, size-0-3m/3-6m/6-9m/9-12m, gender-boy, style-casual |

**תצפית קריטית:** כל 5 המוצרים הם **type-romper**. אין גיוון סוגי מוצר כרגע.

---

## 3. אילו collections אפשר לבנות מהתגיות שכבר קיימות

**ספירת מוצרים לכל תגית:**

| תגית | מוצרים | candidates |
|------|--------|-----------|
| type-romper | **5** | C1, C2, C3, C4, C5 |
| size-3-6m | **5** | C1, C2, C3, C4, C5 |
| size-9-12m | **5** | C1, C2, C3, C4, C5 |
| size-6-9m | **4** | C1, C2, C3, C5 |
| size-0-3m | **3** | C1, C4, C5 |
| size-12-18m | **3** | C3, C4, C5 |
| fabric-denim | **3** | C2, C3, C4 |
| gender-neutral | **2** | C2, C4 |
| style-casual | **3** | C1, C2, C4 |
| gender-girl | **2** | C3, C5 |
| season-spring-fall | **1** | C3 |
| season-summer | **1** | C2 |
| season-winter | **1** | C5 |
| gender-boy | **1** | C1 |
| fabric-cotton | **1** | C5 |

**Collections טכנית אפשריות (≥3 מוצרים):**

| collection | תגית trigger | מוצרים | כדאי? |
|-----------|-------------|--------|-------|
| כל האוברולים | type-romper | 5 | ⚠️ נמוך — 5 מוצרים, מגוון דל |
| מידה 3-6 חודשים | size-3-6m | 5 | ⚠️ נמוך — כולם אוברולים |
| מידה 9-12 חודשים | size-9-12m | 5 | ⚠️ נמוך — כולם אוברולים |
| ג'ינס | fabric-denim | 3 | ⚠️ נמוך — 3 מוצרים |
| קז'ואל | style-casual | 3 | ⚠️ נמוך — 3 מוצרים |

---

## 4. אילו collections אסור לבנות עדיין

| collection | תגית | מוצרים | סיבה |
|-----------|------|--------|------|
| קיץ | season-summer | 1 | collection עם מוצר אחד = חסרת ערך |
| חורף | season-winter | 1 | collection עם מוצר אחד = חסרת ערך |
| אביב/סתיו | season-spring-fall | 1 | collection עם מוצר אחד = חסרת ערך |
| בנות | gender-girl | 2 | דק מדי — 2 מוצרים, אין גיוון סוגים |
| בנים | gender-boy | 1 | collection עם מוצר אחד = חסרת ערך |
| ניוטרלי | gender-neutral | 2 | דק מדי |
| כותנה | fabric-cotton | 1 | מוצר אחד בלבד |
| שמלות | type-dress | 0 | אין מוצרים מתויגים בסוג זה |
| נעליים | type-shoes/sandals/sneakers | 0 | אין מוצרים מתויגים |
| סטים | type-set | 0 | אין מוצרים מתויגים |

**כלל מינימום מומלץ לcollection בת-ערך:** לפחות 10 מוצרים עם גיוון סוגים.

---

## 5. ניווט לקוח גיוני

### א. לפי סוג מוצר (CAT-A)

**מצב נוכחי:** type-romper בלבד (5/5 מוצרים).

| סוג | tagged כרגע | נדרש לניווט |
|-----|------------|------------|
| אוברולים (romper) | 5 | ✅ — אבל קטן |
| שמלות (dress) | 0 | ❌ — אין תגיות |
| סטים (set) | 0 | ❌ — אין תגיות |
| נעליים (shoes/sandals/sneakers) | 0 | ❌ — אין תגיות |
| מכנסיים (pants) | 0 | ❌ — אין תגיות |
| כובעים (hat) | 0 | ❌ — אין תגיות |

**מסקנה:** ניווט לפי סוג מוצר = לא ניתן כרגע. תפריט עם item אחד ("אוברולים") = חסר ערך.

### ב. לפי מידה (CAT-B)

| מידה | tagged | status |
|------|--------|--------|
| 0-3 חודשים | 3 products | ⚠️ קטן |
| 3-6 חודשים | 5 products | ✅ ראוי — אבל אחיד מדי |
| 6-9 חודשים | 4 products | ⚠️ קטן |
| 9-12 חודשים | 5 products | ✅ ראוי — אבל אחיד מדי |
| 12-18 חודשים | 3 products | ⚠️ קטן |

**מסקנה:** Filter לפי מידה אפשרי טכנית (3-6m, 9-12m), אך כל תוצאה = רק אוברולים — UX דל.

### ג. לפי עונה (CAT-C)

| עונה | tagged |
|------|--------|
| קיץ | 1 product |
| חורף | 1 product |
| אביב/סתיו | 1 product |

**מסקנה:** בלתי-ניתן לניווט. 1 מוצר per עונה = collection חסרת משמעות.

### ד. לפי בד (CAT-D)

| בד | tagged |
|----|--------|
| ג'ינס (denim) | 3 products |
| כותנה (cotton) | 1 product |

**מסקנה:** רק filter — לא תפריט ראשי. 3 מוצרי ג'ינס = borderline.

### ה. לפי מגדר (CAT-F)

| מגדר | tagged |
|------|--------|
| בנות | 2 products |
| בנים | 1 product |
| ניוטרלי | 2 products |

**מסקנה:** בלתי-ניתן לניווט בשלב זה. 1-2 מוצרים per מגדר = לא מספיק.

---

## 6. סיכון אם נבנה collections מוקדם מדי

| סיכון | תיאור |
|-------|-------|
| **UX דל** | collection עם 1-5 מוצרים = לקוח מגיע לדף ריק כמעט |
| **Shopify SEO penalty** | Google מאינדקס collections דקות — עלול להזיק לדירוג |
| **Maintenance overhead** | collections ריקות שנבנו מוקדם מדי = תחזוקה ידנית |
| **Navigation confusion** | תפריט עם item אחד = UX בלבול |
| **False completion** | מראית-עין שהמערכת מוכנה בעוד שHתשתית שברירית |
| **Smart Collection mis-fire** | אם taxonomy ישתנה — Smart Collections יתפרקו |

**ציטוט מהspec (section 8):**
> "Collections are a Layer 6 downstream phase — not the first phase. אסור לפתוח Smart Collections לפני שהתגיות הוכחו ב-Phase 6/7."

Phase 7 = **full rollout** לkol inventory. אנחנו בPhase 6 (5 מוצרים מתוך 393).

---

## 7. המלצה: להרחיב תגיות לפני collections

**המלצה: EXPAND TAGS FIRST — קודם Phase 7, אחר-כך Phase 8.**

**למה:**
1. כל 5 המוצרים הם type-romper — אין גיוון. collections לא מועילות ללא גיוון.
2. ניווט לקוח דורש לפחות 3-4 סוגי מוצר שונים עם עשרות מוצרים כל אחד.
3. הspec מגדיר Phase 7 (rollout) לפני Phase 8 (collections) — זו ארכיטקטורה מכוונת.

**target לפני פתיחת collections:**
- לפחות 50 מוצרים מתויגים
- לפחות 4 סוגי מוצר שונים (romper + dress + set + shoes)
- לפחות 5 מוצרים per collection target
- כל 4 עונות מיוצגות בלפחות 3 מוצרים כל אחת

**האם אפשר לבנות collections קטנות ראשונות?**

כן — טכנית אפשרי. אך המלצתנו: **לא עדיין**.
סיכון ה-UX גבוה מהתועלת. 5 מוצרים זהים (כולם אוברולים) = collection אחת שאין בה ערך לקוח.

**יוצא מן הכלל:** אם אייל מבקש collection טכנית internal-only (לא ב-navigation) לצורך בדיקה — זה אפשרי בPhase 8 pilot mode.

---

## 8. השלב הבא הכי מהיר ובטוח

**Phase 7 Small Batches — הרחבת תיוג:**

| צעד | תיאור | אישור |
|-----|-------|-------|
| 1 | T3 approval לPhase 7 batch 1 (20-50 מוצרים) | אייל |
| 2 | dry-run על המוצרים הבאים — עדיפות לגיוון: dress, set, shoes | אוטומטי |
| 3 | גיבוי → כתיבה → verify — לפי אותה שיטת batch | מערכת |
| 4 | אחרי 50+ מוצרים מתויגים עם גיוון — evaluate Phase 8 | אייל |

**עדיפות לbatch הבא (לפי גיוון נדרש):**

| סוג מוצר | מוצרים זמינים בsample | עדיפות |
|---------|---------------------|-------|
| type-romper נוסף | רב | נמוכה — יש כבר 5 |
| type-dress | ישנם | גבוהה |
| type-set | ישנם | גבוהה |
| type-sneakers / type-shoes | C6, C8 (EU sizes — ממתין פתרון) | בינונית |
| type-bodysuit | ישנם | גבוהה |

---

## 9. Verdict

**NEED_MORE_TAGGED_PRODUCTS_FIRST**

| בדיקה | תוצאה |
|-------|-------|
| מוצרים מתויגים | 5/393 (1.3% מהinventory) |
| גיוון סוגי מוצר | type-romper בלבד (0 גיוון) |
| collection מינימלית קיימת | type-romper (5), size-3-6m (5), size-9-12m (5) |
| ניווט לקוח אפשרי | לא — תפריט עם item אחד |
| Phase 7 started | לא |
| spec מאפשר Phase 8 עכשיו | לא — Phase 7 נדרש קודם |

**מה נדרש לפני Phase 8:**
1. T3 approval לPhase 7
2. 50+ מוצרים מתויגים עם גיוון של לפחות 4 סוגים
3. לפחות 2 עונות עם 5+ מוצרים כל אחת
4. Phase 7 dry-run + verify PASS

---

## 10. אישורים

| בדיקה | תוצאה |
|-------|-------|
| נכתב ל-Shopify | **NO** |
| נוצרו collections | **NO** |
| נוצר Mega Menu | **NO** |
| נוסף batch נוסף | **NO** |
| נוספו תגיות חדשות | **NO** |

---

*Phase 7/8/9 planning only. אין שינויים ב-Shopify. כל ביצוע מותנה ב-T3 approval.*
