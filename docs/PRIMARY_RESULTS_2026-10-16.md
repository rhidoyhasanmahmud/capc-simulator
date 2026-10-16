# Frozen Primary Experiment Results — 16 Oct 2026

## Scope

This document records the verified post-audit findings from the frozen 5,400-run primary experiment for the MSc thesis.

The experiment and integrity audit are documented in `docs/MAIN_EXPERIMENT_COMPLETION_2026-10-16.md`.

These results were produced only after:

- all `5,400/5,400` runs completed;
- structural coverage passed;
- all 5,400 per-run metadata records verified the frozen execution revision;
- all `1,080/1,080` condition-seed groups passed exact trace-pair integrity;
- the canonical full matrix was rebuilt from per-run evidence.

Frozen execution revision:

`00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6`

Frozen raw primary YAML SHA-256:

`be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`

No CAPC parameter was retuned after observing these primary results.

---

## Primary analysis hierarchy

- Principal matched baseline: `static_atomic_fifo`.
- Treatment of interest: `capc`.
- Diagnostic FIFO: descriptive only; excluded from matched atomic causal comparisons.
- Primary RQ4 metric: per-run p99 cross-shard end-to-end latency.
- Primary practical effect criterion: at least `10%` p99 reduction with beneficial paired uncertainty, subject to preservation constraints.
- Paired uncertainty: `10,000`-resample paired bootstrap.
- Planned mixed model: log-p99 mixed-effects model with seed random intercept.
- Predeclared fallback if mixed model unusable: paired Wilcoxon within condition plus Holm adjustment.

---

# RQ1 — Contention and burst effects on cross-shard latency

## Question focus

How do contention conditions affect mean, p95, and p99 cross-shard latency under NORMAL and BURST workload states?

RQ1 was evaluated on the matched Static Atomic FIFO baseline so that the contention characterization was not confounded by CAPC scheduling.

## Main finding

BURST p99 latency exceeded NORMAL p99 latency in **all 18 shard/ratio/worker conditions**, and the paired-bootstrap 95% interval for the BURST increase was above zero in every condition.

### BURST increase in p99 latency relative to NORMAL

| Shards | Cross-shard ratio | Workers | Mean BURST increase in p99 | 95% CI |
|---:|---:|---:|---:|---:|
| 4 | 0.10 | 2 | +37.32% | +35.11% to +39.56% |
| 4 | 0.10 | 4 | +37.32% | +35.11% to +39.56% |
| 4 | 0.30 | 2 | +155.07% | +149.95% to +160.42% |
| 4 | 0.30 | 4 | +155.07% | +149.95% to +160.42% |
| 4 | 0.50 | 2 | +574.14% | +533.63% to +617.26% |
| 4 | 0.50 | 4 | +574.14% | +533.63% to +617.26% |
| 8 | 0.10 | 2 | +20.31% | +18.72% to +22.05% |
| 8 | 0.10 | 4 | +20.01% | +18.40% to +21.78% |
| 8 | 0.30 | 2 | +68.06% | +66.33% to +69.87% |
| 8 | 0.30 | 4 | +64.13% | +62.34% to +65.96% |
| 8 | 0.50 | 2 | +147.55% | +143.19% to +152.21% |
| 8 | 0.50 | 4 | +112.72% | +110.54% to +115.06% |
| 16 | 0.10 | 2 | +20.15% | +18.70% to +21.63% |
| 16 | 0.10 | 4 | +19.86% | +18.26% to +21.49% |
| 16 | 0.30 | 2 | +46.49% | +45.27% to +47.72% |
| 16 | 0.30 | 4 | +34.14% | +33.25% to +35.04% |
| 16 | 0.50 | 2 | +139.52% | +133.86% to +145.28% |
| 16 | 0.50 | 4 | +55.36% | +54.26% to +56.49% |

Additional descriptive observations:

- 4 shards, 50% cross-shard, 2 workers: NORMAL p99 `0.277 s`, BURST p99 `1.813 s`.
- 8 shards, 50%, 2 workers: NORMAL p99 `0.137 s`, BURST p99 `0.338 s`.
- 16 shards, 50%, 2 workers: NORMAL p99 `0.112 s`, BURST p99 `0.267 s`.
- 16 shards, 50%, 4 workers: NORMAL p99 `0.108 s`, BURST p99 `0.167 s`.

Interpretation: higher cross-shard ratio substantially amplifies BURST tail latency. Greater shard availability and, where lock concurrency permits, additional workers attenuate that amplification. The identical 2-worker and 4-worker results in the 4-shard conditions are consistent with the atomic shard-lock model imposing the effective concurrency limit in that regime.

Local evidence files:

- `analysis_streaming/rq1_static_latency_by_state_runlevel.csv`;
- `analysis_streaming/rq1_static_latency_by_state_summary.csv`;
- `analysis_streaming/rq1_burst_vs_normal_bootstrap.csv`.

RQ1 evidence status: **FROZEN**.

---

# RQ2 — Queue-entry indicators and subsequent waiting

## Question focus

Are queue-entry-time arrival rate, queue length, shard dependency degree, and transaction-specific active-lock conflict count associated with subsequent cross-shard waiting time?

RQ2 used Static Atomic FIFO transactions only.

Data used:

- Static Atomic FIFO runs: `1,080/1,080`;
- measurement-window cross-shard observations: `13,856,346`;
- complete-case observations: `13,856,346`;
- rows dropped for missing predictors: `0`;
- run groups: `1,080`;
- sampling: **none**.

The model outcome was `log1p(waiting_time)` with a random intercept by run ID. Because the raw transaction table was too large for a safe all-at-once DataFrame/Statsmodels workflow, the exact Gaussian random-intercept ML likelihood was fit using per-group sufficient statistics without sampling or reweighting observations.

Model status:

- optimizer success: `True`;
- residual variance `sigma^2`: `0.0028907215`;
- random-intercept variance `tau^2`: `9.6627083e-06`;
- ICC: `0.00333153`;
- random-intercept boundary zero: `No`.

## Primary predictor associations

| Predictor | Coefficient on log1p(wait) | 95% CI | Direction |
|---|---:|---:|---|
| Arrival rate at entry | +0.000095 | +0.000088 to +0.000102 | Positive |
| Queue length at entry | +0.019729 | +0.019720 to +0.019738 | Positive |
| Dependency degree | +0.011498 | +0.011426 to +0.011569 | Positive |
| Active lock conflicts at entry | +0.029507 | +0.029459 to +0.029556 | Positive |

All four predeclared predictors showed positive associations with subsequent waiting time after controlling for workload state, shard count, cross-shard ratio, and worker count.

Important interpretation constraint: these are **associations**, not causal effects. Coefficient magnitudes are on different native predictor scales; therefore they must not be treated as standardized importance scores.

Local evidence files:

- `analysis_streaming/rq2_compact/rq2_predictor_associations.csv`;
- `analysis_streaming/rq2_compact/rq2_exact_random_intercept_coefficients.csv`;
- `analysis_streaming/rq2_compact/rq2_exact_random_intercept_model.json`;
- `analysis_streaming/rq2_compact/rq2_compact_manifest.json`.

RQ2 evidence status: **FROZEN**.

---

# RQ3 — CAPC design question

RQ3 is a system/algorithm-design question rather than a standalone inferential experiment.

The answer is supported by the frozen CAPC design and Chapter 5 verification evidence:

- atomic eligibility filtering before ranking;
- urgency, aging, dependency, and recent lock-pressure ranking terms;
- contention amplification using frozen global contention indicators;
- deterministic tie-breaking;
- non-preemptive service;
- all-or-nothing shard locking;
- no online retuning;
- verified implementation semantics and V1-V12 checks.

RQ3 performance claims must not be inferred from design verification alone.

---

# RQ4 — CAPC comparative evaluation

## Primary p99 result

