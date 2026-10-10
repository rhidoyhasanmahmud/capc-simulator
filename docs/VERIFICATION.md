# Chapter 5 Verification Plan

The command below executes the V1–V12 verification matrix:

```bash
capc-sim verify --config configs/dev.yaml
```

| ID | Verification target | Required result |
|---|---|---|
| V1 | Trace reproducibility | Same seed/config → same trace hash |
| V2 | Cross-treatment trace equality | Paired schedulers use the same trace hash |
| V3 | Static Atomic FIFO | Earliest **eligible** transaction is selected |
| V4 | Diagnostic FIFO | Raw oldest waiting request is selected |
| V5 | Lock exclusion | Conflicting matched-atomic transactions never overlap in service |
| V6 | Lock release | Required shard locks are released together |
| V7 | Multi-worker dispatch | Non-conflicting work can use multiple free workers |
| V8 | CAPC score | Code matches a hand-composed Eq. 4.12 calculation |
| V9 | Aging | Age contribution is monotonic and bounded at 1 |
| V10 | Accounting | Every generated transaction appears exactly once in lifecycle accounting |
| V11 | Low-load sanity | Negligible queueing when arrivals are well below service capacity |
| V12 | Overload stress | Queue grows when offered work deliberately exceeds supportable capacity |

The automated pytest suite supplements this report with unit, integration, and regression tests.

A passing development verification report demonstrates implementation consistency. It is **not** a positive CAPC performance result.
