# Management Journal — BabyMania
**תחום:** החלטות ניהוליות רחבות — workflow, עדיפויות, חלוקת פרויקטים
**עדכון:** אחרי כל החלטה ניהולית שמשפיעה על יותר מתחום אחד

---

## JOURNAL TEMPLATE

```
## DATE: YYYY-MM-DD
## TASK: שם המשימה
## SCOPE: תחום ההחלטה
## WHAT CHANGED: מה השתנה
## FILES TOUCHED: קבצים
## SYSTEM IMPACT: השפעה על המערכת
## OPEN ISSUES: בעיות פתוחות
## NEXT STEP: הצעד הבא
```

---

## DATE: 2026-04-23
## TASK: CHECK E ACTIVATION — Gate 2 Template Repetition Check
## SCOPE: Layer 4 — Gate 2 Semantic hardening, Check E
## APPROVAL_TIER: T1

## WHAT CHANGED:
- Check E (Template Repetition) הופעל ב-`scripts/gate2_semantic.py`
- ספים שאושרו על ידי אייל: PAIR_WARN=0.6, BATCH_FAIL=0.8
- נוספו קבועים `PAIR_WARN` ו-`BATCH_FAIL` — literals 0.6/0.8 הוחלפו בקבועים
- `check_e` נוסף ל-`check_results` בפלט Gate 2 (תאימות למפרט)
- `docs/operations/semantic-gate-spec.md` עודכן ל-v1.2

## FILES TOUCHED:
- `scripts/gate2_semantic.py` (CHECK_E_ENABLED: False → True, thresholds כקבועים)
- `docs/operations/semantic-gate-spec.md` (v1.1-draft → v1.2, Check E active)
- `docs/management/management-journal.md` (entry זה)
- `BABYMANIA-MASTER-PROMPT.md` (snapshot עדכון — Check E active)

## SYSTEM IMPACT:
- Gate 2 כעת רץ כל 5 checks (A–E) — Check E ברמת batch בלבד
- ספי אישור: PAIR_WARN ≥ 0.6 (pair warning), BATCH_FAIL ≥ 0.8 ב-2+ זוגות (batch stop)
- semantic_signature: true ניתן רק אם Check E לא BATCH_WARN/FAIL ברמת ה-batch

## OPEN ISSUES: NONE

## NEXT STEP:
HUB-9 clusters C1-C6 | Layer 5 unfreeze (Eyal decision)

---

## DATE: 2026-04-23
## TASK: LAYER 3 — L3-1 CLOSURE: 36 clothing PIDs SEO live verification
## SCOPE: Layer 3 — סגירת אמביגואיות אחרונה ב-verify_failed clothing
## APPROVAL_TIER: T0 (read-only)

## WHAT CHANGED:
- live API check (T0) על 36 verify_failed clothing PIDs — `global.title_tag` + `global.description_tag`
- תוצאה: 36/36 PRESENT — 0 MISSING, 0 EMPTY, 0 HTTP errors
- title_tag: 38–63 תווים (כולם ≤ 70 ✅) | description_tag: 105–143 תווים (כולם ≤ 160 ✅)
- הטענה "verify_failed היו RUNTIME only (timeout/429)" — **מאושרת לחלוטין**

## FILES TOUCHED:
- `output/stage-outputs/layer3_36pid_live_check.json` (artifact — נוצר)
- `docs/governance/phase2-live-readback-scope-lock.md` (SCOPE CORRECTIONS + VERDICT + SUMMARY עודכנו)
- `BABYMANIA-MASTER-PROMPT.md` (v4.5 — Layer 3 verified note)
- `docs/management/management-journal.md` (entry זה)

## SYSTEM IMPACT:
- L3-1 מה-backlog — **סגור**
- Layer 3 COMPLETE ✅ מאושר ללא exceptions — אין recovery track נדרש
- Layer 3 + Layer 4 — שניהם סגורים ומאומתים live

## OPEN ISSUES: NONE

## NEXT STEP:
Check E thresholds (Eyal approval) | Layer 5 unfreeze (Eyal decision) | Organic HUB-9 clusters

---

## DATE: 2026-04-21
## TASK: GAP MAP — RECLASSIFY PID 9096636236089 (כפכף) FROM CLOTHING → SHOES
## SCOPE: output/stage-outputs/layer4_geo_gap_map.json — classification fix
## APPROVAL_TIER: T1

## WHAT CHANGED:
- PID `9096636236089` (כפכף פרווה אוסטרלי עדידוש) הועבר מ-clothing ל-shoes בgap_map
- מטרה: מניעת חזרה של ANOMALY-005 אם geo יירגנרט בעתיד

## FILES TOUCHED:
- `output/stage-outputs/layer4_geo_gap_map.json`
  - `categories.shoes.missing`: 51 → 52
  - `categories.clothing.missing`: 242 → 241
  - `categories.shoes.pids_missing`: PID נוסף
  - `categories.clothing.pids_missing`: PID הוסר
  - `all_products_by_category.shoes`: PID נוסף
  - `all_products_by_category.clothing`: PID הוסר
  - `comparison_candidates`: לא שונה (רשימה aggregate)

## VALIDATION:
- JSON parse: PASS
- in shoes.pids_missing: True | in clothing.pids_missing: False
- in all_products shoes: True | in all_products clothing: False
- ללא כפילויות | total_missing=293 (ללא שינוי)