CAPC was compared with Static Atomic FIFO using 60 paired seeds within each of the 18 shard/ratio/worker conditions.

The planned log-p99 mixed-effects model was attempted first. It was not considered inferentially usable because:

- random-effects covariance was singular;
- estimated group variance was zero;
- log-likelihood was infinite;
- AIC/BIC were negative infinite;
- the Hessian was not positive definite;
- random effects could not be predicted from the singular covariance structure.

Accordingly, the predeclared fallback was used: paired Wilcoxon tests within each condition, followed by Holm adjustment across the 18 planned condition tests. The failed mixed-model coefficients are not used as confirmatory evidence.

## Confirmatory p99 summary

Positive reduction means CAPC lowered p99. Negative reduction means CAPC increased p99.

| Shards | Ratio | Workers | Mean p99 reduction | Bootstrap 95% CI | Median reduction | Holm-adjusted p | Classification |
|---:|---:|---:|---:|---:|---:|---:|---|
| 4 | 0.10 | 2 | -1.79% | -2.35% to -1.23% | -2.09% | 6.05e-06 | Significant harm |
| 4 | 0.10 | 4 | -1.79% | -2.35% to -1.23% | -2.09% | 6.05e-06 | Significant harm |
| 4 | 0.30 | 2 | -66.90% | -70.65% to -63.07% | -67.74% | 2.93e-10 | Significant harm |
| 4 | 0.30 | 4 | -66.90% | -70.65% to -63.07% | -67.74% | 2.93e-10 | Significant harm |
| 4 | 0.50 | 2 | -796.38% | -880.62% to -719.62% | -713.90% | 2.93e-10 | Significant harm |
| 4 | 0.50 | 4 | -796.38% | -880.62% to -719.62% | -713.90% | 2.93e-10 | Significant harm |
| 8 | 0.10 | 2 | +0.32% | +0.16% to +0.48% | +0.24% | 1.28e-03 | Significant benefit |
| 8 | 0.10 | 4 | +0.34% | +0.18% to +0.50% | +0.18% | 3.82e-04 | Significant benefit |
| 8 | 0.30 | 2 | -8.85% | -9.64% to -8.04% | -9.21% | 2.93e-10 | Significant harm |
| 8 | 0.30 | 4 | -7.00% | -7.62% to -6.37% | -7.03% | 2.93e-10 | Significant harm |
| 8 | 0.50 | 2 | -44.05% | -46.35% to -41.60% | -45.42% | 2.93e-10 | Significant harm |
| 8 | 0.50 | 4 | -23.38% | -24.80% to -21.97% | -23.70% | 2.93e-10 | Significant harm |
| 16 | 0.10 | 2 | +0.10% | +0.02% to +0.19% | 0.00% | 5.47e-02 | Not significant |
| 16 | 0.10 | 4 | +0.11% | +0.02% to +0.20% | 0.00% | 2.62e-03 | Significant distribution shift; zero median |
| 16 | 0.30 | 2 | -4.22% | -4.74% to -3.68% | -4.39% | 2.93e-10 | Significant harm |
| 16 | 0.30 | 4 | -0.49% | -0.73% to -0.26% | -0.28% | 1.28e-03 | Significant harm |
| 16 | 0.50 | 2 | -32.72% | -34.85% to -30.46% | -32.92% | 2.93e-10 | Significant harm |
| 16 | 0.50 | 4 | -3.88% | -4.17% to -3.58% | -3.68% | 2.93e-10 | Significant harm |

Confirmatory counts:

- significant harm: `14/18`;
- significant benefit: `2/18`;
- not significant: `1/18`;
- statistically significant with zero median difference: `1/18`;
- predeclared primary p99 practical success: **`0/18`**;
- medium/high contention conditions with significant harm: **`12/12`**.

Therefore the frozen CAPC formulation did **not** achieve the predeclared p99 improvement criterion.

The two statistically beneficial 8-shard low-contention effects were only about `0.3%`, far below the `10%` practical threshold.

