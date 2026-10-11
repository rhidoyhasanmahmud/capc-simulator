# Thesis Experiment Evidence Log

## Purpose

This file is the durable research-evidence ledger for the CAPC MSc thesis. It records verified implementation, calibration, pilot, provenance, and later comparative-experiment evidence that may be used in Chapters 5, 6, and 7.

The log distinguishes implementation/verification evidence from performance findings. Entries must not be interpreted as CAPC performance conclusions unless they arise from the frozen comparative experiment and the predeclared analysis.

## Evidence-handling rule

- Preserve raw experiment directories and their `metadata.json`, `effective_config.yaml`, `trace.csv`, `transactions.csv`, `state_events.csv`, `decisions.csv`, `dispatch_snapshots.csv`, `summary.json`, and `queue_recovery.json` files.
- Record the executing Git commit and configuration hash for every final run.
- Do not delete or overwrite completed evidence directories; use a new output directory for reruns.
- Do not add, remove, or replace seeds after labelled comparative effects are inspected.
- Neutral-pilot and runtime-readiness evidence are not CAPC comparative performance findings.

---

## E1 — Chapter 5 implementation verification

Status: **PASS**

Evidence:

- Automated test suite: `31/31 PASS`.
- Deterministic Chapter 5 verification: `V1-V12 PASS`.
- Verified areas include trace reproducibility, cross-treatment trace equality, Static Atomic FIFO ordering, Diagnostic FIFO ordering, atomic lock exclusion, all-or-nothing lock release, multi-worker dispatch, CAPC score hand-check, aging monotonicity, transaction accounting, low-load sanity, and overload queue growth.

Interpretation: software/design verification only; not performance evidence.

---

## E2 — Runtime optimization and semantic-equivalence evidence

Implementation optimization commit:

`91fb476ac67d7755073a8a89a12273f69bc7f6b8`

Merged runtime-optimization main revision:

`e3e425b8ca8f868c42b26729133b9e0bf58ef147`

Validation evidence:

- Reference Static Atomic FIFO primary run before optimization: `44.26 s` wall time.
- Same reference run after optimization: `10.19 s` wall time.
- Approximate speed-up: `4.34x`.
- Approximate wall-time reduction: `77%`.
- Pre/post summary comparison: **PASS**, equivalent within `1e-12` tolerance.
- Representative high-contention Static Atomic FIFO readiness run: `14.70 s` wall time.
- Test suite after optimization: `31/31 PASS`.
- Verification after optimization: `V1-V12 PASS`.

Interpretation: engineering/readiness evidence. The optimizations were intended to change computational cost only, not workload, scheduler, locking, service, metric, or experimental semantics.

---

## E3 — Representative high-contention Static Atomic FIFO readiness run

Run identifier:

`sh4_x50_w2_static_atomic_fifo_seed001`

Recorded diagnostics:

- Measurement-window cross-shard transactions: `22,255`.
- Completed: `22,255`.
- Completed by cutoff: `22,253`.
- Unfinished at cutoff: `2`.
- Unfinished fraction: `0.000089867`.
- Throughput: `13.73642 tx/s`.
- Mean end-to-end latency: `0.2763495 s`.
- Median latency: `0.0884456 s`.
- p95 latency: `1.1048113 s`.
- p99 latency: `2.1626608 s`.
- Latency variability metric: `1.0163656 s`.
- Mean waiting time: `0.2263270 s`.
- p95 waiting time: `1.0526057 s`.
- Maximum waiting time: `4.1245440 s`.
- Mean service time: `0.0500225 s`.
- Mean queue length: `3.109185`.
- Maximum queue length: `77`.
- Final queue slope: `-0.0070049`.
- Worker utilization: `0.34357`.
- Jain index: `0.9999999919`.
- Mean queue-entry arrival rate: `17.5649 tx/s`.
- p95 queue-entry arrival rate: `33.4 tx/s`.
- Mean dependency degree: `2.20054`.
- Mean active-lock conflicts: `1.0833`.
- p95 active-lock conflicts: `2`.
- Dispatch snapshots: `42,008`.
- Candidate observations: `310,405`.
- Blocked candidate observations: `221,263`.
- Lock-block fraction: `0.7128203`.
- Dispatch snapshots with any block: `0.5527995`.
- Burst episodes: `29`.
- Evaluable recovery episodes: `8`.
- Recovered episodes: `8`.
- Recovery fraction: `1.0`.
- Queue stability: `true`.
- Trace hash prefix: `e0421fc3...`.
- Configuration hash prefix: `ce4c3dc...`.