## SYSTEM IMPACT:
- שינוי local בלבד — אין Shopify write
- אם geo יירגנרט ל-9096636236089 בעתיד, הוא ישתמש ב-shoes generator ולא ב-clothing generator

## OPEN ISSUES: NONE

## NEXT STEP:
gap_map fix CLOSED. ANOMALY-005 root cause addressed at data layer.

---

## DATE: 2026-04-21
## TASK: LAYER 4 GEO — SHOES GEO CONTENT DEFECTS AUDIT
## SCOPE: Layer 4 — post-closure audit על geo content quality

## WHAT CHANGED:
- audit ישיר על geo_draft files + gap_map גילה שניסוח "8 shoes עם gtype=בגד" בreadback doc — **שגוי**
- תוקן תיעוד ב-5 מסמכים (ראה FILES TOUCHED)

## FINDINGS (תיעוד בלבד — אין Shopify writes):
1. PID 9096636236089 (כפכף פרווה): geo live עם gtype=בגד + fingerprint (6089) — ANOMALY-005
2. 8 PIDs סניקרס: geo live עם pid fingerprints — gtype נכון — ANOMALY-006
3. PID 9096634106169: borderline phrasing — אין פעולה נדרשת
4. "Content is clean, no fingerprints" בreadback doc — **לא נכון** — תוקן

## ROOT CAUSE (מתועד):
- gen_clothing_geo.py גרסה ישנה (bak): ללא shoes guard + unique_ref עם pid[-4:]
- generate_shoes_geo.py גרסה ישנה: גם כן השתמש ב-pid[-4:]
- gap_map סיווג 9 shoes כclothing — כפכף בכלל clothing list
- Stage-14 דחף כל 242 clothing PIDs כולל כפכף

## FILES TOUCHED:
- `docs/governance/phase2-live-readback-scope-lock.md` (KNOWN ISSUE — תוקן)
- `BABYMANIA-MASTER-PROMPT.md` (Open items — תוקן)
- `docs/operations/known-anomalies-registry.md` (ANOMALY-005 + ANOMALY-006 נוספו)
- `docs/product/shoes-journal.md` (open issues + STAGE-16 correction)
- `docs/management/management-journal.md` (entry זה)

## SYSTEM IMPACT: תיעוד בלבד — אין שינוי ב-Shopify

## OPEN ISSUES:
- [x] regenerate + push geo ל-9096636236089 (T3) — **DONE 2026-04-21**
- [x] regenerate + push geo ל-8 PIDs סניקרס (T3) — **DONE 2026-04-21**

## NEXT STEP:
~~אישור אייל → geo regeneration plan לכל 9 PIDs~~ — CLOSED

---

## DATE: 2026-04-21
## TASK: LAYER 4 GEO — T3 REGEN + PUSH ל-9 PIDs (ANOMALY-005 + ANOMALY-006)
## SCOPE: Layer 4 — geo content defects fix, Shopify live write
## APPROVAL_TIER: T3 (אושר על ידי אייל)

## WHAT CHANGED:
- geo regenerated + pushed לכל 9 PIDs: 1 כפכף (ANOMALY-005) + 8 סניקרס (ANOMALY-006)
- fingerprints (pid[-4:]) הוסרו מכל הטקסט הגלוי ללקוח
- כפכף: gtype תוקן מ"בגד" ל-sandal
- dry-run בוצע לפני push — validated: 0 fingerprints, 0 clothing phrases
- push: 9/9 HTTP 200 PASS
- verify live: 9/9 PASS — content match, clean

## FILES TOUCHED:
- `scripts/t3_geo_regen_push.py` (נוצר — T3 push + verify script)
- `scripts/t3_geo_regen_dryrun.py` (נוצר — dry-run script)
- `fetch_tmp/nine_pids_raw.json` (נוצר — product data ל-9 PIDs)
- `output/stage-outputs/t3_geo_regen_results.json` (נוצר — results artifact)
- `docs/operations/known-anomalies-registry.md` (ANOMALY-005 + ANOMALY-006 → CLOSED)
- `docs/product/shoes-journal.md` (מצב נוכחי עודכן)
- `docs/management/management-journal.md` (entry זה)
- `BABYMANIA-MASTER-PROMPT.md` (v4.4 — geo defects CLOSED, open items עודכנו)

## SYSTEM IMPACT:
- 9 PIDs live בShopify קיבלו geo חדש ונקי
- ANOMALY-005 + ANOMALY-006 סגורים
- Layer 4 GEO נקי לחלוטין

## OPEN ISSUES:
- אין — Layer 4 GEO כל 9 PIDs נקיים
- Layer 5: FROZEN — מחכה להחלטה ניהולית

## NEXT STEP:
Layer 5 — decision needed (FROZEN). לא נדרשת שום פעולה ב-Layer 4.

---

## DATE: 2026-04-21
## TASK: LAYER 3 SHOES — title_tag AUDIT + FIX — 38/38 LIVE
## SCOPE: Layer 3 — shoes title_tag + description_tag closure

