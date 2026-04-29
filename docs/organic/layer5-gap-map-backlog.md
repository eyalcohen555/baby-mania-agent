# Layer 5 — Gap Map Backlog
## BabyMania Organic Content Pipeline
### Version: 1.4 | Created: 2026-04-29 | Updated: 2026-04-29 | Status: ACTIVE | Gap Map Planning: CLOSED ✅

---

## 1. Layer 5 פרינציפים

**Layer 5 = Gap-Based Organic Growth — לא "כתוב מאמרים".**

Layer 5 אינה שכבת ייצור אוטומטי. היא שכבת ניהול פערים מבוססת-עדויות.

### כלל הביצוע:
```
Gap Map → Backlog → בחירת פריט → HUB Selection → כתיבה → QA → פרסום → Post-HUB Audit → חזרה
```

### הגדרות:
- **Gap Map** = רשימה מלאה של כל אזורי התמיכה החסרים — מוצרים ללא מאמרים, נושאים ללא HUB, קישורים חסרים.
- **Backlog** = תור עבודה ממוין לפי עדיפות. כל פריט בבאקלוג הוא מועמד לביצוע.
- **HUB** = ביצוע אחד נבחר מהבאקלוג. כולל Pillar + Cluster articles.
- **Post-HUB Audit** = בדיקת סגירה חובה לאחר כל HUB. HUB לא "סגור לחלוטין" עד שהאוקיט עבר.

---

## 2. Gap Map — מפת פערים מלאה

### 2.1 קטגוריות מכוסות (HUBs פורסמו)

| קטגוריה | HUB | מאמרים | GSC |
|----------|-----|---------|-----|
| Baby Sleep | HUB-1 | 5 | ✅ |
| Newborn Clothing | HUB-2 | 6 | ✅ |
| Baby Bath | HUB-3 | 5 | ✅ |
| Sensitive Skin | HUB-4 | 5 | ✅ |
| Baby Gifts | HUB-5 | 7 | ✅ |
| Baby Shoes | HUB-6 | 7 | ✅ |
| Baby Safety | HUB-7 | 6 | ✅ |
| Baby Daily Routine | HUB-8 | 6 | ✅ |
| Reborn Dolls | HUB-9 | 7 | ✅ |
| Reborn Benefits | HUB-10 | 7 | ✅ |
| Baby Summer Clothing | HUB-11 | 7 | ⏳ C2-C6 pending |

**סה"כ: 11 HUBs, 68 מאמרים live (נכון ל-2026-04-29)**

### 2.2 פערים מזוהים — Gap Map

| גאפ | קטגוריה | סוג גאפ | ממצא |
|-----|---------|---------|-------|
| G-01 | בגדי שמחה / שמלות חגיגיות | Content gap | מוצרים high-value ללא HUB תומך |
| G-02 | Reborn YAML context files | System gap | 6 מוצרים ב-HUB-9/10 ללא קובץ YAML |
| G-03 | נעליים — כפכפים / סנדלים / נעלי קיץ | Content gap | HUB-6 חזק אך subtypes לא מכוסים |
| G-04 | אביזרי תינוק — כובעים / מצופים / עונתי | Content gap | חלקי — HUB-11 מכסה חלק, לא הכל |
| G-05 | בגדי חורף / בגדי עונה | Content gap | פעות עתידי, מוצרים orphan קיימים |
| G-06 | מוצרי האכלה / הנקה | Content gap | קטגוריה לא מכוסה, מוצרים בחנות |
| G-07 | קישורי מוצר→מאמר (HUB-11) | Linking gap | HUB-11 COMPLETE — product pages לא מפנות למאמרים |
| G-08 | קישורי HUB→HUB חסרים (cross-hub) | Linking gap | קישורים חוצי-HUB זוהו ב-hub-registry אך לא ממומשים |
| G-09 | אביזרים לבובת ריבורן | Future Product Gap | מוצרים מתוכננים — HUB-9/10 חזק אך אביזרים לא ממופים |
| G-10 | רחפן משחק | Future Product Gap | מוצר מתוכנן — לא מיוצג בבאקלוג האורגני; נדרשת brand-fit validation |
| G-11 | רובוט AI לילדים TOYA | Future Product Gap | מוצר מתוכנן — פוטנציאל תוכן גבוה; נדרשים product facts + brand-fit validation |
| G-12 | product-reverse-index.json rebuild v2.0 | System gap | v1.2 מכסה HUB-1–8 בלבד; HUB-9, HUB-10, HUB-11 חסרים — משפיע על Product→Article mapping עתידי |

---

## 3. Backlog — תור עבודה ממוין

### סטטוס: ACTIVE (execution) | Gap Map Planning: CLOSED ✅ (2026-04-29) | עודכן: 2026-04-29

