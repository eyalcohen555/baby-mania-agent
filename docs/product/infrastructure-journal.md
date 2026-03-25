# Infrastructure Journal
**תחום:** orchestrator, config, routing, shared runtime infrastructure
**עדכון:** אחרי כל שינוי ב-orchestrator.py / config.yaml / settings.py / pipeline logic

---

## JOURNAL TEMPLATE

```
## DATE: YYYY-MM-DD
## TASK: שם המשימה
## SCOPE: infrastructure component
## WHAT CHANGED:
## FILES TOUCHED:
## SYSTEM IMPACT:
## OPEN ISSUES:
## NEXT STEP:
```

---

## DATE: 2026-03-25
## TASK: Orchestrator Shoes-Aware (B1–B7)
## SCOPE: orchestrator.py — category routing

## WHAT CHANGED:
- orchestrator.py עודכן לתמיכה מלאה בקטגוריה shoes
- category routing: product context → determines clothing vs shoes path
- shoes suffix handling נוסף לpush command
- Stage 2 guard נוסף (thinking layer must complete)
- B4 (FAQ protection) + B6 (verify gate) + B7 (routing) עודכנו

## FILES TOUCHED:
- `00-team-lead/orchestrator.py` (commits f68cfd1, 1bcbd3f)
- `00-team-lead/config.yaml` (commits 086ae8a, 7720f91)

## SYSTEM IMPACT:
- orchestrator עכשיו category-aware
- pipeline route מחושב אוטומטית לפי קטגוריה
- אסור להריץ agents ישירות — orchestrator בלבד

## OPEN ISSUES: none
## NEXT STEP: ריצת בדיקה ראשונה על shoes

---

## DATE: 2026-03-23
## TASK: Settings Cleanup + Architecture Doc
## SCOPE: config/settings.py, CATEGORY-ARCHITECTURE-DECISION.md

## WHAT CHANGED:
- `settings.py`: הוסרו phantom mappings — `bm-store-banner` הוסר, `bm-store-hero` נוסף
- `TEMPLATE_SECTIONS` עודכן ל-12 sections אמיתיות
- `bm-store-fabric` map תוקן מ-`fabric_story` ל-5 flat keys
- `CATEGORY-ARCHITECTURE-DECISION.md` נוצר — ארכיטקטורת thinking/writing/validation

## FILES TOUCHED:
- `config/settings.py`
- `CATEGORY-ARCHITECTURE-DECISION.md` (חדש)

## SYSTEM IMPACT:
- sections mapping מדויק — אין phantom keys
- ארכיטקטורה מתועדת

## OPEN ISSUES: none
## NEXT STEP: shoes rollout
