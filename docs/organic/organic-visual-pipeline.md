# BabyMania Organic Visual Pipeline — Spec v1.0

> **סטטוס:** SPEC ONLY — לא בוצע עדיין  
> **עדכון:** 2026-05-31  
> **מטרה:** הגדרת תהליך אחיד להוספת תמונות לכל מאמר אורגני לפני פרסום

---

## 1. מבנה כללי

```
source MD file
     │
     ├── [A] Product Image Processor
     │       ├── fetch CDN URL from Shopify product handle
     │       ├── select best image (primary or by type)
     │       └── inject <img> into source MD
     │
     ├── [B] AI/Stitch Image Generator  ← T1 approval required per article
     │       ├── generate via Stitch (GEMINI_3_FLASH preferred)
     │       ├── QA visual output
     │       └── upload to Shopify CDN → inject <img>
     │
     └── bm_html_converter.py → Shopify publish
```

**כלל ברירת מחדל:**  
השתמש ב-[A] לכל מאמר שיש לו `target_product_handle` בפרונטמטר.  
השתמש ב-[B] רק כשאין מוצר מקושר או כשהמוצר חסר תמונה ב-CDN — ואך ורק אחרי אישור T1 מפורש.

---

## 2. Product Image Processor [A]

### 2.1 זרימת העבודה

```python
# pseudocode
handle = fm['target_product_handle'].lstrip('/products/')
product = shopify_get(f"/products.json?handle={handle}&fields=images")
if not product or not product['images']:
    STOP → report IMAGE_UNAVAILABLE
primary_image = product['images'][0]['src']   # תמיד התמונה הראשונה = primary
inject_hero_img(md_file, primary_image, alt_text_he)
```

### 2.2 מיקום ה-inject בקובץ MD

| מבנה המאמר | מיקום inject |
|------------|-------------|
| אין `## מבוא` — section ראשון תיאורי | אחרי שורת H2 ולפני פסקה ראשונה |
| יש `## מבוא` — section מבוא קיים | אחרי H2 הגוף הראשון שאינו מבוא |
| Pillar article (1500+ מילים) | אחרי section ראשון (לפני section שני) |

**פורמט HTML:**
```html
<img src="https://cdn.shopify.com/..." alt="[alt text עברית]" class="article-hero-img" loading="lazy">
```

### 2.3 ALT Text — כללים

- בעברית בלבד
- מתאר: מוצר + שימוש + גיל/סיטואציה
- אורך: 80–160 תווים
- ללא מילות מפתח כפולות (לא "SEO stuffing")
- דוגמה טובה: `נעלי דיסני אלזה עם אורות LED לבנות — עיצוב ורוד-סגול, מידות 22–35`
- דוגמה גרועה: `נעלי אורות נעלי LED נעלי ילדים`

### 2.4 Image Selection Rules — Shopify CDN

| מצב | חוק |
|-----|-----|
| מוצר עם 1+ תמונות | השתמש ב-`images[0]` (primary) |
| מוצר עם 0 תמונות | STOP — דווח `NO_CDN_IMAGE`, אל תפרסם |
| handle = `MANUAL_NO_PRODUCT_AVAILABLE` | SKIP image inject — דווח למשתמש |
| URL לא מ-cdn.shopify.com | REJECT — אין להשתמש בתמונות חיצוניות |
| תמונה בפורמט `.gif` | SKIP — gif לא מתאים לhero |

### 2.5 Image Crop / Resize Rules

Shopify CDN תומך ב-URL parameters לשינוי גודל:

```
# הוסף לurl: ?width=N&height=N&crop=center
# דוגמה:
https://cdn.shopify.com/s/files/.../image.webp?v=123&width=800&crop=center
```

| שימוש | width | height | crop |
|-------|-------|--------|------|
| Hero article (desktop) | 800 | ללא | — |
| Hero article (mobile) | 400 | ללא | — |
| Thumbnail | 400 | 400 | center |
| Flat-lay product | 600 | 600 | center |

