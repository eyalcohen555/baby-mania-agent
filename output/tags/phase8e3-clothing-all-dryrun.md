# Phase 8E-3 — clothing-all Smart Collection Dry Run

**Date:** 2026-05-05 16:23:01  
**Shop:** a2756c-c0.myshopify.com  
**Type:** DRY RUN — no writes, no collection created  
**Token suffix:** `37a8`  

---

## 1. מצב מערכת

| Item | Status |
|------|--------|
| Phase 8C — 5 Smart Collections LIVE | ✅ |
| Phase 8E Navigation Dry Run | ✅ PASS |
| Phase 8F navigation write | ✅ לא בוצע — pending T3 |
| 51 מוצרים מתויגים Layer 7B | ✅ |
| GraphQL read | ✅ עובד |
| כתיבה ל-Shopify | ✅ NONE — dry run בלבד |

---

## 2. האם clothing-all כבר קיימת

| Item | Result |
|------|--------|
| clothing-all קיימת | ✅ לא — ניתן לצור |

---

## 3. Rule המדויק (מוצע)

```
title:       כל בגדי התינוקות
handle:      clothing-all
sort_order:  best-selling
published:   true
disjunctive: true  (ANY — OR between rules)

rules:
  - tag equals type-set
  - tag equals type-romper
  - tag equals type-dress
  - tag equals type-bodysuit

seo_title:       בגדי תינוקות | Baby Mania
seo_description: בגדי תינוקות איכותיים מבד אורגני — סטים, סרבלים, שמלות ובגדי גוף לתינוקות מ-0 עד 3 שנים. משלוח מהיר בישראל.
```

---

## 4. ספירה כוללת

| Item | Value |
|------|-------|
| מועמדים שנמצאו | **51** |
| טווח מצופה | 45–58 |
| בתוך הטווח | ✅ כן |
| מוצרים עם flags | 0 |

---

## 5. פילוח לפי type

| Type Tag | ספירה |
|----------|-------|
|  `type-set` | 18 |
|  `type-romper` | 16 |
|  `type-dress` | 9 |
|  `type-bodysuit` | 8 |

---

## 6. פילוח לפי gender

| Gender | ספירה |
|--------|-------|
| `gender-boy` | 19 |
| `gender-girl` | 20 |
| `gender-neutral` | 4 |
| `no-gender` | 8 |

---

## 7. טבלת מועמדים

