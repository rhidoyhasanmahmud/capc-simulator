# Development Verification Record

**Status:** software-development verification only — **not final thesis experimental evidence**.

This record documents the verification snapshot included in the repository package. It demonstrates implementation behaviour; it does **not** demonstrate that CAPC outperforms the matched baseline.

## Automated test suite

Command:

```bash
pytest
```

The final packaged snapshot passed **29 tests** in the packaging environment; the repository README retains the observed console form. The suite covers configuration gating, MMPP determinism, queue/lock behaviour, CAPC feature calculations, fairness helpers, matched-atomic versus diagnostic scheduling semantics, multi-worker dispatch, provenance outputs, piecewise-state analysis, and deterministic replay.

## Chapter 5 verification report

Command:

```bash
capc-sim verify --config configs/dev.yaml --json-output results/verification.json
```

The included development snapshot is expected to pass all V1–V12 checks:

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

## Smoke matrix

A small development-only paired matrix is executed across all five schedulers using one condition/seed. Its purpose is to verify orchestration and paired trace identity. Development performance values must not be used as thesis findings because the CAPC parameters in `configs/dev.yaml` are not the frozen Chapter 4 research parameters.

## Final evidence gate

Before final comparative experimentation, re-run verification on the frozen research environment and retain:

1. environment provenance;
2. exact Git commit;
3. frozen primary configuration and hash;
4. frozen seed list;
5. final test/verification outputs;
6. neutral-pilot evidence.
