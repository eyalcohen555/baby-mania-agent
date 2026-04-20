# AUTOMATION-HARDENING-PLAN v1
## תוכנית הקשחת האוטומציה — BabyMania Layer 4

**גרסה:** v1
**תאריך:** 2026-04-19
**Layer:** 4
**Approval Tier:** T3 (לאישור סופי של מסמך זה)
**סטטוס:** מסמך מקור רשמי — Source of Truth ניהולי

---

## תוכן עניינים

1. אבחנת שורש מערכתית
2. עקרון התכנון החדש
3. ארכיטקטורת ה-Pipeline החדשה
4. מודל סטטוסים לשחרור
5. מודל Rollout מבוסס-סיכון
6. Visual QA כשער שחרור רשמי
7. ארכיטקטורת Rollback
8. רישום חריגים מוכרים (Known Anomalies Registry)
9. מדדי איכות (Quality Metrics)
10. מדיניות Bridge / Conductor
11. כללי אסור וחובה
12. תוכנית ביצוע — Phases 1–4

**נספחים ניהוליים:**
- A. החלטת הנהלה (Executive Decision)
- B. תחום התוכנית (Scope)
- C. מודל אחריות (Ownership Model)
- D. תנאי כניסה ויציאה (Phase Entry / Exit Criteria)
- E. תוצרים נדרשים (Deliverables)
- F. מיפוי רכיבי מערכת (System Mapping)
- G. מפרט שערים קשיחים (Hard Gates Spec)
- H. ממשל שחרור (Release Governance)
- I. מדיניות סגירה (Closure Policy)
- J. סדר עדיפויות לביצוע (Priority Order)
- K. קיים מול מתוכנן (Existing vs Planned)
- L. איסור ארכיטקטורה חדשה ללא אישור
- M. שילוב ב-Runtime הקיים
- N. קודם תיקון, אחר כך הקשחה
- O. מדיניות יצירת קבצים (File Creation Policy)

---

# 1. אבחנת שורש מערכתית

הבעיה אינה כשל של כלי יחיד, ולא חסרון של חוקים נוספים.

הבעיה היא שהמערכת בנויה כך:

**מצב קיים:**
- generator (מחולל) — מייצר טקסט
- validator (בודק תקינות) — בודק מבנה בלבד
- bundler (מאגד) — אוסף תוצאות
- push (דחיפה) — כותב ל-Shopify
- verify (אימות) — בודק קיום

**הכשל המערכתי:**

אין שכבה מחייבת של:
- semantic control (בקרת משמעות)
- release gating (חסימת שחרור)
- rollback safety (בטיחות חזרה לאחור)
- risk-based sampling (דגימה לפי סיכון)

התוצאה: אשליית איכות.
**Pipeline ירוק — output פגום בלייב.**

---

# 2. עקרון התכנון החדש

המערכת עוברת מ:

**Pipeline of execution (צינור ביצוע)** — מוצר עובר כי רץ

ל:

**Pipeline of proof (צינור הוכחה)** — מוצר עובר רק אם **הוכיח** שהוא ראוי להתקדם.

כל שלב מחייב evidence (ראיה). בלי ראיה — אין מעבר.

---

# 3. ארכיטקטורת ה-Pipeline החדשה

## שכבה א — Product Truth Layer (שכבת אמת מוצר)

לפני כל generation (יצירת טקסט), לכל מוצר חייב להיות **Truth Record (רשומת אמת)** מאושרת.

**שדות חובה ב-Truth Record:**

| שדה | תיאור |
|---|---|
| `product_id` | מזהה מוצר |
| `primary_type` | סוג מוצר ראשי |
| `secondary_type` | סוג מוצר משני |
| `category` | קטגוריה |
| `season` | עונה |
| `materials` | חומרים |
| `feature_flags` | תכונות מיוחדות |
| `accessory_terms` | מונחי אביזרים |
| `comparison_eligible` | האם מותרת השוואה |
| `banned_inferences` | מסקנות אסורות |
| `risk_class` | רמת סיכון |

**כלל:** ה-generator לא מפרש title (כותרת) חופשי — הוא מקבל אמת מאושרת בלבד.

**דוגמה:** אם title כולל "עם כובע" אך `primary_type=חליפה` — אסור לייצר טקסט שמייחס למוצר תכונות של כובע.

---

