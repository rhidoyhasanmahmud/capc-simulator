# Experiment Protocol Summary

## Main predeclared factors

- logical shards: 4, 8, 16;
- cross-shard ratios: 10%, 30%, 50%;
- coordination workers: 2, 4;
- five scheduler treatments;
- frozen consecutive seed list `1..N`.

Main matrix size: `3 × 3 × 2 × 5 × N = 90N` runs.

## Workload

- NORMAL: 20 tx/s;
- BURST: 60 tx/s;
- `q_NB = 0.02 s^-1`;
- `q_BN = 0.10 s^-1`;
- run horizon: 1,800 s;
- warm-up: 180 s;
- initial state: NORMAL.

## Cross-shard model

- 2/3-shard dependency mix: 80% / 20%;
- High/Medium/Low priority: 20% / 50% / 30%;
- coordination service: Uniform(40,60) ms;
- all-or-nothing shard locks;
- non-preemptive matched-atomic service.

## Treatments

1. Diagnostic FIFO — descriptive, non-atomic queue-order reference.
2. Static Atomic FIFO — principal matched baseline.
3. Full CAPC.
4. CAPC-No-Contention.
5. CAPC-No-Priority.

## Primary endpoint

Per-run p99 cross-shard end-to-end latency.

## Supporting outcomes

p95, mean/median latency, waiting, service time, queue length, throughput, fairness, starvation, unfinished work, and stability/recovery.

## Before main execution

- freeze CAPC parameters;
- freeze source revision;
- freeze configuration revision/hash;
- run tests and V1–V12 verification;
- complete neutral pilot;
- freeze replication count `N`;
- preserve the seed list and all raw outputs.
