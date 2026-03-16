#!/usr/bin/env python3
"""
BabyMania Pipeline Driver — Claude Code Edition

Python handles: Shopify API, metafields write, file I/O, state machine, audit.
Claude Code (the AI, running in this session) handles: all AI stages (01–07 agents).

Commands:
  fetch  {pid}  — fetch product from Shopify, save full snapshot + context YAML
  push   {pid}  — pre-flight checks + write metafields + assign template_suffix
  verify {pid}  — publish verification: metafields present + body_html empty
  reset  {pid}  — reset validated+published flags (force full re-run)
  audit  {pid}  — print structured audit summary

Stage output files (Claude Code writes these between fetch and push):
  output/stage-outputs/{pid}_analyzer.yaml
  output/stage-outputs/{pid}_visual.json        <- stage 01b output
  output/stage-outputs/{pid}_intelligence.json  <- stage 01c output (product intelligence)
  output/stage-outputs/{pid}_fabric_story.txt
  output/stage-outputs/{pid}_benefits.txt
  output/stage-outputs/{pid}_faq.txt
  output/stage-outputs/{pid}_care.txt
  output/stage-outputs/{pid}_edited.txt      <- content-editor-agent output (post-writer, pre-validator)
  output/stage-outputs/{pid}_validator.txt   <- must contain: STATUS: PASS
  output/stage-outputs/{pid}_publisher.json  <- structured JSON from stage 07

Pipeline order (AI stages):
  01  product-analyzer       → {pid}_analyzer.yaml
  01b visual-product-analyzer → {pid}_visual.json  (parallel with 01)
  01c product-intelligence-builder → {pid}_intelligence.json  (python scripts/product_intelligence_builder.py {pid})
  02  fabric-story-writer    → {pid}_fabric_story.txt
  03  benefits-generator     → {pid}_benefits.txt
  04  faq-builder            → {pid}_faq.txt
  05  care-instructions      → {pid}_care.txt
  06c content-editor-agent   → {pid}_edited.txt   ← reads knowledge/copywriting/ + intelligence + all writer outputs
  06  validator              → {pid}_validator.txt  ← validates edited output
  07  shopify-publisher      → {pid}_publisher.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

# ── Paths ──────────────────────────────────────────────────────────────────────
TEAM_LEAD_DIR = Path(__file__).parent
BASE_DIR      = TEAM_LEAD_DIR.parent
CONTEXT_DIR   = BASE_DIR / "shared" / "product-context"
STAGE_OUT_DIR = BASE_DIR / "output" / "stage-outputs"
PREVIEW_DIR   = BASE_DIR / "output" / "previews"
LOGS_DIR      = BASE_DIR / "logs"
AUDIT_DIR     = LOGS_DIR / "audits"

for _d in [CONTEXT_DIR, STAGE_OUT_DIR, PREVIEW_DIR, LOGS_DIR, AUDIT_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

# ── Load config ────────────────────────────────────────────────────────────────
with open(TEAM_LEAD_DIR / "config.yaml", encoding="utf-8") as _f:
    CFG = yaml.safe_load(_f)

# ── Import pipeline library (run-pipeline.py has a dash — importlib required) ──
_spec = importlib.util.spec_from_file_location(
    "pipeline_lib",
    BASE_DIR / "scripts" / "run-pipeline.py",
)
_lib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_lib)

shopify_get                      = _lib.shopify_get
shopify_put                      = _lib.shopify_put
write_metafields                 = _lib.write_metafields
assign_clothing_template_suffix  = _lib.assign_clothing_template_suffix
update_product_body_html         = _lib.update_product_body_html
save_ctx                         = _lib.save_ctx
save_preview                     = _lib.save_preview
SHOPIFY_HOST                     = _lib.SHOPIFY_HOST
SHOPIFY_TOKEN                    = _lib.SHOPIFY_TOKEN
THEME_ID                         = _lib.THEME_ID
log                              = _lib.log

# ── Audit setup ────────────────────────────────────────────────────────────────
sys.path.insert(0, str(TEAM_LEAD_DIR))
from audit import AuditLogger, StageResult  # noqa: E402

_run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
_logger = AuditLogger(AUDIT_DIR, _run_id)


def _load_or_create_audit(pid: str, title: str):
    """
    Load existing audit stages from {pid}_audit.json (if present), then return
    a ProductAudit that continues from where the previous command left off.
    This lets fetch/push/verify each append to the same audit file.
    """
    audit      = _logger.new_product(pid, title, audit_dir=AUDIT_DIR)
    audit_path = AUDIT_DIR / f"{pid}_audit.json"
    if audit_path.exists():
        try:
            existing          = json.loads(audit_path.read_text(encoding="utf-8"))
            audit.started_at  = existing.get("started_at", audit.started_at)
            audit.final_state = existing.get("final_state", "created")
            for sd in existing.get("stages", []):
                sr           = StageResult(
                    sd["stage"], sd["status"], sd["duration_ms"],
                    sd.get("error"), sd.get("attempt", 1),
                )
                sr.timestamp = sd["timestamp"]
                audit.stages.append(sr)
        except Exception:
            pass  # corrupt / missing -> start fresh
    return audit


# ─────────────────────────────────────────────────────────────────────────────
# Stage wrappers
# ─────────────────────────────────────────────────────────────────────────────

def run_fetch_stage(pid: str) -> int:
    """
    Fetch product from Shopify.
    Saves:
      - full snapshot (body_html/template_suffix/theme info before publish)
      - context YAML (input for Claude AI stages)
    State: created -> analyzed
    """
    log.info("=" * 60)
    log.info("[fetch] product_id=%s", pid)

    try:
        product = shopify_get(f"products/{pid}.json")["product"]
    except Exception as e:
        log.error("[fetch] Shopify fetch failed: %s", e)
        return 1

    title    = product.get("title", pid)
    handle   = product.get("handle", pid)
    variants = product.get("variants") or [{}]
    audit    = _load_or_create_audit(pid, title)
    audit.set_state("created")
    audit.begin_stage("fetch")

    # ── Full snapshot — anchor for before/after comparison ────────────────────
    snapshot = {
        "fetched_at":             datetime.now().isoformat(),
        "product_id":             str(product["id"]),
        "product_title":          title,
        "product_handle":         handle,
        "product_type":           product.get("product_type", ""),
        "status":                 product.get("status", ""),
        "price":                  str(variants[0].get("price", "")),
        "variants_count":         len(variants),
        "body_html_before":       (product.get("body_html") or "").strip(),
        "body_html_before_len":   len((product.get("body_html") or "").strip()),
        "template_suffix_before": product.get("template_suffix") or "",
        "raw_product":            product,
    }

    snapshot_path = STAGE_OUT_DIR / f"{pid}_snapshot.json"
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    # ── Context YAML — input for Claude AI stages ─────────────────────────────
    body_stripped = re.sub(r"<[^>]+>", "", product.get("body_html") or "")
    tags_raw      = product.get("tags") or ""
    ctx = {
        "product_id":              str(product["id"]),
        "product_handle":          handle,
        "product_title":           title,
        "product_type":            product.get("product_type", ""),
        "product_template_type":   "",   # filled by Claude stage 01 (clothing|shoes|accessories)
        "fabric_type":             "",   # filled by Claude stage 01
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

    audit.end_stage("fetch", "pass")
    audit.set_state("analyzed")
    audit.save()

    log.info("[fetch] OK  title=%s  handle=%s", title, handle)
    log.info("  Context  -> %s", CONTEXT_DIR / f"{pid}.yaml")
    log.info("  Snapshot -> %s", snapshot_path)
    log.info("")
    log.info("  Next: Claude Code runs AI stages 01-07 and saves to:")
    log.info("    %s/", STAGE_OUT_DIR)
    log.info("    %s_analyzer.yaml             (stage 01)", pid)
    log.info("    %s_visual.json               (stage 01b — visual analyzer)", pid)
    log.info("    %s_intelligence.json         (stage 01c — product intelligence builder)", pid)
    log.info("    %s_fabric_story.txt           (stage 02)", pid)
    log.info("    %s_benefits.txt               (stage 03)", pid)
    log.info("    %s_faq.txt                    (stage 04)", pid)
    log.info("    %s_care.txt                   (stage 05)", pid)
    log.info("    %s_edited.txt                 (stage 06c — content-editor-agent)", pid)
    log.info("    %s_validator.txt              (stage 06  — must contain: STATUS: PASS)", pid)
    log.info("    %s_publisher.json             (stage 07)", pid)
    log.info("")
    log.info("  Stage 01c — Product Intelligence Builder:")
    log.info("    python scripts/product_intelligence_builder.py %s", pid)
    log.info("")
    log.info("  Knowledge layer (loaded by writer agents automatically):")
    log.info("    knowledge/copywriting/brand-voice.md")
    log.info("    knowledge/copywriting/persuasion-rules.md")
    log.info("    knowledge/copywriting/section-goals.md")
    log.info("    knowledge/copywriting/baby-clothing-library.md")
    return 0


def run_push_stage(pid: str) -> int:
    """
    Pre-flight checks + write metafields + assign template_suffix.
    Aborts hard if any required file is missing or validator did not pass.
    State: sections_generated -> validated -> published
    """
    log.info("=" * 60)
    log.info("[push] product_id=%s", pid)

    ctx_path       = CONTEXT_DIR   / f"{pid}.yaml"
    validator_path = STAGE_OUT_DIR / f"{pid}_validator.txt"
    publisher_path = STAGE_OUT_DIR / f"{pid}_publisher.json"

    # ── Pre-flight: all required files must exist ─────────────────────────────
    missing = []
    if not ctx_path.exists():       missing.append(f"context YAML:     {ctx_path}")
    if not validator_path.exists(): missing.append(f"validator output: {validator_path}")
    if not publisher_path.exists(): missing.append(f"publisher JSON:   {publisher_path}")

    if missing:
        log.error("[push] ABORTED — missing required files:")
        for m in missing:
            log.error("  MISSING: %s", m)
        return 1

    ctx   = yaml.safe_load(ctx_path.read_text(encoding="utf-8"))
    title = ctx.get("product_title", pid)
    audit = _load_or_create_audit(pid, title)
    audit.begin_stage("push_preflight")

    # ── Validator must have passed ────────────────────────────────────────────
    validator_txt = validator_path.read_text(encoding="utf-8")
    if "STATUS: PASS" not in validator_txt:
        audit.end_stage("push_preflight", "fail",
                        error="STATUS: PASS not found in validator output")
        audit.finalize("failed")
        audit.save()
        log.error("[push] ABORTED — validator did not pass. Check: %s", validator_path)
        return 1

    # ── Publisher JSON must be valid ──────────────────────────────────────────
    try:
        pub_data = json.loads(publisher_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        audit.end_stage("push_preflight", "fail",
                        error=f"publisher JSON parse error: {e}")
        audit.finalize("failed")
        audit.save()
        log.error("[push] ABORTED — publisher JSON parse error: %s", e)
        return 1

    audit.end_stage("push_preflight", "pass")
    audit.set_state("validated")

    handle                = ctx.get("product_handle", pid)
    current_suffix        = ctx.get("template_suffix_current", "")
    product_template_type = pub_data.get("product_template_type", "")
    metafields            = pub_data.get("metafields", {})

    # Save preview — audit trail
    def _read_opt(name: str) -> str:
        p = STAGE_OUT_DIR / f"{pid}_{name}"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    gen = {
        "fabric_story":      _read_opt("fabric_story.txt"),
        "benefits":          _read_opt("benefits.txt"),
        "faq":               _read_opt("faq.txt"),
        "care_instructions": _read_opt("care.txt"),
    }
    save_preview(pid, handle, ctx, gen, pub_data)

    # ── Stage: publish ────────────────────────────────────────────────────────
    audit.begin_stage("publish")
    try:
        write_metafields(pid, metafields)                                               # 1. write metafields
        assign_clothing_template_suffix(pid, product_template_type, current_suffix)    # 2. set suffix
        update_product_body_html(pid)                                                   # 3. clear body_html
    except Exception as e:
        audit.end_stage("publish", "fail", error=str(e))
        audit.finalize("failed")
        audit.save()
        log.error("[push] Publish failed: %s", e)
        return 1
    audit.end_stage("publish", "pass")
    audit.set_state("published")

    ctx["generated"].update({"published": True})
    save_ctx(ctx)
    audit.save()

    log.info("[push] OK  Published: %s [%s]", title, pid)
    log.info("  Next: python 00-team-lead/orchestrator.py verify %s", pid)
    return 0


def run_verify_stage(pid: str) -> int:
    """
    Publish verification against live Shopify API.
    Checks: all required metafields present + body_html empty.
    State: published -> published (pass) | failed
    """
    log.info("=" * 60)
    log.info("[verify] product_id=%s", pid)

    ctx_path = CONTEXT_DIR / f"{pid}.yaml"
    ctx      = yaml.safe_load(ctx_path.read_text(encoding="utf-8")) if ctx_path.exists() else {}
    title    = ctx.get("product_title", pid)
    audit    = _load_or_create_audit(pid, title)
    audit.begin_stage("verification")

    vcfg          = CFG.get("publish_verification", {})
    req_mf        = CFG.get("required_metafields", {})
    errors        = []
    product_cache = None

    def _get_product() -> dict:
        nonlocal product_cache
        if product_cache is None:
            product_cache = shopify_get(f"products/{pid}.json")["product"]
        return product_cache

    # 1. All required metafields are present
    if vcfg.get("check_metafields_written"):
        namespace    = req_mf.get("namespace", "baby_mania")
        required_keys = set(req_mf.get("required_keys", []))
        try:
            resp         = shopify_get(f"products/{pid}/metafields.json?namespace={namespace}&limit=250")
            present_keys = {mf["key"] for mf in resp.get("metafields", [])}
            missing_keys = required_keys - present_keys
            if missing_keys:
                errors.append(f"missing metafields: {sorted(missing_keys)}")
            else:
                log.info("  ✓ Metafields: all %d required keys present", len(required_keys))
        except Exception as e:
            errors.append(f"metafields check error: {e}")

    # 2. body_html is empty
    if vcfg.get("check_body_html_empty"):
        try:
            body_html = (_get_product().get("body_html") or "").strip()
            if body_html:
                errors.append(f"body_html not empty ({len(body_html)} chars remain)")
            else:
                log.info("  ✓ body_html: empty")
        except Exception as e:
            errors.append(f"body_html check error: {e}")

    if errors:
        audit.end_stage("verification", "fail", error="; ".join(errors))
        audit.finalize("failed")
        audit.save()
        log.error("[verify] FAIL — %d error(s):", len(errors))
        for err in errors:
            log.error("  FAIL: %s", err)
        return 1

    # ── Update snapshot with after-state ──────────────────────────────────────
    snapshot_path = STAGE_OUT_DIR / f"{pid}_snapshot.json"
    if snapshot_path.exists():
        snap = json.loads(snapshot_path.read_text(encoding="utf-8"))
        snap.update({
            "verified_at":       datetime.now().isoformat(),
            "body_html_after_len": len(
                (product_cache.get("body_html") or "").strip() if product_cache else ""
            ),
        })
        with open(snapshot_path, "w", encoding="utf-8") as f:
            json.dump(snap, f, ensure_ascii=False, indent=2)

    audit.end_stage("verification", "pass")
    audit.finalize("published")
    audit.save()
    audit.print_summary(log)

    log.info("[verify] OK  All checks passed — %s [%s] is live", title, pid)
    return 0


def run_reset(pid: str) -> int:
    """Reset validated + published flags — forces full pipeline re-run."""
    ctx_path = CONTEXT_DIR / f"{pid}.yaml"
    if not ctx_path.exists():
        log.warning("[reset] No context file found for %s", pid)
        return 1
    ctx = yaml.safe_load(ctx_path.read_text(encoding="utf-8"))
    ctx.get("generated", {}).update({"validated": False, "published": False})
    save_ctx(ctx)
    log.info("[reset] OK  Flags reset for product %s", pid)
    return 0


def run_audit_cmd(pid: str) -> int:
    """Print structured audit summary for a product."""
    audit_path = AUDIT_DIR / f"{pid}_audit.json"
    if not audit_path.exists():
        log.warning("[audit] No audit file found for %s", pid)
        return 1
    data = json.loads(audit_path.read_text(encoding="utf-8"))
    log.info("=== Audit: %s [%s] ===", data.get("product_title"), pid)
    log.info("  final_state:       %s", data.get("final_state"))
    log.info("  final_status:      %s", data.get("final_status"))
    log.info("  total_duration_ms: %d", data.get("total_duration_ms", 0))
    for s in data.get("stages", []):
        mark = "OK" if s["status"] == "pass" else "FAIL"
        err  = f" -- {s['error']}" if s.get("error") else ""
        log.info("  [%s] %-25s  %dms%s", mark, s["stage"], s["duration_ms"], err)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

COMMANDS = {
    "fetch":  run_fetch_stage,
    "push":   run_push_stage,
    "verify": run_verify_stage,
    "reset":  run_reset,
    "audit":  run_audit_cmd,
}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "BabyMania Pipeline Driver — Claude Code edition.\n"
            "Python handles Shopify/template/audit. Claude Code runs AI stages."
        )
    )
    ap.add_argument("command", choices=list(COMMANDS),
                    help="fetch | push | verify | reset | audit")
    ap.add_argument("product_id", help="Shopify product ID")
    args = ap.parse_args()
    sys.exit(COMMANDS[args.command](args.product_id))
