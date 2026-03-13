# BabyMania — Usage Example: Content Generator Flow
# date: 2026-03-12
# איך content generator משלב שלושה מקורות לפלט סופי

---

## המוצר לדוגמה

**שם:** Leona Luxe™ חליפת מנומר
**ID:** `10026705748281`
**Shopify data:**
```
product_type: "חליפה"
fabric_type: ""              ← ריק
target_age: "0-18 חודשים"
description_raw: "חליפת מנומר אלגנטית לתינוקת. סט 2 חלקים."
price: 149
variants_count: 4
```

**Visual JSON (מקוצר):**
```json
{
  "primary_subject": {
    "main_garment_type": "two-piece set",
    "is_set_or_single": "set",
    "piece_count_estimate": 2
  },
  "color_palette": {
    "primary_colors": ["black", "white"],
    "overall_palette_mood": "bold, graphic"
  },
  "pattern_and_design": {
    "pattern_type": "animal print",
    "pattern_description": "leopard spots",
    "decorative_elements": ["ruffle collar"]
  },
  "texture_and_season_signals": {
    "softness_impression": "medium-soft",
    "season_signal": "spring-autumn",
    "thickness_signals": "medium"
  },
  "style_interpretation": {
    "style_keywords": ["bold", "feminine", "statement"],
    "occasion_signals": ["outing", "gift", "event"],
    "premium_signals": ["ruffle detail", "matching set"]
  },
  "audience_signals": {
    "gender_styling_signal": "feminine"
  },
  "content_guidance": {
    "useful_benefit_directions": [
      "bold pattern that stands out",
      "matching set removes outfit decisions",
      "ruffle collar adds premium feel"
    ],
    "useful_hero_directions": [
      "statement set for confident little ones",
      "the leopard print that turns heads"
    ],
    "safe_angles_for_copy": ["pattern", "set", "occasion", "gift"]
  }
}
```

---

## שלב 1 — בחירת source לכל field

לפי `writing-rules.md → Source Ladder`:

| Field | Source נבחר | נימוק |
|-------|------------|-------|
| hero_headline | visual.content_guidance.useful_hero_directions[0] | קיים visual JSON |
| hero_subheadline | content-bank → whats_special.set_vs_single.set | is_set_or_single = set |
| benefits | visual.content_guidance + content-bank | benefit_key: neat_look, gift_worthy, free_movement, easy_dressing |
| fabric_title | content-bank → fabric_story.without_composition.title_options[0] | fabric_type ריק |
| fabric_body | content-bank → fabric_story.without_composition.body_options[0] | fabric_type ריק |
| fabric_tags | visual.color_palette + pattern_and_design | "מנומר", "שחור-לבן", "אביב-סתיו" |
| faq | global: size + washing + age + visual_triggered: set_pieces | is_set_or_single = set |
| care | content-bank fallback (שמרני) | fabric_type ריק |
| emotional_reassurance | content-bank → gift_context[0] | occasion includes gift |

---

## שלב 2 — פלט מוצר סופי (metafields)

```yaml
hero_headline: "סט מנומר שבולט — ומרגיש נוח"
hero_subheadline: "סט מתואם — כל מה שצריך בפריט אחד."

benefits:
  - headline: "מראה מסודר גם אחרי שעות"
    supporting: "שומר על צורתו גם אחרי כביסות ולבישה חוזרת."
  - headline: "נראה כמו מתנה, מרגיש כמו בית"
    supporting: "עיצוב שמתאים לאירוע — נוחות שמתאימה לכל יום."
  - headline: "תנועה חופשית בכל פוזיציה"
    supporting: "הגזרה לא מגבילה — גם כשהתינוק זוחל, יושב או משחק."
  - headline: "קל ללבישה ולהחלפה"
    supporting: "פתיחה נגישה — פחות מאמץ לשניכם."

fabric_title: "נוח על העור, נעים ללבישה"
fabric_body: "הלבוש מרגיש נעים על עור רגיש — גם אחרי שעות ארוכות."
fabric_body_2: "קל לכביסה ומחזיר את צורתו."
fabric_highlight: "כי הנוחות של התינוק מתחילה בבחירה הנכונה."
fabric_tags: ["מנומר", "שחור-לבן", "אביב-סתיו", "סט 2 חלקים"]

faq:
  - Q: "איך בוחרים מידה?"
    A: "מומלץ לבחור לפי גיל ומשקל התינוק. אם בספק — עולים מידה."
  - Q: "איך לכבס?"
    A: "כביסה בטמפרטורה נמוכה לפי הוראות התווית. מומלץ לייבש בצל."
  - Q: "לאיזה גיל מתאים?"
    A: "הגדלים מותאמים לגיל המצוין — תינוקות גדלים בקצב שונה, כדאי לבדוק את טבלת המידות."
  - Q: "מה כולל הסט?"
    A: "הסט כולל את הפריטים המופיעים בתמונה — ראו תיאור המוצר לפירוט מדויק."

care_instructions:
  - icon: wash_60 | כותרת: "כביסה עדינה" | טקסט: "מים קרים עד פושרים, לפי התווית."
  - icon: sun_dry | כותרת: "ייבוש בצל" | טקסט: "מומלץ לייבש שטוח בצל."
  - icon: no_bleach | כותרת: "ללא אקונומיקה" | טקסט: "אסור להשתמש בחומרי הלבנה."

emotional_reassurance: "מתנה שמרגישה מיוחדת — ונוחה כמו בגד יומיומי."
```

---

## שלב 3 — בדיקות לפני publish

```
✓ fabric_type ריק → לא הוזכר שם בד ספציפי
✓ ambiguity_flag = false → visual JSON שומש
✓ כל benefit מבוסס על source מוגדר
✓ faq.restricted לא שומשו (fabric_type ריק)
✓ אין ביטויי blacklist
✓ hero_headline < 10 מילים
✓ כל answer ≤ 2 משפטים
```

---

## מיקום בפייפליין

```
[Shopify Fetch]
      ↓
[Product Analyzer — 01a]
      ↓
[Visual Analyzer — 01b]  ← מחזיר visual JSON
      ↓
[Content Generator]  ← משלב: Shopify + visual JSON + content-bank + writing-rules
      ↓
[Validator]
      ↓
[Publisher]
```

**content-bank.yaml** ו-**writing-rules.md** נטענים ע"י Content Generator בתחילת כל ריצה.
הם לא משתנים בין מוצרים — הם שכבת הידע הקבועה.