**כלל:** אל תוסיף crop params לhero image ב-MD — השאר URL מלא.  
הbrowser יבצע responsive scaling דרך CSS (`max-width: 100%; height: auto`).

---

## 3. AI/Stitch Image Generator [B]

### 3.1 תנאים לשימוש

- `target_product_handle` = `MANUAL_NO_PRODUCT_AVAILABLE` **או** המוצר חסר תמונות CDN
- **T1 approval מפורש** מאייל לפני כל גנרציה
- גנרציה מחוץ ל-batch flow הרגיל — מאמר ספציפי בלבד

### 3.2 זרימת העבודה

```
1. T1 approval received (user message: "approved stitch for [HUB/article]")
2. Generate via mcp__stitch__generate_screen_from_text
   - projectId: 8041267646426877 (BabyMania Premium project)
   - modelId: GEMINI_3_FLASH (מהיר, מספיק איכותי)
   - deviceType: DESKTOP
3. QA visual output (see checklist in image-prompt-checklist.md)
4. Upload image to Shopify CDN (separate task, T1 required)
5. Inject CDN URL into source MD
6. Run converter + QA + publish (normal batch flow)
```

### 3.3 שמירת תמונות שנוצרו

```
output/organic/ai-images/
  ├── [hub]-[article]-stitch-[date].json   ← metadata (screen ID, prompt, URL)
  └── [hub]-[article]-stitch-[date].url    ← CDN URL after upload
```

### 3.4 מגבלות Stitch

- Stitch יוצר UI screens, לא תמונות standalone — השתמש ב-`screenType: IMAGE` prompt
- Timeout שכיח — אם timeout: `list_screens` → חפש screen חדש → `get_screen`
- אל תנסה שוב מיד אם timeout — המתן ובדוק
- תמונות Stitch לא עולות אוטומטית ל-CDN — שלב upload נפרד נדרש

---

## 4. Premium BabyMania Visual Style

### 4.1 סגנון כללי

| מאפיין | כלל |
|--------|-----|
| תאורה | אור טבעי / בוקר / צהריים בהיר — ללא פלאש, ללא מוצלל |
| פלטה | לבן חם, קרם, בז', עץ בהיר, פסטל עדין |
| רקע | מינימליסטי — קיר לבן / רצפת עץ / שטיח עדין |
| קומפוזיציה | subject ברור, whitespace נדיב, ללא עומס |
| גיל מוצג | תואם לנושא המאמר (תינוק 0–6 חודשים / פעוט 1–3 / ילד 3–7) |
| אסתטיקה | Scandinavian family lifestyle, Israel modern home |

### 4.2 לפי סוג מאמר

| סוג מאמר | סוג תמונה מומלץ |
|----------|----------------|
| Cluster (נישה ספציפית) | product flat-lay או ילד עם המוצר |
| Pillar (מדריך מלא) | lifestyle scene — הורה + ילד בסיטואציה |
| Comparison article | 2 מוצרים זה לצד זה על רקע נקי |
| Safety/tips article | close-up hands/feet, תמונה עדינה לא מפחידה |
| Seasonal article | scene עם background של העונה |

### 4.3 מה אסור

- ❌ תמונות stock גנריות (Shutterstock feel)
- ❌ צבעים רווים מדי / פילטרים כבדים
- ❌ ילדים עם פנים מעוותות / ידיים לא ריאליות
- ❌ רקע עמוס / messy
- ❌ לוגואים / טקסט בתמונה
- ❌ תאורה כהה / dramatic / moody
- ❌ תמונות מ-AliExpress ישירות (חוסר אמינות ויזואלית)

---

## 5. QA Checks — לפני inject

```python
def qa_image(img_url, alt_text, article_type):
    checks = [
        ('img-url-cdn',        img_url.startswith('https://cdn.shopify.com/'), ''),
        ('img-url-not-gif',    not img_url.endswith('.gif'),                   ''),
        ('alt-hebrew',         any('֐' <= c <= '׿' for c in alt_text), ''),
        ('alt-length',         80 <= len(alt_text) <= 160,
                               f'{len(alt_text)} chars (need 80–160)'),
        ('alt-no-keyword-spam', alt_text.count(keyword) <= 2,                  ''),
        ('img-class-set',      'class="article-hero-img"' in img_html,         ''),
        ('loading-lazy',       'loading="lazy"' in img_html,                   ''),
    ]
    return checks
```

