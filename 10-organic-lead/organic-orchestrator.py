#!/usr/bin/env python3
"""
BabyMania Organic Team — Pipeline Driver

Handles: fetch (reuse or fresh), push tags, verify tags.
Claude Code (AI) handles: 01-organic-tag-generator.

Commands:
  fetch  {pid}  — ensure context YAML exists (reuse from main team or fresh fetch)
  push   {pid}  — read organic_tags.json + update product tags in Shopify
  verify {pid}  — confirm tags were saved correctly
  batch  {pid ...} — run push+verify on multiple products
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
TEAM_DIR     = Path(__file__).parent
BASE_DIR     = TEAM_DIR.parent
CONTEXT_DIR  = BASE_DIR / "shared" / "product-context"
STAGE_OUT_DIR = BASE_DIR / "output" / "stage-outputs"

# ── Import pipeline library (shared with main team) ───────────────────────────
_spec = importlib.util.spec_from_file_location(
    "pipeline_lib",
    BASE_DIR / "scripts" / "run-pipeline.py",
)
_lib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_lib)

shopify_get  = _lib.shopify_get
shopify_put  = _lib.shopify_put
save_ctx     = _lib.save_ctx
log          = _lib.log

import yaml  # noqa: E402


# ─────────────────────────────────────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────────────────────────────────────

def run_fetch(pid: str) -> int:
    """
    Ensure context YAML exists for this product.
    If it already exists (from main team fetch), skip.
    Otherwise, fetch from Shopify and create a minimal context.
    """
    log.info("=" * 60)
    log.info("[organic:fetch] product_id=%s", pid)

    ctx_path = CONTEXT_DIR / f"{pid}.yaml"
    if ctx_path.exists():
        ctx = yaml.safe_load(ctx_path.read_text(encoding="utf-8"))
        log.info("[organic:fetch] Context already exists: %s", ctx.get("product_title", pid))
        log.info("  Skipping fetch — reusing existing context.")
        return 0

    # Fresh fetch
    try:
        product = shopify_get(f"products/{pid}.json")["product"]
    except Exception as e:
        log.error("[organic:fetch] Shopify fetch failed: %s", e)
        return 1

    import re
    title    = product.get("title", pid)
    handle   = product.get("handle", pid)
    variants = product.get("variants") or [{}]
    body_stripped = re.sub(r"<[^>]+>", "", product.get("body_html") or "")
    tags_raw = product.get("tags") or ""

    ctx = {
        "product_id":              str(product["id"]),
        "product_handle":          handle,
        "product_title":           title,
        "product_type":            product.get("product_type", ""),
        "fabric_type":             "",
        "target_age":              "",
        "main_use":                "",
        "price":                   str(variants[0].get("price", "")),
        "variants_count":          len(variants),
        "tags":                    [t.strip() for t in tags_raw.split(",") if t.strip()],
        "fetched_at":              datetime.now().isoformat(),
        "description_raw":         body_stripped[:2000],
        "template_suffix_current": product.get("template_suffix") or "",
        "generated": {
            "validated": False,
            "published": False,
        },
    }
    save_ctx(ctx)
    log.info("[organic:fetch] OK  title=%s  handle=%s", title, handle)
    return 0


def run_push(pid: str) -> int:
    """
    Read organic_tags.json and update product tags in Shopify.
    Does NOT touch body_html, template_suffix, or any other field.
    """
    log.info("=" * 60)
    log.info("[organic:push] product_id=%s", pid)

    tags_path = STAGE_OUT_DIR / f"{pid}_organic_tags.json"
    if not tags_path.exists():
        log.error("[organic:push] ABORTED — missing: %s", tags_path)
        log.error("  Run 01-organic-tag-generator first.")
        return 1

    try:
        tags_data = json.loads(tags_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        log.error("[organic:push] ABORTED — JSON parse error: %s", e)
        return 1

    shopify_tags = tags_data.get("shopify_tags", [])
    if not shopify_tags:
        log.error("[organic:push] ABORTED — shopify_tags is empty")
        return 1

    # Validate: all tags must be lowercase ASCII with hyphens
    for tag in shopify_tags:
        if not tag.isascii():
            log.error("[organic:push] ABORTED — non-ASCII tag found: '%s'", tag)
            return 1
        if tag != tag.lower():
            log.error("[organic:push] ABORTED — uppercase tag found: '%s'", tag)
            return 1

    tags_string = ", ".join(shopify_tags)
    log.info("[organic:push] Updating tags (%d): %s", len(shopify_tags), tags_string)

    try:
        result = shopify_put(
            f"products/{pid}.json",
            {"product": {"id": int(pid), "tags": tags_string}},
        )
    except Exception as e:
        log.error("[organic:push] Shopify update failed: %s", e)
        return 1

    updated_tags = result.get("product", {}).get("tags", "")
    log.info("[organic:push] OK  Tags saved: %s", updated_tags)

    # Update tags_data with push result
    tags_data["pushed_at"] = datetime.now().isoformat()
    tags_data["pushed_tags_string"] = updated_tags
    with open(tags_path, "w", encoding="utf-8") as f:
        json.dump(tags_data, f, ensure_ascii=False, indent=2)

    return 0


def run_verify(pid: str) -> int:
    """
    Verify that the product tags in Shopify match the organic_tags.json.
    """
    log.info("=" * 60)
    log.info("[organic:verify] product_id=%s", pid)

    tags_path = STAGE_OUT_DIR / f"{pid}_organic_tags.json"
    if not tags_path.exists():
        log.error("[organic:verify] No organic_tags.json found for %s", pid)
        return 1

    tags_data = json.loads(tags_path.read_text(encoding="utf-8"))
    expected_tags = set(tags_data.get("shopify_tags", []))

    try:
        product = shopify_get(f"products/{pid}.json")["product"]
    except Exception as e:
        log.error("[organic:verify] Shopify fetch failed: %s", e)
        return 1

    actual_tags_raw = product.get("tags", "")
    actual_tags = {t.strip() for t in actual_tags_raw.split(",") if t.strip()}

    # Check 1: tags not empty
    if not actual_tags:
        log.error("[organic:verify] FAIL — product has no tags")
        return 1

    # Check 2: all expected tags present
    missing = expected_tags - actual_tags
    if missing:
        log.error("[organic:verify] FAIL — missing tags: %s", missing)
        return 1

    log.info("[organic:verify] OK  All %d tags verified", len(expected_tags))
    log.info("  Tags: %s", ", ".join(sorted(expected_tags)))

    # Update verified status
    tags_data["verified_at"] = datetime.now().isoformat()
    tags_data["verified"] = True
    with open(tags_path, "w", encoding="utf-8") as f:
        json.dump(tags_data, f, ensure_ascii=False, indent=2)

    return 0


def run_batch(pids: list[str]) -> int:
    """Run push + verify on multiple products."""
    log.info("=" * 60)
    log.info("[organic:batch] %d products", len(pids))

    failed = []
    for pid in pids:
        rc = run_push(pid)
        if rc != 0:
            failed.append(pid)
            continue
        rc = run_verify(pid)
        if rc != 0:
            failed.append(pid)

    if failed:
        log.error("[organic:batch] %d/%d FAILED: %s", len(failed), len(pids), failed)
        return 1

    log.info("[organic:batch] OK  %d/%d products completed", len(pids), len(pids))
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="BabyMania Organic Team — Pipeline Driver"
    )
    ap.add_argument("command", choices=["fetch", "push", "verify", "batch"],
                    help="fetch | push | verify | batch")
    ap.add_argument("product_ids", nargs="+", help="One or more Shopify product IDs")
    args = ap.parse_args()

    if args.command == "batch":
        sys.exit(run_batch(args.product_ids))
    else:
        cmd_map = {"fetch": run_fetch, "push": run_push, "verify": run_verify}
        rc = 0
        for pid in args.product_ids:
            result = cmd_map[args.command](pid)
            if result != 0:
                rc = result
        sys.exit(rc)
