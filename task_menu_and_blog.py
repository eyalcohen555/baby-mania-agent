"""
Tasks:
1. Add "בלוג" link to main menu via Shopify GraphQL Admin API
2. Fetch blog template from theme assets
"""

import sys
import json
import requests

# Bootstrap settings (loads .env credentials)
sys.path.insert(0, "C:/Projects/baby-mania-agent")
from config.settings import SHOPIFY_SHOP_URL, SHOPIFY_API_VERSION
from shopify_client import _get_access_token

THEME_ID = "183668179257"
GRAPHQL_URL = f"https://{SHOPIFY_SHOP_URL}/admin/api/{SHOPIFY_API_VERSION}/graphql.json"
REST_BASE = f"https://{SHOPIFY_SHOP_URL}/admin/api/{SHOPIFY_API_VERSION}"


def headers():
    return {
        "X-Shopify-Access-Token": _get_access_token(),
        "Content-Type": "application/json",
    }


# ─────────────────────────────────────────────────────────────────
# TASK 1 — Get main menu, then add "בלוג" link
# ─────────────────────────────────────────────────────────────────

def graphql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    resp = requests.post(GRAPHQL_URL, headers=headers(), json=payload)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {json.dumps(data['errors'], ensure_ascii=False)}")
    return data["data"]


# Step 1a: list all menus
LIST_MENUS_QUERY = """
query {
  menus(first: 20) {
    edges {
      node {
        id
        handle
        title
        items {
          id
          title
          url
          type
        }
      }
    }
  }
}
"""

print("=" * 60)
print("TASK 1 — Main Menu")
print("=" * 60)

data = graphql(LIST_MENUS_QUERY)
menus = data["menus"]["edges"]

print(f"\nנמצאו {len(menus)} תפריטים:")
for edge in menus:
    m = edge["node"]
    print(f"\n  handle: {m['handle']} | title: {m['title']} | id: {m['id']}")
    for item in m["items"]:
        print(f"    - {item['title']} → {item['url']} (type: {item['type']})")

# Find main menu
main_menu = None
for edge in menus:
    m = edge["node"]
    if m["handle"] in ("main-menu", "main_menu", "header", "main"):
        main_menu = m
        break

if not main_menu and menus:
    # fallback: first menu
    main_menu = menus[0]["node"]
    print(f"\n[!] לא נמצא 'main-menu' — משתמש ב: {main_menu['handle']}")

if not main_menu:
    print("[ERROR] לא נמצא אף תפריט.")
    sys.exit(1)

print(f"\nתפריט ראשי שנבחר: {main_menu['title']} ({main_menu['handle']})")

# Check if "בלוג" already exists
already_exists = any(
    item["url"] == "/blogs/news" or item["title"] in ("בלוג", "Blog")
    for item in main_menu["items"]
)

if already_exists:
    print("\n[OK] קישור 'בלוג' כבר קיים בתפריט — לא נדרש שינוי.")
else:
    print("\nמוסיף קישור 'בלוג' לתפריט...")

    ADD_ITEM_MUTATION = """
    mutation menuItemCreate($menuId: ID!, $item: MenuItemCreateInput!) {
      menuItemCreate(menuId: $menuId, item: $item) {
        menuItem {
          id
          title
          url
          type
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    # Position: after the last item (append)
    variables = {
        "menuId": main_menu["id"],
        "item": {
            "title": "בלוג",
            "type": "HTTP",
            "url": "/blogs/news",
        },
    }

    result = graphql(ADD_ITEM_MUTATION, variables)
    errors = result["menuItemCreate"]["userErrors"]
    if errors:
        print(f"[ERROR] userErrors: {json.dumps(errors, ensure_ascii=False)}")
    else:
        new_item = result["menuItemCreate"]["menuItem"]
        print(f"[SUCCESS] נוסף: id={new_item['id']} | title={new_item['title']} | url={new_item['url']}")


# ─────────────────────────────────────────────────────────────────
# TASK 2 — Fetch blog template from theme
# ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("TASK 2 — Blog Template")
print("=" * 60)

ASSETS_BASE = f"{REST_BASE}/themes/{THEME_ID}/assets.json"

for key in ("templates/blog.json", "templates/blog.liquid"):
    resp = requests.get(
        ASSETS_BASE,
        headers=headers(),
        params={"asset[key]": key},
    )
    if resp.status_code == 200:
        asset = resp.json().get("asset", {})
        print(f"\nנמצא: {key}")
        print(f"  created_at: {asset.get('created_at')}")
        print(f"  updated_at: {asset.get('updated_at')}")
        print(f"  size: {asset.get('size')} bytes")
        print(f"\n--- תוכן ---\n")
        print(asset.get("value", "(אין value — attachment בלבד)"))
        break
    else:
        print(f"  {key}: לא נמצא (status {resp.status_code})")
else:
    print("[ERROR] לא נמצא template לבלוג.")
