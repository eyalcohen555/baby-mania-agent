#!/usr/bin/env python3
"""
BabyMania Organic Team — Strategy Controller

Strategic decision layer for the Organic Team.
Reads stage outputs and decides whether blog content should be created,
which article to prioritize, and what the next best action is.

This is NOT the technical pipeline runner (that's organic-orchestrator.py).
This is the business-aware decision brain.

Commands:
  decide  {pid}  — evaluate opportunity and produce strategy decision
  check   {pid}  — show current decision without re-evaluating
  batch   {pid ...} — evaluate multiple products
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import yaml

# ── Paths ──────────────────────────────────────────────────────────────────────
TEAM_DIR      = Path(__file__).parent
BASE_DIR      = TEAM_DIR.parent
CONTEXT_DIR   = BASE_DIR / "shared" / "product-context"
STAGE_OUT_DIR = BASE_DIR / "output" / "stage-outputs"

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("organic-strategy")

# ── Valid field values ─────────────────────────────────────────────────────────
VALID_PRIORITY_TIERS   = ("money", "support", "authority", "skip")
VALID_NEXT_ACTIONS     = (
    "write_article", "improve_keywords", "improve_demand_validation",
    "wait_for_data", "skip_topic", "product_seo_next",
)
VALID_LEVELS           = ("low", "medium", "high")


# ─────────────────────────────────────────────────────────────────────────────
# Input loading
# ─────────────────────────────────────────────────────────────────────────────

def _load_json(path: Path) -> dict | None:
    """Load a JSON file, return None if missing or invalid."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        log.warning("[strategy] Could not load %s: %s", path.name, e)
        return None


def _load_yaml(path: Path) -> dict | None:
    """Load a YAML file, return None if missing or invalid."""
    if not path.exists():
        return None
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, OSError) as e:
        log.warning("[strategy] Could not load %s: %s", path.name, e)
        return None


