#!/usr/bin/env python3
"""
submit_gsc.py — Google Search Console URL Status Checker
BabyMania post-publish step: run after publish + verify for new articles.

IMPORTANT — API LIMITATION:
    Google does not provide a programmatic API to "request indexing" for
    regular web pages. The URL Inspection API is inspect-only.
    To request indexing, use GSC UI:
        GSC → URL Inspection → paste URL → "Request Indexing"

What this script does:
    Checks the current indexing status of each URL via the
    Search Console URL Inspection API (correct API for blog articles).

Usage:
    python scripts/submit_gsc.py <url> [<url2> ...]

Examples:
    python scripts/submit_gsc.py https://babymania-il.com/blogs/news/my-article

Output per URL:
    indexed             — URL is indexed by Google
    unknown             — URL is not yet known to Google (new content)
    crawled_not_indexed — Google crawled but did not index
    excluded            — excluded from index (noindex, redirect, etc.)
    error               — API error (details printed)

Credentials:
    Loaded from GSC_SERVICE_ACCOUNT_JSON in .env
    Service account: gsc-access@babymania-001.iam.gserviceaccount.com
    Scope: https://www.googleapis.com/auth/webmasters
    Property: https://www.babymania-il.com/ (siteOwner)

Note on www vs non-www:
    GSC property is registered as https://www.babymania-il.com/
    Shopify serves content on babymania-il.com (no www).
    This script normalizes URLs automatically.
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

CREDENTIALS_PATH = os.environ.get("GSC_SERVICE_ACCOUNT_JSON")
SCOPES = ["https://www.googleapis.com/auth/webmasters"]
SITE_URL = "https://www.babymania-il.com/"


def normalize_url(url):
    """Normalize URL to match the GSC property (www prefix)."""
    url = url.strip()
    if url.startswith("https://babymania-il.com/"):
        url = url.replace("https://babymania-il.com/", "https://www.babymania-il.com/", 1)
    if url.startswith("http://babymania-il.com/"):
        url = url.replace("http://babymania-il.com/", "https://www.babymania-il.com/", 1)
    return url


def get_service():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("ERROR: pip install google-auth google-api-python-client")
        sys.exit(1)

    if not CREDENTIALS_PATH:
        print("ERROR: GSC_SERVICE_ACCOUNT_JSON not set in .env")
        sys.exit(1)

    creds_path = Path(CREDENTIALS_PATH)
    if not creds_path.exists():
        print(f"ERROR: Credentials file not found: {creds_path}")
        sys.exit(1)

    credentials = service_account.Credentials.from_service_account_file(
        str(creds_path), scopes=SCOPES
    )
    service = build("searchconsole", "v1", credentials=credentials, cache_discovery=False)
    return service


def inspect_url(service, url):
    """
    Inspect a URL via Search Console URL Inspection API.
    Returns (status_str, detail_dict).
    """
    normalized = normalize_url(url)
    try:
        body = {"inspectionUrl": normalized, "siteUrl": SITE_URL}
        result = service.urlInspection().index().inspect(body=body).execute()
        ir = result.get("inspectionResult", {})
        index = ir.get("indexStatusResult", {})

        coverage   = index.get("coverageState", "")
        verdict    = index.get("verdict", "")
        last_crawl = index.get("lastCrawlTime", None)
        crawled_as = index.get("crawledAs", None)
        indexing_state = index.get("indexingState", "")

        detail = {
            "coverage": coverage,
            "verdict": verdict,
            "last_crawl": last_crawl,
            "crawled_as": crawled_as,
            "indexing_state": indexing_state,
            "normalized_url": normalized,
        }

        # Map GSC verdicts to our status strings
        if verdict == "PASS":
            return "indexed", detail
        elif "unknown" in coverage.lower():
            return "unknown", detail
        elif "crawled" in coverage.lower() and verdict != "PASS":
            return "crawled_not_indexed", detail
        elif verdict == "FAIL":
            return "excluded", detail
        else:
            return f"neutral:{coverage}", detail

    except Exception as e:
        error_str = str(e)
        if hasattr(e, "resp"):
            status_code = int(e.resp.status)
            if status_code == 403:
                return "inspection_failed", {"msg": "403 — not authorized for this property"}
            if status_code == 400:
                return "inspection_failed", {"msg": f"400 — {error_str[:150]}"}
        return "inspection_failed", {"msg": error_str[:200]}


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/submit_gsc.py <url> [<url2> ...]")
        sys.exit(1)

    urls = sys.argv[1:]
    service = get_service()

    print(f"\nGSC URL INSPECTION -- {len(urls)} URL(s)")
    print(f"Property: {SITE_URL}")
    print("=" * 70)

    results = []
    for url in urls:
        status, detail = inspect_url(service, url)
        results.append({"url": url, "status": status, "detail": detail})

        icon = "OK" if status == "indexed" else ("??" if "unknown" in status else "!!")
        print(f"  {icon} {status:<25} {url}")
        if isinstance(detail, dict) and "msg" not in detail:
            print(f"     coverage:    {detail.get('coverage','')}")
            print(f"     last_crawl:  {detail.get('last_crawl') or 'never'}")
            print(f"     crawled_as:  {detail.get('crawled_as') or 'not yet'}")
        elif isinstance(detail, dict) and "msg" in detail:
            print(f"     detail: {detail['msg']}")
        print()

    print("=" * 70)
    indexed = sum(1 for r in results if r["status"] == "indexed")
    unknown = sum(1 for r in results if "unknown" in r["status"])
    failed  = sum(1 for r in results if r["status"] == "inspection_failed")
    other   = len(results) - indexed - unknown - failed
    print(f"  indexed: {indexed}  |  unknown/new: {unknown}  |  failed: {failed}  |  other: {other}")
    print()

    # Action guidance
    not_indexed = [r for r in results if r["status"] != "indexed"]
    if not_indexed:
        print("ACTION REQUIRED — URLs not yet indexed:")
        print("  GSC UI: https://search.google.com/search-console/inspect")
        print("  For each URL below: paste URL -> click 'Request Indexing'")
        for r in not_indexed:
            print(f"    {r['url']}", flush=True)
        print()

    # Machine-readable
    for r in results:
        print(f"RESULT:{r['status']}:{r['url']}")


if __name__ == "__main__":
    main()
