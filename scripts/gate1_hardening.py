#!/usr/bin/env python3
"""
Gate 1 Extended — Structure Hardening
AUTOMATION-HARDENING-PLAN v1 | P1-S6
Checks: empty publisher values, duplicate metafield keys,
        bundle duplicate PIDs, known anomaly exclusion.

Usage:
  python gate1_hardening.py <pid>
  python gate1_hardening.py <pid> --batch-pids pid1,pid2,pid3
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR      = Path(__file__).parent.parent
STAGE_OUT_DIR = BASE_DIR / "output" / "stage-outputs"
CONTEXT_DIR   = BASE_DIR / "shared" / "product-context"
ANOMALY_REGISTRY_PATH = BASE_DIR / "docs" / "operations" / "known-anomalies-registry.md"

# Required metafields per product type
_REQUIRED_METAFIELDS: dict[str, list[str]] = {
    "clothing": [
        "hero_headline", "hero_subheadline",
        "fabric_title", "fabric_body",
        "whats_special", "benefits",
        "emotional_reassurance", "faq",
    ],
    "shoes": ["benefits", "faq"],
    "accessories": ["hero_headline"],
}


# ── Anomaly Registry ──────────────────────────────────────────────────────────

def load_anomaly_pids() -> set[str]:
    """Extract PIDs from the Known Anomalies Registry markdown file."""
    if not ANOMALY_REGISTRY_PATH.exists():
        return set()
    text = ANOMALY_REGISTRY_PATH.read_text(encoding="utf-8")
    # PIDs appear as `9881362759993` in the markdown
    return set(re.findall(r"`(\d{10,})`", text))


# ── Individual Checks ─────────────────────────────────────────────────────────

def check_empty_publisher_values(pid: str, pub_data: dict) -> dict:
    """Fail if required metafields are empty/null/empty-list."""
    product_type = pub_data.get("product_template_type", "")
    metafields   = pub_data.get("metafields", {})
    required     = _REQUIRED_METAFIELDS.get(product_type, [])

    empty = [
        field for field in required
        if not metafields.get(field)  # catches None, "", [], {}
    ]

    if empty:
        return {
            "check": "empty_publisher_values",
            "status": "FAIL",
            "fail_reason": f"Empty required metafields for type '{product_type}': {empty}",
        }
    return {"check": "empty_publisher_values", "status": "PASS"}


def check_duplicate_content_keys(pid: str, pub_data: dict) -> dict:
    """Fail if benefits titles or FAQ questions contain duplicates."""
    metafields = pub_data.get("metafields", {})

    # Benefits titles
    benefits = metafields.get("benefits", [])
    if isinstance(benefits, list):
        titles = [b.get("title", "") for b in benefits if isinstance(b, dict)]
        dupes  = [t for t in set(titles) if titles.count(t) > 1]
        if dupes:
            return {
                "check": "duplicate_content_keys",
                "status": "FAIL",
                "fail_reason": f"Duplicate benefit titles: {dupes}",
            }

    # FAQ questions
    faq = metafields.get("faq", [])
    if isinstance(faq, list):
        questions = [q.get("question", "") for q in faq if isinstance(q, dict)]
        dupes     = [q for q in set(questions) if questions.count(q) > 1]
        if dupes:
            return {
                "check": "duplicate_content_keys",
                "status": "FAIL",
                "fail_reason": f"Duplicate FAQ questions: {dupes}",
            }

    return {"check": "duplicate_content_keys", "status": "PASS"}


def check_bundle_duplicate_pids(pid: str, batch_pids: list[str]) -> dict:
    """Fail if this PID appears more than once in the batch."""
    count = batch_pids.count(pid)
    if count > 1:
        return {
            "check": "bundle_duplicate_pids",
            "status": "FAIL",
            "fail_reason": f"PID {pid} appears {count} times in batch — must be unique",
        }
    return {"check": "bundle_duplicate_pids", "status": "PASS"}


def check_anomaly_exclusion(pid: str) -> dict:
    """Fail if PID is listed in Known Anomalies Registry."""
    anomaly_pids = load_anomaly_pids()
    if pid in anomaly_pids:
        return {
            "check": "anomaly_exclusion",
            "status": "FAIL",
            "fail_reason": (
                f"PID {pid} is in Known Anomalies Registry — "
                "excluded from bundle until explicit management decision"
            ),
        }
    return {"check": "anomaly_exclusion", "status": "PASS"}


# ── Main Gate Runner ──────────────────────────────────────────────────────────

def run_gate1_extended(
    pid: str,
    pub_data: dict,
    batch_pids: list[str] | None = None,
    save_result: bool = True,
) -> dict:
    """
    Run all Gate 1 extended checks.
    Returns gate1_result dict.
    If save_result=True, writes {pid}_gate1_result.json.
    """
    checks: list[dict] = []

    checks.append(check_empty_publisher_values(pid, pub_data))
    checks.append(check_duplicate_content_keys(pid, pub_data))
    checks.append(check_anomaly_exclusion(pid))

    if batch_pids is not None:
        checks.append(check_bundle_duplicate_pids(pid, batch_pids))

    failed = [c for c in checks if c["status"] == "FAIL"]

    result = {
        "product_id": pid,
        "gate": "gate1_extended",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "FAIL" if failed else "PASS",
        "structure_signature": len(failed) == 0,
        "check_results": {c["check"]: c["status"] for c in checks},
        "fail_reasons": [
            {"check": c["check"], "detail": c["fail_reason"]}
            for c in failed
        ],
    }

    if save_result:
        out_path = STAGE_OUT_DIR / f"{pid}_gate1_result.json"
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    return result


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gate 1 Extended — Structure Hardening")
    parser.add_argument("pid", help="Product ID")
    parser.add_argument(
        "--batch-pids",
        help="Comma-separated list of all PIDs in batch (for duplicate check)",
        default="",
    )
    args = parser.parse_args()

    pub_path = STAGE_OUT_DIR / f"{args.pid}_publisher.json"
    if not pub_path.exists():
        print(f"[GATE1] ERROR: publisher.json not found for {args.pid}")
        sys.exit(1)

    pub_data   = json.loads(pub_path.read_text(encoding="utf-8"))
    batch_pids = [p.strip() for p in args.batch_pids.split(",") if p.strip()] or None

    result = run_gate1_extended(args.pid, pub_data, batch_pids)

    symbol = "✓" if result["status"] == "PASS" else "✗"
    print(f"[GATE1] {symbol} {args.pid} — {result['status']}")
    for fr in result.get("fail_reasons", []):
        print(f"  FAIL [{fr['check']}]: {fr['detail']}")

    sys.exit(0 if result["status"] == "PASS" else 1)