## WHAT CHANGED:
- בוצע audit ייעודי על מוצרי נעליים — נמצאו 38 PIDs עם title_tag גנרי
- false positive: PID 9615375925561 נפסל — ARCHIVED בShopify (ראה ANOMALY-002)
- ANOMALY-003 זוהה ותועד: GraphQL fuzzy match על query של template_suffix:shoes
- ANOMALY-004 זוהה ותועד: is_sneaker מוגדר בschema אך לא היה בשרשרת הסיווג
- dry-run bug של "לד" תוקן לפני push
- 38/38 PIDs נדחפו live ואומתו PASS

## FILES TOUCHED:
- `docs/operations/known-anomalies-registry.md` (ANOMALY-003 + ANOMALY-004 נוספו)
- `docs/product/shoes-journal.md` (entry חדש)
- `BABYMANIA-MASTER-PROMPT.md` (closure note + Layer 3 shoes count מעודכן)
- `docs/management/management-journal.md` (עדכון זה)

## SYSTEM IMPACT:
- Layer 3 shoes = COMPLETE. 51 PIDs נקיים (13 מLayer 3 המקורי + 38 מaudit זה)
- אין שינוי ב-Shopify מעבר לpush המאושר של 38 PIDs

## OPEN ISSUES: NONE — shoes Layer 3 CLOSED

## NEXT STEP:
- המשך HUB-9 clusters / החלטה ניהולית על Layer 5

---

## DATE: 2026-04-20
## TASK: DOCS SYNC — HUB-9 publish + GSC manual request indexing complete
## SCOPE: ניהול — סנכרון סופי אחרי HUB-9 publish + GSC manual requests

## WHAT CHANGED:
- כל מסמכי המקור עודכנו לאחר: HUB-9 Pillar publish + inspection HUB-8/9 + manual Request Indexing
- `gsc_pending_manual_request` → `gsc_manual_requested` עבור HUB-8 + HUB-9
- Pipeline line תוקן: "GSC submit" → "GSC inspect → manual Request Indexing"
- hub-registry.json: last_published=HUB-9, next_hub=HUB-9 Clusters C1-C6

## FILES TOUCHED:
- `BABYMANIA-MASTER-PROMPT.md` — pipeline line + HUBs table (HUB-8 + HUB-9 GSC)
- `teams/organic/hub-registry.json` — gsc_status + last_published + next_hub
- `docs/organic/מצב-הפרויקט-האורגני.md` — HUB-8 + HUB-9 GSC column
- `docs/organic/organic-journal.md` — entry added

## SYSTEM STATE:
- HUBs: 9 live (HUB-1..HUB-9 Pillar) | 48 articles
- HUB-8: gsc_manual_requested ✅ | HUB-9 Pillar: gsc_manual_requested ✅
- HUB-9 C1-C6: pending

## OPEN ISSUES:
- [ ] HUB-9 Clusters C1-C6 כתיבה + פרסום
- [ ] HUB-6 + HUB-7 Manual Request Indexing (נדחה)

## NEXT STEP:
- HUB-9 C2 "בגדי ריבורן" — execution

---

## DATE: 2026-04-20
## TASK: GSC WORKFLOW FINALIZATION — inspection + manual request model
## SCOPE: ניהול — workflow correction, status model

## WHAT CHANGED:
- API PROVEN: Search Console URL Inspection API = inspection only. `urlInspection.index()` has one method: `inspect`. No request indexing endpoint exists.
- Google Indexing API = not suitable for blog articles (URL ownership verification fails for non-JobPosting/BroadcastEvent content).
- `scripts/submit_gsc.py` שוכתב להשתמש ב-URL Inspection API. output: `unknown` / `indexed` / `crawled_not_indexed` / `inspection_failed`
- Status model עודכן:
  - הוסר: `gsc_submitted`, `gsc_requested`, `pending_gsc_permission`
  - נוסף: `gsc_pending`, `gsc_pending_manual_request`, `gsc_inspected`
  - נשאר: `gsc_unknown`, `gsc_indexed`, `gsc_crawled_not_indexed`
- HUB-8 + HUB-9: inspection רץ (result: unknown) → סטטוס = `gsc_pending_manual_request`
- post-publish flow קנוני: publish → verify → inspect(script) → manual request(GSC UI) → docs

## FILES TOUCHED:
- `docs/management/update-policy.md`
- `BABYMANIA-MASTER-PROMPT.md`
- `teams/organic/hub-registry.json`
- `scripts/submit_gsc.py`
- `docs/management/management-journal.md`

## SYSTEM IMPACT:
- אין יותר בלבול בין inspect לבין request indexing
- workflow אמיתי ומוכח תועד בכל מסמכי המקור

## OPEN ISSUES:
- [ ] Manual Request Indexing ב-GSC UI עבור HUB-8 + HUB-9
- [ ] Manual Request Indexing עבור HUB-6 + HUB-7 (גם הם pending)

## NEXT STEP:
- GSC UI → Request Indexing → HUB-8 + HUB-9 → עדכן gsc_status ל-`gsc_indexed` לאחר אישור

---

## DATE: 2026-04-20
## TASK: GSC POST-PUBLISH FLOW — הגדרה רשמית כשלב חובה
## SCOPE: ניהול — workflow change, organic post-publish

