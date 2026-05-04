# Layer 6 — Phase 5f Logic Hardening Report
**תאריך:** 2026-05-04
**Phase:** 5f — Tagger Logic Hardening + Dry Run Revalidation
**DRY RUN ONLY — אין כתיבה ל-Shopify**

---

## 1. סיכום Phase 5f

Phase 5e Candidate Safety Audit (2026-05-04) חשף 7 באגים בלוגיקת הטאגר.
Phase 5f מתקנת את כל 7 הבאגים ומריצה dry-run על אותו sample.

| מדד | Phase 5d | Phase 5f | שינוי |
|---|---|---|---|
| Products tested | 59 | 58 | -1 (*) |
| PASS | 30 (50.8%) | 23 (39.7%) | -7 |
| NEEDS_REVIEW | 29 | 35 | +6 |
| BLOCKED | 0 | 0 | 0 |
| avg quality score | 82.3 | 80.6 | -1.7 |
| RANGE_TOO_BROAD | 4 | 5 | +1 |
| NO_AGE_FOUND | 32 | 41 | +9 |
| DOLL_NO_AGE_APPLICABLE | 8 | 6 | -2 |
| Phase5b exempt (swim-ring) | 0 | 1 | +1 |
| type-sleep-soother | 1 | 1 | 0 |

(*) Sample -1: thermometer product correctly moved from reborn_toys → yaml_gap; yaml_gap at cap.

**הסבר הירידה ב-PASS:** מכוונת — 7 מוצרים שעברו PASS עם age confidence=0.75 (מתחת ל-0.85) עכשיו NEEDS_REVIEW+NO_AGE_FOUND. מוצרים אלה היו UNSAFE_FOR_PHASE6 לפי Phase 5e.

---

## 2. שבעת הבאגים שתוקנו

### Bug 1 — Heuristic Confidence Below Threshold

**קובץ:** `run_layer6_phase5d_rerun.py` — `extract_cat_b()`
**בעיה:** `first_walker_heuristic` ו-`toddler_heuristic` החזירו age tag עם confidence=0.75 (מינימום: 0.85).

**לפני:**
```python
return [_tag("age-6-12m", "CAT-B", 0.75, "handle", "first_walker_heuristic")], "OK", ""
return [_tag("age-2-3y",  "CAT-B", 0.75, "handle", "toddler_heuristic")],      "OK", ""
```
**אחרי:** שניהם מחזירים `[], "NO_AGE_FOUND", "..._below_threshold"`

**השפעה:** C1,C3,C4,C5,C6,C8 — ירדו מ-PASS ל-NEEDS_REVIEW.

---

### Bug 2 — No Handle Age Conflict Detection

**קובץ:** `run_layer6_phase5d_rerun.py` — `extract_cat_b()`
**בעיה:** לפני הפעלת heuristic לא בוצעה בדיקת conflict בין heuristic לsignals סותרים.

**אחרי:**
```python
if re.search(r"\bfirst[\s\-]walker\b", combined, re.IGNORECASE):
    conflict = any(et.lower() in ("newborn-clothing", "newborn") for et in tags_list) or \
               re.search(r"\bnewborn\b|\b0[\s\-]3m\b|\binfant\b", combined, re.IGNORECASE)
    if conflict:
        return [], "NO_AGE_FOUND", "first_walker_conflict"
```

**השפעה:** C6 (9615375565113) — first_walker + existing tag "newborn-clothing" → `first_walker_conflict`.

---

### Bug 3 — RANGE_TOO_BROAD Bypass ("0-to-3-years-old")

**קבצים:** `run_layer6_phase5d_rerun.py`, `layer6_validate_tags.py` — `WIDE_RANGE_PATS`
**בעיה:** handle "0-to-3-years-old" לא היה מזוהה. pattern קיים דורש suffix `y`/`year` ללא `-old`.

**אחרי (pattern חדש הוסף לפני הקיים):**
```python
(r"\b0[\s\-]+to[\s\-]+[2-9][\s\-]years?(?:[\s\-]old)?\b", "0-to-Xy"),
```

**השפעה:** C7 (9606764462393) → RANGE_TOO_BROAD:0-to-Xy. Age blocked.

---

### Bug 4 — Gender Priority and Missing יוניסקס

**קובץ:** `run_layer6_phase5d_rerun.py` — `extract_cat_f()`
**בעיות:** (a) "יוניסקס" לא היה ב-neutral pattern. (b) title לא היה בעדיפות על handle. (c) boys+girls combo → gender-girl שגוי.

**אחרי:**
- "יוניסקס" הוסף ל-`NEUTRAL_PAT`
- title בודק ראשון, handle שני
- boys+girls combo בכל text → gender-neutral

**השפעה:** C4 (9895864205625) — title "יוניסקס" → gender-neutral במקום gender-boy. ✅

---

### Bug 5 — Type Specificity After existing_tag Match

**קובץ:** `run_layer6_phase5d_rerun.py` — `extract_cat_a()`
**בעיה:** existing_tag "baby-shoes" → type-shoes מיד, ללא בדיקת handle לkeyword ספציפי יותר.

