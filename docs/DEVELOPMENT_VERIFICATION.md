# Development Verification Record

**Status:** software-development verification only — **not final thesis experimental evidence**.

This record documents the implementation-verification snapshot used while completing the Chapter 5 software artefact. It demonstrates implementation behaviour; it does **not** demonstrate that CAPC outperforms the matched baseline.

## Automated test suite

Command:

```bash
pytest
```

The updated development snapshot passed **31 tests**. The suite covers configuration gating, MMPP determinism, queue/lock behaviour, CAPC feature calculations, fairness/starvation helpers, paired preservation post-processing, matched-atomic versus diagnostic scheduling semantics, multi-worker dispatch, provenance outputs, piecewise-state analysis, and deterministic replay.

## Chapter 5 verification report

Command:

```bash
capc-sim verify --config configs/dev.yaml --json-output results/verification.json
```

The development verification passes the V1-V12 checks:

- V1 trace reproducibility
- V2 cross-treatment trace equality
- V3 Static Atomic FIFO ordering
- V4 Diagnostic FIFO ordering
- V5 lock exclusion
- V6 lock release
- V7 multi-worker dispatch
- V8 CAPC score hand-check
- V9 aging monotonicity
- V10 transaction accounting
- V11 low-load sanity
- V12 overload stress

## End-to-end smoke workflow

The development snapshot was exercised through the complete software path:

1. paired five-treatment matrix execution;
2. paired trace-integrity verification;
3. deterministic starvation/preservation post-processing;
4. neutral-pilot regime reporting;
5. V1-V12 implementation verification.

These executions validate orchestration and implementation behaviour only. Development CAPC performance values are not thesis findings because `configs/dev.yaml` does not contain the final frozen research parameter set.

## Final evidence gate

Before final comparative experimentation, retain:

1. environment provenance, including physical-memory information where available;
2. exact Git commit/release revision;
3. frozen primary configuration and hash;
4. frozen seed list;
5. final test and V1-V12 verification outputs;
6. neutral-pilot evidence and final replication decision.

The main CAPC performance evidence belongs to Chapter 6 rather than this development-verification record.