Interpretation: runtime/readiness and contention diagnostic only; not a Chapter 6 comparative result.

---

## E4 — Neutral Static Atomic FIFO pilot

Output directory used locally:

`results/neutral_pilot_v1`

Execution:

- Scheduler: Static Atomic FIFO only.
- Seeds: `1-5`.
- Logical shards: `4, 8, 16`.
- Cross-shard ratios: `0.10, 0.30, 0.50`.
- Workers: `2, 4`.
- Total runs: `90`.
- Wall time: `850.83 s`.
- User CPU time: `780.57 s`.
- System CPU time: `48.95 s`.

Provenance audit:

- Metadata files: `90`.
- All pilot runs executed on Git commit: `e3e425b8ca8f868c42b26729133b9e0bf58ef147`.
- All schedulers in pilot metadata: `static_atomic_fifo`.
- Frozen-code provenance check: **PASS**.

Regime coverage:

- LOW: `16` runs.
- TRANSITIONAL: `54` runs.
- HIGH: `20` runs.
- `has_low = true`.
- `has_transitional = true`.
- `has_high = true`.
- `regime_coverage_pass = true`.

Mean regime diagnostics:

| Regime | Raw util. NORMAL | Raw util. BURST | Mean queue | Max queue | Lock-block fraction | Mean run p99 latency (s) |
|---|---:|---:|---:|---:|---:|---:|
| LOW | 0.0391 | 0.1172 | 0.0047 | 2.8125 | 0.0700 | 0.0940 |
| TRANSITIONAL | 0.1157 | 0.3472 | 0.3252 | 11.2593 | 0.3270 | 0.2949 |
| HIGH | 0.1625 | 0.4875 | 0.7840 | 20.3500 | 0.4943 | 0.5775 |

Interpretation: scheduler-neutral regime-coverage evidence. The p99 values are Static Atomic FIFO pilot diagnostics and are not CAPC comparative findings.

---

## E5 — Neutral normalization diagnostics

### Arrival-rate reference

Frozen candidate retained:

`lambda_ref = 30.0`

Observed queue-entry arrival-rate diagnostics:

| Regime | n | p50 | p95 | p99 | max | fraction >= 30 |
|---|---:|---:|---:|---:|---:|---:|
| LOW | 68,430 | 2.6 | 7.2 | 8.2 | 9.4 | 0.0000 |
| TRANSITIONAL | 743,322 | 10.4 | 31.0 | 34.0 | 38.0 | 0.0743 |
| HIGH | 341,688 | 10.8 | 31.2 | 34.0 | 38.0 | 0.0808 |

Rationale: `30 tx/s` equals the declared maximum expected burst cross-shard intensity, `60 x 0.50 = 30 tx/s`. Neutral diagnostics show useful dynamic range with limited saturation.

### Queue-length reference

Initial candidate:

`queue_ref = 40.0`

Neutral time-weighted queue diagnostics showed excessive compression at that reference. Candidate calibration table:

| Regime | Q_ref | Saturated-time fraction | Above-half-scale fraction | Mean normalized queue |
|---|---:|---:|---:|---:|
| LOW | 10 | 0.0000 | 0.0000 | 0.0005 |
| LOW | 15 | 0.0000 | 0.0000 | 0.0003 |
| LOW | 20 | 0.0000 | 0.0000 | 0.0002 |
| LOW | 25 | 0.0000 | 0.0000 | 0.0002 |
| LOW | 30 | 0.0000 | 0.0000 | 0.0002 |
| LOW | 40 | 0.0000 | 0.0000 | 0.0001 |
| TRANSITIONAL | 10 | 0.0095 | 0.0153 | 0.0239 |
| TRANSITIONAL | 15 | 0.0061 | 0.0114 | 0.0184 |
| TRANSITIONAL | 20 | 0.0036 | 0.0095 | 0.0149 |
| TRANSITIONAL | 25 | 0.0020 | 0.0073 | 0.0124 |
| TRANSITIONAL | 30 | 0.0009 | 0.0061 | 0.0106 |
| TRANSITIONAL | 40 | 0.0002 | 0.0036 | 0.0080 |
| HIGH | 10 | 0.0258 | 0.0417 | 0.0550 |
| HIGH | 15 | 0.0164 | 0.0310 | 0.0433 |
| HIGH | 20 | 0.0097 | 0.0258 | 0.0355 |
| HIGH | 25 | 0.0054 | 0.0197 | 0.0298 |
| HIGH | 30 | 0.0025 | 0.0164 | 0.0254 |
| HIGH | 40 | 0.0006 | 0.0097 | 0.0194 |

Final scheduler-neutral calibration decision:

`queue_ref = 10.0`

Reason: it gives materially greater queue-signal dynamic range while preserving low saturation: 0% in LOW, 0.95% in TRANSITIONAL, and 2.58% in HIGH.

---

## E6 — Final CAPC primary-parameter freeze

Final `configs/primary.yaml` CAPC values:

```yaml
capc:
  arrival_window_s: 5.0
  lock_window_s: 5.0
  lambda_ref: 30.0
  queue_ref: 10.0
  contention_weights:
    arrival: 0.25
    queue: 0.25
    dependency: 0.25
    lock: 0.25
  aging_horizon_s: 1.0
  ranking_weights:
    urgency: 0.35
    aging: 0.30
    dependency: 0.20
    lock_pressure: 0.15
  gamma: 1.0
  thresholds:
    low_medium: 0.33
    medium_high: 0.66
```

Final configuration SHA-256:

`be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`

Verification after calibration:

- `V1-V12 PASS`.
- CAPC hand-check V8: computed `0.858750000000`, expected `0.858750000000`.

Parameter-freeze merge commit:

`4c392d9f88f36a92bca4ab23e1db90a55e0f5c4f`

README/status synchronization commit:

`1d611388564b4dda309771d958534af3987c9a90`

Freeze rule: these primary CAPC parameters must not be retuned using labelled CAPC-versus-baseline main-experiment results. Predeclared sensitivity runs are robustness analyses, not parameter-selection procedures.

---

## E7 — Current experiment status

Completed:

- Chapter 5 implementation and V1-V12 verification.
- Runtime optimization and equivalence validation.
- 90-run neutral Static Atomic FIFO regime-coverage pilot.
- Scheduler-neutral normalization calibration.
- Final primary CAPC parameter freeze.

Pending:

- Baseline precision pilot and final replication count `N` selection from `{30, 40, 50, 60}`.
- Frozen consecutive seed list `1..N`.
- Main `90N` research matrix.
- Deterministic post-processing and preservation checks.
- Paired uncertainty/statistical analysis.
- RQ1-RQ4 Chapter 6 results.
- Evidence-dependent Chapter 7 conclusions, limitations, and future work.

---

## Chapter mapping

### Chapter 5 — Implementation and verification

Use E1-E3 and the implementation/provenance parts of E6. These support architecture validation, reproducibility, software verification, and computational-readiness discussion. Do not present E3 as scheduler-performance evidence.

### Chapter 6 — Experimental results and analysis

Use E4-E6 only as setup/calibration evidence. The primary Chapter 6 performance claims must come from the frozen main `90N` comparative dataset and its predeclared statistical analysis, which are still pending.

### Chapter 7 — Discussion and conclusion

Use the final RQ-specific evidence from Chapter 6. Do not infer CAPC effectiveness from neutral-pilot, verification, or runtime-readiness evidence. Conclusions must be limited to actual frozen comparative findings and declared sensitivity/validity evidence.

---

## Next evidence entry

The next entry must record the Static Atomic FIFO baseline precision exercise, the half-width calculations for `N = 30, 40, 50, 60`, the selected `N`, the frozen seed list, the executing Git commit, and the exact experiment/configuration hashes before any labelled CAPC comparative result is inspected.
