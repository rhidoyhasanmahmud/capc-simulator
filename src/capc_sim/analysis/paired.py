from __future__ import annotations

import numpy as np

from capc_sim.analysis.statistics import (
    holm_adjust,
    paired_bootstrap_ci,
    paired_metric_table,
    wilcoxon_paired,
)


def starvation_threshold(baseline_waiting_seconds) -> float:
    """Equation 3.9: max(0.50 s, 5 × paired-baseline median waiting time)."""
    arr = np.asarray(list(baseline_waiting_seconds), dtype=float)
    if arr.size == 0:
        return 0.50
    return max(0.50, 5.0 * float(np.median(arr)))


def starvation_incidence(waiting_seconds, threshold_s: float) -> float:
    arr = np.asarray(list(waiting_seconds), dtype=float)
    if arr.size == 0:
        return 0.0
    return float(np.mean(arr > threshold_s))


def jain_completion_ratio(
    completed_by_class: dict[str, int], admitted_by_class: dict[str, int]
) -> float:
    xs = []
    for cls in ("HIGH", "MEDIUM", "LOW"):
        admitted = admitted_by_class.get(cls, 0)
        xs.append(completed_by_class.get(cls, 0) / admitted if admitted else 1.0)
    denom = len(xs) * sum(x * x for x in xs)
    return (sum(xs) ** 2) / denom if denom else 1.0


__all__ = [
    "starvation_threshold",
    "starvation_incidence",
    "jain_completion_ratio",
    "paired_bootstrap_ci",
    "paired_metric_table",
    "wilcoxon_paired",
    "holm_adjust",
]
