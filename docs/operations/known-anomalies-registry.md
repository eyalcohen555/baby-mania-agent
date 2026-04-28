# KNOWN ANOMALIES REGISTRY

**גרסה:** v2
**תאריך יצירה:** 2026-04-19
**עדכון אחרון:** 2026-04-21 (ANOMALY-005, ANOMALY-006 נוספו)

---

## STATUS

פעיל

---

## PURPOSE

המסמך מרכז חריגים ידועים שחייבים להיות מוחרגים או מטופלים לפני generation / bundle / push / closure.

המטרה: למנוע גילוי חוזר של אותה בעיה בכל ריצה חדשה.

---

## RULE

כל חריג ידוע חייב להופיע כאן **לפני** כל rollout או recovery רלוונטי.

bundle לא יכול לכלול PID שמופיע ברשימה זו — אלא אם כן שונה סטטוסו לאחר החלטה ניהולית מפורשת.

---

## REGISTRY

---

### ANOMALY-001

#### PID
`9881362759993`

#### PRODUCT
מנורת לילה להירדמות

#### CATEGORY
anomaly / non-clothing product

#### DETECTED IN
Layer 4 GEO

#### WHY BLOCKED
המוצר נכנס בטעות לסקופ clothing / GEO למרות שאינו מוצר clothing תקין למסלול זה.

#### AFFECTED LAYERS
- Layer 4

#### EXCLUDE RULE
יש להחריג את PID `9881362759993` מכל bundle / push / recovery שרצים על clothing GEO — עד החלטה ניהולית מפורשת אחרת.

#### LIVE STATUS
לא נכתב אליו GEO ב-live — **מאומת** (management-journal.md, 2026-04-19)

#### REOPEN CONDITION
רק אחרי:
1. אימות סיווג מוצר נכון
2. החלטה ניהולית מפורשת של אייל
3. בדיקה שהמוצר שייך למסלול המתאים

#### OWNER
אייל

#### LAST VERIFIED
2026-04-19

---

### ANOMALY-002

#### PID
`9615375925561`

#### PRODUCT
נעל אופנתית ונוחה לתינוק

#### CATEGORY
false positive / archived product

#### DETECTED IN
Layer 4 Audit (2026-04-20)

#### WHY BLOCKED
המוצר דווח באודיט כ"מוצר יתום שנפל מכל הרשימות". אימות live הראה שהמוצר **ARCHIVED** ב-Shopify עוד לפני בניית הסקופ. אין לו context YAML, אין stage outputs, אין metafields — intentional orphan.

#### AFFECTED LAYERS
- אין — המוצר לא שייך לסקופ מלכתחילה

#### EXCLUDE RULE
אין צורך בהחרגה פעילה — המוצר ARCHIVED ולא יופיע בשום bundle פעיל. אם ייכלל בסריקה עתידית, לדחות אוטומטית על בסיס status=archived.

#### LIVE STATUS
- Status: **ARCHIVED**
- Metafields: **0** (אין כלום — title_tag, description_tag, geo_who_for, geo_use_case — כולם חסרים)
- Template: shoes
- **מאומת בדיקה ישירה ב-Shopify API, 2026-04-20**

#### AUDIT IMPACT
הממצא הזה באודיט הוא **false positive** — לא נדרשת שום פעולת תיקון.

#### REOPEN CONDITION
רק אם המוצר יוחזר לסטטוס active על ידי החלטה ניהולית מפורשת. במקרה כזה יש לבנות לו context YAML ולהכניסו לסקופ מחדש.

#### OWNER
אייל

#### LAST VERIFIED
2026-04-20

---

### ANOMALY-003

#### PID
N/A — סוגיה ברמת שאילתה, לא PID ספציפי

#### PRODUCT
כלל מוצרי נעליים עם template_suffix=shoes

#### CATEGORY
query anomaly / GraphQL fuzzy match

#### DETECTED IN
Layer 3 SEO — title_tag audit (2026-04-21)

