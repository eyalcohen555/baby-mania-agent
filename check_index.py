import requests
import re
import time

BASE = "https://babymania-il.com"
PRODUCT_URL = "/products/easy-sleep"

ARTICLES = [
    {"cluster": "HUB-1-pillar", "path": "/blogs/news/how-to-help-baby-sleep-through-the-night"},
    {"cluster": "HUB-1-C1",     "path": "/blogs/news/white-noise-for-babies"},
    {"cluster": "HUB-1-C2",     "path": "/blogs/news/baby-sleep-routine"},
    {"cluster": "HUB-1-C4",     "path": "/blogs/news/all-in-one-baby-sleep-solution"},
]

INTERNAL_SLUGS = [
    "how-to-help-baby-sleep-through-the-night",
    "white-noise-for-babies",
    "baby-sleep-routine",
    "all-in-one-baby-sleep-solution",
]

UA = {"User-Agent": "Mozilla/5.0 BabyManiaBot/1.0 (indexing-check)"}

results = []

for art in ARTICLES:
    url = BASE + art["path"]
    r = requests.get(url, headers=UA, timeout=30, allow_redirects=True)
    html = r.text

    status = r.status_code

    # Canonical — try both attribute orderings
    can1 = re.search(r'rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', html, re.I)
    can2 = re.search(r'href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', html, re.I)
    canonical_href = (can1 or can2)
    canonical_href = canonical_href.group(1) if canonical_href else "NOT FOUND"
    canonical_ok = canonical_href.rstrip("/") == url.rstrip("/")

    # Robots noindex
    noindex = bool(re.search(r'noindex', html, re.I) and re.search(r'<meta[^>]+robots', html, re.I))
    index_allowed = not noindex

    # Sitemap presence — check /sitemap.xml once
    found_internal = []
    self_slug = art["path"].split("/")[-1]
    for slug in INTERNAL_SLUGS:
        if slug != self_slug and slug in html:
            found_internal.append(slug)

    product_ok = PRODUCT_URL in html

    results.append({
        "cluster": art["cluster"],
        "url": url,
        "status": status,
        "canonical": canonical_href,
        "canonical_ok": canonical_ok,
        "index_allowed": index_allowed,
        "internal_links": found_internal,
        "product_link": product_ok,
    })
    time.sleep(1)

# Check sitemap
print("Checking sitemap.xml ...")
sm = requests.get(BASE + "/sitemap.xml", headers=UA, timeout=30)
sitemap_content = sm.text
sitemap_results = {}
for art in ARTICLES:
    slug = art["path"].split("/")[-1]
    sitemap_results[art["cluster"]] = slug in sitemap_content

print()
print("=" * 70)
print("VERIFICATION TABLE")
print("=" * 70)
print(f"{'Cluster':<15} {'Status':<8} {'Canon':<6} {'Index':<7} {'Sitemap':<9} {'InLinks':<5} {'ProdLink'}")
print("-" * 70)
for r in results:
    cl = r["cluster"]
    st = str(r["status"])
    ca = "OK" if r["canonical_ok"] else "FAIL"
    ix = "YES" if r["index_allowed"] else "NO"
    sm_ok = "YES" if sitemap_results.get(cl) else "CHECK"
    il = str(len(r["internal_links"]))
    pl = "YES" if r["product_link"] else "NO"
    print(f"{cl:<15} {st:<8} {ca:<6} {ix:<7} {sm_ok:<9} {il:<5} {pl}")

print()
print("=" * 70)
print("DETAIL: CANONICAL URLS")
print("=" * 70)
for r in results:
    print(f"  {r['cluster']}: {r['canonical']}")

print()
print("=" * 70)
print("DETAIL: INTERNAL LINKS DETECTED PER ARTICLE")
print("=" * 70)
for r in results:
    print(f"  {r['cluster']}: {r['internal_links']}")

print()
print("=" * 70)
print("INDEX SUBMISSION LIST — Google Search Console > URL Inspection")
print("=" * 70)
for r in results:
    print(r["url"])
