# HUB-11 — Product → Article Implementation Plan
## B-02 Post-HUB Linking Audit — Output
### Version: 1.0 | Created: 2026-04-29 | Status: PENDING IMPLEMENTATION

---

## 1. מטרה

מיפוי כל 16 מוצרי HUB-11 לעמוד המאמר הרלוונטי ביותר.
**זהו mapping בלבד — לא live edit בשופיפיי.**
ביצוע חי = T1 נפרד, לאחר אישור אייל.

---

## 2. מדיניות implementation

| פרמטר | ערך |
|-------|-----|
| Placement | metafield `article_link` (אחיד עם LAYER 2 reverse-index) |
| Approval tier | T1 — אישור אייל לפני ביצוע |
| Scope | 16 מוצרים × 1 article link כל אחד |
| Live edit method | Shopify Admin API — PATCH product metafield |
| Gate | אסור לבצע לפני T1 approval |

---

## 3. טבלת מיפוי — 16 מוצרים

| # | product_id | product_title | handle | best_article | סיבה | עדיפות |
|---|-----------|--------------|--------|-------------|------|--------|
| 1 | 9605887590713 | שמלת שמש לתינוקות וילדות | summer-toddler-girl-dress-solid-cotton-... | C4 — שמלות קיץ | שמלת שמש = הדגם המרכזי ב-C4 | HIGH |
| 2 | 9605887721785 | שמלת סרבל לתינוקת | summer-baby-girl-dress-with-bowknot-... | C4 — שמלות קיץ | שמלת סרבל מוזכרת ישירות ב-C4 | HIGH |
| 3 | 9179162444089 | שמלת כיווצים קיצית מכותנה - ענבל | שמלת-כיווצים-קיצית-ענבל | C4 — שמלות קיץ | שמלת קיץ מכותנה — C4 מכסה | HIGH |
| 4 | 9179150516537 | שמלת מלמלות מתוקה מכותנה - לין | שמלת-מלמלות-מתוקה-מבד-איכותי-לין | C4 — שמלות קיץ | שמלת מלמלות — C4 מכסה קייצי | HIGH |
| 5 | 9605887820089 | סט קיצי לתינוקות וילדות | baby-girls-clothes-set-... | C4 — שמלות קיץ | סט קיצי — C4 עוסק בהלבשה קיצית בנות | MEDIUM |
| 6 | 9179162083641 | בגד ים פרחוני - לייה | בגד-ים-פרחוני-לייה | C2 — בגד ים לתינוקת | לייה מוזכרת ישירות ב-C2 | HIGH |
| 7 | 9179162804537 | בגד ים שני חלקים - יסמין | בגד-ים-שתיי-חלקים-מרין | C2 — בגד ים לתינוקת | יסמין מוזכרת ישירות ב-C2 | HIGH |
| 8 | 9179164344633 | בגד ים שני חלקים פרחוני - קוקומלון | בגד-ים-שתיי-חלקים-קוקומלון | C2 — בגד ים לתינוקת | בגד ים שני חלקים = C2 בדיוק | HIGH |
| 9 | 9606864666937 | כובע בייסבול רך לתינוק | cute-cartoon-bear-baby-baseball-cap-... | C3 — כובע שמש לתינוק | כובע לתינוק = C3 בדיוק | HIGH |
| 10 | 9605887689017 | סרבל קיצי לתינוקות | babys-clothes-summer-jumpsuit-... | C1 — הלבשת תינוק בקיץ | סרבל קיצי = ביגוד יומיומי, C1 עוסק בהלבשה כללית בקיץ | HIGH |
| 11 | 9179159888185 | חליפת קיץ מכותנה - 1977 | חליפת-קיץ-1977 | C1 — הלבשת תינוק בקיץ | חליפת קיץ מכותנה — C1 מכסה לפי גיל וחום | HIGH |
| 12 | 9605887754553 | חליפת פשתן לתינוק | cotton-linen-casual-toddler-baby-boys-... | C5 — חליפת פשתן | C5 = המאמר הייחודי לפשתן | HIGH |
| 13 | 9179158479161 | אוברול פשתן וכותנה וינטג׳ - קייגו | אוברול-וינטג-קייגו | C5 — חליפת פשתן | אוברול פשתן/כותנה — C5 מכסה פשתן לתינוקות | HIGH |
| 14 | 9179170144569 | חליפת מלמלות מכותנה ופשתן - מיילי | חליפת-פשתן-מלמלות-מיילי | C5 — חליפת פשתן | מיילי מוזכרת ישירות ב-C5 | HIGH |
| 15 | 9838580662585 | מצוף שחייה לתינוקות עם גגון וחגורות ורצועה – דגם משה | baby-swimming-ring-with-canopy-... | C6 — בריכה עם תינוק | מצוף משה מוזכר ישירות ב-C6 | HIGH |
| 16 | 10025300853049 | סט Breeze™ – חולצה קצרה ומכנסי קיץ לפעוטות | סט-מכנס-וחולצה-קיצי-דגם-גילי-מתנהcopy | Pillar — בגדי קיץ לתינוק | סט קיצי כללי — Pillar מכסה בגדי קיץ מקיפים | MEDIUM |

