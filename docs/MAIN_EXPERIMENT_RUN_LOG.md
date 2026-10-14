# Main Comparative Experiment Run Log

## Purpose

This file records the operational execution and integrity evidence for the frozen 5,400-run CAPC main comparative experiment. It is a provenance and audit document, not a performance-results document.

No CAPC-versus-baseline performance interpretation should be entered here before the complete matrix has finished and the post-run integrity audit has passed.

---

## Frozen pre-launch state

Status: **LAUNCHED / RUNNING — OPERATIONAL SLOWDOWN UNDER DIAGNOSIS**

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

Existing research evidence is retained and must not be deleted to make room for the main matrix.

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

Interpretation: the main matrix process started successfully and was actively consuming CPU while generating output. This is operational evidence only; it does not establish successful matrix completion or any CAPC performance result.

Operational documentation commits made after the frozen experiment revision do not alter the already-running local checkout or the recorded experiment/configuration hashes.

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

Operational rate at this checkpoint is approximately `433 completed run outputs/hour` based on the elapsed time and marker count. A simple linear extrapolation would imply roughly `11.1 hours` remaining from this checkpoint and about `12.5 hours` total runtime, but this is only an operational estimate because later conditions/schedulers may have different execution costs.

At the observed storage rate (`11 GiB` for `610` completed run-output markers), a simple linear projection is about `97 GiB` for 5,400 runs. This is also only a rough operational estimate; output volume may vary by condition and scheduler. With `244 GiB` still available at the checkpoint, storage headroom remained adequate.

Interpretation: **HEALTHY / CONTINUE**. The process was alive, CPU-active, generating completed run artifacts, and had adequate remaining disk space. No comparative performance result was inspected or recorded.

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

Between checkpoint 1 and checkpoint 2, only `71` additional run-output markers were completed over approximately `10.85` hours, an incremental rate of about `6.5 runs/hour`. This is a major execution-rate reduction relative to the first checkpoint and must not be treated as a normal linear continuation without diagnosis.

The process remains CPU-active and storage remains adequate, so the evidence does not indicate a crash or disk-capacity failure. The slowdown is currently classified as an **operational anomaly / diagnostic requirement**, not as a CAPC performance finding.

Given the matrix loop order in the frozen runner (shard count -> cross-shard ratio -> workers -> seed -> scheduler), 681 completed outputs imply that the first two 300-run condition blocks have completed and execution has entered the third condition block, corresponding to `4 shards`, `0.30` cross-shard ratio, and `2 workers`, assuming no hidden output-count discrepancy. Exact current run/scheduler should be established from file timestamps before any intervention.

Action rule: do not terminate, rerun, edit code/configuration, or inspect comparative performance yet. First perform operational-only diagnosis of the most recently completed run paths and currently modified files.

---

## Launch protocol rule

The final matrix uses the CLI default **fail-fast** behaviour. `--continue-on-error` was not used.

If a technical failure occurs, preserve the partial output exactly as produced and record the failure before any rerun decision. Do not replace or add seeds.

---

## Operational monitoring rule

During execution, only operational status should be inspected. Do not inspect interim CAPC-versus-baseline effects, tune parameters, alter seeds, or make early performance conclusions.

Permitted operational checks include:

```bash
df -h .
du -sh results/main_5400_00d4e2e
PID=$(cat results/main_5400_00d4e2e/main.pid)
ps -p "$PID" -o pid,etime,%cpu,%mem,command
tail -30 results/main_5400_00d4e2e/console.log
```

---

## Post-run integrity audit — pending

After the command completes, record and verify at minimum:

- process exit status;
- total completed runs;
- expected run count = `5,400`;
- failure count;
- complete scheduler x condition x seed coverage;
- paired trace-hash equality;
- one frozen Git revision across final runs;
- one frozen primary configuration SHA-256;
- seed set exactly `1-60`;
- no selective reruns or seed replacement;
- final output-directory size;
- remaining disk space.

The matrix must pass this integrity audit before Chapter 6 performance interpretation begins.

---

## Performance findings

Status: **NOT YET ESTABLISHED**

No CAPC comparative result is recorded while the matrix is running.
