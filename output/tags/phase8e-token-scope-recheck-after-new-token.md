# Phase 8E — Token Scope Recheck After New Token

**Date:** 2026-05-05  
**Type:** READ-ONLY — no writes to Shopify  
**Context:** Ayal updated C:\Projects\baby-mania-agent\.env with a new SHOPIFY_ACCESS_TOKEN

---

## 1. מצב קבצי .env

| קובץ | SHOPIFY_ACCESS_TOKEN | suffix | סטטוס |
|------|----------------------|--------|--------|
| `C:\Projects\baby-mania-agent\.env` | ✅ יש — shpat_ | `7984` | ❌ HTTP 401 — invalid |
| `C:\Users\3024e\Desktop\shopify-token\.env` | ✅ יש — shpat_ | `e29a` | ✅ HTTP 200 (products/collections) — אך 403 menus |

---

## 2. בדיקת Token החדש (Project .env — suffix: `7984`)

| Scope | Endpoint | HTTP | תוצאה |
|-------|----------|------|--------|
| products_read | `/admin/api/2024-10/products/count.json` | **401** | ❌ Invalid token |
| smart_collections | `/admin/api/2024-10/smart_collections.json` | **401** | ❌ Invalid token |
| custom_collections | `/admin/api/2024-10/custom_collections.json` | **401** | ❌ Invalid token |
| themes_read | `/admin/api/2024-10/themes.json` | **401** | ❌ Invalid token |
| menus 2024-10 | `/admin/api/2024-10/menus.json` | **401** | ❌ Invalid token |
| menus 2026-01 | `/admin/api/2026-01/menus.json` | **401** | ❌ Invalid token |

**שגיאה מדויקת:** `[API] Invalid API key or access token (unrecognized login or wrong password)`

---

## 3. אבחנה — למה ה-Token לא תקין

### מבנה Token חשוד:
```
shpat_[32-chars-hex]-[timestamp-digits]
                     ^^^^^^^^^^^^^^^^^
                     חלק זה לא אמור להיות כאן
```

Shopify access tokens אמיתיים נראים כך:
```
shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx   (ללא מקף, ללא מספר בסוף)
```

### מה כנראה קרה:
בגרסה הקודמת של קובץ הפרויקט, `SHOPIFY_CLIENT_SECRET` היה מסוג `shpss_[same-hex]-[timestamp]`.  
הערך הזה — **זהו client secret value**, לא access token.  
אייל שינה בטעות רק את ה-prefix מ-`shpss_` ל-`shpat_`, במקום להשתמש בtoken אמיתי מ-Shopify Admin.

**`shpss_` + ערך מסוים ≠ `shpat_` + אותו ערך.**  
Access token נוצר על ידי Shopify בנפרד ויש לו ערך שונה לחלוטין.

---

## 4. האם בוצעה העתקה?

**לא.** Token לא תקין (HTTP 401) — העתקה לDesktop `.env` תשבור את כל המערכת.  
Desktop `.env` נשאר עם הtoken הישן (`...e29a`) שלפחות תקין לרוב ה-scopes.

---

## 5. מצב Token הישן (Desktop .env — suffix: `e29a`)

| Scope | HTTP | תוצאה |
|-------|------|--------|
| products_read | 200 | ✅ עובד |
| collections_read | 200 | ✅ עובד |
| themes_read | 200 | ✅ עובד |
| menus_read | 403 | ❌ scope חסר |

---

## 6. נכתב לShopify

**שום דבר.** כל הבדיקות GET בלבד.

---

## 7. מה נדרש מאייל — פעולה מדויקת

### שלב 1 — הוסף scope
```
Shopify Admin → Settings → Apps and sales channels →
[שם האפליקציה] → Configuration → Admin API access scopes →
✅ read_online_store_navigation
✅ write_online_store_navigation
→ Save
```

### שלב 2 — קבל Access Token אמיתי
```
[אותה עמוד] → API credentials →
"Admin API access token" → לחץ: "Rotate API credentials"
(מציג את הtoken פעם אחת בלבד — העתק מיד!)
```

### שלב 3 — עדכן את הקובץ הנכון
```
פתח: C:\Users\3024e\Desktop\shopify-token\.env
עדכן רק את השורה:
SHOPIFY_ACCESS_TOKEN=shpat_[הtoken שהעתקת מShopify]

⚠️ לא: shpat_[client-secret-value]
⚠️ לא: שינוי prefix בלבד
✅ כן: הtoken המלא כפי שShopify הציג אותו
```

### שלב 4 — אל תעדכן את קובץ הפרויקט
```
C:\Projects\baby-mania-agent\.env — השאר ללא SHOPIFY_ACCESS_TOKEN
(קובץ זה מיועד לבוט, לא לAPI calls)
```

---

## 8. סיכום

| פריט | תוצאה |
|------|--------|
| .env שאייל עדכן | `C:\Projects\baby-mania-agent\.env` |
| .env שהמערכת קוראת | `C:\Users\3024e\Desktop\shopify-token\.env` |
| Token חדש תקין? | ❌ HTTP 401 — invalid (client secret value עם prefix מוחלף) |
| בוצעה העתקה? | ❌ לא — token פגום, לא מעתיקים |
| products read | ✅ (desktop token ישן) |
| collections read | ✅ (desktop token ישן) |
| themes read | ✅ (desktop token ישן) |
| navigation/menus read | ❌ HTTP 403 — scope חסר |
| נכתב לShopify | ✅ שום דבר |

---

## 9. Verdict

**STILL_BLOCKED_SCOPE_MISSING**

Token החדש בפרויקט `.env` אינו תקין (HTTP 401).  
Token בDesktop עדיין חסר `online_store_navigation` scope (HTTP 403 on menus).  
נדרש token אמיתי שנוצר על ידי Shopify אחרי הוספת ה-scope.

---

*Report generated: Phase 8E token recheck — 2026-05-05*
