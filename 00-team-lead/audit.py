"""
BabyMania Team Lead — Audit Logger

Provides:
  - StageResult  : single stage execution record
  - ProductAudit : full per-product audit trail + structured report
  - AuditLogger  : run-level logger that owns all ProductAudits
"""

from __future__ import annotations

import io
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


# ── Helpers ───────────────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.now().isoformat()


def _duration_ms(start: datetime) -> int:
    return int((datetime.now() - start).total_seconds() * 1000)


# ── StageResult ───────────────────────────────────────────────────────────────

class StageResult:
    """Record of a single pipeline stage execution."""

    def __init__(
        self,
        stage: str,
        status: str,           # "pass" | "fail" | "skip" | "retry"
        duration_ms: int,
        error: Optional[str] = None,
        attempt: int = 1,
    ):
        self.stage        = stage
        self.status       = status
        self.duration_ms  = duration_ms
        self.error        = error
        self.attempt      = attempt
        self.timestamp    = _now_iso()

    def to_dict(self) -> dict:
        return {
            "stage":       self.stage,
            "status":      self.status,
            "duration_ms": self.duration_ms,
            "attempt":     self.attempt,
            "error":       self.error,
            "timestamp":   self.timestamp,
        }


# ── ProductAudit ──────────────────────────────────────────────────────────────

class ProductAudit:
    """Full audit trail for a single product pipeline run."""

    def __init__(self, product_id: str, product_title: str, audit_dir: Path):
        self.product_id    = product_id
        self.product_title = product_title
        self.audit_dir     = audit_dir
        self.started_at    = _now_iso()
        self.stages: list[StageResult] = []
        self.final_state   = "created"
        self.final_status  = "pending"    # "success" | "failed" | "pending"
        self._stage_start: Optional[datetime] = None

    # ── Stage timing helpers ───────────────────────────────────────────────

    def begin_stage(self, stage: str) -> None:
        """Call at stage start to begin timing."""
        self._stage_start = datetime.now()

    def end_stage(
        self,
        stage: str,
        status: str,
        error: Optional[str] = None,
        attempt: int = 1,
    ) -> StageResult:
        """Call at stage end to record result."""
        duration = _duration_ms(self._stage_start) if self._stage_start else 0
        result = StageResult(stage, status, duration, error, attempt)
        self.stages.append(result)
        self._stage_start = None
        return result

    # ── State helpers ──────────────────────────────────────────────────────

    def set_state(self, state: str) -> None:
        self.final_state = state

    def finalize(self, state: str) -> None:
        self.final_state  = state
        self.final_status = "success" if state == "verified" else "failed"

    # ── Report ────────────────────────────────────────────────────────────

    def to_report(self) -> dict:
        total_ms    = sum(s.duration_ms for s in self.stages)
        pass_stages = [s.stage for s in self.stages if s.status == "pass"]
        fail_stages = [s.stage for s in self.stages if s.status == "fail"]
        return {
            "product_id":       self.product_id,
            "product_title":    self.product_title,
            "started_at":       self.started_at,
            "finished_at":      _now_iso(),
            "final_state":      self.final_state,
            "final_status":     self.final_status,
            "total_duration_ms": total_ms,
            "stages_passed":    pass_stages,
            "stages_failed":    fail_stages,
            "stages":           [s.to_dict() for s in self.stages],
        }

    def save(self) -> Path:
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        path = self.audit_dir / f"{self.product_id}_audit.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_report(), f, ensure_ascii=False, indent=2)
        return path

    def print_summary(self, log: logging.Logger) -> None:
        icon = "✓" if self.final_status == "success" else "✗"
        total_s = sum(s.duration_ms for s in self.stages) / 1000
        log.info(
            "%s %s [%s] | state=%s | %.1fs",
            icon,
            self.product_title,
            self.product_id,
            self.final_state,
            total_s,
        )
        for s in self.stages:
            marker = "  ✓" if s.status == "pass" else "  ✗"
            err = f" — {s.error}" if s.error else ""
            log.info("%s %-20s %dms%s", marker, s.stage, s.duration_ms, err)


# ── AuditLogger ───────────────────────────────────────────────────────────────

class AuditLogger:
    """
    Run-level logger.

    Owns all ProductAudit instances for the current pipeline run.
    Saves a structured run_report JSON at the end.
    """

    def __init__(self, logs_dir: Path, run_id: str):
        self.logs_dir      = logs_dir
        self.run_id        = run_id
        self.run_started   = _now_iso()
        self.products: list[ProductAudit] = []

        logs_dir.mkdir(parents=True, exist_ok=True)

        # Force UTF-8 on Windows stdout
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        elif hasattr(sys.stdout, "buffer"):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

        log_file = logs_dir / f"teamlead_{run_id}.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )
        self.log = logging.getLogger("bm-team-lead")
        self.log.info("=" * 60)
        self.log.info("BabyMania Team Lead  |  run_id=%s", run_id)
        self.log.info("=" * 60)

    # ── Per-product audit ──────────────────────────────────────────────────

    def new_product(
        self,
        product_id: str,
        product_title: str,
        audit_dir: Optional[Path] = None,
    ) -> ProductAudit:
        if audit_dir is None:
            audit_dir = self.logs_dir / "audits"
        audit = ProductAudit(product_id, product_title, audit_dir)
        self.products.append(audit)
        self.log.info("━" * 60)
        self.log.info("Product: %s  [%s]", product_title, product_id)
        return audit

    # ── Run report ────────────────────────────────────────────────────────

    def save_run_report(self) -> Path:
        passed  = [p for p in self.products if p.final_status == "success"]
        failed  = [p for p in self.products if p.final_status == "failed"]
        pending = [p for p in self.products if p.final_status == "pending"]

        report = {
            "run_id":       self.run_id,
            "started_at":   self.run_started,
            "finished_at":  _now_iso(),
            "summary": {
                "total":   len(self.products),
                "passed":  len(passed),
                "failed":  len(failed),
                "pending": len(pending),
            },
            "passed_products":  [p.product_id for p in passed],
            "failed_products":  [p.product_id for p in failed],
            "products":         [p.to_report() for p in self.products],
        }

        path = self.logs_dir / f"run_report_{self.run_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        self.log.info("=" * 60)
        self.log.info(
            "RUN COMPLETE | passed=%d  failed=%d  pending=%d",
            len(passed), len(failed), len(pending),
        )
        self.log.info("Report: %s", path)
        return path
