plan_id: layer4-geo-priority-001
plan_file: plans/layer4-geo-priority-001.yaml
status: RUNNING
current_stage: STAGE-9
current_task_id: conductor-layer4-geo-priority-001-STAGE-9-20260416-132424
completed_stages:
- STAGE-1
- STAGE-2
- STAGE-3
- STAGE-4
- STAGE-5
- STAGE-6
- STAGE-7
- STAGE-8
failed_stages:
- STAGE-9
skipped_stages: []
blocked_reason: 'STAGE-9 FAIL: Clothing GEO drafts have systemic quality issues — template reuse, desc bleed, misclassification. Need regeneration before publish.'
waiting_for: 'Conductor decision: regenerate clothing GEO with stricter quality controls'
next_stage: STAGE-9-RETRY
overall_verdict: ''
interrupted_stage: ''
interrupted_at_batch: 0
interrupted_products_done: 0
resume_available: false
started_at: '2026-04-16 08:23:51'
updated_at: '2026-04-16 13:35:00'
recovery_note: 'STAGE-9 FAIL: 228/242 clothing GEO drafts validated. Critical issues: (1) 31.6% template phrase reuse across products, (2) 61% desc bleed in who_for, (3) 1 misclassified product (night light PID 9881362759993), (4) 2 season mismatches. Top repeated sentence appears 54x. Drafts need regeneration with product-specific content.'
