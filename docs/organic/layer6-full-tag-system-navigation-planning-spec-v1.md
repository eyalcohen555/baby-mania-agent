# Layer 6 — Full Tag System & Navigation Foundation
## Planning Specification v1.1
### BabyMania Organic | Created: 2026-04-29 | Status: PLANNING — NOT OPEN FOR EXECUTION

---

> **חובה:** קובץ זה הוא מסמך תכנון בלבד.
> שום ביצוע מהמסמך הזה אינו מורשה עד שאייל נותן אישור מפורש לפתוח Layer 6.
> Opening Audit נדרש לפני כל ביצוע.

---

## 1. הגדרת Layer 6

**Layer 6 = Full Tag System + Navigation Foundation**

Layer 6 היא שכבת תשתית סמנטית. מטרתה: לתת לכל מוצר ב-BabyMania תגיות מובנות, מבוססות-מקורות, ניתנות לאימות — ולהפוך אותן לבסיס לניווט חכם ולאוספים אוטומטיים.

Layer 6 אינה שכבת תוכן. היא אינה Layer 5 product→article. היא אינה שיפור SEO של כותרות.

---

## 2. סקופ מדויק

### 2.1 מה Layer 6 כוללת (IN SCOPE)

| # | פעולה | שלב |
|---|--------|------|
| 1 | Taxonomy design — 7 קטגוריות, כל ערכי תג | Phase 1 |
| 2 | Source mapping — כל תג ← מקור מאומת | Phase 2 |
| 3 | Validation gates (8 שערים) — כל תג חייב לעבור | Phase 3 |
| 4 | Dry-run audit — בדיקת כל תגיות בלי Shopify live | Phase 4 |
| 5 | Ayal review — אישור ידני לפני Shopify | Phase 5 |
| 6 | Small live batch (T3) — 10–20 מוצרי pilot | Phase 6 |
| 7 | Gradual rollout (T3) — verified inventory scope שלם | Phase 7 |
| 8 | Smart Collections planning + test | Phase 8 |
| 9 | Navigation foundation planning | Phase 9 |
| 10 | Mega Menu build (אופציונלי — Phase 10 בלבד) | Phase 10 |

### 2.2 מה Layer 6 אינה כוללת (OUT OF SCOPE)

| נושא | למה הוא בחוץ |
|------|--------------|
| Mega Menu Liquid / theme changes | Phase 10 בלבד — לא לפני Phase 9 |
| Shopify live changes לפני T3 approval | Policy מחייב |
| Product → Article (hub11-product-to-article-plan.md) | Layer 5 carryover — לא Layer 6 |
| GSC indexing (HUB-10/11 pending) | Layer 5 carryover — פעולת אייל ב-GSC UI |
| פתיחת HUB חדש (B-03 ואילך) | Layer 5 execution — לא Layer 6 |
| 244 product title quality fix | SEO quality backlog — לא Layer 6 |
| Layer 3/4 quality backlog (score 5.25/10) | Layer 5 carryover — לא Layer 6 |
| Google Cloud billing renewal | Layer 5 carryover — פעולת אייל |

---

## 3. ארכיטקטורת תגיות — 3 רמות

```
LEVEL 1: Internal Tags (Admin Only)
  prefix:value format — לא גלויים ללקוח
  דוגמה: cat-a:onesie, age-b:0-3m, season-c:summer

LEVEL 2: Collection Tags (SEO Slugs)
  Shopify collection handles — ניתנים לאינדוקס
  דוגמה: "summer-clothing", "newborn-0-3m", "cotton-fabric"

LEVEL 3: Customer Labels (Hebrew UI)
  קריא לאדם — ניווט חזיתי + filters
  דוגמה: "קיץ", "0-3 חודשים", "כותנה"
```

### 3.1 כלל ה-3 רמות:
> כל תג חייב להתקיים ב-3 הרמות. תג ב-Level 1 בלבד = לא הושלם.
> Level 3 = source of truth לניווט לקוח.

---

## 4. 7 קטגוריות תגיות

| קטגוריה | קוד | דוגמאות ערכים |
|---------|-----|--------------|
| Product Type | CAT-A | onesie, dress, pants, swimwear, hat, shoes, romper, set |
| Age Group | CAT-B | 0-3m, 3-6m, 6-12m, 12-18m, 18-24m, 2-3y, 3-5y |
| Season | CAT-C | summer, winter, spring-fall, all-season |
| Fabric | CAT-D | cotton, linen, polyester, bamboo, mixed |
| Occasion | CAT-E | everyday, beach, party, sleep, gift |
| Gender | CAT-F | boy, girl, unisex |
| Style | CAT-G | casual, elegant, sporty, vintage, modern |

### 4.1 שדות חובה לכל מוצר

| שדה | חובה / מומלץ | gates |
|-----|------------|-------|
| CAT-A (Product Type) | חובה | G1–G8 |
| CAT-B (Age Group) | חובה | G1–G8 |
| CAT-C (Season) | חובה | G1–G8 |
| CAT-F (Gender) | חובה | G1–G8 |
| CAT-D (Fabric) | מומלץ | G1–G5 |
| CAT-E (Occasion) | מומלץ | G1–G5 |
| CAT-G (Style) | מומלץ | G1–G5 |

---

## 5. 8 שערי Validation

> כל תג חייב לעבור את כל השערים הרלוונטיים. כישלון בשער אחד = תג לא עולה.

| # | שם השער | תנאי מעבר |
|---|---------|-----------|
| G1 | Source Exists | מקור מוגדר: product title / description / image alt / YAML |
| G2 | Format Valid | prefix:value תקין, ללא רווחים, lowercase |
| G3 | Source Traceable | ניתן לאתר ולאמת את המקור מחדש |
| G4 | No Forbidden Inference | תג לא נובע מהנחה — רק מעובדה מוצהרת |
| G5 | Essential Coverage | כל 4 שדות חובה (A/B/C/F) נוכחים |
| G6 | No Duplicates | אין תגים כפולים באותו מוצר |
| G7 | Collection Consistency | תגים עקביים עם collection הנוכחית של המוצר |
| G8 | Quality Score ≥75 | ראה נוסחת ציון ב-סעיף 7 |

### 5.1 כלל אי-ירידה:
> **No Forbidden Inference (G4) = zero-tolerance.**
> אסור לתייג מוצר ב-"cotton" אם זה לא כתוב מפורשות בתיאור / YAML / כותרת.
> האינפרנס "נראה כמו כותנה" = פסול.

---

## 6. 10 שלבים לביצוע Layer 6

> שלבים 0–5 = לא נוגעים ב-Shopify live.
> שלב 6 ואילך = T3 approval נדרש לפני כל שינוי חי.

### Phase 0 — Opening Audit (GATE BEFORE ALL ELSE)

**מטרה:** לאמת שכל ה-prerequisites קיימים לפני פתיחת Layer 6.

| בדיקה | קריטריון |
|-------|---------|
| verified inventory scope | כמה מוצרים live ב-Shopify כרגע |
| YAML coverage | כמה מתוכם יש להם product-context YAML |
| Layer 5 carryover status | HUB-11 product→article — pending/done |
| Layer 3/4 baseline | COMPLETE (closure לא משתנה — רק quality backlog) |
| Tag tools available | scripts קיימים לקריאת tags מ-Shopify |
| Tag field decision | metafield vs native tag — החלטה נדרשת |

**Output:** Phase 0 Audit Report — מאושר ע"י אייל לפני Phase 1.

---

### Phase 1 — Taxonomy Spec

**מטרה:** להגדיר את כל ערכי התגיות לכל 7 קטגוריות.

- לכל קטגוריה: רשימה סגורה של ערכים מאושרים
- לכל ערך: Hebrew label + English slug + prefix code
- Forbidden values list — ערכים אסורים (e.g. "fancy", "cute", "nice")
- Ambiguity rules — מה לעשות כשלא ברור (e.g. bamboo vs cotton blend)

**Output:** `docs/organic/layer6-taxonomy-spec.md` — חייב להיות מאושר ע"י אייל.

---

### Phase 2 — Source Mapping

**מטרה:** לקשור כל ערך תג לשדה המקור שלו בכל מוצר.

- לכל מוצר: מיפוי source → tag
- מקורות מותרים: title, description, YAML fabric_type, YAML age_range, collection handle, image alt
- מקורות אסורים: inference, assumption, "it looks like"
- Output: `output/tags/tag-source-map.json`

---

### Phase 3 — Validation Gate Scripts

**מטרה:** לבנות scripts שמריצים את 8 שערי ה-Validation אוטומטית.

- `scripts/tags/validate_tags.py` — מריץ G1–G8 על כל מוצר
- `scripts/tags/quality_score.py` — מחשב ציון לכל מוצר
- Output report: `output/tags/validation-report.json`

---

### Phase 4 — Dry Run Audit

**מטרה:** להריץ את כל validation gates על verified inventory scope — בלי Shopify live.

- Input: tag-source-map.json + validate_tags.py
- Output: `output/tags/dry-run-report.json`
- Failure threshold: >5% failure rate = Layer 6 לא ממשיכה
- Quality score threshold: ממוצע ≥75 = PASS

---

### Phase 5 — Ayal Review

**מטרה:** הצגת ממצאי dry-run לאייל לפני כל פעולה ב-Shopify.

- Dry-run report summary
- Failed products list עם סיבות
- Proposed resolutions
- **אישור ידני של אייל נדרש לפני Phase 6**

---

### Phase 6 — Small Live Batch (T3)