## שכבה ב — Generation Layer מפוצלת

אסור generator יחיד שמנסה לעשות הכול.

**במקום זה — 5 stages (שלבים) נפרדים:**

1. `type_inference_stage` — זיהוי סוג המוצר
2. `truth_normalization_stage` — נורמליזציית הנתונים
3. `text_generation_stage` — יצירת הטקסט
4. `semantic_scan_stage` — סריקת משמעות
5. `bundle_admission_stage` — כניסה ל-bundle

כל stage קטן, חד, וניתן לבדיקה עצמאית.

---

## שכבה ג — Multi-Gate Validation (אימות רב-שערי)

לא validator יחיד — 4 שערים עצמאיים:

### Gate 1 — Structure Gate (שער מבנה)
בודק:
- פורמט
- שדות חובה — קיים / חסר / כפול
- תקינות JSON/YAML

### Gate 2 — Semantic Gate (שער משמעות)
בודק:
- התאמת סוג מוצר ל-Truth Record
- איסור מזהים טכניים בטקסט
- איסור social proof (הוכחה חברתית) לא מבוסס
- איסור bleed (דימום) מתיאור ישן
- איסור mismatch (אי-התאמה) בין title לטקסט

### Gate 3 — Repetition Gate (שער חזרות)
בודק:
- פתיחות חוזרות
- סיומות חוזרות
- שלד משפט חוזר
- variation score (ציון גיוון) — חייב לעמוד בסף

### Gate 4 — Release Gate (שער שחרור)
חוסם עד שכל הבאים עברו:
- Gate 1 — Structure: PASS
- Gate 2 — Semantic: PASS
- Gate 3 — Repetition: PASS
- Risk Review: בוצע
- Sample Review: בוצע

**אם אחד נכשל — המוצר לא נכנס ל-bundle.**

---

# 4. מודל סטטוסים לשחרור

**אסור להשתמש ב-"PASS" כללי יחיד.**

**4 סטטוסים מחייבים:**

| סטטוס | משמעות |
|---|---|
| `GENERATED` | הטקסט נוצר |
| `VALIDATED` | עבר בדיקות אוטומטיות (Gates 1–3) |
| `RELEASE-READY` | עבר Gate 4, דגימה, ו-Visual QA |
| `LIVE-VERIFIED` | נדחף ונקרא חזרה בהצלחה |

מעבר בין סטטוסים הוא חד-כיווני ומחייב evidence לכל מעבר.

---

# 5. מודל Rollout מבוסס-סיכון

אסור לעבוד על 200+ מוצרים בבת אחת ללא gating (חסימת-שלבים).

**סולם Rollout מחייב:**

| Stage | גודל | תנאי מעבר |
|---|---|---|
| A — Pilot | 8 מוצרים (כולל high-risk) | אומת בלייב |
| B — Expanded Pilot | 20 מוצרים | Stage A אומת בלייב |
| C — Controlled Batch | 50 מוצרים | Stage B אומת בלייב |
| D — Category Rollout | שאר הקטגוריה | Stages A–C ללא חריגות מערכתיות |
| E — Production Rollout | כל היתר | False Success Rate < 2% |

**חוק עצירה:** אם מתגלה אחד מהבאים — עוצרים ולא ממשיכים לבatch הבא:
- fingerprint (חותמת תבנית) מזוהה
- type mismatch (אי-התאמת סוג מוצר)
- semantic anomaly (חריגה משמעותית)
- repeated template pattern (תבנית חוזרת)

---

# 6. Visual QA כשער שחרור רשמי

Visual QA (בדיקה חזותית) אינו optional (אופציונלי).
הוא **release gate מחייב** — בלעדיו אין push.

**Sample חובה לכל rollout:**

| סוג | כמות |
|---|---|
| clothing sample (דוגמת ביגוד) | 12 |
| shoes sample (דוגמת נעלים) | 4 |
| anomaly controls (בקרות חריגות) | 2 |
| comparison cases (מקרי השוואה) | 2 |

**מה בודקים:**
- האם הטקסט נראה אנושי
- האם יש artifacts (שאריות אוטומציה)
- האם יש semantic mismatch
- האם יש template fingerprint

**בלי Visual QA מאושר — אין live push.**

---

# 7. ארכיטקטורת Rollback

לפני כל push חייבים לייצר חבילת rollback (חזרה לאחור):

