# End-to-End Research Software Workflow

This document defines the executable workflow from a clean checkout to analysis-ready CAPC experiment outputs. It separates **software verification** from **research inference** so that development smoke results cannot be mistaken for thesis findings.

## 1. Install and verify the implementation

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
capc-sim verify --config configs/dev.yaml --json-output results/verification.json
```

Expected implementation gate: the automated test suite passes and V1-V12 all pass.

## 2. Development smoke run

```bash
capc-sim matrix \
  --config configs/dev.yaml \
  --seeds 1 \
  --shards 4 \
  --ratios 0.30 \
  --workers 2 \
  --output results/dev_matrix
```

This confirms orchestration and paired trace identity only. `configs/dev.yaml` is not a thesis-performance configuration.

## 3. Freeze the CAPC research parameters

Before labelled primary comparisons, create a versioned research configuration from `configs/primary_template.yaml` and replace every CAPC `null` value using the academically justified Chapter 4 parameter-freezing decision. Keep `research.require_frozen_capc: true` so an incomplete primary configuration fails fast.

Do not select final values after inspecting labelled CAPC-versus-baseline performance.

## 4. Run the neutral pilot

The pilot executes Static Atomic FIFO only.

```bash
capc-sim pilot \
  --config configs/primary.yaml \
  --seeds 1 2 3 4 5 \
  --shards 4 8 16 \
  --ratios 0.10 0.30 0.50 \
  --workers 2 4 \
  --output results/pilot
```

The command writes `pilot_regime_summary.csv` and `pilot_acceptance.json`. Regime coverage is based on scheduler-neutral burst raw utilisation together with observed lock blocking and queueing. This evidence is for workload/implementation readiness, not CAPC selection.

The final replication count `N` must then be frozen from the predeclared candidate set before labelled scheduler effects are inspected.

## 5. Execute the paired primary matrix

```bash
capc-sim matrix \
  --config configs/primary.yaml \
  --seeds 1 2 3 ... N \
  --shards 4 8 16 \
  --ratios 0.10 0.30 0.50 \
  --workers 2 4 \
  --schedulers diagnostic_fifo static_atomic_fifo capc capc_no_contention capc_no_priority \
  --output results/primary
```

The design contains `3 × 3 × 2 × 5 × N = 90N` runs. One trace is generated for each condition/seed and replayed under every selected scheduler. `pair_integrity.csv` must remain true for every pair.

## 6. Deterministic matrix post-processing

```bash
capc-sim analyze \
  --config configs/primary.yaml \
  --matrix-dir results/primary
```

This produces:

- `analysis/starvation_by_run.csv`
- `analysis/matrix_summary_enriched.csv`
- `analysis/capc_vs_baseline_preservation.csv`
- `analysis/analysis_manifest.json`

The starvation threshold is derived independently for each condition/seed from the matched Static Atomic FIFO run:

```text
max(0.50 s, 5 × paired-baseline median waiting time)
```

The same threshold is then applied to the paired treatments. The post-processing also evaluates the deterministic preservation limits for throughput, Jain's completion-ratio index, starvation, low-priority p95 waiting time, and queue stability.

## 7. Inferential analysis

The repository exposes helpers for:

- paired run-level metric tables;
- 10,000-resample paired bootstrap confidence intervals;
- Holm adjustment for planned contrasts;
- paired Wilcoxon fallback;
- primary log-p99 mixed-effects modelling;
- RQ2 transaction-level mixed-effects modelling restricted to the Static Atomic FIFO measurement window.

The final Chapter 6 interpretation must use the frozen primary dataset, diagnostics, uncertainty estimates and predeclared success criteria. The deterministic preservation table alone does not establish overall CAPC success.

## 8. Evidence retained for Chapter 5

Before Chapter 5 is treated as implementation-complete, retain:

1. exact Git commit/release tag;
2. frozen configuration hash/version where applicable;
3. Python, platform, machine, processor, physical-memory and package provenance;
4. `pytest` output;
5. V1-V12 verification report;
6. paired-trace smoke evidence;
7. representative output-schema examples;
8. neutral-pilot evidence when the pilot is executed.

Performance claims belong to Chapter 6, not Chapter 5.