| product_id | title | type | gender |
|------------|-------|------|--------|
| 10190522941753 | 2Pcs Baby Boys' Sports and Leisure Set lapel Color | `type-set` | `gender-boy` |
| 10029649002809 | Alure™ Baby | `type-romper` | `gender-girl` |
| 10190523203897 | Boys Khaki Letter Print Half Zip Hooded 2Pcs Summe | `type-set` | `gender-boy` |
| 10190523105593 | Boys' Summer Knitted Set, Contrast Color Short-Sle | `type-set` | `gender-boy` |
| 10190523138361 | Boys' summer white striped short-sleeved shorts wi | `type-set` | `gender-boy` |
| 10190523302201 | Children’s Summer New Arrival Boys’ Regular Stripe | `type-set` | `gender-boy` |
| 10190523236665 | Infant Baby Boys Short Sets Patchwork Sleeveless V | `type-set` | `gender-boy` |
| 10190522843449 | Kids Baby Boy Summer Clothes Sets Casual Letters S | `type-set` | `gender-boy` |
| 10029649133881 | Lino™ – סט סריג רך לתינוקות בעיצוב אירופאי | `type-set` | `gender-boy` |
| 10029648970041 | LumiBear™ חליפת פרמיום לחורף | `type-romper` | `gender-boy` |
| 10029649101113 | LUMI™  – אוברול נוחות יוקרתי לתינוקות | `type-romper` | `—` |
| 10190522908985 | Summer Toddler Kids Stripe Bodysuit Boys Loose Tur | `type-bodysuit` | `gender-girl` |
| 9657091293497 | WarmNest™– אוברול חורף מחבק לתינוקות | `type-romper` | `gender-girl` |
| 9687596728633 | אוברול Leopard Cozy | `type-romper` | `gender-girl` |
| 9688932909369 | אוברול אריה חמוד דגם שמר | `type-romper` | `gender-boy` |
| 9874906349881 | אוברול ג'ינס מתוק מבית בייבי מניה דגם זוהר | `type-romper` | `gender-neutral` |
| 9688660312377 | אוברול ג׳ינס דגם אתי | `type-romper` | `gender-girl` |
| 9895864205625 | אוברול ג’ינס יוניסקס לתינוקות דגם שלו | `type-romper` | `gender-neutral` |
| 9687579033913 | אוברול לבבות דגם הילה | `type-romper` | `gender-girl` |
| 9688885985593 | אוברול פיל מתוק דגם נאיה | `type-romper` | `gender-girl` |
| 9688934973753 | אוברול פיל פסים דגם ליאו | `type-romper` | `—` |
| 9179165753657 | בגד גוף כותנה טטרה - פריחת האביב | `type-bodysuit` | `—` |
| 9179154612537 | בגד גוף כיווצים - גאיה | `type-bodysuit` | `—` |
| 9179152154937 | בגד גוף מלמלות - קיטי | `type-bodysuit` | `—` |
| 9179167129913 | בגד גוף מלמלות וכיווצים פרחוני - שיילי | `type-bodysuit` | `—` |
| 9874906382649 | בגד גוף פו הדוב דגם לירון | `type-bodysuit` | `gender-girl` |
| 9096607498553 | בגד גוף פליז | `type-bodysuit` | `gender-neutral` |
| 9179166671161 | בגד גוף שמלה ג׳ינס מכותנה - הרפר | `type-bodysuit` | `—` |
| 9688976326969 | חליפה דוב מופתע דגם ליאל | `type-set` | `gender-boy` |
| 9688964989241 | חליפה דוב מקסימה דגם אריאל | `type-set` | `gender-boy` |
| 9688674566457 | חליפה לבנים דגם אימרי | `type-set` | `gender-boy` |
| 9688976294201 | חליפה מהממת רקמת דובי חמוד דגם אלי | `type-set` | `gender-boy` |
| 9687653122361 | חליפה מנומר עם פפיון דגם נמרה | `type-set` | `gender-girl` |
| 9874906546489 | חליפת דובי  מלאה בסטייל דגם מאור | `type-set` | `gender-boy` |
| 9688964956473 | חליפת דובים דגם אוריאל | `type-set` | `gender-boy` |
| 9858268496185 | חליפת חג פרחונית דגם סמדר | `type-romper` | `gender-girl` |
| 9606694437177 | חליפת פולו קצרה סרוגה לתינוקות | `type-set` | `gender-neutral` |
| 9678573273401 | חליפת פיל דגם אימרי | `type-romper` | `gender-boy` |
| 9688674533689 | חליפת קואלה דגם ליאל | `type-set` | `gender-boy` |
| 9688660377913 | חליפת קואלה דגם שני | `type-set` | `gender-girl` |
| 9731768746297 | סט בגדי תינוקות גינס ושמלה דגם טליה | `type-dress` | `gender-girl` |
| 9687653089593 | סט מכנס וחולצה פרפר פיל דגם נויה | `type-romper` | `gender-girl` |
| 9678598734137 | סרבל גנטלמן בייבי 3 חלקים דגם אליה | `type-romper` | `gender-boy` |
| 9606691324217 | שמלה אופנתית קלאסית לאירועים לתינוקת | `type-dress` | `gender-girl` |
| 9895864369465 | שמלה חגיגית פרחונית דגם מורן | `type-dress` | `gender-girl` |
| 9892557848889 | שמלה כחולה כהה אם דוגמא קלאסית דגם אוראל | `type-dress` | `gender-girl` |
| 9179146256697 | שמלה נסיכותית מפתשן וכותנה, מלאה בסטייל - נועה | `type-dress` | `—` |
| 9606694175033 | שמלה קיצית עם מלמלה לבנות | `type-dress` | `gender-girl` |
| 9688976261433 | שמלת פפיון חורפית דגם ארגמן | `type-dress` | `gender-girl` |
| 9892196450617 | שמלת פרחים מהאגדות דגם איילה | `type-dress` | `gender-girl` |
| 9895864271161 | שמלת תינוקות פרחונית דגם עדן | `type-dress` | `gender-girl` |

---

## 8. חריגות

✅ לא נמצאו חריגות.

---

## 9. SEO Description מוצעת

```
seo_title: בגדי תינוקות | Baby Mania
seo_description: בגדי תינוקות איכותיים מבד אורגני — סטים, סרבלים, שמלות ובגדי גוף לתינוקות מ-0 עד 3 שנים. משלוח מהיר בישראל.
length: 107 תווים (מקסימום 160)
```

---

## 10. אישור — לא נכתב ל-Shopify

**NONE.** כל הפעולות היו GET בלבד. אין collection שנוצרה. אין tag שהוספה. אין mutation.

---

## 11. Verdict

**READY_FOR_PHASE8E4_CLOTHING_ALL_T3_APPROVAL**

✅ 51 מוצרים אושרו לתוך clothing-all.
Dry run עבר. הצעד הבא: T3 approval מאייל → Phase 8E-4 → יצירת collection live.
לאחר מכן: Phase 8F — עדכון navigation (הוספת 'כל הבגדים' כ-6th sub-item).

---

*Report generated by scripts/phase8e3_clothing_all_dryrun.py*