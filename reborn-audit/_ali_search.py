"""AliExpress identity search for 6 reborn products.

Strategy: keyword search via Playwright -> capture candidate item IDs ->
load each candidate page -> compare image hash filenames to Shopify image
filenames. A match = confirmed identity. Extract specs only from confirmed.

NO writes anywhere. NO secrets in output. Saves to _ali_candidates.json.
"""
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote_plus

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
RAW = json.loads((ROOT / "_shopify_raw.json").read_text(encoding="utf-8"))

# Distinctive English keywords per product, derived from Shopify handle.
QUERIES = {
    9689589383481: "19 inches levi reborn baby vinyl 49cm finished hair painted",
    9690182385977: "BZDoll 55cm 22 inch reborn full silicone princess toddler",
    9690182418745: "BZDoll 60cm 24 inch soft silicone reborn 3d painting vascular vein handmade",
    9690182451513: "50cm loulou reborn silicone vinyl cloth body handmade",
    9690247627065: "NPK 19inch Levi reborn baby awake 3d skin visible veins",
    9690247659833: "50cm full vinyl maddie reborn waterproof visible veins 3d skin",
}

# Known confirmed identity (from prior user research)
KNOWN = {
    9689589383481: {
        "ali_item_id": "1005005317212200",
        "size_ali": "46cm",
        "identity_confirmed": True,
        "source": "user-confirmed via image hash (prior)",
    },
}

HASH_RE = re.compile(r"S([0-9a-f]{32})")  # AliExpress CDN hash pattern


def shopify_hashes(product):
    hashes = set()
    for img in product.get("images", []):
        m = HASH_RE.search(img.get("src", ""))
        if m:
            hashes.add(m.group(1))
    return hashes


ITEM_RE = re.compile(r"/item/(\d{10,16})\.html")


def search_ali(page, query, max_items=10):
    """Search AliExpress and return list of candidate item IDs from result page."""
    url = f"https://www.aliexpress.com/wholesale-product.html?SearchText={quote_plus(query)}"
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        # Try alt URL if first didn't show results
        html = page.content()
    except Exception as e:
        return [], f"goto error: {e}"

    ids = []
    seen = set()
    for m in ITEM_RE.finditer(html):
        iid = m.group(1)
        if iid not in seen:
            seen.add(iid)
            ids.append(iid)
        if len(ids) >= max_items:
            break
    return ids, None


def fetch_item_hashes(page, item_id):
    """Load an AliExpress item page and return (image_hashes, raw_html_excerpt)."""
    url = f"https://www.aliexpress.com/item/{item_id}.html"
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        html = page.content()
    except Exception as e:
        return set(), f"goto error: {e}", ""
    hashes = set(HASH_RE.findall(html))
    return hashes, None, html[:300]


def main():
    out = {"per_product": []}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            viewport={"width": 1280, "height": 900},
        )
        page = ctx.new_page()

        for prod in RAW["products"]:
            pid = prod["id"]
            entry = {
                "shopify_pid": pid,
                "handle": prod["handle"],
                "shopify_image_hashes": sorted(shopify_hashes(prod)),
                "query": QUERIES.get(pid, ""),
                "candidates": [],
                "matched_ali_item": None,
                "matched_via_hash": None,
                "identity_confirmed": False,
                "known_override": KNOWN.get(pid),
                "errors": [],
            }
            print(f"\n=== PID {pid} ===")
            print(f"shopify hashes: {entry['shopify_image_hashes']}")

            # If known, skip search and accept
            if KNOWN.get(pid):
                entry["matched_ali_item"] = KNOWN[pid]["ali_item_id"]
                entry["identity_confirmed"] = KNOWN[pid]["identity_confirmed"]
                entry["matched_via_hash"] = "user-confirmed prior"
                out["per_product"].append(entry)
                print(f"  -> KNOWN: {KNOWN[pid]['ali_item_id']}")
                continue

            # Search
            ids, err = search_ali(page, entry["query"])
            if err:
                entry["errors"].append(err)
            entry["candidates"] = ids[:8]
            print(f"  candidates: {ids[:8]}")
            if not ids:
                out["per_product"].append(entry)
                continue

            # Probe candidates for image hash match
            sh_hashes = set(entry["shopify_image_hashes"])
            for iid in ids[:8]:
                hashes, ferr, _ = fetch_item_hashes(page, iid)
                if ferr:
                    entry["errors"].append(f"{iid}: {ferr}")
                    continue
                common = hashes & sh_hashes
                print(f"    item {iid}: ali_hashes={len(hashes)} common_with_shopify={len(common)}")
                if common:
                    entry["matched_ali_item"] = iid
                    entry["matched_via_hash"] = sorted(common)[:3]
                    entry["identity_confirmed"] = True
                    break
                time.sleep(1)

            out["per_product"].append(entry)

        browser.close()

    (ROOT / "_ali_candidates.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nWROTE {ROOT / '_ali_candidates.json'}")


if __name__ == "__main__":
    main()
