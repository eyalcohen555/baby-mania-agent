#!/usr/bin/env python3
"""
BabyMania — Rewrite care_instructions to positive framing.
Rewrites all publisher.json files + pushes updated metafield to Shopify.
"""
import io, json, os, sys, time
from pathlib import Path
from dotenv import load_dotenv
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_DIR      = Path(__file__).parent.parent
STAGE_OUT_DIR = BASE_DIR / "output" / "stage-outputs"

load_dotenv(BASE_DIR / ".env")
tok = Path.home() / "Desktop/shopify-token/.env"
if tok.exists():
    load_dotenv(tok, override=True)

TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOP  = "a2756c-c0.myshopify.com"
HDR   = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}
API   = f"https://{SHOP}/admin/api/2024-10"

# ── Positive framing library ───────────────────────────────────────────────────
# Keys: icon_type
# Values: (card_title, card_text)
# card_text has optional {season} placeholder substituted from product context.

POSITIVE_BASE = {
    "hand_wash": (
        "כביסה עדינה ביד",
        "שומרת על רכות הבד {season_care}כביסה אחרי כביסה",
    ),
    "wash_60": (
        "כביסה עד 60°",
        "בגד עמיד — נשמר כחדש אחרי כביסות חוזרות",
    ),
    "sun_dry": (
        "ייבוש טבעי באוויר",
        "שומר על הצורה והצבע לאורך זמן",
    ),
    "no_bleach": (
        "שמירה על הצבע",
        "הסיבים עמידים — שומר על הגוון המקורי",
    ),
    "no_tumble_dry": (
        "ייבוש טבעי מומלץ",
        "שומר על הצורה המקורית ומאריך את חיי הבגד",
    ),
    "iron": (
        "גיהוץ עדין",
        "מראה נקי ומסודר — חום נמוך מספיק",
    ),
    "repeat": (
        "עמיד לכביסות חוזרות",
        "הצבע והצורה נשמרים כביסה אחרי כביסה",
    ),
}

SEASON_CARE_TEXT = {
    "winter": "ושמירה על החמימות — ",
    "summer": "ונשימת הבד — ",
    "":       "",
}

# Fabric keywords that justify hand_wash (must appear in fabric_type)
DELICATE_FABRIC_KEYWORDS = {
    "צמר", "קשמיר", "משי", "לייקרה", "אנגורה", "מוהר", "שיפון",
    "wool", "cashmere", "silk", "lycra", "angora", "chiffon",
}

# Default card used when hand_wash is not justified by fabric data
HAND_WASH_DEFAULT = {
    "icon_type":  "wash_60",
    "card_title": "כביסה עדינה במכונה",
    "card_text":  "מתאים לכביסה יומיומית — הבד נשמר רך ונעים",
}

# Icon types in the same logical group — keep only the first encountered per group
DUPLICATE_GROUPS = [
    {"sun_dry", "no_tumble_dry"},   # both mean "air-dry" — sun_dry is more positive
]


def detect_season(pid: str) -> str:
    """Detect season from analyzer.yaml. Returns 'winter'|'summer'|''."""
    try:
        import yaml
        path = STAGE_OUT_DIR / f"{pid}_analyzer.yaml"
        if not path.exists():
            return ""
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        use = (data.get("main_use") or "").lower()
        if "חורף" in use or "winter" in use:
            return "winter"
        if "קיץ" in use or "summer" in use:
            return "summer"
    except Exception:
        pass
    return ""


def _hand_wash_justified(fabric_type: str) -> bool:
    """Return True only if fabric_type explicitly mentions a delicate fabric."""
    if not fabric_type:
        return False
    ft = fabric_type.lower()
    return any(kw in ft for kw in DELICATE_FABRIC_KEYWORDS)


def _deduplicate(cards: list) -> list:
    """Remove cards that duplicate the same logical group — keep first in group."""
    seen_groups: set[int] = set()
    result = []
    for card in cards:
        icon = card.get("icon_type", "")
        group_idx = None
        for idx, group in enumerate(DUPLICATE_GROUPS):
            if icon in group:
                group_idx = idx
                break
        if group_idx is not None:
            if group_idx in seen_groups:
                continue  # duplicate in this group — skip
            seen_groups.add(group_idx)
        result.append(card)
    return result


