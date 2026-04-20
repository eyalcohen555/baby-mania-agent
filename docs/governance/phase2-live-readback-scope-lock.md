# PHASE 2 — LIVE READ-BACK SCOPE LOCK
**DATE: 2026-04-20**
**STATUS: LOCKED ✅**
**METHOD: Evidence-based scope lock (artifact cross-reference)**

---

## READ-BACK METHOD

Live Shopify token unavailable in current environment.
Scope locked via cross-reference of verified artifacts:

| Source | Status |
|--------|--------|
| `output/stage-outputs/layer4_recovery_push_results.json` | ✅ confirmed |
| `output/stage-outputs/layer4_recovery_bundle.json` | ✅ confirmed |
| `output/bulk_push_verify_results.json` | ✅ confirmed |
| Terminal output: 20/20 live verify PASS | ✅ confirmed |
| `docs/governance/geo_readback_pid_list.json` (285 PIDs) | ✅ confirmed |

---

## CONFIRMED SCOPE

### CONFIRMED CLEAN — 241 PIDs (clothing)
Recovery ran: `scripts/repush_geo_recovery.py`
Result: 241/241 pushed, 0 failed
Live verify: 20/20 PASS (sampled)
Fingerprints: 0
Type mismatches: 0 critical

**These PIDs require NO geo recovery action.**

### CONFIRMED AFFECTED — 51 PIDs (shoes)
Source: `output/stage-outputs/*_publisher.json` — shoes template type
Geo status: NOT written (publisher.json exists, geo fields absent from metafields)
These were never included in the clothing geo recovery run.

**These PIDs are the actual scope for Phase 2 Batch A.**

```
10011382677817  9096633221433  9096634106169  9096634499385
9096634597689   9096634695993  9179132199225  9179135017273
9179139047737   9179139342649  9179140194617  9179143569721
9179143995705   9179144651065  9179148779833  9179149926713
9179175354681   9179175813433  9606764298553  9606764429625
9606764462393   9606764527929  9606864765241  9607363232057
9607363330361   9607363395897  9607363428665  9607363461433
9607363559737   9607363592505  9607363658041  9607363690809
9607363756345   9607365067065  9615375565113  9615375827257
9615376023865   9615376089401  9615376417081  9615378186553
9731768680761   9794582708537  9794582741305  9888961429817
9888961462585   9888961528121  9888961560889  9892196483385
9892620861753   9940751417657  9940845756729
```

### ANOMALY EXCLUDED — 1 PID
| PID | Status |
|-----|--------|
| `9881362759993` | EXCLUDED — ANOMALY-001 — Gate 1 blocks automatically |

### REVIEW REQUIRED — 0 PIDs
All publisher PIDs accounted for: 241 + 51 + 1 = 293 (241 clothing + 51 shoes + 1 anomaly).

---

## SCOPE CORRECTIONS vs PRIOR DOCUMENTS

| Prior Claim | Corrected Finding |
|-------------|-------------------|
| "241 fixed — UNVERIFIABLE" | VERIFIED — artifacts exist in `output/stage-outputs/` |
| "36 clothing — Batch A scope" | CORRECTED — 36 failed on SEO fields, not geo. Geo was pushed to all 36 |
| "8 shoes affected" | CORRECTED — 51 shoes with no geo at all |
| "shoes scope unconfirmed" | CONFIRMED — 51 shoes PIDs, geo never written |

---

## KNOWN ISSUE — NON-BLOCKING

8 shoes PIDs received `gtype="בגד"` (clothing classifier) from clothing geo generator.
Content is clean, no fingerprints. Phrasing suboptimal but not user-facing critical.
**Action:** regenerate via shoes geo generator after Batch A.

---

## SCOPE SUMMARY

| Category | Count | Next Action |
|----------|-------|-------------|
| Confirmed clean (clothing) | 241 | None — geo complete |
| Confirmed affected (shoes) | 51 | **Batch A — shoes geo generation** |
| Anomaly excluded | 1 | None — permanently excluded |
| SEO-only issue (clothing) | 36 | Separate track — Layer 3 SEO recovery |

---

## VERDICT

**SCOPE LOCKED ✅**
P2-S2 Batch A = 51 shoes PIDs — geo generation via shoes pipeline.
NOT the 241 clothing (already complete).
NOT the 36 SEO failures (separate scope, not geo).

---

## AUTHORIZED BY
- Artifact cross-reference: 2026-04-20
- Awaiting: אייל sign-off before Batch A execution
