"""Verify candidate AliExpress items against Shopify image hashes,
and extract spec table for confirmed items.
"""
import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
RAW = json.loads((ROOT / "_shopify_raw.json").read_text(encoding="utf-8"))

# Candidate item IDs per Shopify PID (from WebSearch results, ranked).
CANDIDATES = {
    9689589383481: ["1005005317212200"],  # KNOWN
    9690182385977: ["1005008494074992", "1005004836875552", "1005006916205033", "32962797746"],
    9690182418745: ["1005006863845547", "1005006127449633", "1005005236155364"],
    9690182451513: ["1005005188539088", "1005010072119208", "1005005306273352"],
    9690247627065: ["1005004447487327", "1005007123488523"],
    9690247659833: ["1005007059750853", "1005007479852919", "1005001779108331", "1005003160035434"],
}

HASH_RE = re.compile(r"S([0-9a-f]{32})")

SAFETY_TERMS = [
    "handmade", "full silicone", "medical grade", "safety certified",
    "CE ", "EN71", "magnetic pacifier", "therapy",
    "anxiety", "dementia", "bath safe", "waterproof",
]


def shopify_hashes(product):
    return {HASH_RE.search(img.get("src", "")).group(1)
            for img in product.get("images", [])
            if HASH_RE.search(img.get("src", ""))}


def extract_text_value(html, label_patterns):
    """Try several regex patterns to find label:value in spec table."""
    for pat in label_patterns:
        m = re.search(pat, html, re.IGNORECASE)
        if m:
            v = m.group(1)
            v = re.sub(r"<[^>]+>", " ", v)
            v = re.sub(r"\s+", " ", v).strip()
            if v and len(v) < 200:
                return v
    return "UNKNOWN"


def extract_specs_from_html(html):
    """Extract spec fields from AliExpress product HTML."""
    specs = {}

    # AliExpress spec rows commonly look like:
    # <div class="specification--prop"><div class="specification--title">Brand Name</div><div class="specification--desc">XXX</div></div>
    # or in JSON __NEXT_DATA__ blob. Use generic key→value extraction.
    spec_pairs = {}
    for m in re.finditer(
        r'"attrName"\s*:\s*"([^"]{1,80})"\s*,\s*"attrValue"\s*:\s*"([^"]{1,200})"',
        html,
    ):
        spec_pairs[m.group(1).strip().lower()] = m.group(2).strip()
    # Fallback HTML pattern
    for m in re.finditer(
        r'specification--title[^>]*>([^<]{1,80})<.*?specification--desc[^>]*>([^<]{1,200})<',
        html,
        re.IGNORECASE | re.DOTALL,
    ):
        k = re.sub(r"\s+", " ", m.group(1)).strip().lower()
        v = re.sub(r"\s+", " ", m.group(2)).strip()
        spec_pairs.setdefault(k, v)

    def pick(*keys):
        for k in keys:
            for sp_k, sp_v in spec_pairs.items():
                if k in sp_k:
                    return sp_v
        return "UNKNOWN"

    specs["raw_spec_pairs_count"] = len(spec_pairs)
    specs["body_material"] = pick("material", "body material")
    specs["body_type"] = pick("filling", "body type", "body")
    specs["size"] = pick("size", "doll size", "height")
    specs["weight"] = pick("weight", "gross weight", "item weight")
    specs["hair_type"] = pick("hair", "hairstyle")
    specs["eye_type"] = pick("eye color", "eyes", "eye")
    specs["gender_option"] = pick("gender", "sex")
    specs["age_recommendation"] = pick("age range", "age", "recommend age")
    specs["clothes_included"] = pick("clothes", "dress")
    specs["washable"] = pick("washable", "waterproof")
    specs["brand"] = pick("brand name", "brand")
    specs["model_number"] = pick("model number")

    # Title
    title_m = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
    specs["ali_title"] = title_m.group(1).strip() if title_m else "UNKNOWN"

    return specs, spec_pairs


def find_safety_flags(html):
    flags = []
    low = html.lower()
    for term in SAFETY_TERMS:
        if term.lower() in low:
            flags.append(term.strip())
    return sorted(set(flags))


def fetch_page(page, item_id):
    url = f"https://www.aliexpress.com/item/{item_id}.html"
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(4)  # let SPA hydrate
        # Scroll a bit to trigger lazy content
        for _ in range(3):
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(0.5)
        return page.content(), None
    except Exception as e:
        return "", str(e)


def main():
    results = {"per_product": []}
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
        # Block heavy resources to speed up & reduce captcha risk
        page.route("**/*.{png,jpg,jpeg,gif,webp,mp4,woff2}",
                   lambda r: r.abort())

        for prod in RAW["products"]:
            pid = prod["id"]
            sh_hashes = shopify_hashes(prod)
            entry = {
                "shopify_pid": pid,
                "shopify_handle": prod["handle"],
                "shopify_hashes_count": len(sh_hashes),
                "matched_item": None,
                "identity_confirmed": False,
                "shared_hashes": [],
                "ali_specs": None,
                "ali_spec_pairs": {},
                "safety_flags": [],
                "errors": [],
                "tested_candidates": [],
            }
            print(f"\n=== PID {pid} ===")

            for iid in CANDIDATES.get(pid, []):
                print(f"  trying {iid} ...")
                html, err = fetch_page(page, iid)
                if err or not html:
                    entry["errors"].append(f"{iid}: {err}")
                    entry["tested_candidates"].append({"id": iid, "ok": False, "shared": 0})
                    continue
                ali_hashes = set(HASH_RE.findall(html))
                shared = sh_hashes & ali_hashes
                print(f"     ali_hashes={len(ali_hashes)} shared={len(shared)}")
                entry["tested_candidates"].append(
                    {"id": iid, "ok": True, "ali_hashes": len(ali_hashes), "shared": len(shared)}
                )
                if shared:
                    entry["matched_item"] = iid
                    entry["identity_confirmed"] = True
                    entry["shared_hashes"] = sorted(shared)[:5]
                    specs, pairs = extract_specs_from_html(html)
                    entry["ali_specs"] = specs
                    entry["ali_spec_pairs"] = pairs
                    entry["safety_flags"] = find_safety_flags(html)
                    break
                time.sleep(1.5)

            # If nothing matched but candidates loaded, still capture the top
            # candidate's specs as "tentative" for inspection.
            if not entry["identity_confirmed"] and entry["tested_candidates"]:
                top_ok = next((c for c in entry["tested_candidates"] if c["ok"]), None)
                if top_ok:
                    iid = top_ok["id"]
                    html, _ = fetch_page(page, iid)
                    if html:
                        specs, pairs = extract_specs_from_html(html)
                        entry["matched_item"] = iid
                        entry["ali_specs"] = specs
                        entry["ali_spec_pairs"] = pairs
                        entry["safety_flags"] = find_safety_flags(html)
                        entry["identity_confirmed"] = False
                        entry["note"] = "tentative — no image-hash match; treat as unverified"

            results["per_product"].append(entry)

        browser.close()

    (ROOT / "_ali_verified.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nWROTE _ali_verified.json")


if __name__ == "__main__":
    main()