#### WHY BLOCKED
שאילתת GraphQL עם `query: "template_suffix:shoes"` מחזירה התאמות fuzzy — מוצרים שה-template_suffix שלהם אינו shoes בדיוק עשויים להיכלל בתוצאות. הממצא גרם לcounting שגוי בסקופ האודיט הראשוני.

#### AFFECTED LAYERS
- Layer 3 (title_tag scope detection)

#### EXCLUDE RULE
בכל שאילתת סקופ לנעליים — לאמת template_suffix בדיוק (exact match) לאחר שליפת התוצאות. אין להסתמך על GraphQL query filtering בלבד.

#### LIVE STATUS
לא PID — סוגיה מתודולוגית. לאחר סינון exact-match, ה-scope הסופי היה 38 PIDs (כולם נדחפו 38/38 PASS). מאומת ב-audit 2026-04-21.

#### AUDIT IMPACT
גרם לכלול false positives בספירה הראשונית. לאחר סינון מדויק — scope נקי, 38/38 נדחפו בהצלחה.

#### REOPEN CONDITION
אם שאילתות GraphQL ישתנו בגרסאות API עתידיות — לאמת מחדש שה-filtering מדויק.

#### OWNER
אייל

#### LAST VERIFIED
2026-04-21

---

### ANOMALY-004

#### PID
N/A — סוגיה לוגית ב-classification chain

#### PRODUCT
מוצרי סניקרס (is_sneaker=true)

#### CATEGORY
logic gap / classification chain missing field

#### DETECTED IN
Layer 3 SEO — title_tag audit (2026-04-21)

#### WHY BLOCKED
הפרמטר `is_sneaker` הוגדר בschema של intelligence_builder אך לא שולב בשרשרת הסיווג הפעילה. בפועל — מוצרי סניקרס לא קיבלו טיפול שונה מיתר מוצרי הנעליים במעבר הסיווג, מה שעלול לגרור title_tag שגוי לסוג זה.

#### AFFECTED LAYERS
- Layer 3 (title_tag classification → generation)

#### EXCLUDE RULE
אין exclusion — הממצא תוקן: `is_sneaker` שולב בשרשרת הסיווג לפני generation ב-audit 2026-04-21. אין צורך בהחרגה פעילה.

#### LIVE STATUS
תוקן לפני push live. 38/38 כולל מוצרי סניקרס נדחפו ואומתו PASS.

#### AUDIT IMPACT
לא השפיע על תוצאה הסופית — תוקן בלוגיקה לפני הריצה. כל הסניקרס קיבלו title_tag מדויק.

#### REOPEN CONDITION
אם schema של intelligence_builder ישתנה — לאמת ש-`is_sneaker` עדיין מחובר לclassification chain.

#### OWNER
אייל

#### LAST VERIFIED
2026-04-21

---

### ANOMALY-005

#### PID
`9096636236089`

#### PRODUCT
כפכף פרווה אוסטרלי עדידוש

#### CATEGORY
live geo content error — wrong gtype + PID fingerprint

#### DETECTED IN
Layer 4 GEO — post-closure audit (2026-04-21)

#### WHY BLOCKED
המוצר נכנס ל-gap_map clothing list (לא shoes list) → עובד על ידי gen_clothing_geo.py גרסה ישנה (לפני הוספת guard) → gtype defaulted ל-`"בגד"` → `unique_ref` השתמש ב-`pid[-4:]="6089"` → fingerprint נוצר.
נדחף ל-Shopify בStage-14 כחלק מ-242 clothing PIDs. לא זוהה בreadback (נספר כclothing, לא כshoes).

**תוכן live:**
- `geo_who_for`: `"אמא שרוצה בגד דגם כפכף פרווה אוסטרלי עדידוש (6089)..."` — גם gtype שגוי וגם fingerprint
- `geo_use_case`: `"בטיול משפחתי כשכפכף פרווה אוסטרלי עדידוש (6089) עובד..."` — fingerprint חוזר

#### AFFECTED LAYERS
- Layer 4 (geo_who_for + geo_use_case חיים בShopify עם תוכן שגוי)

