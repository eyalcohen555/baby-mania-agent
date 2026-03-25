TASK: Changes 1+3 — category routing + template suffix ב-orchestrator.py
LAYER: 4
ACTION:
  1. קרא: 00-team-lead/orchestrator.py
  2. הוסף category routing — קרא categories מ-config.yaml
  3. תקן template suffix — shoes מקבל suffix שונה מ-clothing
  4. תקן B3 — Stage 2 guard שיכיר shoes
  5. שמור ובצע commit+push

FILES_ALLOWED:
  - 00-team-lead/orchestrator.py
  - 00-team-lead/config.yaml

FILES_FORBIDDEN:
  - Shopify
  - sections
  - agents
  - publisher
  - validator

EXPECTED: CHANGES MADE / FILES UPDATED / RISK LEVEL / NEXT STEP