- `push_scope.json` — רשימת מוצרים שנדחפים
- `previous_metafields.json` — הערכים הישנים
- `new_metafields.json` — הערכים החדשים
- `rollback_scope.json` — הוראות לביצוע rollback

אם מתגלה כשל אחרי live — יש פקודת rollback מיידית. אין חקירה ידנית.

---

# 8. Known Anomalies Registry (רישום חריגים מוכרים)

חריגים לא נשמרים בזיכרון אנושי — הם נרשמים בקובץ רשמי.

**נתיב מוצע:** `docs/operations/known-anomalies-registry.md`
*(נתיב סופי ייקבע במיפוי הרשמי — ראה סקשן F)*

**שדות חובה לכל חריג:**

| שדה | תיאור |
|---|---|
| PID | מזהה מוצר |
| category | קטגוריה |
| why blocked | סיבת חסימה |
| affected layers | שכבות מושפעות |
| exclude rules | כלל הוצאה |
| reopen condition | תנאי לפתיחה מחדש |

כך מוצר פגוע מזוהה לא יתגלה מחדש בכל ריצה.

---

# 9. מדדי איכות (Quality Metrics)

**מדדי חובה לכל rollout:**

| מדד | תיאור |
|---|---|
| structural pass rate | אחוז עובר Gate 1 |
| semantic fail rate | אחוז נכשל Gate 2 |
| repetition score | ציון גיוון ממוצע |
| anomaly count | מספר חריגות |
| bundle admission rate | אחוז כניסה ל-bundle |
| push success rate | אחוז push מוצלח |
| post-live mismatch rate | אחוז mismatch אחרי live |
| rollback count | מספר rollbacks |
| false-success count | מספר הצלחות שקריות |

**KPI (מדד מפתח) מרכזי:**
**False Success Rate (שיעור הצלחה שקרית)** — מוצר שקיבל PASS אך פגום בלייב.

זהו הכשל שחזר משכבה 3 לשכבה 4. סף מחייב: **< 2%**.

---

# 10. מדיניות Bridge / Conductor

**מדיניות Tier מעודכנת:**

| Tier | אחריות |
|---|---|
| T2 | תיקון, rerun (הרצה חוזרת), generation |
| T2.5 לוגי | semantic audit + visual sample approval + anomaly confirmation — **שלב חובה לפני push** |
| T3 | push בלבד |

**כלל מפורש:** T3 לא בודק איכות. T3 מאשר כתיבה בלבד.
האיכות חייבת להיות מוכחת לפני הגעה ל-T3.

---

# 11. כללי אסור וחובה

## אסור — ללא יוצא מן הכלל

- לאשר closure לפני Visual QA
- לדחוף bundle בלי semantic signature
- להשתמש ב-PASS כללי אחד
- לבצע full rollout לפני pilot
- להסתמך על untracked artifacts (תוצרים לא רשומים)
- לאפשר known anomaly בתוך approved set

## חובה — ללא יוצא מן הכלל

- Truth Record קודם לכל generation
- Semantic Gate לפני bundle
- Visual Gate לפני push
- Rollback Pack לפני live
- Closure Declaration רק אחרי Live Verification

---

# 12. תוכנית ביצוע — Phases 1–4

## PHASE 1 — Emergency Hardening (עצירת דימום)

**מטרה:** לעצור כשלים פעילים לפני שממשיכים

**משימות:**
1. הקפאת Layer 5 רשמית
2. הפעלת Gates קריטיים:
   - no `(XXXX)` — אין מזהים טכניים
   - no type mismatch
   - no fabricated social proof
3. אכלוס Known Anomalies Registry
4. הגדרת Visual Gate כחובה לפני כל push

---

## PHASE 2 — Layer 4 Live Recovery (תיקון לייב)

**מטרה:** לתקן את כל המוצרים הפגועים בלייב

**משימות:**
1. תיקון לוגיקת generator
2. regenerate (יצירה מחדש) ל-241 מוצרים פגועים
3. repush ממוקד
4. live verify
5. visual verify
6. Closure Declaration של Layer 4 — רק אחרי proof (הוכחה)

---

## PHASE 3 — Architecture Hardening (הקשחת ארכיטקטורה)

**מטרה:** למנוע חזרה על הכשל
*(נפתח רק אחרי Closure Declaration של Phase 2)*

