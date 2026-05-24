# סטטוס Theme Test Upload — שלב 9
**טרמינל 6 | BabyMania | ריבורן בלבד**
**עדכון:** 2026-05-24
**חנות:** a2756c-c0.myshopify.com

---

## 1. Themes בחנות

| שם | role | theme_id | |
|---|---|---|---|
| Dawn | unpublished | 165778555193 | |
| Prestige | unpublished | 165778653497 | |
| Prestige working theme | unpublished | 179979387193 | |
| Copy of Prestige working theme | unpublished | 181901263161 | |
| **Dawn** | **unpublished** | **182057763129** | **← TEST** |
| BACKUP – Dawn (do not edit) | unpublished | 182139945273 | גיבוי |
| Copy of Dawn new | **main** | 183668179257 | **← LIVE** |

---

## 2. גישה סופית — Legacy Liquid Template

**גישה ראשונה שנכשלה:** JSON template + Dawn section עם `{% stylesheet %}` → דף ריק.
**סיבה:** `{% stylesheet %}` בסקשן עם CSS גדול + Tailwind config לא render ב-Dawn.

**גישה שנבחרה:** `templates/product.reborn.liquid` עם `{% layout none %}` — standalone HTML מלא.

| | |
|---|---|
| **template_suffix של לוי** | `reborn` |
| **קובץ template בטיים בדיקה** | `templates/product.reborn.liquid` |
| **גישה** | `{% layout none %}` — HTML עצמאי מלא |
| **product object** | זמין (Shopify מזריק ל-product templates) |
| **שינוי template_suffix נדרש?** | לא — suffix כבר `reborn` |

---

## 3. קבצים ב-Theme Test (182057763129)

| key | סטטוס | גודל |
|---|---|---|
| `templates/product.reborn.liquid` | ✅ הועלה + אומת | 119,449 bytes |
| `templates/product.reborn.json` | ✅ נמחק (הוחלף ב-liquid) | — |
| `sections/bm-reborn-product-page.liquid` | קיים (לא בשימוש בגישה הנוכחית) | 116,811 bytes |

---

## 4. Template Suffix של לוי

| | |
|---|---|
| **PID** | 9689589383481 |
| **template_suffix** | `reborn` |
| **template בטיים בדיקה** | `templates/product.reborn.liquid` ✅ תואם |
| **שינוי נדרש?** | לא |

---

## 5. Preview URL

```
https://a2756c-c0.myshopify.com/products/9689589383481?preview_theme_id=182057763129
```

פתיחת קישור זה תציג את לוי עם:
- S1 Hero דינמי (metafields + variant price)
- S17 Final CTA דינמי
- S2–S16 כמו שהם
- `{% layout none %}` — דף עצמאי, ללא header/footer של Dawn

---

## 6. מה עדיין hardcoded (בכוונה)

| מיקום | ערך | סיבה |
|---|---|---|
| S2 Bundle | ₪299 / ₪549 / ₪779 | מחוץ לתחולה |
| S15 Price compare | 299 ₪ | סקשן static |
| S16 FAQ | 5 שאלות | ממתין לשלב FAQ |
| S1 trust bar | טקסטים קבועים | ברמת חנות |

---

## 7. מה נשאר לפני production

- [ ] פתיחת Preview URL לאישור ויזואלי עם אייל
- [ ] Buy Now JS (לשלב 10)
- [ ] Tailwind CDN → compiled asset (לפני push live)
- [ ] אישור אייל על דף לפני דחיפה ל-live theme
