# Phase 7C Long Run Tagging Completion Plan

## MODE
READ-ONLY PLANNING. No Shopify writes.

## SYSTEM STATE
- Total active products: 393
- Live tagged products now: 78
- SAFE candidates at original plan: 207
- Estimated remaining SAFE candidates: 180
- REVIEW_ONLY count: 135
- Rejected count: 0

## BLOCKED / EXCLUDED
- Shoes / sandals / sneakers remain excluded.
- EU shoe size mapping remains blocked.
- REVIEW_ONLY remains excluded.

## RECOMMENDED STRATEGY
- Use max 20 products per live batch.
- Separate T3 approval per live batch is safest.
- Batch order:
  1. dress / set / romper / bodysuit with strongest source trace
  2. remaining clean clothing types
  3. REVIEW_ONLY only after manual review
  4. shoes only after EU-size mapping approval

## REQUIRED GATES PER BATCH
- backup before write
- dry run
- forbidden tag check
- age-* check
- RANGE_TOO_BROAD check
- type collision check
- gender collision check
- false-positive keyword check
- Shopify PUT only after T3
- Shopify GET verify
- post-verify independent check
- rollback plan
- report
- explicit git add only

## STOP CONDITIONS
- any WARN
- any FAIL
- missing source trace
- REVIEW_ONLY candidate
- shoe/sandal/sneaker candidate
- EU shoe size product
- collection/navigation/theme change
- Shopify write/verify mismatch

## NEXT ACTION
Phase 7C Batch 3 READ-ONLY planning from remaining SAFE pool.

## VERDICT
READY_FOR_PHASE7C_LONG_RUN_REVIEW