from __future__ import annotations

import pandas as pd

from capc_sim.analysis.preservation import (
    capc_preservation_table,
    enrich_matrix_summary,
    starvation_by_run,
)


def _tx_rows():
    rows = []
    base = {
        "seed": 1,
        "shard_count": 4,
        "cross_shard_ratio": 0.3,
        "workers": 2,
        "is_cross_shard": True,
        "arrival_time": 200.0,
        "status": "COMPLETED",
    }
    # Baseline median = 0.10 -> threshold is safeguarded at 0.50 s.
    for i, wait in enumerate([0.05, 0.10, 0.80]):
        rows.append({**base, "scheduler": "static_atomic_fifo", "waiting_time": wait, "priority": ["HIGH", "MEDIUM", "LOW"][i]})
    for i, wait in enumerate([0.04, 0.12, 0.70]):
        rows.append({**base, "scheduler": "capc", "waiting_time": wait, "priority": ["HIGH", "MEDIUM", "LOW"][i]})
    return rows


def test_starvation_uses_paired_baseline_threshold():
    df = starvation_by_run(pd.DataFrame(_tx_rows()), warmup_s=180.0, duration_s=1800.0)
    assert set(df["starvation_threshold_s"]) == {0.5}
    baseline = df[df.scheduler == "static_atomic_fifo"].iloc[0]
    capc = df[df.scheduler == "capc"].iloc[0]
    assert baseline.starvation_incidence == 1 / 3
    assert capc.starvation_incidence == 1 / 3


def test_preservation_table_applies_predeclared_margins():
    starv = starvation_by_run(pd.DataFrame(_tx_rows()), warmup_s=180.0, duration_s=1800.0)
    summary = pd.DataFrame([
        {
            "seed": 1, "shard_count": 4, "cross_shard_ratio": 0.3, "workers": 2,
            "scheduler": "static_atomic_fifo", "p99_latency_s": 1.0,
            "throughput_tx_per_s": 10.0, "jain_completion_ratio": 0.98,
            "p95_waiting_low_s": 0.40, "queue_stable": True,
        },
        {
            "seed": 1, "shard_count": 4, "cross_shard_ratio": 0.3, "workers": 2,
            "scheduler": "capc", "p99_latency_s": 0.85,
            "throughput_tx_per_s": 9.7, "jain_completion_ratio": 0.97,
            "p95_waiting_low_s": 0.45, "queue_stable": True,
        },
    ])
    enriched = enrich_matrix_summary(summary, starv)
    table = capc_preservation_table(enriched)
    row = table.iloc[0]
    assert round(row.p99_reduction_pct, 8) == 15.0
    assert bool(row.p99_practical_threshold_pass)
    assert bool(row.all_preservation_constraints_pass)
