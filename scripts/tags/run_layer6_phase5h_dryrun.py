"""
Layer 6 — Phase 5h Dry Run
CAT-B pivot: age → size. DRY RUN ONLY — no Shopify writes.
Overrides output paths from run_layer6_phase5d_rerun (which carries all Phase 5f fixes + size pivot).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import run_layer6_phase5d_rerun as r

r.OUT_SAMPLE        = "output/tags/phase5h-size-taxonomy-sample-58.json"
r.OUT_REPORT_JSON   = "output/tags/phase5h-size-taxonomy-dryrun-report.json"
r.OUT_REPORT_MD     = "output/tags/phase5h-size-taxonomy-dryrun-report.md"
r.OUT_COMPARISON_MD = "output/tags/phase5h-size-taxonomy-comparison.md"

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "..", ".."))
    r.main()
