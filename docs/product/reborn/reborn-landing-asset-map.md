# Reborn Landing Asset Map

**תפקיד:** מפת נכסים ויזואליים לדף נחיתה ריבורן
**נוצר:** 2026-04-27
**כפוף ל:** `REBORN-MASTER-PROMPT.md` → `BABYMANIA-MASTER-PROMPT.md`

---

## Status

**S1 Hero — DONE (local preview only).**
Desktop + Mobile hero images נוצרו, אושרו ויזואלית על ידי אייל, ומחוברות לפריוויו המקומי (2026-04-27).
Shopify live לא נגע. שאר ה-assets: planning only — לא לייצר לפני אישור אייל.

---

## 1. Asset Rules

| כלל | פרוט |
|---|---|
| Hero / lifestyle | מותר AI — לשימוש כ-mood/brand visual בלבד. אינו מוכיח מוצר ספציפי. |
| הסבר חומרים / סוג גוף | תמונת ספק / מוצר אמיתית בעדיפות — אם מוצגת כהסבר פיזי. |
| כרטיסי מוצר | תמונת מוצר אמיתית בלבד — ללא יוצא מן הכלל. |
| ביקורות / וידאו | מותר כהמחשה ויזואלית — אסור להציג כ-UGC אמיתי אלא אם הוא כזה. חובה לתייג: "תגובות אמיתיות של לקוחות, מוצגות בהמחשה ויזואלית". |
| אביזרים | אין להציג אביזר שאין לו מלאי אמיתי. |
| טקסט / לוגו בתמונה | אסור ב-AI image ללא אישור נפרד. |
| פלטה | כל תמונה חייבת להיות במגמה חמה / קרם / נחושת — תואמת BabyMania palette. |
| AliExpress | לא לציין כמקור בשום תמונה או כיתוב. |
| **Card image ratio (מכאן והלאה)** | **כרטיסים / cards: 1:1 ברירת מחדל — 900×900 WebP. גרסה קלה: 768×768 WebP. לא מייצרים desktop/mobile נפרד לכרטיסים אלא אם יש סיבה חריגה.** |
| **Existing assets — ללא שינוי** | Hero desktop/mobile, S3 gift, S5 lifestyle — אינם מושפעים. כלל ה-1:1 חל מכאן והלאה בלבד. |

---

## 2. Section-by-Section Asset Map

---

### S1 — HERO

| שדה | פרוט |
|---|---|
| **Asset needed** | תמונה ראשית: 2–4 בובות ריבורן על ספה, אווירת בית חם |
| **Asset type** | AI — mood/brand image בלבד |
| **Purpose** | פתיחת חלום — "זה מוצר ביתי, חם, יוקרתי — לא Amazon" |
| **Visual direction** | ספה בצבע בז'/קרם, תאורה טבעית, עומק שדה רך, בובות מסודרות לא מדויקות |
| **What it must NOT imply** | אלו המוצרים המדויקים שנמכרים / אריזה / לוגו / ילד/ה מזוהה |
| **Priority** | **HIGH — קובע את כל השפה הוויזואלית** |
| **STATUS** | ✓ DONE — local preview only (2026-04-27) |
| **Desktop file** | `assets/reborn/landing/reborn-hero-desktop.webp` — 1920×960 |
| **Mobile file** | `assets/reborn/landing/reborn-hero-mobile.webp` — 768×960 |
| **Source** | ChatGPT Image — 3 בובות על ספה. Desktop: 1774×887 → scaled. Mobile: 1122×1402 → scaled. ללא חיתוך (יחסי aspect ratio תואמים). |
| **Connected to** | `output/pages/reborn-landing/reborn-landing-preview.html` — `<picture>` + `<source media="(max-width: 768px)">` |
| **Shopify** | לא נגע |

---

### S2 — Trust Promise

| שדה | פרוט |
|---|---|
| **Asset needed** | אלמנט ויזואלי לבטחון — badge / seal / CSS element |
| **Asset type** | CSS visual element (no external image required) |
| **Purpose** | להפוך את ההבטחה "כמו בתמונות — אחרת החזר" לאלמנט ויזואלי מרשים |
| **Visual direction** | עיגול נחושת עם ✓ / מגן CSS / קו עיטור עדין |
| **What it must NOT imply** | תעודת בטיחות / אישור צד שלישי / ביקורות ספציפיות |
| **Priority** | MEDIUM — כבר ממומש ב-CSS בpreview |

