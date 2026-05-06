# Phase 7C Live Batch 6 — Rollback Plan

**Generated:** 2026-05-06T06:16:37.449662+00:00  
**Use if live write fails.** For each product below, PUT the before_tags back.

| # | product_id | title | before_tags |
|---|-----------|-------|------------|
| 1 | `9606694011193` | שמלת קיץ מיוחדת לבנות | `baby-dress, baby-gift, girls-clothing, neutral-baby-outfit, newborn-clothing, summer-baby-wear` |
| 2 | `9895864402233` | שמלת קיץ פרחונית לתינוקות דגם אלין | `baby-dress, baby-gift, floral-baby, newborn-clothing, summer-baby-wear` |
| 3 | `9605887590713` | שמלת שמש לתינוקות וילדות | `baby-dress, baby-gift, cotton-baby, everyday-baby-wear, kids-clothing, neutral-baby-outfit` |
| 4 | `9892620960057` | שמלת תחרה כפלים דגם טליה | `` |
| 5 | `9096607400249` | חליפת דוב  סוודר כותנה  - דגם דנה | `baby-gift, baby-suit, bear-print-baby, cotton-baby, everyday-baby-wear, newborn-clothing` |
| 6 | `9096606810425` | חליפת דוב  סוודר כותנה  - דגם רותם | `baby-gift, baby-suit, bear-print-baby, cotton-baby, everyday-baby-wear, newborn-clothing` |
| 7 | `9688965022009` | חליפת דובי דגם נתן | `baby-gift, baby-suit, bear-print-baby, everyday-baby-wear, newborn-clothing` |
| 8 | `9096606974265` | חליפת וופל במגוון צבעים | `baby-gift, baby-suit, everyday-baby-wear, neutral-baby-outfit, newborn-clothing, waffle-knit` |
| 9 | `10005779710265` | חליפת חורף לתינוקת עם כובע דגם שון | `baby-gift, baby-suit, cotton-baby, neutral-baby-outfit, newborn-clothing, winter-baby-wear` |
| 10 | `9179167654201` | חליפת חצאית תחרה אלגנטית - קארין | `` |
| 11 | `9179170799929` | חליפת טטרה קיצית מכותנה - עידודו | `` |
| 12 | `9606691356985` | חליפת טניס קיצית לבנות | `baby-gift, baby-suit, girls-clothing, neutral-baby-outfit, newborn-clothing, summer-baby-wear` |
| 13 | `9179157725497` | חליפת כותנה אורגנית - בילי | `` |
| 14 | `9179133870393` | חליפת כותנה וופל בשילוב דובי - בנים, בנו | `` |
| 15 | `9179158839609` | חליפת כותנה ופשתן - בייבילו | `` |
| 16 | `9179164705081` | חליפת כותנה משובצת - נטע | `` |
| 17 | `9179166376249` | חליפת כותנה סרוגה בייסיק - אדריאן | `` |
| 18 | `9179148190009` | חליפת כותנה קז'ואל - מאורי | `` |
| 19 | `9179168473401` | חליפת מלמלות טטרה- אלכסה | `` |
| 20 | `9179170144569` | חליפת מלמלות מכותנה ופשתן - מיילי | `` |

**Rollback command pattern:**
```
PUT /products/{id}.json  →  tags = before_tags
```