# Phase 7C Live Batch 9 — Rollback Plan

**Generated:** 2026-05-07T09:02:20.966716+00:00  
**Use if live write fails.** For each product below, PUT the before_tags back.

| # | product_id | title | before_tags |
|---|-----------|-------|------------|
| 1 | `10011383071033` | סט מכנס וחולצה מהממים דגם דניאל | `baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 2 | `9724813476153` | סט מכנס וחולצה קואלה דגם ראם | `animal-print-baby, baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, newborn-clothing` |
| 3 | `9855017648441` | סט מכנס וחולצה קיצי דגם גילי | `baby-gift, baby-set, baby-shower-gift, cotton-baby, neutral-baby-outfit, newborn-clothing, summer-baby-wear` |
| 4 | `9096636694841` | סט מלא לתינוקות - קופסת מתנה | `` |
| 5 | `9688955978041` | סט מתוק מפליז אם ווסט תואם דגם ראם | `12-18 חודש, 18-24 חודש, 2-3 שנים, 6-12 חודש, חורף, סט` |
| 6 | `10029649068345` | סט נוחות אליאב | `` |
| 7 | `9096607203641` | סט סוודר חורפי דניאל | `` |
| 8 | `9606693749049` | סט פיג'מה ארוכה דובונים לחורף | `baby-gift, baby-set, baby-shower-gift, neutral-baby-outfit, newborn-clothing, winter-baby-wear` |
| 9 | `9606694306105` | סט פיג'מה ארוכה לילד | `baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, kids-clothing, neutral-baby-outfit` |
| 10 | `9606671008057` | סט פרחוני וג'ינס לתינוקת | `baby-gift, baby-set, baby-shower-gift, denim-baby, everyday-baby-wear, floral-baby, newborn-clothing` |
| 11 | `9606691586361` | סט פשתן קלאסי ואלגנטי לבנים ובנות | `` |
| 12 | `9605887820089` | סט קיצי לתינוקות וילדות | `baby-gift, baby-set, baby-shower-gift, kids-clothing, neutral-baby-outfit, summer-baby-wear` |
| 13 | `9864947728697` | סט קיצי משגע לבנות דגם בת אל | `baby-gift, baby-set, baby-shower-gift, girls-clothing, neutral-baby-outfit, newborn-clothing, summer-baby-wear` |
| 14 | `10029649035577` | סט רומפר מעבר דגם אורן | `autumn-baby-wear, baby-gift, baby-romper, baby-shower-gift, neutral-baby-outfit, newborn-clothing` |
| 15 | `9606691389753` | סט שיא הסטייל לבנים | `` |
| 16 | `9873510957369` | סט של 3 אוברולים עונת מעבר דגם ישראל | `אוברול` |
| 17 | `9687653024057` | סט שני חליפות חד קרן דגם אנה | `baby-gift, baby-set, baby-shower-gift, everyday-baby-wear, newborn-clothing, unicorn-baby` |
| 18 | `10011383136569` | סטים 3 חליפות סגירה קלה דגם רוני | `baby-gift, baby-set, baby-shower-gift, cotton-baby, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |
| 19 | `9678573207865` | סרבל מעוצב אלגנטי דגם מאור | `baby-gift, baby-romper, elegant-baby, everyday-baby-wear, newborn-clothing` |
| 20 | `9605887492409` | סרבל עבודה אופנתי לתינוק | `baby-gift, baby-romper, everyday-baby-wear, neutral-baby-outfit, newborn-clothing` |

**Rollback command pattern:**
```
PUT /products/{id}.json  →  tags = before_tags
```