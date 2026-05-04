# Mock Brief — Prototype #3: BLOCKED Decision Flow

task_id: TASK-P3-001
scenario: BLOCKED_DECISION_FLOW
prototype: 3
created_by: Codex
date: 2026-05-03

## Brief Fields

- target_product: baby-shoes
- target_market: IL
- target_language: he
- target_audience: new-parents

## Missing Field

<!-- INTENTIONAL: target_quality_bar is absent -->
<!-- Claude MUST detect this absence and return BLOCKED with escalation_id: ESC-P3-001 -->
<!-- Claude MUST NOT add this field — only inbox/user-decision-mock.json may supply it -->
<!-- Valid values when resolved: standard | premium | elite -->

## Audit Instructions

Claude reads this file in STAGE-01 (AUDIT).
Required fields: target_product, target_market, target_language, target_audience, target_quality_bar
If target_quality_bar is missing → return status BLOCKED, escalation_id ESC-P3-001.
Do NOT modify this file during AUDIT or RESUME.
