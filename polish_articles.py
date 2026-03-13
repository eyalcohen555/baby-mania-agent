"""
Content polish + UX pass on 4 Baby Sleep hub articles.
Parts: title fix, image insertion, Hebrew polish, CTA microcopy, verify.
"""

import sys, io, re, time, requests, json
from shopify_client import _headers, BASE_URL

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BLOG_ID = 109164036409
PRODUCT_ID = 10085913231673

ARTICLES = {
    "pillar": {"id": 681270837561, "handle": "how-to-help-baby-sleep-through-the-night"},
    "C1":     {"id": 681272115513, "handle": "white-noise-for-babies"},
    "C2":     {"id": 681272181049, "handle": "baby-sleep-routine"},
    "C4":     {"id": 681272246585, "handle": "all-in-one-baby-sleep-solution"},
}

NEW_TITLES = {
    "pillar": "איך לעזור לתינוק לישון בלילה — המדריך המלא להורים עייפים",
    "C1":     "רעש לבן לתינוקות — האם זה באמת עוזר?",
    "C2":     "שגרת שינה לתינוק: מדריך שלב-אחר-שלב",
    "C4":     "פתרון שינה לתינוק: מה באמת עובד",
}


def fetch_article(article_id):
    r = requests.get(
        f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json",
        headers=_headers(), timeout=30
    )
    r.raise_for_status()
    return r.json()["article"]


