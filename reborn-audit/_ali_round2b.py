"""Round 2b — same tasks, fixed spec regex + Show-More click + save HTML."""
import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

ROOT = Path(__file__).resolve().parent
SHOTS = ROOT / "screenshots"
HTMLS = ROOT / "html"
SHOTS.mkdir(exist_ok=True)
HTMLS.mkdir(exist_ok=True)

SHOPIFY = json.loads((ROOT / "_shopify_raw_v2.json").read_text(encoding="utf-8"))

TASKS = [
    (9690182385977,  "https://he.aliexpress.com/item/1005007060038271.html"),
    (10190523040057, "https://he.aliexpress.com/item/1005008896313230.html"),
    (10190523072825, "https://he.aliexpress.com/item/1005008275277733.html"),
    (10190523007289, "https://he.aliexpress.com/item/1005008672285275.html"),
    (10190522777913, "https://he.aliexpress.com/item/1005007170009461.html"),
    (10190522810681, "https://he.aliexpress.com/item/1005007170009461.html"),
    (9690247627065,  "https://he.aliexpress.com/item/1005009088718947.html"),
    (9690182451513,  "https://he.aliexpress.com/item/1005007525021217.html"),
    (9690182451513,  "https://he.aliexpress.com/item/1005005188539088.html"),
    (9690182418745,  "https://he.aliexpress.com/w/wholesale-.html?isNewImageSearch=y&filename=OSS%2Fae-image-search-sg2%2F2026-05-21%2F8e9f5620-1446-4b43-9e51-23fa3ff93b54.jpg&imageId=1779364019678"),
    (9689589383481,  "https://he.aliexpress.com/item/1005005317212200.html"),
]

ITEM_ID_RE = re.compile(r"/item/(\d{10,16})\.html")
SHOPIFY_HASH_RE = re.compile(r"/S([0-9a-f]{32})[A-Za-z0-9]?\.")

SAFETY_TERMS = [
    "handmade", "full silicone", "medical grade", "ce ", "en71",
    "magnetic pacifier", "waterproof", "bath safe", "therapy",
    "anxiety", "dementia",
]
SAFETY_TERMS_HE = [
    "עבודת יד", "סיליקון מלא", "רפואי", "EN71", "CE",
    "עמיד למים", "אמבטיה", "מגנט", "טיפול",
]


def shopify_hashes_for(pid):
    for p in SHOPIFY["products"]:
        if p["id"] == pid:
            return {SHOPIFY_HASH_RE.search(i["src"]).group(1)
                    for i in p["images"]
                    if SHOPIFY_HASH_RE.search(i["src"])}
    return set()


def page_hashes(html):
    found = set()
    for m in re.finditer(r"alicdn\.com/[^\"'>\s]+", html):
        for h in re.findall(r"([0-9a-f]{32})", m.group(0)):
            found.add(h)
    for m in re.finditer(r"S([0-9a-f]{32})", html):
        found.add(m.group(1))
    return found


SPEC_PATTERN = re.compile(
    r'class="specification--title[^"]*"\s*>\s*<span>\s*([^<]{1,80}?)\s*</span>'
    r'.*?'
    r'class="specification--desc[^"]*"\s*title="([^"]{0,300})"',
    re.DOTALL,
)


def extract_specs(html):
    pairs = {}
    for m in SPEC_PATTERN.finditer(html):
        k = re.sub(r"\s+", " ", m.group(1)).strip()
        v = re.sub(r"\s+", " ", m.group(2)).strip()
        if k and v:
            pairs.setdefault(k, v)
    return pairs


def safety_scan(text):
    found = []
    low = text.lower()
    for term in SAFETY_TERMS:
        pattern = r"(?<![a-z])" + re.escape(term.strip()) + r"(?![a-z])"
        if re.search(pattern, low):
            found.append(term.strip())
    for term_he in SAFETY_TERMS_HE:
        if term_he in text:
            found.append(term_he)
    return sorted(set(found))