---

## 4. URLי מאמרים (HUB-11)

| מאמר | URL |
|------|-----|
| Pillar | https://www.babymania-il.com/blogs/news/bgdey-kayts-letinok-madrikh-male-ma-lilbosh-ma-lakakhat-layam |
| C1 | https://www.babymania-il.com/blogs/news/eikh-lhalbisht-tinok-bakayts-madrikh-lfi-gil-khom-ushaot |
| C2 | https://www.babymania-il.com/blogs/news/bgad-yam-letineket-eikh-livkhor-ma-livdok-ukrem-haganah |
| C3 | https://www.babymania-il.com/blogs/news/kovah-shemesh-letinok-lama-zeh-hova-vekheytsad-livkhor-nakhon |
| C4 | https://www.babymania-il.com/blogs/news/smlot-kayts-letineket-hadgamim-yoter-nonhim-lahom-hayisraeli |
| C5 | https://www.babymania-il.com/blogs/news/khalifat-pishtan-letinok-hayitronot-eikh-livkhor-umatay-lilbosh |
| C6 | https://www.babymania-il.com/blogs/news/brekha-im-tinok-bitakhon-tsiyud-ushahot-hamumlatsot |

---

## 5. פילוח לפי מאמר

| מאמר | מוצרים | עדיפות |
|------|---------|--------|
| C4 — שמלות קיץ | 5 מוצרים: 9605887590713, 9605887721785, 9179162444089, 9179150516537, 9605887820089 | HIGH×4, MEDIUM×1 |
| C2 — בגד ים | 3 מוצרים: 9179162083641, 9179162804537, 9179164344633 | HIGH×3 |
| C5 — חליפת פשתן | 3 מוצרים: 9605887754553, 9179158479161, 9179170144569 | HIGH×3 |
| C1 — הלבשת קיץ | 2 מוצרים: 9605887689017, 9179159888185 | HIGH×2 |
| C3 — כובע שמש | 1 מוצר: 9606864666937 | HIGH×1 |
| C6 — בריכה | 1 מוצר: 9838580662585 | HIGH×1 |
| Pillar | 1 מוצר: 10025300853049 | MEDIUM×1 |

---

## 6. אזהרות מהאוקיט (B-02)

| קוד | אזהרה | מה לעשות |
|-----|-------|----------|
| W-01 | Pillar לא מקשר לאף אחד מ-C1–C6 | עדכון Pillar — הוסף internal links ל-C1–C6 (T1 נפרד) |
| W-02 | Pillar לא מקשר ל-HUB-5 (מתנות לתינוק) למרות רלוונטיות | הוסף cross-hub link ל-HUB-5 Pillar (T1 נפרד) |

---

## 7. שיפורים ממתינים (לא חוסמים)

| קוד | שיפור | סטטוס |
|-----|-------|--------|
| I-01 | Reverse cross-links: עדכון HUB-2-C1, HUB-4-Pillar, HUB-7-C3 לקשר להUB-11 | PENDING — T1 |
| I-02 | product-reverse-index.json rebuild ל-v2.0 כולל HUB-9–11 (כיום מכסה HUB-1–8 בלבד) | PENDING — משימה נפרדת |

---

## 8. היסטוריית עדכונים

| תאריך | שינוי |
|-------|-------|
| 2026-04-29 | v1.0 — נוצר. B-02 Post-HUB-11 Audit. 16 מוצרים ממופו. |
