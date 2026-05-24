"""Read-only fetch of 6 reborn products from Shopify.

No writes. No secrets in output. Uses the project's shopify_client.
"""
import json
import sys
from pathlib import Path

# Ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from shopify_client import get_product  # noqa: E402

PIDS = [
    9689589383481,
    9690182385977,
    9690182418745,
    9690182451513,
    9690247627065,
    9690247659833,
]

OUT = ROOT / "reborn-audit" / "_shopify_raw.json"


def slim_product(p):
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
                "id": v.get("id"),
                "sku": v.get("sku"),
                "title": v.get("title"),
                "option1": v.get("option1"),
                "option2": v.get("option2"),
                "option3": v.get("option3"),
                "price": v.get("price"),
                "inventory_quantity": v.get("inventory_quantity"),
            }
            for v in (p.get("variants") or [])
        ],
        "options": p.get("options"),
        "images": [
            {
                "id": img.get("id"),
                "src": img.get("src"),
                "alt": img.get("alt"),
                "position": img.get("position"),
                "width": img.get("width"),
                "height": img.get("height"),
            }
            for img in (p.get("images") or [])
        ],
        "image_main": (p.get("image") or {}).get("src"),
    }


def main():
    results = []
    errors = []
    for pid in PIDS:
        try:
            p = get_product(pid)
            results.append(slim_product(p))
            print(f"OK  {pid} :: {p.get('title')}")
        except Exception as e:
            errors.append({"pid": pid, "error": str(e)[:200]})
            print(f"ERR {pid} :: {e}")
    OUT.write_text(
        json.dumps({"products": results, "errors": errors}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nWROTE {OUT}")


if __name__ == "__main__":
    main()
