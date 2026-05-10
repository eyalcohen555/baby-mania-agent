# Future Smart Collections Roadmap — BabyMania

**תאריך:** 2026-05-10  
**מצב:** READ-ONLY PLANNING — אין כתיבות Shopify  
**מבוסס על:** Phase 8 Navigation Pipeline (complete), Layer 6 closure, shoes taxonomy proposal

---

## 1. Smart Collections קיימות (6 live)

| Collection | Shopify ID | תנאי | מוצרים |
|---|---|---|---|
| gender-girl | 526691729721 | tag:gender-girl | 20+ |
| gender-boy | 526691762489 | tag:gender-boy | 19+ |
| type-set | 526691795257 | tag:type-set | 18+ |
| type-romper | 526691828025 | tag:type-romper | 16+ |
| occ-gift | 526691860793 | tag:occ-gift | 14+ |
| clothing-all | 526700020025 | type-set OR type-romper OR type-dress OR type-bodysuit | 51+ |

---

## 2. Smart Collections מוצעות — רודמאפ

| Collection | תג | פתוח עכשיו? | מינימום מוצרים | ניווט? | הערות |
|---|---|---|---|---|---|
| כל הנעליים | `shoes-all` (disjunctive) | לא | 30+ | ניווט ראשי | ממתין להשלמת תיוג נעליים |
| סנדלים | `shoes-sandals` | אחרי תיוג | 10+ | Sub-nav | תלוי בimage review |
| סניקרס | `shoes-sneakers` | אחרי תיוג | 10+ | Sub-nav | תלוי בimage review |
| נעלי צעד ראשון | `shoes-first-step` | אחרי תיוג | 8+ | Sub-nav | שוק ספציפי, SEO: "נעלי צעד ראשון" |
| נעלי אלגנט | `shoes-elegant` | אחרי תיוג | 8+ | Internal only | מתחת לסף ניווט — ממתין |
| שמלות | `type-dress` | אחרי REVIEW_ONLY | 9+ (עכשיו) | Sub-nav | עכשיו 9 — מספיק, חסר T3 approval |
| בגדי גוף | `type-bodysuit` | אחרי REVIEW_ONLY | 8+ (עכשיו) | Sub-nav | עכשיו 8 — על הגבול |
| כובעים | `type-hat` | אחרי REVIEW_ONLY | 4 (עכשיו) | לא | מתחת לסף, internal בלבד |
| מעילים | `type-coat` | אחרי REVIEW_ONLY | 3 (עכשיו) | לא | מתחת לסף, internal בלבד |
| מתנות | `occ-gift` | קיים ✅ | 14+ | ניווט ראשי | live — "מתנות לתינוק" בmain-menu |
| ברית/אקווינה | `occ-brit` | אחרי הרחבת occ | 8+ | Sub-nav | ביקוש ישראלי ייחודי |
| אמבטיה | `cat-bath` | שלב עתידי | 15+ | ניווט עתידי | נדרש taxonomy + scan נפרד |
| האכלה | `cat-feeding` | שלב עתידי | 15+ | ניווט עתידי | נדרש taxonomy + scan נפרד |

---

## 3. Navigation — מצב נוכחי

**main-menu (17 פריטים לאחר Phase 8F):**
- "בגדי תינוקות" (parent) עם 5 sub-items: סטים / סרבלים / בגדי בנות / בגדי בנים / כל הבגדים
- "מתנות לתינוק" — פריט ראשי נפרד
- Legacy: "בגדי בנות" / "בגדי בנים" / "מארזי מתנה" הוסרו מניווט (collections קיימות)

**Sub-nav נעליים (עתידי):**
```
נעליים (parent)
  ├── כל הנעליים
  ├── סנדלים
  ├── סניקרס
  └── נעלי צעד ראשון
```
לא לפתוח עד השלמת תיוג נעליים + 30+ מוצרים ב-shoes-all.

---

## 4. Mega Menu — שלב עתידי

**החלטה:** Mega Menu לא עכשיו.  
**מתי לשקול:** כאשר יש 4+ קטגוריות ניווט ראשיות עם sub-navs, ותנועה מספקת שמצדיקה את ה-UX.

---

## 5. summer-2024 / קיץ 2026 — הערה על handle

**handle:** `summer-2024`  
**שם תצוגה:** קיץ 2026  

**הערכה:** לא באג — עדכון שם תצוגה מכוון.  

**SEO risk:** URL כולל "summer-2024" — מבלבל לקוחות שרואים "קיץ 2026" אבל URL מכיל "2024". עשוי לפגוע בCTR כאשר URL נחשף ב-SERP.

**המלצה:** להשאיר כעת. כאשר יש תנועה אורגנית משמעותית על collection זו:
1. צור collection חדשה: handle `summer-2026`, שם "קיץ 2026"
2. הוסף 301 redirect מ-`/collections/summer-2024` → `/collections/summer-2026`
3. עדכן את הקישורים הפנימיים

**לא לשנות עכשיו** — priority נמוכה, ללא תנועה מוכחת.

---

## 6. Smart Collection — כלל פתיחה

| שלב | דרישה |
|---|---|
| 1 | תגים live על 8+ מוצרים (מוכח) |
| 2 | Dry run — Smart Collection query מחזיר count נכון |
| 3 | T3 approval מאייל |
| 4 | Live create via GraphQL/REST |
| 5 | 16 QA checks PASS (כפי שהוגדר ב-Phase 8C/8E-4) |
| 6 | שקול הוספה לניווט — navigation update נפרד (T3) |

---

## 7. תרחיש מלא — מסלול נעליים לcollections

```
עכשיו → Shoes taxonomy approved
       → Image review agent built
       → ~65 shoes reviewed + tagged (T3 batches)
       → shoes-sandals: 10+ → Smart Collection → Sub-nav
       → shoes-sneakers: 10+ → Smart Collection → Sub-nav
       → shoes-first-step: 8+ → Smart Collection → Sub-nav
       → shoes-all (disjunctive): 30+ → Smart Collection → Main nav
       → Navigation update: "נעליים" parent + 4 sub-items
```

---

*מסמך זה הוא roadmap בלבד. אין כתיבות Shopify ללא אישור T3.*
