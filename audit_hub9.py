import requests, re, os
from html.parser import HTMLParser

OUTPUT_DIR = r"C:\Projects\baby-mania-agent\output\hub9-reborn"
HEADERS_REQ = {"User-Agent": "Mozilla/5.0"}

ARTICLES = [
    {"id":"Pillar","file":"HUB9_Pillar_blog_article.html",
     "url":"https://babymania-il.com/blogs/news/bobat-reborn-madrih-male-ma-ze-ech-livhor"},
    {"id":"C1","file":"HUB9_C1_blog_article.html",
     "url":"https://babymania-il.com/blogs/news/eich-livhor-bobat-reborn-madrih-larokhesh-harishon"},
    {"id":"C2","file":"HUB9_C2_blog_article.html",
     "url":"https://babymania-il.com/blogs/news/bigdei-reborn-ma-hilobshot-eizeh-midah-matima"},
    {"id":"C3","file":"HUB9_C3_blog_article.html",
     "url":"https://babymania-il.com/blogs/news/bobat-reborn-kematana-mi-matim-mah-levakesh"},
    {"id":"C4","file":"HUB9_C4_blog_article.html",
     "url":"https://babymania-il.com/blogs/news/eich-letapel-bobat-reborn-shmirah-nikuy-achsun"},
    {"id":"C5","file":"HUB9_C5_blog_article.html",
     "url":"https://babymania-il.com/blogs/news/reborn-leyeladim-vs-reborn-leasefanim-mah-hahedel"},
    {"id":"C6","file":"HUB9_C6_blog_article.html",
     "url":"https://babymania-il.com/blogs/news/hashvahat-bobot-reborn-midot-khomrim-tekhunyot"},
]

HUB9_URLS = {a["id"]: a["url"] for a in ARTICLES}
REBORN_PIDS = ["9689589383481","9690182385977","9690182418745",
               "9690182451513","9690247627065","9690247659833"]
HUB2_PILLAR = "https://babymania-il.com/blogs/news/how-many-clothes-does-a-newborn-need"


class LinkImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "img":
            self.images.append(attrs.get("src", ""))


def check_url(url, timeout=10):
    try:
        r = requests.head(url, headers=HEADERS_REQ, timeout=timeout, allow_redirects=True)
        return r.status_code
    except Exception as e:
        return f"ERR:{e}"


print("=" * 70)
print("HUB-9 POST-PUBLISH AUDIT")
print("=" * 70)

# 1. URL LIVE
print("\n--- 1. URL LIVE ---")
url_results = {}
for art in ARTICLES:
    code = check_url(art["url"])
    ok = code == 200
    url_results[art["id"]] = ok
    print(f"  {art['id']:6} | HTTP {code} | {'PASS' if ok else 'FAIL'} | {art['url']}")

# 2. PLACEHOLDERS
print("\n--- 2. PLACEHOLDERS (local HTML) ---")
placeholder_pattern = re.compile(
    r"\[(?:CLUSTER-URL:[A-Z0-9]+|HUB-\d+-PILLAR-URL|HUB-\d+-[A-Z-]+-URL)\]"
)
placeholder_issues = {}
for art in ARTICLES:
    fpath = os.path.join(OUTPUT_DIR, art["file"])
    html = open(fpath, encoding="utf-8").read()
    found = placeholder_pattern.findall(html)
    placeholder_issues[art["id"]] = found
    status = "PASS" if not found else f"FAIL -- {found}"
    print(f"  {art['id']:6} | {status}")

# 3. INTERNAL LINKS
print("\n--- 3. INTERNAL LINKS (local HTML) ---")
link_issues = {}
link_details = {}
for art in ARTICLES:
    fpath = os.path.join(OUTPUT_DIR, art["file"])
    html = open(fpath, encoding="utf-8").read()
    parser = LinkImageParser()
    parser.feed(html)

    issues = []
    hub9_found = {k: False for k in HUB9_URLS}
    hub2_found = False

    for href in parser.links:
        if not href or href.startswith("#"):
            continue
        for cid, curl in HUB9_URLS.items():
            if curl in href:
                hub9_found[cid] = True
        if HUB2_PILLAR in href:
            hub2_found = True

    if art["id"] == "Pillar":
        for cid in ["C1", "C2", "C3", "C4", "C5", "C6"]:
            if not hub9_found[cid]:
                issues.append(f"MISSING link to {cid}")
    else:
        if not hub9_found["Pillar"]:
            issues.append("MISSING link to Pillar")
        if art["id"] == "C2" and not hub2_found:
            issues.append("MISSING link to HUB-2 Pillar")

    link_issues[art["id"]] = issues
    link_details[art["id"]] = {
        "hub9_found": hub9_found,
        "hub2_found": hub2_found,
        "all_links": parser.links,
    }
    status = "PASS" if not issues else f"FAIL -- {issues}"
    print(f"  {art['id']:6} | {status}")

