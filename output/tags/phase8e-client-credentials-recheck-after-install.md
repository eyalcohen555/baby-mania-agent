# Phase 8E — client_credentials Recheck After App Install

**Date:** 2026-05-05  
**Shop:** a2756c-c0.myshopify.com  
**Type:** READ-ONLY — no writes to Shopify  
**Purpose:** Verify if navigation scope is now available after app reinstall/reconfiguration

---

## 1. client_credentials Flow

| Item | Result |
|------|--------|
| Flow source | `shopify_client.py` → `_get_access_token()` |
| CLIENT_ID | ✅ exists — suffix `0d09` |
| CLIENT_SECRET | ✅ exists — prefix `shpss_` suffix `6d06` |
| Token exchange (POST) | ✅ HTTP 200 |
| New token prefix | `shpat_` |
| New token suffix (last 4) | `a01c` |

---

## 2. Desktop .env Update

| Item | Result |
|------|--------|
| Token valid (`shpat_`) | ✅ Yes |
| `SHOPIFY_ACCESS_TOKEN` updated in Desktop .env | ✅ Updated |
| Token suffix written | `a01c` |

---

## 3. Scope Check Results

| Scope | Endpoint | HTTP | Result | Detail |
|-------|----------|------|--------|--------|
| `products_read` | `/admin/api/2024-10/products/count.json` | 200 | ✅ PASS | count=600 |
| `smart_collections` | `/admin/api/2024-10/smart_collections.json` | 200 | ✅ PASS | 5 items |
| `custom_collections` | `/admin/api/2024-10/custom_collections.json` | 200 | ✅ PASS | 5 items |
| `themes_read` | `/admin/api/2024-10/themes.json` | 200 | ✅ PASS | 7 items |
| `menus_2024` | `/admin/api/2024-10/menus.json` | **403** | ❌ FAIL | Scope undefined for API access: menus |
| `menus_2026` | `/admin/api/2026-01/menus.json` | **403** | ❌ FAIL | Scope undefined for API access: menus |

---

## 4. Navigation Scope Analysis

| Check | Result |
|-------|--------|
| menus 2024-10 HTTP | **403** |
| menus 2026-01 HTTP | **403** |
| Navigation accessible | ❌ NO — HTTP 403 on both API versions |
| Error message | `Scope undefined for API access: menus` |

### אבחנה מדויקת:

שגיאת Shopify: **"Scope undefined for API access: menus"**

המשמעות: האפליקציה **לא כוללת** scope בשם `menus` / `online_store_navigation` ברשימת ה-scopes שלה.

רשימת ה-"Valid scopes" שShopify מחזיר היא **כלל ה-scopes האפשריים בפלטפורמה** — לא מה שמוגדר לאפליקציה.
`online_store_navigation` מופיע ברשימה הזו, אך האפליקציה עדיין לא ביקשה אותו.

**הבעיה:** כשמוסיפים scope ב-Shopify Admin → Configuration → Admin API access scopes ולוחצים Save,
Shopify לא מנפיק token חדש אוטומטית — token קיים ממשיך עם ה-scopes הישנים עד שמסובבים credentials.

**הפתרון המדויק:**
```
1. Shopify Admin → Settings → Apps and sales channels
2. לחץ על האפליקציה → Configuration → Admin API integration
3. Admin API access scopes → וודא שמופיעים:
   ✅ read_online_store_navigation
   ✅ write_online_store_navigation
4. לחץ Save
5. לחץ: API credentials → Rotate API credentials
   (מפיק token חדש עם ה-scopes החדשים — מוצג פעם אחת!)
6. אין צורך לעדכן Desktop .env ידנית —
   client_credentials flow יפיק token חדש עם ה-scopes המעודכנים אוטומטית
```

---

## 5. Writes to Shopify

**NONE.** כל הבדיקות היו HTTP GET בלבד. אין PUT/POST/DELETE.

---

## 6. Summary

| Item | Result |
|------|--------|
| client_credentials flow | ✅ עובד |
| New token obtained | ✅ suffix `a01c` |
| Desktop .env updated | ✅ suffix `a01c` |
| products read | ✅ HTTP 200 (count=600) |
| smart_collections read | ✅ HTTP 200 (5 items) |
| custom_collections read | ✅ HTTP 200 (5 items) |
| themes read | ✅ HTTP 200 (7 items) |
| navigation/menus read (2024-10) | ❌ HTTP 403 |
| navigation/menus read (2026-01) | ❌ HTTP 403 |
| HTTP 403 still present | ✅ כן |
| Shopify writes | ✅ NONE |
| State docs updated | ❌ לא — verdict לא READY |

---

## 7. Verdict

**STILL_BLOCKED_SCOPE_MISSING**

Token חדש הופק בהצלחה (`shpat_...a01c`) — flow עובד.
אך `online_store_navigation` scope עדיין לא מוגדר באפליקציה.
HTTP 403 ב-`menus_2024` + `menus_2026` — Phase 8E navigation dry run חסום.

הפעולה הנדרשת: Shopify Admin → Apps → Configuration → הוסף `read_online_store_navigation` + `write_online_store_navigation` → Save → **Rotate API credentials** (חובה!).

---

*Report generated: Phase 8E recheck after app install — 2026-05-05*
