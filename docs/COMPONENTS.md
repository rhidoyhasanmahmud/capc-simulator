# CAPC Simulator Component Guide

This document describes every major component in the repository, what it does, what it receives, what it produces, and how it maps to the thesis implementation design.

## 1. Configuration layer

### `src/capc_sim/config/schema.py`
**Purpose:** Defines the typed experiment configuration and validates research constraints before a run starts.

**Key responsibilities**
- simulation duration and warm-up;
- MMPP NORMAL/BURST parameters;
- shard count and cross-shard ratio;
- two-/three-shard dependency mix;
- priority-class composition;
- coordination worker count and service-time range;
- CAPC observation windows, normalization references, weights, aging horizon, gamma, and thresholds;
- main experiment matrix levels.

**Important rule:** `configs/primary_template.yaml` cannot be used for final comparative execution until the CAPC parameters are frozen.

### `src/capc_sim/config/loader.py`
**Purpose:** Loads YAML, converts it to the typed configuration object, serializes effective configurations, and calculates a deterministic configuration hash.

**Output:** an `ExperimentConfig` object plus reproducibility metadata.

---

## 2. Workload layer

### `src/capc_sim/workload/mmpp.py`
**Purpose:** Generates the exogenous two-state MMPP workload independently of scheduler execution.

**Model implemented**
- NORMAL arrival rate: `lambda_normal`;
- BURST arrival rate: `lambda_burst`;
- NORMAL→BURST transition rate: `q_normal_to_burst`;
- BURST→NORMAL transition rate: `q_burst_to_normal`;
- deterministic initial state;
- independent random streams derived from one root seed.

**Why separate random streams?** A scheduler must never change future arrivals, priorities, shard assignments, or service requirements by consuming extra random numbers.

### `src/capc_sim/workload/trace.py`
**Purpose:** Stores the fully materialized transaction trace and NORMAL/BURST state intervals.

**Key feature:** `Trace.hash()` gives a deterministic SHA-256 identity. The matrix runner checks that paired scheduler runs use exactly the same trace hash.

**Files written**
- `trace.csv`
- `workload_states.csv`

---

## 3. Core model layer

### `src/capc_sim/model/enums.py`
Defines workload state, priority class, and transaction lifecycle state.

### `src/capc_sim/model/transaction.py`
Separates immutable exogenous transaction attributes from mutable execution state.

**Immutable research attributes**
- transaction ID;
- arrival time;
- priority class;
- workload state;
- required shard set;
- service requirement;
- intra-/cross-shard classification.

**Mutable lifecycle fields**
- queue-entry time;
- service-start time;
- completion time;
- worker assignment;
- queue-entry RQ2 predictors;
- cutoff completion flag.

### `src/capc_sim/model/events.py`
Defines deterministic event ordering for arrival, service completion, and the measurement cutoff.

---

## 4. Coordination layer

### `src/capc_sim/coordinator/queue.py`
**Purpose:** Stores pending cross-shard transactions without implementing scheduling policy.

This separation is important: the queue owns data, while the scheduler owns service-order decisions.

### `src/capc_sim/coordinator/worker_pool.py`
**Purpose:** Models finite coordination capacity.

A worker services at most one transaction at a time. The simulator supports the thesis worker levels of 2 and 4, while tests can use other positive values for verification.

### `src/capc_sim/coordinator/lock_manager.py`
**Purpose:** Implements all-or-nothing logical shard locking for matched atomic treatments.

**Invariants**
- no partial lock acquisition by a waiting transaction;
- a shard has at most one in-service owner;
- all required locks are acquired together;
- all locks are released together at completion;
- recent per-shard occupancy history is retained for CAPC lock-pressure calculation.

This module is the implementation boundary that distinguishes the matched atomic schedulers from Diagnostic FIFO.

---

## 5. Scheduler layer

### `src/capc_sim/scheduler/base.py`
Defines the common selection contract. A scheduler selects a transaction; it does **not** acquire locks, allocate workers, or complete service.

### `src/capc_sim/scheduler/diagnostic_fifo.py`
**Purpose:** Non-atomic descriptive queue-order reference.

**Rule:** oldest waiting cross-shard request when a worker is free.

**Research role:** descriptive only; excluded from causal matched comparisons.

### `src/capc_sim/scheduler/static_atomic_fifo.py`
**Purpose:** Principal matched baseline.

**Rule:** select the earliest-arriving transaction among those whose required shards are currently unlocked.

If the oldest queued transaction is blocked, it remains queued and the next eligible transaction can be selected. This avoids artificial head-of-line blocking.

### `src/capc_sim/scheduler/capc.py`
**Purpose:** Full CAPC scheduler.

For each eligible transaction, it calculates:
- urgency `U_i`;
- normalized waiting age `A_i(t)`;
- normalized dependency burden `D_i`;
- recent lock pressure `H_i(t)`;
- global contention score `C(t)`;
- final CAPC ranking score `S_i(t)`.

Implemented ranking structure:

```text
S_i(t) = w_U U_i + w_A A_i(t)
         + [1 + gamma C(t)]
           [w_D (1 - D_i) + w_H (1 - H_i(t))]
```

Instantaneous active-lock conflict `K_i(t)` is used for eligibility and RQ2 logging, not as a ranking term after eligibility filtering.

**Tie-breaking:** higher score → greater age → earlier queue entry/arrival → lower transaction ID.

### `src/capc_sim/scheduler/capc_no_contention.py`
Ablation of full CAPC with `gamma = 0` at runtime. All other logic is inherited from the full CAPC implementation.

### `src/capc_sim/scheduler/capc_no_priority.py`
Ablation of full CAPC with urgency weight treated as zero. All other logic is inherited from the full CAPC implementation.

### `src/capc_sim/scheduler/factory.py`
Creates the selected scheduler from a configuration/CLI name.

---

## 6. Runtime state and simulation engine

### `src/capc_sim/simulation/state.py`
**Purpose:** Computes the state visible to schedulers.

**Global contention components**
- recent cross-shard arrival pressure;
- normalized queue pressure;
- mean dependency pressure;
- active lock pressure.

**Transaction-specific components**
- urgency;
- bounded aging;
- dependency burden;
- instantaneous lock conflict;
- recent required-shard lock occupancy.

The module separates global state from candidate-specific features so that global constants are not incorrectly used as candidate-ranking terms.

### `src/capc_sim/simulation/engine.py`
**Purpose:** Executes the discrete-event lifecycle.

**Event flow**
1. transaction arrives;
2. intra-shard transaction bypasses the cross-shard queue;
3. cross-shard transaction enters the coordination queue;
4. queue-entry RQ2 predictors are recorded;
5. while workers are free, the active scheduler selects work;
6. matched atomic treatments acquire all required shard locks;
7. non-preemptive service begins;
8. completion releases locks and worker capacity;
9. scheduler is triggered again;
10. arrivals stop at the configured cutoff, then admitted work drains.

**Important invariant:** after each event the engine checks transaction state and lock/worker consistency.

---

## 7. Metrics and provenance layer

### `src/capc_sim/metrics/recorder.py`
Records three event streams:
- `state_events`: queue length, active workers, locked shards, workload state;
- `decisions`: scheduler selection and CAPC diagnostic fields;
- `dispatch_snapshots`: candidate, eligible, and blocked counts at dispatch opportunities.

### `src/capc_sim/metrics/outputs.py`
Writes the complete run artefact.

**Per-run files**
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

**Provenance metadata includes**
- configuration hash;
- trace hash;
- Git commit when available;
- Python/platform information;
- installed package versions;
- cutoff snapshot;
- output schema version.

---

## 8. Analysis layer

### `src/capc_sim/analysis/state_series.py`
Implements exact piecewise-state operations from event logs:
- time-weighted means;
- continuous-time least-squares queue slope;
- sliding queue mean;
- sustained post-burst recovery detection.

This avoids arbitrary fixed-interval polling for queue summaries.

