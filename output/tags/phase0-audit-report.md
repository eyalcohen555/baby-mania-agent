# Layer 6 — Phase 0 Opening Audit Report
## BabyMania Organic | Date: 2026-04-29 | Status: COMPLETE

---

## 1. Verified Inventory Scope

| מדד | ערך |
|-----|-----|
| Total products (Shopify) | **600** |
| Active | **393** ← verified inventory scope לLayer 6 |
| Draft | **44** |
| Archived | **159** |
| Pages fetched (REST, limit=250) | 2 |
| Data source | Shopify REST API 2024-10 — read-only |

**Verified inventory scope לLayer 6: 393 מוצרים active.**

---

## 2. YAML Coverage

| מדד | ערך | % |
|-----|-----|---|
| YAML files (shared/product-context/) | 294 | — |
| Active products WITH yaml | **269** | **68.4%** |
| Active products WITHOUT yaml | **124** | **31.6%** |
| YAMLs not matched to active product | 25 | (archived/draft) |

### ממצא YAML:
- 124 active products אין להם YAML — Layer 6 tag sourcing יהיה חלקי עבורם
- 25 YAMLs מיותמים (archived/draft) — ניתן להתעלם
- YAML coverage מספקת לpilot (Phase 6) אם מגבילים ל-269 מוצרים בשלב הראשון

---

## 3. ניתוח תגיות קיימות

| מדד | ערך | % |
|-----|-----|---|
| Active products עם תגיות | **268** | **68.2%** |
| Active products ללא תגיות כלל | **125** | **31.8%** |
| סה"כ ערכי תג ייחודיים | **71** | — |
| סה"כ תגיות (כולל כפילויות) | ~1,200+ | — |

### Top 30 תגיות קיימות:

| תג | כמות | קטגוריה שייכת | מצב |
|----|------|--------------|-----|
| baby-gift | 150 | CAT-E (Occasion) | ✅ valid |
| newborn-clothing | 136 | CAT-A (Product Type) | ✅ valid |
| everyday-baby-wear | 104 | CAT-E (Occasion) | ✅ valid |
| neutral-baby-outfit | 101 | CAT-F (Gender) | ✅ valid |
| **Copy AI** | **75** | — | ❌ **SPURIOUS — לא תגית SEO** |
| baby-shower-gift | 43 | CAT-E (Occasion) | ✅ valid |
| `������` (garbled) | 38 | — | ❌ **GARBLED — קידוד עברית שבור** |
| baby-set | 35 | CAT-A (Product Type) | ✅ valid |
| baby-suit | 33 | CAT-A (Product Type) | ✅ valid |
| baby-shoes | 26 | CAT-A (Product Type) | ✅ valid |
| winter-baby-wear | 20 | CAT-C (Season) | ✅ valid |
| summer-baby-wear | 20 | CAT-C (Season) | ✅ valid |
| girls-clothing | 18 | CAT-F (Gender) | ✅ valid |
| cotton-baby | 13 | CAT-D (Fabric) | ✅ valid |
| kids-clothing | 12 | CAT-A (Product Type) | ⚠️ too broad |
| bear-print-baby | 11 | CAT-G (Style) | ✅ valid |
| elegant-baby | 10 | CAT-G (Style) | ✅ valid |
| 12-18 `????` | 7 | CAT-B (Age) | ❌ **GARBLED Hebrew** |
| 6-12 `????` | 7 | CAT-B (Age) | ❌ **GARBLED Hebrew** |
| All categories | 3 | — | ❌ **SPURIOUS — admin tag** |
| 18-24M | 2 | CAT-B (Age) | ⚠️ format inconsistent |
| 3-6M6-9M | 1 | CAT-B (Age) | ❌ **MALFORMED — merged values** |

---

## 4. בעיות קריטיות שזוהו

### B1 — "Copy AI" tag (75 מוצרים) — HIGH PRIORITY
- תג `Copy AI` קיים ב-75 מוצרים active
- מקור: automation קודמת (Layer 3/4) שהוסיפה תג admin בטעות
- בעיה: תג זה מופיע בניווט Shopify ונגלה ללקוחות
- פעולה נדרשת: **הסרה לפני Phase 1** — T1 (read+write, requires Ayal approval)

### B2 — Garbled Hebrew encoding (38+ מוצרים)
- תגיות בעברית שנשברו בייצוא/ייבוא: `������`, `12-18 ????`, `6-12 ????`, `18-24 ????` וכו'
- כמות כוללת: ~70 instances גרסאות שבורות
- פעולה נדרשת: **ניקוי לפני Phase 1** — T1

### B3 — "All categories" tag (3 מוצרים)
- תג admin לא-SEO
- פעולה נדרשת: הסרה — T1

### B4 — גיל: פורמט לא עקבי
- חלק: `18-24M` (אנגלית), חלק: `18-24 ????` (עברית שבורה), חלק: ללא גיל
- פורמט הטקסונומיה עדיין לא מוגדר — ייקבע ב-Phase 1

