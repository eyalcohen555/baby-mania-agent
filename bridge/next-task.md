TASK: סגור B4+B6+B7 ב-orchestrator.py
LAYER: 4
ACTION:
  1. B4 — FAQ overwrite protection: הוסף shoes לרשימת החריגים
  2. B6 — verify gate: קרא required_metafields לפי category (clothing/shoes)
  3. B7 — agents.order: הוסף shoes agents לסדר הריצה
  4. שמור ובצע commit+push

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
