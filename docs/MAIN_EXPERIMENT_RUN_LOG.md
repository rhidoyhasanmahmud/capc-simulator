# Main Comparative Experiment Run Log

## Purpose

This file records the operational execution and integrity evidence for the frozen 5,400-run CAPC main comparative experiment. It is primarily a provenance and audit document; final comparative findings are summarized in `docs/PRIMARY_RESULTS_2026-10-16.md`.

---

## Frozen pre-launch state

Status: **COMPLETE — 5,400/5,400 RUNS; FINAL INTEGRITY AUDIT PASS**

Frozen experiment revision:

`00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6`

Frozen primary configuration SHA-256:

`be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`

Replication design:

- Final replication count: `N = 60`
- Frozen seeds: `1-60`
- Logical shards: `4, 8, 16`
- Cross-shard ratios: `0.10, 0.30, 0.50`
- Coordination workers: `2, 4`
- Scheduler treatments: `diagnostic_fifo`, `static_atomic_fifo`, `capc`, `capc_no_contention`, `capc_no_priority`
- Expected total runs: `3 x 3 x 2 x 5 x 60 = 5,400`

Final verification immediately before launch:

- Automated tests: `31/31 PASS`
- Deterministic verification: `V1-V12 PASS`
- CAPC V8 hand-check: computed `0.858750000000`, expected `0.858750000000`
- Local working tree: clean before launch

Storage readiness immediately before launch:

- Filesystem size: `466 GiB`
- Used: `186 GiB`
- Available immediately before launch: `262 GiB`
- Capacity used: `42%`

Existing research evidence was retained and was not deleted to make room for the main matrix.

---

## Actual launch evidence

Launch timestamp recorded locally:

`Tue Oct 13 19:54:10 +08 2026`

Pre-launch provenance file:

`results/main_5400_00d4e2e/PRELAUNCH_PROVENANCE.txt`

Recorded environment:

- Git commit: `00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6`
- Configuration SHA-256: `be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`
- Python: `3.14.0`
- Seeds: `1-60`
- Expected runs: `5,400`
- Free disk immediately before launch: `262 GiB`

Actual background launch command:

```bash
RUN_DIR="results/main_5400_00d4e2e"

nohup caffeinate -ims \
  capc-sim matrix \
  --config configs/primary.yaml \
  --seeds $(seq 1 60) \
  --output "$RUN_DIR" \
  > "$RUN_DIR/console.log" 2>&1 &

echo $! | tee "$RUN_DIR/main.pid"
```

Launch process identifier:

`48172`

Initial operational check approximately 28 seconds after launch:

- Process present: **YES**
- Elapsed time: `00:28`
- CPU usage: `100.0%`
- Memory usage: `1.1%`
- Output directory size: `76M`
- `console.log`: empty at this early stage

Interpretation: the main matrix process started successfully and was actively consuming CPU while generating output. This was operational evidence only.

Operational documentation commits made after the frozen experiment revision did not alter the already-running local checkout or the recorded experiment/configuration hashes.

---

## Operational checkpoint 1

Timestamp:

`Tue Oct 13 21:19:53 +08 2026`

Observed execution state:

- Process identifier: `48172`
- Process present: **YES**
- Elapsed time: `01:24:31`
- CPU usage: `100.0%`
- Memory usage: `1.5%`
- Completed run-output markers (`summary.json` count): `610`
- Planned run count: `5,400`
- Approximate completion fraction by marker count: `11.3%`
- Output directory size: `11 GiB`
- Filesystem used: `203 GiB`
- Filesystem available: `244 GiB`
- Filesystem capacity used: `46%`
- `console.log` tail: empty; no traceback or error text observed

Operational rate at this checkpoint was approximately `433 completed run outputs/hour`. This rate was not used for any scientific inference.

Interpretation: **HEALTHY / CONTINUE**. No comparative performance result was inspected or recorded.

---

## Operational checkpoint 2 — slowdown detected

Timestamp:

`Wed Oct 14 08:11:09 +08 2026`

Observed execution state:

- Process identifier: `48172`
- Process present: **YES**
- Elapsed time: `12:15:47`
- CPU usage: `100.0%`
- Memory usage: `1.4%`
- Completed run-output markers (`summary.json` count): `681`
- Planned run count: `5,400`
- Approximate completion fraction by marker count: `12.6%`
- Output directory size: `13 GiB`
- Filesystem used: `208 GiB`
- Filesystem available: `239 GiB`
- Filesystem capacity used: `47%`
- `console.log` tail: empty; no traceback or error text observed

Between checkpoint 1 and checkpoint 2, only `71` additional run-output markers were completed over approximately `10.85` hours. The process remained CPU-active and storage remained adequate.

The slowdown was classified as an **operational anomaly / diagnostic requirement**, not as a CAPC performance finding.

Later diagnosis showed very high CPU time in CAPC contention/queue calculations for the constrained 4-shard/high-cross-shard region. No simulator optimization was introduced during the frozen experiment.

---

## Host interruption and preserved partial evidence

A host shutdown interrupted the original process on 14 Oct 2026.

Post-reboot active evidence showed:

- four complete condition blocks = `1,200` runs;
- `sh4_x50_w2` seeds `1-46` complete across five schedulers = `230` runs;
- seed `47` Diagnostic FIFO and Static Atomic FIFO outputs = `2` partial scheduler outputs;
- observed total summaries = `1,432`.

