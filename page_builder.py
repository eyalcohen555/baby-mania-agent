"""Assembles product data into an HTML product page using Jinja2 templates."""

import os
from jinja2 import Environment, FileSystemLoader
from config.settings import SIZE_CHART

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def build_size_table(available_sizes):
    """Build size chart rows for the given sizes."""
    rows = []
    for size_key in available_sizes:
        if size_key in SIZE_CHART:
            info = SIZE_CHART[size_key]
            rows.append({
                "size": size_key,
                "age": info["age"],
                "height": info["height_cm"],
                "weight": info["weight_kg"],
            })
    return rows


def build_product_page(product, description, benefits, image_url=None):
    """Render the full product page HTML.

    Args:
        product: Shopify product dict.
        description: Hebrew product description from Gemini.
        benefits: Hebrew benefits text from Gemini.
        image_url: Optional generated image URL.

    Returns:
        Rendered HTML string.
    """
    # Extract available sizes from Shopify variants
    available_sizes = []
    for variant in product.get("variants", []):
        opt = variant.get("option1", "")
        if opt and opt not in available_sizes:
            available_sizes.append(opt)

    size_rows = build_size_table(available_sizes)

    # Use existing product image if no generated one
    if not image_url and product.get("images"):
        image_url = product["images"][0]["src"]

    template = env.get_template("product_page.html")
    return template.render(
        title=product.get("title", ""),
        description=description,
        benefits=benefits,
        image_url=image_url,
        price=product.get("variants", [{}])[0].get("price", ""),
        sizes=size_rows,
        variants=product.get("variants", []),
    )
