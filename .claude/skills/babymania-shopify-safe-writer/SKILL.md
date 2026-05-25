---
name: babymania-shopify-safe-writer
description: אוכף פרוטוקול כתיבה בטוחה לכל פעולה שמשנה את Shopify ב-BabyMania. הפעל לפני כל כתיבה ל-Shopify — עדכוני theme assets, metafields, templates, sections, מוצרים, inventory, או כל Admin API PUT/POST. טריגרים: "כתוב לשופיפיי", "עדכן מוצר", "שנה תבנית", "PUT", "POST", "live write", "T3", "theme asset", "sections/", "templates/", "metafield", "כתיבה חיה", "apply patch", "deploy", כל שינוי ב-Shopify. אסור להמשיך בלי לעבור את הchecklist.
allowed-tools: Read, Grep, Glob, Bash
---

# babymania-shopify-safe-writer — כתיבה בטוחה לשופיפיי

## מתי להשתמש

- לפני כל PUT/POST לשופיפיי (theme assets, products, metafields)
- לפני הרצת script שכותב לשופיפיי
- כשמתכוננים ל-live write כלשהו
- לפני הפעלת Conductor plan עם T3 stage

## מתי לא להשתמש

- קריאות GET בלבד (T0 audit) — לא נדרש
- dry-run בלבד — לא נדרש, אבל מומלץ לעיין בכללים

## Checklist חובה לפני כל כתיבה חיה

```
☐ 1. T3 + אישור אייל — קיבלת אישור מפורש לכתיבה זו?
☐ 2. BACKUP — גיבית את הקובץ/מידע לפני השינוי?
☐ 3. DRY-RUN — בצעת dry-run ובדקת את הdiff?
☐ 4. SCOPE — השינוי ממוקד בדיוק במה שאושר?
☐ 5. EASY-SLEEP / TEMPIO — שינוי זה נוגע בהם? (אם כן — STOP)
☐ 6. AUTH — משתמשים ב-OAuth client_credentials (לא token סטטי)?
☐ 7. BULK — אם bulk, יש רשימת מוצרים מפורשת?
☐ 8. VERIFY — יש תוכנית verify אחרי הכתיבה?
```

**אם אחד מהם לא עבר — STOP. לא לכתוב.**

## כלל 1 — T3 ואישור אייל

כל כתיבה חיה לשופיפיי = T3. Bridge חוסם T3 אוטומטית.
אין לכתוב ל-Shopify בלי אישור מפורש מאייל לפעולה הספציפית הנוכחית.

## כלל 2 — גיבוי לפני כתיבה

לפני כל שינוי ב-`sections/*.liquid` / `templates/*.json`:
```python
backup = {"date": ..., "asset_key": ..., "source": live_source}
# שמור ל-output/tags/<phase>-backup.json
```
גיבוי חסר = אסור להמשיך.

## כלל 3 — Dry-run לפני Live Write

```
python scripts/<script>.py --mode=dry-run
```
- בדוק שה-diff הוא בדיוק מה שאושר
- אשר sanity checks (HTML unchanged, schema unchanged, CSS unchanged)
- רק אחרי dry-run PASS — עבור ל-`--mode=live`

## כלל 4 — Verify אחרי כתיבה

- HTTP 200 על מוצר/עמוד רלוונטי ב-storefront
- הוודא שהשינוי נמצא ב-HTML
- הוודא שלא נשבר שום דבר אחר (no regression)
- תעד תוצאה ב-`output/tags/<phase>-verify.json`

## כלל 5 — EasySleep / Tempio

**אסור לגעת ב-`product.easy-sleep.json` ו-`product.tempio.json` בלי אישור מפורש.**
הסיבה: main-product מושבת בתבניות אלו — כל שינוי עלול לשבור את layout הייחודי.
אם שינוי נוגע להם — STOP + שאל אייל.

## כלל 6 — Auth (OAuth client_credentials)

**אסור:** להשתמש ב-`SHOPIFY_ACCESS_TOKEN` סטטי.
**חובה:** OAuth client_credentials flow:

```python
def get_token():
    r = requests.post(
        f"https://{SHOP}/admin/oauth/access_token",
        data={"grant_type": "client_credentials",
              "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET},
    )
    return r.json()["access_token"]
```

מפתחות: `SHOPIFY_CLIENT_ID` + `SHOPIFY_CLIENT_SECRET` מ-`.env`.
אסור: להדפיס CLIENT_SECRET או token מלא ב-output.
אסור: להכניס `.env` ל-git.

Reference: `scripts/phase7c_live_batch9.py` → `_fetch_oauth_token()`.

## כלל 7 — Bulk Update

- אסור: bulk update בלי רשימת PIDs / handles מפורשת ומאושרת
- חייב: dry-run על כל הbatch לפני live
- חייב: verify על כל מוצר אחרי כתיבה
- Bulk > 5 מוצרים = T3 = אישור אייל

## Rollback

```python
backup = json.load(open("output/tags/<phase>-backup.json"))
put_asset(session, backup["asset_key"], backup["source"])
```
תמיד צור `output/tags/<phase>-rollback-plan.md` לפני כתיבה חיה.

## פורמט פלט חובה

```
SHOPIFY WRITE:         [מה מתכוונים לכתוב]
T3_APPROVAL:           YES / NO / PENDING
BACKUP:                DONE / MISSING
DRY_RUN:               PASS / FAIL / NOT_RUN
SCOPE_CONFIRMED:       YES / NO
EASYSLEEP_TEMPIO:      AFFECTED (STOP) / NOT AFFECTED
AUTH_METHOD:           oauth_client_credentials / STATIC_TOKEN (שגוי!)
BULK_LIST_PROVIDED:    YES / NO / N/A
VERIFY_PLAN:           [מה תבדוק אחרי]
STATUS:                CLEAR_TO_WRITE / BLOCKED — [סיבה]
```

## קבצי מקור שחובה לקרוא

- `docs/management/approval-policy.md` — מדיניות אישורים
- `BABYMANIA-MASTER-PROMPT.md` — Shopify Config + Auth section

## פעולות אסורות

- לגעת ב-Shopify live בלי T3 ואישור אייל
- להשתמש ב-SHOPIFY_ACCESS_TOKEN סטטי
- לעשות bulk update בלי רשימת PIDs מפורשת
- לדלג על dry-run
- לדלג על backup
- לכתוב ל-EasySleep / Tempio בלי אישור מפורש
- להחזיר token מלא ב-output / ב-log

## חוקי BabyMania

- Shop: `a2756c-c0.myshopify.com` | Theme ID: `183668179257` | API: `2024-10`
- Token location: `C:\Users\3024e\Desktop\shopify-token\.env`
- לפני כל משימת Shopify live בסשן חדש — smoke test OAuth
- אם OAuth נכשל — STOP. לא לעבור ל-token ישן.

## טעויות נפוצות למניעה

- לגשת ל-Shopify בלי לאמת שה-OAuth עובד בסשן הנוכחי.
- להניח ש"אישרתי T3 קודם" — אישור T3 תקף לפעולה ספציפית בלבד.
- לשכוח לגבות לפני שינוי — אין undo ב-Shopify.
- לכתוב bulk update ל-50 מוצרים ב-loop ללא verify בין לבין.
- לבדוק verify רק על staging ולא על storefront live.
