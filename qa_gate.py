"""
qa_gate.py — Agent 10 QA Hard Gate
------------------------------------
Validates that every article has a passing QA file
before allowing it to be published to Shopify.

Usage:
    from qa_gate import preflight_qa_check, check_article_qa

Both functions raise SystemExit on failure — the script
stops immediately, nothing is published.
"""

import json
import sys
from pathlib import Path


def _qa_filepath(hub_dir: Path, article_file: str) -> Path:
    """
    Derive QA file path from article filename.

    Convention:
        HUB6_Pillar_blog_article.html
        → HUB6_Pillar_internal_link_validation.json
    """
    qa_filename = article_file.replace("_blog_article.html", "_internal_link_validation.json")
    return hub_dir / qa_filename


def check_article_qa(hub_dir: Path, article_def: dict) -> None:
    """
    Check QA gate for a single article.
    Raises SystemExit if:
      - QA file does not exist
      - overall_result != "PASS"

    Called once per article immediately before the Shopify API call.
    """
    article_file = article_def["file"]
    cluster_id = article_def["cluster_id"]
    qa_path = _qa_filepath(hub_dir, article_file)

    # Gate 1 — file must exist
    if not qa_path.exists():
        print(f"\n  [BLOCKED] BLOCKED: QA file missing")
        print(f"  Expected: {qa_path}")
        print(f"  Run Agent 10 on {article_file} before publishing.")
        sys.exit(1)

    # Gate 2 — result must be PASS
    try:
        qa_data = json.loads(qa_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"\n  [BLOCKED] BLOCKED: QA file unreadable — {e}")
        print(f"  File: {qa_path}")
        sys.exit(1)

    result = qa_data.get("overall_result", "UNKNOWN")

    if result != "PASS":
        failures = qa_data.get("failures", [])
        warnings = qa_data.get("warnings", [])
        print(f"\n  [BLOCKED] BLOCKED: QA FAIL — {cluster_id}")
        print(f"  QA result: {result}")
        if failures:
            print(f"  Failures:")
            for f in failures:
                print(f"    • {f}")
        if warnings:
            print(f"  Warnings:")
            for w in warnings:
                print(f"    • {w}")
        print(f"  Fix the issues above and re-run Agent 10 before publishing.")
        sys.exit(1)


def preflight_qa_check(hub_dir: Path, articles: list, hub_name: str) -> None:
    """
    Pre-flight: validate ALL articles before publishing ANY.

    Checks every QA file upfront so a failure on article 4
    doesn't leave articles 1–3 published without their cluster.

    Raises SystemExit on the first failure found.
    Prints a full summary before aborting.
    """
    print(f"\n{'─'*60}")
    print(f"QA PRE-FLIGHT — {hub_name} ({len(articles)} articles)")
    print(f"{'─'*60}")

    failed = []
    missing = []
    passed = []

    for article in articles:
        article_file = article["file"]
        cluster_id = article["cluster_id"]
        qa_path = _qa_filepath(hub_dir, article_file)

        if not qa_path.exists():
            missing.append((cluster_id, str(qa_path)))
            continue

        try:
            qa_data = json.loads(qa_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            missing.append((cluster_id, f"unreadable: {e}"))
            continue

        result = qa_data.get("overall_result", "UNKNOWN")
        if result == "PASS":
            passed.append(cluster_id)
            print(f"  [PASS] {cluster_id}")
        else:
            failures = qa_data.get("failures", [])
            failed.append((cluster_id, result, failures))
            failure_summary = "; ".join(failures[:2]) if failures else "no details"
            print(f"  [FAIL] {cluster_id} — {result} — {failure_summary}")

    # Report missing
    for cluster_id, path in missing:
        print(f"  [MISS] {cluster_id} — QA file not found: {path}")

    total_blocked = len(failed) + len(missing)

    print(f"{'─'*60}")
    print(f"Pre-flight result: {len(passed)} PASS  |  {len(failed)} FAIL  |  {len(missing)} MISSING")

    if total_blocked > 0:
        print(f"\n[BLOCKED] BLOCKED: {total_blocked} article(s) did not pass QA.")
        print("Nothing will be published. Fix all failures and re-run Agent 10.")
        print(f"{'─'*60}\n")
        sys.exit(1)

    print(f"All {len(passed)} articles passed QA. Proceeding to publish.")
    print(f"{'─'*60}\n")
