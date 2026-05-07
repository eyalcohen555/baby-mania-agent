# Phase 7C Live Batch 8 — Rollback Plan

**Generated:** 2026-05-06T14:06:55.733944+00:00  
**Use if live write fails.** For each product below, PUT the before_tags back.

| # | product_id | title | before_tags |
|---|-----------|-------|------------|
| 1 | `9096622473529` | סט Solé™ | `` |
| 2 | `9606691848505` | סט אבטיח לקיץ דגם אביבית | `` |
| 3 | `9606694240569` | סט אוברול וחולצה דגם קובי | `אוברול` |
| 4 | `9606670909753` | סט אופנתי קצר לתינוק | `` |
| 5 | `9606694076729` | סט אלגנטי דגם מעיין | `baby-gift, baby-set, baby-shower-gift, elegant-baby, everyday-baby-wear, newborn-clothing` |
| 6 | `9096622604601` | סט בגדי תינוקות  בנות | `baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, girls-clothing, neutral-baby-outfit, newborn-clothing` |
| 7 | `10011383234873` | סט בגדים לתינוקות – חולצה ארוכה + אוברול | `אוברול` |
| 8 | `9873511055673` | סט בייסיק לתינוקות דגם  לירון | `baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 9 | `9606694371641` | סט בסגנון וינטג' אלגנטי לתינוקת | `` |
| 10 | `9606693945657` | סט ג'ינס אופנתי לבנות | `baby-gift, baby-set, baby-shower-gift, denim-baby, denim-style-baby, everyday-baby-wear, girls-clothing, newborn-clothing` |
| 11 | `9724813410617` | סט גי'נס מושלם דגם נחמן | `baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 12 | `9673732260153` | סט דובי פליז מחמם דגם נאור | `baby-gift, baby-set, baby-shower-gift, bear-print-baby, fleece-baby, newborn-clothing, winter-baby-wear` |
| 13 | `9864947958073` | סט חגיגי לקיץ דגם שירה | `baby-gift, baby-set, baby-shower-gift, newborn-clothing, special-occasion-baby, summer-baby-wear` |
| 14 | `9606670942521` | סט חגיגי לתינוקת | `baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, newborn-clothing, special-occasion-baby` |
| 15 | `9687579066681` | סט חד קרן דגם לינוי | `` |
| 16 | `9606691619129` | סט חולצה וחצאית ג'ינס חגיגי | `baby-gift, baby-set, baby-shower-gift, denim-baby, denim-style-baby, everyday-baby-wear, newborn-clothing` |
| 17 | `9687563403577` | סט חתול קלאסי דגם אדל | `` |
| 18 | `9672569749817` | סט לב גדול דגם שני | `` |
| 19 | `9606691422521` | סט לילדה וינטג' - מורן | `` |
| 20 | `9688674500921` | סט מכנס וחולצה דובי דגם רפאל | `baby-gift, baby-set, baby-shower-gift, bear-print-baby, everyday-baby-wear, newborn-clothing` |

**Rollback command pattern:**
```
PUT /products/{id}.json  →  tags = before_tags
```