# Pre-Phase-1 Tag Cleanup — Dry-Run Report
## Layer 6 | Date: 2026-05-03 | Status: DRY-RUN ONLY — לא בוצע שינוי

---

## תיקון קריטי לגבי CL-2

> **Phase 0 audit report טעה.** תגיות שנראו "garbled" בטרמינל (`������`, `12-18 ????`) הן עברית תקינה לחלוטין.
> הבעיה הייתה encoding של הטרמינל (Windows cp1255), לא הנתונים.
> בדיקת JSON ישירה: **0 תגיות עם replacement character.**
> **CL-2 = 0 מוצרים — אין מה לנקות.**

---

## Cleanup Scope אמיתי

| קוד | תג להסרה | מוצרים מושפעים | מצב |
|-----|---------|----------------|-----|
| CL-1 | `Copy AI` | **75** | ✅ מאושר לביצוע |
| CL-2 | garbled Hebrew | **0** | ✅ N/A — אין garbled |
| CL-3 | `All categories` | **3** | ✅ מאושר לביצוע |
| **סה"כ** | | **76** (2 overlap) | |

### הערה על `3-6M6-9M` (מוצר 1):
- תג malformed (שני טווחי גיל מחוברים בטעות: "3-6M" + "6-9M")
- **לא garbled encoding** — שגיאת data
- **לא נכלל בcleanup** — נדרש אישור אייל בנפרד

---

## Safety Check

| בדיקה | תוצאה |
|-------|-------|
| NO VALID TAGS WILL BE REMOVED | **YES** |
| תגיות תקינות שנשמרות | baby-gift, newborn-clothing, everyday-baby-wear, neutral-baby-outfit, אוברול, 12-18 חודש, 6-12 חודש, וכל השאר |
| backup קיים | YES — output/tags/pre-phase1-cleanup-backup.json |

---

## דוגמאות לפני/אחרי (15 ראשונים)

| # | product_id | title | tags_before | tags_to_remove | tags_after |
|---|-----------|-------|------------|---------------|-----------|
| 1 | 9166992900409 | BABY MANIA™ בובה נושמת | Copy AI | Copy AI | (empty) |
| 2 | 9179155693881 | אוברול אלגנט דגם עומרי | Copy AI, אוברול | Copy AI | אוברול |
| 3 | 9179176141113 | אוברול דובונים מכותנה - ליאור | Copy AI, אוברול | Copy AI | אוברול |
| 4 | 9179161231673 | אוברול כותנה קיצי - נועה | Copy AI, אוברול | Copy AI | אוברול |
| 5 | 9179137933625 | אוברול מתוק מכותנה - נויה | Copy AI | Copy AI | (empty) |
| 6 | 9179158479161 | אוברול פשתן וכותנה - קייגו | Copy AI, אוברול | Copy AI | אוברול |
| 7 | 9179138457913 | אוברול קיצי סטייל - יואבי | Copy AI | Copy AI | (empty) |
| 8 | 9179152482617 | בגד גוף אלגנטי - מייקל | Copy AI | Copy AI | (empty) |
| 9 | 9179165753657 | בגד גוף כותנה טטרה | Copy AI | Copy AI | (empty) |
| 10 | 9179154612537 | בגד גוף כיווצים - גאיה | Copy AI | Copy AI | (empty) |
| 11 | 9179149173049 | בגד גוף עם כובע | Copy AI | Copy AI | (empty) |
| 12 | 9179168964921 | בגד גוף עם תחרה | Copy AI | Copy AI | (empty) |
| 13 | 9179150516537 | שמלת מלמלות מתוקה - לין | Copy AI | Copy AI | (empty) |
| 14 | 9179162444089 | שמלת כיווצים קיצית - ענבל | Copy AI | Copy AI | (empty) |
| 15 | 9179163689273 | (All categories product) | All categories, ... | All categories | (rest unchanged) |

---

## Verdict

```
NO VALID TAGS WILL BE REMOVED: YES
BACKUP EXISTS: YES
DRY-RUN CREATED: YES
SAFE TO PROCEED: YES
```

*Dry-run created: 2026-05-03 | no Shopify writes performed*
