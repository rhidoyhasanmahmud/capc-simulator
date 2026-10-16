# Thesis Evidence Reference Index — 16 Oct 2026

## Purpose

This file is the compact reference map for the CAPC MSc thesis after completion of the frozen primary experiment. It links the major research activities, integrity records, analysis outputs, and RQ-specific findings to their durable repository documentation and local evidence paths.

---

## 1. Implementation and verification

Repository records:

- `docs/COMPONENTS.md`
- `docs/VERIFICATION.md`
- `docs/DEVELOPMENT_VERIFICATION.md`
- `docs/OUTPUT_SCHEMA.md`
- `docs/THESIS_TRACEABILITY.md`

Verified state:

- automated tests: `31/31 PASS`;
- deterministic verification: `V1-V12 PASS`;
- CAPC score hand-check V8: exact match;
- atomic eligibility, locking, dispatch, aging, accounting, and trace-pair semantics verified.

Use primarily in Chapters 4 and 5.

---

## 2. Calibration and parameter freeze

Repository records:

- `docs/PARAMETER_FREEZE.md`
- `docs/EXPERIMENT_EVIDENCE_LOG.md`

Frozen raw primary configuration SHA-256:

`be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`

Key frozen CAPC values:

- arrival window: `5 s`;
- lock window: `5 s`;
- `lambda_ref = 30`;
- `queue_ref = 10`;
- equal contention weights `0.25` each;
- aging horizon `1 s`;
- ranking weights: urgency `0.35`, aging `0.30`, dependency `0.20`, lock pressure `0.15`;
- `gamma = 1`;
- contention thresholds `0.33`, `0.66`.

Research-integrity rule: no post-result retuning.

---

## 3. Replication freeze

Repository records:

- `docs/REPLICATION_PRECISION_LOG.md`
- `docs/REPLICATION_FREEZE.md`
- `docs/EXPERIMENT_EVIDENCE_LOG.md`

Frozen replication state:

- `N = 60`;
- seeds `1-60`;
- 18 fixed shard/ratio/worker conditions;
- 1,080 Static Atomic FIFO precision runs;
- residual precision limitation in 2/18 4-shard/50% conditions;
- no extra seeds added after the maximum predeclared candidate.

---

## 4. Main experiment launch, interruption, recovery, and completion

Repository records:

- `docs/MAIN_EXPERIMENT_RUN_LOG.md`
- `docs/MAIN_EXPERIMENT_CHECKPOINT_2026-10-14_1918.md`
- `docs/MAIN_EXPERIMENT_OPERATIONAL_DIAGNOSIS_2026-10-14.md`
- `docs/MAIN_EXPERIMENT_INTERRUPTION_2026-10-14.md`
- `docs/MAIN_EXPERIMENT_COMPLETION_2026-10-16.md`

Frozen execution revision:

`00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6`

Final state:

- planned runs: `5,400`;
- completed runs: `5,400`;
- failures: `0` in the canonical completed matrix;
- conditions: `18/18` complete;
- seeds: exact `1-60`;
- schedulers: exact five treatments per paired seed;
- paired condition-seed units: `1,080/1,080`;
- unequal paired trace hashes: `0`;
- per-run execution commit mismatches: `0`;
- per-run metadata files: `5,400/5,400`;
- unique effective condition hashes: `18`;
- execution environment signatures: `1`.

---

## 5. Canonical local experiment evidence

Canonical active root:

`results/main_5400_00d4e2e`

Core canonical files:

- `matrix_summary.csv` — 5,400 data rows;
- `pair_integrity.csv` — 1,080 data rows;
- `failures.json` — empty array;
- `matrix_manifest.json` — canonical 5,400-run manifest.

Audit files:

- `audit/full_integrity_audit.json`;
- `audit/metadata_provenance_5400.csv`;
- `audit/effective_config_hashes.json`;
- `audit/precanonical_root_artifacts_20261016_195452/`.

Raw transaction evidence:

- `5,400` transaction CSV files;
- approximately `50.34 GB` of transaction CSV data;
- approximately `126 GB` total final result directory at analysis-readiness check.

---

## 6. Deterministic post-processing

Local analysis root:

`results/main_5400_00d4e2e/analysis_streaming`

Core outputs:

- `starvation_by_run.csv` — 5,400 rows;
- `matrix_summary_enriched.csv` — 5,400 rows;
- `capc_vs_baseline_preservation.csv` — 1,080 rows;
- `analysis_manifest.json`.

Memory-safe streaming was used because the transaction CSV evidence was approximately 50.34 GB. The research definitions were preserved; no sampling was used for the reported primary analyses.

---

## 7. RQ1 evidence

Question focus: contention/burst effects on cross-shard latency.

