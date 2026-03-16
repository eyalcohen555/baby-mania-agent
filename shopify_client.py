"""Shopify API client using client_credentials OAuth flow.

Tokens are short-lived (~24h). This module handles automatic token
acquisition and renewal before each API call.
"""

import time
import requests
from config.settings import (
    SHOPIFY_SHOP_URL,
    SHOPIFY_CLIENT_ID,
    SHOPIFY_CLIENT_SECRET,
    SHOPIFY_API_VERSION,
)

BASE_URL = f"https://{SHOPIFY_SHOP_URL}/admin/api/{SHOPIFY_API_VERSION}"
TOKEN_URL = f"https://{SHOPIFY_SHOP_URL}/admin/oauth/access_token"

# Module-level token cache
_token_cache = {"access_token": None, "expires_at": 0}


def _get_access_token():
    """Return a valid access token, requesting a new one if expired."""
    # Re-use cached token if still valid (with 5-min safety margin)
    if _token_cache["access_token"] and time.time() < _token_cache["expires_at"] - 300:
        return _token_cache["access_token"]

    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": SHOPIFY_CLIENT_ID,
            "client_secret": SHOPIFY_CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    resp.raise_for_status()
    data = resp.json()

    _token_cache["access_token"] = data["access_token"]
    _token_cache["expires_at"] = time.time() + data.get("expires_in", 86399)

    return _token_cache["access_token"]


def _headers():
    """Build request headers with a fresh access token."""
    return {
        "X-Shopify-Access-Token": _get_access_token(),
        "Content-Type": "application/json",
    }


def get_products(limit=50):
    """Fetch products from Shopify."""
    resp = requests.get(f"{BASE_URL}/products.json", headers=_headers(), params={"limit": limit})
    resp.raise_for_status()
    return resp.json()["products"]


def get_product(product_id):
    """Fetch a single product by ID."""
    resp = requests.get(f"{BASE_URL}/products/{product_id}.json", headers=_headers())
    resp.raise_for_status()
    return resp.json()["product"]


def update_product(product_id, body_html):
    """Update a product's HTML description in Shopify."""
    payload = {"product": {"id": product_id, "body_html": body_html}}
    resp = requests.put(f"{BASE_URL}/products/{product_id}.json", headers=_headers(), json=payload)
    resp.raise_for_status()
    return resp.json()["product"]


# ─── Blog Articles ────────────────────────────────────────────────────────────

def get_blog_articles(blog_id, limit=250):
    """Fetch all articles from a Shopify blog (paginated)."""
    articles = []
    params = {"limit": limit}
    url = f"{BASE_URL}/blogs/{blog_id}/articles.json"

    while url:
        resp = requests.get(url, headers=_headers(), params=params)
        resp.raise_for_status()
        batch = resp.json().get("articles", [])
        articles.extend(batch)

        # Follow Shopify pagination via Link header
        link_header = resp.headers.get("Link", "")
        next_url = None
        for part in link_header.split(","):
            part = part.strip()
            if 'rel="next"' in part:
                next_url = part.split(";")[0].strip().strip("<>")
                break
        url = next_url
        params = {}  # page_info is embedded in next_url

    return articles


def get_blog_article(blog_id, article_id):
    """Fetch a single blog article."""
    resp = requests.get(
        f"{BASE_URL}/blogs/{blog_id}/articles/{article_id}.json",
        headers=_headers(),
    )
    resp.raise_for_status()
    return resp.json()["article"]


def update_blog_article(blog_id, article_id, body_html):
    """Update a blog article's HTML body in Shopify."""
    payload = {"article": {"id": article_id, "body_html": body_html}}
    resp = requests.put(
        f"{BASE_URL}/blogs/{blog_id}/articles/{article_id}.json",
        headers=_headers(),
        json=payload,
    )
    resp.raise_for_status()
    return resp.json()["article"]
