# bm-organic Template Track — מצב ואופן עבודה
**נוצר:** 2026-06-06
**מסלול:** נפרד מ-43-article batch pipeline
**עדכון אחרון:** 2026-06-06

---

## 1. מהו bm-organic

`templates/article.bm-organic.json` — Shopify OS2.0 JSON article template.
כל מאמר עם `template_suffix = bm-organic` מציג 7 sections בסדר קבוע:

```
hero → trust-strip → quick-answer → article-body → product-card → cta-banner → faq
```

הגדרות ה-sections (hero image, product URL, מחיר, FAQ וכו') נכתבות ב-template JSON.
body_html של המאמר מכיל רק את תוכן המדריך הנקי — ללא CTAs, FAQ, TOC כפולים.

---

## 2. Theme IDs

| Role | ID | שם | אזהרה |
|------|----|----|-------|
| TEST (עבודה) | **187183563065** | Working/001 | עבודה כאן בלבד |
| LIVE (ייצור) | **183668179257** | ORGINAL Dawn new | ❌ לא לגעת ללא אישור |

BLOG_ID: `109164036409`

---

## 3. מאמרים שהושלמו בטסט — QA PASS

| # | handle | article_id | HUB | מוצר | מחיר | QA | hero CDN | backup |
|---|--------|------------|-----|------|------|-----|----------|--------|
| 1 | naalei-mayim-letinok-meize-gil | 689095672121 | HUB-13/C1 | נעלי מים לתינוק | — | PASS | אייל סיפק | ✅ |
| 2 | naal-tsaad-rishon-ma-kol-horeh-tzarich-ladaat | 682290053433 | HUB-6/C1 | סנייקרס צעד ראשון | ₪111 | 43/43 PASS | `pishtan_c1_hero_naale_tsaad_rishon.png` | ✅ |
| 3 | khalifat-pishtan-letinok-hayitronot-eikh-livkhor-umatay-lilbosh | 686728216889 | standalone | חליפת פשתן לתינוק | ₪151 | 44/44 PASS | `pishtan_c1_hero_khalifat_pishtan_letinok.png` | ✅ |

**LIVE:** ❌ שלושת המאמרים טרם הועלו ל-LIVE. מוכנים לבדיקת preview ואישור Live פרטני של אייל.

---

## 4. Scripts שנוצרו

| script | תפקיד |
|--------|--------|
| `scripts/organic/_hub6_step1_upload_hero.py` | העלאת hero ל-CDN (staged upload + poll) |
| `scripts/organic/_hub6_step2_execute.py` | cleanup body + template push + article update |
| `scripts/organic/_hub6_step3_qa.py` | QA מלא HUB-6/C1 |
| `scripts/organic/_pishtan_execute.py` | cleanup + template + update — חליפת פשתן |
| `scripts/organic/_pishtan_qa.py` | QA מלא חליפת פשתן |
| `scripts/organic/_candidate_check.py` | בדיקת מועמדים לשכפול בm-organic |
| `scripts/organic/_qa_bm_organic_final.py` | QA כללי bm-organic |

Template JSONs מקומיים:
- `scripts/organic/_article_bm_organic_hub6_c1.json`
- `scripts/organic/_article_bm_organic_pishtan_c1.json`

Hero refs:
- `scripts/organic/_hub6_hero_ref.json`
- `scripts/organic/_pishtan_hero_ref.json`

Backups:
- `output/organic/backups/bm-organic-hub6c1-body-before-cleanup-682290053433.json`
- `output/organic/backups/bm-organic-pishtan-body-before-cleanup-686728216889.json`

---

## 5. Hero Image Protocol

**כלל:** אסור לקלוד ליצור תמונות ב-AI / DALL-E / Stitch. תמונות ידניות שאייל יוצר ומספק מותרות.

### דרישות hero image לבדיקה:
| בדיקה | דרישה |
|--------|--------|
| יחס | לנדסקייפ — 16:9 או 3:2 לפחות |
| גודל | ≥ 1200 × 675 px |
| נושא | תינוק/פעוט לובש את המוצר הספציפי |
| רקע | נקי / טבעי / קיצי — אין watermark, לוגו, טקסט |
| איכות | editorial — לא catalog-only shot |
| Shopify | מועלה דרך staged upload → fileCreate → poll READY |
| Ref | `shopify://shop_images/{filename}` |

### תהליך אם אין hero מתאים בתמונות המוצר:
1. **עצור** — אל תשנה body_html, אל תשייך template
2. **החזר דוח** — טבלת 11 תמונות + הערכת כל אחת
3. **שלח brief לאייל** — כולל יחס, נושא, רקע, גודל מינימלי

---

## 6. Safety Checklist לפני כל שכפול

```
□ עובדים על test theme 187183563065 בלבד
□ live theme 183668179257 — אסור לגעת
□ backup body_html נשמר לפני כל שינוי
□ תמונת Hero אושרה — ידנית מאייל בלבד
□ product קיים ב-Shopify + status = active
□ מחיר נכון לפי variants בפועל
□ ≥ 2 internal /blogs/news/ links בגוף — קיימים וקיים מאמר עם handle זה
□ אין placeholders (alt="", TODO, SLOT_, YOUR_)
□ כל 7 sections + כל fields required מוגדרים
□ לא לשנות title / handle / author / SEO
□ QA PASS לפני דיווח על השלמה
```

---

## 7. body_html Cleanup — מה מוסרים

| אלמנט | Class/Selector | פעולה |
|-------|----------------|--------|
| תיבת מבוא | `div.intro-box` | להסיר |
| תשובה קצרה | `div.quick-answer` | להסיר (עובר ל-section) |
| תוכן עניינים | `nav.toc` | להסיר |
| CTA | `div.cta-banner` | להסיר (עובר ל-section) |
| FAQ | `section#faq` | להסיר (עובר ל-section) |
| JSON-LD | `script[type="application/ld+json"]` | להסיר |
| תגיות מאמר | `div.article-tags` | להסיר |
| כרטיס מוצר inline | `div.product-mention` | להסיר |
| כרטיס מוצר inline | `div.product-card-inline` | להסיר אם קיים |

**לשמור:** `div.article-body`, `figure.article-image`, `figcaption`, `blockquote`, `div.tip-box`, `div.warning-box`, `table`, קישורים פנימיים.

**קישורים:** להמיר absolute URLs של babymania-il.com לקישורים יחסיים (`/blogs/news/...`).

---

## 8. Admin Preview

```
https://babymania-il.com/blogs/news/{handle}?preview_theme_id=187183563065
```

**הערה חשובה:** דרוש Shopify admin session בדפדפן לפני פתיחת הקישור.
URL עם `?preview_theme_id=` לא עובד ללא authentication — ה-`www.` redirect מוריד את ה-query params.

**דרך עבודה:**
1. היכנס ל-Shopify Admin בדפדפן
2. עבור Themes → Working/001 → Preview
3. נווט ידנית אל /blogs/news/{handle}

---

## 9. תנאים לפני Push ל-LIVE

```
□ Preview נצפה עם Shopify admin session — נראה תקין
□ אישור מפורש של אייל לכל מאמר בנפרד
□ QA מלא ב-test theme — PASS
□ לא מאמר שנמצא בלוח ה-Batch הרגיל
□ live theme push מבוצע דרך REST API themes/{LIVE_ID}/assets.json
□ לאחר push ל-live — QA נוסף על live theme
□ GSC Request Indexing ידני אחרי אימות live
```

---

## 10. שלב עתידי (לא מאושר)

אחרי אישור אייל: push של 3 המאמרים ל-LIVE theme + GSC.
מסלול זה נפרד לחלוטין מ-43-article batch pipeline.