## WHAT CHANGED:
- GSC submission הוגדר רשמית כשלב חובה ב-post-publish flow אורגני
- Pipeline רשמי עודכן: `11 → 03 → 04 → 08 → publish → verify → GSC submit → docs update`
- `scripts/submit_gsc.py` נוצר — integration קבוע ל-Google Indexing API
- סטטוסים רשמיים נקבעו: `gsc_submitted` / `pending_gsc_permission` / `gsc_pending` / `gsc_indexed`
- כלל: publish complete ≠ FULLY COMPLETE. FULLY COMPLETE = publish + gsc_submitted.
- HUB-8 + HUB-9 Pillar סומנו `pending_gsc_permission` ב-hub-registry.json

## PERMISSION BLOCKER:
- service account `gsc-access@babymania-001.iam.gserviceaccount.com` — צריך הרשאת Owner
- GSC → babymania-il.com → Settings → Users and permissions → Add user → Owner
- אחרי הוספה: `python scripts/submit_gsc.py <url>` — submit יעבור

## FILES TOUCHED:
- `docs/management/update-policy.md` — Post-Publish Flow section + סטטוסים
- `BABYMANIA-MASTER-PROMPT.md` — pipeline + HUBs table + GSC integration note
- `teams/organic/hub-registry.json` — gsc_status + gsc_note ל-HUB-8 + HUB-9
- `docs/organic/organic-journal.md` — entry GSC integration
- `docs/organic/מצב-הפרויקט-האורגני.md` — post-publish flow + blocker
- `scripts/submit_gsc.py` — new

## SYSTEM IMPACT:
- כל HUB עתידי חייב לעבור 4 שלבים לפני שנחשב complete
- GSC לא יישכח — מתועד ב-hub-registry per HUB

## OPEN ISSUES:
- [ ] הוסף `gsc-access@babymania-001.iam.gserviceaccount.com` כ-Owner ב-GSC
- [ ] הרץ: `python scripts/submit_gsc.py` עבור HUB-8 + HUB-9 Pillar + HUB-6 + HUB-7

## NEXT STEP:
- הוספת service account כ-Owner ב-GSC → re-run submit → עדכן gsc_status ל-`gsc_submitted`

---

## DATE: 2026-04-20
## TASK: HUB-9 DIRECTION CHANGE — רשימת קניות → בובת ריבורן
## SCOPE: ניהול — שינוי עדיפות אורגנית

## WHAT CHANGED:
- HUB-9 שונה רשמית מ"רשימת קניות לתינוק" ל"בובת ריבורן"
- נימוק: Reborn = קטגוריה #1 בחנות (בובת ריבורן pos 2.7, בגדי ריבורן pos 1.5), 6 מוצרים קיימים, אפס HUB תומך
- "רשימת קניות לתינוק" (pos 36) נדחה ל-HUB-10

## FILES TOUCHED:
- `teams/organic/hub-registry.json` — HUB-9 added (planned, Reborn)
- `docs/organic/organic-journal.md` — entry 2026-04-20
- `docs/organic/מצב-הפרויקט-האורגני.md` — HUB-9 בטבלה + override note

## SYSTEM IMPACT:
- HUB-9 = בובת ריבורן. ממתין ל-execution plan.

## OPEN ISSUES:
- [ ] execution plan לכתיבת Pillar HUB-9 Reborn

## NEXT STEP:
- הכנת execution plan לכתיבת Pillar

---

## DATE: 2026-04-20
## TASK: OFFICIAL CLOSURE — LAYER 3 + LAYER 4
## SCOPE: ניהול — סגירה רשמית של שתי שכבות
## WHAT CHANGED:
- Layer 3 SEO: מוכרז COMPLETE — live audit אימת 36/36 clothing נקיים
- Layer 4 GEO: מוכרז COMPLETE — live audit אימת 241 clothing + 51 shoes נקיים
- failures היסטוריים (verify_failed, stage16 60.8%) — RUNTIME בלבד, לא data issue
- Batch A לא בוצע ולא נדרש — הכל היה תקין כבר
- clothing-journal.md עודכן עם מצב 2026-04-20
- shoes-journal.md עודכן עם מצב 2026-04-20
- phase2-scope-confirmation.md — סומן SUPERSEDED
- BABYMANIA-MASTER-PROMPT.md → v4.2 — שתי שכבות COMPLETE, Layer 5 FROZEN
## FILES TOUCHED:
- `docs/product/clothing-journal.md`
- `docs/product/shoes-journal.md`
- `docs/governance/phase2-scope-confirmation.md` (SUPERSEDED note)
- `docs/management/management-journal.md` (עדכון זה)
- `BABYMANIA-MASTER-PROMPT.md` (v4.2)
## SYSTEM IMPACT: תיעוד בלבד — אין שינוי ב-Shopify
## OPEN ISSUES:
- Layer 5: FROZEN — נדרשת החלטה ניהולית מפורשת של אייל לפתיחה
- PID 9179135017273 — metafield sync ממתין (non-blocking)
## NEXT STEP: החלטה ניהולית על Layer 5 בלבד

---

