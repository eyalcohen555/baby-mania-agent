# Phase 7C Live Batch 5 — Rollback Plan

**Generated:** 2026-05-06T05:47:18.874861+00:00  
**Use if live write fails.** For each product below, PUT the before_tags back.

| # | product_id | title | before_tags |
|---|-----------|-------|------------|
| 1 | `9892620894521` | שמלת פליסה דגם אוריה | `baby-dress, baby-gift, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 2 | `9179151008057` | שמלת פפיון אחורי קלאסית - לוראן | `` |
| 3 | `9179149173049` | שמלת פפיון אלגנטית קלאסית - לין | `` |
| 4 | `9892196417849` | שמלת פפיון כחולה דגם אביבה | `baby-dress, baby-gift, neutral-baby-outfit, newborn-clothing, spring-baby-wear` |
| 5 | `9606693978425` | שמלת קיץ חגיגית עם מלמלה | `` |
| 6 | `9858268528953` | חליפת אביב יוקרתית דגם  דין | `baby-gift, baby-shower-gift, baby-suit, newborn-clothing, special-occasion-baby, spring-baby-wear` |
| 7 | `9179145568569` | חליפת אוברול קיצית נושמת ונעימה - גיא | `` |
| 8 | `10011383103801` | חליפת אלופים מהממת דגם שון  מבית בייבי מ | `baby-gift, baby-suit, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 9 | `9179151335737` | חליפת גופייה פרחונית - מאיה | `` |
| 10 | `9179152875833` | חליפת גופייה קיצית - מאור | `` |
| 11 | `10009173033273` | אוברול קטיפתי לתינוק – חמימות, נוחות וסט | `אוברול` |
| 12 | `9895864435001` | אוברול קיץ לתינוקות בעיצוב דובי דגם שי | `אוברול` |
| 13 | `9605503516985` | סרבל ארנב לתינוק | `baby-gift, baby-romper, cotton-baby, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 14 | `9874906415417` | רומפר קייצי מבית בייבי מניה דגם דין | `baby-gift, baby-romper, neutral-baby-outfit, newborn-clothing, summer-baby-wear` |
| 15 | `9864947859769` | סט פרחוני קיצי דגם לירון | `baby-gift, baby-set, baby-shower-gift, floral-baby, newborn-clothing, summer-baby-wear` |
| 16 | `9855017615673` | סט קיצי אלגנטי דגם מיה | `baby-gift, baby-set, baby-shower-gift, elegant-baby, newborn-clothing, summer-baby-wear` |
| 17 | `9605503451449` | סרבל ללא שרוולים לתינוק | `baby-gift, baby-romper, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 18 | `9687502422329` | סריג דובי דגם אריאל | `אוברול` |
| 19 | `9687653056825` | שלוש חליפות בייבי  דגם אנה | `baby-gift, baby-set, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 20 | `9096606056761` | חליפת ג׳ינס וחמניות- גיילוס | `baby-gift, baby-suit, denim-baby, denim-style-baby, everyday-baby-wear, newborn-clothing` |

**Rollback command pattern:**
```
PUT /products/{id}.json  →  tags = before_tags
```