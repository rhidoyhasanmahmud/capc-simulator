# Baseline Replication Precision Log

## Purpose

This file records the Static Atomic FIFO-only replication-count selection evidence used before any labelled CAPC comparative experiment. It is part of the thesis evidence trail for Chapters 5-7 and must not be interpreted as CAPC performance evidence.

## Frozen execution provenance

- Executing Git revision: `282ee70e735294bde8500de15a8c376d0cfdd94c`
- Frozen primary YAML SHA-256: `be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`
- Scheduler used for precision selection: `static_atomic_fifo` only
- Experimental conditions: 3 shard counts x 3 cross-shard ratios x 2 worker counts = 18 conditions
- Candidate replication counts: `{30, 40, 50, 60}`
- Precision target: 95% CI half-width for baseline mean log-p99 `<= 0.05`
- Conservative selection rule used in the analysis: the candidate N is accepted only if all 18 fixed conditions meet the target.

The simulator hashes each condition-specific effective configuration, so 18 effective configuration hashes are expected across the 18 matrix conditions.

---

## N = 30 candidate

Output directory:

`results/replication_precision_n30_282ee70e`

Execution:

- Seeds: `1-30`
- Runs: `540`
- Regime coverage: `PASS`
- Wall time: `5622.59 s`
- User CPU time: `4388.57 s`
- System CPU time: `237.12 s`

Condition-level precision result:

| Shards | Cross-shard ratio | Workers | Half-width log-p99 | Pass |
|---:|---:|---:|---:|---|
| 4 | 0.10 | 2 | 0.015614 | Yes |
| 4 | 0.10 | 4 | 0.015614 | Yes |
| 4 | 0.30 | 2 | 0.027124 | Yes |
| 4 | 0.30 | 4 | 0.027124 | Yes |
| 4 | 0.50 | 2 | 0.070277 | No |
| 4 | 0.50 | 4 | 0.070277 | No |
| 8 | 0.10 | 2 | 0.006826 | Yes |
| 8 | 0.10 | 4 | 0.006791 | Yes |
| 8 | 0.30 | 2 | 0.013889 | Yes |
| 8 | 0.30 | 4 | 0.013948 | Yes |
| 8 | 0.50 | 2 | 0.024317 | Yes |
| 8 | 0.50 | 4 | 0.015920 | Yes |
| 16 | 0.10 | 2 | 0.007361 | Yes |
| 16 | 0.10 | 4 | 0.007381 | Yes |
| 16 | 0.30 | 2 | 0.011885 | Yes |
| 16 | 0.30 | 4 | 0.010065 | Yes |
| 16 | 0.50 | 2 | 0.031038 | Yes |
| 16 | 0.50 | 4 | 0.010729 | Yes |

Summary:

- Conditions passed: `16/18`
- Conditions failed: `2/18`
- Worst condition: shards `4`, cross-shard ratio `0.50`, workers `2`
- Worst half-width: `0.07027666748626817`
- Decision: `EXTEND_TO_N_40`

Provenance audit:

- Metadata files: `540`
- Git commits: only `282ee70e735294bde8500de15a8c376d0cfdd94c`
- Scheduler set: only `static_atomic_fifo`
- Effective configuration hashes: `18`, one per fixed condition

---

## N = 40 candidate

Additional output directory:

`results/replication_precision_n31_40_282ee70e`

Additional execution:

- Seeds: `31-40`
- Additional runs: `180`
- Regime coverage: `PASS`
- Wall time: `2280.31 s`
- User CPU time: `2088.32 s`
- System CPU time: `119.08 s`

Combined analysis directory:

`results/replication_precision_n40_combined_282ee70e`

Combined evidence:

- Seeds: `1-40`
- Total runs represented: `720`

Condition-level precision result:

| Shards | Cross-shard ratio | Workers | Half-width log-p99 | Pass |
|---:|---:|---:|---:|---|
| 4 | 0.10 | 2 | 0.013468 | Yes |
| 4 | 0.10 | 4 | 0.013468 | Yes |
| 4 | 0.30 | 2 | 0.024025 | Yes |
| 4 | 0.30 | 4 | 0.024025 | Yes |
| 4 | 0.50 | 2 | 0.060462 | No |
| 4 | 0.50 | 4 | 0.060462 | No |
| 8 | 0.10 | 2 | 0.006023 | Yes |
| 8 | 0.10 | 4 | 0.006007 | Yes |
| 8 | 0.30 | 2 | 0.013218 | Yes |
| 8 | 0.30 | 4 | 0.013398 | Yes |
| 8 | 0.50 | 2 | 0.022545 | Yes |
| 8 | 0.50 | 4 | 0.016038 | Yes |
| 16 | 0.10 | 2 | 0.006817 | Yes |
| 16 | 0.10 | 4 | 0.007225 | Yes |
| 16 | 0.30 | 2 | 0.012098 | Yes |
| 16 | 0.30 | 4 | 0.009180 | Yes |
| 16 | 0.50 | 2 | 0.028365 | Yes |
| 16 | 0.50 | 4 | 0.009993 | Yes |

Summary:

- Conditions passed: `16/18`
- Conditions failed: `2/18`
- Worst condition: shards `4`, cross-shard ratio `0.50`, workers `2`
- Worst half-width: `0.060461733801890384`
- Decision: `EXTEND_TO_N_50`

Combined provenance audit:

- Metadata files: `720`
- All 720 metadata files present: `true`
- Git commits: only `282ee70e735294bde8500de15a8c376d0cfdd94c`
- All runs on frozen Git revision: `true`
- Scheduler set: only `static_atomic_fifo`
- Only Static Atomic FIFO: `true`
- Effective configuration hash count: `18`
- Expected 18 condition-specific effective configurations: `true`

---

## Interpretation boundary

The N=30 and N=40 exercises are baseline precision evidence only. They determine replication sufficiency before labelled CAPC comparative effects are inspected. They are not evidence that CAPC improves or degrades latency, throughput, fairness, starvation, or stability.

At N=40, the same two high cross-shard-demand four-shard conditions remain above the predeclared 0.05 precision threshold, so the protocol requires extension to N=50 using consecutive seeds `41-50` only. Existing seeds are not rerun, removed, or replaced.

## Next step

Run Static Atomic FIFO for seeds `41-50` across all 18 conditions, combine with seeds `1-40`, and evaluate the N=50 candidate using the same condition-level log-p99 half-width rule. If any condition still exceeds 0.05, extend once more to N=60 using seeds `51-60`.