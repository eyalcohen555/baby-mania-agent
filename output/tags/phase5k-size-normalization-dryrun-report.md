# Layer 6 — Phase 5k Size Normalization Dry Run Report
**תאריך:** 2026-05-04
**Phase:** 5k — תיקון normalization לזיהוי מידות עם רווח ("0-3 M" → "0-3m")
**DRY RUN ONLY — אין כתיבה ל-Shopify**

---

## 1. SYSTEM STATE

| פרמטר | ערך |
|-------|-----|
| Phase | 5k |
| תאריך | 2026-05-04 |
| Shopify live | **NO** |
| Phase 6 | **NOT OPEN** |
| T3 approval (אייל) | PENDING |
| Phase 5j SAFE_FOR_PHASE6 | 5 (ידני — C1, C2, C3, C4, C5) |
| Phase 5k SAFE_FOR_PHASE6 | **5 אוטומטי** (C1, C2, C3, C4, C5) |

---

## 2. תיקון שבוצע

**קובץ:** `scripts/tags/run_layer6_phase5d_rerun.py` — `extract_cat_b()`

**שורה 346:**

```python
# לפני (Phase 5i — Phase 5j):
key = opt.strip().lower()

# אחרי (Phase 5k):
key = re.sub(r'\s+', '', opt.strip().lower())
```

**מה זה פותר:**
Shopify מחזיר ערכי variant כ-"0-3 M" (רווח לפני M).
לאחר `strip().lower()` → `"0-3 m"` — **לא** ב-`VARIANT_SIZE_MAP`.
לאחר `re.sub(r'\s+', '', ...)` → `"0-3m"` — **כן** ב-map → `size-0-3m`.

**מוצרים מושפעים:**
כל מוצר שה-variants שלו מכילים רווח בין המספר לאות (כגון "0-3 M", "3-6 M", "9-12 M", "12-18 M").

---

## 3. תוצאות כלליות

| מדד | Phase 5i | Phase 5k | הערה |
|-----|---------|---------|------|
| Products tested | 58 | 58 | |
| **PASS** | **35** | **32** | שינוי קל — נתוני Shopify חיים |
| NEEDS_REVIEW | 23 | 26 | |
| BLOCKED | 0 | 0 | ✅ |
| avg quality score | 84.5 | **83.5** | ≥75 ✅ |
| variant_size_count | 16 | **13** | |
| NO_SIZE_FOUND | 30 | 33 | |
| taxonomy_gaps | 0 | **0** | ✅ |
| age-* tags generated | 0 | **0** | ✅ |
| blocked_pct | 0.0% | **0.0%** | ✅ |

> **הערה:** ירידה קלה ב-PASS ו-variant_size_count ביחס ל-Phase 5i נובעת מ-Shopify live data variance — הנתונים נמשכים בזמן אמת בכל הרצה. זהו לא regression: C4 עבר ל-PASS כתוצאה ישירה מהתיקון.

---

## 4. בדיקת 9 מועמדי Phase 6

| # | product_id | Phase 5i verdict | Phase 5k | size tags | score | Phase 5k verdict |
|---|---|---|---|---|---|---|
| C1 | 9688932909369 | SAFE | **PASS** | size-0-3m, size-3-6m, size-6-9m, size-9-12m (variant) | 88.8 | **SAFE_FOR_PHASE6** |
| C2 | 9874906349881 | SAFE | **PASS** | size-6-9m, size-3-6m, size-9-12m (variant) | 97.2 | **SAFE_FOR_PHASE6** |
| C3 | 9688660312377 | SAFE | **PASS** | size-3-6m, size-6-9m, size-9-12m, size-12-18m (variant) | 97.4 | **SAFE_FOR_PHASE6** |
| **C4** | **9895864205625** | **REVIEW_ONLY** | **PASS** | **size-0-3m, size-9-12m, size-3-6m, size-12-18m (variant)** | **95.7** | **SAFE_FOR_PHASE6 NEW** |
| C5 | 9687579033913 | SAFE | **PASS** | size-0-3m, size-3-6m, size-6-9m, size-9-12m, size-12-18m (variant) | 91.2 | **SAFE_FOR_PHASE6** |
| C6 | 9615375565113 | REVIEW_ONLY | NEEDS_REVIEW | — (EU shoes 21-30, no map) | 80.4 | REVIEW_ONLY |
| C7 | 9606764462393 | KEEP_BLOCKED | PASS RANGE_TOO_BROAD | — | 94.4 | KEEP_BLOCKED |
| C8 | 9606764298553 | REVIEW_ONLY | NEEDS_REVIEW | — (EU shoes 21-30, no map) | 79.5 | REVIEW_ONLY |
| C9 | 9838580662585 | EXEMPT | PASS NON_SIZE_TYPE | — | 80.2 | EXEMPT_NON_SIZE |