**משימות:**
1. Truth Record layer — מיושם ומחייב
2. Validation signature על כל bundle
3. Bundle admission rules
4. Rollout ladder: 8 → 20 → 50 → full
5. Rollback pack אוטומטי לפני כל push

---

## PHASE 4 — Governance Upgrade (שדרוג ממשל)

**מטרה:** שליטה ניהולית מלאה
*(נפתח רק אחרי Closure Declaration של Phase 3)*

**משימות:**
1. Closure model חדש — מוגדר ומתועד
2. metrics dashboard בסיסי
3. Known Anomalies Registry — מתוחזק שוטף
4. Release checklist קשיח — מאושר על ידי אייל

---

---

# נספחים ניהוליים

---

# A. החלטת הנהלה (Executive Decision)

## למה התוכנית נפתחת עכשיו

Layer 4 נסגר בצורה חלקית. בדיקת live גילתה שמוצרים שקיבלו סטטוס PASS מכילים:
- type mismatch בין title לטקסט
- template fingerprint שחוזר בין מוצרים
- semantic artifacts שלא סוננו בזמן אמת

הכשל אינו נקודתי — הוא מערכתי: ה-pipeline מייצר False Success.
לכן נפתחת תוכנית הקשחה מלאה.

## מה מוקפא עד סיום Phase 2

| פעילות | סטטוס |
|---|---|
| Layer 5 — כל עבודה חדשה | מוקפא |
| Full rollout של batch חדש | מוקפא |
| Push ללא Visual Gate | מוקפא |
| שינוי ב-generator ללא regression test | מוקפא |
| Closure Declaration ללא live evidence | מוקפא |

## למה אי אפשר להתקדם ל-Layer 5

Layer 5 מניח pipeline יציב של Layer 4. כרגע הוא אינו יציב.
כניסה ל-Layer 5 על pipeline פגום תיצור:
- double contamination (זיהום כפול) בנתוני אימון
- אי-יכולת לבודד כשל לשכבה ספציפית
- עלות תיקון גבוהה פי 3 לפחות

**Layer 5 לא נפתח לפני:**
Known Anomalies Registry מאוכלס **וגם** Phase 2 סגור **וגם** False Success Rate < 2%.

---

# B. תחום התוכנית (Scope)

## In Scope (בתחום)

- כל ה-generation pipeline של Layer 4
- validator, bundler, push flow, verify
- known anomalies מזוהים
- visual QA process
- rollback architecture
- release governance model
- closure criteria

## Out of Scope (מחוץ לתחום)

- Layer 5 — כולל תכנון, ניסויים, ו-POC
- Shopify admin UI ישיר
- שינויים ב-product catalog שאינם קשורים לתיאורים
- blog pipeline
- שינויי תמחור או תמונות

## Deferred (נדחה לשלב מאוחר יותר)

| פריט | נדחה ל |
|---|---|
| metrics dashboard ויזואלי | Phase 4 |
| אוטומציה מלאה של Visual QA | לאחר Phase 3 |
| Known Anomalies auto-detection | Phase 3 |

---

# C. מודל אחריות (Ownership Model)

## טבלת אחריות מלאה

| רכיב | אחראי תכנון | מבצע | מאשר מעבר | חוסם live push |
|---|---|---|---|---|
| Generator logic | אייל | Claude / orchestrator | אייל | אייל |
| Validator gates | אייל | Claude / orchestrator | אייל | שער אוטומטי |
| Bundler admission | אייל | orchestrator | אייל | שער אוטומטי |
| Push execution | orchestrator | orchestrator | T3 approval | אייל |
| Visual QA | אייל | אייל | אייל | אייל |
| Rollback execution | orchestrator | orchestrator | אייל | אייל |
| Closure declaration | אייל | — | אייל | אייל |

## כלל ברזל

**שום live push לא מתבצע ללא אישור מפורש של אייל.**
Orchestrator מכין, מייצר, ובודק — אבל לא דוחף.

---

# D. תנאי כניסה ויציאה (Phase Entry / Exit Criteria)

## PHASE 1 — Emergency Hardening

**תנאי כניסה:**
- Layer 5 מוקפא רשמית
- רשימת known anomalies קיימת (גם אם חלקית)

**תנאי יציאה:**
- Gates 1+2 פעילים ומחייבים
- Known Anomalies Registry מכיל את כל הפגועים המזוהים
- Visual Gate מוגדר כחובה לפני push

