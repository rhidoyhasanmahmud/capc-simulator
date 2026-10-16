# Main Experiment Completion and Final Integrity Audit — 16 Oct 2026

## Purpose

This document records the final operational completion, recovery history, provenance audit, canonical matrix reconstruction, and analysis-readiness state of the frozen 5,400-run CAPC primary comparative experiment.

It complements the earlier execution records in:

- `docs/MAIN_EXPERIMENT_RUN_LOG.md`;
- `docs/MAIN_EXPERIMENT_INTERRUPTION_2026-10-14.md`;
- `docs/MAIN_EXPERIMENT_OPERATIONAL_DIAGNOSIS_2026-10-14.md`.

This file is an execution/integrity record. Comparative performance findings are recorded separately in `docs/PRIMARY_RESULTS_2026-10-16.md`.

---

## Frozen experiment identity

Frozen execution Git revision:

`00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6`

Frozen raw `configs/primary.yaml` SHA-256:

`be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`

Primary design:

- logical shards: `4, 8, 16`;
- cross-shard ratios: `0.10, 0.30, 0.50`;
- coordination workers: `2, 4`;
- schedulers: `diagnostic_fifo`, `static_atomic_fifo`, `capc`, `capc_no_contention`, `capc_no_priority`;
- seeds: consecutive `1-60`;
- conditions: `18`;
- paired condition-seed units: `18 x 60 = 1,080`;
- planned runs: `18 x 60 x 5 = 5,400`.

The experiment used one exogenous trace per condition/seed and replayed that trace across the five scheduler treatments.

---

## Original launch and interruption

The original 5,400-run process was launched on 13 Oct 2026 from the frozen execution revision. Operational-only monitoring was used while the process was active; interim CAPC-versus-baseline effects were not inspected.

A host shutdown interrupted the process on 14 Oct 2026. After reboot, the active output tree contained:

- four complete 300-run condition blocks = `1,200` runs;
- `sh4_x50_w2`, seeds `1-46`, complete across all five schedulers = `230` runs;
- seed `47`, Diagnostic FIFO and Static Atomic FIFO only = `2` partial scheduler outputs.

Total observed summaries immediately after interruption: `1,432`.

The two partial seed-47 scheduler directories were preserved in a separate interruption archive rather than deleted. The active research tree was therefore returned to `1,430` complete, pair-safe outputs before recovery.

No seed was replaced or substituted.

---

## Recovery of interrupted condition

A recovery invocation reran the full scheduler set for `sh4_x50_w2`, seeds `47-60`, on the same frozen execution revision and configuration.

Recovery invocation result:

- planned runs: `70`;
- completed runs: `70`;
- failures: `0`;
- paired seed rows: `14`;
- paired-trace integrity: `PASS`.

After this recovery the first five 300-run research condition blocks were complete, giving `1,500` active per-run summaries.

The interrupted partial outputs remain archived outside the active canonical research tree as historical recovery evidence.

---

## Resumable completion driver

To reduce host-interruption risk, the remaining matrix was executed using an operational resumable shell driver in 10-seed chunks.

The research design did not change: each research condition still contained 60 seeds x 5 schedulers = 300 runs. The 10-seed chunking was only an execution-resilience mechanism.

Key driver controls:

- exact frozen Git revision guard;
- exact raw primary YAML SHA-256 guard;
- clean-working-tree guard at chunk boundaries;
- five required scheduler outputs per seed;
- automatic preservation/archive of any incomplete seed before a full paired rerun;
- invocation-level failure check;
- invocation-level paired-trace integrity check;
- completed-chunk marker and progress log;
- automatic skip of already complete paired seeds on restart.

The resumable remaining-matrix driver was launched on 15 Oct 2026 at approximately 21:34 +08 from an active count of `1,500` summaries.

It completed the remaining `3,900` runs without changing the frozen simulator/configuration semantics.

---

## Final completion

Final monitor state on 16 Oct 2026:

- completed per-run summaries: `5,400 / 5,400`;
- progress: `100.0%`;
- final chunk: `sh16_x50_w4_seed051_060`;
- final chunk integrity: `50/50` runs, `10` paired seed rows, `PASS`;
- driver final message: `SUCCESS: 5400 / 5400 per-run summaries present.`;
- driver process exited after successful completion;
- no simulator process remained active.

The last run outputs were written on 16 Oct 2026 at approximately 19:44 +08.

---

## Structural coverage audit

Canonical active output root:

`results/main_5400_00d4e2e`

Structural audit results:

- expected runs: `5,400`;
- actual `summary.json` files: `5,400`;
- unique run directories: `5,400`;
- missing expected runs: `0`;
- unexpected runs: `0`;
- missing `metadata.json`: `0`.

Every one of the 18 shard/ratio/worker conditions contained exactly `300/300` active runs.

Structural coverage: **PASS**.

---

## Per-run execution provenance audit

All 5,400 `metadata.json` files were audited.

Results:

- executing Git commit: `00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6` in `5,400/5,400` runs;
- research mode: `primary` in `5,400/5,400` runs;
- research label: `thesis-primary` in `5,400/5,400` runs;
- output schema version: `2` in `5,400/5,400` runs;
- bad run IDs: `0`;
- scheduler/path mismatches: `0`;
- seed/path mismatches: `0`;
- bad seed ranges: `0`;
- missing trace hashes: `0`;
- missing effective configuration hashes: `0`.

Observed execution environment was identical across all 5,400 runs:

- machine: `x86_64`;
- platform: `macOS-15.7.9-x86_64-i386-64bit-Mach-O`;
- Python: `3.14.0`;
- physical memory: `34,359,738,368` bytes;
- PyYAML `6.0.3`;
- matplotlib `3.11.2`;
- numpy `2.5.4`;
- pandas `3.0.6`;
- scipy `1.18.1`;
- statsmodels `0.15.0`.

A later documentation checkout state must not be confused with execution provenance: the authoritative execution identity is the per-run metadata, which records the frozen execution revision in all 5,400 final runs.

---

## Effective configuration audit

For each fixed shard/ratio/worker condition, all scheduler/seed runs shared one effective configuration hash.

Results:

- conditions represented: `18/18`;
- one effective configuration hash within each condition: `PASS`;
- unique effective condition hashes: `18/18`.

The condition-specific effective hashes are expected to differ because shard count, cross-shard ratio, and worker count are part of the effective configuration.

---

## Paired-trace integrity audit

Condition/seed grouping produced exactly `1,080` paired units.

Results:

- paired condition-seed groups: `1,080/1,080`;
- groups not containing exactly five scheduler runs: `0`;
- groups with missing/extra schedulers: `0`;
- groups with unequal trace hashes across schedulers: `0`.

Paired-trace integrity: **PASS**.

This establishes exact exogenous workload pairing for the matched scheduler comparisons.

---

## Canonical full-matrix reconstruction

The matrix was completed across multiple invocations. The runner's root-level aggregate files are invocation-local, so the final canonical aggregates were reconstructed from the preserved per-run outputs after the 5,400-run audit passed.

The previous root invocation-level aggregates were archived under:

`results/main_5400_00d4e2e/audit/precanonical_root_artifacts_20261016_195452`

Canonical files rebuilt:

- `matrix_summary.csv`: `5,400` data rows (`5,401` lines including header);
- `pair_integrity.csv`: `1,080` data rows (`1,081` lines including header);
- `failures.json`: `[]`;
- `matrix_manifest.json`: full 5,400-run canonical manifest.

Additional audit records created locally:

- `audit/effective_config_hashes.json`;
- `audit/metadata_provenance_5400.csv`;
- `audit/full_integrity_audit.json`.

Canonical full-matrix reconstruction: **PASS**.

---

## Canonical audit record

The final local audit record contains:

```text
canonical_matrix_summary_rows      5400
canonical_pair_integrity_rows      1080
condition_count                    18
effective_config_hash_count        18
environment_signature_count        1
paired_group_count                 1080
paired_trace_integrity             PASS
run_count                          5400
structural_coverage                PASS
metadata_provenance                PASS
```

Execution commit:

`00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6`

Primary YAML SHA-256:

`be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`

---

## Raw data scale and analysis-readiness decision

Final transaction evidence:

- `transactions.csv` files: `5,400 / 5,400`;
- transaction CSV bytes: `54,051,452,153`;
- transaction CSV size: approximately `50.34 GB`;
- full result directory size at readiness check: approximately `126 GB`;
- available disk at readiness check: approximately `74 GiB`.

Because the frozen in-memory analysis loader would attempt to concatenate all transaction CSVs at once, the deterministic transaction-level post-processing was implemented as a memory-safe sequential procedure while preserving the same research definitions and frozen analysis functions.

No observations were sampled for the primary analyses described in the results record.

---

## Deterministic post-processing completion

Memory-safe deterministic post-processing processed all `1,080` paired condition-seed groups.

Outputs:

- `analysis_streaming/starvation_by_run.csv`: `5,400` rows;
- `analysis_streaming/matrix_summary_enriched.csv`: `5,400` rows;
- `analysis_streaming/capc_vs_baseline_preservation.csv`: `1,080` rows;
- `analysis_streaming/analysis_manifest.json`.

Deterministic post-processing: **PASS**.

The starvation rule remained the predeclared paired-baseline rule:

`max(0.50 s, 5 x paired Static Atomic FIFO median waiting time)`.

---

## Research-integrity closure

The following controls remained in force through completion and analysis:

- no CAPC parameter retuning after labelled primary results were inspected;
- no seed replacement;
- no selective deletion of adverse results;
- Diagnostic FIFO kept descriptive and excluded from matched atomic causal comparisons;
- frozen execution revision and frozen primary YAML preserved in all final run metadata;
- interruption evidence retained separately rather than erased;
- complete scheduler pairing preserved for every condition/seed;
- large-data post-processing performed without sampling.

The primary experiment execution/integrity phase is therefore **COMPLETE AND AUDITED**.

Performance findings and RQ-specific evidence are recorded in `docs/PRIMARY_RESULTS_2026-10-16.md` and indexed in `docs/THESIS_EVIDENCE_INDEX_2026-10-16.md`.
