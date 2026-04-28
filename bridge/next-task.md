TASK_ID: conductor-layer4-geo-priority-001-STAGE-13-20260416-182032
APPROVAL_TIER: T3
CONDUCTOR_PLAN: layer4-geo-priority-001
CONDUCTOR_STAGE: STAGE-13

GOAL:
בדיקה כפולה לפני כתיבה ל-Shopify live — T3 gate.

ACTION:
1. בדוק שוב draft coverage = 100%
2. בדוק שאין כפילות עם faq / benefits / accordion_blocks
3. אמת שכל metafield חדש בלבד:
   - baby_mania.geo_who_for
   - baby_mania.geo_use_case
   - baby_mania.geo_comparison
4. אמת שאין נגיעה בשדות sealed
5. חשב risk level סופי

הדפס:
COVERAGE: 100% / BELOW
SEALED_FIELDS_SAFE: YES / NO
NEW_FIELDS_ONLY: YES / NO
RISK_LEVEL: LOW / MEDIUM / HIGH
READY_FOR_LIVE: YES / NO
STAGE_VERDICT: PASS / FAIL

FILES_ALLOWED:
- (not restricted)

FILES_FORBIDDEN:
- (not restricted)

EXPECTED:
PRE-LIVE DOUBLE-CHECK REPORT

OUTPUT_REQUIRED:
Include in your response:
STAGE_VERDICT: PASS | FAIL | AWAITING_APPROVAL
EVIDENCE: [proof or failure reason]
SYSTEM STATE: [current state after this stage]
