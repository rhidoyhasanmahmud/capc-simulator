# CAPC Simulator — Component Guide

This document explains the implementation role of each major repository component and how it supports the Chapter 3 methodology and Chapter 4 CAPC design. The simulator is intentionally modular so that scheduler treatment is the manipulated mechanism while workload generation, locking, worker capacity, service time, and measurement remain controlled.

## 1. Configuration layer

### `src/capc_sim/config/schema.py`
Defines typed configuration objects and validates simulation, workload, sharding, priority, coordination, matrix, and CAPC settings.

Important research control: when `research.require_frozen_capc` is enabled, missing CAPC parameters cause configuration validation to fail instead of silently substituting development values.

### `src/capc_sim/config/loader.py`
Loads YAML configuration, converts it to the typed schema, creates deterministic configuration hashes, and writes effective configurations to run outputs.

### `configs/dev.yaml`
Runnable development/smoke-test configuration. Its CAPC numbers exist only to exercise the implementation and must not automatically become thesis parameters.

### `configs/primary_template.yaml`
Research configuration template. Methodology-level values are present, while final CAPC numerical parameters remain `null` until the Chapter 4 parameter-freezing decision is completed.

---

## 2. Workload layer

### `src/capc_sim/workload/mmpp.py`
Implements the two-state NORMAL/BURST MMPP workload. Independent deterministic random streams are used for state transitions, inter-arrivals, intra/cross-shard classification, dependency degree, shard assignment, priority, and service time.

Research purpose: scheduler-specific code cannot alter future exogenous workload values.

### `src/capc_sim/workload/trace.py`
Stores the complete scheduler-independent transaction trace and workload-state intervals. It provides a canonical trace hash and CSV serialization so paired treatments can prove they consumed the same exogenous input.

---

## 3. Core model layer

### `src/capc_sim/model/transaction.py`
Represents immutable transaction attributes plus mutable lifecycle state. Key fields include transaction ID, arrival, required shards, priority, workload state, service requirement, queue-entry time, service start, completion, and queue-entry RQ2 predictors.

### `src/capc_sim/model/enums.py`
Defines workload, priority, and transaction lifecycle enums.

### `src/capc_sim/model/events.py`
Defines deterministic discrete-event ordering for arrivals, completions, and the arrival-horizon cutoff.

---

## 4. Coordination layer

### `src/capc_sim/coordinator/queue.py`
Stores pending cross-shard transactions. It does not decide service order; scheduler implementations operate over the same queue abstraction.

### `src/capc_sim/coordinator/worker_pool.py`
Models finite coordination capacity. A worker services at most one cross-shard transaction at a time.

### `src/capc_sim/coordinator/lock_manager.py`
Implements the matched atomic boundary:

- all required shard locks must be available before service;
- acquisition is all-or-nothing;
- waiting transactions never hold partial locks;
- locks remain held for the full non-preemptive service interval;
- all locks are released together at completion;
- per-shard occupancy history supports recent-lock-pressure calculation.

---

## 5. Scheduler layer

### `src/capc_sim/scheduler/base.py`
Defines the common scheduler selection contract. A scheduler chooses a transaction; lock acquisition, worker allocation, and completion remain in the shared simulator/coordinator path.

### `src/capc_sim/scheduler/diagnostic_fifo.py`
Non-atomic descriptive reference. It selects the oldest waiting request and is intentionally excluded from matched causal inference.

### `src/capc_sim/scheduler/static_atomic_fifo.py`
Principal matched baseline. It filters to currently eligible transactions and selects the earliest-arriving eligible transaction. A blocked oldest transaction remains queued while another eligible transaction may proceed.

### `src/capc_sim/scheduler/capc.py`
Implements full CAPC. For each eligible transaction it evaluates urgency, bounded waiting age, dependency burden, recent required-shard lock pressure, global contention, and the final CAPC score:

```text
S_i(t) = w_U U_i + w_A A_i(t)
         + [1 + gamma C(t)]
           [w_D (1 - D_i) + w_H (1 - H_i(t))]
```

Instantaneous active-lock conflict `K_i(t)` is used for eligibility and RQ2 logging, not as an additive ranking feature after eligibility filtering.

Tie-breaking is deterministic: higher score → greater age → earlier arrival/queue entry → lower transaction ID.

### `src/capc_sim/scheduler/capc_no_contention.py`
Ablation using the same CAPC code path with contention amplification disabled (`gamma = 0`).

### `src/capc_sim/scheduler/capc_no_priority.py`
Ablation using the same CAPC code path with urgency contribution disabled.

### `src/capc_sim/scheduler/factory.py`
Creates the selected scheduler from its experiment label.

---

## 6. Runtime state and discrete-event engine

### `src/capc_sim/simulation/state.py`
Provides the read-only scheduling view and implements:

- recent cross-shard arrival rate;
- normalized arrival and queue pressure;
- dependency pressure;
- active-lock pressure;
- global contention score;
- urgency mapping;
- monotonic aging;
- instantaneous lock-conflict count;
- recent transaction-specific lock pressure;
- atomic eligibility filtering.