---

### S3 — למה לא הכי יקרה

| שדה | פרוט |
|---|---|
| **Asset needed** | תמונת lifestyle: הורה/סבתא עם ילדה, בחירת מתנה, אווירת בית |
| **Asset type** | AI — lifestyle/gift mood image |
| **Purpose** | לתמוך במסר "מתאים לילדים — לא לאספנים" בלי להגיד זאת בטקסט |
| **Visual direction** | אמא ביתית חמה עם בובה ביד / בחירת מתנה על שולחן / תאורה רכה |
| **What it must NOT imply** | זה מוצר זול / אריזת חנות / סצנה מסחרית |
| **Priority** | MEDIUM |

---

### S4 — הסבר סוגי גוף

| שדה | פרוט |
|---|---|
| **Asset needed — כרטיס 1 (גוף בד)** | תמונת בובה עם גוף בד מוחזקת בחיבוק |
| **Asset needed — כרטיס 2 (גוף סיליקון)** | תמונת בובה סיליקון — אפשר עם מים / מקלחת קטנה |
| **Asset type** | תמונת ספק / מוצר אמיתית בעדיפות — זהו הסבר פיזי ולא אווירה |
| **Purpose** | להסביר את ההבדל הפיזי החזותי בין שני הסוגים |
| **Visual direction** | תמונות נקיות על רקע בהיר / לבן. כרטיס 1: חיבוק. כרטיס 2: מים/ניקיון. |
| **What it must NOT imply** | "סיליקון מלא" / "Medical-grade" / "בטוח לשימוש רפואי" |
| **Source note** | PID 9689589383481 — ספקית אישרה תמונות אמיתיות ל-fabric + silicone girl. silicone boy — ממתין לאישור. |
| **Target size** | 900×900 WebP (1:1) |
| **Fabric file** | `assets/reborn/landing/reborn-s4-fabric-body.webp` — ✓ CONNECTED (local, 2026-04-27) |
| **Silicone file** | `assets/reborn/landing/reborn-s4-silicone-body.webp` — ✓ CONNECTED (local, 2026-04-27) |
| **Priority** | HIGH — הסבר ישיר על חומר, חייב תמונה אמיתית |

---

### S5 — חוויית משחק וטיפול

| שדה | פרוט |
|---|---|
| **Asset needed** | תמונת lifestyle: ילדה (4–8) מחבקת/מטפלת בבובה ריבורן |
| **Asset type** | AI — lifestyle mood image |
| **Purpose** | לגשר על הרגש — "הרגע שהפנים שלה ידלקו" |
| **Visual direction** | ילדה על ספה / שטיח, בובה בחיק, תאורה טבעית ביתית, צבעי קרם/חמים |
| **What it must NOT imply** | הבובה הספציפית שנמכרת / שיוך UGC / הילדה היא לקוחה אמיתית |
| **Priority** | HIGH — הסקשן הרגשי המרכזי, ריק בלי תמונה |
| **IMAGE STATUS** | ✓ Desktop approved (2026-04-27) — ילדה מחבקת בובת ריבורן עם אוזני ארנב, אינטריאור קרם |
| **IMAGE STATUS** | ✓ Mobile approved (2026-04-27) — אותה קומפוזיציה, פורמט אנכי |
| **VIDEO STATUS** | ⛔ POSTPONED — S5 video attempted via `models/veo-3.0-fast-generate-001` (2026-04-27) |
| **VIDEO FAILURE** | `429 RESOURCE_EXHAUSTED` — Veo quota 0/0. כרטיס אשראי תוקן אך Veo עדיין חסום. Gemini/Imagen — מכסות תקינות. |
| **VIDEO ROOT CAUSE** | Veo quota אפסי ב-Google AI Studio — לא בעיית קוד / תמונה / פרומפט. מחייב חקירה נפרדת. |
| **VIDEO DECISION** | S5 נשאר כתמונה בלבד. דף הנחיתה לא עוצר בגלל הווידאו. |
| **VIDEO FOLLOW-UP** | משימה פתוחה: לבדוק איך פותחים/מתקנים Veo quota עבור Google AI Studio / Gemini API. |
| **Script** | `_reborn_s5_video_test.py` — שמור ב-root, לא committed, מוכן לריצה חוזרת כשיש quota |
| **PREVIEW FILE** | `assets/reborn/landing/reborn-s5-lifestyle.webp` — 800×1000 WebP — מחובר ל-preview (local only) |
| **PREVIEW STATUS** | ✓ CONNECTED — `output/pages/reborn-landing/reborn-landing-preview.html` S5 section. Shopify לא נגע. |