The two partial seed-47 scheduler directories were archived separately, reducing the active pair-safe tree to `1,430` outputs before recovery. They were preserved as interruption evidence rather than deleted.

See `docs/MAIN_EXPERIMENT_INTERRUPTION_2026-10-14.md`.

---

## Recovery batch

A recovery batch reran the full five-scheduler set for `sh4_x50_w2`, seeds `47-60`.

Recovery result:

- planned: `70` runs;
- completed: `70` runs;
- failures: `0`;
- paired seed rows: `14`;
- paired trace integrity: `PASS`.

After recovery the active canonical tree contained `1,500` complete run summaries: the first five full 300-run research condition blocks.

---

## Resumable remaining-matrix execution

The remaining `3,900` runs were executed using a resumable 10-seed chunk driver. Chunking changed only operational packaging; the scientific unit remained the 60-seed x five-scheduler condition.

The driver enforced:

- frozen execution Git revision;
- frozen raw primary YAML hash;
- clean working tree at chunk boundaries;
- full five-scheduler completeness per seed;
- archival of incomplete seed outputs before a complete paired rerun;
- empty invocation failure record;
- paired-trace integrity;
- completed-chunk markers and resumable skip logic.

Driver launch:

`2026-10-15 21:34 +08`

Initial active count:

`1,500 / 5,400`

---

## Final completion

Final monitor state on 16 Oct 2026:

```text
Completed: 5400 / 5400
Progress: 100.0%
Final chunk: sh16_x50_w4_seed051_060
Invocation integrity: PASS (50/50 runs; 10 paired seed rows)
SUCCESS: 5400 / 5400 per-run summaries present
```

The final outputs were written at approximately `19:44 +08` and the resumable driver exited after success.

---

## Final integrity audit

Structural coverage:

- `5,400/5,400` summary files;
- `5,400` unique active run directories;
- missing expected runs: `0`;
- unexpected runs: `0`;
- missing metadata: `0`;
- all 18 conditions: `300/300` runs.

Per-run metadata provenance:

- execution Git commit `00d4e2eb...`: `5,400/5,400` runs;
- research mode `primary`: `5,400/5,400`;
- research label `thesis-primary`: `5,400/5,400`;
- output schema version `2`: `5,400/5,400`;
- path/metadata mismatches: `0`;
- missing trace/config hashes: `0`;
- environment signatures: `1`.

Effective configuration audit:

- conditions represented: `18/18`;
- one effective configuration hash within each condition: `PASS`;
- unique effective condition hashes: `18`.

Paired-trace audit:

- paired condition-seed groups: `1,080/1,080`;
- groups not size five: `0`;
- scheduler-set mismatches: `0`;
- unequal trace hashes: `0`.

Final integrity verdict: **PASS**.

---

## Canonical full-matrix reconstruction

Because root aggregate files are invocation-local, the final canonical aggregate was rebuilt from the complete per-run evidence after the integrity gate passed.

Canonical outputs:

- `matrix_summary.csv`: `5,400` rows;
- `pair_integrity.csv`: `1,080` rows;
- `failures.json`: `[]`;
- `matrix_manifest.json`: full canonical manifest.

Previous invocation-level root artifacts were archived under:

`results/main_5400_00d4e2e/audit/precanonical_root_artifacts_20261016_195452`

Canonical rebuild verdict: **PASS**.

---

## Analysis-readiness and data scale

At readiness check:

- transaction CSV files: `5,400/5,400`;
- transaction CSV size: approximately `50.34 GB`;
- full result directory: approximately `126 GB`;
- remaining disk: approximately `74 GiB`.

The 50.34 GB transaction input was processed with a memory-safe sequential post-processing path preserving the frozen metric definitions. No primary reported analysis sampled observations.

Deterministic post-processing outputs:

- `starvation_by_run.csv`: `5,400` rows;
- `matrix_summary_enriched.csv`: `5,400` rows;
- `capc_vs_baseline_preservation.csv`: `1,080` rows;
- deterministic post-processing verdict: `PASS`.

---

## Performance findings — final status

Status: **ESTABLISHED FROM THE COMPLETE, AUDITED PRIMARY DATASET**

The performance result record is intentionally separated from the operational log. See:

- `docs/PRIMARY_RESULTS_2026-10-16.md`;
- `docs/THESIS_EVIDENCE_INDEX_2026-10-16.md`.

Headline RQ4 evidence:

- significant p99 harm: `14/18` conditions;
- significant p99 benefit: `2/18`, both small low-contention effects;
- predeclared practical p99 success: `0/18`;
- medium/high contention significant harm: `12/12`;
- throughput preservation: `100%` of paired CAPC-vs-Static seed units;
- Jain preservation: `100%`;
- all deterministic preservation constraints jointly pass: `56.2%`.

No post-result retuning was performed.

---

## Final research-integrity statement

- No seeds were replaced.
- No adverse completed run was selectively removed.
- Interrupted partial outputs were archived separately.
- All final canonical pairs use identical exogenous trace hashes across schedulers.
- All 5,400 final runs record the frozen execution revision.
- CAPC parameters were not retuned after labelled primary results were inspected.
- Diagnostic FIFO remains descriptive and is excluded from matched atomic causal claims.

The main comparative experiment is therefore **COMPLETE, AUDITED, CANONICALIZED, AND READY FOR THESIS CHAPTER 6 USE**.
