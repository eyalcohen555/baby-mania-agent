# Organic Article Image Agent — Spec v1.0
**Created:** 2026-05-21
**Status:** ACTIVE
**Owner:** אייל
**RULE: אין publish live ללא אישור אייל אחרי סיום generate**

---

## 1. תפקיד הסוכן

Organic Article Image Agent מייצר 2–3 תמונות פרימיום לכל מאמר אורגני של BabyMania,
לפי ה-`alt-placeholder-*` שהוגדרו במאמר על ידי הסופר.

הסוכן מחליף את ה-placeholders בתמונות אמיתיות שנוצרות ב-Stitch,
ומעדכן את ה-Markdown **רק לאחר אישור אייל**.

---

## 2. מיקום בפייפליין

```
כתיבת מאמר (agent 04)
        ↓
QA מאמר (organic-article-qa.md)
        ↓
[ARTICLE IMAGE AGENT] ← כאן
        ↓
אישור אייל → עדכון Markdown
        ↓
Publish (publish script)
        ↓
GSC indexing
```

**חשוב:** הסוכן עובד **לפני** publish ו**לאחר** QA.
לא נוגע ב-Shopify, לא עושה commit, לא push.

---

## 3. עבודה על batches — סדר עדיפויות

- עובד על מאמרים **PENDING** בלבד (לא על מאמרים שכבר פורסמו)
- מתחיל מ-**Batch 2** (Batch 1 כבר live)
- עובד batch אחד בכל פעם — לא כל 43 בבת אחת
- לאחר אישור תמונות batch → מעדכן Markdown → מוסר ל-publish

---

## 4. קלט

```
scripts/organic/generate_article_images.py --dry-run --batch 2
scripts/organic/generate_article_images.py --dry-run --article output/organic/hub16-crocs/HUB16_C1.md
scripts/organic/generate_article_images.py --generate --article output/organic/hub16-crocs/HUB16_C1.md
```

| פרמטר | תיאור |
|-------|-------|
| `--dry-run` | מדפיס prompts ומניפסט בלבד — אין יצירה |
| `--generate` | מפעיל Stitch ומוריד תמונות |
| `--batch N` | מריץ על כל מאמרי ה-batch לפי publish-schedule-43.md |
| `--article PATH` | מריץ על מאמר ספציפי |
| `--update-md` | מעדכן Markdown עם נתיבי תמונות (רק לאחר אישור) |

---

## 5. פלט

### תמונות
נשמרות ב: `output/organic/{hub-folder}/images/{slug}-{placeholder-id}.jpg`

דוגמה:
```
output/organic/hub16-crocs/images/crocs-leyeladim-madrih-male-mida-dagamim-hero.jpg
output/organic/hub16-crocs/images/crocs-leyeladim-madrih-male-mida-dagamim-pool.jpg
```

### Manifest JSON
נשמר ב: `output/organic/image-manifests/batch-{N}-manifest.json`

```json
{
  "batch": 2,
  "generated_at": "2026-05-21T...",
  "mode": "dry-run",
  "articles": [
    {
      "file": "hub16-crocs/HUB16_Pillar.md",
      "slug": "crocs-leyeladim-madrih-male-mida-dagamim",
      "title": "קרוקס לילדים — המדריך המלא",
      "images": [
        {
          "placeholder_id": "hero",
          "alt_text": "ילד קטן עומד בגינה בקרוקס...",
          "image_type": "hero",
          "prompt": "...",
          "output_path": "...",
          "status": "PLANNED"
        }
      ]
    }
  ]
}
```

### Markdown מעודכן (רק לאחר --update-md + אישור)
```markdown
<!-- לפני -->
![alt text](alt-placeholder-hero)

<!-- אחרי -->
![alt text](images/slug-hero.jpg)
```

---

## 6. חוקי סגנון BabyMania — Visual Contract

