#!/usr/bin/env python3
"""
BabyMania Organic Team — Hub Status Agent
==========================================
מציג את רשימת כל ה-HUBs עם הסטטוס שלהם.
הרץ בתחילת כל עבודה על הצוות האורגני.

Usage:
  python hub-status.py           — הצג את כל ה-HUBs
  python hub-status.py --next    — הצג רק את ה-HUB הבא לעבודה
  python hub-status.py --update HUB-5 published  — עדכן סטטוס
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# Fix Windows console encoding
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

REGISTRY_PATH = Path(__file__).parent.parent / "hub-registry.json"

STATUS_EMOJI = {
    "published": "✅",
    "in_progress": "🔄",
    "planned": "📋",
    "draft": "✏️",
}


def load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        print(f"❌ לא נמצא קובץ רישום: {REGISTRY_PATH}")
        raise SystemExit(1)
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def save_registry(data: dict) -> None:
    data["last_updated"] = date.today().isoformat()
    REGISTRY_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"✅ רישום עודכן: {REGISTRY_PATH}")


def show_all(registry: dict) -> None:
    print()
    print("=" * 55)
    print("  📊 BabyMania — סטטוס HUBs אורגני")
    print("=" * 55)
    print(f"  עודכן לאחרונה: {registry.get('last_updated', '?')}")
    print(f"  הועלה אחרון:   {registry.get('last_published', '?')}")
    print(f"  HUB הבא:       {registry.get('next_hub', '?')}")
    print("=" * 55)
    print()

    for hub in registry["hubs"]:
        emoji = STATUS_EMOJI.get(hub["status"], "❓")
        count = hub["articles_count"]
        pub_date = hub.get("published_at") or "—"
        articles = ", ".join(hub["articles"]) if hub["articles"] else "—"

        print(f"  {emoji} {hub['hub_id']:8s} | {hub['hub_name_he']:25s} | {hub['status']:12s} | {str(count):2s} מאמרים | {pub_date}")
        if hub.get("pillar_keyword"):
            print(f"           Pillar: \"{hub['pillar_keyword']}\"")
        if hub.get("notes"):
            print(f"           📝 {hub['notes']}")
        print()

    print("=" * 55)


def show_next(registry: dict) -> None:
    next_hub_id = registry.get("next_hub")
    hub = next(
        (h for h in registry["hubs"] if h["hub_id"] == next_hub_id),
        None
    )
    if not hub:
        print(f"❌ לא נמצא {next_hub_id} ברישום")
        return

    print()
    print("=" * 45)
    print(f"  ▶️  HUB הבא לעבודה: {hub['hub_id']}")
    print("=" * 45)
    print(f"  נושא: {hub['hub_name_he']}")
    print(f"  סטטוס: {hub['status']}")
    if hub.get("pillar_keyword"):
        print(f"  Pillar keyword: {hub['pillar_keyword']}")
    print(f"  📝 {hub.get('notes', '—')}")
    print("=" * 45)
    print()


def update_status(registry: dict, hub_id: str, new_status: str) -> None:
    hub = next(
        (h for h in registry["hubs"] if h["hub_id"] == hub_id),
        None
    )
    if not hub:
        print(f"❌ לא נמצא {hub_id}")
        return

    old_status = hub["status"]
    hub["status"] = new_status

    if new_status == "published" and not hub.get("published_at"):
        hub["published_at"] = date.today().isoformat()

    # Update last_published and next_hub if needed
    if new_status == "published":
        registry["last_published"] = hub_id
        # Find the next planned hub
        for h in registry["hubs"]:
            if h["status"] in ("planned", "draft") and h["hub_id"] != hub_id:
                registry["next_hub"] = h["hub_id"]
                break

    save_registry(registry)
    print(f"✅ {hub_id}: {old_status} → {new_status}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="BabyMania Hub Status")
    ap.add_argument("--next", action="store_true", help="הצג רק HUB הבא")
    ap.add_argument("--update", nargs=2, metavar=("HUB_ID", "STATUS"),
                    help="עדכן סטטוס — לדוגמה: --update HUB-5 in_progress")
    args = ap.parse_args()

    registry = load_registry()

    if args.update:
        update_status(registry, args.update[0], args.update[1])
        registry = load_registry()  # reload
        show_all(registry)
    elif args.next:
        show_next(registry)
    else:
        show_all(registry)
