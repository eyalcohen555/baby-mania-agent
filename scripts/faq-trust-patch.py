#!/usr/bin/env python3
"""
FAQ Trust Patch — BabyMania
Prepends "מי אנחנו?" and appends "מהם זמני המשלוח?" to existing clothing
product FAQ metafields without destroying product-specific questions.

Usage:
  python faq-trust-patch.py [--dry-run] PRODUCT_ID [PRODUCT_ID ...]

Flags:
  --dry-run   Print what would be written without touching Shopify
"""
import io
import os
import sys
import json
import argparse
from pathlib import Path

import requests
from dotenv import load_dotenv

# ── Encoding ──────────────────────────────────────────────────────────────────
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── Env ───────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")
_tok = Path.home() / "Desktop/shopify-token/.env"
if _tok.exists():
    load_dotenv(_tok, override=True)

SHOPIFY_HOST  = os.getenv("SHOPIFY_SHOP_URL", "a2756c-c0.myshopify.com")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
NAMESPACE     = "baby_mania"

# ── Trust questions ───────────────────────────────────────────────────────────
TRUST_Q1 = {
    "question": "מי אנחנו?",
    "answer": (
        "בייבי מניה היא מותג ישראלי מוביל לביגוד תינוקות פרימיום. "
        "אנחנו מציעים בגדים איכותיים, נוחים ואופנתיים לתינוקות וילדים "
        "עד גיל 3, עם שירות לקוחות אישי וחוויית קנייה מהנה."
    ),
}
TRUST_Q2 = {
    "question": "מהם זמני המשלוח?",
    "answer": (
        "אנחנו שולחים עם שירות משלוח מהיר — הזמנות מגיעות תוך 3-5 ימי עסקים. "
        "משלוח חינם בהזמנות מעל 199 ₪. ניתן לעקוב אחר ההזמנה עם קוד המעקב "
        "שנשלח ב-SMS לאחר השליחה."
    ),
}

# ── Shopify helpers ───────────────────────────────────────────────────────────
def _headers():
    return {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json",
    }

def get_faq_metafield(product_id: str) -> tuple[list, int | None]:
    """
    Returns (faq_list, metafield_id_or_None).
    faq_list is [] if no metafield exists yet.
    """
    url = (
        f"https://{SHOPIFY_HOST}/admin/api/2024-10/"
        f"products/{product_id}/metafields.json"
        f"?namespace={NAMESPACE}&key=faq&limit=5"
    )
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    mfs = r.json().get("metafields", [])
    if not mfs:
        return [], None
    mf = mfs[0]
    raw = mf["value"]
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
    except json.JSONDecodeError:
        data = []
    return data, mf["id"]


def write_faq_metafield(product_id: str, faq: list, metafield_id: int | None) -> None:
    """Upsert the faq metafield (PUT if exists, POST if new)."""
    payload = {
        "metafield": {
            "namespace": NAMESPACE,
            "key":       "faq",
            "value":     json.dumps(faq, ensure_ascii=False),
            "type":      "json",
        }
    }
    if metafield_id:
        url = (
            f"https://{SHOPIFY_HOST}/admin/api/2024-10/"
            f"products/{product_id}/metafields/{metafield_id}.json"
        )
        r = requests.put(url, headers=_headers(), json=payload)
    else:
        url = (
            f"https://{SHOPIFY_HOST}/admin/api/2024-10/"
            f"products/{product_id}/metafields.json"
        )
        r = requests.post(url, headers=_headers(), json=payload)
    r.raise_for_status()


# ── Patch logic ───────────────────────────────────────────────────────────────
TRUST_DEDUP_SUBSTRINGS = ["מי אנחנו", "זמני המשלוח"]

def is_trust_question(q: dict) -> bool:
    text = q.get("question", "")
    return any(s in text for s in TRUST_DEDUP_SUBSTRINGS)


def patch_faq(existing: list) -> list:
    """
    Returns new FAQ list:
      [TRUST_Q1] + [middle product-specific questions] + [TRUST_Q2]
    Deduplicates any existing trust questions.
    """
    middle = [q for q in existing if not is_trust_question(q)]
    return [TRUST_Q1] + middle + [TRUST_Q2]


# ── Main ──────────────────────────────────────────────────────────────────────
def process_product(product_id: str, dry_run: bool) -> None:
    print(f"\n{'='*60}")
    print(f"Product ID: {product_id}")

    existing, mf_id = get_faq_metafield(product_id)

    print(f"  Current FAQ ({len(existing)} questions):")
    for i, q in enumerate(existing, 1):
        print(f"    {i}. {q.get('question', '')}")

    patched = patch_faq(existing)

    print(f"  Patched FAQ ({len(patched)} questions):")
    for i, q in enumerate(patched, 1):
        marker = " [TRUST]" if is_trust_question(q) else ""
        print(f"    {i}. {q.get('question', '')}{marker}")

    if dry_run:
        print("  [DRY RUN] — no changes written to Shopify")
    else:
        write_faq_metafield(product_id, patched, mf_id)
        action = "updated" if mf_id else "created"
        print(f"  OK — metafield {action} (id={mf_id})")


def main():
    parser = argparse.ArgumentParser(description="FAQ Trust Patch for BabyMania")
    parser.add_argument("product_ids", nargs="+", help="Shopify numeric product IDs")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    args = parser.parse_args()

    if not SHOPIFY_TOKEN:
        print("ERROR: SHOPIFY_ACCESS_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    for pid in args.product_ids:
        try:
            process_product(pid.strip(), args.dry_run)
        except requests.HTTPError as e:
            print(f"  HTTP ERROR for {pid}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"  ERROR for {pid}: {e}", file=sys.stderr)

    print("\nDone.")


if __name__ == "__main__":
    main()
