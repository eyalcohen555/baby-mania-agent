# Layer 6 — Phase 4 Dry Run Report
**תאריך:** 2026-05-03  
**סה"כ מוצרים:** 59 | **DRY RUN ONLY — אין כתיבה ל-Shopify**

---

## 1. תוצאות כלליות

| מדד | ערך |
|---|---|
| PASS (כל 8 gates) | 30/59 |
| NEEDS_REVIEW | 29/59 |
| BLOCKED | 0/59 |
| ממוצע quality score | 77.7 |
| % PASS+NEEDS_REVIEW | 100.0% |
| % BLOCKED | 0.0% |

### התפלגות לפי קבוצה

| קבוצה | מוצרים |
|---|---|
| clothing_yaml | 20 |
| shoes_yaml | 15 |
| reborn_toys | 9 |
| yaml_gap | 10 |
| edge_cases | 5 |

---

## 2. תוצאות Gates (8 שערים)

| Gate | כשלונות |
|---|---|
| SOURCE_EXISTS | 0/59 |
| FORMAT_VALID | 0/59 |
| ALLOWED_VALUE | 0/59 |
| SOURCE_TRACEABLE | 0/59 |
| NO_FORBIDDEN_INFERENCE | 0/59 |
| CATEGORY_COVERAGE | 26/59 |
| DUPLICATE_CONFLICT | 0/59 |
| QUALITY_SCORE | 17/59 |

---

## 3. בעיות מיוחדות

| בעיה | כמות |
|---|---|
| RANGE_TOO_BROAD (גיל נחסם) | 4 |
| NO_AGE_FOUND (אין מקור גיל) | 31 |
| DOLL_NO_AGE_APPLICABLE | 9 |
| Multi-age (מוצר עם >1 טווחי גיל) | 0 |
| YAML_GAP (ללא YAML) | 18 |

---

## 4. 10 דוגמאות טובות (PASS)

**9688932909369** — אוברול אריה חמוד דגם שמר  
Tags: `type-romper, age-2-3y, season-unknown, occ-everyday, gender-boy, style-casual` | Score: 86.4  

**9678573240633** — אוברול אריה מתוק דגם שמר  
Tags: `type-romper, age-newborn, season-unknown, occ-everyday, gender-boy` | Score: 79.6  

**10005779808569** — אוברול בייבי מניה דגם חן  
Tags: `type-romper, season-winter, fabric-cotton, occ-everyday, gender-girl, style-modern` | Score: 81.5  

**9874906349881** — אוברול ג'ינס מתוק מבית בייבי מניה דגם זוהר  
Tags: `type-romper, age-newborn, season-summer, fabric-denim, occ-everyday, gender-girl` | Score: 96.6  

**9688660312377** — אוברול ג׳ינס דגם אתי  
Tags: `type-romper, age-2-3y, season-spring-fall, fabric-denim, occ-everyday, gender-girl` | Score: 96.2  

**9895864205625** — אוברול ג’ינס יוניסקס לתינוקות דגם שלו  
Tags: `type-romper, age-2-3y, season-unknown, fabric-denim, occ-everyday, gender-boy` | Score: 93.8  

**9688965087545** — אוברול דוב מתוק דגם אייל  
Tags: `type-romper, age-2-3y, season-unknown, occ-everyday, gender-boy` | Score: 79.2  

**9717957525817** — אוברול דובי דגם דניאל  
Tags: `type-romper, season-spring-fall, occ-everyday, gender-girl, style-teddy` | Score: 74.7  

**10005779841337** — אוברול חורפי לתינוקות דגם אנגל  
Tags: `type-romper, season-winter, fabric-cotton, occ-everyday, gender-girl, style-european` | Score: 81.2  

**9687579033913** — אוברול לבבות דגם הילה  
Tags: `type-romper, age-2-3y, season-winter, fabric-cotton, occ-everyday, gender-girl` | Score: 89.7  

---

## 5. 10 דוגמאות בעייתיות (NEEDS_REVIEW / BLOCKED)

**9688934940985** — אוברול בייבי  לתינוק – Baby Bear Cozy Set — `NEEDS_REVIEW`  
Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE | Score: 59.1 | Notes: NO_AGE_FOUND  

**10026520445241** — אוברול בייבי מניה דגם חן — `NEEDS_REVIEW`  
Failed gates: CATEGORY_COVERAGE | Score: 78.8 | Notes: NO_AGE_FOUND  

**9858268430649** — אוברול גינס מהמם דגם רוית — `NEEDS_REVIEW`  
Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE | Score: 74.6 | Notes: NO_AGE_FOUND  

**9179176141113** — אוברול דובונים מכותנה - ליאור — `NEEDS_REVIEW`  
Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE | Score: 59.1 | Notes: NO_AGE_FOUND  

**9719189635385** — אוברול דובי אם רגלית דגם אוריאל — `NEEDS_REVIEW`  
Failed gates: CATEGORY_COVERAGE | Score: 78.8 | Notes: NO_AGE_FOUND  

**9864947827001** — אוברול חגיגי דגם אנה — `NEEDS_REVIEW`  
Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE | Score: 74.8 | Notes: NO_AGE_FOUND  

**9179161231673** — אוברול כותנה קיצי - נועה — `NEEDS_REVIEW`  
Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE | Score: 67.9 | Notes: NO_AGE_FOUND  

**9096607138105** — אוברול מכופתרת — `NEEDS_REVIEW`  
Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE | Score: 72.4 | Notes: NO_AGE_FOUND  

**9179137933625** — אוברול מתוק מכותנה מלאה ללא כתפיות - נויה — `NEEDS_REVIEW`  
Failed gates: CATEGORY_COVERAGE, QUALITY_SCORE | Score: 59.2 | Notes: NO_AGE_FOUND  

**9607363232057** — נעל הלו קיטי עם אורות לילדות — `NEEDS_REVIEW`  
Failed gates: CATEGORY_COVERAGE | Score: 82.4 | Notes: NO_AGE_FOUND  

---

## 6. תנאי PASS ל-Phase 4

| תנאי | סטטוס |
|---|---|
| אין Shopify live | YES |
| אין gender-unisex / type-doll | YES |
| אין default_unisex / fallback source | YES |
| אין גיל מטעה מטווח רחב | YES |
| Native tags באנגלית בלבד | YES |
| Avg quality score >= 75 | YES (77.7) |
| >= 70% PASS+NEEDS_REVIEW | YES (100.0%) |
| BLOCKED <= 20% | YES (0.0%) |

---

## 7. מה צריך לתקן לפני Phase 5

1. **CATEGORY_COVERAGE failures** — מוצרים ללא CAT-A/C/F: לבדוק ידנית
2. **RANGE_TOO_BROAD** (4 מוצרים) — להחליט: age-unknown fallback / manual split / multi-tag
3. **NO_AGE_FOUND** (31 מוצרים) — להעשיר YAML או לאשר age-unknown
4. **YAML_GAP** (18 מוצרים) — שיפור coverage יוריד NEEDS_REVIEW משמעותית

---

## 8. האם Phase 4 מספיק לבדיקה אנושית?

**YES** — כל תנאי Phase 4 מתקיימים. Phase 5 Human Review יכול להתחיל.