def load_inputs(pid: str) -> dict:
    """Load all available stage inputs for a product."""
    ctx           = _load_yaml(CONTEXT_DIR / f"{pid}.yaml")
    keywords      = _load_json(STAGE_OUT_DIR / f"{pid}_keyword_research.json")
    topic_map     = _load_json(STAGE_OUT_DIR / f"{pid}_topic_map.json")
    blog_strategy = _load_json(STAGE_OUT_DIR / f"{pid}_blog_strategy.json")
    search_demand = _load_json(STAGE_OUT_DIR / f"{pid}_search_demand.json")

    return {
        "product_context":  ctx,
        "keyword_research": keywords,
        "topic_map":        topic_map,
        "blog_strategy":    blog_strategy,
        "search_demand":    search_demand,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Scoring helpers
# ─────────────────────────────────────────────────────────────────────────────

def _level_score(level: str) -> int:
    """Convert low/medium/high to numeric."""
    return {"low": 1, "medium": 2, "high": 3}.get(str(level).lower(), 0)


def _avg_demand_score(demand_data: dict) -> float:
    """Average demand_score across keyword and topic rankings."""
    scores = []
    for item in demand_data.get("keyword_demand_ranking", []):
        s = item.get("demand_score")
        if isinstance(s, (int, float)):
            scores.append(s)
    for item in demand_data.get("topic_demand_ranking", []):
        s = item.get("demand_score")
        if isinstance(s, (int, float)):
            scores.append(s)
    return sum(scores) / len(scores) if scores else 0.0


def _top_topic(demand_data: dict, blog_strategy: dict | None) -> dict:
    """Pick the best topic from demand ranking or blog strategy."""
    # Prefer demand-ranked topics
    rec = demand_data.get("recommended_top_topics", [])
    if rec:
        return {
            "title": rec[0].get("title", ""),
            "target_keyword": rec[0].get("target_keyword", ""),
        }
    # Fallback to blog strategy first topic
    if blog_strategy:
        topics = blog_strategy.get("blog_topics", [])
        if topics:
            return {
                "title": topics[0].get("title", ""),
                "target_keyword": topics[0].get("target_keyword", ""),
            }
    return {}


def _avg_dimension(demand_data: dict, dimension: str) -> float:
    """Average a dimension (parent_search_relevance, etc.) across rankings."""
    total, count = 0, 0
    for ranking_key in ("keyword_demand_ranking", "topic_demand_ranking"):
        for item in demand_data.get(ranking_key, []):
            val = item.get(dimension)
            if val:
                total += _level_score(val)
                count += 1
    return total / count if count else 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Decision engine
# ─────────────────────────────────────────────────────────────────────────────

def evaluate(pid: str, inputs: dict) -> dict:
    """
    Core decision logic. Returns a strategy decision dict.

    Decision matrix:
      High demand + high product fit + strong parent relevance  → money, write_article
      Medium demand + strong commercial + strong product fit    → money, write_article
      High informational demand + weak product fit              → authority, product_seo_next
      Low demand + weak relevance                               → skip, skip_topic
      Missing critical data                                     → wait_for_data
    """
    blockers: list[str] = []
    ctx            = inputs["product_context"]
    keywords       = inputs["keyword_research"]
    topic_map      = inputs.get("topic_map")
    blog_strategy  = inputs["blog_strategy"]
    search_demand  = inputs["search_demand"]

    # ── Check for missing critical inputs ──────────────────────────────────
    if ctx is None:
        blockers.append("Missing product context YAML — run fetch first")
    if keywords is None:
        blockers.append("Missing keyword_research.json — run agent 02 first")
    if blog_strategy is None:
        blockers.append("Missing blog_strategy.json — run agent 03 first")

    # If search_demand is missing, we can still decide but note it
    has_demand_data = search_demand is not None

    if not has_demand_data:
        blockers.append("Missing search_demand.json — run agent 05 for better prioritization")

    # ── If critical inputs are missing, return blocker decision ────────────
    if ctx is None or keywords is None or blog_strategy is None:
        return {
            "product_id":               pid,
            "should_create_blog_article": False,
            "recommended_first_article": {},
            "priority_tier":            "skip",
            "next_best_action":         "wait_for_data",
            "confidence_level":         "low",
            "business_value":           "low",
            "blocking_issues":          blockers,
            "reasoning_summary":        "Cannot make a strategic decision — critical input files are missing.",
            "decided_at":               datetime.now().isoformat(),
        }

    # ── Compute scores ────────────────────────────────────────────────────
    if has_demand_data:
        avg_demand    = _avg_demand_score(search_demand)
        parent_rel    = _avg_dimension(search_demand, "parent_search_relevance")
        commercial    = _avg_dimension(search_demand, "commercial_relevance")
        product_fit   = _avg_dimension(search_demand, "product_fit")
        cluster_val   = _avg_dimension(search_demand, "cluster_value")
        eval_method   = search_demand.get("demand_evaluation_method", "unknown")
    else:
        # Heuristic fallback from keyword research
        commercial_text = (keywords.get("commercial_relevance") or "").lower()
        avg_demand    = 5.0  # neutral default
        parent_rel    = 2.0  # assume medium
        commercial    = 3.0 if "high" in commercial_text else (2.0 if "medium" in commercial_text else 1.0)
        product_fit   = 2.0  # assume medium
        cluster_val   = 2.0
        eval_method   = "fallback-heuristic"

    # ── Determine priority tier ───────────────────────────────────────────
    # Composite score (weighted): demand 30%, parent_rel 20%, commercial 25%, product_fit 25%
    composite = (
        (avg_demand / 10.0) * 0.30 +       # normalize 1-10 to 0-1
        (parent_rel / 3.0)  * 0.20 +        # normalize 1-3 to 0-1
        (commercial / 3.0)  * 0.25 +
        (product_fit / 3.0) * 0.25
    )

    if composite >= 0.70 and product_fit >= 2.5:
        priority_tier = "money"
    elif composite >= 0.55 and commercial >= 2.0:
        priority_tier = "money" if product_fit >= 2.0 else "support"
    elif composite >= 0.45:
        priority_tier = "authority" if parent_rel >= 2.0 else "support"
    else:
        priority_tier = "skip"

    # ── Determine action ──────────────────────────────────────────────────
    if priority_tier == "skip":
        should_create = False
        next_action   = "skip_topic"
    elif priority_tier == "authority":
        should_create = False
        next_action   = "product_seo_next"
    elif not has_demand_data:
        should_create = False
        next_action   = "improve_demand_validation"
    else:
        should_create = True
        next_action   = "write_article"

    # ── Confidence ────────────────────────────────────────────────────────
    if has_demand_data and eval_method == "data-backed":
        confidence = "high"
    elif has_demand_data:
        confidence = "medium"
    else:
        confidence = "low"

    # ── Business value ────────────────────────────────────────────────────
    if composite >= 0.70:
        biz_value = "high"
    elif composite >= 0.45:
        biz_value = "medium"
    else:
        biz_value = "low"

    # ── Best topic — prefer topic_map global queue if available ──────────
    if topic_map:
        queue = topic_map.get("global_prioritized_queue", [])
        if queue:
            top_item = queue[0]
            best_topic = {
                "title":          top_item.get("title", ""),
                "target_keyword": top_item.get("primary_keyword", ""),
                "hub_id":         top_item.get("hub_id", ""),
                "item_type":      top_item.get("item_type", ""),
            }
        else:
            best_topic = _top_topic(search_demand, blog_strategy) if has_demand_data else _top_topic({}, blog_strategy)
    else:
        best_topic = _top_topic(search_demand, blog_strategy) if has_demand_data else _top_topic({}, blog_strategy)

    # ── Reasoning ─────────────────────────────────────────────────────────
    parts = []
    parts.append(f"Composite score: {composite:.2f}")
    parts.append(f"Avg demand: {avg_demand:.1f}/10")
    parts.append(f"Parent relevance: {parent_rel:.1f}/3")
    parts.append(f"Commercial: {commercial:.1f}/3")
    parts.append(f"Product fit: {product_fit:.1f}/3")
    if priority_tier == "money":
        parts.append("Strong opportunity — proceed with article creation.")
    elif priority_tier == "support":
        parts.append("Moderate opportunity — useful supporting content.")
    elif priority_tier == "authority":
        parts.append("Authority-building topic — not immediate priority for product conversion.")
    else:
        parts.append("Weak opportunity — not worth writing now.")
    if not has_demand_data:
        parts.append("Decision made without search demand data — confidence is lower.")

    # Remove demand-missing from blockers if we still made a decision
    non_critical_blockers = [b for b in blockers if "search_demand" not in b]
    # Keep search_demand note only as informational
    info_blockers = [b for b in blockers if "search_demand" in b]

    return {
        "product_id":                pid,
        "should_create_blog_article": should_create,
        "recommended_first_article": best_topic,
        "priority_tier":             priority_tier,
        "next_best_action":          next_action,
        "confidence_level":          confidence,
        "business_value":            biz_value,
        "topic_map_available":       topic_map is not None,
        "topic_map_hub_count":       len(topic_map.get("hubs", [])) if topic_map else 0,
        "blocking_issues":           non_critical_blockers + info_blockers,
        "reasoning_summary":         " | ".join(parts),
        "evaluation_method":         eval_method,
        "scores": {
            "composite":               round(composite, 3),
            "avg_demand":              round(avg_demand, 1),
            "parent_search_relevance": round(parent_rel, 1),
            "commercial_relevance":    round(commercial, 1),
            "product_fit":             round(product_fit, 1),
            "cluster_value":           round(cluster_val, 1),
        },
        "decided_at":                datetime.now().isoformat(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────────────────────────────────────

def run_decide(pid: str) -> int:
    """Evaluate a product and save the strategy decision."""
    log.info("=" * 60)
    log.info("[strategy:decide] product_id=%s", pid)

    inputs = load_inputs(pid)
    decision = evaluate(pid, inputs)

    # Save decision
    out_path = STAGE_OUT_DIR / f"{pid}_organic_strategy_decision.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(decision, f, ensure_ascii=False, indent=2)

    # Log result
    log.info("[strategy:decide] Decision saved: %s", out_path)
    log.info("  should_create_blog_article: %s", decision["should_create_blog_article"])
    log.info("  priority_tier:              %s", decision["priority_tier"])
    log.info("  next_best_action:           %s", decision["next_best_action"])
    log.info("  confidence_level:           %s", decision["confidence_level"])
    log.info("  business_value:             %s", decision["business_value"])

    if decision["recommended_first_article"]:
        log.info("  recommended_article:        %s", decision["recommended_first_article"].get("title", ""))

    if decision["blocking_issues"]:
        for issue in decision["blocking_issues"]:
            log.warning("  BLOCKER: %s", issue)

    log.info("  reasoning: %s", decision["reasoning_summary"])

    # Return 0 if proceed, 2 if skip/wait (non-fatal), 1 if blockers
    if decision["next_best_action"] == "wait_for_data" and not decision["should_create_blog_article"]:
        critical_blockers = [b for b in decision["blocking_issues"] if "search_demand" not in b]
        if critical_blockers:
            return 1
    return 0


def run_check(pid: str) -> int:
    """Show existing decision without re-evaluating."""
    log.info("=" * 60)
    log.info("[strategy:check] product_id=%s", pid)

    path = STAGE_OUT_DIR / f"{pid}_organic_strategy_decision.json"
    if not path.exists():
        log.error("[strategy:check] No decision file found. Run 'decide' first.")
        return 1

    decision = json.loads(path.read_text(encoding="utf-8"))
    log.info("[strategy:check] Current decision:")
    log.info("  should_create: %s | tier: %s | action: %s | confidence: %s",
             decision.get("should_create_blog_article"),
             decision.get("priority_tier"),
             decision.get("next_best_action"),
             decision.get("confidence_level"))

    if decision.get("recommended_first_article"):
        log.info("  recommended: %s", decision["recommended_first_article"].get("title", ""))

    log.info("  decided_at: %s", decision.get("decided_at", "unknown"))
    return 0


def run_batch(pids: list[str]) -> int:
    """Evaluate multiple products."""
    log.info("=" * 60)
    log.info("[strategy:batch] %d products", len(pids))

    results = {"proceed": [], "skip": [], "blocked": []}

    for pid in pids:
        rc = run_decide(pid)
        path = STAGE_OUT_DIR / f"{pid}_organic_strategy_decision.json"
        if path.exists():
            d = json.loads(path.read_text(encoding="utf-8"))
            if d.get("should_create_blog_article"):
                results["proceed"].append(pid)
            elif d.get("next_best_action") == "wait_for_data":
                results["blocked"].append(pid)
            else:
                results["skip"].append(pid)
        else:
            results["blocked"].append(pid)

    log.info("[strategy:batch] Summary:")
    log.info("  Proceed:  %d — %s", len(results["proceed"]), results["proceed"])
    log.info("  Skip:     %d — %s", len(results["skip"]), results["skip"])
    log.info("  Blocked:  %d — %s", len(results["blocked"]), results["blocked"])
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="BabyMania Organic Team — Strategy Controller"
    )
    ap.add_argument("command", choices=["decide", "check", "batch"],
                    help="decide | check | batch")
    ap.add_argument("product_ids", nargs="+", help="One or more Shopify product IDs")
    args = ap.parse_args()

    if args.command == "batch":
        sys.exit(run_batch(args.product_ids))
    else:
        cmd_map = {"decide": run_decide, "check": run_check}
        rc = 0
        for pid in args.product_ids:
            result = cmd_map[args.command](pid)
            if result != 0:
                rc = result
        sys.exit(rc)