---

### S6 — לקוחות שרכשו מספרים (Video Reviews)

| שדה | פרוט |
|---|---|
| **Asset needed** | 4 קטעי וידאו קצרים — 5–10 שניות כל אחד, פורמט 9:16 אנכי |
| **Asset type** | CapCut — המחשה ויזואלית מבוססת ביקורות אמיתיות |
| **Purpose** | הוכחה חברתית — לקוחות שרכשו מספרים |
| **Visual direction** | בובה בידיים / אריזה נפתחת / ילדה מחבקת — אנכי 9:16, תנועה עדינה |
| **What it must NOT imply** | "לקוח מצלם בעצמו" אם אין UGC אמיתי. חובה לתייג: "תגובות אמיתיות של לקוחות, מוצגות בהמחשה ויזואלית" |
| **Source** | 40 ביקורות AliExpress קיימות (Phase 2 בדוח) — לבחור 4 |
| **Blocker** | spec טכני לסקשן לא מאושר עדיין |
| **Priority** | HIGH — אך חסום עד spec + videos |

---

### S7 — שער קטגוריות ריבורן

| שדה | פרוט |
|---|---|
| **Asset — כרטיס 1: כל הבובות שלנו** | תמונת קטגוריה: 2–3 בובות ריבורן יחד — mood |
| **Asset — כרטיס 2: אביזרים לבובות** | תמונת קטגוריה: אביזר ריבורן (שמיכה / מנשא / בקבוק) |
| **Asset — כרטיס 3: מדריכי ריבורן** | תמונת קטגוריה: ספר / מגזין על שולחן / mood editorial |
| **Asset type** | AI allowed — category card backgrounds (illustrative) |
| **Purpose** | כניסה קלה לכל נושא — גייטוויי ויזואלי |
| **What it must NOT imply** | אביזרים זמינים בפועל אם אין מלאי / מוצרים ספציפיים לפני PHASE 5 |
| **Target size (future)** | **900×900 WebP (1:1) לכל כרטיס — כלל card ratio החדש** |
| **Priority** | MEDIUM — כרטיס 2 חסום עד שיש מלאי אביזרים |

---

### S8 — FAQ

| שדה | פרוט |
|---|---|
| **Asset needed** | ככל הנראה אין תמונה — accordion טקסטואלי בלבד |
| **Asset type** | CSS decorative element אופציונלי (עיטור עדין / ספריייה icon) |
| **Purpose** | רגיעה ויזואלית לפני CTA — לא לעמוס |
| **Priority** | LOW |

---

### S9 — CTA סופי

| שדה | פרוט |
|---|---|
| **Asset needed** | רקע gradient בלבד — או crop עדין מתמונת ה-Hero |
| **Asset type** | CSS gradient / reuse Hero image crop |
| **Purpose** | סגירה רגשית — לא להוסיף עומס חדש |
| **What it must NOT imply** | לחץ / urgency / מחיר |
| **Priority** | LOW — gradient CSS מספיק |

---

## 3. Hero Image Brief

**תמונה לבריף לגנרטור AI:**

```
Style:     Warm Scandinavian nursery / premium home interior
Mood:      Soft, intimate, cozy — not commercial
Setting:   Light beige/cream sofa or armchair, warm afternoon light
Content:   2–4 reborn baby dolls resting together on the sofa
           Dolls look peaceful and realistic — no unsettling expressions
           No children, no adults, no hands
Colors:    Warm cream, soft caramel, ivory, blush — no greens, no blues
Lighting:  Natural window light from the right, golden-hour warmth
Depth:     Shallow depth of field — background softly blurred
Aspect:    16:9 desktop primary / also export 1:1 for mobile crop
DON'T:     No product packaging / no price tags / no logos / no text
           No specific brand markings / no AliExpress-style flat lay
           Do not show this as a product shot — it's a brand mood image
Palette:   #FFFDF9 bg / #F5EDE4 sofa / #D4B99A accent tones
```

