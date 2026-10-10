# Research Integrity Rules

1. **Do not use `configs/dev.yaml` for thesis performance claims.** Its CAPC values are software-development placeholders only.
2. **Do not run labelled primary CAPC comparisons until Chapter 4 parameters are frozen.** Use a versioned copy of `configs/primary_template.yaml` only after all `null` CAPC values have been replaced and reviewed.
3. **Do not replace failed seeds.** Investigate and document failures; keep the frozen seed list unchanged.
4. **Do not tune CAPC using final CAPC-vs-baseline outcomes.** Sensitivity runs are separate and cannot be used retrospectively to choose the primary model.
5. **Keep Diagnostic FIFO outside causal matched claims.** It intentionally omits the matched atomic eligibility/completion semantics.
6. **Preserve raw outputs.** Chapter 6 summaries should be regenerated from `transactions.csv`, state logs, and metadata rather than manually entered.
7. **Record the exact repository commit and configuration hash before the final matrix.**
8. **Treat development/demo output as software evidence, not empirical thesis results.**
9. **If implementation requires a methodological change, resolve it before inspecting labelled comparative results and update Chapters 3–5 consistently.**
10. **Do not claim production-blockchain performance from this simulator.** Conclusions are bounded to the declared logical simulation model.