def visible_variants(page):
    variants = []
    # Try several common SKU selectors
    for sel in [
        '[class*="sku-item-image"] img',
        '[class*="sku-item-title"]',
        '[class*="sku-property"] [class*="sku-item"]',
    ]:
        try:
            els = page.locator(sel).all()
            for e in els:
                try:
                    txt = ""
                    # Prefer alt or title
                    for attr in ("alt", "title"):
                        v = e.get_attribute(attr, timeout=500)
                        if v:
                            txt = v
                            break
                    if not txt:
                        try:
                            txt = (e.inner_text(timeout=500) or "").strip()
                        except Exception:
                            pass
                    txt = txt.strip()
                    if txt and txt not in variants and len(txt) < 80:
                        variants.append(txt)
                except Exception:
                    continue
            if variants:
                break
        except Exception:
            continue
    return variants


def get_item_id(url):
    m = ITEM_ID_RE.search(url)
    return m.group(1) if m else "imgsearch"


def fetch(page, pid, url):
    item_id = get_item_id(url)
    sh = shopify_hashes_for(pid)
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
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        time.sleep(7)
        for _ in range(12):
            page.evaluate("window.scrollBy(0, 1100)")
            time.sleep(0.4)
        time.sleep(2)
        # Click "Show more" on specs if present
        try:
            btn = page.locator('button:has-text("להציג יותר")').first
            if btn.count() > 0:
                btn.click(timeout=4000)
                time.sleep(2)
        except Exception:
            pass
        # Also try English variant
        try:
            btn = page.locator('button:has-text("Show More")').first
            if btn.count() > 0:
                btn.click(timeout=3000)
                time.sleep(2)
        except Exception:
            pass

        # Scrollback to top and screenshot
        page.evaluate("window.scrollTo(0, 0)"); time.sleep(1)
        s1 = SHOTS / f"{pid}-{item_id}-top.png"
        page.screenshot(path=str(s1), full_page=False)
        entry["screenshots"].append(s1.name)
        # scroll down a bit and shot
        page.evaluate("window.scrollBy(0, 1800)"); time.sleep(1)
        s2 = SHOTS / f"{pid}-{item_id}-mid.png"
        page.screenshot(path=str(s2), full_page=False)
        entry["screenshots"].append(s2.name)
        # full spec area
        page.evaluate("window.scrollBy(0, 2200)"); time.sleep(1)
        s3 = SHOTS / f"{pid}-{item_id}-spec.png"
        page.screenshot(path=str(s3), full_page=False)
        entry["screenshots"].append(s3.name)

        html = page.content()
        # Save HTML for later analysis
        (HTMLS / f"{pid}-{item_id}.html").write_text(html, encoding="utf-8")

        title_m = re.search(r"<title>([^<]+)</title>", html, re.IGNORECASE)
        if title_m:
            entry["ali_title"] = title_m.group(1).strip()

        ali_h = page_hashes(html)
        entry["image_hashes"] = sorted(ali_h)[:40]
        entry["shared_hashes"] = sorted(sh & ali_h)[:15]

        entry["spec_pairs"] = extract_specs(html)
        entry["visible_variants"] = visible_variants(page)
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
            locale="he-IL",
            viewport={"width": 1366, "height": 900},
        )
        page = ctx.new_page()
        for pid, url in TASKS:
            print(f"\n=== PID {pid} -> {url}")
            e = fetch(page, pid, url)
            print(f"   shared={len(e['shared_hashes'])} specs={len(e['spec_pairs'])} variants={len(e['visible_variants'])}")
            if e["spec_pairs"]:
                for k, v in list(e["spec_pairs"].items())[:8]:
                    print(f"     {k} = {v[:80]}")
            out.append(e)
        browser.close()
    (ROOT / "_ali_round2b.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\nWROTE _ali_round2b.json")


if __name__ == "__main__":
    main()
