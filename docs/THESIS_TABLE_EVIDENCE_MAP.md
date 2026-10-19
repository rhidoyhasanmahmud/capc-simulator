# CAPC MSc Thesis — Table-by-Table Evidence & Reproducibility Map

> **Evidence-navigation index, prepared 19 October 2026; NOT an independent raw-data audit.** Inventory: 28 numbered tables in `CAPC_MSc_Thesis_Professor_Review_Preflight_Fixed_2026.docx`. Described file paths come from the project's existing evidence documentation. We did not access or publish the original experiment CSV/JSON files for this mapping, so no cell-level re-computation, checksum validation, or full third-party reproducibility is claimed.

## Research versions and source records

- CAPC-v1 primary: [repository](https://github.com/rhidoyhasanmahmud/capc-simulator), frozen simulator commit `00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6`.
- CAPC-v1 protocol/result references: [docs/THESIS_EVIDENCE_INDEX_2026-10-16.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/THESIS_EVIDENCE_INDEX_2026-10-16.md), [docs/PRIMARY_RESULTS_2026-10-16.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/PRIMARY_RESULTS_2026-10-16.md), [docs/OUTPUT_SCHEMA.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/OUTPUT_SCHEMA.md), [docs/THESIS_TRACEABILITY.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/THESIS_TRACEABILITY.md).
- CAPC-v2 TailGuard: [separate exploratory repository](https://github.com/rhidoyhasanmahmud/capc-v2-tailguard-simulator), frozen study revision `7933b151292ff8eca01bd10959809dafec8d9ec1`.
- [Machine-readable companion index](table_evidence_index.csv).

## Evidence chain

**Thesis table/cell → exact analysis-output row and calculation → analysis script and parameters → original run files → metadata/config/trace hash → frozen code revision → checksum and independently verified regeneration.**

According to [docs/THESIS_EVIDENCE_INDEX_2026-10-16.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/THESIS_EVIDENCE_INDEX_2026-10-16.md), the v1 study contains **5,400 runs**, 18 workload conditions, 60 paired seeds, five policies, and 1,080 matched condition-seed groups.
Documented *local* primary root: `results/main_5400_00d4e2e/`; derived files are under `results/main_5400_00d4e2e/analysis_streaming/`.
The primary documentation describes about **50.34 GB** of transaction CSVs and **126 GB** of total local outputs. **Those bytes have not been uploaded to this repository or independently checked for this index.**
Frozen v1 primary YAML SHA-256 **as recorded in existing research documentation**: `be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`. This is a recorded reference, not a freshly recalculated hash.

## Verification status definitions

| Status | Interpretation |
|---|---|
| `DOCUMENTED` | Public protocol/source documentation describes it; this is not a fresh audit of every table cell. |
| `LOCAL_RAW_NOT_PRESENT` | Exact source/output filenames documented, but original bytes were unavailable during mapping. |
| `ROW_AUDIT_PENDING` | Selected conditions, row filtering, and reported cell values require re-computation from original sources. |
| `RECALCULATE` | Recompute simple arithmetic from the frozen configuration before claiming a numerical audit. |
| `CITATION_AUDIT_REQUIRED` | Check the cited literature against the synthesized table. |
| `AUTHOR_CONFIRM` | Author-supplied event/history needs documentary confirmation. |
| `DERIVED_SYNTHESIS` | Derived research assessment; trace claims to prior evidence rather than a standalone raw table. |
| `AUTHOR_INTERPRETATION` | Non-empirical recommendation requiring clear distinction from observed data. |

## All numbered thesis tables

| Thesis table | Table title / subject | Evidence class | Documented evidence pointer / regeneration input | Status |
|---|---|---|---|---|
| **Table 2.1** | Comparative Analysis of Representative Studies and CAPC-Relevant Gaps | Literature synthesis | Cited studies and author's SLR; non-experimental synthesis | `CITATION_AUDIT_REQUIRED` |
| **Table 3.1** | Research Tools and Their Roles | Tool declaration | [docs/COMPONENTS.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/COMPONENTS.md); [docs/THESIS_TRACEABILITY.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/THESIS_TRACEABILITY.md) | `DOCUMENTED` |
| **Table 3.2** | Core Simulation Assumptions and Justifications | Assumptions | [docs/EXPERIMENT_PROTOCOL.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/EXPERIMENT_PROTOCOL.md); [docs/OUTPUT_SCHEMA.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/OUTPUT_SCHEMA.md) | `DOCUMENTED` |
| **Table 3.3** | Predeclared Main Experimental Parameters | Frozen protocol | [docs/PARAMETER_FREEZE.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/PARAMETER_FREEZE.md); [configs/primary.yaml](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/configs/primary.yaml); configuration fingerprint in [docs/THESIS_EVIDENCE_INDEX_2026-10-16.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/THESIS_EVIDENCE_INDEX_2026-10-16.md) | `DOCUMENTED` |
| **Table 3.4** | Research Question-Method-Metric Traceability | Methods crosswalk | [docs/THESIS_TRACEABILITY.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/THESIS_TRACEABILITY.md); thesis Chapter 3 | `DOCUMENTED` |
| **Table 3.5** | Scheduler-Neutral Offered-Load and Raw Coordination-Capacity Check | Derived arithmetic | [configs/primary.yaml](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/configs/primary.yaml); calculate λ_cross=λ×cross-shard ratio, ρ=λ_cross×mean service time/workers | `RECALCULATE` |
| **Table 3.6** | MSc Research Development and Execution Timeline | Author chronology | February 2025 MSc start; dated proposal, publication, and version-control records to be author-confirmed | `AUTHOR_CONFIRM` |
| **Table 4.1** | CAPC Design Requirements and Traceability | Design requirements | [docs/THESIS_TRACEABILITY.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/THESIS_TRACEABILITY.md); [docs/COMPONENTS.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/COMPONENTS.md) | `DOCUMENTED` |
| **Table 4.2** | Core CAPC Notation | Algorithm definitions | Thesis Chapter 4 equations; [docs/THESIS_TRACEABILITY.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/THESIS_TRACEABILITY.md) | `DOCUMENTED` |
| **Table 4.3** | Scheduler Definitions at the Design Level | Scheduler mechanisms | [docs/THESIS_TRACEABILITY.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/THESIS_TRACEABILITY.md); scheduler modules in [src/capc_sim/scheduler/](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/src/capc_sim/scheduler/) | `DOCUMENTED` |
| **Table 4.4** | CAPC Parameters Requiring Pre-Experiment Freezing | Parameter freeze | [docs/PARAMETER_FREEZE.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/PARAMETER_FREEZE.md); [configs/primary.yaml](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/configs/primary.yaml) | `DOCUMENTED` |
| **Table 5.1** | Implementation environment and research role of the main software components | Software environment | [docs/COMPONENTS.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/COMPONENTS.md); [README.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/README.md); per-run metadata.json | `LOCAL_RAW_NOT_PRESENT` |
| **Table 5.2** | Frozen CAPC parameters used by the primary experiment | Frozen configuration | [docs/PARAMETER_FREEZE.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/PARAMETER_FREEZE.md); [docs/THESIS_EVIDENCE_INDEX_2026-10-16.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/THESIS_EVIDENCE_INDEX_2026-10-16.md); [configs/primary.yaml](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/configs/primary.yaml) | `DOCUMENTED` |
| **Table 5.3** | Implemented scheduler treatments and their experimental roles | Treatments | [docs/THESIS_TRACEABILITY.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/THESIS_TRACEABILITY.md); [docs/OUTPUT_SCHEMA.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/OUTPUT_SCHEMA.md); source scheduler modules | `DOCUMENTED` |
| **Table 5.4** | Frozen primary comparative experiment matrix | Experiment design/audit | [docs/MAIN_EXPERIMENT_COMPLETION_2026-10-16.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/MAIN_EXPERIMENT_COMPLETION_2026-10-16.md); local matrix_manifest.json and matrix_summary.csv | `LOCAL_RAW_NOT_PRESENT` |
| **Table 5.5** | Deterministic implementation verification matrix | Verification | [docs/VERIFICATION.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/VERIFICATION.md); [docs/DEVELOPMENT_VERIFICATION.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/DEVELOPMENT_VERIFICATION.md); saved V1–V12/pytest outputs | `LOCAL_RAW_NOT_PRESENT` |
| **Table 5.6** | Baseline replication-precision sequence used before comparative inference | Neutral pilot precision | [docs/REPLICATION_PRECISION_LOG.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/REPLICATION_PRECISION_LOG.md); [docs/REPLICATION_FREEZE.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/REPLICATION_FREEZE.md); neutral-pilot outputs | `LOCAL_RAW_NOT_PRESENT` |
| **Table 6.1** | Final main-experiment integrity and provenance summary | Audit | [docs/MAIN_EXPERIMENT_COMPLETION_2026-10-16.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/MAIN_EXPERIMENT_COMPLETION_2026-10-16.md); local matrix_manifest.json, pair_integrity.csv and audit/full_integrity_audit.json | `LOCAL_RAW_NOT_PRESENT` |
| **Table 6.2** | RQ1 p99 latency under NORMAL and BURST workload states | RQ1 quantitative | analysis_streaming/rq1_static_latency_by_state_summary.csv; analysis_streaming/rq1_burst_vs_normal_bootstrap.csv; [docs/PRIMARY_RESULTS_2026-10-16.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/PRIMARY_RESULTS_2026-10-16.md) | `LOCAL_RAW_NOT_PRESENT` |
| **Table 6.3** | RQ2 random-intercept model estimates for the four primary queue-entry predictors | RQ2 quantitative | analysis_streaming/rq2_compact/rq2_exact_random_intercept_coefficients.csv; analysis_streaming/rq2_compact/rq2_exact_random_intercept_model.json; [docs/PRIMARY_RESULTS_2026-10-16.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/PRIMARY_RESULTS_2026-10-16.md) | `LOCAL_RAW_NOT_PRESENT` |
| **Table 6.4** | Primary CAPC p99 confirmatory results versus Static Atomic FIFO | RQ4 primary quantitative | analysis_streaming/primary_p99_confirmatory_summary.csv; analysis_streaming/primary_p99_wilcoxon_holm.csv; analysis_streaming/rq4_thesis_compact_table.csv; [docs/PRIMARY_RESULTS_2026-10-16.md](https://github.com/rhidoyhasanmahmud/capc-simulator/blob/main/docs/PRIMARY_RESULTS_2026-10-16.md) | `LOCAL_RAW_NOT_PRESENT` |
| **Table 6.5** | CAPC preservation and ablation summary relative to Static Atomic FIFO | Preservation/ablation | analysis_streaming/capc_vs_baseline_preservation.csv; analysis_streaming/p99_ablation_vs_static.csv; analysis_streaming/direct_ablation_component_effect.csv | `LOCAL_RAW_NOT_PRESENT` |
| **Table 6.6** | Selected extreme waiting-tail changes under CAPC relative to Static Atomic FIFO | Post-primary diagnostics | analysis_streaming/extreme_wait_tail_diagnostic.csv; analysis_streaming/capc_queue_lock_diagnostics.csv; check each selection and cell | `ROW_AUDIT_PENDING` |
| **Table 6.7** | Selected global and priority-specific p99 changes for CAPC-v1 relative to Static Atomic FIFO | Post-primary class-specific diagnostics | Candidate class-wait source: analysis_streaming/extreme_wait_tail_diagnostic.csv; global result: analysis_streaming/primary_p99_confirmatory_summary.csv; verify exact rows and all 18 conditions | `ROW_AUDIT_PENDING` |
| **Table 6.8** | Research-question and objective evidence summary | Integrated synthesis | Synthesis of Tables 6.2–6.7, Chapters 4–5 verification, and original RQ/objectives | `DERIVED_SYNTHESIS` |
| **Table 7.1** | Final answers to the research questions | Research synthesis | Chapters 3–6 and frozen RQ1/RQ2/RQ4 records; author interpretation | `DERIVED_SYNTHESIS` |
| **Table 7.2** | Achievement of the research aim and objectives | Objective crosswalk | Original objectives/criteria checked against Tables 6.2–6.8 | `DERIVED_SYNTHESIS` |
| **Table 7.3** | Priority directions for future research | Recommendations | Interpretation of observed limitations and trade-offs; not a measured dataset | `AUTHOR_INTERPRETATION` |

## TailGuard-B1 additional exploratory findings (Chapter 6.9)

The exploratory Stage E study is separate from the frozen CAPC-v1 primary matrix: 18 conditions × 30 internal-validation seeds × 3 treatments = **1,620 runs** (540 matched triples). Independent confirmation seeds `2001–2060` remained unused. Specific per-condition activation rates and millisecond effects must not be described as independently verified or downloadable without corresponding raw files, scripts, and checksum evidence.

## Raw data publication / reproducibility status

- **This publication supplies navigation and methodological evidence only.** It does not include original transaction CSVs, run-level JSONs, or the 126 GB local results directory.
- Existing repository documentation records the primary experiment audit, but no independent file-by-file/cell-by-cell audit was performed to produce this mapping.
- Suitable future archival process: supervisor/institution release approval → deposit original and derived data (with large-data archival storage rather than normal Git commits) → calculate SHA-256 file manifest → publish immutable archive URLs → verify one table end-to-end from an independent environment.
- Required release metadata per file: experiment version, run/condition/seed, relative path, archive link, byte size, SHA-256, disclosure category, script/command and verification date.

## Interpretation guardrails

- Primary CAPC-v1 endpoint was **global end-to-end p99**, not HIGH-priority waiting p99. Selected HIGH-priority results were **post-primary diagnostics**, not retroactively primary.
- Static Atomic FIFO is the matched atomic baseline; Diagnostic FIFO is not an atomic causal comparator.
- TailGuard-B1 internal validation is exploratory, not independent confirmation or a replacement for v1.
- A link to a published documentation page **does not** establish that the underlying raw CSV file is public or that its numerical content was independently checked.

## To complete evidence verification

Provide (1) the original primary `results/main_5400_00d4e2e` outputs or independently archived exports/manifest, (2) the exact Chapter 6 analysis scripts and source-output rows, (3) the separate TailGuard Stage E data and scripts, and (4) permitted release locations and checksums. Keep frozen experimental versions unchanged.