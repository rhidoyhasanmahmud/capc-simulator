# Supervisor Progress Update — 14 October 2026

This note supports the MSc supervisor update presentation. It records progress and execution evidence only. It does **not** claim CAPC performance before the full main matrix passes post-run integrity audit.

## Research status

Thesis title: **A Contention-Aware Priority Coordination (CAPC) Model for Reducing Cross-Shard Latency in Blockchain-Based IoT Systems**.

Completed before main-effect analysis:

- Proposal and thesis Chapters 1–5 substantially developed.
- CAPC discrete-event simulator implemented.
- Matched atomic baselines and CAPC ablations implemented.
- Automated verification: 31/31 tests PASS.
- Deterministic verification: V1–V12 PASS.
- Primary configuration frozen with SHA-256 `be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`.
- Frozen execution revision: `00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6`.
- Replication study completed for N = 30, 40, 50, 60.
- Final replication count frozen at N = 60 with a transparent residual precision limitation.

## Replication precision evidence

Worst 95% CI half-width for mean log-p99 baseline by candidate replication count:

| N | Worst half-width |
|---|---:|
| 30 | 0.0702767 |
| 40 | 0.0604617 |
| 50 | 0.0566601 |
| 60 | 0.0515515907 |

Target: 0.05. At N = 60, 16/18 conditions meet the target. The remaining two 4-shard, 50% cross-shard conditions are slightly above target. No post-hoc extra seeds will be added.

## Main experiment

Frozen design:

- Shards: 4, 8, 16
- Cross-shard ratios: 10%, 30%, 50%
- Workers: 2, 4
- Schedulers: Diagnostic FIFO, Static Atomic FIFO, CAPC, CAPC-No-Contention, CAPC-No-Priority
- Seeds: 1–60
- Planned runs: 5,400

Latest observed execution checkpoint:

- Main process running
- PID 48172
- CPU about 99.9%
- Completed outputs: 711 / 5,400 (about 13.2%)
- Remaining: 4,689

An overnight wall-clock slowdown was diagnosed as being consistent with host sleep/suspension rather than simulator failure. Active progress resumed once the host was awake. The run continues unchanged from the frozen revision and configuration.

## Interpretation boundary

No CAPC comparative performance finding has yet been established. Main-effect interpretation will begin only after:

1. all 5,400 runs complete,
2. failure count and coverage are audited,
3. paired trace integrity is verified,
4. frozen revision/configuration provenance is confirmed.

## Remaining work

1. Complete the 5,400-run matrix.
2. Post-run integrity audit.
3. Main statistical analysis for RQ1, RQ2 and RQ4.
4. Pre-planned sensitivity / robustness experiments using frozen variations.
5. Chapter 6 results, analysis and discussion.
6. Chapter 7 conclusions and future work.
7. Final cross-chapter consistency and examiner-readiness review.

## Provisional timeline

Assuming the main matrix completes cleanly and no major methodological redesign is requested:

- Main matrix: roughly 20–30 further active compute hours from the latest checkpoint, subject to condition-dependent runtime.
- Integrity audit: 0.5–1 day.
- Main statistical analysis: 2–3 focused days.
- Sensitivity experiments: roughly 1–3 compute days, pending exact frozen matrix size.
- Chapter 6: 3–5 focused days.
- Chapter 7 and final consistency review: 2–3 focused days.

A realistic estimate after the main matrix completes is approximately **10–14 focused working days to a defensible full thesis draft**, with supervisor revision cycles potentially extending final readiness to **2–3 weeks**.