# 4. IMAGES
print("\n--- 4. IMAGES (local HTML) ---")
image_issues = {}
for art in ARTICLES:
    fpath = os.path.join(OUTPUT_DIR, art["file"])
    html = open(fpath, encoding="utf-8").read()
    parser = LinkImageParser()
    parser.feed(html)

    issues = []
    empty_srcs = [s for s in parser.images if not s]
    broken = [
        s for s in parser.images
        if s and not s.startswith("http") and not s.startswith("//") and not s.startswith("data:")
    ]
    if empty_srcs:
        issues.append(f"{len(empty_srcs)} empty src")
    if broken:
        issues.append(f"relative/bad src: {broken[:3]}")

    image_issues[art["id"]] = issues
    total = len(parser.images)
    status = "PASS" if not issues else f"WARN -- {issues}"
    print(f"  {art['id']:6} | {total} imgs | {status}")

# 5. PRODUCT BRIDGE
print("\n--- 5. PRODUCT BRIDGE (local HTML) ---")
product_issues = {}
for art in ARTICLES:
    fpath = os.path.join(OUTPUT_DIR, art["file"])
    html = open(fpath, encoding="utf-8").read()

    pid_found = [p for p in REBORN_PIDS if p in html]
    prod_hrefs = re.findall(r'href=["\']([^"\']*\/products\/[^"\']+)["\']', html)

    issues = []
    if not pid_found and not prod_hrefs:
        issues.append("NO product links found")

    product_issues[art["id"]] = issues
    flag = "PASS" if not issues else "WARN"
    print(f"  {art['id']:6} | {flag} | PIDs:{len(pid_found)} product_hrefs:{len(prod_hrefs)}")

# 6. CROSS-ARTICLE COHERENCE
print("\n--- 6. CROSS-ARTICLE COHERENCE ---")
pillar_links = link_details["Pillar"]["hub9_found"]
clusters_linked = [cid for cid in ["C1","C2","C3","C4","C5","C6"] if pillar_links[cid]]
clusters_missing = [cid for cid in ["C1","C2","C3","C4","C5","C6"] if not pillar_links[cid]]
print(f"  Pillar -> clusters linked: {clusters_linked}")
if clusters_missing:
    print(f"  Pillar -> MISSING: {clusters_missing}")
for cid in ["C1", "C2", "C3", "C4", "C5", "C6"]:
    back = link_details[cid]["hub9_found"].get("Pillar", False)
    print(f"  {cid} -> Pillar: {'YES' if back else 'MISSING'}")
print(f"  C2 -> HUB-2 Pillar: {'YES' if link_details['C2']['hub2_found'] else 'MISSING'}")

# SUMMARY
print("\n" + "=" * 70)
print("AUDIT SUMMARY")
print("=" * 70)
all_url_ok = all(url_results.values())
all_placeholder_ok = all(not v for v in placeholder_issues.values())
all_link_ok = all(not v for v in link_issues.values())
all_image_ok = all(not v for v in image_issues.values())
all_product_ok = all(not v for v in product_issues.values())

print(f"URL LIVE:         {'PASS' if all_url_ok else 'FAIL'}")
print(f"PLACEHOLDERS:     {'PASS' if all_placeholder_ok else 'FAIL'}")
print(f"INTERNAL LINKS:   {'PASS' if all_link_ok else 'FAIL'}")
print(f"IMAGES:           {'PASS' if all_image_ok else 'FAIL'}")
print(f"PRODUCT BRIDGE:   {'PASS' if all_product_ok else 'WARN'}")
