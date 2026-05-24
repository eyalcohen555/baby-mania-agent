"""Re-verify with broader hash regex (any 32-hex token) + image loading on."""
import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
RAW = json.loads((ROOT / "_shopify_raw.json").read_text(encoding="utf-8"))

CANDIDATES = {
    9689589383481: ["1005005317212200"],
    9690182385977: ["1005008494074992", "1005004836875552", "1005006916205033",
                    "1005006135082630", "1005006136386727", "1005006127425938"],
    9690182418745: ["1005006863845547"],
    9690182451513: ["1005005188539088"],
    9690247627065: ["1005004447487327", "1005003774227741"],
    9690247659833: ["1005007059750853", "1005007479852919", "1005001779108331",
                    "1005003160035434", "1005005989236974"],
}

# Match any 32-hex hash that might appear in an alicdn URL
HASH_BROAD = re.compile(r"([0-9a-f]{32})")
HASH_SH_PATTERN = re.compile(r"/S([0-9a-f]{32})[A-Za-z0-9]?\.")
# AliExpress URLs frequently look like /kf/<id>.<ext> where id is one of:
#   S<32hex><1char>   (newer)
#   H<id>             (older)
#   <number/letter mix>

SAFETY_TERMS = ["handmade", "full silicone", "medical grade", "safety certified",
                "CE ", "EN71", "magnetic pacifier", "therapy",
                "anxiety", "dementia", "bath safe", "waterproof"]


def shopify_hashes(product):
    out = set()
    for img in product.get("images", []):
        for m in HASH_SH_PATTERN.finditer(img.get("src", "")):
            out.add(m.group(1))
    return out


def page_hashes(html):
    """Extract every 32-hex hash that's part of an alicdn-style image filename."""
    found = set()
    for m in re.finditer(r"alicdn\.com/[^\"'>\s]+", html):
        seg = m.group(0)
        for h in HASH_BROAD.findall(seg):
            found.add(h)
    # Also look at any S<32hex> in HTML (covers JSON embeds)
    for m in re.finditer(r"S([0-9a-f]{32})", html):
        found.add(m.group(1))
    return found


def extract_specs(html):
    pairs = {}
    for m in re.finditer(
        r'"attrName"\s*:\s*"([^"]{1,80})"\s*,\s*"attrValue"\s*:\s*"([^"]{1,200})"',
        html,
    ):
        pairs[m.group(1).strip().lower()] = m.group(2).strip()
    for m in re.finditer(
        r'specification--title[^>]*>([^<]{1,80})<.*?specification--desc[^>]*>([^<]{1,200})<',
        html, re.IGNORECASE | re.DOTALL,
    ):
        k = re.sub(r"\s+", " ", m.group(1)).strip().lower()
        v = re.sub(r"\s+", " ", m.group(2)).strip()
        pairs.setdefault(k, v)

    def pick(*keys):
        for k in keys:
            for sp_k, sp_v in pairs.items():
                if k in sp_k:
                    return sp_v
        return "UNKNOWN"

    specs = {
        "raw_spec_pairs_count": len(pairs),
        "body_material": pick("material"),
        "body_type": pick("filling", "body type", "body "),
        "size": pick("size", "doll size", "height"),
        "weight": pick("weight"),
        "hair_type": pick("hair", "hairstyle"),
        "eye_type": pick("eye color", "eyes", "eye "),
        "gender_option": pick("gender", "sex"),
        "age_recommendation": pick("age range", "age", "recommend age"),
        "clothes_included": pick("clothes", "dress"),
        "washable": pick("washable", "waterproof"),
        "brand": pick("brand name", "brand"),
        "model_number": pick("model number"),
        "feature": pick("feature"),
        "theme": pick("theme"),
    }
    title_m = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
    specs["ali_title"] = title_m.group(1).strip() if title_m else "UNKNOWN"
    return specs, pairs


def safety_flags(html):
    low = html.lower()
    return sorted({t.strip() for t in SAFETY_TERMS if t.lower() in low})


def fetch(page, iid):
    url = f"https://www.aliexpress.com/item/{iid}.html"
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(5)
        for _ in range(4):
            page.evaluate("window.scrollBy(0, 1200)")
            time.sleep(0.5)
        time.sleep(1)
        return page.content(), None
    except Exception as e:
        return "", str(e)


def main():
    results = {"per_product": []}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 1280, "height": 900},
        )
        page = ctx.new_page()

        for prod in RAW["products"]:
            pid = prod["id"]
            sh = shopify_hashes(prod)
            print(f"\n=== PID {pid}  (shopify hashes: {len(sh)}) ===")
            print(f"  {sorted(sh)}")
            entry = {
                "shopify_pid": pid,
                "shopify_handle": prod["handle"],
                "shopify_hashes": sorted(sh),
                "matched_item": None,
                "identity_confirmed": False,
                "shared_hashes": [],
                "ali_specs": None,
                "ali_spec_pairs": {},
                "safety_flags": [],
                "tested": [],
                "errors": [],
            }
            best_candidate_html = None
            best_candidate_id = None

            for iid in CANDIDATES.get(pid, []):
                html, err = fetch(page, iid)
                if err or not html:
                    entry["errors"].append(f"{iid}: {err}")
                    entry["tested"].append({"id": iid, "ok": False})
                    continue
                ph = page_hashes(html)
                shared = sh & ph
                entry["tested"].append({"id": iid, "ok": True,
                                        "ph": len(ph), "shared": len(shared)})
                print(f"   {iid}: ali_hashes={len(ph)} shared={len(shared)}")
                if best_candidate_html is None:
                    best_candidate_html = html
                    best_candidate_id = iid
                if shared:
                    entry["matched_item"] = iid
                    entry["identity_confirmed"] = True
                    entry["shared_hashes"] = sorted(shared)[:8]
                    specs, pairs = extract_specs(html)
                    entry["ali_specs"] = specs
                    entry["ali_spec_pairs"] = pairs
                    entry["safety_flags"] = safety_flags(html)
                    break
                time.sleep(1.5)

            if not entry["identity_confirmed"] and best_candidate_html:
                specs, pairs = extract_specs(best_candidate_html)
                entry["matched_item"] = best_candidate_id
                entry["ali_specs"] = specs
                entry["ali_spec_pairs"] = pairs
                entry["safety_flags"] = safety_flags(best_candidate_html)
                entry["note"] = "tentative – no image hash match"

            results["per_product"].append(entry)

        browser.close()

    (ROOT / "_ali_verified2.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\nWROTE _ali_verified2.json")


if __name__ == "__main__":
    main()
