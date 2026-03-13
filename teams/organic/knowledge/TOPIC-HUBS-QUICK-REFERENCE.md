# BabyMania Topic Hubs — Quick Reference

> סקירה מהירה של 7 ה-hubs המאושרים. למפה המלאה עם supporting articles, agent instructions, ו-cross-hub links — ראה `TOPIC-HUBS-KNOWLEDGE.md`.

---

## Hub Priority Order

| עדיפות | Hub | Product Bridge |
|--------|-----|----------------|
| 1 | **HUB-1: Baby Sleep** | BabySleep Pro (live ✓), night lights, sleep accessories — see `babysleep-pro.yaml` |
| 2 | **HUB-2: Newborn Clothing** | baby outfits, bodysuits, baby sets |
| 3 | **HUB-3: Baby Essentials** | gift bundles, baby clothing, sleep accessories |
| 4 | **HUB-4: Sensitive Baby Skin** | cotton baby clothing, soft baby outfits, newborn sets |
| 5 | **HUB-5: Baby Gifts** | gift bundles, newborn gift sets |
| 6 | **HUB-6: Baby Routine** | sleep accessories, comfortable baby clothing |
| 7 | **HUB-7: Baby Safety** | sleep accessories, safe baby clothing |

---

## Hub Map

### HUB-1: Baby Sleep
**Pillar:** How to Help Your Baby Sleep Through the Night
**Supporting (top 3):** Baby Sleep Routine for Newborns · Is White Noise Safe for Babies · Safe Sleep Environment Checklist
**Hidden Diamond Signal:** white noise / safe sleep / newborn sleep schedule

---

### HUB-2: Newborn Clothing
**Pillar:** How Many Clothes Does a Newborn Really Need
**Supporting (top 3):** What Fabric Is Best for Newborn Skin · Newborn Clothing Checklist · How to Dress a Newborn for Sleep
**Hidden Diamond Signal:** how many onesies / best fabric newborn skin

---

### HUB-3: Baby Essentials
**Pillar:** Complete Newborn Shopping Checklist
**Supporting (top 3):** What Do You Really Need for a Baby · Baby Essentials for the First 3 Months · Minimalist Baby List
**Hidden Diamond Signal:** minimalist baby list / what new parents really need

---

### HUB-4: Sensitive Baby Skin
**Pillar:** How to Care for a Baby With Sensitive Skin
**Supporting (top 3):** Best Fabrics for Sensitive Baby Skin · Why Cotton Is Best for Newborns · Signs of Sensitive Skin in Babies
**Hidden Diamond Signal:** cotton vs synthetic baby clothes / baby skin irritation clothing

---

### HUB-5: Baby Gifts
**Pillar:** Best Gifts for a New Mom
**Supporting (top 3):** Baby Shower Gift Ideas · Practical Gifts for New Parents · Luxury Baby Gift Ideas
**Hidden Diamond Signal:** what new moms really need / practical baby shower gifts

---

### HUB-6: Baby Routine
**Pillar:** How to Build a Healthy Baby Routine
**Supporting (top 3):** Newborn Daily Routine · Sleep Routine for Babies · How to Calm a Fussy Baby
**Hidden Diamond Signal:** when do babies start a routine / signs your baby needs a routine

---

### HUB-7: Baby Safety
**Pillar:** How to Create a Safe Environment for Your Baby
**Supporting (top 3):** Safe Sleep Guidelines for Newborns · How to Prevent Baby Overheating · Safe Baby Clothing Tips
**Hidden Diamond Signal:** how to prevent baby overheating / safe sleep clothing

---

## Agent Field Reference

| Agent | שדות חדשים |
|-------|-----------|
| 02 keyword-research | `suggested_topic_hub`, `possible_new_hub_candidate` |
| 03 blog-strategist | `topic_hub`, `article_role`, `related_pillar`, `product_bridge_relevance` |
| 05 demand-validator | `topic_hub`, `hub_strengthening_value` |
| 06 content-prioritizer | `topic_hub`, `cluster_position`, `supports_topical_authority` |
| 04 blog-writer | קורא `topic_hub` + `cluster_position` מ-content_priority.json |

---

## כללי מיפוי מהיר

- מוצר **שינה** (white noise, night light) → **HUB-1**
- מוצר **ביגוד יילוד** (rompers, sets, bodysuits) → **HUB-2**
- מוצר **ציוד כללי** → **HUB-3**
- מוצר **כותנה / עור רגיש** → **HUB-4**
- מוצר **מתנות / gift sets** → **HUB-5**
- מוצר **שגרה / נוחות** → **HUB-6**
- מוצר **בטיחות / מניעת התחממות** → **HUB-7**
- מוצר שלא מתאים לאף hub → `possible_new_hub_candidate: true`
