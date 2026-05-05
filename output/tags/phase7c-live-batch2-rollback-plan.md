# Phase 7C Live Batch 2 — Rollback Plan

**Backup file:** `output/tags/phase7c-live-batch2-backup.json`  
**Trigger:** any product verify FAIL during live write  

## Protocol

1. Stop immediately on first FAIL
2. Read backup — get `before_tags` for each written product
3. PUT back `before_tags` for each written product
4. GET verify rollback
5. Commit: `rollback(layer7): phase7c live batch2`

## Products (7)

| product_id | title | proposed_tags |
|-----------|-------|---------------|
| `9179141308729` | כובע בייסבול דובוני לתינוקות מעוצב ומהמם | type-hat, gender-girl |
| `9606864666937` | כובע בייסבול רך לתינוק | type-hat, gender-girl |
| `10024854847801` | כובע צמר מתנה | type-hat, occ-gift |
| `9179140915513` | כובע קייצי רך ונעים מכותנה מתאים לתנוקות | type-hat |
| `9731768713529` | מעיל אופנתי לבנות – דגם שיראל | type-coat, gender-girl, occ-gift, occ-everyday |
| `9673730359609` | מעיל חורף צמר דגם שנאל | type-coat, gender-girl, occ-gift, occ-seasonal |
| `9688976228665` | מעיל קורדרוי מחמם מאוד דגם אליה | type-coat, gender-boy, occ-gift, occ-seasonal |