#### EXCLUDE RULE
לא להכניס לאף clothing geo recovery batch. מחייב regeneration דרך `generate_shoes_geo.py` בלבד.

#### LIVE STATUS
- **CLOSED ✅** — geo תוקן ונדחף ב-T3 (2026-04-21)
- geo חדש: gtype=sandal (נכון), ללא fingerprint — 9/9 PASS verify live
- scripts/t3_geo_regen_push.py: push 9/9 PASS · verify 9/9 PASS

#### AUDIT IMPACT
Gate 2 Check A היה תופס את fingerprint אילו היה פעיל בזמן geo push. Gate 2 לא מוגדר לבדוק geo fields — blind spot ידוע.

#### REOPEN CONDITION
סגור לאחר: regenerate geo דרך generate_shoes_geo.py + push (T3 — נדרש אישור אייל). **DONE — 2026-04-21.**

#### OWNER
אייל

#### LAST VERIFIED
2026-04-21

---

### ANOMALY-006

#### PID
8 PIDs — ראה רשימה

#### PRODUCT
סניקרס — 8 מוצרים

#### CATEGORY
live geo fingerprint — gtype נכון, PID tag גלוי

#### DETECTED IN
Layer 4 GEO — post-closure audit (2026-04-21)

#### PIDs
```
9096635089209  סניקרס סטייל- גולדן          fingerprint: (9209)
9096633090361  סניקרס- אנג׳לינו             fingerprint: (0361)
9615669100857  סניקרס חלקות קלאסיות לבנות   fingerprint: (0857)
9607363526969  סניקרס ארנבים לתינוקת        fingerprint: (6969)
9731753017657  סניקרס מהממות לבנים דגם ישראל fingerprint: (7657)
9096634925369  סניקרס קלאסיות- דיויד        fingerprint: (5369)
9606764200249  סניקרס לתינוקות מונעות החלקה  fingerprint: (0249)
9607365132601  נעל אולסטאר צעד ראשון לתינוק  fingerprint: (2601)
```

#### WHY BLOCKED
generate_shoes_geo.py גרסה ישנה השתמשה ב-`pid[-4:]` ב-unique_ref — יצרה fingerprint טכני גלוי ב-geo_who_for.
gtype נכון (סניקרס), category נכון (shoes). הבעיה: `(9209)`, `(0361)` וכו' מופיעים בטקסט הגלוי ללקוח.

#### AFFECTED LAYERS
- Layer 4 (geo_who_for עם fingerprint חי ב-Shopify)

#### EXCLUDE RULE
לא להכניס לshoes geo recovery ברשימה ישנה — לבצע regeneration מחדש עם הגרסה הנוכחית של generate_shoes_geo.py.

#### LIVE STATUS
- **CLOSED ✅** — geo תוקן ונדחף ב-T3 (2026-04-21)
- fingerprints הוסרו מכל 8 PIDs — verify live PASS לכל 8
- scripts/t3_geo_regen_push.py: push 9/9 PASS · verify 9/9 PASS (כולל ANOMALY-005)

#### AUDIT IMPACT
Gate 2 Check A היה תופס fingerprints אילו היה פעיל. Readback אימת geo קיים (PASS) אך לא בדק content quality.

#### REOPEN CONDITION
סגור לאחר: regenerate + push לכל 8 PIDs (T3 — נדרש אישור אייל). **DONE — 2026-04-21.**

#### OWNER
אייל

#### LAST VERIFIED
2026-04-21

---

## ADDING NEW ANOMALIES

לפני הוספת חריג חדש, לבדוק:
- האם יש evidence (ראיה) מתועדת — log / journal / live check?
- האם ה-PID מזוהה בוודאות?
- האם הסיבה ברורה ומנוסחת?

**אין להוסיף חריג חלקי או מבוסס-השערה.**

פורמט חובה לכל רשומה חדשה: ANOMALY-NNN + כל שדות החובה לעיל.

---

*KNOWN ANOMALIES REGISTRY — BabyMania Layer 4 — P1-S2 / AUTOMATION-HARDENING-PLAN v1*