## DATE: 2026-04-20
## TASK: Layer 4 post-closure — gen_clothing_geo shoes guard
## SCOPE: Layer 4 — LOGIC fix (prevention only, no Shopify write)
## WHAT CHANGED:
- Audit: 51 shoes PIDs נסרקו live — נמצא 1 PID גבולי (לא 8 כנטען)
- שורש: `gen_clothing_geo.py` חסר shoes classification → gtype defaults to "בגד"
- Fix: הוסף guard בשורה 119 שחוסם shoes PIDs מלהיכנס לclothing generator
- אין write לShopify — הoutput ב-live תקין
## FILES TOUCHED:
- `scripts/gen_clothing_geo.py` (guard נוסף)
## SYSTEM IMPACT: מניעה — ריצה עתידית של clothing geo לא תוכל לכלול shoes PIDs
## OPEN ISSUES: 1 PID גבולי (9096634106169) — geo_who_for מקובל, לא מצריך שינוי
## NEXT STEP: 36 clothing SEO — track נפרד (Layer 3)

---

## DATE: 2026-04-20
## TASK: LAYER 4 GEO — CLOSURE DECLARATION
## SCOPE: Layer 4 — Phase 2 Batch A + Live Read-Back
## WHAT CHANGED:
- בוצע live read-back מלא ל-285 publisher PIDs דרך Shopify REST API
- ממצא: כל 51 shoes — CLEAN ✅ | כל clothing sampled — CLEAN ✅ | anomaly — NO GEO ✅
- Batch A לא נדרש — כל shoes כבר עם geo
- Layer 4 GEO מוכרז COMPLETE
- עודכן `docs/governance/phase2-live-readback-scope-lock.md` → STATUS: COMPLETE
## FILES TOUCHED:
- `docs/governance/phase2-live-readback-scope-lock.md` (עדכון — COMPLETE)
- `docs/management/management-journal.md` (עדכון זה)
- `BABYMANIA-MASTER-PROMPT.md` (עדכון — Layer 4 COMPLETE)
## SYSTEM IMPACT: אין — תיעוד בלבד. Shopify לא שונה.
## OPEN ISSUES:
- 36 clothing verify_failed — בעיית SEO בלבד (Layer 3 track)
- 8 shoes עם gtype="בגד" — לא קריטי, לתקן בעתיד דרך shoes geo generator
## NEXT STEP: Layer 5 — לאחר אישור ניהולי. Layer 5 נמצא ב-FREEZE (layer5-freeze.md)

---

## DATE: 2026-04-20
## TASK: P2-S2 SCOPE LOCK — LIVE READ-BACK EVIDENCE-BASED
## SCOPE: Layer 4 — Phase 2
## WHAT CHANGED:
- נוצר `docs/governance/phase2-live-readback-scope-lock.md` — LOCKED ✅
- ממצא קריטי: 241 clothing כבר תקינים — recovery אומת מ-artifacts
- ממצא קריטי: 51 shoes — geo לא נכתב מעולם — הם ה-Batch A האמיתי
- 36 verify_failed = בעיית SEO בלבד, לא geo — סקופ נפרד לחלוטין
- Shoes geo path צריך generate נפרד דרך shoes generator
## FILES TOUCHED:
- `docs/governance/phase2-live-readback-scope-lock.md` (חדש — LOCKED)
- `docs/management/management-journal.md` (עדכון זה)
## SYSTEM IMPACT: אין — תיעוד בלבד
## OPEN ISSUES:
- אישור אייל נדרש לפני Batch A
- 8 shoes עם gtype="בגד" — לתקן אחרי Batch A
- 36 SEO failures — Layer 3 track נפרד
## NEXT STEP: אישור אייל → Batch A — shoes geo generation (51 PIDs)

---

## DATE: 2026-04-20
## TASK: PHASE 2 LIVE READBACK PREP — PID LIST BUILD
## SCOPE: Layer 4 — Phase 2 Recovery Prep
## WHAT CHANGED:
- נבנתה רשימת PID נקייה ל-live read-back
- מקור: `output/stage-outputs/*_publisher.json`
- סך הכל: 285 PIDs — 0 כפילויות — anomaly 9881362759993 לא נמצא ברשימה
- נשמר: `C:/Windows/Temp/geo_readback_pid_list.json`
## FILES TOUCHED:
- `C:/Windows/Temp/geo_readback_pid_list.json` (חדש)
- `docs/management/management-journal.md` (עדכון זה)
## SYSTEM IMPACT: אין — הכנה בלבד
## OPEN ISSUES:
- Shopify live read-back טרם בוצע — מחכה ל-SHOPIFY_ACCESS_TOKEN פעיל
## NEXT STEP: live read-back עם token → scope lock → P2-S2 Batch A

---

## DATE: 2026-03-25
## TASK: בניית מערכת תיעוד ניהולי רשמית
## SCOPE: ניהול — כלל הפרויקט
## WHAT CHANGED:
- נוצר מבנה `docs/` מלא עם journals לכל תחום
- הוגדר source of truth מדויק לכל domain
- הוגדרה update-policy עם חוקי עדכון ברורים
- BABYMANIA-MASTER-PROMPT.md עודכן עם section תיעוד רשמי

## FILES TOUCHED:
- `docs/management/management-index.md` (חדש)
- `docs/management/source-of-truth.md` (חדש)
- `docs/management/update-policy.md` (חדש)
- `docs/management/management-journal.md` (חדש)
- `docs/operations/bridge-operations-journal.md` (חדש)
- `docs/operations/bridge-runtime-status.md` (חדש)
- `docs/product/shoes-journal.md` (חדש)
- `docs/product/clothing-journal.md` (חדש)
- `docs/product/infrastructure-journal.md` (חדש)
- `docs/organic/organic-journal.md` (חדש)
- `BABYMANIA-MASTER-PROMPT.md` (עודכן)