**מטרה:** Pilot — 10–20 מוצרים live ב-Shopify עם tags מלאות.

- Approval tier: T3 (אישור אייל מפורש)
- Scope: מוצרים שעברו G1–G8 ב-Phase 4
- Rollback plan: קובץ backup לפני כל push
- Validation post-push: קריאת tags חזרה ואימות

---

### Phase 7 — Gradual Rollout (T3)

**מטרה:** הרחבה הדרגתית לכל verified inventory scope.

- Approval tier: T3
- Batches: 20–50 מוצרים כל batch
- Monitoring: quality score לאחר כל batch
- Stop condition: >3% unexpected failures → עצירה ו-review

---

### Phase 8 — Smart Collections Planning & Test

**מטרה:** להגדיר ולבדוק Shopify Smart Collections המבוססות על תגיות שהוכחו.

**הכלל הקריטי:**
> Collections are a Layer 6 downstream phase — not the first phase.
> אסור לפתוח Smart Collections לפני שהתגיות הוכחו ב-Phase 6/7.

- Smart Collection per CAT-A, CAT-B, CAT-C, CAT-F
- Test: 2–3 collections ב-staging לפני go-live
- Approval: T3

---

### Phase 9 — Navigation & Mega Menu Planning

**מטרה:** תכנון ארכיטקטורת הניווט על בסיס Collections שאומתו.

**הכלל הקריטי:**
> Mega Menu is part of the Layer 6 goal — but cannot start before tags and collections are proven.

- Information architecture: menu hierarchy
- Mobile vs desktop navigation plan
- Filter sidebar specification
- Technical spec: Shopify sections / Liquid requirements
- **Output: navigation-spec.md — לא ביצוע Liquid עדיין**

---

### Phase 10 — Mega Menu Build (אופציונלי)

**מטרה:** ביצוע בפועל של Mega Menu ב-Shopify theme.

**תנאים:**
- Phase 9 navigation-spec.md אושר ע"י אייל
- Smart Collections מה-Phase 8 פעילות ומאומתות
- T3 approval מפורש לכל שינוי theme

**Scope:**
- Liquid changes ב-theme (header section)
- Navigation links → Smart Collections
- Visual QA: mobile + desktop + RTL

---

## 7. נוסחת ציון איכות

```
Quality Score = 
  (required_present / required_expected) × 60
  + (recommended_present / recommended_expected) × 20
  + (avg_confidence / 100) × 20

Threshold: Score ≥ 75 = PASS
           Score < 75 = FAIL — טעון תיקון לפני rollout
```

| שדה | משקל |
|-----|------|
| CAT-A, B, C, F (חובה × 4) | 60% |
| CAT-D, E, G (מומלץ × 3) | 20% |
| confidence score ממוצע | 20% |

---

## 8. ANTI-FALSE-COMPLETE RULES

### 8.1 Layer 6 אינה COMPLETE כאשר:

- ❌ תגיות קיימות ב-Shopify אבל אין source trace לכל תג
- ❌ Dry run לא הורץ (Phase 4 לא הושלם)
- ❌ Quality score ממוצע < 75
- ❌ אייל לא אישר ידנית (Phase 5 לא הושלם)
- ❌ Rollback לא נבדק
- ❌ Collections לא אומתו (Phase 8 הגיע אחרי Phase 6/7 בלבד)
- ❌ Phase 10 לא הושלם אם הוחלט לבנות Mega Menu
- ❌ "נראה טוב" / "רוב התגיות עלו" = לא מספיק

### 8.2 Layer 6 COMPLETE מוגדר בשני טיירים:

**LAYER 6 CORE COMPLETE:**
```
✅ Taxonomy approved (Phase 1)
✅ Source mapping complete (Phase 2)
✅ Validation gates passing ≥95% (Phase 3-4)
✅ Ayal review approved (Phase 5)
✅ Full rollout complete (Phase 7) — verified inventory scope
✅ Quality score ≥75 ממוצע על כל מוצר
✅ Rollback tested and documented
```

**LAYER 6 FULL COMPLETE:**
```
✅ כל תנאי CORE COMPLETE
✅ Smart Collections active and validated (Phase 8)
✅ Navigation spec approved (Phase 9)
✅ Mega Menu live + visual QA passed (Phase 10) — אם הוחלט לבנות
```

---

## 9. Product → Article — מדיניות הפרדה מפורשת

> **Product → Article הוא Layer 5 carryover — לא Layer 6.**

| נושא | Layer |
|------|-------|
| HUB-11 product→article mapping (hub11-product-to-article-plan.md) | Layer 5 — T1 approval נדרש |
| article_link metafield push ל-16 מוצרי HUB-11 | Layer 5 — T1 approval נדרש |
| Reverse cross-links (HUB-2-C1, HUB-4-Pillar, HUB-7-C3) | Layer 5 — I-01 PENDING |
| product-reverse-index.json rebuild v2.0 (B-12) | Layer 5 system task |

