# Phase 8E — Token Env Path Fix Report

**Date:** 2026-05-05  
**Type:** READ-ONLY — no writes to Shopify  
**Purpose:** Verify which .env holds the active token and whether navigation scope is available

---

## 1. מצב קבצי .env

| קובץ | קיים | SHOPIFY_ACCESS_TOKEN | SHOPIFY_CLIENT_SECRET | הערה |
|------|------|----------------------|-----------------------|------|
| `C:\Projects\baby-mania-agent\.env` | ✅ | ❌ אין | ✅ יש (shpss_ — חדש) | Token לא נמצא כאן |
| `C:\Users\3024e\Desktop\shopify-token\.env` | ✅ | ✅ יש (shpat_) | ✅ יש (shpss_ — ישן) | הקובץ שהמערכת קוראת |

---

## 2. Token שנטען בפועל

| שדה | ערך |
|-----|-----|
| קובץ מקור | `C:\Users\3024e\Desktop\shopify-token\.env` |
| שם משתנה | `SHOPIFY_ACCESS_TOKEN` |
| Prefix | `shpat_` |
| Suffix (4 אחרונים) | `e29a` |
| סוג | Admin API access token ✅ |

---

## 3. ניתוח המצב — מה אייל עשה

### מה שהשתנה:
- `C:\Projects\baby-mania-agent\.env` קיבל `SHOPIFY_CLIENT_SECRET` **חדש** (`shpss_...7984`)
- זה שונה מהclient secret הישן בדסקטופ (`shpss_...6d06`)

### מה שלא השתנה:
- `SHOPIFY_ACCESS_TOKEN` בדסקטופ עדיין `shpat_...e29a` — **לא עודכן**

### האבחנה:
> אייל רענן את **Client Secret** של האפליקציה בShopify Admin,  
> אך **לא יצר/חשף Access Token חדש**.  
>
> Client Secret (`shpss_`) ≠ Access Token (`shpat_`).  
> הם שני דברים נפרדים. ה-Access Token הוא מה שנשלח לAPI.

---

## 4. האם בוצעה העתקה?

**לא.** אין `SHOPIFY_ACCESS_TOKEN` בקובץ הפרויקט — אין מה להעתיק.

---

## 5. בדיקת Navigation Scope

| Scope | URL | HTTP | תוצאה |
|-------|-----|------|--------|
| menus_read | `/admin/api/2024-10/menus.json` | **403** | ❌ חסום |
| products_read | `/admin/api/2024-10/products/count.json` | 200 | ✅ עובד |
| collections_read | `/admin/api/2024-10/smart_collections.json` | 200 | ✅ עובד |

**Navigation scope: עדיין HTTP 403 — לא השתנה.**

---

## 6. כתיבה לShopify

**שום דבר.** כל הבדיקות היו GET בלבד.

---

## 7. מה נדרש מאייל — פעולה מדויקת

הבעיה: Token קיים (`shpat_...e29a`) לא כולל `online_store_navigation` scope.  
Client secret חדש שנוצר לא מספיק — צריך Access Token חדש.

### פעולות ב-Shopify Admin:

```
1. Shopify Admin → Settings → Apps and sales channels
2. לחץ על "Develop apps" (או על שם האפליקציה הקיימת)
3. לחץ על האפליקציה שלך
4. לחץ: "Configuration" → "Admin API integration"
5. תחת "Admin API access scopes" — חפש והוסף:
   ✅ read_online_store_navigation
   ✅ write_online_store_navigation
6. לחץ: "Save"
7. לחץ על: "API credentials"
8. תחת "Access tokens" → לחץ: "Rotate API credentials"
   (או "Generate" אם לא קיים)
9. העתק את הtoken החדש (מוצג פעם אחת בלבד!)
10. עדכן: C:\Users\3024e\Desktop\shopify-token\.env
    שורה: SHOPIFY_ACCESS_TOKEN=shpat_[הtoken החדש]
```

---

## 8. סיכום

| פריט | תוצאה |
|------|--------|
| קובץ .env מעודכן בפועל | `C:\Projects\baby-mania-agent\.env` (client secret חדש) |
| קובץ שהמערכת קוראת | `C:\Users\3024e\Desktop\shopify-token\.env` |
| בוצעה העתקה בין קבצים | ❌ לא — אין ACCESS_TOKEN חדש להעתיק |
| Token קיים בקובץ הנכון | ✅ כן — אך ישן, ללא navigation scope |
| Navigation/Menus read | ❌ HTTP 403 — scope חסר |
| עדיין יש HTTP 403 | ✅ כן |
| נכתב לShopify | ✅ שום דבר |

---

## 9. Verdict

**STILL_BLOCKED_SCOPE_MISSING**

Token חדש עם `read_online_store_navigation` + `write_online_store_navigation` scopes  
נדרש לפני שPhase 8E יכול להתקדם.

---

*Report generated: Phase 8E env token path check — 2026-05-05*