## SYSTEM IMPACT:
- יש עכשיו source of truth אחד ברור לכל domain
- Master prompt לא ישמש יותר כ-journal מלא
- כל תחום עם journal משלו

## OPEN ISSUES:
- journals ריקים עד לעדכון שוטף ראשון

## NEXT STEP:
- לעדכן journals לאחר כל משימה משמעותית בהתאם לupdate-policy.md

---

## DATE: 2026-03-25
## TASK: הגדרת Bridge כערוץ תפעול רשמי
## SCOPE: ניהול — workflow, ביטול copy-paste ידני
## WHAT CHANGED:
- הוחלט: Bridge הוא ערוץ התפעול הרשמי היחיד
- הוחלט: GPT כותב משימות ל-bridge/next-task.md, Claude Code מחזיר תוצאות
- הוחלט: אין עוד copy-paste ידני בין sessions

## FILES TOUCHED:
- `bridge/task-format.md`
- `bridge/EXECUTION_RULES.md`

## SYSTEM IMPACT:
- ביטול תלות בנוכחות ידנית של אייל כשליח
- עיגון workflow ב-bridge בלבד

## OPEN ISSUES:
- none

## NEXT STEP:
- bridge מוכן לשימוש יומיומי

---

## DATE: 2026-03-25
## TASK: סגירת Operations Lane — מעבר עדיפות ל-Shoes
## SCOPE: ניהול — שינוי עדיפות

## WHAT CHANGED:
- Operations lane הוכרז רשמית כ-CLOSED / OPERATIONAL
- עדיפות חוזרת ל-shoes lane

## SYSTEM IMPACT:
Operations lane סגורה. מבנה תפעולי מלא ופעיל:
- Bridge: `bridge/` path יחיד, singleton-safe, auto-start ב-login
- Task Scheduler: `BabyMania Bridge AutoStart` — Enabled, trigger logon
- Entrypoint: `start-bridge.bat` → `python -u bridge.py`
- כל משימה: `bridge/next-task.md` → claude.cmd → `bridge/last-result.md`

## PRIORITY DECISION:
```
Operations lane:  ✅ CLOSED
Shoes lane:       🔶 NEXT — ריצת test ראשונה על מוצר נעל אמיתי
Clothing lane:    ✅ Production (10 מוצרים ממתינים להעברה מ-clothing-test)
Organic lane:     ✅ HUB-8 pending — נושא טרם נבחר
```

## FILES TOUCHED: תיעוד בלבד
## OPEN ISSUES: none
## NEXT STEP: shoes — ריצת pipeline ראשונה על מוצר נעל אמיתי דרך orchestrator

## DATE: 2026-04-19
## TASK: P2-S1 — FINAL AFFECTED SCOPE CONFIRMATION
## SCOPE: Layer 4 — Phase 2 Recovery
## WHAT CHANGED:
- נוצר `docs/governance/phase2-scope-confirmation.md`
- VERDICT: PARTIAL PASS — Batch A חסום עד Shopify live read-back
- ממצא קריטי: "241 fixed" claim ב-conductor-state אינו ניתן לאימות — אין output artifacts
- מאומת: 36 clothing verify_failed (מ-bulk_push_verify_results.json)
- מאומת: PID 9881362759993 מוחרג לחלוטין
- REVIEW REQUIRED: 7 PIDs ללא publisher, shoes scope לא אושר, scope הכולל דורש live read-back
## FILES TOUCHED:
- `docs/governance/phase2-scope-confirmation.md` (חדש)
## SYSTEM IMPACT: אין — תיעוד בלבד
## OPEN ISSUES:
- Shopify live read-back נדרש לפני Batch A
- shoes scope לא מאושר
- 7 PIDs ללא publisher טעונים חקירה
## NEXT STEP: Shopify live read-back → scope lock → P2-S2 Batch A

---

## DATE: 2026-04-19
## TASK: PHASE 2 DECOMPOSITION — LAYER 4 LIVE RECOVERY
## SCOPE: Layer 4 — Phase 2 Controlled Rollout Planning
## WHAT CHANGED:
- Phase 2 פורק ל-9 תת-שלבים (P2-S1 עד P2-S9)
- rollout ladder הוגדר: 8 → 20 → 50 → remainder
- stop conditions מפורשות לכל batch
- Visual QA חובה לאחר כל batch
## FILES TOUCHED:
- `docs/management/management-journal.md` (עדכון זה)
## SYSTEM IMPACT: תכנון בלבד — אין שינוי runtime
## OPEN ISSUES:
- Phase 2 לא נפתח עד חתימת אייל על phase1-closure-declaration.md
## NEXT STEP: P2-S1 — Final Affected Scope Confirmation (אחרי אישור אייל)

---

