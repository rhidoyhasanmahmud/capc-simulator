# Main Experiment Interruption — 2026-10-14

This note records an execution interruption only. It is not a CAPC performance-results document.

## Frozen experiment identity

- Execution revision: `00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6`
- Primary configuration SHA-256: `be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875`
- Frozen seed set: `1-60`
- Planned total runs: `5,400`

## Interruption evidence

The host shut down unexpectedly while the main matrix was running.

Post-reboot verification showed:

- Git revision unchanged and correct.
- Primary configuration hash unchanged and correct.
- Working tree clean.
- Old process PID `48172` no longer running.
- `1,432` completed `summary.json` outputs present.
- The most recent complete paired unit was seed `46` for condition `sh4_x50_w2`.
- For seed `47` in condition `sh4_x50_w2`, only `diagnostic_fifo` and `static_atomic_fifo` had completed outputs.
- No completed output directories existed for the remaining three schedulers of that paired seed at the post-reboot check.

## Research-integrity recovery rule

The interruption is treated as a technical execution failure, not as an outcome-based exclusion.

The recovery protocol is:

1. Preserve completed earlier paired units unchanged.
2. Preserve the interrupted seed-47 partial outputs separately for audit provenance.
3. Remove those partial seed-47 outputs from the active primary-results directory.
4. Re-run the full affected paired unit (all five schedulers) for the same frozen seed `47`, configuration, and code revision.
5. Continue with seeds `48-60` for the same condition, then the remaining frozen condition blocks.
6. Do not replace seeds, retune CAPC, or inspect/select results based on performance.
7. Perform a final full-coverage integrity audit across exactly 5,400 active primary run directories before statistical interpretation.

This procedure preserves the paired-design principle while avoiding unnecessary re-execution of already complete paired units.
