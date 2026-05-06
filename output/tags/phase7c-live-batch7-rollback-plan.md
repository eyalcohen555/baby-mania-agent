# Phase 7C Live Batch 7 — Rollback Plan

**Generated:** 2026-05-06T08:49:46.913455+00:00  
**Use if live write fails.** For each product below, PUT the before_tags back.

| # | product_id | title | before_tags |
|---|-----------|-------|------------|
| 1 | `9688935039289` | חליפת מתוקה הדפס אריהדגם שמר | `baby-gift, baby-suit, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 2 | `9606694273337` | חליפת ספורט-אלגנט לילד | `baby-gift, baby-suit, everyday-baby-wear, kids-clothing, sporty-baby` |
| 3 | `9179172077881` | חליפת סריג אלגנטית - מייגן | `` |
| 4 | `9673732194617` | חליפת פליז דגם שרון | `baby-gift, baby-suit, fleece-baby, neutral-baby-outfit, newborn-clothing, winter-baby-wear` |
| 5 | `9874906513721` | חליפת פסים מהפנטת דגם ריף | `baby-gift, baby-suit, cotton-baby, everyday-baby-wear, newborn-clothing, striped-baby` |
| 6 | `9179158217017` | חליפת פפיון - אלין | `` |
| 7 | `9179169128761` | חליפת פפיון קיצית - קרן | `` |
| 8 | `9606693880121` | חליפת פרווה סטייל לבנות | `baby-gift, baby-set, baby-shower-gift, faux-fur-baby, girls-clothing, neutral-baby-outfit, newborn-clothing, winter-baby-wear` |
| 9 | `9605887754553` | חליפת פשתן לתינוק | `baby-gift, baby-suit, everyday-baby-wear, linen-baby, neutral-baby-outfit, newborn-clothing` |
| 10 | `9179157266745` | חליפת פשתן מלמלות - קיילי | `` |
| 11 | `9858268463417` | חליפת קיץ מהפנטת דגם עומרי | `baby-gift, baby-suit, neutral-baby-outfit, newborn-clothing, summer-baby-wear` |
| 12 | `9874906480953` | חליפת קיץ מושלמת דגם רונה | `baby-gift, baby-suit, neutral-baby-outfit, newborn-clothing, summer-baby-wear` |
| 13 | `9179159888185` | חליפת קיץ מכותנה - 1977 | `baby-gift, baby-suit, cotton-baby, neutral-baby-outfit, newborn-clothing, summer-baby-wear` |
| 14 | `9179173617977` | חליפת קיץ פרחונית לתינוקות – מורן | `0-3 חודש, 12-18 חודש, 3-6 חודש, 6-12 חודש, חליפה` |
| 15 | `9606694043961` | חליפת קרופ לקיץ | `baby-gift, baby-suit, neutral-baby-outfit, newborn-clothing, summer-baby-wear` |
| 16 | `9688935006521` | חליפת שלוש חלקים פיל דגם אימרי | `baby-gift, baby-set, baby-shower-gift, elephant-print-baby, everyday-baby-wear, newborn-clothing` |
| 17 | `9179167949113` | חליפת תחרה אלגנטית - אלינויה | `` |
| 18 | `9864947990841` | סט  קיץ לבנות דגם אודיה | `` |
| 19 | `10025300853049` | סט Breeze™ – חולצה קצרה ומכנסי קיץ לפעוט | `baby-gift, baby-pants, baby-shower-gift, neutral-baby-outfit, summer-baby-wear, toddler` |

**Rollback command pattern:**
```
PUT /products/{id}.json  →  tags = before_tags
```