### B5 — אין prefix:value format
- תגיות קיימות: `baby-gift`, `cotton-baby` — לא `cat-a:set`, `age-b:0-3m`
- **החלטה נדרשת:** האם Layer 6 ממיר תגיות קיימות לפורמט חדש, או מוסיף בנוסף?

---

## 5. כיסוי קטגוריות קיים (Partial Assessment)

| קטגוריה | כיסוי קיים | הערה |
|---------|-----------|------|
| CAT-A (Product Type) | ✅ חלקי — 15+ ערכים | לא מקיף, לא עקבי |
| CAT-B (Age Group) | ❌ גרבל — לא שמיש | פורמט שבור + חסר |
| CAT-C (Season) | ✅ חלקי — 4 עונות | coverage נמוכה |
| CAT-D (Fabric) | ✅ חלקי — 8 ערכים | coverage נמוכה |
| CAT-E (Occasion) | ✅ חלקי — gift heavy | לא מאוזן |
| CAT-F (Gender) | ✅ חלקי — 3 ערכים | ✓ |
| CAT-G (Style) | ✅ חלקי — ~10 ערכים | inconsistent |

**מסקנה:** 6/7 קטגוריות קיימות בצורה חלקית — טקסונומיה מלאה ועקבית אינה קיימת.

---

## 6. Phase Prerequisites Check

| # | תנאי | מצב | הערה |
|---|------|-----|------|
| 1 | Layer 5 Gap Map Planning CLOSED | ✅ | 2026-04-29 |
| 2 | HUB-11 COMPLETE | ✅ | 7/7 LIVE |
| 3 | B-02 Post-HUB Audit COMPLETE | ✅ | 2026-04-29 |
| 4 | Layer 3/4 closure UNCHANGED | ✅ | COMPLETE |
| 5 | Shopify API access — read | ✅ | verified |
| 6 | Verified inventory scope defined | ✅ | 393 active |
| 7 | YAML coverage assessed | ✅ | 269/393 (68.4%) |
| 8 | Existing tags audited | ✅ | 71 unique values |
| 9 | Critical tag issues identified | ✅ | B1-B5 documented |

---

## 7. Tag Field Decision — נדרש מאייל

**השאלה:** איפה ישבו תגיות Layer 6?

| אפשרות | יתרון | חסרון |
|--------|-------|-------|
| **Native Shopify tags** | פשוט, ב-Smart Collections, גלוי ב-Storefront API | גלוי ללקוח — כל tag רע נראה |
| **Metafields (custom)** | שליטה מלאה, לא גלוי אוטומטית | צריך Liquid לחשוף בניווט |
| **שניהם במקביל** | גמישות מלאה | כפילות, יותר maintenance |

**המלצה:** Native tags — מכיוון שהמטרה היא Smart Collections + navigation. אבל B1-B3 חייבים להיות מנוקים קודם.

**הכרעה סופית: אייל**

---

## 8. Pre-Phase-1 Cleanup — נדרש T1 Approval

לפני שניתן לפתוח Phase 1 (Taxonomy), שלושה cleanups נדרשים:

| קוד | פעולה | כמות מוצרים | Tier |
|-----|--------|------------|------|
| CL-1 | הסרת "Copy AI" מכל מוצר | 75 | T1 |
| CL-2 | הסרת garbled Hebrew tags | ~38+ | T1 |
| CL-3 | הסרת "All categories" | 3 | T1 |

**אלה אינן Layer 6 tag additions — זהו tag cleanup בלבד.**
**ניתן לבצע כ-Pre-Phase-1 batch אחד, עם אישור אייל.**

---

## 9. סיכום Phase 0 — VERDICT

| שדה | ערך |
|-----|-----|
| Phase 0 status | ✅ COMPLETE |
| Verified inventory scope | **393 active products** |
| YAML coverage | **269/393 (68.4%)** — מספיק לpilot |
| Existing tags | **71 unique values, partial structure, 3 critical issues** |
| Pre-Phase-1 cleanup needed | **YES — CL-1, CL-2, CL-3 (T1 approval)** |
| Ready for Phase 1 | **CONDITIONAL — pending T1 cleanup + Ayal tag field decision** |

---

## 10. פעולות נדרשות מאייל

| # | פעולה | עדיפות |
|---|--------|-------|
| A1 | אישור Pre-Phase-1 cleanup (CL-1/2/3) — T1 | HIGH |
| A2 | בחירת tag field: Native tags vs Metafields | HIGH |
| A3 | אישור פתיחת Phase 1 (Taxonomy Spec) לאחר cleanup | HIGH |
| A4 | YAML gap decision: 124 active products ללא YAML — ליצור? לדלג? | MEDIUM |

---

## 11. Files Created

| קובץ | תוכן |
|------|------|
| `output/tags/phase0-raw-products.json` | 393 מוצרים active עם tags |
| `output/tags/phase0-audit-summary.json` | סיכום מספרי |
| `output/tags/phase0-audit-report.md` | קובץ זה |

---

*Phase 0 הורץ: 2026-04-29 | read-only | T0 | אין שינוי ב-Shopify*
