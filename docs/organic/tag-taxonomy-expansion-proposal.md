# Tag Taxonomy Expansion Proposal — BabyMania Premium Baby Store

**תאריך:** 2026-05-10  
**מצב:** READ-ONLY PLANNING — אין כתיבות Shopify  
**גרסה:** 1.0  
**מבוסס על:** Layer 6 Closure (2026-05-08), Phase 7C Long-Run Plan, shoes journal

---

## עקרונות יסוד

כל תג חייב לעמוד בלפחות אחד מהתנאים הבאים:

1. **UX:** עוזר לקונה לסנן ולמצוא מוצרים
2. **SEO / Smart Collection:** מאפשר Smart Collection שתכנס לניווט
3. **Internal tool:** שימושי לאוטומציה ולדיווח פנימי

**כלל מינימום:** לפחות 8–10 מוצרים לפני פתיחת Smart Collection. פחות מ-8 → tag פנימי בלבד, ללא collection.

---

## A. תגי ביגוד (Clothing Type Tags)

### תגים קיימים ופעילים (Smart Collections live)

| תג | כינוי עברי | מוצרים live | Smart Collection |
|---|---|---|---|
| `type-set` | סטים | 18+ | כן ✅ |
| `type-romper` | סרבלים | 16+ | כן ✅ |
| `type-dress` | שמלות | 9+ | לא (מתחת לסף) |
| `type-bodysuit` | בגדי גוף | 8+ | לא (על הגבול) |

### תגים מוצעים להרחבה

| תג | כינוי עברי | הגדרה | סף מינימום לcollection |
|---|---|---|---|
| `type-coat` | מעילים | מעיל, ז'קט, בלייזר לתינוק — כיסוי חיצוני | 8 מוצרים |
| `type-hat` | כובעים | כובע לתינוק (ביגוד ראש בלבד — לא צעצוע) | 8 מוצרים |

