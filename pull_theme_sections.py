#!/usr/bin/env python3
"""
Pull product sections from the active Shopify theme and save locally.
Targets: bm-store-*, main-product.liquid, related-products.liquid
"""

import sys
import os
import json
import requests
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, "C:/Projects/baby-mania-agent")
from shopify_client import _headers, BASE_URL

LOCAL_DIR = Path("C:/Projects/baby-mania-agent/theme_assets/sections")
LOCAL_DIR.mkdir(parents=True, exist_ok=True)

TARGET_PREFIXES = ("bm-store-",)
TARGET_EXACT = {"sections/main-product.liquid", "sections/related-products.liquid"}


def get_active_theme_id():
    resp = requests.get(f"{BASE_URL}/themes.json", headers=_headers())
    resp.raise_for_status()
    themes = resp.json()["themes"]
    for t in themes:
        if t.get("role") == "main":
            return t["id"], t["name"]
    # fallback: first theme
    return themes[0]["id"], themes[0]["name"]


def list_section_assets(theme_id):
    """Return all asset keys that start with 'sections/'."""
    resp = requests.get(
        f"{BASE_URL}/themes/{theme_id}/assets.json",
        headers=_headers(),
    )
    resp.raise_for_status()
    assets = resp.json()["assets"]
    return [a for a in assets if a["key"].startswith("sections/")]


def is_target(key):
    filename = key.replace("sections/", "")
    if key in TARGET_EXACT:
        return True
    for prefix in TARGET_PREFIXES:
        if filename.startswith(prefix):
            return True
    return False


def fetch_asset_content(theme_id, key):
    resp = requests.get(
        f"{BASE_URL}/themes/{theme_id}/assets.json",
        headers=_headers(),
        params={"asset[key]": key},
    )
    resp.raise_for_status()
    asset = resp.json()["asset"]
    return asset.get("value", "")


def main():
    print("=" * 65)
    print("Pull Theme Sections — BabyMania")
    print("=" * 65)

    # Step 1: Active theme
    print("\n[1] Finding active theme...")
    theme_id, theme_name = get_active_theme_id()
    print(f"    Theme: {theme_name} (id={theme_id})")

    # Step 2: List all section assets
    print("\n[2] Listing sections in theme...")
    all_sections = list_section_assets(theme_id)
    print(f"    Total sections in theme: {len(all_sections)}")

    # Step 3: Filter targets
    targets = [a for a in all_sections if is_target(a["key"])]
    print(f"    Matched targets       : {len(targets)}")

    if not targets:
        print("\n    No target sections found in theme.")
        return

    print("\n    Target sections found:")
    for a in targets:
        print(f"    · {a['key']}")

    # Step 4: Download and save
    print("\n[3] Downloading and saving...")
    results = []

    for asset in targets:
        key = asset["key"]
        filename = key.replace("sections/", "")
        local_path = LOCAL_DIR / filename

        print(f"\n    {filename}")
        print(f"    key: {key}")

        content = fetch_asset_content(theme_id, key)
        size_bytes = len(content.encode("utf-8"))
        size_kb = size_bytes / 1024

        local_path.write_text(content, encoding="utf-8")

        results.append({
            "filename": filename,
            "key": key,
            "local_path": str(local_path),
            "size_bytes": size_bytes,
            "size_kb": round(size_kb, 1),
        })

        print(f"    saved: {local_path}")
        print(f"    size : {size_kb:.1f} KB")

    # Step 5: Verify — list all files now in sections/
    print("\n[4] Verifying local directory...")
    all_local = sorted(LOCAL_DIR.glob("*.liquid"))
    print(f"\n    Files in theme_assets/sections/ ({len(all_local)} total):\n")
    for f in all_local:
        size = f.stat().st_size / 1024
        print(f"    {f.name:<45} {size:>6.1f} KB")

    # Summary report
    print("\n" + "=" * 65)
    print("REPORT")
    print("=" * 65)
    for r in results:
        print(f"\n  {r['filename']}")
        print(f"  key  : {r['key']}")
        print(f"  saved: {r['local_path']}")
        print(f"  size : {r['size_kb']} KB")

    out_path = "C:/Projects/baby-mania-agent/PULL_SECTIONS_RESULTS.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"theme_id": theme_id, "theme_name": theme_name, "sections": results}, f, ensure_ascii=False, indent=2)
    print(f"\n  Results -> {out_path}")


if __name__ == "__main__":
    main()