### Absolute p99 examples

- 4 shards, 50%, 2 workers: Static mean p99 `1.521 s`, CAPC mean p99 `13.875 s` (`9.12x` Static by ratio of means).
- 8 shards, 50%, 2 workers: Static `0.281 s`, CAPC `0.405 s`.
- 16 shards, 50%, 2 workers: Static `0.221 s`, CAPC `0.294 s`.
- 16 shards, 50%, 4 workers: Static `0.141 s`, CAPC `0.147 s`.

---

## Preservation results

Across the `1,080` paired CAPC-vs-Static condition-seed units:

- throughput preservation criterion pass rate: **100.0%**;
- Jain completion-ratio preservation criterion pass rate: **100.0%**;
- all preservation constraints jointly passed in **56.2%** of seed pairs;
- primary p99 >=10% practical threshold pass rate: **0.0%**.

Important: the deterministic preservation table does not itself declare overall CAPC success; it evaluates per-seed practical/preservation constraints only.

Selected low-priority p95 waiting changes illustrate the main QoS concern:

- 4 shards, 30%: approximately `+56.1%`;
- 4 shards, 50%: approximately `+543.7%`;
- 8 shards, 50%, 2 workers: approximately `+43.8%`;
- 8 shards, 50%, 4 workers: approximately `+26.1%`;
- 16 shards, 50%, 2 workers: approximately `+41.5%`;
- 16 shards, 50%, 4 workers: approximately `+4.5%`.

Queue-stability preservation was generally high, but the 4-shard/50% conditions reached only `70%` stable CAPC runs.

---

## Ablation results

Mean p99 reduction versus Static Atomic FIFO; positive is better than Static, negative is worse.

| Shards | Ratio | Workers | Full CAPC | No contention | No priority |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.10 | 2 | -1.79% | -1.92% | -0.63% |
| 4 | 0.10 | 4 | -1.79% | -1.92% | -0.63% |
| 4 | 0.30 | 2 | -66.90% | -53.62% | -78.84% |
| 4 | 0.30 | 4 | -66.90% | -53.62% | -78.84% |
| 4 | 0.50 | 2 | -796.38% | -425.61% | -1179.57% |
| 4 | 0.50 | 4 | -796.38% | -425.61% | -1179.57% |
| 8 | 0.10 | 2 | +0.32% | +0.31% | +0.21% |
| 8 | 0.10 | 4 | +0.34% | +0.32% | +0.25% |
| 8 | 0.30 | 2 | -8.85% | -9.01% | -4.83% |
| 8 | 0.30 | 4 | -7.00% | -7.20% | -4.04% |
| 8 | 0.50 | 2 | -44.05% | -38.16% | -37.82% |
| 8 | 0.50 | 4 | -23.38% | -20.75% | -18.81% |
| 16 | 0.10 | 2 | +0.10% | +0.11% | +0.05% |
| 16 | 0.10 | 4 | +0.11% | +0.11% | +0.02% |
| 16 | 0.30 | 2 | -4.22% | -4.40% | -2.09% |
| 16 | 0.30 | 4 | -0.49% | -0.53% | -0.17% |
| 16 | 0.50 | 2 | -32.72% | -30.66% | -22.28% |
| 16 | 0.50 | 4 | -3.88% | -3.94% | -2.16% |

All three CAPC variants were harmful by confidence interval in `14/18` conditions. Therefore no single removed component solves the global tail-latency problem.

Direct full-CAPC-versus-ablation comparisons showed regime dependence:

- the priority contribution helped full CAPC relative to No-Priority in the constrained 4-shard medium/high conditions, but was harmful in many 8/16-shard medium/high conditions;
- the contention contribution was strongly harmful in 4-shard medium/high conditions, mildly helpful in several moderate 8/16-shard conditions, and again harmful in several high-contention conditions.

Because there is no factorial double-ablation with both priority and contention removed, interaction effects should be discussed as a plausible interpretation rather than uniquely identified causal components.

---

## Diagnostic tail-degradation evidence

A major diagnostic pattern was **tail polarization**: p95 waiting could improve or remain close to baseline while p99/p99.5/max waiting deteriorated sharply.

Selected CAPC-vs-Static waiting-tail changes:

| Condition | p95 wait | p99 wait | p99.5 wait | Max wait | High-priority p99 | Medium-priority p99 | Low-priority p99 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 4 shards, 50%, w2 | +52.3% | +839.5% | +1159.6% | +1800.5% | -42.0% | +488.0% | +1698.0% |
| 8 shards, 50%, w2 | -4.2% | +54.2% | +85.0% | +250.7% | -20.1% | +41.7% | +102.3% |
| 16 shards, 50%, w2 | -10.7% | +43.1% | +73.7% | +281.5% | -37.0% | +22.5% | +98.2% |
| 16 shards, 50%, w4 | -2.8% | +6.4% | +13.2% | +53.2% | -11.2% | +3.9% | +21.4% |

This supports the interpretation that the frozen CAPC ordering often protected the high-priority tail while redistributing extreme waiting toward medium- and especially low-priority transactions.

The most constrained case, 4 shards / 50% cross-shard ratio, also showed broad queue buildup rather than only extreme-tail redistribution:

- mean waiting approximately `+181%`;
- mean queue length approximately `+184%`;
- max queue length approximately `+166%`.

Worker utilization remained effectively unchanged, so the observed deterioration is more consistent with service-order/lock-eligibility queue dynamics than with a reduction in nominal worker capacity. This is an interpretation of the controlled model, not a claim about production blockchain networks.

---

# Overall evidence-constrained interpretation

The primary experiment does not support the claim that this frozen CAPC formulation reduces global cross-shard p99 latency under the tested medium/high contention regimes.

What the experiment does establish is:

1. BURST conditions materially amplify cross-shard tail latency, especially at high cross-shard ratios and low shard counts.
2. Queue-entry arrival rate, queue length, dependency degree, and active lock conflicts are all positively associated with subsequent waiting time.
3. The CAPC design preserves throughput and completion-ratio fairness well in this simulator, but does not meet the predeclared p99 improvement target.
4. Under medium/high contention, CAPC significantly worsens p99 in all 12 tested conditions.
5. The deterioration is strongly distributional: high-priority waiting can improve while medium/low-priority extreme tails worsen.
6. Priority and contention terms are regime-dependent; neither single ablation provides a universal remedy.

This is a valid negative/conditional research result. It should be reported without post-result retuning or reframing the failed primary criterion as a success.

---

## Local evidence index

Primary confirmatory and diagnostic files under `results/main_5400_00d4e2e/analysis_streaming/` include:

- `primary_p99_capc_vs_static.csv`;
- `primary_p99_wilcoxon_holm.csv`;
- `primary_p99_confirmatory_summary.csv`;
- `primary_mixed_model_fallback_note.txt`;
- `capc_vs_baseline_preservation.csv`;
- `p99_ablation_vs_static.csv`;
- `direct_ablation_component_effect.csv`;
- `capc_queue_lock_diagnostics.csv`;
- `extreme_wait_tail_diagnostic.csv`;
- `rq1_static_latency_by_state_runlevel.csv`;
- `rq1_static_latency_by_state_summary.csv`;
- `rq1_burst_vs_normal_bootstrap.csv`;
- `rq2_compact/rq2_predictor_associations.csv`;
- `rq2_compact/rq2_exact_random_intercept_coefficients.csv`;
- `rq2_compact/rq2_exact_random_intercept_model.json`;
- `rq4_final_evidence_register.csv`;
- `rq4_thesis_compact_table.csv`;
- `rq4_evidence_freeze.json`;
- `thesis_master_evidence_manifest.json`.

Master experimental evidence freeze status:

**PRIMARY EXPERIMENT COMPLETE; RQ1, RQ2 AND RQ4 EVIDENCE FROZEN.**