**חוסם מוחלט:**
- חסרים gates
- known anomaly ללא registry entry

---

## PHASE 2 — Layer 4 Recovery

**תנאי כניסה:**
- Phase 1 יצא רשמית
- רשימת 241 מוצרים פגועים מוכנה ומאומתת

**תנאי יציאה:**
- 241 מוצרים regenerated ועברו gates 1–4
- Visual QA בוצע על sample מייצג
- Live push בוצע ואומת
- False Success Rate < 2%

**חוסם מוחלט:**
- Visual QA לא בוצע
- מוצר מ-known anomalies נכנס ל-bundle
- False Success Rate > 2%

---

## PHASE 3 — Architecture Hardening

**תנאי כניסה:**
- Phase 2 יצא רשמית
- Rollback pack קיים ל-Layer 4

**תנאי יציאה:**
- Truth Record layer מיושם ומחייב
- Validation signature פועלת על כל bundle
- Rollout ladder מוגדר ומוטמע (8 → 20 → 50 → full)
- Rollback pack נוצר אוטומטית לפני כל push

**חוסם מוחלט:**
- Truth Record לא מחייב
- Rollback pack לא אוטומטי

---

## PHASE 4 — Governance Upgrade

**תנאי כניסה:**
- Phase 3 יצא רשמית
- לפחות Rollout Stage B (20 מוצרים) הושלם בהצלחה

**תנאי יציאה:**
- Closure model חדש מוגדר ומתועד
- Anomalies Registry מתוחזק ומעודכן
- Release checklist מאושר על ידי אייל

**חוסם מוחלט:**
- Closure model לא מאושר

---

# E. תוצרים נדרשים (Deliverables)

> **הערה:** כל הנתיבים הבאים הם **מוצעים** בהתאם לטיוטת המקור.
> הנתיבים הסופיים ייאומתו מול ה-repo האמיתי לפני ביצוע.

## PHASE 1

| תוצר | נתיב מוצע | סטטוס נדרש |
|---|---|---|
| Semantic Gate | `validators/semantic_gate` | פעיל ומחייב |
| Known Anomalies Registry | `docs/operations/known-anomalies-registry.md` | מאוכלס |
| Visual QA Checklist | `docs/operations/visual-qa-checklist.md` | מאושר |
| Layer 5 Freeze Notice | `docs/governance/layer5-freeze.md` | נחתם |

## PHASE 2

| תוצר | נתיב מוצע | סטטוס נדרש |
|---|---|---|
| Regenerated batch | `output/layer4-recovery/` | עבר gates 1–4 |
| Visual QA Report | `docs/qa/visual-qa-layer4-recovery.md` | חתום אייל |
| Live Push Log | `logs/push/layer4-recovery-push.log` | קיים |
| Live Verify Report | `docs/qa/live-verify-layer4-recovery.md` | קיים |
| Rollback Pack | `rollback/layer4-recovery/` | קיים לפני push |

## PHASE 3

| תוצר | נתיב מוצע | סטטוס נדרש |
|---|---|---|
| Truth Record Schema | `docs/schema/truth-record.md` | מאושר |
| Validation Signature spec | `docs/schema/validation-signature.md` | מאושר |
| Rollout Ladder config | `config/rollout-ladder.json` | פעיל |
| Rollback Automation | רכיב rollback לוגי | נבדק |

## PHASE 4

| תוצר | נתיב מוצע | סטטוס נדרש |
|---|---|---|
| Closure Model doc | `docs/governance/closure-model.md` | מאושר |
| Release Checklist | `docs/governance/release-checklist.md` | מאושר |
| Metrics Definition | `docs/governance/metrics-definition.md` | מאושר |

---

# F. מיפוי רכיבי מערכת (System Mapping)

## docs

| קובץ (מוצע) | תפקיד | Phase |
|---|---|---|
| `docs/operations/known-anomalies-registry.md` | רישום חריגים | 1 |
| `docs/operations/visual-qa-checklist.md` | תהליך Visual QA | 1 |
| `docs/governance/layer5-freeze.md` | הקפאת Layer 5 | 1 |
| `docs/governance/closure-model.md` | הגדרת סגירה | 4 |
| `docs/governance/release-checklist.md` | רשימת שחרור | 4 |
| `docs/schema/truth-record.md` | סכמת Truth Record | 3 |

