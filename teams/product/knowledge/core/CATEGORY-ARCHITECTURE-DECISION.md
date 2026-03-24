# BabyMania — Category Architecture Decision
**Version:** 1.0
**Date:** 2026-03-23
**Status:** ACTIVE

---

## 1. CORE SYSTEM

### Shared Rules

- All runs execute through `00-team-lead/orchestrator.py` only — no direct script runs
- `config.yaml` is the single source of truth for required metafields and pipeline configuration
- `settings.py` is the single source of truth for template sections and section→metafield mapping
- Every product passes through the same stage sequence: fetch → analyze → think → write → validate → publish → verify
- Push is blocked unless all required files exist and validator contains `STATUS: PASS`

### Shared Validation Principles

- Content is invalid if it uses words not sourced from `description_raw` or `fabric_type` (see `content_rules.blocked_if_not_in_source`)
- Brand voice violations always fail — no exceptions, no category overrides
- Forbidden words: "מושלם", "הכי טוב", "תינוקכם", "מעוצב בקפידה", "נבחר בקפידה", "מביא לכם את הטוב ביותר"
- Sentence length cap: 12 words per sentence across all categories
- Language: Hebrew only (except emoji, °C, kg, cm, brand names)
- No template language in output: block, section, template, Liquid

### Shared Output Rules

- Publisher (stage 07) produces a single `_publisher.json` with a `metafields` top-level key — V2 format only
- `body_html` is always cleared at push — no category exception
- Metafields are always written to namespace `baby_mania`
- Publisher is a serializer only — it never rewrites, shortens, or improves content

### Shared Checkpoint Structure

| Checkpoint | File | Blocks push if missing |
|---|---|---|
| Context | `{pid}.yaml` | YES |
| Thinking | `{pid}_thinking.yaml` | YES |
| Validator | `{pid}_validator.txt` | YES |
| Publisher | `{pid}_publisher.json` | YES |
| Validator pass | `STATUS: PASS` in validator | YES |
| Thinking pass | `Stage 2 result: PASS` in validator | YES |
| Staleness | `edited.txt` newer than `validator.txt` | YES (if edited.txt exists) |
| Page validator | `{pid}_page_validator.json` → status FAIL | YES (if file exists) |

---

## 2. THINKING LAYER

### What Thinking Agents Decide

- Which content angle (cluster) belongs to each section — `owns`
- Which content angle is forbidden for each section — `forbidden`
- The intended message direction per section — `message`
- This assignment is set once per product and cannot be overridden by writing agents

### What Thinking Agents Must Output

`{pid}_thinking.yaml` with a `message_budget` block structured as:

```yaml
message_budget:
  fabric_body:
    owns: <cluster_name>
    forbidden: <cluster_name>
    message: <single line of intent>
  benefits:
    owns: <cluster_name>
    forbidden: <cluster_name>
    message: <single line of intent>
  # ... one entry per writing section
```

### What Thinking Agents Must Never Do

- Write final content
- Produce metafield-ready text
- Skip any section in `message_budget`
- Assign the same cluster to two different sections
- Run if `_thinking.yaml` already exists from a previous valid run (unless explicitly reset)

---

## 3. WRITING LAYER

### What Writing Agents Do

Each agent owns one section and produces a flat text file:

| Agent | Stage | Output file | Section owned |
|---|---|---|---|
| fabric-story-writer | 02 | `{pid}_fabric_story.txt` | fabric + hero + whats_special |
| benefits-generator | 03 | `{pid}_benefits.txt` | benefits + emotional_reassurance |
| faq-builder | 04 | `{pid}_faq.txt` | faq |
| care-instructions | 05 | `{pid}_care.txt` | care_instructions |

Stages 02–05 run in parallel after thinking (stage 02b) completes.

### What Writing Agents Receive from Thinking

- `owns` — the cluster they are permitted to write from
- `forbidden` — content territory they must not enter, even indirectly
- `message` — the intended direction, used as a starting point only

If `_thinking.yaml` is absent: agent must stop and output `THINKING_LAYER_MISSING`.

### What Writing Agents Must Never Re-decide

