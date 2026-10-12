# Main Comparative Experiment Run Log

## Purpose

This file records the operational execution and integrity evidence for the frozen 5,400-run CAPC main comparative experiment. It is a provenance and audit document, not a performance-results document.

No CAPC-versus-baseline performance interpretation should be entered here before the complete matrix has finished and the post-run integrity audit has passed.

---

## Frozen pre-launch state

Status: **READY TO LAUNCH**

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
- Available: `261 GiB`
- Capacity used: `42%`

Existing research evidence is retained and must not be deleted to make room for the main matrix.

---

## Launch protocol

Recommended output directory:

`results/main_5400_00d4e2e`

Recommended launch command:

```bash
RUN_DIR="results/main_5400_00d4e2e"

test ! -e "$RUN_DIR" || {
  echo "ERROR: $RUN_DIR already exists"
  exit 1
}

mkdir -p "$RUN_DIR"

{
  echo "CAPC MAIN COMPARATIVE EXPERIMENT"
  echo "Launch date: $(date)"
  echo "Git commit: $(git rev-parse HEAD)"
  echo "Config SHA256: $(shasum -a 256 configs/primary.yaml | awk '{print $1}')"
  echo "Python: $(python --version 2>&1)"
  echo "Seeds: 1-60"
  echo "Expected runs: 5400"
  echo "Schedulers: frozen from configs/primary.yaml"
} > "$RUN_DIR/PRELAUNCH_PROVENANCE.txt"

set -o pipefail

caffeinate -dimsu \
capc-sim matrix \
  --config configs/primary.yaml \
  --seeds $(seq 1 60) \
  --output "$RUN_DIR" \
  2>&1 | tee "$RUN_DIR/console.log"
```

The final matrix should use the CLI default **fail-fast** behaviour. Do not add `--continue-on-error` for the thesis main run.

---

## Operational monitoring rule

During execution, only operational status should be inspected. Do not inspect interim CAPC-versus-baseline effects, tune parameters, alter seeds, or make early performance conclusions.

Permitted operational checks include:

```bash
df -h .
du -sh results/main_5400_00d4e2e
ps aux | grep '[c]apc-sim'
tail -f results/main_5400_00d4e2e/console.log
```

If the process fails, preserve the partial output exactly as produced and record the failure before any rerun decision. Do not replace or add seeds.

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

No CAPC comparative result is recorded in this file at pre-launch stage.