def put_article(article_id, payload):
    r = requests.put(
        f"{BASE_URL}/blogs/{BLOG_ID}/articles/{article_id}.json",
        headers=_headers(),
        json={"article": {"id": article_id, **payload}},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["article"]


# ─── 0. Fetch product images ─────────────────────────────────────────────────
print("Fetching EasySleep product images...")
r = requests.get(
    f"{BASE_URL}/products/{PRODUCT_ID}/images.json",
    headers=_headers(), timeout=30
)
r.raise_for_status()
product_images = r.json()["images"]
print(f"  Found {len(product_images)} product images")
for img in product_images[:5]:
    print(f"  id={img['id']} w={img['width']} h={img['height']} src={img['src'][:80]}")

# Pick best images: prefer landscape (width > height)
landscape_imgs = [i for i in product_images if i["width"] >= i["height"]]
portrait_imgs  = [i for i in product_images if i["width"] < i["height"]]
available = landscape_imgs if landscape_imgs else product_images

IMG_1 = available[0]["src"] if len(available) > 0 else None
IMG_2 = available[1]["src"] if len(available) > 1 else (available[0]["src"] if available else None)
if not IMG_2 and len(product_images) > 1:
    IMG_2 = product_images[1]["src"]

print(f"\n  IMG_1: {IMG_1[:80] if IMG_1 else 'NONE'}")
print(f"  IMG_2: {IMG_2[:80] if IMG_2 else 'NONE'}")


def make_img_block(src, alt, caption=None):
    cap_html = f'\n      <p class="img-caption">{caption}</p>' if caption else ""
    return (
        f'\n    <div class="article-img" style="margin:28px 0;text-align:center;">'
        f'\n      <img src="{src}" alt="{alt}" loading="lazy"'
        f' style="max-width:100%;border-radius:12px;box-shadow:0 2px 16px rgba(61,43,31,.1);">'
        f'{cap_html}'
        f'\n    </div>\n'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────────────────────

def fix_cta(html):
    """Standardize CTA button text across all articles."""
    replacements = [
        # Product card buttons
        ('לפרטים ורכישה',    'לעמוד המוצר'),
        ('לפרטים',           'לעמוד המוצר'),
        ('לרכישה — ₪319',   'לרכישת EasySleep™'),
        # CTA banner product button
        ('לצפייה ב-EasySleep™', 'לרכישת EasySleep™'),
        ('לצפייה ב-EasySleep',  'לרכישת EasySleep™'),
        # Internal link CTAs
        ('המדריך המלא →',    'למדריך המלא'),
        ('לקריאה נוספת',     'לקריאה נוספת'),  # already correct
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    return html


def polish_hebrew(html):
    """Targeted Hebrew language improvements — naturalness fixes."""
    fixes = [
        # Clunky phrases → natural
        ('כדאי לעיין ב',                    'מומלץ לקרוא גם את ה'),
        ('עיינו ב',                          'קראו גם: '),
        ('כפי שניתן לראות',                 'כפי שרואים'),
        ('יש לציין כי',                     'חשוב לדעת:'),
        ('ניתן לומר',                        'אפשר לומר'),
        ('ביצוע',                            'ביצוע'),  # keep
        ('על מנת ל',                         'כדי ל'),
        ('על מנת שה',                        'כדי שה'),
        ('בנוסף לכך',                        'בנוסף,'),
        ('בהתאם לכך',                        'בהתאם,'),
        ('לאור האמור',                       'לכן'),
        ('המלצה שלנו',                       'ההמלצה שלנו'),
        ('לידי ביטוי',                       'לידי ביטוי'),  # keep
        # Formal → conversational
        ('הורים המחפשים',                    'הורים שמחפשים'),
        ('תינוקות הסובלים',                  'תינוקות שסובלים'),
        ('ילדים המתקשים',                    'ילדים שמתקשים'),
        ('מחקרים מראים ש',                   'מחקרים מראים:'),
        # Fix spacing issues
        ('  ',                               ' '),
        # Mixed English labels in Hebrew context
        ('QUICK ANSWER BOX',                 ''),
        # AEO label cleanup
        ('תשובה מהירה',                      'תשובה מהירה'),  # keep
    ]
    for old, new in fixes:
        html = html.replace(old, new)
    return html


# ─────────────────────────────────────────────────────────────────────────────
# ARTICLE PILLAR — how-to-help-baby-sleep-through-the-night
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("ARTICLE 1: PILLAR")
art = fetch_article(ARTICLES["pillar"]["id"])
body = art["body_html"]
old_title = art["title"]

# Part 3: Hebrew polish
body = polish_hebrew(body)

# Part 4: CTA fix
body = fix_cta(body)

# Part 2: Images — after intro-box and mid-article (before H2#sleep-routine or similar)
IMG_PILLAR_1 = make_img_block(
    IMG_1,
    "תינוקת ישנה בשקט — מדריך לשינת תינוקות",
    "שינה טובה מתחילה בסביבה נכונה ושגרה עקבית"
)
IMG_PILLAR_2 = make_img_block(
    IMG_2 or IMG_1,
    "EasySleep™ — מכשיר שינה חכם לתינוק, רעש לבן ומנורת לילה",
    "EasySleep™ — רעש לבן, מנורת לילה וטיימר במכשיר אחד"
)

# Insert IMG_1 after .intro-box closing div
if IMG_1 and 'class="intro-box"' in body and IMG_1 not in body:
    body = re.sub(
        r'(</div>\s*)(<!-- ── QUICK ANSWER)',
        lambda m: m.group(1) + IMG_PILLAR_1 + m.group(2),
        body, count=1
    )
    if IMG_1 not in body:  # fallback: after first </div>
        body = body.replace('</div>', '</div>' + IMG_PILLAR_1, 1)

# Insert IMG_2 before the 3rd H2
if IMG_2 and IMG_2 not in body:
    h2s = list(re.finditer(r'<h2 ', body))
    if len(h2s) >= 3:
        pos = h2s[2].start()
        body = body[:pos] + IMG_PILLAR_2 + body[pos:]

payload_p = {"title": NEW_TITLES["pillar"], "body_html": body}
result_p = put_article(ARTICLES["pillar"]["id"], payload_p)
print(f"  Title: '{old_title}' → '{result_p['title']}'")
print(f"  Images: {2 if IMG_2 else 1 if IMG_1 else 0} inserted")
print("  PUT: OK")
time.sleep(1)


# ─────────────────────────────────────────────────────────────────────────────
# ARTICLE C1 — white-noise-for-babies
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("ARTICLE 2: C1 white-noise-for-babies")
art2 = fetch_article(ARTICLES["C1"]["id"])
body2 = art2["body_html"]
old_title2 = art2["title"]

body2 = polish_hebrew(body2)
body2 = fix_cta(body2)

IMG_C1_1 = make_img_block(
    IMG_1,
    "תינוק ישן לצד מכשיר רעש לבן — שינה רגועה",
    "רעש לבן מסנן רעשים סביבתיים ועוזר לתינוק להירדם"
)
IMG_C1_2 = make_img_block(
    IMG_2 or IMG_1,
    "EasySleep™ — 5 מצבי רעש לבן לתינוקות",
    "EasySleep™ מציעה white, pink ו-brown noise — כל תינוק מוצא את הצליל שלו"
)

if IMG_1 and IMG_1 not in body2:
    body2 = re.sub(
        r'(</div>\s*)(<!-- ── QUICK ANSWER|<div class="quick-answer")',
        lambda m: m.group(1) + IMG_C1_1 + m.group(2),
        body2, count=1
    )

if IMG_2 and IMG_2 not in body2:
    h2s2 = list(re.finditer(r'<h2 ', body2))
    if len(h2s2) >= 3:
        pos = h2s2[2].start()
        body2 = body2[:pos] + IMG_C1_2 + body2[pos:]

payload_c1 = {"title": NEW_TITLES["C1"], "body_html": body2}
result_c1 = put_article(ARTICLES["C1"]["id"], payload_c1)
print(f"  Title: '{old_title2}' → '{result_c1['title']}'")
print(f"  Images: inserted")
print("  PUT: OK")
time.sleep(1)


# ─────────────────────────────────────────────────────────────────────────────
# ARTICLE C2 — baby-sleep-routine
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("ARTICLE 3: C2 baby-sleep-routine")
art4 = fetch_article(ARTICLES["C2"]["id"])
body4 = art4["body_html"]
old_title4 = art4["title"]

body4 = polish_hebrew(body4)
body4 = fix_cta(body4)

IMG_C2_1 = make_img_block(
    IMG_1,
    "הורים בונים שגרת שינה עם תינוק — אמבטיה, עיסוי, מנגינה",
    "שגרת שינה עקבית מקצרת את זמן ההירדמות תוך שבועיים"
)
IMG_C2_2 = make_img_block(
    IMG_2 or IMG_1,
    "EasySleep™ מדליק רעש לבן ומנורת לילה כחלק משגרת הערב",
    "שלב 5 בשגרה: עמעום אורות + רעש לבן + כיבוי עם טיימר"
)

if IMG_1 and IMG_1 not in body4:
    body4 = re.sub(
        r'(</div>\s*)(<!-- ── QUICK ANSWER|<div class="quick-answer")',
        lambda m: m.group(1) + IMG_C2_1 + m.group(2),
        body4, count=1
    )

if IMG_2 and IMG_2 not in body4:
    h2s4 = list(re.finditer(r'<h2 ', body4))
    if len(h2s4) >= 3:
        pos = h2s4[2].start()
        body4 = body4[:pos] + IMG_C2_2 + body4[pos:]

payload_c2 = {"title": NEW_TITLES["C2"], "body_html": body4}
result_c2 = put_article(ARTICLES["C2"]["id"], payload_c2)
print(f"  Title: '{old_title4}' → '{result_c2['title']}'")
print(f"  Images: inserted")
print("  PUT: OK")
time.sleep(1)


# ─────────────────────────────────────────────────────────────────────────────
# ARTICLE C4 — all-in-one-baby-sleep-solution
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("ARTICLE 4: C4 all-in-one-baby-sleep-solution")
art3 = fetch_article(ARTICLES["C4"]["id"])
body3 = art3["body_html"]
old_title3 = art3["title"]

body3 = polish_hebrew(body3)
body3 = fix_cta(body3)

IMG_C4_1 = make_img_block(
    IMG_1,
    "מכשיר שינה all-in-one לתינוק — רעש לבן, מנורת לילה, טיימר",
    "מכשיר אחד שעושה הכל: פחות עומס, יותר שינה"
)
IMG_C4_2 = make_img_block(
    IMG_2 or IMG_1,
    "EasySleep™ — השוואה: all-in-one מול מוצרים נפרדים",
    "EasySleep™ עומד בכל 5 הפרמטרים — במחיר נגיש מ-3 מכשירים נפרדים"
)

if IMG_1 and IMG_1 not in body3:
    body3 = re.sub(
        r'(</div>\s*)(<!-- ── QUICK ANSWER|<div class="quick-answer")',
        lambda m: m.group(1) + IMG_C4_1 + m.group(2),
        body3, count=1
    )

if IMG_2 and IMG_2 not in body3:
    h2s3 = list(re.finditer(r'<h2 ', body3))
    if len(h2s3) >= 3:
        pos = h2s3[2].start()
        body3 = body3[:pos] + IMG_C4_2 + body3[pos:]

payload_c4 = {"title": NEW_TITLES["C4"], "body_html": body3}
result_c4 = put_article(ARTICLES["C4"]["id"], payload_c4)
print(f"  Title: '{old_title3}' → '{result_c4['title']}'")
print(f"  Images: inserted")
print("  PUT: OK")
time.sleep(1)


# ─────────────────────────────────────────────────────────────────────────────
# PART 5 — VERIFY
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("VERIFICATION")

PILLAR_URL = "https://www.babymania-il.com/blogs/news/how-to-help-baby-sleep-through-the-night"
WHITE_URL  = "https://www.babymania-il.com/blogs/news/white-noise-for-babies"
ROUTINE_URL= "https://www.babymania-il.com/blogs/news/baby-sleep-routine"
ALLINONE_URL= "https://www.babymania-il.com/blogs/news/all-in-one-baby-sleep-solution"
PRODUCT_URL = "/products/easy-sleep"

checks = [
    {"key": "pillar", "id": ARTICLES["pillar"]["id"], "title": NEW_TITLES["pillar"],
     "self_url": PILLAR_URL, "internal": [WHITE_URL, ROUTINE_URL], "product": PRODUCT_URL},
    {"key": "C1",  "id": ARTICLES["C1"]["id"],  "title": NEW_TITLES["C1"],
     "self_url": WHITE_URL,  "internal": [PILLAR_URL, ROUTINE_URL], "product": PRODUCT_URL},
    {"key": "C2",  "id": ARTICLES["C2"]["id"],  "title": NEW_TITLES["C2"],
     "self_url": ROUTINE_URL,"internal": [PILLAR_URL, WHITE_URL],   "product": PRODUCT_URL},
    {"key": "C4",  "id": ARTICLES["C4"]["id"],  "title": NEW_TITLES["C4"],
     "self_url": ALLINONE_URL,"internal":[PILLAR_URL, WHITE_URL],  "product": PRODUCT_URL},
]

ver_results = []
for c in checks:
    a = fetch_article(c["id"])
    b = a["body_html"]
    title_ok = a["title"] == c["title"]
    int_ok = all(url.split("/blogs/news/")[1] in b for url in c["internal"])
    prod_ok = c["product"] in b
    img_ok  = ('<img ' in b) and (b.count('<img ') >= 2)
    rtl_ok  = 'dir="rtl"' in b or 'direction: rtl' in b or 'direction:rtl' in b
    ver_results.append({
        "key": c["key"], "title_ok": title_ok, "int_ok": int_ok,
        "prod_ok": prod_ok, "img_ok": img_ok, "rtl_ok": rtl_ok,
        "img_count": b.count('<img ')
    })
    time.sleep(0.4)

print(f"\n{'Article':<10} {'Title':<7} {'InLinks':<9} {'ProdLink':<10} {'Images':<10} {'RTL'}")
print("-" * 60)
for v in ver_results:
    print(
        f"{v['key']:<10} {'OK' if v['title_ok'] else 'FAIL':<7} "
        f"{'OK' if v['int_ok'] else 'FAIL':<9} {'OK' if v['prod_ok'] else 'FAIL':<10} "
        f"{str(v['img_count'])+'x OK' if v['img_ok'] else str(v['img_count'])+'x':<10} "
        f"{'OK' if v['rtl_ok'] else 'CHECK'}"
    )

print("\n" + "="*60)
print("DONE")
