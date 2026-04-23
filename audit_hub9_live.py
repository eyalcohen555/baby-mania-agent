"""
audit_hub9_live.py
Live audit of published HUB-9 articles — fetches real Shopify pages.
"""
import re
import requests
from html.parser import HTMLParser

BLOG_BASE = "https://babymania-il.com/blogs/news"
SHOP = "a2756c-c0.myshopify.com"
TOKEN = "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"
API_BASE = f"https://{SHOP}/admin/api/2024-10"
API_HDR = {"X-Shopify-Access-Token": TOKEN}
BLOG_ID = 109164036409

ARTICLES = [
    {"id": "Pillar", "article_id": 685558825273,
     "url": f"{BLOG_BASE}/bobat-reborn-madrih-male-ma-ze-ech-livhor"},
    {"id": "C1", "article_id": 686018756921,
     "url": f"{BLOG_BASE}/eich-livhor-bobat-reborn-madrih-larokhesh-harishon"},
    {"id": "C2", "article_id": 686018724153,
     "url": f"{BLOG_BASE}/bigdei-reborn-ma-hilobshot-eizeh-midah-matima"},
    {"id": "C3", "article_id": 686018789689,
     "url": f"{BLOG_BASE}/bobat-reborn-kematana-mi-matim-mah-levakesh"},
    {"id": "C4", "article_id": 686018822457,
     "url": f"{BLOG_BASE}/eich-letapel-bobat-reborn-shmirah-nikuy-achsun"},
    {"id": "C5", "article_id": 686018855225,
     "url": f"{BLOG_BASE}/reborn-leyeladim-vs-reborn-leasefanim-mah-hahedel"},
    {"id": "C6", "article_id": 686018887993,
     "url": f"{BLOG_BASE}/hashvahat-bobot-reborn-midot-khomrim-tekhunyot"},
]

HUB9_HANDLES = {
    "Pillar": "bobat-reborn-madrih-male-ma-ze-ech-livhor",
    "C1": "eich-livhor-bobat-reborn-madrih-larokhesh-harishon",
    "C2": "bigdei-reborn-ma-hilobshot-eizeh-midah-matima",
    "C3": "bobat-reborn-kematana-mi-matim-mah-levakesh",
    "C4": "eich-letapel-bobat-reborn-shmirah-nikuy-achsun",
    "C5": "reborn-leyeladim-vs-reborn-leasefanim-mah-hahedel",
    "C6": "hashvahat-bobot-reborn-midot-khomrim-tekhunyot",
}

REBORN_PIDS = ["9689589383481", "9690182385977", "9690182418745",
               "9690182451513", "9690247627065", "9690247659833"]


def fetch_article_api(article_id):
    """Fetch article body_html from Shopify Admin API."""
    r = requests.get(
        f"{API_BASE}/blogs/{BLOG_ID}/articles/{article_id}.json",
        headers=API_HDR, timeout=30
    )
    if r.status_code != 200:
        return None, r.status_code
    d = r.json()["article"]
    return d, 200


def fetch_live_page(url):
    """Fetch actual rendered page from live site."""
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    return r.status_code, r.text


def parse_images(html):
    """Extract all img tags: src, alt, lazy."""
    imgs = re.findall(r'<img([^>]*)>', html, re.I)
    results = []
    for attrs in imgs:
        src = re.search(r'src=["\']([^"\']*)["\']', attrs)
        data_src = re.search(r'data-src=["\']([^"\']*)["\']', attrs)
        alt = re.search(r'alt=["\']([^"\']*)["\']', attrs)
        loading = re.search(r'loading=["\']([^"\']*)["\']', attrs)
        results.append({
            "src": src.group(1) if src else "",
            "data_src": data_src.group(1) if data_src else "",
            "alt": alt.group(1) if alt else "",
            "lazy": (loading.group(1) if loading else ""),
        })
    return results


def parse_links(html):
    hrefs = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', html, re.I)
    return hrefs