**הערות:**
- `type-coat` ו-`type-hat` כבר עודכנו ב-Phase 7C Batch 2 (Phase 7C Batch 2: hat:4, coat:3 = 7 בסה"כ). נדרש 1 נוסף לכל אחד להגיע לסף.
- `type-dress` ו-`type-bodysuit` כבר מתויגים — לא נוצרו Smart Collections כי ב-Phase 8C הן היו מחוץ לסקופ T3. להעריך מחדש ב-Phase 9.
- **לא ליצור** תגי `type-*` נוספים ללא בדיקת product count מוכחת.
- **לא ליצור:** type-onesie (כפל עם type-romper/type-bodysuit), type-pajamas (מעט מוצרים), type-swimwear (חסום — false positive rate גבוה).

---

## B. תגי מגדר (Gender Tags)

### תגים קיימים ופעילים

| תג | כינוי עברי | מוצרים live | Smart Collection |
|---|---|---|---|
| `gender-girl` | לבנות | 20+ | כן ✅ |
| `gender-boy` | לבנים | 19+ | כן ✅ |

### מתי להשתמש בכל תג

**gender-girl:**
- ורוד, סגול, פרחים, פרפרים, דמויות בנות
- שמלות (כמעט תמיד בנות)
- כינויים: "לבנות", "girls"

**gender-boy:**
- כחול, ירוק, דינוזאורים, מכוניות, דמויות בנים
- כינויים: "לבנים", "boys"

**gender-neutral:**
- צהוב, לבן, אפור, כמה גוונים
- כינויים: "יוניסקס", "unisex", "לכל המינים"
- **שימוש:** רק כשיש הצהרה מפורשת על כך בכותרת/תיאור — לא כ-default

**ללא תג מגדר (מומלץ):**
- כשהמוצר אמביוולנטי לחלוטין ולא יוניסקס מוצהר
- כשהכותרת לא מספקת כל רמז — לא לנחש, לא לתייג

**כלל:** אסור לתייג `gender-neutral` כ"ברירת מחדל" לכל מה שאינו בנות/בנים. ללא ראיה — ללא תג.

---

## C. תגי אירוע (Occasion Tags)

### תגים קיימים ופעילים

| תג | כינוי עברי | מוצרים live | Smart Collection |
|---|---|---|---|
| `occ-gift` | מתנות | 14+ | כן ✅ |

### תגים מוצעים

| תג | כינוי עברי | הגדרה | ביסוס מסחרי | סף |
|---|---|---|---|---|
| `occ-brit` | לברית / אקווינה | מוצרים מתאימים לברית מילה או טקס אקווינה | בינוני — שוק ישראלי ייחודי | 8+ |
| `occ-event` | לאירוע | לשבת, יום הולדת, גן — לא ברית ולא יומיומי | בינוני | 8+ |
| `occ-everyday` | יומיומי | פשוט, נוח, יומיומי — לא אירוע | SEO פחות חזק | 10+ |

**עדיפות:**
1. `occ-brit` — ביקוש ישראלי ייחודי, ריכוז מוצרים ספציפי
2. `occ-event` — עונתי, שימושי לניווט
3. `occ-everyday` — internal tagging בעיקר, לא collection בטווח הקרוב

**לא ליצור:**
- `occ-party` (חפיפה עם occ-event)
- `occ-holiday` (מעט מוצרים, חפיפה עם occ-gift)

---

## D. תגי נעליים (Shoe Tags) — Phase B

### תגים מוצעים לנעליים

| תג | כינוי עברי | הגדרה קצרה |
|---|---|---|
| `shoes-sneakers` | סניקרס | נעל ספורט/קז'ואל עם סוליה קשה |
| `shoes-sandals` | סנדלים | נעל פתוחה לקיץ |
| `shoes-boots` | מגפיים | מגף לרגל או לקרסול |
| `shoes-first-step` | צעד ראשון | עיצוב לתינוק שרק מתחיל ללכת |
| `shoes-elegant` | אלגנטי | נעל שמחה, אירוע, ברית |
| `shoes-soft-sole` | סוליה רכה | סוליה רכה — מתאים לזחילה/צעדים ראשונים |
| `shoes-review-only` | ממתין לבדיקה | לא ניתן לסווג ללא ראיית תמונה |

**Multi-tag מותר ומומלץ:**
- `shoes-sneakers` + `shoes-soft-sole` (סניקרס לתינוק עם סוליה רכה)
- `shoes-sandals` + `shoes-first-step` (סנדל לצעד ראשון)
- `shoes-boots` + `shoes-elegant` (מגפון שמחה)

**לא ליצור:**
- `shoes-doll` — אין עדות למוצרי נעל בובה כקטגוריה נפרדת
- `shoes-size-*`, `shoes-eu-*`, `shoes-22`, וכו' — NEVER tag by size

**חסמים נוכחיים:**
- כל ~65 מוצרי נעליים חסומים עד אישור אייל על EU size mapping
- לאחר אישור — taxonomy זו תשמש כבסיס לסיווג

---

## E. קטגוריות עתידיות — לא לתייג כעת

| קטגוריה | תגים עתידיים | מינימום מוצרים לפני פתיחה | הערות |
|---|---|---|---|
| אמבטיה | `cat-bath` | 15+ | אמבטיות, מגבות, פריטי רחצה |
| האכלה | `cat-feeding` | 15+ | בקבוקים, צלחות, כפות |
| צעצועים | `cat-toys` | 15+ | כדאי ל-False Positive blocking קודם |
| טקסטיל | `cat-textile` | 12+ | שמיכות, כריות, מצעים |
| אחרי לידה | `cat-postpartum` | 8+ | מוצרי אמא — שוק קיים |
| סיר | `cat-potty` | 8+ | גיל 12m+ בלבד |

**כלל:** אין לתייג קטגוריות אלו עד שיש 8+ מוצרים מאומתים ואישור ניהולי.

---

## F. כללי תיוג כלליים

### Multi-tag

מוצר יכול לקבל תגים ממספר דימנסיות:
```
type-set + gender-girl + occ-gift
shoes-sneakers + shoes-soft-sole + gender-boy
```

### כלל Smart Collection

| מצב | פעולה |
|---|---|
| תג עם 8+ מוצרים | מתאים לSmart Collection |
| תג עם 5–7 מוצרים | Internal use only, no collection |
| תג עם פחות מ-5 | לא ליצור |

### כלל QA

כל כתיבת תג live (T3) דורשת evidence table מלאה עם 11 בדיקות לכל מוצר.
אין "PASS" כללי — ראה `docs/organic/layer7-live-tagging-qa-contract.md`.

### כלל EU Size

NEVER TAG by EU size, age range numeric mapping, or physical measurements.  
חסימה: EU-22, EU-23, size-18m, age-3m — אסורים לחלוטין כתגים.

---

*מסמך זה הוא הצעה בלבד. אין כתיבות Shopify ללא אישור T3 מאייל.*
