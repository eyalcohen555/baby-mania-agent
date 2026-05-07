# Phase 7C — Batch 10 Revised Rollback Plan

**תאריך:** 2026-05-07  
**מוצר:** PID 9687563338041  
**פעולה שבוצעה:** הוספת תגיות `type-set`, `gender-girl`  
**מצב לפני:** תגיות ריקות (`""`)

---

## מתי להפעיל Rollback

הפעל rollback רק אם:
1. אחד מ-11 checks ב-verify נכשל
2. המוצר הוסר מ-Smart Collection לא נכוח
3. תגיות נמחקו בשגגה
4. אישור ניהולי מפורש מאייל

---

## פעולת Rollback

### Option A — מחיקת תגיות (חזרה למצב לפני)

```
PUT /admin/api/2024-10/products/9687563338041.json
{
  "product": {
    "id": 9687563338041,
    "tags": ""
  }
}
```

תוצאה: המוצר חוזר לתגיות ריקות — מצב לפני הכתיבה.

### Option B — החלפה לתגיות ספציפיות

אם יש תגיות אחרות שצריך לשמר — החלף את הערך ב-`tags`.

---

## Verify אחרי Rollback

```
GET /admin/api/2024-10/products/9687563338041.json
```

בדוק: `tags == ""` (ריק)

---

## גיבוי מצב לפני

קובץ: `output/tags/phase7c-live-batch10-revised-backup.json`

```json
{
  "product_id": "9687563338041",
  "tags_before": "",
  "tags_list_before": []
}
```

---

## סיכום

| | |
|---|---|
| מצב לפני | תגיות ריקות |
| מצב אחרי | gender-girl, type-set |
| Rollback action | PUT tags: "" |
| Rollback risk | LOW — מחזיר למצב ריק |
| Rollback needed | לא — 11/11 QA PASS |