## DATE: 2026-04-19
## TASK: P1-S7 — PHASE 1 EXIT VERIFICATION AND CLOSURE DECLARATION
## SCOPE: Layer 4 — Phase 1 Emergency Hardening
## WHAT CHANGED:
- אומתו כל 9 תנאי היציאה של Phase 1 — כולם PASS
- נוצר `docs/governance/phase1-closure-declaration.md`
- VERDICT: PASS
## FILES TOUCHED:
- `docs/governance/phase1-closure-declaration.md` (חדש)
## SYSTEM IMPACT: אין — תיעוד ממשל בלבד
## OPEN ISSUES:
- Check E מחכה לאישור אייל על ספי Jaccard (0.6/0.8)
- Phase 2 מחכה לחתימת אייל על phase1-closure-declaration.md
## NEXT STEP: Phase 2 — Live Recovery of 241 products (אחרי אישור אייל)

---

## DATE: 2026-04-19
## TASK: P1-S6 — GATES IMPLEMENTATION + TEST BATCH VERIFY
## SCOPE: Layer 4 — Phase 1 Emergency Hardening
## WHAT CHANGED:
- נוצר `scripts/gate1_hardening.py` — Gate 1 Extended (empty values, duplicate keys, anomaly exclusion, bundle duplicates)
- נוצר `scripts/gate2_semantic.py` — Gate 2 Semantic (Checks A–D פעילים, Check E מושבת)
- נוצר `scripts/test_gate_batch.py` — test harness עם 4 מוצרים אמיתיים + 4 הזרקות סינתטיות
- עודכן `00-team-lead/orchestrator.py` — gates מוטמעים לפני push_preflight עם graceful degradation
- הורץ test batch: **9/9 passed**
  - 4 real products: PASS ✓
  - Anomaly PID 9881362759993: Gate1 FAIL ✓
  - Fingerprint injection: Gate2 check_a FAIL ✓
  - Type mismatch injection: Gate2 check_b FAIL ✓
  - Fabricated claim injection: Gate2 check_c FAIL ✓
  - Check E: DISABLED ✓
## FILES TOUCHED:
- `scripts/gate1_hardening.py` (חדש)
- `scripts/gate2_semantic.py` (חדש)
- `scripts/test_gate_batch.py` (חדש)
- `00-team-lead/orchestrator.py` (עדכון)
## SYSTEM IMPACT:
- Gates פעילים ב-pipeline לפני כל push
- Graceful degradation: gate load error → warning בלוג, push ממשיך
- Check E מושבת עד אישור אייל על ספי Jaccard (0.6/0.8)
## OPEN ISSUES:
- Check E מחכה לאישור אייל על ספים
- P1-S7 Exit Verification טרם בוצע
## NEXT STEP: P1-S7 — Phase 1 Exit Verification

---

## DATE: 2026-04-19
## TASK: P1-S5 — VISUAL QA CHECKLIST
## SCOPE: Layer 4 — Phase 1 Emergency Hardening
## WHAT CHANGED:
- נוצר `docs/operations/visual-qa-checklist.md`
- הוגדרו 8 visual checks מחייבים (A–H)
- הוגדר פורמט אישור רשמי + stop rule מוחלט
- מעתה: אין push ללא VISUAL QA APPROVAL חתום
## FILES TOUCHED:
- `docs/operations/visual-qa-checklist.md` (חדש)
## SYSTEM IMPACT: אין — תיעוד ממשל בלבד
## OPEN ISSUES: none
## NEXT STEP: P1-S6 — Gates Implementation (מחכה לאישור T2 של semantic-gate-spec.md)

---

## DATE: 2026-04-19
## TASK: P1-S4 SECOND T2 REVIEW — APPROVED
## SCOPE: Layer 4 — Phase 1 Emergency Hardening
## WHAT CHANGED:
- semantic-gate-spec.md v1.1 עבר T2 review שני בהצלחה
- כל 5 הבלוקרים מ-review ראשון אושרו כפתורים
- נמצאו 3 הערות קטנות — אף אחת לא חוסמת
## FILES TOUCHED: management-journal.md בלבד
## SYSTEM IMPACT: אין — review בלבד
## OPEN ISSUES:
- Check E ספים (0.6/0.8) טעונים אישור אייל לפני הפעלה
- Check E יישאר מושבת עד אישור — Checks A–D פעילים מיד
## NEXT STEP: P1-S6 — Gates Implementation (Checks A–D מיידי, Check E אחרי אישור אייל על ספים)

---

## DATE: 2026-04-19
## TASK: P1-S4.1 — SEMANTIC GATE SPEC BLOCKERS FIX
## SCOPE: Layer 4 — Phase 1 Emergency Hardening
## WHAT CHANGED:
- תוקנו 5 בלוקרים שאותרו ב-T2 review:
  1. Check A: הוחלף תנאי עמום ברשימת patterns סגורה (BM-, handle patterns, file suffixes)
  2. Check B: הוחלף "כנושא ראשי" ב-3 כללים מדידים עם lookup tables
  3. Check C: הוסר Known Anomalies Registry מ-INPUTS (לא רלוונטי לcheck זה)
  4. Check D: נוסף `batch_product_titles[]` ל-INPUTS + הבהרה שתנאי 2-3 הם batch-level
  5. Check E: הוגדר אלגוריתם 4-gram Jaccard similarity + תוקן output conflict לגבי semantic_signature
- גרסה עודכנה ל-v1.1-draft
## FILES TOUCHED:
- `docs/operations/semantic-gate-spec.md` (עדכון)
## SYSTEM IMPACT: אין — spec בלבד
## OPEN ISSUES:
- ספי Check E (0.6/0.8) טעונים אישור אייל לפני implementation
- T2 review שני נדרש
## NEXT STEP: T2 review שני על semantic-gate-spec v1.1