| # | פריט | סוג | עדיפות | סטטוס | הערה |
|---|------|-----|--------|--------|-------|
| B-01 | HUB-11 — בגדי קיץ לתינוק | HUB | HIGH | ✅ COMPLETE | ראשון מה-Layer 5, 7 מאמרים live |
| B-02 | Post-HUB-11 Linking Audit | Linking audit | HIGH | ✅ COMPLETE | בוצע 2026-04-29 — ראה hub11-product-to-article-plan.md |
| B-03 | G-01 — בגדי שמחה / שמלות חגיגיות | HUB candidate | HIGH | ⏳ WAITING | likely next HUB |
| B-04 | G-02 — Reborn YAMLs (6 missing) | System task | MEDIUM | ⏳ WAITING | prerequisite לפני Reborn expansion |
| B-05 | G-03 — נעלי קיץ / כפכפים | HUB candidate | MEDIUM | ⏳ WAITING | expansion of HUB-6 |
| B-06 | G-04 — אביזרים עונתיים (השלמה) | HUB candidate | MEDIUM | ⏳ PARTLY COVERED | HUB-11 מכסה חלק — audit נדרש |
| B-07 | G-05 — בגדי חורף / עונתי | HUB candidate | MEDIUM | ⏳ WAITING | seasonal — לפתוח לפני ספטמבר |
| B-08 | G-06 — מוצרי האכלה / הנקה | HUB candidate | LOW | ⏳ WAITING | קטגוריה חדשה — audit תחילה |
| B-09 | G-09 — אביזרים לבובת ריבורן | Future Product Gap | HIGH | ⏳ WAITING | נדרשים: product data + T1 approval לפני ביצוע |
| B-10 | G-10 — רחפן משחק | Future Product Gap | MEDIUM-HIGH | ⏳ WAITING | נדרשת brand-fit validation לפני ביצוע |
| B-11 | G-11 — רובוט AI לילדים TOYA | Future Product Gap | HIGH | ⏳ WAITING | נדרשים: product facts, age range, safety claims + T1 approval |
| B-12 | G-12 — product-reverse-index.json rebuild v2.0 | System task | MEDIUM | ⏳ WAITING | rebuild לכלול HUB-9, HUB-10, HUB-11; אימות מול internal_content_map v5.9+ |

### כלל הבחירה:
> לפני בחירת הפריט הבא מהבאקלוג — חייב להיות Post-HUB Audit עבור ה-HUB הקודם.
> B-02 חייב להיסגר לפני פתיחת B-03.

---

## 3a. Layer 5 Gap Map Planning — מצב לקראת סגירה

> **סטטוס:** ✅ CLOSED — Gap Map Planning הוכרז סגור רשמית (2026-04-29).

| פרמטר | ערך |
|-------|-----|
| Gap Map items | 12 (G-01–G-12) |
| Backlog items | 12 (B-01–B-12) |
| DONE | 2 (B-01 HUB-11, B-02 Post-HUB Audit) |
| WAITING | 10 (B-03–B-12) |
| BLOCKED | 0 |
| Future Product Gaps included | YES (B-09–B-11) |
| Product→Article planning included | YES (hub11-product-to-article-plan.md) |
| System Gaps included | YES (B-04 Reborn YAMLs, B-12 reverse-index rebuild) |
| Linking Gaps included | YES (G-07, G-08) |
| Content Gaps included | YES (G-01, G-03, G-04, G-05, G-06) |
| Layer 5 execution backlog | ACTIVE — B-03–B-12 available for future selection |

### הכרזת סגירה רשמית:

> **"Layer 5 planning is closed. Execution items B-03 through B-12 remain available for future selection. No next backlog item is selected automatically."**

### תנאי שנסגרו:
```
✅ Gap Map כולל: content gaps, system gaps, linking gaps, future product gaps, GSC tasks
✅ G-12/B-12 נוסף — reverse-index rebuild רשום
✅ B-01 HUB-11 COMPLETE — 7 מאמרים live
✅ B-02 Post-HUB Audit COMPLETE — 16 מוצרים ממופו
✅ Backlog ממוין לפי עדיפות
✅ Completion Audit עבר PASS conditional → PASS
```

> **הבחנה חשובה:** סגירת Gap Map Planning ≠ סגירת Layer 5.
> Layer 5 execution (HUBs, Post-HUB Audits) ממשיך עם כל HUB שנבחר מהבאקלוג.
> Layer 6 לא נפתח — פתיחת Layer 6 דורשת audit ואישור נפרדים.

---

## 3b. Future Product Gaps — מדיניות

**הגדרה:** מוצרים מתוכננים לחנות שאינם live עדיין, אך עם פוטנציאל תוכן ברור.

