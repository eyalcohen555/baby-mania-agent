"""
Layer 6 — Phase 5k Dry Run
Size normalization fix: re.sub(r'\\s+', '', opt) collapses spaces ("0-3 M" → "0-3m").
DRY RUN ONLY — no Shopify writes.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import run_layer6_phase5d_rerun as r

r.OUT_SAMPLE        = "output/tags/phase5k-size-normalization-sample-58.json"
r.OUT_REPORT_JSON   = "output/tags/phase5k-size-normalization-dryrun-report.json"
r.OUT_REPORT_MD     = "output/tags/phase5k-size-normalization-dryrun-report.md"
r.OUT_COMPARISON_MD = "output/tags/phase5k-size-normalization-comparison.md"

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "..", ".."))
    r.main()