Primary repository result record:

- `docs/PRIMARY_RESULTS_2026-10-16.md`

Local evidence:

- `analysis_streaming/rq1_static_latency_by_state_runlevel.csv`;
- `analysis_streaming/rq1_static_latency_by_state_summary.csv`;
- `analysis_streaming/rq1_burst_vs_normal_bootstrap.csv`.

Frozen headline result:

- BURST p99 exceeded NORMAL p99 with 95% bootstrap CI above zero in all `18/18` conditions;
- largest mean p99 burst amplification: approximately `+574%` in 4-shard/50% conditions.

Status: **EVIDENCE FROZEN**.

---

## 8. RQ2 evidence

Question focus: association of queue-entry contention indicators with subsequent waiting time.

Local evidence:

- `analysis_streaming/rq2_compact/rq2_compact_manifest.json`;
- `analysis_streaming/rq2_compact/rq2_predictor_associations.csv`;
- `analysis_streaming/rq2_compact/rq2_exact_random_intercept_coefficients.csv`;
- `analysis_streaming/rq2_compact/rq2_exact_random_intercept_model.json`.

Frozen model evidence:

- observations: `13,856,346`;
- groups: `1,080`;
- sampling: none;
- active-lock conflicts, queue length, dependency degree, and arrival rate all positively associated with later `log1p(waiting_time)`;
- interpretation is associative, not causal.

Status: **EVIDENCE FROZEN**.

---

## 9. RQ3 evidence

Question focus: design an atomicity-preserving contention-aware priority coordination mechanism.

Evidence is primarily design/verification rather than inferential:

- `docs/COMPONENTS.md`;
- `docs/THESIS_TRACEABILITY.md`;
- `docs/VERIFICATION.md`;
- frozen CAPC configuration and Chapter 4 design specification.

Status: **DESIGN QUESTION — ANSWER THROUGH CHAPTER 4 + CHAPTER 5 VERIFICATION**.

---

## 10. RQ4 evidence

Question focus: CAPC vs matched Static Atomic FIFO under the frozen primary matrix.

Primary repository result record:

- `docs/PRIMARY_RESULTS_2026-10-16.md`

Local confirmatory files:

- `analysis_streaming/primary_p99_capc_vs_static.csv`;
- `analysis_streaming/primary_p99_wilcoxon_holm.csv`;
- `analysis_streaming/primary_p99_confirmatory_summary.csv`;
- `analysis_streaming/primary_mixed_model_fallback_note.txt`;
- `analysis_streaming/rq4_final_evidence_register.csv`;
- `analysis_streaming/rq4_thesis_compact_table.csv`;
- `analysis_streaming/rq4_evidence_freeze.json`.

Ablation/diagnostic files:

- `analysis_streaming/p99_ablation_vs_static.csv`;
- `analysis_streaming/direct_ablation_component_effect.csv`;
- `analysis_streaming/capc_queue_lock_diagnostics.csv`;
- `analysis_streaming/extreme_wait_tail_diagnostic.csv`.

Frozen headline results:

- significant p99 harm: `14/18` conditions;
- significant p99 benefit: `2/18` conditions, both small low-contention 8-shard effects;
- not significant: `1/18`;
- statistically significant with zero median difference: `1/18`;
- predeclared primary p99 practical success: `0/18`;
- medium/high contention significant harm: `12/12`;
- throughput preservation: `100%` of 1,080 CAPC-vs-Static seed pairs;
- Jain preservation: `100%`;
- all deterministic preservation constraints jointly pass: `56.2%` of seed pairs.

Status: **EVIDENCE FROZEN**.

---

## 11. Master evidence freeze

Local master evidence file:

`analysis_streaming/thesis_master_evidence_manifest.json`

Frozen state:

- RQ1: evidence frozen;
- RQ2: evidence frozen;
- RQ3: design question;
- RQ4: evidence frozen;
- primary experiment: complete;
- integrity audit: pass;
- no post-result retuning;
- no seed replacement.

Overall experimental state:

**PRIMARY EXPERIMENT COMPLETE; RQ1, RQ2 AND RQ4 EVIDENCE FROZEN.**

---

## 12. Chapter use

### Chapter 5

Use implementation, verification, reproducibility, configuration freeze, and experiment-readiness evidence. Do not present readiness evidence as CAPC performance evidence.

### Chapter 6

Use the completed/audited primary dataset and the frozen RQ1, RQ2, and RQ4 evidence. Keep observation, statistical evidence, and interpretation distinct.

### Chapter 7

Conclusions must follow the frozen Chapter 6 evidence. In particular, do not claim that the frozen CAPC formulation achieved the intended global p99 reduction; the predeclared practical p99 success criterion was not met in any of the 18 conditions.
