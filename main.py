"""Baby Mania Agent — Shopify product page generator.

Fetches products from Shopify, generates Hebrew descriptions and images
via Google Gemini, assembles a styled HTML product page, and pushes
the result back to Shopify.
"""

import argparse
import base64
import os
import sys

# Ensure Unicode output works on Windows consoles (cp1255, etc.)
if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from shopify_client import get_products, get_product, update_product
from gemini_client import (
    generate_product_description,
    generate_product_benefits,
    generate_product_image,
)
from page_builder import build_product_page


def process_product(product, generate_image=False, dry_run=False):
    """Generate a full product page for a single Shopify product."""
    title = product["title"]
    product_type = product.get("product_type", "בגד תינוק")
    tags = product.get("tags", "").split(", ") if product.get("tags") else []
    product_id = product["id"]

    print(f"\n{'='*60}")
    print(f"Processing: {title} (ID: {product_id})")
    print(f"{'='*60}")

    # --- Step 1: Generate Hebrew description ---
    print("  [1/4] Generating Hebrew description...")
    description = generate_product_description(title, product_type, tags)
    print(f"  ✓ Description generated ({len(description)} chars)")

    # --- Step 2: Generate benefits ---
    print("  [2/4] Generating product benefits...")
    benefits = generate_product_benefits(title, product_type)
    print(f"  ✓ Benefits generated")

    # --- Step 3: Generate image (optional) ---
    image_url = None
    if generate_image:
        print("  [3/4] Generating product image...")
        image_data, mime_type = generate_product_image(title, product_type)
        if image_data:
            # Save locally for preview
            os.makedirs("output", exist_ok=True)
            ext = "png" if "png" in (mime_type or "") else "jpg"
            image_path = f"output/{product_id}.{ext}"
            with open(image_path, "wb") as f:
                f.write(image_data)
            print(f"  ✓ Image saved to {image_path}")
        else:
            print("  ⚠ Image generation returned no image")
    else:
        print("  [3/4] Skipping image generation (use --images to enable)")

    # --- Step 4: Assemble HTML page ---
    print("  [4/4] Building product page HTML...")
    html = build_product_page(product, description, benefits, image_url)

    # Save HTML preview locally
    os.makedirs("output", exist_ok=True)
    preview_path = f"output/{product_id}.html"
    with open(preview_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ Preview saved to {preview_path}")

    # --- Push to Shopify ---
    if dry_run:
        print("  ⏭ Dry run — skipping Shopify update")
    else:
        print("  Updating Shopify product...")
        update_product(product_id, html)
        print("  ✓ Shopify product updated!")

    return html


def main():
    parser = argparse.ArgumentParser(description="Baby Mania — Shopify Product Page Generator")
    parser.add_argument("--product-id", type=int, help="Process a single product by ID")
    parser.add_argument("--all", action="store_true", help="Process all products")
    parser.add_argument("--limit", type=int, default=10, help="Max products to fetch (default: 10)")
    parser.add_argument("--images", action="store_true", help="Generate product images via Gemini")
    parser.add_argument("--dry-run", action="store_true", help="Generate pages without updating Shopify")
    args = parser.parse_args()

    if not args.product_id and not args.all:
        parser.print_help()
        print("\nExample usage:")
        print("  python main.py --product-id 123456789 --dry-run")
        print("  python main.py --all --limit 5 --dry-run")
        print("  python main.py --all --images")
        sys.exit(1)

    if args.product_id:
        product = get_product(args.product_id)
        process_product(product, generate_image=args.images, dry_run=args.dry_run)
    else:
        products = get_products(limit=args.limit)
        print(f"Fetched {len(products)} products from Shopify")
        for product in products:
            process_product(product, generate_image=args.images, dry_run=args.dry_run)

    print("\n✓ Done!")


if __name__ == "__main__":
    main()