> ⚠️ Future Product Gaps אינם מוצרים קיימים. אין לכלול אותם בספירת orphan products.
> ביצוע כל פריט מסוג זה מותנה ב:
> 1. אישור T1 נפרד מאייל
> 2. קבלת נתוני מוצר (עובדות, טווח גיל, קליימים)
> 3. brand-fit validation לפי קטגוריה

### פירוט Future Product Gaps

**B-09 — אביזרים לבובת ריבורן (G-09)**
- קשר ל-HUB קיים: HUB-9 / HUB-10
- רציונל: אורגני Reborn חזק — אביזרים לא ממופים
- כיווני תוכן מוצעים:
  - אביזרים לבובת ריבורן
  - מה קונים יחד עם בובת ריבורן
  - בגדים / מוצצים / עגלה / ערכת טיפול לבובת ריבורן
- חסמים: product data נדרש + T1 approval

**B-10 — רחפן משחק (G-10)**
- קשר HUB אפשרי: toys / gifts / smart toys
- רציונל: מוצר מתוכנן, לא מיוצג כלל בבאקלוג
- כיווני תוכן מוצעים:
  - רחפן משחק לילדים
  - איך לבחור רחפן לילד
  - מתנה טכנולוגית לילדים
- חסמים: brand-fit validation נדרשת לפני ביצוע

**B-11 — רובוט AI לילדים TOYA (G-11)**
- קשר HUB אפשרי: AI toys / smart toys / gifts for kids
- רציונל: differentiation גבוה, פוטנציאל תוכן חזק
- כיווני תוכן מוצעים:
  - רובוט AI לילדים
  - צעצוע חכם לילדים
  - מתנה טכנולוגית לילדים
  - TOYA robot product support content
- חסמים: product facts, age range, safety claims, brand-fit validation — הכל נדרש לפני ביצוע

**B-12 — product-reverse-index.json rebuild v2.0 (G-12)**
- סוג: System gap
- רציונל: v1.2 נוצר 2026-04-12, מכסה HUB-1 עד HUB-8 בלבד (25 מוצרים). HUB-9 (Reborn), HUB-10 (Reborn Benefits), HUB-11 (Summer Clothing) — כולם חסרים.
- השפעה: כל future Article→Product ו-Product→Article mapping ל-HUB-9–11 אינו מגובה ב-reverse-index.
- סקופ לביצוע עתידי:
  - rebuild v2.0 לכלול HUB-9, HUB-10, HUB-11
  - כלול מוצרי Reborn (HUB-9/10)
  - כלול summer clothing / swimwear / hats / swimming accessories (HUB-11, 16 מוצרים)
  - אימות מול internal_content_map.json v5.9+
- חסמים: ביצוע לא נדרש עכשיו — לפי עדיפות ב-backlog

---

## 4. הכלל: Post-HUB Linking Audit

**אחרי שHUB מסומן COMPLETE, הוא אינו נחשב סגור לחלוטין עד שPost-HUB Linking Audit הושלם.**

### Policy (מחייב):

> "After a HUB is marked COMPLETE, it is not considered fully closed until a Post-HUB Linking Audit is completed. This audit must verify:
> 1. Article → Product links exist where relevant.
> 2. Product → Article links are possible and mapped.
> 3. Article → Article links inside the HUB are valid.
> 4. Hub → Hub cross-links are valid.
> 5. All linked URLs return HTTP 200.
> 6. GSC manual indexing list is documented."

### 4.1 ארבעת סוגי האוקיט:

| סוג | שאלה | מה בודקים |
|-----|-------|-----------|
| Article → Product | האם המאמרים מפנים למוצרים הנכונים? | product_mention, href=/products/handle |
| Product → Article | האם עמודי המוצר מפנים למאמרים רלוונטיים? | הגדרת mapping בלבד — לא live edit |
| Article → Article | האם הקישורים הפנימיים בתוך ה-HUB תקינים? | בדיקת href, HTTP 200 |
| Hub → Hub | האם קישורי cross-hub בין HUBs שונים תקינים? | internal_content_map cross-references |

### 4.2 חשוב — Product→Article:
**Product-to-Article linking = mapping ראשון, לא עריכה חיה.**
האוקיט מגדיר היכן עמוד מוצר *צריך* לקשר למאמר — לא ביצוע השינוי בשופיפיי.
ביצוע שינויים חיים בשופיפיי = T0 נפרד, אחרי אישור אייל.

### 4.3 מצב HUB-11:

| בדיקה | מצב |
|-------|------|
| Article → Product | ✅ בוצע — product_mention בכל 7 מאמרים |
| Product → Article | ✅ MAPPED — 16 מוצרים ממופו ב-hub11-product-to-article-plan.md | PENDING IMPLEMENTATION (T1) |
| Article → Article | ✅ בוצע — cross-links ב-hub-registry |
| Hub → Hub | ✅ חלקי — C1→HUB-7, C3→HUB-4, C5→HUB-2, C6→HUB-3 |
| HTTP 200 verify | ✅ כל 7 URLs אומתו |
| GSC indexing | ⏳ PENDING — C2-C6 ממתינים לבקשה ידנית (פעולת אייל) |

---

## 5. HUB-11 — תיעוד ביצוע (Layer 5 — פריט ראשון)

| שדה | ערך |
|-----|-----|
| HUB | HUB-11 — בגדי קיץ לתינוק |
| Layer | Layer 5 |
| Backlog item | B-01 |
| Articles | 7 (Pillar + C1-C6) |
| Published | 2026-04-28 (Pillar) + 2026-04-29 (C1-C6) |
| QA | 16/16 PASS × 7 מאמרים |
| Product groups | summer clothing, swimwear, hats, swimming accessory |
| Article IDs | Pillar: 686702362937, C1: 686705443129, C2: 686727070009, C3: 686727528761, C4: 686727790905, C5: 686728216889, C6: 686728479033 |

### URLs חיות:
- Pillar: `https://www.babymania-il.com/blogs/news/bgdey-kayts-letinok-madrikh-male-ma-lilbosh-ma-lakakhat-layam`
- C1: `https://www.babymania-il.com/blogs/news/eikh-lhalbisht-tinok-bakayts-madrikh-lfi-gil-khom-ushaot`
- C2: `https://www.babymania-il.com/blogs/news/bgad-yam-letineket-eikh-livkhor-ma-livdok-ukrem-haganah`
- C3: `https://www.babymania-il.com/blogs/news/kovah-shemesh-letinok-lama-zeh-hova-vekheytsad-livkhor-nakhon`
- C4: `https://www.babymania-il.com/blogs/news/smlot-kayts-letineket-hadgamim-yoter-nonhim-lahom-hayisraeli`
- C5: `https://www.babymania-il.com/blogs/news/khalifat-pishtan-letinok-hayitronot-eikh-livkhor-umatay-lilbosh`
- C6: `https://www.babymania-il.com/blogs/news/brekha-im-tinok-bitakhon-tsiyud-ushahot-hamumlatsot`

### פעולות ממתינות:
1. **GSC Manual Indexing Request** — C2-C6 (5 URLs) — פעולת אייל ב-GSC UI
2. ~~**Post-HUB-11 Linking Audit** — B-02~~ — ✅ COMPLETE (2026-04-29)
3. **Product→Article implementation** — 16 מוצרים — T1 approval נדרש לפני ביצוע ב-Shopify
4. **B-03 — בגדי שמחה / שמלות חגיגיות** — ✅ UNBLOCKED (B-02 סגור)

---

## 6. מדיניות בחירת הבא

```
לא פותחים HUB חדש עד:
  ✅ HUB הקודם COMPLETE (כל מאמרים live + HTTP 200)
  ✅ Post-HUB Linking Audit הושלם
  ✅ GSC indexing list תועד
  ✅ Backlog מסודר לפי עדיפות עדכנית
```

### המלצה נוכחית:
**הצעד הבא המומלץ: B-03 — בגדי שמחה / שמלות חגיגיות**
- B-02 סגור ✅ — hub11-product-to-article-plan.md נוצר
- GSC Manual Indexing Request עדיין ממתין (פעולת אייל)
- Product→Article implementation ממתין ל-T1 approval
- B-03 UNBLOCKED — ניתן לפתוח HUB חדש

---

## 7. היסטוריית עדכונים

| תאריך | שינוי |
|-------|-------|
| 2026-04-29 | v1.0 — נוצר. Layer 5 OPEN. HUB-11 COMPLETE. Backlog ראשוני. Post-HUB rule נוסף. |
| 2026-04-29 | v1.1 — B-02 COMPLETE. Product→Article mapping נוצר (hub11-product-to-article-plan.md). B-03 UNBLOCKED. |
| 2026-04-29 | v1.2 — Future Product Gaps נוספו: G-09 (אביזרים לריבורן), G-10 (רחפן), G-11 (TOYA). Backlog: B-09–B-11. Gap Map: 11 פריטים. |
| 2026-04-29 | v1.3 — G-12/B-12 נוסף (reverse-index rebuild v2.0). סעיף 3a נוסף (closure prep). Gap Map: 12 פריטים. Backlog: 12 פריטים. READY FOR CLOSURE DECLARATION. |
| 2026-04-29 | v1.4 — Gap Map Planning CLOSED ✅ רשמית. הכרזת סגירה נוספה. Execution backlog נשאר פתוח. Layer 6 לא נפתח. |
