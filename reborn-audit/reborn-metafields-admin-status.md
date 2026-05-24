# סטטוס Metafield Definitions — Shopify Admin
**טרמינל 6 | BabyMania | ריבורן בלבד**
**עדכון:** 2026-05-24 08:38

---

## 1. שדות קיימים (מה שנמצא בשופיפיי)

| namespace | key | type | status |
|---|---|---|---|
| `baby_mania` | `faq` | `json` | ✅ existed |
| `reborn_doll` | `hebrew_name` | `single_line_text_field` | ✅ created |
| `reborn_doll` | `model_label` | `single_line_text_field` | ✅ created |
| `reborn_specs` | `size_cm` | `single_line_text_field` | ✅ created |
| `reborn_specs` | `source_note` | `single_line_text_field` | ✅ created |
| `reborn_copy` | `hero_subtitle` | `multi_line_text_field` | ✅ created |

---

## 2. טבלת שימוש לפי סקשן

| namespace | key | Hero S1 | Final CTA S17 | FAQ S16 | פרטי דגם S13 |
|---|---|---|---|---|---|
| `reborn_doll` | `hebrew_name` | ✅ | ✅ | ✅ | ❌ |
| `reborn_doll` | `model_label` | ✅ | ✅ | ✅ | ❌ |
| `reborn_specs` | `size_cm` | ✅ | ❌ | ❌ | ✅ |
| `reborn_specs` | `source_note` | ❌ | ❌ | ❌ | ✅ |
| `reborn_copy` | `hero_subtitle` | ✅ | ❌ | ❌ | ❌ |
| `baby_mania` | `faq` | ❌ | ❌ | ✅ | ❌ |

---

## 3. שדות שלא נוצרו ולמה

| שדה | סיבה |
|---|---|
| שיער / עיניים / אביזרים / בגדים | UNKNOWN בכל המוצרים |
| רחיץ / גיל / CE | לא מאומת |
| `baby_mania.faq` | existed — check-only, לא נגעו |

---

## 4. האם אפשר לעבור לשלב 7?

✅ **כן** — כל 5 definitions נוצרו בהצלחה. `baby_mania.faq` קיים ולא שונה.

לפני שלב 7 נדרש גם:
- [ ] כתיבת ערכי לוי לשופיפיי (לפי `levi-metafield-values-draft.md`)
- [ ] אישור אייל על הערכים
