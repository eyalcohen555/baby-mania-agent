# Phase 7C Live Batch 1 — Rollback Plan

**Backup file:** `output/tags/phase7c-live-batch1-backup.json`  
**Trigger:** any product verify FAIL during live write  

## Protocol

1. Stop immediately on first FAIL
2. Read backup JSON — get `before_tags` for each written product
3. For each written product: PUT back `before_tags` only
4. GET verify rollback completed
5. Commit with message: `rollback(layer7): phase7c live batch1`

## Products in this batch (20)

| product_id | title | proposed_tags |
|-----------|-------|---------------|
| `9606694142265` | שמלת אירועים אלגנטית לתינוקת | type-dress, gender-girl |
| `9606690111801` | שמלת בסגנון אמריקאי לבנות | type-dress, gender-girl |
| `9892620927289` | שמלת וי פסים דגם יהלי | type-dress, gender-girl |
| `9179134132537` | שמלת טוטו נסיכותית - אלין | type-dress |
| `9179152482617` | בגד גוף אלגנטי - מייקל | type-bodysuit |
| `9179168964921` | בגד גוף כיווצים אלגנטי - נטלי | type-bodysuit |
| `9096607301945` | בגד גוף פליז שרוולים ארוכים ופונפונים | type-bodysuit, gender-neutral, occ-gift, occ-seasonal |
| `9179172733241` | בגד גוף פסים אלגנטי - ריף | type-bodysuit |
| `9179138687289` | בגד גוף קיצי נוח ואוורירי, כולל כובע מתו | type-bodysuit |
| `10190523334969` | 0-18 Months old Newborn Baby boy Jumpsui | type-set, gender-boy, occ-seasonal |
| `10190522876217` | Toddler Summer Outfits 2026 New Baby Boy | type-set, gender-boy, occ-everyday, occ-seasonal |
| `9855017550137` | Veloura Baby™ חליפה פרחונית | type-set, gender-girl, occ-gift, occ-everyday |
| `10190523269433` | VISgogo Toddler Baby Boys Clothes Set Sh | type-set, gender-boy, occ-everyday, occ-seasonal |
| `9688934940985` | אוברול בייבי  לתינוק – Baby Bear Cozy Se | type-set |
| `10005779808569` | אוברול בייבי מניה דגם חן | type-set, gender-girl, occ-seasonal |
| `9179155693881` | אוברול אלגנט דגם עומרי | type-romper |
| `9096606908729` | אוברול ארוך | type-romper, gender-neutral, occ-gift, occ-everyday |
| `9096599994681` | אוברול ארוך עם רוכסן | type-romper, gender-neutral, occ-gift, occ-everyday |
| `9678573240633` | אוברול אריה מתוק דגם שמר | type-romper, gender-boy |
| `10026520445241` | אוברול בייבי מניה דגם חן | type-romper |