## bridge / conductor

- `00-team-lead/orchestrator.py` — נקודת הכניסה **היחידה** לכל הרצה
- מפעיל stages, מנהל gate checks, מדווח סטטוס
- **אינו** מבצע push ללא אישור T3

## שמות לוגיים של רכיבים

> **הערה חשובה:** השמות הבאים הם **שמות לוגיים/תפקודיים**.
> הם אינם שמות קבצים סופיים.
> המיפוי הסופי לקבצים האמיתיים ב-repo יתבצע בתוכנית הביצוע בלבד.

| שם לוגי | תפקיד |
|---|---|
| generator | יצירת טקסט מוצר |
| structure-gate | Gate 1 — בדיקת מבנה |
| semantic-gate | Gate 2 — בדיקת משמעות |
| repetition-gate | Gate 3 — בדיקת חזרות |
| release-gate | Gate 4 — שער שחרור |
| bundler | אסיפת bundle אחרי gates |
| push | דחיפה ל-Shopify |
| verify | אימות קריאה חזרה |
| rollback | ביצוע rollback |

## output (תיקיות פלט — מוצע)

| תיקייה | תוכן |
|---|---|
| `output/generated/` | טקסטים שנוצרו |
| `output/validated/` | טקסטים שעברו gates |
| `output/bundle/` | bundle מוכן לפוש |
| `output/rejected/` | מוצרים שנדחו + סיבה |
| `rollback/` | חבילות rollback לפי push_id |

## validators — מבנה gate_result

כל gate מייצר קובץ תוצאה עם:
- `status`: PASS / FAIL
- `gate_name`
- `product_id`
- `fail_reason` (אם נכשל)
- `timestamp`

## bundler

- מקבל רק מוצרים עם gate_result PASS על כל 4 gates
- מייצר bundle_manifest עם רשימת מוצרים מאושרים
- מצרף validation_signature לכל bundle
- דוחה כל מוצר שמופיע ב-Known Anomalies Registry

## push flow — סדר מחייב

1. rollback pack נוצר
2. bundle_manifest מאושר על ידי T3
3. push מתבצע
4. verify מאמת קריאה חזרה
5. visual QA מבוצע
6. סטטוס מתעדכן ל-LIVE-VERIFIED

---

# G. מפרט שערים קשיחים (Hard Gates Spec)

## Gate 1 — Structure Gate

| שדה | ערך |
|---|---|
| Gate Name | structure-gate |
| Failure Condition | שדה חסר / כפול / JSON לא תקין / פורמט שגוי |
| Blocking Behavior | מוצר נשמר ב-rejected עם סיבה. לא עובר לשלב הבא |
| Required Evidence | gate1_result עם status=PASS לכל מוצר ב-bundle |

## Gate 2 — Semantic Gate

| שדה | ערך |
|---|---|
| Gate Name | semantic-gate |
| Failure Condition | type mismatch / מזהה טכני בטקסט / social proof לא מבוסס / bleed מתיאור קודם |
| Blocking Behavior | מוצר לא נכנס ל-bundle. מקרה קיצוני: כל ה-batch נעצר לבדיקה |
| Required Evidence | gate2_result + semantic_signature על כל מוצר |

## Gate 3 — Repetition Gate

| שדה | ערך |
|---|---|
| Gate Name | repetition-gate |
| Failure Condition | variation score מתחת לסף / פתיחה חוזרת ב-3 מוצרים רצופים / template fingerprint |
| Blocking Behavior | מוצרים פוגעים נדחים. אם >10% מה-batch נכשל — כל ה-batch נעצר |
| Required Evidence | gate3_result + variation_score לכל מוצר |

## Gate 4 — Release Gate

| שדה | ערך |
|---|---|
| Gate Name | release-gate |
| Failure Condition | כל אחד מ-gates 1–3 לא עבר / risk review לא בוצע / visual QA לא אושר |
| Blocking Behavior | bundle לא נוצר. push לא מתאפשר בשום תנאי |
| Required Evidence | gate4_result עם חתימה על כל 4 gates + visual_qa_approved=true |

---

# H. ממשל שחרור (Release Governance)

