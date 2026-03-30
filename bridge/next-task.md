TASK_ID: conductor-shoes-rollout-001-STAGE-4-20260330-080503
APPROVAL_TIER: T3
CONDUCTOR_PLAN: shoes-rollout-001
CONDUCTOR_STAGE: STAGE-4

GOAL:
פרסם 2 מוצרי נעליים אחרונים ל-Shopify ואמת

ACTION:
עבור כל PID ברשימה הבאה בסדר:
  1. 9615375794489
  2. 9615669461305

לכל PID:
  python 00-team-lead/orchestrator.py push <PID>
  python 00-team-lead/orchestrator.py verify <PID>

לאחר כל PID דווח:
  PID: <id> | push: PASS/FAIL | verify: PASS/FAIL | required_keys: N | LIVE: YES/NO

כלל עצירה:
  - אם push נכשל → עצור מיד, STAGE_VERDICT: FAIL + PID שנכשל
  - אם verify מדווח required_keys=0 → עצור מיד, STAGE_VERDICT: FAIL
  - אם verify נכשל → עצור מיד, STAGE_VERDICT: FAIL

אם שניהם עברו → STAGE_VERDICT: PASS

FILES_ALLOWED:
- (not restricted)

FILES_FORBIDDEN:
- (not restricted)

EXPECTED:
2 PIDs עם push PASS + verify PASS + required_keys=3 + LIVE=YES + STAGE_VERDICT: PASS

OUTPUT_REQUIRED:
Include in your response:
STAGE_VERDICT: PASS | FAIL | AWAITING_APPROVAL
EVIDENCE: [proof or failure reason]
SYSTEM STATE: [current state after this stage]