- Which angle the product leads with — decided by thinking
- Which section owns a given benefit or pain point — decided by thinking
- Fabric composition facts not in the source — always sourced from `fabric_type` or `description_raw`
- Gender attribution — only from `gender_signal` in `_intelligence.json`

---

## 4. CATEGORY ADAPTATION

### Clothing

| Property | Value |
|---|---|
| Template suffix | `clothing` |
| Thinking agent | `02b-clothing-thinking.md` |
| Unique sections | `bm-store-fabric`, `bm-store-hero`, `bm-store-sizes` |
| Size chart | Israeli standard (0-3M → 2-3Y) defined in `config/settings.py` |
| Fabric sourcing | `fabric_type` field or reclassified from title/description |
| Care icons | Constrained to allowed set in `config.yaml` — `wash_60`, `sun_dry`, `iron`, `no_bleach`, `repeat`, `no_tumble_dry`, `hand_wash` |
| Care fallback | If `fabric_type` is empty → `hand_wash` only, no `wash_60` |
| FAQ protection | `faq` metafield is write-protected by default unless `faq_overwrite: true` in context |

### Shoes

| Property | Value |
|---|---|
| Template suffix | `shoes` |
| Unique sections | Material/construction focus instead of fabric |
| No fabric stage | Stage 02 does not apply — no `fabric_story.txt` required |
| Size chart | Different from clothing — shoe sizing applies |

### Accessories

| Property | Value |
|---|---|
| Template suffix | `accessories` |
| Unique sections | Simplified — no fabric, no size guide |
| Thinking scope | Narrower `message_budget` — fewer sections to assign |

> **Rule:** When adding a new category, define its thinking agent first. Writing agents do not run until a thinking agent and its `_thinking.yaml` contract are in place.

---

## 5. VALIDATION LAYER

### What Remains Common Across All Categories

| Check | Rule |
|---|---|
| `STATUS: PASS` | Required in every `_validator.txt` |
| `Stage 2 result: PASS` | Required — confirms thinking layer was executed |
| Forbidden words | Same blocklist for all categories |
| Brand voice | Same rules for all categories |
| Sentence length | 12-word cap — all categories |
| Language | Hebrew only — all categories |
| No template language | All categories |
| Publisher format | V2 `metafields` key required — all categories |

### What Becomes Category-Specific

| Check | Clothing | Shoes | Accessories |
|---|---|---|---|
| Fabric sourcing (F01) | Required — `fabric_type` or hint | Not applicable | Not applicable |
| Care icon constraint (F02) | Enforced — `hand_wash` fallback if fabric unknown | Different set | Not applicable |
| Intelligence rules (I01–I05) | Enforced — no generic fabric phrases | Different rules | TBD |
| Gender guard (G01) | Enforced — `gender_signal` required before any gender content | Enforced | Enforced |
| Care positive format | Required — all care cards must be benefits, not restrictions | Not applicable | Not applicable |
| Size chart validation | From Israeli standard | From shoe sizing | Not applicable |

### Validation Execution Order

```
Stage 06 validator  →  content validation (common + category checks)
Stage 09 page-validator  →  cross-section coherence (blocks push if FAIL)
Orchestrator push preflight  →  file presence + staleness + Stage 2 guard
Orchestrator verify  →  live Shopify metafield count + body_html empty
```

No stage can be skipped. A product is not published unless all four pass.

---

## Decision Log

| Date | Decision | Reason |
|---|---|---|
| 2026-03-23 | Created this document | Clothing rollout completed; system needs documented architecture before next category rollout |
| 2026-03-23 | `settings.py` cleaned — removed `bm-store-banner` from SECTION_METAFIELD_MAP, added `bm-store-hero`, updated `TEMPLATE_SECTIONS` to 12 sections | Audit revealed phantom mappings from original design |
| 2026-03-23 | `bm-store-fabric` metafield map corrected — `fabric_story` replaced with 5 real flat keys | `fabric_story` never existed in pipeline output |
| 2026-03-23 | `clothing-test` template renamed to `test-template` | Category-specific naming in test infrastructure was a structural risk |
