# SEMANTIC GATE SPEC

**גרסה:** v1.2
**תאריך עדכון:** 2026-04-23
**שייך ל:** P1-S4.1 / AUTOMATION-HARDENING-PLAN v1
**סטטוס:** Checks A–E פעילים. Check E הופעל 2026-04-23.

---

## STATUS

v1.2 — Checks A–E פעילים. Check E הופעל 2026-04-23 (PAIR_WARN=0.6, BATCH_FAIL=0.8, אישור אייל).

---

## PURPOSE

Gate 2 נועד לחסום פלטים שעוברים Gate 1 (מבנה תקין) אך נכשלים סמנטית — כלומר, הטקסט לא מדויק, לא עקבי, או מכיל טענות שאין להן עיגון.

Gate 2 פועל **לפני** bundle, **לפני** push, **לפני** closure.

---

## CHECKS

---

### CHECK A — TECHNICAL FINGERPRINT CHECK

#### WHAT IT DETECTS
מזהים טכניים גלויים בתוך הטקסט שהלקוח אמור לראות — לדוגמה: `(1113)`, `(XXXX)`, `pid:`, ביטויים שנראים כמו SKU, ID, או code-artifact.

#### INPUTS
- פלט הטקסט של כל section (hero, benefits, faq, care, fabric וכו')
- product_id

#### FAILURE CONDITION
תוצאה קטגוריית FAIL אם מתקיים **אחד** מהבאים:
- מוצאים ביטוי שמתאים לתבנית `\(\d{3,}\)` (ספרות בסוגריים)
- מוצאים ביטוי שמתאים ל-`pid:`, `id:`, `sku:`, `handle:` בטקסט גלוי
- מוצאים אחד מה-patterns הסגורים הבאים בטקסט גלוי:
  - `BM-` (קידומת פנימית)
  - `-SUIT-`, `-SET-`, `-SHOES-` (חלקי handle)
  - `_edited`, `_publisher`, `_validator` (שמות קבצים פנימיים)
  - רצף של 8+ תווים אנגליים ברצף עם מקף `-` בתוכם שאינם שם מותג ידוע

#### EXAMPLES OF FAIL
- `"חליפת קיץ לתינוק (1113) — עיצוב מאוורר"`
- `"sku: BM-SUIT-221 בד נעים לעור עדין"`
- `"handle: toddler-suit-blue כולל כובע"`

#### BLOCKING BEHAVIOR
מוצר שנכשל → **FAIL מיידי**, לא נכנס ל-bundle.
אין "warning" — זו שגיאה קשה.

#### REQUIRED EVIDENCE
- `gate2_result.json` לכל מוצר עם `check_a: PASS | FAIL`
- אם FAIL: הביטוי המזוהה + section שבו נמצא

---

### CHECK B — PRODUCT TYPE CONSISTENCY CHECK

#### WHAT IT DETECTS
אי-התאמה (mismatch) בין סוג המוצר האמיתי כפי שמוגדר ב-context לבין הטקסט שנוצר.
לדוגמה: מוצר שסוגו `חליפה` אך מתואר בטקסט כאילו הוא כובע, נעל, או אביזר.

#### INPUTS
- `product_template_type` מתוך context
- `primary_type` / `secondary_type` (אם קיימים)
- פלט הטקסט המלא של המוצר

#### FAILURE CONDITION
תוצאה קטגוריית FAIL אם מתקיים **אחד** מהבאים:

**כלל 1 — type term שגוי ב-hero_headline:**
אחד מהמונחים הבאים מופיע ב-`hero_headline` כשה-`product_template_type` אינו מסוגו:

| מונח אסור | product_template_type שבו אסור |
|---|---|
| `כובע`, `מצחייה`, `קסקט` | clothing, shoes |
| `נעל`, `סנדל`, `מגף`, `כפכף` | clothing |
| `סוליה`, `שרוכים`, `צייזל` | clothing |
| `כפפות`, `גרביים` | clothing, shoes (אלא אם כן accessories) |

**כלל 2 — תכונת מוצר שגויה ב-geo_who_for או ב-hero_subheadline:**
מוצר עם `product_template_type=clothing` שה-field `geo_who_for` או `hero_subheadline` שלו מכיל מונח מרשימת הנעלים/אביזרים לעיל.

**כלל 3 — accessory בתפקיד ראשי:**
FAIL אם `product_template_type=accessories` וה-`hero_headline` מכיל שם מוצר שאינו accessory (חליפה, סרבל, פיג'מה, בגד גוף).

#### EXAMPLES OF FAIL
- `primary_type=חליפה`, טקסט: `"הכובע הצבעוני מגן מהשמש ושומר על התינוק"` — כובע הפך לנושא
- `primary_type=סרבל`, טקסט: `"הסוליה הגמישה מאפשרת תנועה חופשית"` — תכונת נעל בסרבל

#### BLOCKING BEHAVIOR
מוצר שנכשל → **FAIL**, לא נכנס ל-bundle.
נרשם ב-`fail_reasons` עם: `detected_type` (מה הטקסט תיאר) + `expected_type` (מה ה-context מגדיר).

#### REQUIRED EVIDENCE
- `gate2_result.json` עם `check_b: PASS | FAIL`
- אם FAIL: הביטוי שגרם לכשל + הסוג שזוהה בטקסט + הסוג שצוין ב-context

---

### CHECK C — FABRICATED CLAIM CHECK

#### WHAT IT DETECTS
טענות שאין להן עיגון בנתוני המוצר — social proof מומצא, תעודות לא קיימות, נתונים מספריים ללא מקור, ציטוטים מומצאים מהורים.

#### INPUTS
- פלט הטקסט המלא
- `has_reviews` flag מה-context (`fallback_flags.has_reviews`)
- `has_stock_data` flag מה-context (`fallback_flags.has_stock_data`)

#### FAILURE CONDITION
תוצאה קטגוריית FAIL אם מתקיים **אחד** מהבאים:
- הטקסט כולל ציון כוכבים (`★`, `4.8/5`, `מדורג`) ו-`has_reviews=false`
- הטקסט כולל ציטוט הורה (`"אמרה לנו אמא..."`, `"לפי הורים רבים..."`) ו-`has_reviews=false`
- הטקסט כולל תעודה ספציפית (`"עומד בתקן ISO"`, `"מאושר על ידי..."`) שלא מופיעה ב-context
- הטקסט כולל נתון מספרי (`"90% מההורים"`, `"נבדק על ידי 500 משפחות"`) ללא מקור ב-context

#### EXAMPLES OF FAIL
- `"4.9 כוכבים — הורים אוהבים!"` כאשר `has_reviews=false`
- `"מאושר ע"י רופאי ילדים"` כאשר אין אישור ב-context
- `"'הכי טוב שקנינו' — אמרה אמא מתל אביב"` ללא review source

#### BLOCKING BEHAVIOR
מוצר שנכשל → **FAIL**.
נרשם ב-`fail_reasons` עם: `claim_text` (הטענה שזוהתה) + `missing_source` (מה לא קיים ב-context).

#### REQUIRED EVIDENCE
- `gate2_result.json` עם `check_c: PASS | FAIL`
- אם FAIL: הטענה המדויקת + הסיבה שאין לה עיגון

---

### CHECK D — DESCRIPTION BLEED CHECK

#### WHAT IT DETECTS
קטעי טקסט שהועתקו ישירות מתיאורים שיווקיים ישנים (description_raw) לתוך GEO output, או bleed של ניסוח ממוצר אחר שנכנס בטעות לטקסט הנוכחי.

#### INPUTS
- `description_raw` מה-context של המוצר (`context.yaml → description_raw`)
- פלט הטקסט המלא שנוצר
- אם קיים: טקסט קודם שהיה live למוצר זה
- `batch_product_titles[]` — רשימת title + handle של **כל** שאר המוצרים ב-batch הנוכחי (נדרש לזיהוי cross-product bleed)

> **הערה:** בדיקת ה-cross-product bleed (תנאי 2–3 להלן) היא **batch-level**. הגייט חייב לקבל את `batch_product_titles[]` כ-input לפני הרצה על כל מוצר בודד.

#### FAILURE CONDITION
תוצאה קטגוריית FAIL אם מתקיים **אחד** מהבאים:
- רצף של 8+ מילים מ-`description_raw` מופיע בטקסט החדש ללא שינוי
- מוצאים שם מוצר ספציפי של מוצר **אחר** בטקסט הנוכחי
- מוצאים handle או product title מוצר אחר בתוך הטקסט

#### EXAMPLES OF FAIL
- `description_raw`: `"סרבל פרחוני עם רוכסן בגב ורצועות קשירה"`
  טקסט חדש: `"סרבל פרחוני עם רוכסן בגב ורצועות קשירה לנוחות מקסימלית"` — 8 מילים זהות
- טקסט כולל `"חליפת LINO"` בעוד המוצר הנוכחי הוא `"חליפת MIMI"`

#### BLOCKING BEHAVIOR
מוצר שנכשל → **FAIL**.
נרשם ב-`fail_reasons` עם: `bleed_source` (מאיפה הגיע הטקסט) + `matched_sequence` (הרצף שזוהה).

#### REQUIRED EVIDENCE
- `gate2_result.json` עם `check_d: PASS | FAIL`
- אם FAIL: הרצף המדויק שזוהה + מקורו

---

### CHECK E — TEMPLATE REPETITION CHECK

#### WHAT IT DETECTS
פתיחות, סיומות, או שלדי משפטים שחוזרים על פני מוצרים שונים באותו batch, מעל סף מותר — סימן ש-generator השתמש בתבנית קבועה במקום לייצר טקסט מותאם.

#### INPUTS
- פתיחת הטקסט הראשית (2 משפטים ראשונים) של **כל** מוצר ב-batch — שדה `hero_headline` + `hero_subheadline`
- סיום הטקסט הראשי (2 משפטים אחרונים) — שדה `emotional_reassurance` או המשפט האחרון ב-faq
- ה-benefits של כל מוצר — רשימת ה-`title` fields (ללא description)

> **הערה:** check זה הוא **batch-level בלבד**. לא רץ על מוצר בודד.

#### FAILURE CONDITION
**ברמת מוצר בודד:** לא רלוונטי — check E לא מוחל על מוצר בודד.

**ברמת batch — אלגוריתם: 4-gram Jaccard similarity:**

**הגדרה:** לכל שני מוצרים A ו-B ב-batch, מחשבים Jaccard similarity על 4-grams של `hero_headline`:
```
similarity = |4grams(A) ∩ 4grams(B)| / |4grams(A) ∪ 4grams(B)|
```

**תוצאות:**
- similarity ≥ 0.6 בין שני מוצרים → PAIR_WARN (מסומן, לא עוצר)
- similarity ≥ 0.6 ב-3+ זוגות שונים → BATCH_WARN (batch מושהה)
- similarity ≥ 0.8 בין 2+ מוצרים → BATCH_FAIL (batch נעצר)

**הסף הסופי:** PAIR_WARN = 0.6 | BATCH_FAIL = 0.8 — **אושר על ידי אייל 2026-04-23, פעיל.**

#### EXAMPLES OF FAIL
- 7 מתוך 8 מוצרים פותחים ב: `"בגד איכותי שנבחר בקפידה עבור תינוקך"`
- כל מוצר ב-batch מסיים ב: `"מתאים לכל עונה ומוכן לחיבוק הבא"`

#### BLOCKING BEHAVIOR
- מוצר בודד שזוהה כחלק מ-pattern → מסומן בלבד, לא נחסם לבד
- כאשר מגיעים לסף batch → כל ה-batch נעצר לבדיקה ידנית
- אין auto-continue עד אישור אייל

#### REQUIRED EVIDENCE
- `gate2_result.json` עם `check_e: PASS | BATCH_WARN | BATCH_FAIL`
- אם BATCH_FAIL: הפתיחה/שלד החוזר + רשימת ה-PIDs שנכשלו

---

## OUTPUT FORMAT

כל הפעלה של Gate 2 על מוצר בודד מחזירה:

```json
{
  "product_id": "...",
  "timestamp": "ISO-8601",
  "status": "PASS | FAIL",
  "semantic_signature": true,
  "check_results": {
    "check_a": "PASS | FAIL",
    "check_b": "PASS | FAIL",
    "check_c": "PASS | FAIL",
    "check_d": "PASS | FAIL",
    "check_e": "PASS | BATCH_WARN | BATCH_FAIL"
  },
  "fail_reasons": [
    {
      "check": "check_X",
      "detail": "תיאור מדויק של הכשל"
    }
  ]
}
```

**כללים:**
- `semantic_signature: true` מופיע **רק** אם `status: PASS` על checks A–D **וגם** check_e אינו `BATCH_WARN` או `BATCH_FAIL` ברמת ה-batch
- `fail_reasons` הוא רשימה ריקה אם `status: PASS`
- Gate 4 (Release Gate) דורש `semantic_signature: true` — בלי זה אין bundle

**כלל signature לגבי Check E:**
- כל עוד ה-batch בסטטוס `BATCH_WARN` או `BATCH_FAIL` — **אף מוצר ב-batch לא מקבל `semantic_signature: true`**, גם אם checks A–D עברו.
- Signatures מונפקות רק אחרי שאישור אייל ניתן והסטטוס מתנקה ל-PASS.

---

## BATCH-LEVEL STOP RULE

אם מתגלה אותו semantic pattern (אחד מ-checks A–E) ביותר ממספר מוגדר של מוצרים ב-batch:

| תרחיש | סף נוכחי | פעולה |
|---|---|---|
| Check A: fingerprint חוזר | כל מקרה = 1 | FAIL מיידי לכל מוצר. אם ≥3 מוצרים — batch נעצר |
| Check B: type mismatch חוזר | ≥2 מוצרים | batch נעצר לבדיקה |
| Check C: fabricated claim | כל מקרה = 1 | FAIL מיידי. אם ≥2 מוצרים — batch נעצר |
| Check D: bleed חוזר | ≥2 מוצרים מאותו מקור | batch נעצר |
| Check E: template repetition | PAIR_WARN ≥ 0.6 → warn pair; BATCH_FAIL ≥ 0.8 ב-2+ זוגות → batch stop | עצירה + הודעה לאייל |

**ספי Check E:** PAIR_WARN = 0.6 | BATCH_FAIL = 0.8 — אושרו על ידי אייל 2026-04-23.

**כלל על-כולם:** כל batch-level stop מחייב הודעה מפורשת לאייל ואסור auto-continue.

---

## OUT OF SCOPE

Gate 2 **לא** בודק את הדברים הבאים — כדי לא לערבב Phase 1 עם Phase 3:

| נושא | למה לא כאן |
|---|---|
| Truth Record validation (אמת מוצר מלאה) | Phase 3 — Truth Record layer לא קיים עדיין |
| Variation score (ציון גיוון כמותי מלא) | Gate 3 — Repetition Gate נפרד |
| Visual QA (בדיקה חזותית) | שלב נפרד — לאחר Gate 4 |
| Rollback logic | Phase 3 |
| Risk classification per product | Phase 3 — Truth Record |
| Comparison eligibility checks | Phase 3 |
| Metafield schema validation | Gate 1 — Structure Gate |
| JSON / YAML parse errors | Gate 1 — Structure Gate |

---

*SEMANTIC GATE SPEC v1.2 — BabyMania Layer 4 — P1-S4.1 / AUTOMATION-HARDENING-PLAN v1*
*Checks A–E פעילים. Check E הופעל 2026-04-23 (PAIR_WARN=0.6, BATCH_FAIL=0.8).*