**כלל:** Layer 6 validation gates ו-tag rollout לא נחסמים ע"י Layer 5 carryovers.
שני הנתיבים יכולים לרוץ במקביל — אבל Layer 6 לא מחכה ל-Layer 5.

---

## 10. Rollback Plan

> כל push של תגיות ל-Shopify חייב להיות עם backup מוכן לפני הpush.

| שלב | backup |
|-----|--------|
| לפני Phase 6 (pilot) | `output/tags/backup-pre-pilot-{date}.json` |
| לפני כל Phase 7 batch | `output/tags/backup-batch-{n}-{date}.json` |
| לפני Phase 8 collections | `output/collections/backup-pre-collections-{date}.json` |
| לפני Phase 10 theme | theme export מלא לפני כל Liquid change |

**Rollback trigger:** >3% unexpected failures post-push → עצירה מיידית → restore backup.

---

## 11. Gate לפני פתיחת Layer 6

> Layer 6 לא נפתחת עד שכל הפריטים הבאים ירוקים:

| # | תנאי | מצב נוכחי |
|---|------|-----------|
| 1 | Layer 5 Gap Map Planning CLOSED | ✅ CLOSED (2026-04-29) |
| 2 | HUB-11 COMPLETE (כל 7 מאמרים live) | ✅ COMPLETE (2026-04-29) |
| 3 | B-02 Post-HUB Audit COMPLETE | ✅ COMPLETE (2026-04-29) |
| 4 | Layer 3/4 closure status UNCHANGED | ✅ UNCHANGED |
| 5 | Opening Audit (Phase 0) הורץ ואושר | ⏳ PENDING |
| 6 | אישור אייל לפתוח Layer 6 | ⏳ PENDING |

**מצב נוכחי:** Layer 6 = NOT OPEN. פריטים 5–6 ממתינים.

---

## 12. תלויות חיצוניות (לא חוסמות Layer 6)

| פריט | סטטוס | בעלים |
|------|--------|-------|
| Google Cloud billing renewal | ⏳ חסום — Mastercard 0400 נדחה | אייל |
| Service account GSC Owner | ⏳ ממתין | אייל |
| HUB-10 GSC C5-C6 manual indexing | ⏳ ממתין | אייל |
| HUB-11 GSC C2-C6 manual indexing | ⏳ ממתין | אייל |
| 4 collections GSC indexing | ⏳ ממתין | אייל |

> תלויות אלה הן Layer 5 carryovers. הן לא חוסמות את Phase 0 של Layer 6.
> Phase 6 ואילך (Shopify live) תלויים רק ב-T3 approval — לא בGSC.

---

## 13. Conductor YAML — תבנית

```yaml
plan_id: "layer6-phase0-audit"
layer: 6
phase: 0
name: "Layer 6 Opening Audit"
approval_tier: "T0"
requires_ayal_approval: false

steps:
  - id: "count_live_products"
    action: "shopify_read"
    description: "Count live products — verified inventory scope"
    output: "output/tags/phase0-product-count.json"

  - id: "yaml_coverage_check"
    action: "local_read"
    description: "Check YAML coverage for all live products"
    input: "shared/product-context/"
    output: "output/tags/phase0-yaml-coverage.json"

  - id: "existing_tags_audit"
    action: "shopify_read"
    description: "Read existing tags for all products — no write"
    output: "output/tags/phase0-existing-tags.json"

  - id: "generate_audit_report"
    action: "generate_report"
    description: "Compile Phase 0 audit report"
    inputs:
      - "output/tags/phase0-product-count.json"
      - "output/tags/phase0-yaml-coverage.json"
      - "output/tags/phase0-existing-tags.json"
    output: "output/tags/phase0-audit-report.md"
```

---

## 14. מגבלות scope — verified inventory scope

> בכל מסמך Layer 6: "verified inventory scope" = מספר המוצרים שאומת ב-Phase 0.
> אין להשתמש במספר ספציפי (כגון 244, 294) כי המלאי משתנה.
> המספר המדויק נקבע ב-Phase 0 Audit בלבד.

---

## 15. היסטוריית גרסאות

| גרסה | תאריך | שינוי |
|------|-------|-------|
| v1.0 | 2026-04-29 | Draft ראשוני — תכנון ב-session |
| v1.1 | 2026-04-29 | 9 תיקונים: scope, product→article separation, phase ordering, anti-false-complete rules, 2-tier completion, "verified inventory scope" throughout, collections as downstream, navigation stays in Layer 6, Mega Menu phase 10 only |

---

*קובץ זה נוצר לתכנון בלבד. ביצוע מותנה ב-Phase 0 Audit + אישור אייל.*
