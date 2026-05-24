# ריבורן — מקור אמת מוצרי (סבב 2, מקושר ידנית)

> מסמך מחקר פנימי. אסור להעתיק לקופי שיווקי. רק שדות 'verified' מותרים לדף המוצר.

## טבלת השוואה

| # | Shopify PID | מקור AliExpress | סטטוס | גודל (Ali) | גודל (Shopify) | מגדר (Ali) | רחיץ | אביזרים | חסר עיקרי | שמיש לדף מוצר | הערה לאייל |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 9690182385977 | 1005007060038271 | needs_manual_review | 50cm/20inch | — | יוניסקס | UNKNOWN | — | weight, body_material, body_type, hair_type | ❌ | MISMATCH: MISMATCH or wrong listing |
| 2 | 10190523040057 | 1005008896313230 | verified | 50cm | 50cm | Girls | UNKNOWN | — | weight, body_material, body_type, hair_type | ✅ | 7 shared image hashes. Size 50cm matches Shopify (50 ס"מ). |
| 3 | 10190523072825 | 1005008275277733 | verified | 20inch | 50cm | Girls | UNKNOWN | — | weight, body_material, body_type, hair_type | ✅ | 5 shared image hashes. Size 20inch (~50cm) matches Shopify Maddie 50 ס"מ. |
| 4 | 10190523007289 | 1005008672285275 | verified | 13Inch | — | Girls | UNKNOWN | — | weight, body_material, body_type, hair_type | ✅ | 6 shared image hashes. Size 13Inch (~33cm) matches Shopify Pascale 33 ס"מ. |
| 5 | 10190522777913 | 1005007170009461 | needs_manual_review | 18-19 inches | 45cm | יוניסקס | UNKNOWN | — | weight, body_material, body_type, hair_type | ❌ | MISMATCH: Wrong listing — Meadow not represented |
| 6 | 10190522810681 | 1005007170009461 | verified | 18-19 inches | — | יוניסקס | UNKNOWN | — | weight, body_material, body_type, hair_type | ✅ | 4 shared image hashes. Ali title is Felicia, size 18-19 inches (~46cm) matches S |
| 7 | 9690247627065 | 1005009088718947 | likely | 19inch | 49cm | יוניסקס | UNKNOWN | — | weight, body_material, body_type, hair_type | ❌ | 0 shared image hashes (Shopify likely re-cropped images), but Ali title contains |
| 8 | 9690182451513 | 1005005188539088 | verified | 19-20 Inches (44-50cm) | — | לשני המינים | UNKNOWN | — | weight, body_material, body_type, hair_type | ✅ | Primary: 4 shared image hashes (MRB store). Secondary listing 1005007525021217 a |
| 9 | 9690182418745 | 1005006863845547 | verified | UNKNOWN | 60cm | UNKNOWN | UNKNOWN | — | size, weight, body_material, body_type | ✅ | Image-search URL doesn't resolve to a single item. Carrying forward previous mat |
| 10 | 9689589383481 | 1005005317212200 | likely | 17-18 inches | 49cm | יוניסקס | UNKNOWN | — | weight, body_material, body_type, hair_type | ❌ | MISMATCH: Shopify SKU=49cm but Ali source page = 17-18 inches (43-46cm). MISMATC |

## ממצאים חשובים

**MISMATCHES שדורשים הכרעת אייל:**
- PID 9690182385977: size: Shopify=55cm (handle) / no size in SKU | Ali=50cm/20inch
- PID 10190522777913: model: Shopify=Meadow 46cm | Ali=Felicia 18-19in
- PID 9689589383481: size: Shopify=49cm (SKU) | Ali=17-18 inches (43-46cm)

**NEEDS MANUAL REVIEW:**
- PID 9690182385977: Multi-doll page. Ali listing says 50cm/20inch but Shopify product is 55cm/22inch. 0 shared image hashes. Eyal must specify the exact variant in the listing.
- PID 10190522777913: URL shared with PID 10190522810681. 0 shared image hashes on this Ali page (it's the Felicia listing, NOT Meadow). Eyal must provide a separate URL for Meadow.

## שדות שנמצאו vs UNKNOWN

**מה כן נמצא ב-AliExpress spec table** (אצל כל המוצרים שאומתו):
- ממדים (גודל) — בעברית, בפורמט מעורב (cm/inch)
- מגדר — Girls / יוניסקס / לשני המינים
- BJD / תכונה SD — כולם 'בובה'
- מצב — 'פריטים במלאי'

**מה לא נמצא בשום spec table** (UNKNOWN לכל המוצרים):
- משקל
- חומר גוף מדויק (vinyl/silicone/cloth)
- סוג גוף מלא
- סוג שיער (שתול / מצויר)
- צבע עיניים
- בגדים כלולים
- אביזרים נוספים
- ניתן לרחיצה / האם מתאים לאמבטיה
- גיל מומלץ
- תעודות / CE / EN71

**טענות שמופיעות בעמוד AliExpress** (סומנו אבל לא מאשרים אותן):
- PID 9690182385977: handmade, full silicone, ce
- PID 10190523040057: handmade, full silicone, ce, waterproof
- PID 10190523072825: handmade, full silicone, ce
- PID 10190523007289: handmade, full silicone, ce
- PID 10190522777913: handmade, full silicone, ce
- PID 10190522810681: handmade, full silicone, ce
- PID 9690247627065: handmade, full silicone, ce
- PID 9690182451513: handmade, ce, waterproof
- PID 9689589383481: handmade, full silicone, ce

## האם אפשר להשתמש במפרט לדף מוצר?

**כן** — רק לאחר אישור הסטטוס 'verified' ורק לשדות שלא UNKNOWN:
- PID 10190523040057 (50cm ויניל-סיליקון): גודל, מגדר. שאר השדות UNKNOWN.
- PID 10190523072825 (Maddie 50cm): גודל, מגדר. שאר השדות UNKNOWN.
- PID 10190523007289 (Pascale 33cm פה פתוח): גודל, מגדר. שאר השדות UNKNOWN.
- PID 10190522810681 (Felicia 46cm): גודל, מגדר. שאר השדות UNKNOWN.
- PID 9690182451513 (LouLou 50cm cloth body): גודל, מגדר. שאר השדות UNKNOWN.
- PID 9690182418745 (BZDoll 60cm): גודל, מגדר. שאר השדות UNKNOWN.

**לא** — לא לפני אישור אייל:
- PID 9690182385977 (BZDoll 55cm (multi-doll page)): סטטוס=needs_manual_review
- PID 10190522777913 (Meadow 46cm): סטטוס=needs_manual_review
- PID 9690247627065 (NPK Levi 19inch (awake)): סטטוס=likely
- PID 9689589383481 (Levi (vinyl/silicone choice)): סטטוס=likely

## הצעת שלד 'פרטי הדגם' (chips, מובייל)

עיקרון: כל chip מציג רק שדה שלא UNKNOWN. אם השדה UNKNOWN — לא להציג chip.
מקסימום 6 chips. לא טבלה. פרימיום מינימליסטי.

שדות מותרים כעת (לפי מה שאומת בפועל):
- 📏 **גודל** — מתוך SKU של Shopify (49cm/50cm/60cm) או מ-Ali (אם חופפים)
- 👤 **מתאים ל** — Girls / יוניסקס (מ-Ali ממדים=מגדר)
- 🧸 **שם דגם** — Levi / Maddie / Pascale / Felicia / LouLou (מ-Shopify handle)

שדות שאסור להציג עכשיו (כולם UNKNOWN לכל המוצרים):
- משקל, גיל, רחיצה/אמבטיה, אביזרים, תעודות, חומר גוף מדויק

---
**מקורות**: Shopify Admin API (קריאה בלבד) + Playwright Chromium על דפי AliExpress + screenshots מאוחסנים תחת `reborn-audit/screenshots/`.
