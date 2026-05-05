# Phase 8E — Shopify Auth Token Flow Check

**Date:** 2026-05-05  
**Type:** READ-ONLY — no writes to Shopify  
**Purpose:** Determine how the project obtains Shopify tokens and whether browser/localhost OAuth is needed

---

## 1. האם נמצא flow לקבלת token דרך הדפדפן

**לא.** הפרויקט משתמש ב-`client_credentials` grant — אין צורך בדפדפן או ב-localhost.

---

## 2. איזו פקודה להריץ

Flow קיים ב-`shopify_client.py` — הוא רץ אוטומטית בכל קריאת API. אין פקודה נפרדת להפעלה.

```python
# shopify_client.py
TOKEN_URL = f"https://{SHOPIFY_SHOP_URL}/admin/oauth/access_token"

def _get_access_token():
    resp = requests.post(TOKEN_URL, data={
        "grant_type": "client_credentials",
        "client_id": SHOPIFY_CLIENT_ID,
        "client_secret": SHOPIFY_CLIENT_SECRET,
    })
    data = resp.json()
    _token_cache["access_token"] = data["access_token"]
```

---

## 3. האם צריך localhost:3000

**לא.** `client_credentials` flow:
- לא מצריך הפניית דפדפן
- לא מצריך callback URL
- לא מצריך localhost
- עובד ישירות בין שרת לשרת (server-to-server)

---

## 4. איפה לשים את ה-token

`config/settings.py` טוען שני קבצי `.env`:

```python
load_dotenv()                                                          # project .env ראשון
load_dotenv(r"C:\Users\3024e\Desktop\shopify-token\.env", override=True)  # Desktop מנצח
```

| קובץ | מנצח? | תפקיד |
|------|--------|--------|
| `C:\Projects\baby-mania-agent\.env` | ❌ | Client ID + Client Secret לflow |
| `C:\Users\3024e\Desktop\shopify-token\.env` | ✅ | Desktop מנצח (override=True) |

עבור `client_credentials` flow, מה שחשוב הוא `SHOPIFY_CLIENT_ID` + `SHOPIFY_CLIENT_SECRET` (לא ה-access token הסטטי).

---

## 5. תוצאת בדיקת ה-flow

| בדיקה | תוצאה |
|--------|--------|
| Exchange request (POST to `/admin/oauth/access_token`) | ✅ HTTP 200 |
| Token prefix בתשובה | `shpat_` ✅ (Admin API access token) |
| Token suffix (4 אחרונים של token חדש) | `d55d` |
| `menus_read` עם token חדש | ❌ HTTP 403 |
| סיבה ל-403 | `online_store_navigation` scope לא מוגדר באפליקציה |

**הסבר:** `client_credentials` מחזיר token עם ה-scopes שמוגדרים לאפליקציה בShopify Admin.  
כל עוד `read_online_store_navigation` + `write_online_store_navigation` לא מוגדרים — כל token שמתקבל (סטטי או דינמי) יחזיר HTTP 403 על menus.

---

## 6. כתיבה לShopify

**שום דבר.** POST ל-`/admin/oauth/access_token` הוא קריאת auth (לא כתיבת נתונים), וה-GET על menus רק בדק גישה.

---

## 7. מה נדרש מאייל — פעולה אחת

```
Shopify Admin → Settings → Apps and sales channels
→ [האפליקציה שלך] → Configuration → Admin API integration
→ Admin API access scopes → הוסף:
   ✅ read_online_store_navigation
   ✅ write_online_store_navigation
→ Save
→ API credentials → Rotate API credentials
→ העתק token חדש (מוצג פעם אחת בלבד!)
→ עדכן: C:\Users\3024e\Desktop\shopify-token\.env
   SHOPIFY_ACCESS_TOKEN=shpat_[token החדש]
```

אחרי הפעולה הזו — גם ה-`client_credentials` flow וגם ה-token הסטטי יעבדו עם menus.

---

## 8. סיכום

| שאלה | תשובה |
|-------|--------|
| האם נמצא flow דרך הדפדפן | ❌ לא — `client_credentials` server-to-server בלבד |
| פקודה להרצה | אוטומטי ב-`shopify_client.py` — אין פקודה נפרדת |
| צריך localhost:3000 | ❌ לא |
| איפה לשים token | `C:\Users\3024e\Desktop\shopify-token\.env` |
| נכתב לShopify | ✅ שום דבר |
| Flow עובד בפועל | ✅ HTTP 200, token suffix `d55d` |
| menus עם token החדש | ❌ HTTP 403 — scope חסר |

---

## 9. Verdict

**TOKEN_FLOW_FOUND — STILL_BLOCKED_SCOPE_MISSING**

`shopify_client.py` כבר מכיל `client_credentials` flow עובד — אין צורך בהגדרת OAuth חדשה.  
הבלוקר היחיד: `read_online_store_navigation` + `write_online_store_navigation` לא מוגדרים בשopify app.  
אחרי שאייל יוסיף scopes וירוטייט credentials — Phase 8E navigation dry run יוכל לרוץ אוטומטית.

---

*Report generated: Phase 8E auth flow check — 2026-05-05*
