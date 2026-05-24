"""Round 2 — manual-link AliExpress scraping with screenshots and spec extraction.

For each Shopify PID + given Ali URL:
  - Open with Playwright (real browser).
  - Wait for SPA to hydrate.
  - Screenshot to reborn-audit/screenshots/PID-itemID-<step>.png
  - Extract image hashes, spec table (multiple strategies), variants.
  - Cross-match image hashes vs Shopify hashes.
"""
import json
import re
import time
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

ROOT = Path(__file__).resolve().parent
SHOTS = ROOT / "screenshots"
SHOTS.mkdir(exist_ok=True)

SHOPIFY = json.loads((ROOT / "_shopify_raw_v2.json").read_text(encoding="utf-8"))

# (PID, Ali URL)
TASKS = [
    (9690182385977,  "https://he.aliexpress.com/item/1005007060038271.html"),
    (10190523040057, "https://he.aliexpress.com/item/1005008896313230.html"),
    (10190523072825, "https://he.aliexpress.com/item/1005008275277733.html"),
    (10190523007289, "https://he.aliexpress.com/item/1005008672285275.html"),
    (10190522777913, "https://he.aliexpress.com/item/1005007170009461.html"),
    (10190522810681, "https://he.aliexpress.com/item/1005007170009461.html"),
    (9690247627065,  "https://he.aliexpress.com/item/1005009088718947.html"),
    (9690182451513,  "https://he.aliexpress.com/item/1005007525021217.html"),
    # Also re-check the previous LouLou candidate for product #8
    (9690182451513,  "https://he.aliexpress.com/item/1005005188539088.html"),
    # #9 — image-search URL; cannot resolve to a single item without manual click
    (9690182418745,  "https://he.aliexpress.com/w/wholesale-.html?isNewImageSearch=y&filename=OSS%2Fae-image-search-sg2%2F2026-05-21%2F8e9f5620-1446-4b43-9e51-23fa3ff93b54.jpg&imageId=1779364019678"),
    (9689589383481,  "https://he.aliexpress.com/item/1005005317212200.html"),
]

HASH_RE = re.compile(r"S([0-9a-f]{32})")
ITEM_ID_RE = re.compile(r"/item/(\d{10,16})\.html")
SHOPIFY_HASH_RE = re.compile(r"/S([0-9a-f]{32})[A-Za-z0-9]?\.")

SAFETY_TERMS = [
    "handmade", "full silicone", "medical grade",
    "ce ", "en71", "magnetic pacifier",
    "waterproof", "bath safe", "therapy",
    "anxiety", "dementia",
]


def get_item_id(url):
    m = ITEM_ID_RE.search(url)
    return m.group(1) if m else "imgsearch"


def shopify_hashes_for(pid):
    for p in SHOPIFY["products"]:
        if p["id"] == pid:
            return {SHOPIFY_HASH_RE.search(i["src"]).group(1)
                    for i in p["images"]
                    if SHOPIFY_HASH_RE.search(i["src"])}
    return set()


def shopify_meta_for(pid):
    for p in SHOPIFY["products"]:
        if p["id"] == pid:
            return p
    return None


def page_hashes(html):
    """Extract any 32-hex hash that's part of an alicdn image URL or S<hash> token."""
    found = set()
    for m in re.finditer(r"alicdn\.com/[^\"'>\s]+", html):
        for h in re.findall(r"([0-9a-f]{32})", m.group(0)):
            found.add(h)
    for m in HASH_RE.finditer(html):
        found.add(m.group(1))
    return found


def parse_runparams(html):
    """Pull runParams JSON out of the inline script and look for spec attrs."""
    m = re.search(r"window\.runParams\s*=\s*({.+?});", html, re.DOTALL)
    if not m:
        # Try another shape
        m = re.search(r'"runParams"\s*:\s*({.+?})\s*[,}]', html, re.DOTALL)
    if not m:
        return None
    blob = m.group(1)
    # We don't try to parse as JSON (often malformed) — just regex-mine fields.
    return blob


def extract_specs(html):
    """Extract spec key/value pairs using multiple regex strategies."""
    pairs = {}
    # 1. Spec block in HTML
    for m in re.finditer(
        r'specification--title[^>]*>\s*([^<]{1,80})\s*<.*?specification--desc[^>]*>\s*([^<]{1,300})\s*<',
        html, re.IGNORECASE | re.DOTALL,
    ):
        k = re.sub(r"\s+", " ", m.group(1)).strip().lower()
        v = re.sub(r"\s+", " ", m.group(2)).strip()
        pairs.setdefault(k, v)

    # 2. JSON-style attrName/attrValue
    for m in re.finditer(
        r'"attrName"\s*:\s*"([^"]{1,80})"\s*,\s*"attrValue(?:Id)?"\s*:\s*"?([^",}]{1,200})"?',
        html,
    ):
        pairs.setdefault(m.group(1).strip().lower(),
                         m.group(2).strip())

    # 3. Generic name/value pairs in product info JSON
    for m in re.finditer(
        r'"propertyName"\s*:\s*"([^"]{1,80})"\s*,\s*"propertyValue"\s*:\s*"([^"]{1,200})"',
        html,
    ):
        pairs.setdefault(m.group(1).strip().lower(),
                         m.group(2).strip())

    # 4. AliExpress new format: "name":"...","value":"..."
    for m in re.finditer(
        r'\{[^{}]{0,200}"name"\s*:\s*"([^"]{1,80})"[^{}]{0,200}"value"\s*:\s*"([^"]{1,200})"[^{}]{0,200}\}',
        html,
    ):
        k = m.group(1).strip().lower()
        v = m.group(2).strip()
        # Filter junk — keep only entries that look like spec keys
        if any(t in k for t in ("brand", "material", "size", "weight",
                                 "age", "gender", "color", "model",
                                 "feature", "type", "filling", "hair",
                                 "eye", "theme", "origin", "certificate",
                                 "wash", "waterproof")):
            pairs.setdefault(k, v)
    return pairs


