# Main Experiment Operational Checkpoint — 2026-10-14 19:18 +08

This note records operational progress only. It is not a CAPC performance-results document.

- Frozen execution revision: `00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6`
- Frozen primary configuration SHA-256: `be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`
- Planned matrix size: `5,400` runs
- Completed `summary.json` markers: `1,374`
- Approximate completion: `25.4%`
- Remaining runs: `4,026`

The run has continued from the morning without restart. Earlier liveness checks showed the simulator process active near 100% CPU when the Mac was awake. No comparative CAPC-versus-baseline effect is inferred from this checkpoint.

Given the frozen runner order (shard count -> cross-shard ratio -> workers -> seed -> scheduler) and 300 runs per condition block, 1,374 completed outputs places execution in the fifth 300-run condition block. Under the frozen matrix ordering, this corresponds to `4 shards`, cross-shard ratio `0.50`, `2 workers`, approximately around seed 35 within that block. This is an operational location inference only, not a performance conclusion.

The increase from 711 to 1,374 completed outputs is 663 additional runs. Because later high-contention conditions can be computationally more expensive, remaining wall-clock time should not be extrapolated from the earliest low-contention blocks alone. Continue with the same frozen run, keep the machine powered and awake, and do not inspect interim comparative outcomes or retune parameters.
