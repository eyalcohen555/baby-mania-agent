# BabyMania — Writing Rules + Source Ladder
# version: 1.0 | date: 2026-03-12
# שכבת כללי כתיבה לכל סוכני התוכן במערכת

---

## כלל עליון

> **אם אין source — אין טענה.**
> כל משפט שנכתב חייב להיתמך ב-Shopify data, visual JSON, או content-bank.yaml.
> ניחוש = שגיאה.

---

## F. SOURCE LADDER — סדר עדיפות לכל section

### 1. Hero (hero_headline + hero_subheadline)

| עדיפות | מקור | תנאי שימוש |
|--------|------|------------|
| 1 | `product_title` (Shopify) | תמיד |
| 2 | `visual.summary.content_team_summary` | אם קיים visual JSON |
| 3 | `visual.style_interpretation.mood_keywords` | לניסוח subheadline |
| 4 | `content-bank → whats_special` | לפי pattern/silhouette/occasion |
| fallback | ניסוח גנרי על פי `product_type` | רק אם שאר המקורות ריקים |
| hide when | `product_title` ריק לחלוטין | — |

### 2. Benefits (4–6 פריטים)

| עדיפות | מקור | תנאי שימוש |
|--------|------|------------|
| 1 | `visual.content_guidance.useful_benefit_directions` | אם קיים visual JSON |
| 2 | `content-bank → benefits` | לפי visual signals + product_type |
| 3 | `description_raw` (Shopify) | רק אם מפורש — לא להסיק |
| fallback | benefits: comfort_daily + free_movement + easy_dressing | תמיד בטוח |
| hide when | לא נדרש hide — תמיד יש לפחות 4 |

### 3. Fabric Story (title + body + body_2 + highlight + tags)

| עדיפות | מקור | תנאי שימוש |
|--------|------|------------|
| 1 | `fabric_type` (Shopify, מפורש) | אם קיים |
| 2 | `visual.texture_and_season_signals` | לתחושה ועונה |
| 3 | `content-bank → fabric_story.without_composition` | כשאין composition |
| 4 | `visual.color_palette + pattern_and_design` | לתגיות בלבד |
| fallback | ניסוח כללי: "תחושה נעימה ללבישה יומיומית" | תמיד בטוח |
| hide when | **לא מסתירים** — תמיד מציגים section זה |

### 4. FAQ (3–4 שאלות)

| עדיפות | מקור | תנאי שימוש |
|--------|------|------------|
| 1 | `content-bank → faq.global` | תמיד: size + washing + age |
| 2 | `content-bank → faq.visual_triggered` | לפי visual signals |
| 3 | `fabric_type` (Shopify) | רק שאלת בד אם יש data אמיתי |
| fallback | global בלבד (3 שאלות) | כשאין visual data |
| hide when | אין סיבה להסתיר |

### 5. Care Instructions (3–5 הוראות)

| עדיפות | מקור | תנאי שימוש |
|--------|------|------------|
| 1 | `care_instructions` (Shopify metafield) | אם קיים |
| 2 | `fabric_type` → כללי כביסה סטנדרטיים | אם קיים |
| 3 | `content-bank` → הוראות שמרניות כלליות | fallback תמיד |
| hide when | לעולם לא מסתירים care |

### 6. Emotional Reassurance

| עדיפות | מקור | תנאי שימוש |
|--------|------|------------|
| 1 | `content-bank → emotional_reassurance` לפי context | occasion/season signal |
| 2 | `visual.style_interpretation.mood_keywords` | לבחירת variant |
| fallback | `emotional_reassurance.general[0]` | תמיד בטוח |
| hide when | אין section כזה כרגע — עתידי |

### 7. What's Special (whats_special)

