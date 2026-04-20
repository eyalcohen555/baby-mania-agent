# PHASE 2 SCOPE CONFIRMATION
**P2-S1 — Final Affected Scope Confirmation Before Live Recovery**
**DATE: 2026-04-19**
**STATUS: PARTIAL — Shopify live read-back required before Batch A**

---

## PHASE 1 PREREQUISITE

Phase 1 Closure Declaration: `docs/governance/phase1-closure-declaration.md`
- VERDICT: PASS ✓
- Authorized by: אייל ✓
- Gates 1 + 2 active ✓
- Phase 2 may proceed ✓

---

## CONFIRMED SCOPE (from local evidence)

### Anomaly Exclusion — CONFIRMED
| PID | Status |
|-----|--------|
| `9881362759993` | EXCLUDED — not in push_success, push_failed, or verify_failed. Not in any recovery batch. Gate 1 anomaly_exclusion blocks automatically. |

### Confirmed verify_failed — 36 clothing PIDs
Source: `output/bulk_push_verify_results.json`
All 36 confirmed type=clothing via publisher.json.

```
9179173617977  9688976326969  9678573240633  9688660377913
9096606810425  9096607301945  9179155693881  9717957525817
9606694043961  9096606974265  9179158217017  9719189635385
9688670110009  9179172733241  9096599994681  9179133870393
9873511022905  9179170799929  9688964989241  9687596663097
9858268430649  9096607138105  9895864435001  10011383103801
9605887754553  9874906513721  9858268496185  9179138687289
9179152482617  9688674533689  9874906382649  9874906349881
9605887787321  9673732194617  9724813443385  9688965087545
```

### PIDs with geo_draft but no publisher.json — 8 PIDs
Source: `output/stage-outputs/` (diff of geo_draft vs publisher sets)
These products were processed through Layer 4 geo but never produced publisher output.

```
10085913231673  9096628732217  9605709791545  9606864666937
9606864699705  9838580662585  9881362759993  9895864303929
```

Note: `9881362759993` is the anomaly PID — correctly excluded.
Remaining 7: **REVIEW REQUIRED** — unknown why publisher was not generated. Must not enter Batch A without investigation.

---

## SCOPE GAPS — REVIEW REQUIRED

### ⚠ CRITICAL: "241" count cannot be confirmed from local evidence

The conductor-state (`bridge/conductor-state.md`) and task-log contain:
```
"241 fixed, 0 fingerprints live, 0 type mismatches"
"RECOVERY: 241 PIDs regenerated+repushed. 0 fingerprints. 20/20 live verify PASS."
```

**This claim is UNVERIFIABLE** because:
1. `output/layer4-recovery/` — does NOT exist
2. `docs/qa/live-verify-layer4-recovery.md` — does NOT exist
3. `rollback/layer4-recovery/` — does NOT exist
4. The task-log entry (2026-04-19 12:18:18) was logged DURING Phase 1 hardening — before Gate 1 + Gate 2 existed
5. Stage 16 live verify (`output/stage16_live_verify_final.json`): 29/74 checked products FAILED (60.8% pass rate) — state is NOT clean

This is an instance of the same **False Success** failure mode the hardening plan was created to address.

### ⚠ Stage 16 live verify state
- Checked: 74 products
- PASS: 45 (60.8%)
- FAIL: 29 (39.2%)
- Issues: 22/43 bulk clothing missing SEO fields, 6/6 accessories missing SEO fields

### ⚠ Scope delta: "241" vs confirmed evidence
- Original plan scope: 233 clothing + 8 shoes = 241
- Confirmed verify_failed from local data: 36 clothing, 0 shoes
- Difference: 197 clothing unaccounted — live read-back required to determine current state
- Shoes: `shoes_pids[]` — CANNOT CONFIRM from local evidence. Zero shoes in verify_failed. Shoes template products (65 total in publisher) may be in different state than claimed.

---

## EXCLUDED PIDS
| PID | Reason | Source |
|-----|--------|--------|
| `9881362759993` | ANOMALY-001 — מנורת לילה להירדמות — Known Anomalies Registry | `docs/operations/known-anomalies-registry.md` |

This PID must not appear in any recovery batch. Gate 1 (`check_anomaly_exclusion`) will block it automatically. Verified: not present in any push list.

---

## SOURCE EVIDENCE
| File | Finding |
|------|---------|
| `output/bulk_push_verify_results.json` | 36 verify_failed clothing PIDs, 43 push_success, 0 push_failed |
| `output/stage16_live_verify_final.json` | 60.8% pass rate on 74 sampled products |
| `output/stage-outputs/` (diff) | 8 PIDs with geo_draft but no publisher |
| `bridge/conductor-state.md` | Claims "241 fixed" — NOT verifiable from artifacts |
| `bridge/task-log.md` (12:18:18) | Claims "241 regenerated+repushed" — NOT verifiable |
| `output/layer4-recovery/` | DOES NOT EXIST |
| `docs/qa/live-verify-layer4-recovery.md` | DOES NOT EXIST |

---

## VERDICT
**PARTIAL PASS — Batch A BLOCKED until Shopify live read-back**

### What IS confirmed:
- Anomaly PID `9881362759993`: EXCLUDED ✓
- 36 clothing verify_failed: confirmed scope for Batch A start ✓
- Gates 1 + 2: active and blocking ✓

---

## ⚠ SUPERSEDED — 2026-04-20

המסמך הזה הוחלף על ידי ממצאי ה-live read-back שבוצע ב-2026-04-20.

**תוצאות live read-back (2026-04-20):**
- 36 clothing verify_failed — נבדקו live → כולם CLEAN (title_tag + description_tag קיימים)
- 51 shoes — נבדקו live → כולם CLEAN (geo_who_for + geo_use_case קיימים)
- Batch A לא בוצע ולא נדרש
- failures היסטוריים היו RUNTIME בלבד (timeout/429) — לא evidence לבעיה data

**Source of truth עדכני:** `docs/governance/phase2-live-readback-scope-lock.md` (STATUS: COMPLETE)

### What requires resolution before Batch A:
1. **Shopify live read-back** on all publisher PIDs — determine actual live state of geo_who_for + geo_use_case fields
2. **Investigate 7 PIDs** with geo_draft but no publisher (excluding anomaly)
3. **Confirm or reject shoes scope** — 0 shoe verify_failed in local data contradicts "8 affected shoes" claim

---

## NEXT ALLOWED STEP

**P2-S2 (Batch A) is BLOCKED** until:
1. Shopify live read-back executed (read-only)
2. Scope confirmed as LOCKED by אייל
3. Shoes vs clothing split verified

Batch A should begin with the 36 confirmed verify_failed clothing PIDs only — not the claimed 241.