def extract_article_body(html):
    """Extract article body from live page (look for article-template or rte div)."""
    # Try multiple selectors Shopify uses
    for pattern in [
        r'<div[^>]+class="[^"]*rte[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]+class="[^"]*article[^"]*body[^"]*"[^>]*>(.*?)</div>',
        r'<article[^>]*>(.*?)</article>',
    ]:
        m = re.search(pattern, html, re.DOTALL | re.I)
        if m:
            return m.group(1)
    return html  # fallback: full page


def strip_tags(html):
    return re.sub(r'<[^>]+>', ' ', html)


def check_img_live(src):
    if not src or not src.startswith("http"):
        return None
    try:
        r = requests.head(src, timeout=8, allow_redirects=True)
        return r.status_code
    except Exception:
        return 0


# Generic/trust warning patterns (Hebrew + English)
GENERIC_PATTERNS = [
    (r'בובת ריבורן היא(?! רק| לא| גם)', "generic opener — 'ריבורן היא'"),
    (r'(?i)שאלות נפוצות', None),  # FAQ section — OK, skip
    (r'ניתן (?:לרכוש|למצוא|להשיג).{0,30}בקלות', "vague availability claim"),
    (r'מחיר\s+(?:נגיש|סביר|טוב)', "vague price claim"),
    (r'(?:איכות|מוצר)\s+(?:גבוהה|מעולה|טובה)\s+(?:ב|מ)', "generic quality claim"),
    (r'(?:כל|הכל|כולם)\s+(?:אוהבים|רוצים|צריכים)', "vague mass appeal"),
    (r'\bplaceholder\b', "literal placeholder text"),
    (r'\[(?:CLUSTER|HUB|PILLAR)', "unreplaced placeholder"),
    (r'lorem ipsum', "lorem ipsum text"),
]

print("=" * 72)
print("HUB-9 LIVE POST-PUBLISH AUDIT")
print("=" * 72)

audit_results = {}

