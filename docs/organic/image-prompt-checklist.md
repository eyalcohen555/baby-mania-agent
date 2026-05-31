# BabyMania Image Prompt Checklist — Spec v1.0

> **סטטוס:** SPEC ONLY — לא בוצע עדיין  
> **עדכון:** 2026-05-31  
> **שימוש:** לכל גנרציית תמונה ב-Stitch — לאחר T1 approval בלבד

---

## 1. תנאי סף לפני כל גנרציה

```
□ T1 approval received (user message מפורש: "approved stitch for [article]")
□ article_id + slug ידועים
□ נאמת: אין תמונת CDN מוצר זמינה (Product Image Processor נכשל)
□ article type מוגדר (cluster / pillar / comparison / seasonal)
□ target subject מוגדר (תינוק / פעוט / ילד + גיל משוער + מגדר אם רלוונטי)
```

---

## 2. Prompt Templates לפי סוג מאמר

### 2.1 Cluster — מאמר נישה מסחרי (intent: commercial)

```
Premium editorial hero image for BabyMania Israeli baby store.
Full-bleed photorealistic lifestyle scene — no UI, no text, no buttons.

Scene: [describe child age/gender using product in realistic home setting]
Setting: bright minimalist Israeli living room / kitchen / garden.
Lighting: natural morning daylight, warm soft fill, no harsh shadows.
Background: softly blurred — white walls / light wood floor / linen curtains.
Composition: close-medium shot, clean framing, subject clearly visible.

Style: premium baby brand catalog photography. Think Petit Bateau or Mamas & Papas editorial.
Color palette: warm whites, soft cream, natural wood, gentle pastel accents.
No logos, no text, no watermarks, no unrealistic anatomy.
```

**דוגמה — מאמר נעלי מים לתינוק:**
```
Premium editorial hero image for BabyMania Israeli baby store.
Full-bleed photorealistic lifestyle scene — no UI, no text, no buttons.

Scene: Toddler (18 months, gender-neutral, realistic proportions) sitting at the edge 
of a small inflatable backyard pool, wearing soft mesh water sandals in light blue. 
Parent's hands gently support the child. Feet visible in gentle focus.
Setting: bright Israeli backyard, summer afternoon, natural greenery in background.
Lighting: soft diffused sunlight, warm tones, no harsh shadows.
Background: blurred — green lawn, light fence, sunny sky.
Composition: medium shot, eye-level with child.

Style: premium baby brand catalog photography.
Color palette: sky blue, cream, natural green, warm whites.
No logos, no text, no watermarks, no extra fingers, no distorted feet.
```

---

### 2.2 Pillar — מדריך מלא (intent: informational + commercial)

```
Premium editorial lifestyle photograph for BabyMania Israeli baby store.
Full-bleed photorealistic — no UI chrome, no text, no buttons.

Scene: Israeli parent (realistic, natural look) with child aged [X], 
engaged in [activity related to article topic].
Setting: [relevant home location — bathroom/bedroom/living room/outdoor].
Lighting: natural daylight, bright and airy, golden hour warmth.
Background: softly blurred, clean and uncluttered.
Composition: medium-wide shot, emotional connection visible, room to breathe.

Style: high-end family lifestyle editorial. Warm minimalism.
Color palette: [article-specific palette — see section 3].
Emotional tone: calm, trustworthy, nurturing, aspirational.
No logos, no text overlays, no staged stock-photo feeling.
```

---

### 2.3 Comparison Article (A vs B)

```
Premium product comparison flat-lay for BabyMania Israeli baby store.
Full-bleed photorealistic — no UI, no text, no labels.

Scene: Two [product type] side by side on a light natural surface 
(white marble / light wood / soft linen fabric).
Left product: [description of option A].
Right product: [description of option B].
Small natural props: a sprig of eucalyptus, a neutral wooden toy.
Lighting: soft studio-style natural light from above, no shadows between products.
Background: clean, white or very light cream.
Composition: centered, equal space for both products, top-down or 35-degree angle.

Style: premium ecommerce product photography, editorial quality.
Color palette: whites, cream, neutral wood.
No text, no price tags, no logos, no unrealistic colors.
```

---

### 2.4 Safety / Tips Article

```
Premium soft editorial image for BabyMania Israeli baby store.
Full-bleed photorealistic — no UI, no text.

Scene: [Specific safe, reassuring scene related to topic].
Emphasis on: hands, gentle touch, safe environment.
Avoid: anything that looks clinical, scary, or hospital-like.
Lighting: warm, very soft, calming.
Background: bedroom / living room — clean and safe-looking.
Composition: close-up or medium, focus on action not face.

Style: reassuring parent-guide editorial. Calm and trustworthy.
Color palette: soft pastels, cream, warm white.
No text, no scary imagery, no unrealistic anatomy.
```

---

### 2.5 Seasonal Article (קיץ / חורף)

```
Premium seasonal lifestyle editorial for BabyMania Israeli baby store.
Full-bleed photorealistic — no UI, no text, no logos.

Season: [קיץ / חורף ישראלי]
Scene: [age-appropriate child in seasonal setting with relevant product].

SUMMER: bright outdoor scene, natural light, pool/beach/garden, soft shadows.
WINTER: warm indoor scene, natural light through window, cozy textures.

Lighting: season-appropriate — summer: bright diffused sunlight / winter: golden window light.
Color palette: [season palette — summer: blues/whites/yellows; winter: creams/terracotta/sage].
No logos, no text, no staged feel, no unsafe situations.
```

