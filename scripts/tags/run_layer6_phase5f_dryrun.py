"""
Layer 6 — Phase 5f Dry Run
Phase 5f logic hardening. DRY RUN ONLY — no Shopify writes.
Overrides output paths from run_layer6_phase5d_rerun (which carries all 7 bug fixes).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import run_layer6_phase5d_rerun as r

# Override output paths for Phase 5f
r.OUT_SAMPLE        = "output/tags/phase5f-rerun-sample-59.json"
r.OUT_REPORT_JSON   = "output/tags/phase5f-logic-hardening-report.json"
r.OUT_REPORT_MD     = "output/tags/phase5f-logic-hardening-report.md"
r.OUT_COMPARISON_MD = "output/tags/phase5f-comparison.md"

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "..", ".."))
    r.main()
