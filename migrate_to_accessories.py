"""
Step 5: Migrate non-shoe products from template=shoes to template=accessories
- Reads: output/shoe_classification_report.json
- Updates template_suffix from "shoes" to "accessories" for:
  - products classified as clothing (ביגוד)
  - products classified as accessories/equipment (אביזר/ציוד)
  - products that could not be classified (לא ניתן לסווג)
- Real shoes are untouched.
"""
import sys
import json
import time
import requests

# Fix encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config.settings import SHOPIFY_SHOP_URL, SHOPIFY_API_VERSION
from shopify_client import _headers

BASE_URL = f"https://{SHOPIFY_SHOP_URL}/admin/api/{SHOPIFY_API_VERSION}"
BATCH_SIZE = 10
DELAY_BETWEEN_CALLS = 0.5   # seconds between individual API calls
DELAY_BETWEEN_BATCHES = 2   # seconds between batches

CLASSIFICATIONS_TO_MOVE = ["ביגוד", "אביזר", "לא ניתן לסווג"]


def should_move(classification: str) -> bool:
    return any(k in classification for k in CLASSIFICATIONS_TO_MOVE)


def update_template_suffix(product_id: int, new_suffix: str) -> dict:
    payload = {"product": {"id": product_id, "template_suffix": new_suffix}}
    resp = requests.put(
        f"{BASE_URL}/products/{product_id}.json",
        headers=_headers(),
        json=payload,
    )
    resp.raise_for_status()
    return resp.json()["product"]


def main():
    # 1. Load classification report
    with open("output/shoe_classification_report.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2. Filter products to migrate
    to_move = [p for p in data if should_move(p["classification"])]
    total = len(to_move)
    print(f"=== Migrate to accessories ===")
    print(f"Total records in report: {len(data)}")
    print(f"Products to migrate: {total}")
    print(f"Batch size: {BATCH_SIZE}")
    print()

    # 3. Process in batches of 10
    success_ids = []
    failed = []

    for batch_start in range(0, total, BATCH_SIZE):
        batch = to_move[batch_start: batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1
        batch_success = 0

        print(f"--- Batch {batch_num} ({batch_start + 1}–{batch_start + len(batch)}) ---")

        for product in batch:
            pid = product["id"]
            title_short = product["title"][:55]
            try:
                update_template_suffix(pid, "accessories")
                success_ids.append(pid)
                batch_success += 1
                print(f"  OK  {pid}  {title_short}")
            except requests.HTTPError as e:
                status_code = e.response.status_code if e.response is not None else "?"
                failed.append({"id": pid, "title": product["title"], "error": str(e), "status": status_code})
                print(f"  ERR {pid}  HTTP {status_code}  {title_short}")
            except Exception as e:
                failed.append({"id": pid, "title": product["title"], "error": str(e), "status": "?"})
                print(f"  ERR {pid}  {type(e).__name__}: {e}  {title_short}")

            time.sleep(DELAY_BETWEEN_CALLS)

        print(f"  Batch {batch_num} done: {batch_success}/{len(batch)} succeeded")
        print()

        if batch_start + BATCH_SIZE < total:
            time.sleep(DELAY_BETWEEN_BATCHES)

    # 4. Save failed list if any
    if failed:
        with open("output/accessories_migration_failed.json", "w", encoding="utf-8") as f:
            json.dump(failed, f, ensure_ascii=False, indent=2)
        print(f"Failed list saved to output/accessories_migration_failed.json")

    # 5. Summary
    print("=" * 50)
    print("MIGRATION SUMMARY")
    print("=" * 50)
    print(f"Products to migrate:     {total}")
    print(f"Migrated successfully:   {len(success_ids)}")
    print(f"Failed:                  {len(failed)}")
    print(f"Real shoes (untouched):  {len(data) - total}")

    if failed:
        print()
        print("Failed products:")
        for f_item in failed:
            print(f"  id={f_item['id']}  HTTP {f_item['status']}  {f_item['title'][:60]}")


if __name__ == "__main__":
    main()