| שלב | Tier נדרש | Visual Review חובה | אישור אייל חובה | Auto-Progress מותר |
|---|---|---|---|---|
| Generation | T1 | לא | לא | כן |
| Gates 1–3 | T1 | לא | לא | כן |
| Gate 4 / Release Gate | T2 | **כן** | **כן** | **לא** |
| Bundle creation | T2 | לא | לא | כן |
| Push execution | **T3** | **כן** | **כן** | **לא** |
| Live Verify | T2 | לא | לא | כן |
| Closure Declaration | **T3** | **כן** | **כן** | **לא** |
| Layer 5 Entry | **T3+** | **כן** | **כן** | **לא** |

**כלל ממשל:** כל שלב עם "Auto-Progress לא" — דורש הודעה מפורשת מאייל לפני המשך. Orchestrator ממתין ולא מניח אישור.

---

# I. מדיניות סגירה (Closure Policy)

Phase נחשב **סגור** רק כשמתקיימים **שלושת** התנאים הבאים יחד:

## 1. Technically Complete (הושלם טכנית)

- כל המשימות המוגדרות רוצו
- כל ה-deliverables קיימים בנתיביהם
- אין שגיאות פתוחות ב-gate logs

## 2. Quality Verified (איכות מאומתת)

- False Success Rate < 2%
- Semantic Gate pass rate > 98%
- Repetition Gate: אפס fingerprints מזוהים ב-sample
- Visual QA בוצע על sample מלא ואושר על ידי אייל

## 3. Production Safe (בטוח לייצור)

- Rollback Pack קיים ומוכן
- Live Verify אישר קריאה חזרה תקינה
- אייל חתם על Closure Declaration

**אין Closure בלי שלושת התנאים גם יחד — ללא יוצא מן הכלל.**

---

# J. סדר עדיפויות לביצוע (Priority Order)

## ראשון

1. **הקפאת Layer 5** — תנאי מוקדם לכל דבר
2. **אכלוס Known Anomalies Registry** — לפני כל generation חדש
3. **הפעלת Semantic Gate** — לפני כל push

## שני

4. **הגדרת Visual QA כ-release gate** — לפני כל push
5. **הכנת Rollback Pack ל-Layer 4 הקיים** — לפני Phase 2
6. **בניית רשימת 241 מוצרים פגועים** — לפני regeneration

## שלישי

7. **Regeneration של 241** — רק אחרי gates 1–4 פעילים
8. **Rollout Stage A (8 מוצרים)** — לפני כל batch גדול
9. **Visual QA על Stage A** — לפני Stage B

## טבלת תנאי מוקדמים

| פעולה | לא מתחילה לפני |
|---|---|
| Regeneration | Gates 1–4 פעילים + Registry מאוכלס |
| Push | Visual QA approved + Rollback Pack + T3 approval |
| Stage B (20) | Stage A אומת בלייב |
| Stage C (50) | Stage B אומת בלייב |
| Full Rollout | Stage C אומת + False Success Rate < 2% |
| Phase 3 | Phase 2 Closure Declaration חתום |
| Phase 4 | Phase 3 Closure Declaration חתום |
| Layer 5 | Phase 4 Closure Declaration חתום + False Success Rate < 2% לאורך זמן |

---

# K. קיים מול מתוכנן (Existing vs Planned)

> **כלל:** אסור לתכנן שינוי ברכיב קיים לפני שמאמתים את מצבו בפועל.
> עמודת "קיים בפועל" מבוססת על מה שידוע בתאריך המסמך — **חייבת אימות לפני ביצוע**.

| רכיב | קיים בפועל | מתוכנן |
|---|---|---|
| generator | כן | שדרוג type inference |
| Gate 1 — Structure | כן (חלקי) | הרחבה ל-missing/duplicate מלא |
| Gate 2 — Semantic | **לא** | ליצור מאפס |
| Gate 3 — Repetition | **לא** | ליצור מאפס |
| Gate 4 — Release | **לא** | ליצור מאפס |
| bundler | כן | הוספת admission rules |
| push | כן | הוספת rollback pack אוטומטי |
| verify | כן | ללא שינוי בשלב זה |
| rollback | **לא** | ליצור מאפס |
| Known Anomalies Registry | **לא** | Phase 1 |
| Visual QA Checklist | **לא** | Phase 1 |
| Truth Record layer | **לא** | Phase 3 |
| Validation Signature | **לא** | Phase 3 |
| Rollout Ladder | **לא** | Phase 3 |
| Closure Model doc | **לא** | Phase 4 |
| Bridge / orchestrator | כן | ללא שינוי — כל hardening משתלב בו |

