from __future__ import annotations

import math
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from capc_sim.config.schema import ExperimentConfig
from capc_sim.experiments.runner import run_matrix


REPLICATION_CANDIDATES = (30, 40, 50, 60)


def raw_utilization(config: ExperimentConfig, state: str) -> float:
    rate = config.workload.lambda_normal if state.upper() == "NORMAL" else config.workload.lambda_burst
    cross_rate = rate * config.sharding.cross_shard_ratio
    mean_service_s = (config.coordination.service_time_ms.min + config.coordination.service_time_ms.max) / 2000.0
    return cross_rate * mean_service_s / config.coordination.workers


def baseline_log_p99_half_width(p99_values: list[float]) -> float | None:
    vals = np.asarray([x for x in p99_values if x is not None and x > 0], dtype=float)
    if len(vals) < 2:
        return None
    logs = np.log(vals)
    # Normal-approximation precision diagnostic used only for replication selection.
    return float(1.96 * np.std(logs, ddof=1) / math.sqrt(len(logs)))


def choose_replication_count(p99_by_seed: dict[int, float], target_half_width: float = 0.05) -> dict:
    """Apply the Chapter 3 candidate rule over consecutive seeds 1..N."""
    decisions = []
    selected = 60
    for n in REPLICATION_CANDIDATES:
        values = [p99_by_seed[s] for s in range(1, n + 1) if s in p99_by_seed]
        half = baseline_log_p99_half_width(values) if len(values) == n else None
        decisions.append({"N": n, "half_width_log_p99": half, "passes": half is not None and half <= target_half_width})
        if half is not None and half <= target_half_width:
            selected = n
            break
    return {"selected_N": selected, "target_half_width": target_half_width, "decisions": decisions}


def run_neutral_pilot(
    config: ExperimentConfig,
    *,
    seeds: list[int],
    output: str | Path,
    shard_counts: list[int] | None = None,
    cross_shard_ratios: list[float] | None = None,
    workers: list[int] | None = None,
) -> pd.DataFrame:
    """Run Static Atomic FIFO only; never inspects labelled CAPC performance."""
    return run_matrix(
        config,
        seeds=seeds,
        output=output,
        shard_counts=shard_counts,
        cross_shard_ratios=cross_shard_ratios,
        workers=workers,
        schedulers=["static_atomic_fifo"],
    )


def contention_regime(row: pd.Series) -> str:
    rho = float(row["raw_utilization"])
    block = float(row["lock_block_fraction_candidate_observations"])
    queueing = float(row.get("mean_queue_length", 0.0)) > 0.0
    if rho <= 0.25 and block < 0.10:
        return "LOW"
    if (0.25 < rho < 0.60) or (0.10 <= block < 0.30):
        return "TRANSITIONAL"
    if (rho >= 0.60 or block >= 0.30) and queueing:
        return "HIGH"
    return "UNCLASSIFIED"


def summarize_neutral_pilot(df: pd.DataFrame, config: ExperimentConfig) -> tuple[pd.DataFrame, dict]:
    """Attach scheduler-neutral load diagnostics and assess regime coverage.

    The regime label uses BURST raw utilization because the neutral-pilot acceptance
    criteria are intended to confirm that the matrix spans low, transitional and
    high contention when burst pressure is present. Whole-run lock blocking and
    queueing remain observed diagnostics rather than assumed quantities.
    """
    report = df.copy()
    mean_service_s = (
        config.coordination.service_time_ms.min + config.coordination.service_time_ms.max
    ) / 2000.0
    report["raw_utilization_normal"] = (
        config.workload.lambda_normal
        * report["cross_shard_ratio"].astype(float)
        * mean_service_s
        / report["workers"].astype(float)
    )
    report["raw_utilization_burst"] = (
        config.workload.lambda_burst
        * report["cross_shard_ratio"].astype(float)
        * mean_service_s
        / report["workers"].astype(float)
    )
    report["raw_utilization"] = report["raw_utilization_burst"]
    report["contention_regime"] = report.apply(contention_regime, axis=1)

    observed = set(report["contention_regime"].dropna().astype(str))
    acceptance = {
        "has_low": "LOW" in observed,
        "has_transitional": "TRANSITIONAL" in observed,
        "has_high": "HIGH" in observed,
    }
    acceptance["regime_coverage_pass"] = all(acceptance.values())
    acceptance["classification_utilization_basis"] = "BURST raw utilization"
    acceptance["note"] = (
        "Neutral-pilot regime coverage is scheduler-independent evidence only; "
        "it does not inspect or select settings from CAPC performance."
    )
    return report, acceptance
