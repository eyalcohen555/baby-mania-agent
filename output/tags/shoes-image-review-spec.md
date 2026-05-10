# Shoes Image Review Agent — Specification

**תאריך:** 2026-05-10  
**מצב:** READ-ONLY SPEC — אין כתיבות Shopify  
**מטרה:** הגדרת input/output לסוכן vision שיסווג נעליים לפי תמונה

---

## 1. עקרונות

- הסוכן לא יוחלף בכותרת בלבד — תמונה היא source of truth לסיווג נעליים
- confidence נמוך → shoes-review-only → לא נכנס לbatch
- אסור לתייג לפי גודל EU/cm או גיל מספרי בלבד
- multi-tag מותר ומומלץ (ראה shoes-taxonomy-proposal.md)

---

## 2. Input per product

```json
{
  "product_id": "string — Shopify product ID",
  "title": "string — כותרת מוצר מלאה",
  "handle": "string — Shopify handle",
  "description_snippet": "string — 200 תווים ראשונים מהתיאור",
  "image_urls": ["string — URLs לתמונות מוצר (כל התמונות הזמינות)"],
  "current_tags": ["string — תגים קיימים אם יש"]
}
```

---

## 3. Output per product

```json
{
  "product_id": "string",
  "recommended_shoe_tags": ["shoes-sneakers", "shoes-soft-sole"],
  "visual_evidence": "string — תיאור מה נראה בתמונה שמבסס את ההחלטה",
  "confidence": "HIGH | MEDIUM | LOW",
  "needs_manual_review": true,
  "reason": "string — הסבר קצר להחלטה"
}
```

**הגדרות confidence:**

| רמה | משמעות | פעולה |
|---|---|---|
| HIGH | ניתן לזהות בבירור סוג נעל + מאפיינים עיקריים | כלול בbatch planning |
| MEDIUM | יש עדות חלקית, לא מספיקה לודאות מלאה | הוסף shoes-review-only + שלח לbatch review נוסף |
| LOW | לא ניתן לסווג מתמונה — תמונה לא ברורה / לא קיימת / מוצר לא נעל | shoes-review-only + human review |

---

## 4. כללי החלטה

### HIGH confidence — תנאים להכנסה לbatch

כל התנאים חייבים להתקיים:
- [ ] מוצר ברור שהוא נעל/סנדל/מגף לתינוק
- [ ] ניתן לזהות לפחות תג אחד מ: shoes-sneakers / shoes-sandals / shoes-boots / shoes-first-step / shoes-elegant / shoes-soft-sole
- [ ] אין סתירה בין כותרת לתמונה
- [ ] התמונה מציגה את הנעל ברזולוציה מספקת

### MEDIUM confidence

- מוצר נראה כנעל אך תמונה לא מספקת לבדיקת כל המאפיינים
- כותרת מרמזת על סוג אך תמונה לא מאשרת בבירור
- תמונה ראשית לא מציגה את הנעל (תמונת אריזה בלבד)

### LOW confidence — חסימה

- התמונה לא קיימת (no images)
- המוצר בתמונה לא נראה כנעל
- כותרת אמביוולנטית לחלוטין + תמונה לא ברורה
- יש סתירה ברורה בין כותרת לתמונה

---

## 5. Multi-tag examples

```json
{
  "product_id": "9940751417657",
  "title": "1-4T Baby Sandals Summer Breathable Air Mesh...",
  "recommended_shoe_tags": ["shoes-sandals", "shoes-soft-sole"],
  "visual_evidence": "תמונה מציגה סנדל פתוח עם רצועות בד, סוליה גמישה דקה, מתאים לצעד ראשון",
  "confidence": "HIGH",
  "needs_manual_review": false,
  "reason": "סנדל קיצי ברור, סוליה גמישה גלויה"
}
```

```json
{
  "product_id": "EXAMPLE_002",
  "title": "Baby First Step Sneaker Anti-Slip",
  "recommended_shoe_tags": ["shoes-sneakers", "shoes-first-step", "shoes-soft-sole"],
  "visual_evidence": "נעל ספורטיבית עם סוליה גומי דקה ורכה, כפות גמישות, מתאים לתינוק מתחת ל-18m",
  "confidence": "HIGH",
  "needs_manual_review": false,
  "reason": "multi-tag: סניקרס + first-step + soft-sole — כולם גלויים בתמונה"
}
```

```json
{
  "product_id": "EXAMPLE_003",
  "title": "Baby Shoes Spring Autumn Boy Girl",
  "recommended_shoe_tags": ["shoes-review-only"],
  "visual_evidence": "תמונת אריזה בלבד, הנעל עצמה לא גלויה בבירור",
  "confidence": "LOW",
  "needs_manual_review": true,
  "reason": "כותרת כללית, תמונה לא מספקת לסיווג"
}
```

---

## 6. Few-shot prompt לסוכן Vision

```
You are a children's shoe categorization agent for BabyMania, a premium Israeli baby store.

Your task: Given a product title, description snippet, and image URLs, assign appropriate shoe tags from this allowed list only:
- shoes-sneakers: sporty/casual shoe with hard rubber sole
- shoes-sandals: open-toe or open-heel shoe, summer style
- shoes-boots: boot covering ankle or higher
- shoes-first-step: designed for early walkers, flexible sole, 0-18m
- shoes-elegant: formal/event shoe, party/brit
- shoes-soft-sole: clearly flexible/rubber-dot sole for crawlers
- shoes-review-only: cannot classify from image

Rules:
1. You MUST look at the image before deciding. Title alone is insufficient.
2. Multi-tag is allowed and encouraged (max 3 shoe tags).
3. NEVER use EU size, age numbers, or measurements as tags.
4. If image is unclear or absent → shoes-review-only + confidence: LOW
5. Output must be valid JSON matching the output schema exactly.

Example 1 (HIGH confidence):
Input: title="Baby Sandals Summer Breathable Air Mesh Anti-Slip Soft Sole", image shows open strappy sandal with flexible sole
Output: { "recommended_shoe_tags": ["shoes-sandals", "shoes-soft-sole"], "confidence": "HIGH", "visual_evidence": "Open sandal with straps visible, thin flexible sole with rubber dots", "needs_manual_review": false, "reason": "Clear sandal with soft sole" }

Example 2 (LOW confidence):
Input: title="Baby Shoes 0-6M", image shows product box only
Output: { "recommended_shoe_tags": ["shoes-review-only"], "confidence": "LOW", "visual_evidence": "Only packaging visible, shoe itself not shown", "needs_manual_review": true, "reason": "Cannot classify without seeing the shoe" }

Now classify the following product:
Title: {title}
Description: {description_snippet}
Images: {image_urls}
Current tags: {current_tags}
```

---

## 7. Batch workflow לimage review

1. שלוף ~65 מוצרי נעליים חסומים מ-Shopify (GET /products.json?tag=shoes-blocked OR keyword filter)
2. לכל מוצר — הרכב input JSON
3. שלח לסוכן vision
4. אסוף output
5. HIGH → כנס לbatch planning
6. MEDIUM → shoes-review-only זמני, שלח לsub-batch
7. LOW → shoes-review-only קבוע, human review queue
8. לאחר batch planning → dry run → T3 approval → live write

---

*מסמך זה הוא spec בלבד. אין build ואין Shopify writes עד אישור.*