**אחרי:** `GENERIC_SHOE_OVERRIDES` — אם existing_tag="baby-shoes" + handle מכיל "sneaker/sandal/boot" → type ספציפי יותר עם confidence גבוה יותר.

**השפעה:** C8 (9606764298553) → type-sneakers במקום type-shoes. ✅

---

### Bug 6 — Wrong Source Labels (title vs handle)

**קובץ:** `run_layer6_phase5d_rerun.py` — `extract_cat_c()`, `extract_cat_d()`
**בעיה:** בדיקת source Season/Fabric חיפשה ב-`(title + " " + handle)` ודיווחה "title" — גם כשה-keyword ב-handle.

**אחרי:** בדיקה נפרדת לכל שדה:
```python
src = "title" if re.search(pat, title.lower()) else ("handle" if re.search(pat, handle.lower()) else "existing_tag")
```

**השפעה:** source attribution מדויק — שיפור ב-gate G4 עבור auditor.

---

### Bug 7 — Swimming Ring Misclassified as reborn_toys

**קובץ:** `run_layer6_phase5d_rerun.py` — `classify_product()`, `tag_product()`
**בעיות:**
- 7a: "float"/"swimming-ring" → reborn_toys (שגוי)
- 7b: product_group="reborn_toys" → is_reborn=True → DOLL_NO_AGE_APPLICABLE (שגוי)

**אחרי:**
- `is_swim_accessory` — group נפרד "accessories"
- word-boundary `\bfloat\b` (לא "floating")
- `NON_AGE_TYPES` includes "type-swimming-ring" → Phase5b exempt

**השפעה:** C9 (9838580662585) → group=accessories, catb_exempt=Phase5b:type-swimming-ring. ✅

---

## 3. בדיקה מחדש של 9 Phase 6 Candidates

| # | product_id | Phase 5d | Phase 5f | Bugs fixed |
|---|---|---|---|---|
| C1 | 9688932909369 | PASS age-2-3y | NEEDS_REVIEW NO_AGE_FOUND | 1 |
| C2 | 9874906349881 | PASS age-newborn | PASS age-newborn | — |
| C3 | 9688660312377 | PASS age-2-3y | NEEDS_REVIEW NO_AGE_FOUND | 1 |
| C4 | 9895864205625 | PASS age-2-3y gender-boy | NEEDS_REVIEW NO_AGE_FOUND gender-neutral | 1+4 |
| C5 | 9687579033913 | PASS age-2-3y | NEEDS_REVIEW NO_AGE_FOUND | 1 |
| C6 | 9615375565113 | PASS age-6-12m | NEEDS_REVIEW NO_AGE_FOUND | 1+2 |
| C7 | 9606764462393 | PASS age-2-3y | PASS RANGE_TOO_BROAD | 3 |
| C8 | 9606764298553 | PASS age-2-3y type-shoes | NEEDS_REVIEW NO_AGE_FOUND type-sneakers | 1+5 |
| C9 | 9838580662585 | PASS DOLL_NO_AGE_APP | PASS Phase5b:type-swimming-ring | 7 |

**Phase 6 verdict after Phase 5f:**
- **SAFE:** C2 בלבד (1/9) — YAML age source, score 96.5. לא מספיק ל-batch.
- **NEEDS_REVIEW:** C1,C3,C4,C5,C6,C8 — דורשים age source ידני.
- **BLOCKED_AGE:** C7 — 0-to-3-years-old חסום.
- **EXEMPT:** C9 — Phase5b:type-swimming-ring, תקין.

**PHASE6_STILL_BLOCKED** — נדרש ≥5 SAFE candidates + T3 approval.

---

## 4. Gates Summary

| Gate | Phase 5d | Phase 5f | שינוי |
|---|---|---|---|
| CATEGORY_COVERAGE fails | 26/59 | 33/58 | +7 |
| QUALITY_SCORE fails | 17/59 | 19/58 | +2 |
| כל שאר | 0/59 | 0/58 | 0 |

---

## 5. Phase 5f Pass Criteria

| תנאי | סטטוס |
|---|---|
| no_shopify_live | ✅ |
| no_forbidden_tags | ✅ |
| no_type_reborn_on_sleep_soother | ✅ |
| no_wide_range_bypass | ✅ |
| heuristics_below_threshold_blocked | ✅ |
| gender_title_priority_enforced | ✅ |
| swimming_ring_correct_exempt | ✅ |
| avg_score_gte_75 | ✅ (80.6) |
| blocked_pct_lt_20 | ✅ (0.0%) |

---

## 6. הצעד הבא המומלץ

1. **Human review** — age source ידני ל-6 clothing/shoes candidates.
2. **Phase 5g** — לאחר שיש ≥5 candidates עם age source מהימן.
3. **T3 approval (אייל)** — נדרש לפני Phase 6 live.
4. **Phase 6 NOT OPEN** — Shopify live: NO.

---

*Phase 5f — DRY RUN ONLY. אין שינויים ב-Shopify.*