def rewrite_care(care_list: list, season: str, fabric_type: str = "") -> list:
    """Rewrite a list of care cards to positive framing."""
    season_care = SEASON_CARE_TEXT.get(season, "")
    rewritten = []
    for card in care_list:
        icon = card.get("icon_type", "")

        # hand_wash: replace with safe default if not justified by fabric data
        # Guard: skip replacement if card_title is already the correct positive framing
        if icon == "hand_wash" and not _hand_wash_justified(fabric_type):
            rewritten.append(dict(HAND_WASH_DEFAULT))
            continue

        if icon in POSITIVE_BASE:
            title, text = POSITIVE_BASE[icon]
            text = text.replace("{season_care}", season_care)
        else:
            # Unknown icon — keep original but sanitise negative language
            title = card.get("card_title", "")
            text  = card.get("card_text", "")
            # Replace common negative phrases with positive equivalents
            for neg, pos in [
                ("אין להשתמש ב", "שומר על "),
                ("ללא ", "עם "),
                ("אסור ", "מומלץ "),
                ("הימנעו", "מומלץ"),
                ("לא להכניס", "מומלץ לייבש"),
                ("בלבד", ""),
            ]:
                title = title.replace(neg, pos)
                text  = text.replace(neg, pos)
        rewritten.append({
            "icon_type":  icon,
            "card_title": title.strip(),
            "card_text":  text.strip(),
        })

    return _deduplicate(rewritten)


def push_care_metafield(pid: str, care_list: list) -> bool:
    """Upsert care_instructions metafield in Shopify. Returns True on success."""
    namespace = "baby_mania"
    key       = "care_instructions"
    value     = json.dumps(care_list, ensure_ascii=False)

    # Find existing metafield ID
    r = requests.get(
        f"{API}/products/{pid}/metafields.json",
        headers={"X-Shopify-Access-Token": TOKEN},
        params={"namespace": namespace, "key": key, "limit": 10},
        timeout=15,
    )
    existing = r.json().get("metafields", [])

    payload = {"metafield": {
        "namespace": namespace,
        "key":       key,
        "value":     value,
        "type":      "json",
    }}

    if existing:
        mf_id = existing[0]["id"]
        resp  = requests.put(
            f"{API}/products/{pid}/metafields/{mf_id}.json",
            headers=HDR, json=payload, timeout=15,
        )
    else:
        resp = requests.post(
            f"{API}/products/{pid}/metafields.json",
            headers=HDR, json=payload, timeout=15,
        )
    return resp.status_code in (200, 201)


# ── Main ───────────────────────────────────────────────────────────────────────

publisher_files = sorted(STAGE_OUT_DIR.glob("*_publisher.json"))
print(f"Products to process: {len(publisher_files)}\n")
print(f"{'PRODUCT ID':<20} {'SEASON':<8} {'CARDS':<6} {'SHOPIFY':<10} STATUS")
print("-" * 60)

ok_count = fail_count = 0

for f in publisher_files:
    pid = f.stem.replace("_publisher", "")
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"{pid:<20} {'?':<8} {'?':<6} {'?':<10} PARSE ERROR: {e}")
        fail_count += 1
        continue

    mf = data.get("metafields", {})
    old_care = mf.get("care_instructions", [])
    if not old_care:
        print(f"{pid:<20} {'?':<8} {'0':<6} {'SKIPPED':<10} NO CARE DATA")
        continue

    season      = detect_season(pid)
    fabric_type = data.get("metafields", {}).get("fabric_type", "") or \
                  data.get("fabric_type", "") or ""
    new_care = rewrite_care(old_care, season, fabric_type)

    # Update publisher.json
    data["metafields"]["care_instructions"] = new_care
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Push to Shopify
    pushed = push_care_metafield(pid, new_care)
    status = "OK" if pushed else "PUSH FAIL"
    if pushed:
        ok_count += 1
    else:
        fail_count += 1

    print(f"{pid:<20} {season:<8} {len(new_care):<6} {'OK' if pushed else 'FAIL':<10} {status}")
    time.sleep(0.3)

print(f"\nDone: {ok_count} OK  {fail_count} FAIL")
