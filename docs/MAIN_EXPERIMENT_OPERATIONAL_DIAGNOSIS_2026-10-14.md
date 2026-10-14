# Main Experiment Operational Diagnosis — 2026-10-14

This note records execution-health evidence only. It is not a CAPC performance-results document.

## Context

The frozen main matrix is running from experiment revision `00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6` with frozen configuration SHA-256 `be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`.

At 21:19:53 on 2026-10-13 the run had produced 610 `summary.json` files after 01:24:31 elapsed time. At 08:11:09 on 2026-10-14 it had produced 681, which initially looked like a severe slowdown.

## Diagnostic snapshot

Shortly after the 08:11 checkpoint:

- PID: `48172`
- wall-clock elapsed: `12:20:23`
- accumulated CPU time: `106:38.71`
- instantaneous CPU usage: `99.8%`
- memory usage: `1.4%`
- process state: `RN`
- total completed `summary.json` count by the end of the diagnostic command: `699`

Recent completed outputs were in condition `sh4_x30_w2`. Seed 20 artifacts showed active progression:

- Diagnostic FIFO summary: about `08:14:54`
- Static Atomic FIFO summary: about `08:15:02`
- CAPC summary: about `08:15:20`
- CAPC-No-Contention summary: about `08:15:39`

Multiple scheduler runs were therefore completing within seconds to tens of seconds while the host was active.

## Continued-liveness confirmation

A follow-up process check showed:

- PID: `48172`
- elapsed wall time: `12:23:24`
- instantaneous CPU usage: `99.9%`
- memory usage: `1.4%`
- process state: `RN`
- completed `summary.json` count: `709`

The count increased from `699` to `709` over about 3 minutes of wall-clock time while the host was active, corresponding to roughly `200 completed run outputs/hour` over that short interval. This confirms active forward progress and argues against a simulator hang.

## Operational interpretation

The key observation is the large mismatch between roughly 12 h 20 m of wall-clock elapsed time and only about 1 h 46 m of accumulated CPU time, despite near-100% CPU usage while the simulator is actively running. This makes a continuous simulator-computation slowdown unlikely.

The stronger working hypothesis is that the Mac/process spent much of the overnight interval suspended or otherwise not scheduled, for example due to system sleep or clamshell sleep. This remains an operational inference until confirmed from macOS sleep/wake logs.

## Action rule

Do not terminate, restart, retune, change seeds, or inspect comparative performance. The process is making forward progress. Confirm host sleep/wake history and current power-management assertions, then continue the same frozen run if the evidence supports host suspension rather than a simulator fault.