---

# L. איסור ארכיטקטורה חדשה ללא אישור

## כלל מחייב

**אסור** ליצור — ללא אישור מפורש של אייל:
- עץ תיקיות חדש
- flow חדש שאינו קיים כרגע
- runtime (סביבת הרצה) מקביל לזה הקיים
- layer ארכיטקטוני חדש

## ברירת המחדל — מתלבשים על הקיים

לפני כל שינוי: **מתלבשים על המערכת הקיימת, לא מחליפים אותה.**

- gate חדש נכנס לתוך ה-pipeline הקיים, לא לצדו
- validator חדש נרשם אצל ה-orchestrator הקיים, לא מופעל ישירות
- קובץ חדש נוצר רק אם אין קובץ קיים שיכול לשאת את הפונקציה

---

# M. שילוב ב-Runtime הקיים (Existing Runtime Integration)

## מסלול הפעלה רשמי יחיד

```
bridge / conductor / team_lead / watchdog → orchestrator
```

**אסור:**
- להפעיל סקריפטים ישירות מחוץ ל-orchestrator
- לבנות runtime מקביל
- לעקוף את ה-orchestrator בכל דרך

## כל hardening משתלב — לא עוקף

- gate חדש → נרשם כ-stage ב-orchestrator
- validator חדש → מופעל דרך ה-pipeline הקיים
- rollback → מופעל דרך ה-orchestrator בלבד
- push → מופעל דרך ה-orchestrator בלבד, עם T3 approval

**עיקרון:** אם hardening לא ניתן להשתלב ב-runtime הקיים — זו אינדיקציה שהוא דורש בחינה מחדש, לא runtime חדש.

---

# N. קודם תיקון, אחר כך הקשחה (Recovery First, Hardening Second)

## הבחנה מחייבת בין סוגי עבודה

| Phase | סוג עבודה | מה כלול |
|---|---|---|
| Phase 1 | Emergency Hardening | gates קריטיים בלבד, ללא ארכיטקטורה |
| Phase 2 | Live Recovery | תיקון 241 פגועים, push, verify |
| Phase 3 | Architecture Hardening | רק אחרי Phase 2 סגור |
| Phase 4 | Governance | רק אחרי Phase 3 סגור |

## כלל מחייב

**אסור** לערבב recovery (שחזור) עם architecture hardening (הקשחת ארכיטקטורה) באותה משימת ביצוע.

**למה:** ערבוב יוצר תלויות שמאטות את התיקון הדחוף, מקשה על בידוד כשלים, ומסכן את לוח הזמנים של Layer 4 live correction.

**Phase 3 לא נפתח בשום צורה לפני Closure Declaration של Phase 2.**

---

# O. מדיניות יצירת קבצים (File Creation Policy)

## 4 כללים מחייבים לכל קובץ חדש

**1. חייב להיות מנומק (justified)**
הצהרה מפורשת: "קובץ זה נוצר כי ___ ואין קובץ קיים שיכול לשאת פונקציה זו."

**2. חייב להופיע בטבלת Deliverables**
קובץ שאינו מופיע בסקשן E — לא נוצר.

**3. חייב להיות ממופה ב-System Mapping**
קובץ שאינו מופיע בסקשן F — לא נוצר.

**4. אין placeholder files (קבצי מקום-שמור)**
אסור: קבצים ריקים, תוכן זמני, קבצים "לטובת העתיד" ללא צורך ביצועי אמיתי ומיידי.

## Self-Check לפני יצירת קובץ

לפני כל יצירת קובץ חדש, לבדוק:
- האם הקובץ כבר קיים?
- האם קובץ קיים יכול לשאת את הצורך?
- האם הקובץ מופיע ב-Deliverables?
- האם הקובץ מופיע ב-System Mapping?
- האם יש צורך ביצועי אמיתי עכשיו?

**אם תשובה אחת היא "לא" — לא יוצרים.**

---

*AUTOMATION-HARDENING-PLAN v1 — BabyMania Layer 4 — 2026-04-19*
*מסמך Source of Truth ניהולי — אין לשנות ללא T3 approval*

STATUS: OFFICIAL V1 — READY FOR PHASE DECOMPOSITION
