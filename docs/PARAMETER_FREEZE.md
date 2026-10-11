# Primary Experiment Parameter Freeze

## Purpose

This document records the pre-comparative freeze of the primary CAPC experiment configuration. The freeze was completed before any labelled CAPC-versus-baseline performance results were inspected.

## Frozen implementation basis

The simulator implementation and runtime optimizations were validated on:

- Git commit: `e3e425b8ca8f868c42b26729133b9e0bf58ef147`
- Automated tests: `31/31 PASS`
- Chapter 5 verification: `V1-V12 PASS`
- Runtime-optimization summary equivalence: PASS

The Git revision recorded in each final run's `metadata.json` remains the authoritative execution provenance after this parameter-freeze branch is merged.

## Neutral pilot

The scheduler-neutral pilot used Static Atomic FIFO only.

Experimental coverage:

- 4, 8, and 16 logical shards
- cross-shard ratios 0.10, 0.30, and 0.50
- 2 and 4 coordination workers
- seeds 1-5
- 90 Static Atomic FIFO runs in total

Observed contention-regime counts:

- LOW: 16
- TRANSITIONAL: 54
- HIGH: 20

The neutral-pilot acceptance criterion passed because all three predeclared contention regimes were represented.

No CAPC-labelled comparative performance result was used during this calibration step.

## Normalization calibration

The initial candidate configuration used:

- `lambda_ref = 30.0`
- `queue_ref = 40.0`

`lambda_ref = 30.0` was retained because it corresponds to the declared maximum expected cross-shard burst arrival intensity:

`60 transactions/s × 0.50 = 30 cross-shard transactions/s`.

Neutral-baseline diagnostics showed that this reference preserved useful dynamic range while avoiding dominant saturation.

`queue_ref` was revised from `40.0` to `10.0` using only Static Atomic FIFO neutral-pilot queue-state observations.

For `queue_ref = 10.0`:

- LOW saturation fraction: 0.0000
- TRANSITIONAL saturation fraction: 0.0095
- HIGH saturation fraction: 0.0258
- HIGH fraction above half-scale: 0.0417

This setting gives the queue component measurable dynamic range under contention while keeping saturation limited. Larger candidate references progressively compressed the normalized queue signal.

## Final CAPC configuration

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