### `src/capc_sim/simulation/engine.py`
Executes the transaction lifecycle:

1. arrival;
2. intra-shard bypass or cross-shard enqueue;
3. queue-entry predictor capture;
4. repeated scheduling while workers remain free;
5. atomic lock acquisition for matched treatments;
6. non-preemptive service;
7. completion and lock release;
8. re-dispatch after state changes;
9. arrival cutoff followed by drain of admitted work.

The engine checks transaction, lock, and worker invariants after events.

---

## 7. Metrics and provenance layer

### `src/capc_sim/metrics/recorder.py`
Captures state events, scheduler decisions, and dispatch snapshots. These logs preserve queue/eligibility dynamics rather than only final averages.

### `src/capc_sim/metrics/outputs.py`
Writes the per-run research artefact:

- `trace.csv`
- `workload_states.csv`
- `transactions.csv`
- `decisions.csv`
- `dispatch_snapshots.csv`
- `state_events.csv`
- `summary.json`
- `queue_recovery.json`
- `metadata.json`
- `effective_config.yaml`

`metadata.json` records configuration/trace hashes, source revision when available, Python executable/runtime, platform, machine, processor, best-effort physical memory, package versions, and cutoff state.

---

## 8. Analysis layer

### `src/capc_sim/analysis/state_series.py`
Performs exact piecewise-state calculations from timestamped state changes, including time-weighted means, continuous-time queue slope, moving averages, and sustained recovery detection.

### `src/capc_sim/analysis/run_metrics.py`
Produces run-level latency, waiting, service, throughput, queue, worker-utilization, Jain-index, unfinished-work, recovery/stability, and RQ2 predictor summaries.

### `src/capc_sim/analysis/paired.py`
Contains the Equation 3.9 starvation-threshold helper, starvation incidence, Jain completion-ratio helper, and paired-statistics exports.

### `src/capc_sim/analysis/preservation.py`
Completes paired matrix post-processing. For each condition/seed it derives the starvation threshold from the matched Static Atomic FIFO waiting distribution:

```text
max(0.50 s, 5 × baseline median waiting time)
```

It applies that threshold to paired treatments, enriches run summaries, and calculates deterministic CAPC-versus-baseline preservation checks for p99, throughput, Jain index, starvation, low-priority p95 waiting, and queue stability.

It deliberately does not declare overall CAPC success because final inference also requires paired uncertainty across seeds.

### `src/capc_sim/analysis/loaders.py`
Loads matrix-level run summaries and transaction records for offline analysis.

### `src/capc_sim/analysis/statistics.py`
Provides:

- paired bootstrap confidence intervals;
- paired metric tables;
- Wilcoxon paired fallback;
- Holm adjustment;
- primary log-p99 mixed-effects model;
- RQ2 waiting-time mixed-effects model restricted to Static Atomic FIFO transactions within the arrival-based measurement window.

---

## 9. Experiment orchestration

### `src/capc_sim/experiments/runner.py`
Executes one run or the paired matrix. One trace is generated for each condition/seed and replayed under all selected treatments. Failed runs are logged rather than silently replaced with different seeds.

Matrix-level outputs include `matrix_summary.csv`, `pair_integrity.csv`, `matrix_manifest.json`, and `failures.json`.

### `src/capc_sim/experiments/pilot.py`
Implements neutral Static Atomic FIFO pilot support, baseline log-p99 precision calculations for candidate `N ∈ {30,40,50,60}`, scheduler-neutral raw utilization, and LOW/TRANSITIONAL/HIGH contention-regime reporting.

The pilot never uses labelled CAPC performance to choose readiness settings.

### `src/capc_sim/experiments/sensitivity.py`
Generates the predeclared workload, dependency, service-time, CAPC-weight, and threshold sensitivity configurations separately from the primary matrix.

### `src/capc_sim/experiments/verify.py`
Implements the V1-V12 Chapter 5 verification matrix covering trace reproducibility, scheduler ordering, lock safety/release, multi-worker dispatch, CAPC score checks, aging, accounting, low-load sanity, and overload queue growth.

---

## 10. Command-line interface

### `src/capc_sim/cli.py`
Provides:

```text
capc-sim run
capc-sim matrix
capc-sim pilot
capc-sim analyze
capc-sim verify
```

The `analyze` command performs paired starvation/preservation post-processing after a matrix run.

---

## 11. Tests

### `tests/unit/`
Tests configuration, MMPP determinism, queue/lock functions, CAPC features, fairness/starvation helpers, preservation calculations, and piecewise-state analysis.

### `tests/integration/`
Tests complete event flows, matched atomicity, diagnostic behaviour, multi-worker execution, output/provenance, and the V1-V12 report.

### `tests/regression/`
Tests deterministic replay and cross-treatment exogenous trace equality.

---

## 12. Research boundary

The simulator deliberately does not model production consensus execution, validator committees, P2P topology, cryptographic cost, smart-contract execution, physical IoT communication, or protocol-specific production failure/retry behaviour outside the declared coordination abstraction.

These are explicit thesis-scope exclusions, not unfinished implementation components.
