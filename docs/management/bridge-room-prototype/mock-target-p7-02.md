# Product Brief: BabyMania Knit Wool Sleep Sack

**target_id:** TGT-P7-02
**prototype:** P7 / P8
**initial_state:** BROKEN — `review_status` has invalid value "unreviewed"
**p7_state:** ROLLED BACK — restored to pre-fix state after P7 FIX ERROR
**final_state:** FIXED — `review_status` corrected to "approved" by P8 STAGE-02 FIX
**resolved_issue:** ISS-P7-002
**resolved_by_pack:** EXEC-PACK-P8-001

---

## Required Fields

- **product_name:** BabyMania Knit Wool Sleep Sack
- **target_market:** Israel
- **target_audience:** Parents of infants age 3–12 months
- **target_language:** Hebrew
- **quality_standard:** standard
- **review_status:** approved

---

## Notes

This file was originally BROKEN (review_status: unreviewed — ISS-P7-002).
P7 FIX produced ERROR (review_status written as null). P7 ROLLBACK restored to broken state.
P8 STAGE-02 FIX correctly wrote review_status as string "approved".
P8 snapshot: `inbox/snapshots/pre-fix-target-p8-02.md.bak` (SNAP-P8-01).
ISS-P7-002 is now RESOLVED.