---

## 6. שילוב ב-Batch 5 — לפני publish

### 6.1 תהליך מלא

```
Batch 5 pre-publish checklist:
□ 1. כל 6 מאמרי Batch 5 נקראו — frontmatter target_product_handle מאומת
□ 2. Product Image Processor הופעל — כל מאמר קיבל CDN URL
□ 3. HUB-13/C5 טופל בנפרד (MANUAL_NO_PRODUCT_AVAILABLE)
□ 4. SEO meta gate — seo_title + seo_description נוספו לכל 6 מאמרים
□ 5. batch5.json נוצר
□ 6. dry-run: python publish_organic_batch.py --batch batch5.json
□ 7. כל 6 מאמרים: PASS (כולל SEO gate + img check)
□ 8. T1 approval מאייל: "APPROVED PUBLISH BATCH-5 — אורגני"
□ 9. live publish: python publish_organic_batch.py --batch batch5.json --live
□ 10. GSC indexing ידני — 6 URLs
```

### 6.2 HUB-13/C5 — טיפול מיוחד

`bgad-yam-livanim-tinokot-mah-amid-yoter` — `handle=MANUAL_NO_PRODUCT_AVAILABLE`

אפשרויות (בחירת אייל):
- **Option A:** חיפוש מוצר חלופי בחנות (`bgad yam` / swimwear boys) → החלפת handle
- **Option B:** הוצאת C5 מ-Batch 5 → publish 5 מאמרים
- **Option C:** שימוש ב-collections CTA (`/collections/all`) ← fallback ריק

---

## 7. Script — Product Image Processor (לפיתוח)

**מיקום:** `scripts/organic/inject_hero_images.py`  
**סטטוס:** PLANNED — לא נכתב עדיין

```python
# interface spec
def inject_hero_images(batch_json_path, dry_run=True):
    """
    For each article in batch:
    1. Read source MD, extract target_product_handle
    2. Fetch Shopify product images via REST API
    3. Select primary image
    4. Run image QA checks
    5. Inject <img> HTML into source MD at correct position
    6. Report: INJECTED / SKIP / NO_IMAGE per article
    Returns: list of results, all_pass bool
    """
```

**פרמטרים:**
- `--batch output/organic/batch5.json`
- `--dry-run` — בדיקה בלבד, ללא כתיבה לקבצי MD
- `--live` — כתיבה בפועל לקבצי MD

**output:**
```
[1/6] HUB-13/C2 — INJECTED: cdn.shopify.com/...jpeg
[2/6] HUB-13/C3 — INJECTED: cdn.shopify.com/...webp
[3/6] HUB-13/C4 — INJECTED: cdn.shopify.com/...webp
[4/6] HUB-13/C5 — SKIP: MANUAL_NO_PRODUCT_AVAILABLE
[5/6] HUB-13/C6 — INJECTED: cdn.shopify.com/...webp
[6/6] HUB-14/Pillar — INJECTED: cdn.shopify.com/...webp
IMAGE INJECTION: 5/6 PASS | 1 SKIP (manual)
```

---

## 8. הערות ואירועי עבר

- **2026-05-31 Batch 4:** hero images הוזרקו ידנית ל-6 מאמרים (C3–C6 + Pillar + C1) דרך inline Python script. כל 6: QA 13/13 PASS, len ratio 1.00.
- **2026-05-31 Stitch test:** תמונה אחת נוצרה ב-Stitch באופן לא מאושר בסשן זה (screen ID: `b293af6c758c43488623ca634ac06559`, project: 8041267646426877). התמונה **לא אושרה ולא שולבה** בשום מאמר. אין להשתמש בה עד לאישור מפורש.