for art in ARTICLES:
    print(f"\n{'='*72}")
    print(f"ARTICLE: {art['id']} — {art['url']}")
    print("=" * 72)

    # 1. Fetch API body_html (the actual content stored in Shopify)
    api_data, api_status = fetch_article_api(art["article_id"])
    if not api_data:
        print(f"  API FETCH FAIL — HTTP {api_status}")
        audit_results[art["id"]] = {"fail": True}
        continue

    body_html = api_data.get("body_html", "")
    title = api_data.get("title", "")
    published_at = api_data.get("published_at", "")

    print(f"  title: {title}")
    print(f"  published_at: {published_at}")
    print(f"  body_html length: {len(body_html)} chars")

    # 2. Fetch live page for HTTP check
    live_status, live_html = fetch_live_page(art["url"])
    print(f"  live HTTP: {live_status}")

    # 3. IMAGES from body_html (what Shopify actually stores)
    imgs = parse_images(body_html)
    cdn_imgs = [i for i in imgs if "cdn.shopify.com" in i["src"]]
    empty_imgs = [i for i in imgs if not i["src"] and not i["data_src"]]
    relative_imgs = [i for i in imgs if i["src"] and not i["src"].startswith("http") and not i["src"].startswith("//")]

    print(f"\n  [IMAGES]")
    print(f"    Total img tags in body: {len(imgs)}")
    print(f"    CDN images: {len(cdn_imgs)}")
    if imgs:
        for img in imgs:
            src_display = img["src"][:80] if img["src"] else "(empty)"
            code = check_img_live(img["src"]) if img["src"] else "no-src"
            print(f"      src={src_display} | alt={img['alt'][:40]} | HTTP={code}")
    if empty_imgs:
        print(f"    WARN: {len(empty_imgs)} empty src")
    if relative_imgs:
        print(f"    WARN: {len(relative_imgs)} relative src: {[i['src'] for i in relative_imgs]}")

    img_count = len(imgs)
    img_flag = "OK" if img_count >= 2 else ("WARN:only-1" if img_count == 1 else "FAIL:no-images")

    # 4. LINKS from body_html
    links = parse_links(body_html)
    hub9_links = [l for l in links if "babymania-il.com/blogs/news" in l
                  and any(h in l for h in HUB9_HANDLES.values())]
    product_links = [l for l in links if "/products/" in l or "/search" in l
                     or any(pid in l for pid in REBORN_PIDS)]
    external_blog_links = [l for l in links if "babymania-il.com/blogs/news" in l
                           and l not in [art["url"]]]
    broken_placeholder_links = [l for l in links if "[" in l]

    print(f"\n  [LINKS]")
    print(f"    Total links: {len(links)}")
    print(f"    HUB-9 internal links: {len(hub9_links)}")
    print(f"    Product/store links: {len(product_links)}")
    if broken_placeholder_links:
        print(f"    FAIL: placeholder in href: {broken_placeholder_links}")

    # 5. CONTENT QUALITY — analyze body text
    body_text = strip_tags(body_html)
    word_count = len(body_text.split())

    print(f"\n  [CONTENT]")
    print(f"    Word count (approx): {word_count}")

    generic_hits = []
    for pattern, label in GENERIC_PATTERNS:
        if label is None:
            continue
        if re.search(pattern, body_text, re.I):
            generic_hits.append(label)

    # Check for unreplaced placeholders
    placeholder_in_body = re.findall(r'\[(?:CLUSTER-URL|HUB-\d+-[A-Z-]+-URL)[^\]]*\]', body_html)
    if placeholder_in_body:
        print(f"    FAIL: unreplaced placeholders: {placeholder_in_body}")

    if generic_hits:
        print(f"    GENERIC warnings: {generic_hits}")
    else:
        print(f"    Generic check: CLEAN")

    # 6. First ~200 chars of body text for quick read
    intro_text = body_text[:300].strip()
    print(f"    Intro: {intro_text[:200]}")

    # 7. Structure checks
    has_faq = "שאלות נפוצות" in body_html or "faq" in body_html.lower()
    has_h2 = bool(re.findall(r'<h2', body_html, re.I))
    has_h3 = bool(re.findall(r'<h3', body_html, re.I))
    h2_count = len(re.findall(r'<h2', body_html, re.I))
    h3_count = len(re.findall(r'<h3', body_html, re.I))

    print(f"\n  [STRUCTURE]")
    print(f"    H2s: {h2_count} | H3s: {h3_count} | FAQ: {has_faq}")

    audit_results[art["id"]] = {
        "title": title,
        "live_status": live_status,
        "word_count": word_count,
        "img_count": img_count,
        "img_flag": img_flag,
        "cdn_imgs": len(cdn_imgs),
        "hub9_links": len(hub9_links),
        "product_links": len(product_links),
        "generic_hits": generic_hits,
        "placeholder_remaining": placeholder_in_body,
        "has_faq": has_faq,
        "h2": h2_count,
        "h3": h3_count,
    }

# SUMMARY TABLE
print("\n\n" + "=" * 72)
print("AUDIT SUMMARY TABLE")
print("=" * 72)
print(f"{'Art':6} {'HTTP':5} {'Words':6} {'Imgs':5} {'ImgFlag':12} {'Hub9Lnk':8} {'ProdLnk':8} {'Generic':8}")
print("-" * 72)
for art in ARTICLES:
    r = audit_results.get(art["id"], {})
    if r.get("fail"):
        print(f"{art['id']:6} FETCH FAIL")
        continue
    print(
        f"{art['id']:6} {str(r.get('live_status','-')):5} "
        f"{str(r.get('word_count','-')):6} "
        f"{str(r.get('img_count','-')):5} "
        f"{r.get('img_flag','?'):12} "
        f"{str(r.get('hub9_links','-')):8} "
        f"{str(r.get('product_links','-')):8} "
        f"{'WARN' if r.get('generic_hits') else 'OK':8}"
    )
