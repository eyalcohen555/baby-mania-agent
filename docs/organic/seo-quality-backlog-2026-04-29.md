# SEO Quality Backlog
## BabyMania Organic — Second Terminal Findings
### Created: 2026-04-29 | Status: ACTIVE BACKLOG | Layer: NOT Layer 6

---

> **חשוב:** קובץ זה מתעד פערי איכות שזוהו — לא פעולות בביצוע.
> שום דבר בקובץ זה לא מורשה לביצוע בלי אישור מפורש מאייל.
> Layer 3 ו-Layer 4 נשארים COMPLETE טכנית — הסטטוס לא השתנה.

---

## 1. Product Title Quality Gap

| פרמטר | ערך |
|-------|-----|
| מספר מוצרים | 244 |
| בעיה שזוהתה | כותרות SEO גנריות, חלשות ביחס למתחרים |
| מתחרים שנבדקו | Chozen, Shilav |
| ציון איכות | 5.25 / 10 |
| prompt לשיפור | נוצר — לא בוצע |
| סטטוס | BACKLOG ONLY — לא לבצע בלי אישור |
| עדיפות | HIGH |

**מה נמצא:**
- כותרות רבות אינן ממנפות מילות מפתח ספציפיות לקטגוריה
- מטא תיאורים חלשים ביחס לחיפוש ישראלי
- gap בין COMPLETE טכני (שדות קיימים ב-Shopify) לבין איכות תוכן SEO

**מה אסור לעשות עכשיו:**
- אסור לרוץ push של 244 כותרות בלי audit + אישור T3
- אסור לשנות Layer 3 ל-"open" בגלל ממצא זה

**מה מותר לעשות כשמאשרים:**
- להריץ prompt שיפור על batch קטן (5-10 מוצרים) לבדיקה
- לאחר PASS — לשקול rollout מלא עם T3 approval

---

## 2. Collection Meta Status

| פרמטר | ערך |
|-------|-----|
| קולקציות שעודכנו ב-Shopify | 15 |
| validation | 5/5 PASS |
| הוגשו ל-GSC | 1/5 |
| נותרות להגשה | ~4 קולקציות |
| חסם | Google Cloud billing (ראה סעיף 6) |
| עדיפות | MEDIUM |

**פעולה נדרשת (אייל):**
Manual Request Indexing ב-GSC UI ל-4 קולקציות שלא הוגשו.

---

## 3. 10-Product Meta Report

| פרמטר | ערך |
|-------|-----|
| דוח נוצר | 2026-04-29 |
| מוצרים שנבדקו | 10 |
| מתחרים | Chozen, Shilav |
| ממצא | פער בין meta שלנו לבין מתחרים |
| סטטוס | לא בוצע שינוי |
| עדיפות | MEDIUM |

הדוח קיים כ-reference — לא בוצע שינוי בפועל.
לפני שיפור meta: audit + T3 approval נדרשים.

---

## 4. Layer 3 / Layer 4 Quality Warning

| פרמטר | ערך |
|-------|-----|
| ציון איכות | 5.25 / 10 |
| מתחרים | Chozen, Shilav |
| Layer 3 סטטוס טכני | COMPLETE ✅ — לא השתנה |
| Layer 4 סטטוס טכני | COMPLETE ✅ — לא השתנה |
| עדיפות ל-fix | HIGH (לטווח הבינוני) |

**הבחנה חשובה:**
- Layer 3 = COMPLETE טכנית: שדות title_tag + description_tag + FAQ קיימים ב-244 מוצרים
- Layer 4 = COMPLETE טכנית: geo_who_for + geo_use_case קיים ב-241 מוצרים
- Quality backlog = שיפור האיכות של התוכן שכבר קיים — לא re-open של הלayers
- זו לא משימת Layer 6 כרגע

---

## 5. GSC SEO Opportunities (4 זוהו)

