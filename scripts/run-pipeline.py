#!/usr/bin/env python3
"""
BabyMania Content Pipeline
- Stages 2-5 parallel (ThreadPoolExecutor)
- Writes 14 baby_mania metafields to Shopify (no template JSON assets)
- Assigns template_suffix="clothing" by product_template_type
- Skip:   validated=True + published=True
- Resume: validated=True + published=False  → publish only, no re-generation
"""
import io
import os
import sys
import json
import re
import logging
from pathlib import Path
from datetime import datetime
import yaml
import requests
from dotenv import load_dotenv

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent.parent
AGENTS_DIR  = BASE_DIR / ".claude" / "agents"
PROMPTS_DIR = BASE_DIR / "prompts"
CONTEXT_DIR = BASE_DIR / "shared" / "product-context"
LOGS_DIR    = BASE_DIR / "logs"

for _d in [CONTEXT_DIR, LOGS_DIR, BASE_DIR / "output" / "previews"]:
    _d.mkdir(parents=True, exist_ok=True)

# ── Env ───────────────────────────────────────────────────────
load_dotenv(BASE_DIR / ".env")
_tok = Path.home() / "Desktop/shopify-token/.env"
if _tok.exists():
    load_dotenv(_tok, override=True)

# ── Logging ───────────────────────────────────────────────────
# Force utf-8 on Windows stdout (cp1255 doesn't support Hebrew/Unicode symbols)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

_ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = LOGS_DIR / f"pipeline_{_ts}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("bm-pipeline")

# ── Config ────────────────────────────────────────────────────
PREVIEW_MODE  = False
BATCH_SIZE    = 5
THEME_ID      = os.getenv("SHOPIFY_THEME_ID", "183668179257")
SHOPIFY_HOST  = os.getenv("SHOPIFY_SHOP_URL", "a2756c-c0.myshopify.com")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")

VALID_ICON_TYPES = {
    "wash_60", "sun_dry", "iron",
    "no_bleach", "repeat", "no_tumble_dry", "hand_wash",
}

PROTECTED_TEMPLATE_SUFFIXES = {"tempio", "easy-sleep"}


# ── Loaders ───────────────────────────────────────────────────

def load_agent(filename: str) -> str:
    """Load system prompt from .claude/agents/*.md, stripping YAML frontmatter."""
    text = (AGENTS_DIR / filename).read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return text.strip()


def load_prompt(filename: str) -> str:
    """Load prompt template from prompts/*.md."""
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def format_prompt(template: str, ctx: dict) -> str:
    """Safe token replacement — handles special chars in values."""
    for key, value in ctx.items():
        if isinstance(value, (str, int, float)):
            template = template.replace(f"{{{key}}}", str(value or ""))
    return template


# ── Shopify API ───────────────────────────────────────────────

def shopify_get(path: str) -> dict:
    url = f"https://{SHOPIFY_HOST}/admin/api/2024-10/{path}"
    r = requests.get(url, headers={"X-Shopify-Access-Token": SHOPIFY_TOKEN})
    r.raise_for_status()
    return r.json()


def shopify_put(path: str, payload: dict) -> dict:
    url = f"https://{SHOPIFY_HOST}/admin/api/2024-10/{path}"
    r = requests.put(
        url,
        headers={
            "X-Shopify-Access-Token": SHOPIFY_TOKEN,
            "Content-Type"          : "application/json",
        },
        json=payload,
    )
    r.raise_for_status()
    return r.json()


def shopify_post(path: str, payload: dict) -> dict:
    url = f"https://{SHOPIFY_HOST}/admin/api/2024-10/{path}"
    r = requests.post(
        url,
        headers={
            "X-Shopify-Access-Token": SHOPIFY_TOKEN,
            "Content-Type"          : "application/json",
        },
        json=payload,
    )
    r.raise_for_status()
    return r.json()


def write_metafields(product_id: str, metafields: dict, skip_if_exists: set = frozenset()) -> int:
    """
    Upsert all baby_mania metafields for a product.
    Fetches existing metafields first, then PUT for updates and POST for new keys.
    Returns count of metafields written.

    skip_if_exists: keys to skip if they already exist in Shopify (preserve approved values).
    """
    namespace = "baby_mania"
    json_keys = {"benefits", "care_instructions", "faq", "fabric_tags", "accordion_blocks"}

    existing_resp = shopify_get(
        f"products/{product_id}/metafields.json?namespace={namespace}&limit=250"
    )
    existing_map = {mf["key"]: mf["id"] for mf in existing_resp.get("metafields", [])}

    written = 0
    for key, value in metafields.items():
        if key in skip_if_exists and key in existing_map:
            log.info("  Protecting %s — existing value preserved", key)
            continue
        mf_type  = "json" if key in json_keys else "single_line_text_field"
        mf_value = (
            json.dumps(value, ensure_ascii=False)
            if isinstance(value, (list, dict))
            else str(value or "")
        )
        # Shopify rejects empty single_line_text_field values — skip them
        if not mf_value or mf_value in ("[]", "{}"):
            log.info("  Skipping %s — empty value", key)
            continue
        payload = {"metafield": {
            "namespace": namespace,
            "key"      : key,
            "value"    : mf_value,
            "type"     : mf_type,
        }}

        if key in existing_map:
            shopify_put(
                f"products/{product_id}/metafields/{existing_map[key]}.json",
                payload,
            )
        else:
            shopify_post(f"products/{product_id}/metafields.json", payload)

        written += 1

    log.info("  ✓ Metafields written: %d/%d  (namespace=%s)", written, len(metafields), namespace)
    return written