def pick(pairs, *keys):
    for k in keys:
        for sp_k, sp_v in pairs.items():
            if k in sp_k:
                return sp_v
    return "UNKNOWN"


def safety_scan(text):
    found = []
    low = text.lower()
    for term in SAFETY_TERMS:
        pattern = r"(?<![a-z])" + re.escape(term.strip()) + r"(?![a-z])"
        if re.search(pattern, low):
            found.append(term.strip())
    return sorted(set(found))


def extract_visible_variants(page):
    """Try to extract on-screen variant labels (size/color buttons)."""
    variants = []
    selectors = [
        '[class*="sku-property"] [class*="sku-item-name"]',
        '[class*="sku-list"] [class*="title"]',
        '[class*="SkuItem"] [class*="title"]',
    ]
    for sel in selectors:
        try:
            els = page.locator(sel).all()
            for e in els:
                try:
                    txt = (e.inner_text(timeout=1000) or "").strip()
                    if txt and txt not in variants and len(txt) < 80:
                        variants.append(txt)
                except Exception:
                    continue
            if variants:
                break
        except Exception:
            continue
    return variants


def fetch_and_extract(page, pid, url):
    item_id = get_item_id(url)
    entry = {
        "pid": pid,
        "url": url,
        "item_id": item_id if item_id != "imgsearch" else None,
        "is_image_search": item_id == "imgsearch",
        "screenshots": [],
        "ali_title": "UNKNOWN",
        "image_hashes": [],
        "shared_hashes": [],
        "spec_pairs": {},
        "visible_variants": [],
        "safety_present": [],
        "errors": [],
    }
    sh = shopify_hashes_for(pid)
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)
        # Scroll through to load specs
        for _ in range(8):
            page.evaluate("window.scrollBy(0, 1500)")
            time.sleep(0.5)
        time.sleep(2)
        # Screenshot 1 — full page top + scrolled
        try:
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(1)
            sp1 = SHOTS / f"{pid}-{item_id}-top.png"
            page.screenshot(path=str(sp1), full_page=False)
            entry["screenshots"].append(sp1.name)
        except Exception as e:
            entry["errors"].append(f"sshot top: {e}")
        try:
            page.evaluate("window.scrollBy(0, 2000)")
            time.sleep(1)
            sp2 = SHOTS / f"{pid}-{item_id}-spec.png"
            page.screenshot(path=str(sp2), full_page=False)
            entry["screenshots"].append(sp2.name)
        except Exception as e:
            entry["errors"].append(f"sshot spec: {e}")
        # Try clicking "Show More" on specs if exists
        try:
            page.evaluate(
                "() => { const el = document.querySelector('[class*=\"specification--showMore\"]'); if(el) el.click(); }"
            )
            time.sleep(1)
        except Exception:
            pass
        try:
            page.evaluate("window.scrollBy(0, 1500)")
            time.sleep(1)
            sp3 = SHOTS / f"{pid}-{item_id}-spec-more.png"
            page.screenshot(path=str(sp3), full_page=False)
            entry["screenshots"].append(sp3.name)
        except Exception:
            pass

        html = page.content()
        title_m = re.search(r"<title>([^<]+)</title>", html, re.IGNORECASE)
        if title_m:
            entry["ali_title"] = title_m.group(1).strip()

        ali_hashes = page_hashes(html)
        entry["image_hashes"] = sorted(ali_hashes)[:30]
        entry["shared_hashes"] = sorted(sh & ali_hashes)[:10]

        entry["spec_pairs"] = extract_specs(html)
        entry["visible_variants"] = extract_visible_variants(page)
        entry["safety_present"] = safety_scan(html)

    except PWTimeout as e:
        entry["errors"].append(f"timeout: {e}")
    except Exception as e:
        entry["errors"].append(f"error: {e}")
    return entry


def main():
    out = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 1366, "height": 900},
        )
        page = ctx.new_page()
        for (pid, url) in TASKS:
            print(f"\n=== PID {pid} -> {url}")
            e = fetch_and_extract(page, pid, url)
            print(f"   shared_hashes={len(e['shared_hashes'])}, spec_pairs={len(e['spec_pairs'])}, variants={len(e['visible_variants'])}, shots={len(e['screenshots'])}")
            if e['shared_hashes']:
                print(f"   matched: {e['shared_hashes'][:3]}")
            if e['spec_pairs']:
                for k, v in list(e['spec_pairs'].items())[:6]:
                    print(f"     spec: {k} = {v[:60]}")
            out.append(e)
        browser.close()
    (ROOT / "_ali_round2.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\nWROTE _ali_round2.json")


if __name__ == "__main__":
    main()