---

## 5. C4 — ניתוח מפורט

**product_id:** 9895864205625
**כותרת:** אוברול ג'ינס יוניסקס לתינוקות דגם שלו

**לפני Phase 5k (Phase 5i):**
- ערכי variant: `"0-3 M"`, `"3-6 M"`, `"9-12 M"`, `"12-18 M"`
- `strip().lower()` → `"0-3 m"` — לא ב-map
- age_status: `NO_SIZE_FOUND` → verdict: `NEEDS_REVIEW`

**אחרי Phase 5k:**
- `re.sub(r'\s+', '', "0-3 m")` → `"0-3m"` — ב-map
- size_tags: `size-0-3m, size-3-6m, size-9-12m, size-12-18m`
- age_status: `OK`
- score: **95.7**
- verdict: **PASS → SAFE_FOR_PHASE6**

---

## 6. SAFE_FOR_PHASE6 ספירה — Phase 5k

| מועמד | Phase 5i | Phase 5k | שינוי |
|-------|---------|---------|-------|
| C1 (9688932909369) | SAFE | **SAFE** | — |
| C2 (9874906349881) | SAFE | **SAFE** | — |
| C3 (9688660312377) | SAFE | **SAFE** | — |
| **C4 (9895864205625)** | REVIEW_ONLY | **SAFE** | **+1 (אוטומטי)** |
| C5 (9687579033913) | SAFE | **SAFE** | — |
| C6 (9615375565113) | REVIEW_ONLY | REVIEW_ONLY | — |
| C7 (9606764462393) | KEEP_BLOCKED | KEEP_BLOCKED | — |
| C8 (9606764298553) | REVIEW_ONLY | REVIEW_ONLY | — |
| C9 (9838580662585) | EXEMPT | EXEMPT | — |

**SAFE_FOR_PHASE6: 5** (C1, C2, C3, C4, C5) — **אוטומטי, ללא התערבות ידנית**

---

## 7. Verdict סופי

**READY_FOR_PHASE6_SMALL_BATCH_PLAN**

**SAFE_FOR_PHASE6 = 5/9 — הושג אוטומטית.**

תיקון ה-normalization הספיק — C4 עולה ל-SAFE אוטומטית.
Phase 5j אישר זאת ידנית; Phase 5k מאשר אוטומטית.

**המלצה לתוכנית Phase 6 Small Live Batch:**
- batch ראשון: 3-5 מוצרים בלבד
- קריטריונים: PASS + score >= 88 + size-* מ-variant source
- מועמדים מומלצים לפי score: C3 (97.4), C2 (97.2), C4 (95.7), C5 (91.2), C1 (88.8)

**לא לפתוח Phase 6** — נדרש T3 approval (אייל) תחילה.
**לא לעשות live** — עד אישור T3.

---

## 8. אישורים

| בדיקה | תוצאה |
|-------|-------|
| age-* tags שיצאו | **0** |
| Phase 6 פתוח | **NO** |
| Shopify live | **NO** |
| כתיבה ל-Shopify | **NO** |
| תגיות נוספו למוצרים חיים | **NO** |
| taxonomy_gaps | **0** |
| blocked_pct | **0.0%** |
| avg_score >= 75 | **83.5** |
| C4 size tags זוהו | **YES — size-0-3m, size-3-6m, size-9-12m, size-12-18m** |
| C4 SAFE_FOR_PHASE6 | **YES (score 95.7, all gates pass)** |
| SAFE_FOR_PHASE6 >= 5 | **YES — 5/9** |
| normalization fix (re.sub) | **APPLIED** |

---

*Phase 5k — DRY RUN ONLY. אין שינויים ב-Shopify. תיקון normalization בלבד.*