### סגנון חובה
- **premium Israeli baby boutique** — בוטיק תינוקות ישראלי איכותי
- **צבעי ליבה:** soft cream (#FAF7F4), warm beige (#F2EBE2), muted gold (#C4876A)
- **editorial lifestyle photography** — צילום חיים, לא קטלוגי
- **natural light** — אור טבעי, חלון, בוקר/צהריים רך
- **realistic baby/kids environment** — חדר אמיתי, גינה אמיתית, לא סטודיו
- **warm and calm** — חמים, שקט, מרגיע

### אסור בתמונות
| חוק | הסבר |
|-----|-------|
| no cheap AI look | לא תמונה גנרית שנראית מזויפת |
| no distorted hands | ידיים נורמליות בלבד |
| no unreadable text | אם יש טקסט בתמונה — חייב להיות קריא |
| no logos / no brand text | אסור לוגו כלשהו |
| no random text in image | אסור טקסט אקראי |
| no scary baby faces | פנים תינוק רגועות, לא מבועתות |
| no unsafe baby sleep scenes | ראה סעיף בטיחות |
| no messy background | רקע נקי ומאורגן |
| no plastic stock image style | לא תמונות סטוק גנריות |
| no dark/dramatic lighting | תמיד אור חם ורך |

---

## 7. חוקי בטיחות — Safety Contract

| כלל | תיאור |
|-----|-------|
| **שינה בטוחה** | תינוק ישן = בבגד שינה בלבד, סדין מתוח, **ללא שמיכה, ללא כרית, ללא ממולאים** |
| **תינוק בסיכון** | אסור לתאר תינוק בסיכון גופני — גבוה מדי, ליד מדרגות ללא השגחה |
| **טענות רפואיות** | אסור תמונה שמרמזת על טיפול רפואי עצמי או מסר רפואי |
| **טקסט בתמונה** | אסור להכניס טקסט לתוך התמונה — לא כותרות, לא מספרים |
| **flag HUB8 crib** | `alt-placeholder-crib` במאמר HUB8_C6 מכיל "שמיכה רכה" — **MUST OVERRIDE** prompt להסיר שמיכה |

---

## 8. גדלים מומלצים

| סוג | יחס | מינ׳ px | שימוש |
|-----|-----|---------|-------|
| hero | 16:9 | 1200×675 | featured image, OG |
| body | 4:3 | 800×600 | in-article |
| square | 1:1 | 600×600 | product mention |

> Stitch מייצר ב-1024×1024 ברירת מחדל — תמיד לבקש landscape עבור hero.

---

## 9. QA לתמונות — Image QA Checklist

לפני `--update-md` ולפני publish:

| # | בדיקה |
|---|-------|
| 1 | לפחות 2 תמונות למאמר (לא 1, לא 0) |
| 2 | כל placeholder הוחלף או דווח SKIPPED |
| 3 | לכל תמונה alt text בעברית (≥10 מילים) |
| 4 | אין קובץ חסר (כל output_path קיים) |
| 5 | אין נתיב שבור בMarkdown |
| 6 | אין תמונות מ-dry-run במאמר אמיתי |
| 7 | אין publish live לפני אישור אייל |
| 8 | תמונת crib/sleep עברה safety review |

---

## 10. הגדרת סוגי תמונות

| סוג | תיאור | דוגמה ל-prompt |
|-----|-------|---------------|
| `hero` | תמונה ראשית, landscape, סצנה רחבה | "Israeli living room, toddler in crocs..." |
| `body` | תמונה בגוף המאמר, פרטנית יותר | "Close-up of crocs sandals on child..." |
| `product` | תמונת מוצר על רקע ניטרלי | "Baby shoes on white marble surface..." |
| `explanatory` | תמונה שמסבירה מושג | "Diagram-style photo of heel strap..." |

סוג נקבע לפי שם ה-placeholder:
- `hero` → type=hero
- `floor`, `pool`, `bench`, `care`, `fit`, `crib` וכו' → type=body
- `product`, `pair` → type=product
- `ticks-visual`, `diagram` וכו' → type=explanatory

---

## 11. מבנה prompt סטנדרטי

```
[STYLE PREFIX]
Editorial lifestyle photography for a premium Israeli baby boutique.
Soft cream, warm beige, muted gold color palette.
Natural window light, warm and calm atmosphere.
Realistic home or outdoor environment, not a studio.
No text, no logos, no distorted hands.

[SUBJECT — from alt text + *alt:* description]
{alt_text_detailed}

[SAFETY MODIFIERS if needed]
Baby sleeping safely: no blankets, no pillows, fitted sheet only.
```
