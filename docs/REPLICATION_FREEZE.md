# Final Replication Freeze

## Purpose

This document records the final replication-count decision for the CAPC MSc thesis before any labelled CAPC comparative-performance result is inspected. It is part of the durable evidence trail for Chapters 5, 6, and 7.

This is baseline precision evidence only. It is not evidence that CAPC improves or degrades performance.

## Frozen execution provenance

- Precision-pilot executing Git revision: `282ee70e735294bde8500de15a8c376d0cfdd94c`
- Frozen primary YAML SHA-256: `be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`
- Scheduler used for replication selection: `static_atomic_fifo` only
- Fixed experimental conditions: 3 shard counts x 3 cross-shard ratios x 2 worker counts = 18 conditions
- Candidate replication counts: `{30, 40, 50, 60}`
- Precision target: 95% CI half-width for the baseline mean log-p99 `<= 0.05`
- Selection rule used: accept a candidate N only if all 18 fixed conditions meet the target; if the target is not fully met by N=60, freeze N=60 and report the residual precision limitation rather than adding post-hoc seeds.

The simulator records condition-specific effective-configuration hashes. Across the 18 fixed conditions, 18 effective configuration hashes are therefore expected.

## Candidate history

| Candidate N | Conditions passing | Conditions failing | Worst half-width | Decision |
|---:|---:|---:|---:|---|
| 30 | 16/18 | 2/18 | 0.0702766675 | Extend to N=40 |
| 40 | 16/18 | 2/18 | 0.0604617338 | Extend to N=50 |
| 50 | 16/18 | 2/18 | 0.0566600734 | Extend to N=60 |
| 60 | 16/18 | 2/18 | 0.0515515907 | Freeze N=60 with residual precision limitation |

Across all four candidates, the two conditions above the target were the four-shard, 50%-cross-shard cases with 2 and 4 workers.

## N = 60 final candidate

Additional output directory:

`results/replication_precision_n51_60_282ee70e`

Additional execution:

- Seeds: `51-60`
- Additional runs: `180`
- Regime coverage: `PASS`
- Wall time: `1586.87 s`
- User CPU time: `1486.48 s`
- System CPU time: `85.29 s`

Final combined analysis directory:

`results/replication_precision_n60_final_282ee70e`

Final combined evidence:

- Consecutive seeds represented: `1-60`
- Total Static Atomic FIFO runs represented: `1080`
- Conditions checked: `18`
- Conditions passing target: `16`
- Conditions above target: `2`

### Condition-level precision results

| Shards | Cross-shard ratio | Workers | Half-width log-p99 | Pass |
|---:|---:|---:|---:|---|
| 4 | 0.10 | 2 | 0.011967 | Yes |
| 4 | 0.10 | 4 | 0.011967 | Yes |
| 4 | 0.30 | 2 | 0.020758 | Yes |
| 4 | 0.30 | 4 | 0.020758 | Yes |
| 4 | 0.50 | 2 | 0.051552 | No |
| 4 | 0.50 | 4 | 0.051552 | No |
| 8 | 0.10 | 2 | 0.005101 | Yes |
| 8 | 0.10 | 4 | 0.005182 | Yes |
| 8 | 0.30 | 2 | 0.011696 | Yes |
| 8 | 0.30 | 4 | 0.011496 | Yes |
| 8 | 0.50 | 2 | 0.020601 | Yes |
| 8 | 0.50 | 4 | 0.014694 | Yes |
| 16 | 0.10 | 2 | 0.006055 | Yes |
| 16 | 0.10 | 4 | 0.006255 | Yes |
| 16 | 0.30 | 2 | 0.010854 | Yes |
| 16 | 0.30 | 4 | 0.007610 | Yes |
| 16 | 0.50 | 2 | 0.024233 | Yes |
| 16 | 0.50 | 4 | 0.008901 | Yes |

## Final replication decision

**Final replication count: `N = 60`.**

**Frozen seed list: consecutive seeds `1-60`.**

Decision label:

`FREEZE_N_60_WITH_PRECISION_LIMITATION`

The two residual baseline-precision limitations are:

- 4 shards, cross-shard ratio 0.50, 2 workers: half-width `0.0515515907`;
- 4 shards, cross-shard ratio 0.50, 4 workers: half-width `0.0515515907`.

These values are slightly above the target of `0.05`. Because N=60 is the maximum predeclared candidate, no additional seeds are added. The limitation must be reported transparently in the thesis rather than corrected post hoc.

## Provenance audit

Final combined audit across the precision exercise:

- Metadata files: `1080`
- All expected metadata present: `true`
- Git revisions observed: only `282ee70e735294bde8500de15a8c376d0cfdd94c`
- All runs executed on the frozen precision-pilot revision: `true`
- Scheduler set: only `static_atomic_fifo`
- Effective configuration hash count: `18`
- Expected 18 condition-specific effective configurations: `true`

## Research-integrity freeze

From this point forward:

- do not add, remove, replace, or selectively rerun seeds based on labelled CAPC effects;
- use the same frozen consecutive seed list `1-60` for every scheduler and main experimental condition;
- do not retune the frozen CAPC parameters using main comparative results;
- preserve all raw outputs and metadata;
- report the residual baseline-precision limitation explicitly;
- report achieved paired-contrast precision after the matched analyses as a diagnostic, not as a reason to add post-hoc seeds.

## Planned main comparative matrix

With `N = 60`, the main matrix is:

`3 shard counts x 3 cross-shard ratios x 2 worker counts x 5 scheduler treatments x 60 seeds = 5400 runs`.

The Static Atomic FIFO precision exercise does not substitute for this main paired comparative matrix.

## Thesis use

### Chapter 5

Use this evidence to document final experimental readiness, replication selection, provenance, seed freezing, and reproducibility controls. The two residual precision-limit cases should be reported as a transparent methodological limitation rather than hidden.

### Chapter 6

The precision exercise is setup evidence only. CAPC performance findings must come from the frozen 5400-run paired comparative matrix and the predeclared analyses.

### Chapter 7

Any conclusion about CAPC effectiveness must follow from Chapter 6 comparative evidence. The residual baseline-precision limitation can be included under limitations/threats to validity where relevant.
