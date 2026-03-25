# Clothing Pipeline Journal
**תחום:** ביגוד — production status, issues, decisions
**עדכון:** אחרי כל שינוי ב-clothing lane או production issue

---

## JOURNAL TEMPLATE

```
## DATE: YYYY-MM-DD
## TASK: שם המשימה
## SCOPE: clothing component
## WHAT CHANGED:
## FILES TOUCHED:
## SYSTEM IMPACT:
## OPEN ISSUES:
## NEXT STEP:
```

---

## מצב נוכחי (2026-03-25)

```
סטטוס: ✅ פרודקשן
מוצרים לייב: 15
ממתין: 10 מוצרים על clothing-test → להעביר ל-clothing
```

---

## DATE: 2026-03-23
## TASK: Clothing Rollout — Production
## SCOPE: clothing pipeline + settings cleanup

## WHAT CHANGED:
- 15 מוצרי ביגוד עלו לאוויר בהצלחה
- `settings.py` נוקה — הוסרו phantom mappings ישנים
- `bm-store-banner` הוסר מ-SECTION_METAFIELD_MAP
- `bm-store-hero` נוסף
- TEMPLATE_SECTIONS עודכן ל-12 sections
- `bm-store-fabric` metafield map תוקן — `fabric_story` הוחלף ב-5 flat keys
- template `clothing-test` → שונה ל-`test-template`
- `CATEGORY-ARCHITECTURE-DECISION.md` נוצר

## FILES TOUCHED:
- `config/settings.py`
- `CATEGORY-ARCHITECTURE-DECISION.md` (חדש)

## SYSTEM IMPACT:
- clothing בפרודקשן ויציב

## OPEN ISSUES:
- [ ] 10 מוצרים על clothing-test — צריכים להעבר ל-template clothing

## NEXT STEP:
העברת 10 מוצרים מ-clothing-test ל-clothing template.
