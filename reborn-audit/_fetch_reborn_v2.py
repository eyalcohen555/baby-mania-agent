"""Read-only fetch of 10 reborn products from Shopify (round 2)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from shopify_client import get_product  # noqa: E402

# Order matches user's task list (1..10)
PIDS = [
    9690182385977,   # 1
    10190523040057,  # 2  (new)
    10190523072825,  # 3  (new)
    10190523007289,  # 4  (new)
    10190522777913,  # 5  (new, shares Ali link with #6)
    10190522810681,  # 6  (new, shares Ali link with #5)
    9690247627065,   # 7
    9690182451513,   # 8
    9690182418745,   # 9
    9689589383481,   # 10
]

OUT = ROOT / "reborn-audit" / "_shopify_raw_v2.json"


def slim(p):
    return {
        "id": p.get("id"),
        "title": p.get("title"),
        "handle": p.get("handle"),
        "vendor": p.get("vendor"),
        "product_type": p.get("product_type"),
        "tags": p.get("tags"),
        "status": p.get("status"),
        "variants": [
            {
                "id": v.get("id"), "sku": v.get("sku"), "title": v.get("title"),
                "option1": v.get("option1"), "option2": v.get("option2"),
                "option3": v.get("option3"), "price": v.get("price"),
                "inventory_quantity": v.get("inventory_quantity"),
            }
            for v in (p.get("variants") or [])
        ],
        "options": p.get("options"),
        "images": [
            {
                "id": i.get("id"), "src": i.get("src"), "alt": i.get("alt"),
                "position": i.get("position"),
                "width": i.get("width"), "height": i.get("height"),
            }
            for i in (p.get("images") or [])
        ],
        "image_main": (p.get("image") or {}).get("src"),
    }


def main():
    results = []
    errors = []
    for pid in PIDS:
        try:
            p = get_product(pid)
            results.append(slim(p))
            print(f"OK  {pid} :: variants={len(p.get('variants') or [])} images={len(p.get('images') or [])}")
        except Exception as e:
            errors.append({"pid": pid, "error": str(e)[:200]})
            print(f"ERR {pid} :: {e}")
    OUT.write_text(json.dumps({"products": results, "errors": errors},
                              ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWROTE {OUT}")


if __name__ == "__main__":
    main()
