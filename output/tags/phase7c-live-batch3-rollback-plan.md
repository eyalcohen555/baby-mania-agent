# Phase 7C Live Batch 3 — Rollback Plan

**Backup file:** `output/tags/phase7c-live-batch3-backup.json`  
**Trigger:** any product verify FAIL during live write  

## Protocol

1. Stop immediately on first FAIL
2. Read backup JSON — get `before_tags` for each written product
3. For each written product: PUT back `before_tags` only
4. GET verify rollback completed
5. Commit with message: `rollback(layer7): phase7c live batch3`

## Products in this batch (20)

| product_id | title | proposed_new_tags | source_trace |
|-----------|-------|------------------|---------------|
| `9864947827001` | אוברול חגיגי דגם אנה | type-dress, gender-girl | type matched 'dress' in handle (conf=0.90); gender matched ' |
| `9179136426297` | שמלת ורדים חגיגית אלגנטית מלאה בסטייל -  | type-dress | type matched 'שמלת' in title (conf=0.90) |
| `9179151794489` | שמלת טול חגיגית - אוריאן | type-dress | type matched 'שמלת' in title (conf=0.90) |
| `9179137048889` | שמלת כותנה חגיגית - אלין | type-dress | type matched 'שמלת' in title (conf=0.90) |
| `9179147829561` | שמלת כותנה קיצית עם טקסטורה - יעל | type-dress | type matched 'שמלת' in title (conf=0.90) |
| `9687596663097` | אוברול סריג מתוק לתינוקות דגם שוהם | type-set, gender-girl | type matched 'set' in handle (conf=0.88); gender matched 'gi |
| `9724813443385` | אוברול סריג פסים דגם רפאל | type-set, gender-girl | type matched 'outfit' in handle (conf=0.88); gender matched  |
| `9179138457913` | אוברול קיצי מתוק סטייל קז'ואל - יואבי | type-set | type matched 'סט' in handle (conf=0.88) |
| `9673732292921` | חליפה 3 חלקים מבית בייבי מניה דגם אריאל | type-set, gender-girl | type matched 'חליפה' in title (conf=0.88); gender matched 'g |
| `9179156742457` | חליפה מסוגננת פרחונית - מיקה | type-set | type matched 'חליפה' in title (conf=0.88) |
| `9858268430649` | אוברול גינס מהמם דגם רוית | type-romper, gender-girl | type matched 'romper' in handle (conf=0.88); gender matched  |
| `9179176141113` | אוברול דובונים מכותנה - ליאור | type-romper | type matched 'אוברול' in title (conf=0.88) |
| `9179161231673` | אוברול כותנה קיצי - נועה | type-romper | type matched 'אוברול' in title (conf=0.88) |
| `10005779743033` | אוברול לתינוקות דגם סטייסי | type-romper, gender-girl | type matched 'romper' in handle (conf=0.88); gender matched  |
| `9096607138105` | אוברול מכופתרת | type-romper | type matched 'אוברול' in title (conf=0.88) |
| `9688965087545` | אוברול דוב מתוק דגם אייל | type-bodysuit, gender-boy | type matched 'bodysuit' in handle (conf=0.90); gender matche |
| `9719189635385` | אוברול דובי אם רגלית דגם אוריאל | type-bodysuit, gender-boy | type matched 'bodysuit' in handle (conf=0.90); gender matche |
| `9717957525817` | אוברול דובי דגם דניאל | type-bodysuit, gender-girl | type matched 'bodysuit' in handle (conf=0.90); gender matche |
| `10005779841337` | אוברול חורפי לתינוקות דגם אנגל | type-bodysuit, gender-girl | type matched 'bodysuit' in handle (conf=0.90); gender matche |
| `9688885952825` | חליפה מכנס וחולצה לבנות דגם אנה | type-bodysuit, gender-girl | type matched 'bodysuit' in handle (conf=0.90); gender matche |
