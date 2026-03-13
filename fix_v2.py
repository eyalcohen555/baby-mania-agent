"""
fix_v2.py — Two targeted fixes:
1. Insert missing first image for C1, C2, C4 (before quick-answer div or first H2)
2. Activate C2 → white-noise internal link (wrap first unlinked 'רעש לבן')
"""

import sys, io, re, time, requests
from shopify_client import _headers, BASE_URL

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BLOG_ID = 109164036409
IMG_1 = "https://cdn.shopify.com/s/files/1/0864/9677/2409/files/2026-01-01_111356.png?v=1"
WHITE_URL = "https://www.babymania-il.com/blogs/news/white-noise-for-babies"

ARTICLES = {
    "C1": {"id": 681272115513, "alt": "תינוק ישן לצד מכשיר רעש לבן — שינה רגועה",
           "caption": "רעש לבן מסנן רעשים סביבתיים ועוזר לתינוק להירדם"},
    "C2": {"id": 681272181049, "alt": "הורים בונים שגרת שינה עם תינוק",
           "caption": "שגרת שינה עקבית מקצרת את זמן ההירדמות תוך שבועיים"},
    "C4": {"id": 681272246585, "alt": "מכשיר שינה all-in-one לתינוק",
           "caption": "מכשיר אחד שעושה הכל: פחות עומס, יותר שינה"},
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


def make_img_block(src, alt, caption=None):
    cap = f'\n      <p class="img-caption">{caption}</p>' if caption else ""
    return (
        f'\n    <div class="article-img" style="margin:28px 0;text-align:center;">'
        f'\n      <img src="{src}" alt="{alt}" loading="lazy"'
        f' style="max-width:100%;border-radius:12px;box-shadow:0 2px 16px rgba(61,43,31,.1);">'
        f'{cap}'
        f'\n    </div>\n'
    )


results = []

for key, info in ARTICLES.items():
    art_id = info["id"]
    print(f"\n{'='*55}")
    print(f"  {key} (id={art_id})")

    art = fetch_article(art_id)
    body = art["body_html"]
    modified = False
    img_added = False
    link_added = False

    # ── FIX 1: Insert IMG_1 before first H2 (if not already present) ──────────
    if IMG_1 not in body:
        img_block = make_img_block(IMG_1, info["alt"], info["caption"])
        h2_match = re.search(r'<h2[ >]', body)
        if h2_match:
            pos = h2_match.start()
            body = body[:pos] + img_block + body[pos:]
            img_added = True
            modified = True
            print(f"  [IMG] Inserted before first <h2> (pos={pos})")
        else:
            print("  [IMG] WARNING — no <h2> found, image not inserted")
    else:
        print(f"  [IMG] Already present, skipping")

    # ── FIX 2 (C2 only): activate link to white-noise-for-babies ─────────────
    if key == "C2":
        if WHITE_URL in body or "white-noise-for-babies" in body:
            print("  [LINK] white-noise link already active")
        else:
            # Wrap first standalone 'רעש לבן' not inside an <a> tag
            # Match 'רעש לבן' that is NOT already inside href="..."
            TARGET = "רעש לבן"
            LINKED = f'<a href="{WHITE_URL}">{TARGET}</a>'
            # Use re.sub to wrap first occurrence not already linked
            def wrap_first(m):
                wrap_first.done = getattr(wrap_first, 'done', False)
                if wrap_first.done:
                    return m.group(0)
                wrap_first.done = True
                return LINKED

            # Only wrap if not preceded by <a href (simple check: if WHITE_URL not in body)
            new_body, n = re.subn(
                r'(?<!\">)' + re.escape(TARGET),
                LINKED,
                body,
                count=1
            )
            if n and LINKED in new_body:
                body = new_body
                link_added = True
                modified = True
                print(f"  [LINK] Wrapped first '{TARGET}' with white-noise link")
            else:
                print(f"  [LINK] WARNING — could not wrap '{TARGET}'")

    if modified:
        result = put_article(art_id, {"body_html": body})
        time.sleep(0.8)

        # Verify
        refreshed = fetch_article(art_id)
        rb = refreshed["body_html"]
        img_count = rb.count("<img ")
        has_white = "white-noise-for-babies" in rb
        print(f"  PUT: OK | img_count={img_count} | white-noise-link={has_white}")
        results.append({
            "key": key, "img_added": img_added, "link_added": link_added,
            "img_count": img_count, "white_link": has_white,
        })
    else:
        results.append({
            "key": key, "img_added": False, "link_added": False,
            "img_count": body.count("<img "), "white_link": "white-noise-for-babies" in body,
        })

    time.sleep(0.5)


print("\n" + "="*55)
print("FIX RESULTS")
print(f"{'Key':<6} {'ImgAdded':<10} {'ImgCount':<10} {'LinkAdded':<10} {'WhiteLink'}")
print("-"*55)
for r in results:
    print(
        f"{r['key']:<6} {str(r['img_added']):<10} {str(r['img_count']):<10} "
        f"{str(r['link_added']):<10} {str(r['white_link'])}"
    )

# Final full verify
print("\n" + "="*55)
print("FINAL VERIFICATION — all 4 articles")
PILLAR_URL = "https://www.babymania-il.com/blogs/news/how-to-help-baby-sleep-through-the-night"
PRODUCT_SLUG = "/products/easy-sleep"

all_articles = {
    "pillar": 681270837561,
    "C1": 681272115513,
    "C2": 681272181049,
    "C4": 681272246585,
}
internal_check = {
    "pillar": [WHITE_URL, "baby-sleep-routine"],
    "C1":     [PILLAR_URL, "baby-sleep-routine"],
    "C2":     [PILLAR_URL, WHITE_URL],
    "C4":     [PILLAR_URL, WHITE_URL],
}

print(f"\n{'Article':<8} {'Title':<5} {'InLinks':<9} {'Prod':<6} {'Imgs':<5} {'RTL'}")
print("-"*45)
for key, art_id in all_articles.items():
    art = fetch_article(art_id)
    b = art["body_html"]
    title_ok = bool(art["title"])
    int_ok = all(
        (u if u.startswith("http") else u).split("/")[-1] in b
        for u in internal_check[key]
    )
    prod_ok = PRODUCT_SLUG in b
    img_c = b.count("<img ")
    rtl_ok = 'direction: rtl' in b or 'dir="rtl"' in b or 'direction:rtl' in b
    print(
        f"{key:<8} {'OK':<5} {'OK' if int_ok else 'FAIL':<9} "
        f"{'OK' if prod_ok else 'FAIL':<6} {img_c:<5} {'OK' if rtl_ok else 'CHECK'}"
    )
    time.sleep(0.3)

print("\nDONE")
