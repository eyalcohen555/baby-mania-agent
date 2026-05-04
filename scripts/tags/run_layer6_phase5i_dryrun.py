"""
Layer 6 — Phase 5i Dry Run
Variant-based size detection. DRY RUN ONLY — no Shopify writes.
Adds variants to Shopify fetch so extract_cat_b() can read size from option values.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import run_layer6_phase5d_rerun as r

r.OUT_SAMPLE        = "output/tags/phase5i-variant-size-sample-58.json"
r.OUT_REPORT_JSON   = "output/tags/phase5i-variant-size-dryrun-report.json"
r.OUT_REPORT_MD     = "output/tags/phase5i-variant-size-dryrun-report.md"
r.OUT_COMPARISON_MD = "output/tags/phase5i-variant-size-comparison.md"

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "..", ".."))
    r.main()
