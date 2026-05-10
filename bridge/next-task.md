TASK: NIGHT RUN — Organic catch-up plan and draft production
TASK_ID: organic-night-catchup-20260510
APPROVAL_TIER: T2
LAYER: ORGANIC + AUTOMATION
SOURCE_ISSUE: https://github.com/eyalcohen555/baby-mania-agent/issues/4

MISSION MODE:
Run a controlled night workflow through Claude Code and Conductor.
This is NOT full automation.
This is one controlled plan run only.

BUSINESS GOAL:
BabyMania is about 4 days behind on organic work. Create a safe multi-stage organic catch-up workflow that can prepare new article drafts and reports overnight without touching live Shopify.

ABSOLUTE SAFETY RULES:
- DO NOT publish articles live.
- DO NOT write to Shopify.
- DO NOT modify Shopify navigation.
- DO NOT touch EasySleep / Tempio.
- DO NOT run full automation.
- DO NOT merge to main.
- DO NOT delete files.
- DO NOT use static SHOPIFY_ACCESS_TOKEN.
- If any step requires Shopify live write, publishing, or T3 approval: STOP and report AWAITING_AYAL_APPROVAL.

REQUIRED SOURCE FILES:
1. BABYMANIA-MASTER-PROMPT.md
2. docs/management/chat-to-automation-operating-protocol.md
3. docs/management/conductor-plan-format.md
4. docs/organic/מצב-הפרויקט-האורגני.md
5. docs/organic/organic-journal.md
6. GitHub Issue #4: BabyMania night execution plan - organic catch-up

FILES ALLOWED:
- plans/organic-night-catchup-001.yaml
- docs/organic/night-catchup-article-plan-*.md
- output/stage-outputs/**
- output/organic/**
- bridge/conductor-state.md
- bridge/conductor-log.md
- bridge/conductor-notify.md
- bridge/last-result.md

FILES FORBIDDEN:
- theme-live/**
- theme_assets/**
- sections/**
- snippets/**
- templates/**
- config/**
- scripts/** except if only reading existing organic QA scripts is required
- shopify_client.py
- bridge.py
- teams/team-lead/**
- any Shopify live data write

ACTION:

STEP 1 — STATE AUDIT
Read the required source files.
Confirm current organic state.
Confirm next open organic item.
Confirm what can safely run tonight.
Output:
CURRENT ORGANIC STATE
NEXT OPEN ITEM
BLOCKERS
SAFE_TO_CONTINUE: YES / NO

STEP 2 — CREATE CONDUCTOR PLAN
Create a valid Conductor YAML plan:
plans/organic-night-catchup-001.yaml

The plan MUST include:
- STAGE-0 ORGANIC STATE READ, type AUDIT, approval_tier T0
- STAGE-1 OPEN FIXES AUDIT, type AUDIT
- STAGE-2 ARTICLE_DRAFTS_ALLOWED decision, type LOGIC
- STAGE-3 SELECT NEXT ORGANIC TOPIC / HUB, type LOGIC or AUDIT
- STAGE-4 CREATE ARTICLE PRODUCTION PLAN, type FIX
- STAGE-5 GENERATE ARTICLE DRAFTS, type FIX, drafts only, max 4 articles
- STAGE-6 CONTENT QA, type RETEST
- STAGE-7 POST-RUN REPORT, type RETEST

The plan MUST include files_allowed, files_forbidden, expected_output, exit_conditions, fail_conditions, next_on_pass, next_on_fail for every stage.
The plan MUST NOT include any Shopify live write or live publish stage.

STEP 3 — DRY RUN
Run dry-run only:
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe teams/team-lead/conductor.py plans/organic-night-catchup-001.yaml --dry-run

If dry-run fails: STOP and report.

STEP 4 — CONTROLLED REAL RUN
Only if dry-run PASS and bridge precheck is safe, run the plan once:
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe teams/team-lead/conductor.py plans/organic-night-catchup-001.yaml

Precheck required before running:
- current branch is main
- bridge.py running single instance with real Python path
- telegram_bot.py running
- watchdog.py running
- bridge/status.md is idle/done and not running
- bridge/next-task.md has been consumed or safe according to bridge runtime rules
- conductor-state is not RUNNING and not BLOCKED

If precheck fails: DO NOT RUN. Report PRECHECK_FAILED.

STEP 5 — MORNING REPORT
Create a clear Hebrew morning report in last-result.md including:
- PLAN_CREATED: YES / NO
- DRY_RUN: PASS / FAIL / NOT_RUN
- REAL_RUN: PASS / FAIL / BLOCKED / NOT_RUN
- ARTICLE_DRAFTS_CREATED: number
- ARTICLE_TITLES
- QA_RESULT per article
- FILES_CREATED
- FILES_MODIFIED
- SHOPIFY_WRITE: NO
- LIVE_PUBLISH: NO
- NEEDS_AYAL_APPROVAL: YES / NO
- NEXT_STEP_FOR_AYAL

SUCCESS CONDITIONS:
- plan YAML created and valid
- dry-run PASS before any real run
- real run only if precheck PASS
- no Shopify write
- no live publish
- no EasySleep/Tempio touch
- max 4 article drafts
- QA report produced
- morning report clear

FAIL CONDITIONS:
- organic state unclear
- plan YAML invalid
- dry-run fails
- bridge/conductor precheck unsafe
- any live Shopify action needed
- article pipeline requires missing data
- risk of touching forbidden files

FINAL OUTPUT FORMAT:
STAGE_VERDICT: PASS / FAIL / AWAITING_APPROVAL
SUMMARY:
PLAN_FILE:
DRY_RUN_RESULT:
REAL_RUN_RESULT:
ARTICLE_DRAFTS_CREATED:
QA_RESULT:
FILES_CREATED:
FILES_MODIFIED:
SHOPIFY_WRITE: NO
LIVE_PUBLISH: NO
NEXT_STEP_FOR_AYAL:
