# Thesis Experiment Evidence Log — Post-Main Continuation

## Purpose

This document continues `docs/EXPERIMENT_EVIDENCE_LOG.md` after the pre-main readiness gate. The earlier evidence log is retained as a historical pre-result ledger rather than rewritten retrospectively.

Entries below record completion of the frozen main experiment, integrity audit, post-processing, and RQ-specific evidence produced only after the complete matrix passed its audit.

---

## E9 — Frozen 5,400-run primary matrix completion

Status: **PASS**

Frozen execution revision:

`00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6`

Frozen raw primary configuration SHA-256:

`be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`

Completion evidence:

- planned runs: `5,400`;
- completed canonical runs: `5,400`;
- 18 conditions, each `300/300` runs;
- seeds exactly `1-60`;
- five schedulers per paired seed;
- canonical failures: `0`;
- no seed replacement.

Operational interruption/recovery evidence is preserved separately. The interrupted partial seed-47 outputs were archived outside the canonical active matrix and the full paired seed was rerun under the same frozen revision/configuration.

Interpretation: experiment execution complete; performance interpretation permitted only after E10 integrity audit.

---

## E10 — Final structural, provenance, and pairing audit

Status: **PASS**

Structural audit:

- expected runs: `5,400`;
- actual summaries: `5,400`;
- unique active run directories: `5,400`;
- missing expected runs: `0`;
- unexpected runs: `0`;
- missing metadata: `0`.

Metadata audit:

- frozen executing Git revision in `5,400/5,400` runs;
- research mode `primary` in `5,400/5,400`;
- research label `thesis-primary` in `5,400/5,400`;
- output schema `2` in `5,400/5,400`;
- path/metadata mismatches: `0`;
- missing trace/config hashes: `0`;
- execution environment signatures: `1`.

Effective configuration audit:

- fixed conditions represented: `18/18`;
- one effective configuration hash within each condition: `PASS`;
- unique effective condition hashes: `18`.

Pair audit:

- paired condition-seed groups: `1,080/1,080`;
- groups not size five: `0`;
- missing/extra scheduler sets: `0`;
- unequal trace hashes: `0`.

Interpretation: the canonical dataset is structurally complete, provenance-consistent, and exactly workload-paired across scheduler treatments.

---

## E11 — Canonical aggregate reconstruction and deterministic post-processing

Status: **PASS**

Because the matrix was completed across multiple invocations, root invocation aggregates were archived and canonical aggregates were rebuilt from the preserved per-run evidence.

Canonical files:

- `matrix_summary.csv`: `5,400` rows;
- `pair_integrity.csv`: `1,080` rows;
- `failures.json`: `[]`;
- `matrix_manifest.json`: full canonical manifest.

Raw transaction evidence:

- transaction CSV files: `5,400`;
- transaction CSV input size: approximately `50.34 GB`;
- full result directory: approximately `126 GB` at readiness check.

Memory-safe deterministic post-processing was used to avoid unsafe all-at-once concatenation while preserving the frozen analysis definitions.

Outputs:

- `starvation_by_run.csv`: `5,400` rows;
- `matrix_summary_enriched.csv`: `5,400` rows;
- `capc_vs_baseline_preservation.csv`: `1,080` rows.

No sampling was used for the reported primary analyses.

---

## E12 — RQ1 contention/burst evidence

Status: **EVIDENCE FROZEN**

Scheduler used for contention characterization: Static Atomic FIFO.

Finding:

- BURST p99 latency exceeded NORMAL p99 latency in all `18/18` fixed conditions;
- paired-bootstrap 95% interval for the BURST p99 increase was above zero in all 18 conditions;
- p99 BURST amplification increased sharply with cross-shard ratio;
- the largest mean increase was approximately `+574%` in the 4-shard/50% conditions;
- greater shard availability and, where effective, additional workers attenuated the burst amplification.

Use in Chapter 6: RQ1 results and discussion.

---

## E13 — RQ2 queue-entry predictor evidence

Status: **EVIDENCE FROZEN**

Data:

- Static Atomic FIFO runs: `1,080`;
- measurement-window cross-shard observations: `13,856,346`;
- complete-case observations: `13,856,346`;
- missing-predictor drops: `0`;
- sampling: none.

Exact random-intercept ML fit:

- groups: `1,080`;
- ICC: approximately `0.00333`;
- random-intercept variance above zero boundary.

Primary predictor coefficients on `log1p(waiting_time)`:

- arrival rate at entry: `+0.000095`, 95% CI `[0.000088, 0.000102]`;
- queue length at entry: `+0.019729`, 95% CI `[0.019720, 0.019738]`;
- dependency degree: `+0.011498`, 95% CI `[0.011426, 0.011569]`;
- active lock conflicts at entry: `+0.029507`, 95% CI `[0.029459, 0.029556]`.

All four predeclared indicators were positively associated with subsequent waiting time after model controls.

Interpretation constraint: association only; no causal claim.

---

## E14 — RQ4 primary CAPC comparative evidence

Status: **EVIDENCE FROZEN**

Primary metric: per-run p99 cross-shard end-to-end latency.

Baseline: Static Atomic FIFO.

Treatment: full CAPC.

The planned log-p99 mixed model was attempted but was inferentially unusable because the random-effects covariance was singular, estimated group variance was zero, likelihood/AIC/BIC were degenerate, the Hessian was not positive definite, and random effects could not be predicted. The failed coefficients are not used as confirmatory evidence.

The predeclared paired Wilcoxon fallback was therefore applied within each of the 18 fixed conditions and Holm-adjusted across the family.

Confirmatory counts:

- significant p99 harm: `14/18`;
- significant p99 benefit: `2/18`;
- not significant: `1/18`;
- statistically significant with zero median difference: `1/18`;
- primary p99 practical success (>=10% reduction with beneficial paired uncertainty): **`0/18`**;
- medium/high contention significant harm: **`12/12`**.

Preservation evidence across 1,080 paired CAPC-vs-Static seed units:

- throughput preservation: `100.0%`;
- Jain completion-ratio preservation: `100.0%`;
- all deterministic preservation constraints jointly pass: `56.2%`;
- p99 >=10% practical threshold pass: `0.0%`.

Ablation evidence:

- full CAPC, CAPC-No-Contention, and CAPC-No-Priority each showed harmful confidence intervals in `14/18` conditions;
- component contributions were regime-dependent;
- no single ablation provided a universal remedy.

Diagnostic evidence:

- high-priority tail waiting often improved;
- medium- and low-priority extreme waiting often worsened;
- under 8/16-shard high-contention conditions, p95 waiting could improve while p99/p99.5/max waiting worsened;
- 4-shard/50% conditions additionally showed broad queue buildup.

Interpretation: the frozen CAPC formulation did not meet its intended global p99 reduction target under the tested primary matrix. The negative/conditional result is retained without post-result retuning.

---

## E15 — Master experimental evidence freeze

Status: **PASS**

Local master evidence file:

`results/main_5400_00d4e2e/analysis_streaming/thesis_master_evidence_manifest.json`

Frozen state:

- RQ1: evidence frozen;
- RQ2: evidence frozen;
- RQ3: design question answered through design/verification evidence;
- RQ4: evidence frozen;
- primary experiment: complete and audited;
- no post-result CAPC retuning;
- no seed replacement.

Overall state:

**PRIMARY EXPERIMENT COMPLETE; RQ1, RQ2 AND RQ4 EVIDENCE FROZEN.**

---

## Chapter mapping after the primary experiment

### Chapter 5

Use E1-E11 for implementation, verification, calibration, replication, execution, provenance, canonicalization, and reproducibility evidence. Do not present these process checks as CAPC performance success.

### Chapter 6

Use E12-E14 for RQ1, RQ2, and RQ4 results. Use RQ3 design evidence from Chapter 4/5 when connecting the algorithm to the evaluation. Keep observed result, inferential evidence, diagnostic interpretation, and limitation separate.

### Chapter 7

Conclusions must preserve the failed primary practical criterion: the frozen CAPC formulation achieved `0/18` practical p99-success conditions and significantly worsened p99 in all 12 medium/high contention conditions. Any future adaptive/retuned CAPC variant must be presented as future work or a new experiment, not as a reinterpretation of the frozen primary result.

---

## Durable references

- Completion/audit record: `docs/MAIN_EXPERIMENT_COMPLETION_2026-10-16.md`
- Primary results record: `docs/PRIMARY_RESULTS_2026-10-16.md`
- Thesis evidence index: `docs/THESIS_EVIDENCE_INDEX_2026-10-16.md`
- Operational run log: `docs/MAIN_EXPERIMENT_RUN_LOG.md`