def assign_clothing_template_suffix(
    product_id: str, product_template_type: str, current_suffix: str
) -> bool:
    """
    Set template_suffix="clothing" when product_template_type=="clothing".
    Skips if suffix is already correct, or if it's a protected template.
    Returns True if an update was made.
    """
    if current_suffix in PROTECTED_TEMPLATE_SUFFIXES:
        log.warning(
            "  [PROTECTED] template_suffix='%s' is protected — skipping suffix update",
            current_suffix,
        )
        return False

    if product_template_type != "clothing":
        log.info("  template_suffix: no change (product_template_type=%s)", product_template_type)
        return False

    target = "clothing"
    if current_suffix == target:
        log.info("  template_suffix already '%s' — no update needed", target)
        return False

    url = f"https://{SHOPIFY_HOST}/admin/api/2024-10/products/{product_id}.json"
    r = requests.put(
        url,
        headers={
            "X-Shopify-Access-Token": SHOPIFY_TOKEN,
            "Content-Type"          : "application/json",
        },
        json={"product": {"id": int(product_id), "template_suffix": target}},
    )
    r.raise_for_status()
    log.info("  ✓ template_suffix: '%s' → '%s'", current_suffix or "(none)", target)
    return True


def update_product_body_html(product_id: str, body_html: str = "") -> bool:
    """
    Replace product body_html with short text or empty string.
    Sections handle all content display — body_html would duplicate it.
    """
    url = f"https://{SHOPIFY_HOST}/admin/api/2024-10/products/{product_id}.json"
    r = requests.put(
        url,
        headers={
            "X-Shopify-Access-Token": SHOPIFY_TOKEN,
            "Content-Type"          : "application/json",
        },
        json={"product": {"id": int(product_id), "body_html": body_html}},
    )
    r.raise_for_status()
    log.info("  ✓ body_html cleared for product %s", product_id)
    return True


# ── Context & preview helpers ─────────────────────────────────

def extract_section(text: str, key: str) -> str:
    """Extract content after 'key:\\n' until next top-level key or end."""
    m = re.search(
        rf"^{re.escape(key)}:\s*\n(.*?)(?=^\w[\w_]*:\s*$|\Z)",
        text, re.DOTALL | re.MULTILINE,
    )
    return m.group(1).strip() if m else ""


def save_ctx(ctx: dict):
    pid  = str(ctx["product_id"])
    path = CONTEXT_DIR / f"{pid}.yaml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(ctx, f, allow_unicode=True, default_flow_style=False)


def save_preview(pid: str, handle: str, ctx: dict, gen: dict, publisher_payload: dict):
    """Save full preview file: context + agent outputs + metafields payload."""
    preview_dir = BASE_DIR / "output" / "previews"
    preview_dir.mkdir(parents=True, exist_ok=True)
    preview = {
        "product_id"      : pid,
        "product_handle"  : handle,
        "product_title"   : ctx.get("product_title", ""),
        "generated_at"    : datetime.now().isoformat(),
        "context"         : ctx,
        "agent_outputs"   : gen,
        "publisher_payload": publisher_payload,
    }
    path = preview_dir / f"{pid}_preview.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(preview, f, ensure_ascii=False, indent=2)
    log.info("  Preview → %s", path)


def should_skip(p: dict) -> tuple:
    """Pre-pipeline product filter (before context-file check)."""
    if p.get("status") != "active":
        return True, "not active"
    price = float((p.get("variants") or [{}])[0].get("price", 0))
    if price == 0:
        return True, "price=0"
    if "TEST" in (p.get("title") or "").upper():
        return True, "test product"
    return False, None


# ── CLI ───────────────────────────────────────────────────────
# This file is a function library imported by 00-team-lead/orchestrator.py.
# Running it directly delegates to the orchestrator (thin wrapper).

if __name__ == "__main__":
    import subprocess
    _orch = Path(__file__).parent.parent / "00-team-lead" / "orchestrator.py"
    sys.exit(subprocess.call([sys.executable, str(_orch)] + sys.argv[1:]))