---

## 4. Assets That Must Be Real (No AI Substitutes)

| Asset | סיבה |
|---|---|
| תמונות כרטיסי מוצר (S7 doll grid) | הלקוח קונה מה שרואה — חייב תמונת מוצר אמיתית |
| תמונות סוג גוף (S4) | הסבר פיזי — תמונת AI לא יכולה לייצג חומר אמיתי |
| תמונות SKU בדפי מוצר (מחוץ ל-landing) | הוכחת מוצר — חייב תמונה מהספק |
| כל תמונה שמוצגת עם טקסט "תמונה אמיתית של המוצר" | חובה משפטית + אמינות |
| וידאו ביקורת שמוצג כ-UGC | רק אם יש UGC אמיתי — אחרת חובה label המחשה |

---

## 5. Assets We Can Generate With AI

| Asset | הערה |
|---|---|
| Hero mood image | אווירה בלבד — לא מוצר |
| Lifestyle gift / child caring image (S5) | ילדה + בובה — mood, לא אימות |
| Category card backgrounds (S7 כרטיסים 1+3) | illustrative — לא כרטיס 2 אם אין אביזרים |
| CTA visual | gradient CSS מספיק / crop מ-Hero |
| Price positioning image (S3) | הורה בוחר מתנה — אווירה |

---

## 6. Missing Assets Checklist

```
PRIORITY HIGH:
[x] Hero image — Desktop 1920×960 + Mobile 768×960 — נוצר ואושר לפריוויו מקומי (2026-04-27)
[x] Lifestyle image — Desktop + Mobile approved (S5) — 2026-04-27
[ ] Lifestyle VIDEO — S5 ⛔ BLOCKED (Veo quota 0/0) — fallback: תמונה / CapCut manual
[x] Body type images — fabric + silicone (S4) — 900×900 WebP, מחוברים לפריוויו (2026-04-27)
[ ] Review videos × 4 — CapCut, 5–10s, 9:16 (S6) — תלוי ב-spec אישור

PRIORITY MEDIUM:
[x] Lifestyle / gift image — S3 approved + connected to preview (2026-04-27) — reborn-s3-gift-lifestyle.webp 1000×600
[ ] Category card image — "כל הבובות שלנו" (S7)
[ ] Category card image — "מדריכי ריבורן" (S7)

PRIORITY LOW / BLOCKED:
[ ] Product images × 6 dolls (S7 future doll grid) — ממתין ל-PHASE 5 + Hebrew names
[ ] Category card image — "אביזרים" (S7) — חסום עד שיש מלאי
[ ] CTA visual — gradient CSS מספיק לעכשיו
[ ] FAQ decorative element — לא חובה

EXTERNAL DECISION REQUIRED:
[ ] אייל: האם תמונת Hero תהיה AI או תמונה אמיתית מהמוצרים?
[ ] ספקית: תמונות אמיתיות ל-silicone boy type (PID 9689589383481)
[ ] אייל: האם לתייג תמונות AI כ-"תמונות המחשה" בפומבי?
```

---

## 7. Next Recommended Image To Create

**Hero — DONE. הבא: S5 Lifestyle.**

**Hero status (2026-04-27):**
- Desktop + Mobile נוצרו ואושרו ויזואלית על ידי אייל.
- מחוברות לפריוויו המקומי בלבד. Shopify לא נגע.
- שפה ויזואלית נקבעה: ספה קרם, תאורה חמה, 3 בובות.

**S5 — Image: DONE. Video: POSTPONED.**

S5 Desktop + Mobile images אושרו (2026-04-27).
S5 Video נדחה — Veo quota 0/0 גם לאחר תיקון כרטיס אשראי. החלטה: S5 ממשיך עם תמונה בלבד.
משימה פתוחה: לחקור כיצד לפתוח Veo quota ב-Google AI Studio. לא לעצור את דף הנחיתה.

**הבא לפי עדיפות (לאחר S5 video blocker):**
S3 — Lifestyle/gift image: הורה/סבתא בוחרת מתנה, אווירת בית, תאורה רכה.

---

*תכנון נכסים בלבד — אין תמונות שנוצרו. כפוף ל-REBORN-MASTER-PROMPT.md.*
