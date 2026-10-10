# Thesis-to-Code Traceability

| Thesis requirement | Implementation location | Evidence/output |
|---|---|---|
| Two-state MMPP NORMAL/BURST workload | `workload/mmpp.py` | `trace.csv`, `workload_states.csv` |
| Same exogenous trace across schedulers | `experiments/runner.py`, `Trace.hash()` | `pair_integrity.csv`, trace hashes |
| Logical shards and 2/3-shard dependencies | `workload/mmpp.py`, `model/transaction.py` | `required_shards`, `dependency_degree` |
| Finite 2/4-worker coordination service | `coordinator/worker_pool.py` | state/transaction logs |
| All-or-nothing atomic lock eligibility | `coordinator/lock_manager.py`, `simulation/engine.py` | V5/V6 verification |
| No partial lock holding | `lock_manager.acquire_all()` | unit tests and V6 |
| Non-preemptive service | `simulation/engine.py` | lifecycle timestamps |
| Static Atomic FIFO causal baseline | `scheduler/static_atomic_fifo.py` | treatment outputs |
| Diagnostic FIFO descriptive only | `scheduler/diagnostic_fifo.py` | separate treatment label |
| CAPC contention estimator | `simulation/state.py` | decision diagnostics |
| Urgency mapping | `simulation/state.py` | `urgency` decision field |
| Monotonic bounded aging | `simulation/state.py` | V9 + unit tests |
| Dependency normalization | `simulation/state.py` | decision diagnostics |
| Instantaneous conflict for eligibility/RQ2 | `state.active_lock_conflicts()` | `active_lock_conflicts_at_entry` |
| Recent lock pressure for eligible ranking | `lock_manager.occupancy_fraction()`, `state.recent_lock_pressure()` | `recent_lock_pressure` |
| CAPC score Eq. 4.12 | `scheduler/capc.py` | V8 + decision log |
| No-Contention ablation | `scheduler/capc_no_contention.py` | separate treatment |
| No-Priority ablation | `scheduler/capc_no_priority.py` | separate treatment |
| Deterministic tie-breaking | `scheduler/capc.py` | unit tests |
| Repeated dispatch while workers free | `simulation/engine.py` | V7 |
| Measurement-window drain | `simulation/engine.py` | cutoff metadata |
| Per-run p95/p99, queue and throughput | `analysis/run_metrics.py` | `summary.json` |
| Queue recovery/stability rule | `analysis/run_metrics.py`, `analysis/state_series.py` | `queue_recovery.json` |
| RQ2 queue-entry predictors | `simulation/engine.py` | `transactions.csv` |
| Paired bootstrap/Wilcoxon/Holm helpers | `analysis/statistics.py` | Chapter 6 analysis |
| Primary mixed p99 model helper | `analysis/statistics.py` | Chapter 6 analysis |
| RQ2 mixed model helper | `analysis/statistics.py` | Chapter 6 analysis |
| Neutral pilot support | `experiments/pilot.py` | pilot matrix outputs |
| Primary matrix = 90N | `configs/primary_template.yaml`, `runner.py` | `matrix_manifest.json` |
| Sensitivity separation | `experiments/sensitivity.py` | separate generated configs/runs |
| Environment/source/config provenance | `metrics/outputs.py` | `metadata.json`, `effective_config.yaml` |
| Verification evidence gate | `experiments/verify.py`, `tests/` | V1–V12, pytest output |

## Important interpretation boundary

The code implements the research design; it does not establish that CAPC improves performance. Performance claims require the frozen primary configuration, neutral pilot, final paired experiment matrix, and Chapter 6 analysis.