---

## 3. Color Palettes לפי נושא

| נושא | Primary | Secondary | Accent |
|------|---------|-----------|--------|
| נעלי ילדים | קרם, עץ בהיר | לבן חם | כחול פסטל / ורוד עדין |
| בגדי תינוק | לבן רך, קרם | בז' | ירוק מנטה / לילך |
| אמבטיה | לבן, תכלת עדין | עץ במבוק | כחול ים עדין |
| שינה / לילה | אפור עדין, לבן | מוקה חם | לוונדר / קרם |
| קיץ / ים | לבן, צהוב חמאה | תכלת | ירוק עשב |
| חורף | אוף-וויט, פלנל | קרמל | ירוק זית / חרדל עדין |
| ריבורן / בובות | קרם, אפור בהיר | לבן | זהב עדין |

---

## 4. Negative Prompts — מה לכלול תמיד

הוסף לכל prompt:

```
No logos, no text overlays, no watermarks, no brand marks.
No distorted hands, no extra fingers, no unrealistic feet or faces.
No dark moody lighting, no harsh shadows, no dramatic contrast.
No generic stock-photo feel, no over-saturated colors.
No messy or cluttered backgrounds.
No hospital or clinical setting.
No unsafe situations involving children.
No ethnically ambiguous forced diversity — use natural realistic Israeli family look.
```

---

## 5. QA Checklist — אחרי גנרציה

### 5.1 Visual QA (צפייה ידנית)

```
□ אין טקסט בתמונה
□ אין לוגו / watermark
□ ידיים ורגליים ריאליות (ספירת אצבעות)
□ פנים ילד/תינוק ריאליות (לא AI-uncanny)
□ תאורה טבעית ורכה — לא moody / לא פלאש
□ רקע נקי ולא עמוס
□ קומפוזיציה ברורה — subject מזוהה מיד
□ פלטת צבעים תואמת BabyMania style
□ מרגיש כמו catalog premium — לא stock photo
□ אין אלמנטים מסוכנים / לא מתאימים לילדים
```

### 5.2 Technical QA

```
□ image URL תקף (HTTP 200)
□ URL מ-Shopify CDN (לאחר upload) — cdn.shopify.com
□ פורמט: webp / jpg (לא gif)
□ גודל קובץ: < 500KB לhero (< 200KB לthumbnail)
□ alt text בעברית, 80–160 תווים
□ class="article-hero-img" בHTML
□ loading="lazy" בHTML
□ אין alt-placeholder בHTML הסופי
```

### 5.3 Pipeline QA (אחרי inject)

```
□ dry-run: python publish_organic_batch.py --batch [file] → PASS
□ no-placeholder check: PASS
□ has-img check: PASS (CDN URL קיים בHTML)
□ 13/13 QA checks: PASS
□ len ratio: 0.90–1.10 (vs baseline)
```

---

## 6. Logging — מה לתעד

לכל תמונה שנוצרה ב-Stitch, תעד ב-`output/organic/ai-images/`:

```json
{
  "date": "2026-05-31",
  "article": "HUB-13/C5",
  "slug": "bgad-yam-livanim-tinokot-mah-amid-yoter",
  "stitch_project_id": "8041267646426877",
  "stitch_screen_id": "b293af6c...",
  "prompt_template": "seasonal",
  "model": "GEMINI_3_FLASH",
  "status": "APPROVED / REJECTED / PENDING",
  "shopify_cdn_url": null,
  "injected_into_md": false,
  "approved_by": "Ayal",
  "notes": ""
}
```

---

## 7. Stitch Usage Log — Session 2026-05-31

| תמונה | Screen ID | סטטוס |
|-------|-----------|-------|
| Accidental test — לא מאמר ספציפי | `b293af6c758c43488623ca634ac06559` | ❌ NOT APPROVED — לא לשימוש |

**הערה:** תמונה זו נוצרה בסשן 2026-05-31 ללא אישור T1. אין להשתמש בה בשום מאמר עד לאישור מפורש.

---

## 8. אינטגרציה ב-Batch 5

### סדר עבודה נכון לפני publish:

```
שלב 1: SEO Meta
  → הוסף seo_title + seo_description לכל 6 קבצי MD

שלב 2: Hero Images
  → הפעל inject_hero_images.py (כשיפותח) על batch5.json
  → או: inject ידנית לכל מאמר (כמו ב-Batch 4)
  → HUB-13/C5: קבל החלטה (מוצר חלופי / הוצאה / fallback)

שלב 3: Dry-run
  → python publish_organic_batch.py --batch output/organic/batch5.json
  → ציפייה: 5–6/6 PASS (תלוי בהחלטה על C5)

שלב 4: T1 Approval מאייל
  → "APPROVED PUBLISH BATCH-5 — אורגני"

שלב 5: Live publish
  → python publish_organic_batch.py --batch output/organic/batch5.json --live

שלב 6: GSC indexing ידני — 6 URLs
```