---

## DATE: 2026-04-19
## TASK: P1-S4 — GATE 2 SEMANTIC GATE SPEC
## SCOPE: Layer 4 — Phase 1 Emergency Hardening
## WHAT CHANGED:
- נוצר `docs/operations/semantic-gate-spec.md`
- הוגדרו 5 checks מדויקים: Technical Fingerprint, Type Consistency, Fabricated Claim, Description Bleed, Template Repetition
- הוגדרו output format, batch-level stop rule, ו-out of scope
- סף Check E (template repetition) מסומן כ"טעון אישור אייל" — לא נקבע שרירותית
## FILES TOUCHED:
- `docs/operations/semantic-gate-spec.md` (חדש)
## SYSTEM IMPACT: אין — spec בלבד, אין שינוי קוד
## OPEN ISSUES:
- סף Check E טעון אישור אייל לפני implementation
- המסמך כולו טעון אישור T2
## NEXT STEP: אישור T2 של semantic-gate-spec.md → P1-S5 (Visual QA Checklist)

---

## DATE: 2026-04-19
## TASK: P1-S3 — GATE 1 AUDIT (STRUCTURE GATE GAP MAP)
## SCOPE: Layer 4 — Phase 1 Emergency Hardening
## WHAT CHANGED:
- בוצע audit קריאה-בלבד על כל ה-validators הקיימים
- מופו: orchestrator.py, 06-validator.md, 09-page-validator.md, conductor.py, contracts.yaml, config.yaml
- זוהו פערים ב-bundle level, JSON schema enforcement, ו-duplicate detection
## FILES TOUCHED: management-journal.md בלבד (קריאה בלבד על שאר הקבצים)
## SYSTEM IMPACT: אין — audit בלבד
## OPEN ISSUES:
- Gate 2 spec (P1-S4) עדיין לא כתוב
- הפערים המזוהים מחכים ל-P1-S6 לביצוע
## NEXT STEP: P1-S4 — Gate 2 Semantic Gate Spec

---

## DATE: 2026-04-19
## TASK: P1-S2 — KNOWN ANOMALIES REGISTRY
## SCOPE: Layer 4 — Phase 1 Emergency Hardening
## WHAT CHANGED:
- נוצר `docs/operations/known-anomalies-registry.md`
- PID 9881362759993 (מנורת לילה להירדמות) נרשם רשמית כ-ANOMALY-001
- הוגדר פורמט רשמי לרשומות עתידיות
## FILES TOUCHED:
- `docs/operations/known-anomalies-registry.md` (חדש)
## SYSTEM IMPACT:
- אין שינוי runtime — תיעוד בלבד
- P1-S2 סגור
## OPEN ISSUES: none
## NEXT STEP: P1-S3 — Gate 1 Audit

---

## DATE: 2026-04-19
## TASK: P1-S1 — LAYER 5 FREEZE DECLARATION
## SCOPE: Layer 4 — Phase 1 Emergency Hardening
## WHAT CHANGED:
- Layer 5 הוקפא רשמית
- נוצר `docs/governance/layer5-freeze.md` עם תאריך, סיבות, תנאי הפשרה, וסמכות
## FILES TOUCHED:
- `docs/governance/layer5-freeze.md` (חדש)
## SYSTEM IMPACT:
- אין שינוי runtime — תיעוד ממשל בלבד
- P1-S1 סגור — תנאי הכניסה לשאר Phase 1 מתקיים
## OPEN ISSUES: none
## NEXT STEP: P1-S2 — Known Anomalies Registry

---

## DATE: 2026-04-19
## TASK: PHASE 1 DECOMPOSITION — AUTOMATION-HARDENING-PLAN v1
## SCOPE: Layer 4 — Emergency Hardening
## WHAT CHANGED:
- Phase 1 פורק ל-7 תתי-שלבים ביצועיים
- סדר ביצוע מחייב נקבע
- stop conditions הוגדרו
## FILES TOUCHED:
- `docs/management/AUTOMATION-HARDENING-PLAN-v1.md` (קריאה)
- `docs/management/management-journal.md` (עדכון זה)
## SYSTEM IMPACT: תכנון בלבד — אין שינוי runtime
## OPEN ISSUES: Implementation טרם החל
## NEXT STEP: P1-S1 — Layer 5 Freeze Declaration

---

## LAYER-4 GEO ROLLOUT CLOSED — 2026-04-19 04:24:25

## DECISION:
Layer 4 GEO push (STAGE-14 through STAGE-16) completed successfully.
All 292 products enriched with geo metafields. Excluded anomaly (PID 9881362759993) verified clean.

## SYSTEM IMPACT:
- 292 products now carry baby_mania.geo_who_for + geo_use_case (all)
- 20 products additionally carry baby_mania.geo_comparison (eligible only)
- Shopify live state confirmed via read-back (STAGE-15 PASS)

## PRIORITY DECISION:
```
Layer 4 GEO:  COMPLETE
STAGE-17:     NEXT
```

## FILES TOUCHED: shoes-journal.md, task-log.md, conductor-state.md, stage-progress.md
## OPEN ISSUES: none
## NEXT STEP: STAGE-17
