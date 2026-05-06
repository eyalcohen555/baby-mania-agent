# Phase 7C Live Batch 4 — Rollback Plan

**Generated:** 2026-05-06T04:53:04.581404+00:00  
**Use if live write fails.** For each product below, PUT the before_tags back.

| # | product_id | title | before_tags |
|---|-----------|-------|------------|
| 1 | `9179162444089` | שמלת כיווצים קיצית מכותנה - ענבל | `` |
| 2 | `9179150516537` | שמלת מלמלות מתוקה מכותנה - לין | `` |
| 3 | `9179142750521` | שמלת סטרפלס סטייל קז'ואל - ליאל | `` |
| 4 | `9605887721785` | שמלת סרבל לתינוקת | `baby-gift, baby-romper, cotton-baby, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 5 | `9179136131385` | שמלת ערב נסיכותית - רצ'ל | `` |
| 6 | `9855017582905` | חליפה מעוצבת סטייל שובב דגם ליאם | `baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 7 | `10009173721401` | חליפה קטיפתית לתינוק – חמימות, נוחות וסט | `baby-gift, baby-set, baby-shower-gift, neutral-baby-outfit, newborn-clothing, velvet-baby, winter-baby-wear` |
| 8 | `9179173191993` | חליפה קיצית פרחונית - היילי | `0-3 חודש, 12-18 חודש, 18-24 חודש, 3-6 חודש, 6-12 חודש` |
| 9 | `9606691914041` | חליפה קלאסית ואופנתית לבנות | `baby-gift, baby-suit, everyday-baby-wear, girls-clothing, neutral-baby-outfit, newborn-clothing` |
| 10 | `9688955912505` | חליפת 3 חלקים אריה מתוקה אם ווסט פרוותי  | `12-18 חודש, 18-24 חודש, 2-3 שנים, 6-12 חודש, סט` |
| 11 | `9179137933625` | אוברול מתוק מכותנה מלאה ללא כתפיות - נוי | `` |
| 12 | `9096607072569` | אוברול סרבל ארוך | `baby-gift, baby-overall, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 13 | `9688670110009` | אוברול פינגווין דגם נועם | `אוברול` |
| 14 | `9657036374329` | אוברול פליז דובי לתינוק – Teddy Cozy Sui | `אוברול` |
| 15 | `9179158479161` | אוברול פשתן וכותנה וינטג׳ - קייגו | `אוברול` |
| 16 | `9605887787321` | חליפה סרוגה לתינוק | `baby-gift, baby-suit, everyday-baby-wear, neutral-baby-outfit, newborn-clothing, soft-knit` |
| 17 | `9606691750201` | יחידת בגד גוף עם סרט לשיער לתינוק | `baby-bodysuit, baby-gift, cotton-baby, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 18 | `9687563305273` | סט 3 אוברולים ארנב דגם  שני | `אוברול` |
| 19 | `9687563370809` | סט לב לבנות דגם נועה | `` |
| 20 | `9719189733689` | סט מכנס וחולצה דגם הלל | `` |

**Rollback command pattern:**
```
PUT /products/{id}.json  →  tags = before_tags
```