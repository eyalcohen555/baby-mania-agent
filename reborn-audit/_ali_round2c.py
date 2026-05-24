"""Round 2c — fresh browser per task to defeat AliExpress baxia rate limiting."""
import json
import random
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

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
    (10190522810681, "https://he.aliexpress.com/item/1005007170009461.html"),
    (9690247627065,  "https://he.aliexpress.com/item/1005009088718947.html"),
    (9690182451513,  "https://he.aliexpress.com/item/1005007525021217.html"),
    (9690182451513,  "https://he.aliexpress.com/item/1005005188539088.html"),
    (9689589383481,  "https://he.aliexpress.com/item/1005005317212200.html"),
]

ITEM_ID_RE = re.compile(r"/item/(\d{10,16})\.html")
SHOPIFY_HASH_RE = re.compile(r"/S([0-9a-f]{32})[A-Za-z0-9]?\.")

SAFETY_TERMS = [
    "handmade", "full silicone", "medical grade", "ce ", "en71",
    "magnetic pacifier", "waterproof", "bath safe", "therapy",
    "anxiety", "dementia",
]
SAFETY_HE = ["עבודת יד", "סיליקון מלא", "רפואי", "EN71", "CE",
             "עמיד למים", "ניתן לרחיצה", "מגנט"]

SPEC_PATTERN = re.compile(
    r'class="specification--title[^"]*"\s*>\s*<span>\s*([^<]{1,80}?)\s*</span>'
    r'.*?'
    r'class="specification--desc[^"]*"\s*title="([^"]{0,300})"',
    re.DOTALL,
)


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
    for t in SAFETY_TERMS:
        if re.search(r"(?<![a-z])" + re.escape(t.strip()) + r"(?![a-z])", low):
            found.append(t.strip())
    for t in SAFETY_HE:
        if t in text:
            found.append(t)
    return sorted(set(found))


def visible_variants(page):
    out = []
    for sel in ['[class*="sku-item-image"] img',
                '[class*="sku-item-title"]',
                '[class*="sku-property"] [class*="sku-item"]']:
        try:
            for e in page.locator(sel).all():
                try:
                    t = ""
                    for a in ("alt", "title"):
                        v = e.get_attribute(a, timeout=500)
                        if v:
                            t = v; break
                    if not t:
                        try:
                            t = (e.inner_text(timeout=500) or "").strip()
                        except Exception:
                            pass
                    t = t.strip()
                    if t and t not in out and len(t) < 80:
                        out.append(t)
                except Exception:
                    pass
            if out:
                break
        except Exception:
            continue
    return out


def get_item_id(url):
    m = ITEM_ID_RE.search(url)
    return m.group(1) if m else "imgsearch"


def fetch_one(pw, pid, url):
    item_id = get_item_id(url)
    sh = shopify_hashes_for(pid)
    entry = {
        "pid": pid, "url": url,
        "item_id": item_id if item_id != "imgsearch" else None,
        "is_image_search": item_id == "imgsearch",
        "screenshots": [], "ali_title": "UNKNOWN",
        "image_hashes": [], "shared_hashes": [],
        "spec_pairs": {}, "visible_variants": [],
        "safety_present": [], "captcha": False, "errors": [],
    }
    browser = pw.chromium.launch(headless=True)
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0.0.0 Safari/537.36",
        locale="he-IL",
        viewport={"width": 1366, "height": 900},
    )
    page = ctx.new_page()
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        time.sleep(7)
        # human-like slow scroll
        for _ in range(14):
            page.evaluate("window.scrollBy(0, 900)")
            time.sleep(random.uniform(0.4, 0.9))
        time.sleep(2)
        # try Show More
        for label in ["להציג יותר", "Show More", "更多"]:
            try:
                btn = page.locator(f'button:has-text("{label}")').first
                if btn.count() > 0:
                    btn.click(timeout=4000)
                    time.sleep(2)
                    break
            except Exception:
                pass

        # Screenshots
        page.evaluate("window.scrollTo(0, 0)"); time.sleep(1)
        s1 = SHOTS / f"{pid}-{item_id}-top.png"
        page.screenshot(path=str(s1), full_page=False)
        entry["screenshots"].append(s1.name)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight/2)"); time.sleep(1)
        s2 = SHOTS / f"{pid}-{item_id}-mid.png"
        page.screenshot(path=str(s2), full_page=False)
        entry["screenshots"].append(s2.name)
        # Find spec section
        try:
            el = page.locator('[class*="specification--prop"]').first
            if el.count() > 0:
                el.scroll_into_view_if_needed(timeout=3000)
                time.sleep(1)
                s3 = SHOTS / f"{pid}-{item_id}-spec.png"
                page.screenshot(path=str(s3), full_page=False)
                entry["screenshots"].append(s3.name)
        except Exception:
            pass

        html = page.content()
        (HTMLS / f"{pid}-{item_id}.html").write_text(html, encoding="utf-8")

        entry["captcha"] = "specification--prop" not in html and (
            "captcha" in html.lower() or "punish" in html.lower() or
            len(html) < 100000)

        title_m = re.search(r"<title>([^<]+)</title>", html, re.IGNORECASE)
        if title_m:
            entry["ali_title"] = title_m.group(1).strip()
        ah = page_hashes(html)
        entry["image_hashes"] = sorted(ah)[:40]
        entry["shared_hashes"] = sorted(sh & ah)[:15]
        entry["spec_pairs"] = extract_specs(html)
        entry["visible_variants"] = visible_variants(page)
        entry["safety_present"] = safety_scan(html)
    except Exception as e:
        entry["errors"].append(str(e)[:200])
    finally:
        try:
            ctx.close()
            browser.close()
        except Exception:
            pass
    return entry


def main():
    out = []
    with sync_playwright() as pw:
        for i, (pid, url) in enumerate(TASKS):
            print(f"\n=== [{i+1}/{len(TASKS)}] PID {pid} -> {url}")
            e = fetch_one(pw, pid, url)
            print(f"   shared={len(e['shared_hashes'])} specs={len(e['spec_pairs'])} captcha={e['captcha']} title={e['ali_title'][:60]}")
            if e["spec_pairs"]:
                for k, v in list(e["spec_pairs"].items())[:6]:
                    print(f"     {k} = {v[:80]}")
            out.append(e)
            # Random sleep between tasks
            time.sleep(random.uniform(8, 16))
    (ROOT / "_ali_round2c.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\nWROTE _ali_round2c.json")


if __name__ == "__main__":
    main()