| עדיפות | מקור | תנאי שימוש |
|--------|------|------------|
| 1 | `visual.distinctive_features.top_5_visual_features` | אם קיים visual JSON |
| 2 | `content-bank → whats_special` לפי pattern + silhouette + color | |
| 3 | `description_raw` — רק עובדות מפורשות | לא להסיק |
| fallback | `whats_special.set_vs_single` | לפי is_set_or_single |
| hide when | אין section נפרד — משולב ב-hero subheadline |

---

## G. SAFETY RULES — מה אסור לטעון

### רמה 1 — אסור בהחלט (Hard Block)

אלה הטענות שאסור לכתוב בשום תנאי בלי source מפורש:

| טענה | מדוע אסורה |
|------|------------|
| הרכב בד מדויק ("100% כותנה") | ממציא עובדה שיכולה להיות שקר |
| תקנים ואישורים ("עומד בתקן OEKO-TEX") | טענה משפטית — חייב מסמך |
| הוראות טיפול ספציפיות ("לכבס ב-30°C") | תלוי בד — בלי תווית, לא לכתוב |
| הבטחות בטיחות ("בטוח לעור רגיש") | טענה רפואית — אסור |
| מידות מדויקות ("אורך 45 ס"מ") | חייב מידות אמיתיות |
| השוואה למתחרים | אסור בכל מצב |
| ביטויי הגזמה ("הכי נוח שיש") | אסור — blacklist |

### רמה 2 — מותנה (Conditional)

| טענה | מותר כשיש | אסור כשאין |
|------|-----------|------------|
| "בד כותנה" | fabric_type = כותנה ב-Shopify | fabric_type ריק |
| "סט של X פריטים" | piece_count ב-visual JSON | ambiguity_flag = true |
| "מתאים לגיל 0–3" | גיל מפורש ב-Shopify | רק משוער |
| "ניתן לייבש במייבש" | care data אמיתי | — |
| "מגן מקור" | product specs | visual בלבד |

### רמה 3 — תמיד מותר (Always Safe)

- נוחות גזרה
- תנועה חופשית
- תחושה נעימה (בלי לפרט חומר)
- מראה מסודר
- קל ללבישה והחלפה
- מתאים לשגרה יומיומית
- עיצוב עדין / פרחוני / ניטרלי (לפי visual)
- "לפי הוראות התווית"

---

## כללי כתיבה — חוקים משותפים לכל section

### שפה
- עברית בלבד
- משפטים עד 12 מילים
- לא להשתמש ב: "מושלם", "הכי טוב", "איכות גבוהה", "מדהים", "תינוקכם", "פרימיום במיוחד", "חובה לכל אמא"

### טון
- רגוע, אנושי, חם
- לא אגרסיבי שיווקי
- לא AI-generic: "מעוצב בקפידה", "נבחר בקפידה"

### מבנה
- תועלת > תכונה — תמיד להסביר מה ההורה מרוויח
- כל benefit חייב לענות: "מה יוצא לי מזה?"
- לא לחזור על אותה תועלת פעמיים

### fallback logic
- אם visual JSON חסר → להשתמש ב-content-bank בלבד
- אם Shopify data דל → להשתמש ב-visual JSON בלבד
- אם שניהם חסרים → fallback מ-content-bank, ללא המצאה

---

## חוק ambiguity

אם `ambiguity_flag = true` ב-visual JSON:
- **אסור** להשתמש בניתוח החזותי כ-source
- **חובה** לפעול לפי Shopify data בלבד
- **חובה** להוסיף note פנימי: `"visual_skipped": true`

---

## הגדרות מינימום לכל section

| Section | מינימום פריטים | מינימום מילים בפריט |
|---------|---------------|---------------------|
| hero_headline | 1 | 3 |
| hero_subheadline | 1 | 5 |
| benefits | 4 | 8 |
| fabric_title | 1 | 3 |
| fabric_body | 1 | 10 |
| faq | 3 Q&A pairs | 8 (answer) |
| care | 3 instructions | 4 |
| emotional_reassurance | 1 | 6 |