| הזדמנות | סוג | סטטוס |
|---------|-----|--------|
| CTR optimization: bath-water, white-noise, sleep-routine | Blog titles | BACKLOG |
| Query-to-page fit: מאניה ילדים → homepage | Landing page | BACKLOG |
| Shoes/sandals cluster expansion | Content gap | BACKLOG |
| Reborn accessories content | Future product | BACKLOG |

**כלל:** לא לפתוח עבודה על אף הזדמנות בלי אישור ניהולי מפורש.

---

## 6. Google Cloud / GSC Automation Blockers

| בלוק | תיאור | פעולה נדרשת | עדיפות |
|------|--------|-------------|--------|
| Google Cloud billing | Mastercard ending 0400 נדחה — account terminated | אייל: חידוש billing ידני | HIGH |
| Service account לא Owner | gsc-access@babymania-001.iam.gserviceaccount.com לא מוגדר כ-Owner ב-GSC | אייל: GSC Settings → Users → Add Owner | HIGH |
| submit_gsc.py | לא יכול לרוץ אוטומטית עד שהחסמים נפתרים | תלוי ב-billing + service account | — |

**השפעה:**
- scripts/submit_gsc.py = חסום
- כל AI automation שתלויה ב-Google Cloud = חסומה
- Manual workaround בלבד: GSC UI → URL Inspection → "Request Indexing"

---

## 7. Duplicate Content Decision Required

| פרמטר | ערך |
|-------|-----|
| דף | בגדי-חורף-1 |
| בעיה | תוכן כפול / דף דומה קיים |
| אפשרות א | מיזוג עם דף קיים (301 redirect) |
| אפשרות ב | תוכן ייחודי — differentiation |
| מי מחליט | אייל |
| עדיפות | MEDIUM |

**לא לבצע שום פעולה** בלי החלטת אייל.

---

## 8. Pink Noise — Future Content Idea

| פרמטר | ערך |
|-------|-----|
| רעיון | Pink Noise article |
| מקור | Top 10 טרנדים 2026 research |
| סטטוס | Future idea ONLY |
| HUB | אין — לא לפתוח עכשיו |

Pink Noise = הזדמנות תוכן עתידית. לא לפתוח HUB. לשמור כ-B-candidate לבחירה עתידית.

---

## 9. Security / GSC Token

| פרמטר | ערך |
|-------|-----|
| ממצא | Verification token לא בשימוש ב-GSC Settings |
| סיכון | נמוך |
| פעולה | בדיקה ידנית — אייל |
| עדיפות | LOW |

---

## 10. Priorities Summary

| עדיפות | פריט | פעולה | בעלים |
|--------|------|--------|-------|
| HIGH | Google Cloud billing renewal | חידוש ידני | אייל |
| HIGH | Service account → GSC Owner | GSC Settings | אייל |
| HIGH | 244 title quality improvement | audit + T3 approval | Claude + אייל |
| MEDIUM | HUB-10 GSC C5-C6 manual indexing | GSC UI | אייל |
| MEDIUM | HUB-11 GSC C2-C6 manual indexing | GSC UI | אייל |
| MEDIUM | 4 collections GSC indexing | GSC UI | אייל |
| MEDIUM | Duplicate content "בגדי-חורף-1" | החלטה | אייל |
| LOW | GSC verification token cleanup | GSC Settings | אייל |

---

## 11. What NOT to Do (from these findings)

- ❌ אסור לשנות Layer 3 ל-"open" בגלל ציון 5.25/10
- ❌ אסור לשנות Layer 4 ל-"open"
- ❌ אסור לפתוח Layer 6 בגלל ממצאים אלה
- ❌ אסור לרוץ 244 title update בלי T3 approval
- ❌ אסור לפתוח Pink Noise HUB עכשיו
- ❌ אסור לפתוח B-03 בלי אישור אייל (זה Layer 5 execution, לא quality fix)
- ❌ אסור להריץ submit_gsc.py עד שbilling + service account נפתרים

---

*קובץ זה עודכן אוטומטית מממצאי second terminal session (2026-04-29). לא בוצע שינוי live.*