### `src/capc_sim/analysis/run_metrics.py`
Calculates run-level metrics:
- mean/median/p95/p99 cross-shard latency;
- p95-minus-median latency spread;
- waiting and service times;
- cross-shard coordination throughput;
- time-weighted mean/max queue length;
- final queue slope;
- worker utilization;
- class completion ratios and Jain index;
- RQ2 run-level predictor summaries;
- post-burst recovery and queue-stability classification.

### `src/capc_sim/analysis/paired.py`
Contains fairness/starvation helpers and re-exports paired statistical utilities.

### `src/capc_sim/analysis/loaders.py`
Loads matrix-level transaction and summary files for offline RQ2 and comparative analysis. It deliberately lives outside the simulator core so data loading cannot influence event-level execution.

### `src/capc_sim/analysis/statistics.py`
Provides reusable functions for:
- paired bootstrap confidence intervals;
- paired treatment-baseline tables;
- Wilcoxon paired fallback;
- Holm adjustment;
- the predeclared primary p99 mixed model;
- the RQ2 waiting-time mixed model.

These functions support later Chapter 6 analysis; they do not alter simulation execution.

---

## 9. Experiment orchestration

### `src/capc_sim/experiments/runner.py`
Runs one simulation or the paired experiment matrix.

**Pairing guarantee:** one trace is generated for each condition/seed and replayed under all requested treatments.

**Matrix outputs**
- `matrix_summary.csv`
- `pair_integrity.csv`
- `matrix_manifest.json`
- `failures.json`

Failed runs are recorded; replacement seeds are never silently substituted.

### `src/capc_sim/experiments/pilot.py`
Supports the neutral Static Atomic FIFO pilot and the Chapter 3 candidate replication counts `{30, 40, 50, 60}`.

It contains utilities for:
- raw coordination utilization;
- baseline log-p99 precision half-width;
- selecting the smallest candidate `N` satisfying the predeclared precision target;
- neutral-pilot execution without labelled CAPC performance.

### `src/capc_sim/experiments/sensitivity.py`
Generates the predeclared sensitivity families for:
- burst intensity;
- burst persistence;
- dependency mix;
- service-time multiplier;
- CAPC ranking weights;
- CAPC contention weights;
- interpretation thresholds.

Sensitivity generation is separate from the primary matrix so that sensitivity runs cannot be accidentally mixed with confirmatory results.

### `src/capc_sim/experiments/verify.py`
Implements the Chapter 5 V1–V12 implementation verification report.

The checks cover reproducibility, paired trace equality, FIFO ordering, lock exclusion/release, multi-worker dispatch, CAPC score correctness, aging, accounting, low-load sanity, and overload queue growth.

---

## 10. Command-line interface

### `src/capc_sim/cli.py`
Provides the `capc-sim` command:

```text
capc-sim run
capc-sim matrix
capc-sim pilot
capc-sim verify
```

The `scripts/` directory contains small Python wrappers for the same commands.

---

## 11. Configurations

### `configs/dev.yaml`
Runnable **development-only** settings. The CAPC numbers here exist only to exercise and verify the implementation.

### `configs/primary_template.yaml`
Thesis primary configuration template. CAPC numerical values are intentionally `null` until the Chapter 4 parameter-freezing decision is complete.

The primary template is designed to fail validation while those values remain unset.

---

## 12. Verification tests

### `tests/unit/`
Tests isolated formulae, configuration rules, lock behavior, queue behavior, MMPP reproducibility, CAPC features, fairness helpers, and piecewise-state analysis.

### `tests/integration/`
Tests complete event flows, atomic lock exclusion, non-atomic Diagnostic FIFO behavior, multi-worker execution, output provenance, and the V1–V12 verification report.

### `tests/regression/`
Tests deterministic replay and cross-scheduler exogenous trace equality.

---

## 13. Research boundary

The repository deliberately does **not** model:
- production blockchain consensus;
- validator committees;
- cryptographic execution;
- P2P networking;
- smart-contract execution;
- physical IoT network latency;
- protocol-specific rollback/retry behavior beyond the defined coordination abstraction.

These are exclusions of the thesis simulation boundary, not missing software features.
