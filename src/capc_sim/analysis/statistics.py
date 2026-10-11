from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from statsmodels.formula.api import mixedlm


@dataclass(frozen=True)
class BootstrapResult:
    estimate: float
    lower: float
    upper: float
    resamples: int


def paired_bootstrap_ci(
    differences,
    *,
    resamples: int = 10_000,
    seed: int = 20261005,
    alpha: float = 0.05,
) -> BootstrapResult:
    d = np.asarray(list(differences), dtype=float)
    if d.size == 0:
        raise ValueError("No paired differences supplied")
    rng = np.random.default_rng(seed)
    boot = np.empty(resamples, dtype=float)
    for i in range(resamples):
        boot[i] = float(np.mean(rng.choice(d, size=len(d), replace=True)))
    return BootstrapResult(
        estimate=float(np.mean(d)),
        lower=float(np.quantile(boot, alpha / 2)),
        upper=float(np.quantile(boot, 1 - alpha / 2)),
        resamples=resamples,
    )


def paired_metric_table(
    summary_df: pd.DataFrame,
    metric: str,
    treatment: str,
    baseline: str = "static_atomic_fifo",
) -> pd.DataFrame:
    keys = ["seed", "shard_count", "cross_shard_ratio", "workers"]
    left = summary_df[summary_df.scheduler == treatment][keys + [metric]].rename(columns={metric: "treatment"})
    right = summary_df[summary_df.scheduler == baseline][keys + [metric]].rename(columns={metric: "baseline"})
    merged = left.merge(right, on=keys, validate="one_to_one")
    merged["difference"] = merged["treatment"] - merged["baseline"]
    merged["percent_difference"] = np.where(
        merged["baseline"] != 0,
        100.0 * merged["difference"] / merged["baseline"],
        np.nan,
    )
    return merged


def wilcoxon_paired(differences) -> tuple[float, float]:
    d = np.asarray(list(differences), dtype=float)
    if len(d) == 0:
        raise ValueError("No differences supplied")
    result = wilcoxon(d)
    return float(result.statistic), float(result.pvalue)


def holm_adjust(p_values) -> list[float]:
    p = np.asarray(list(p_values), dtype=float)
    n = len(p)
    order = np.argsort(p)
    adjusted = np.empty(n, dtype=float)
    running = 0.0
    for rank, idx in enumerate(order):
        value = (n - rank) * p[idx]
        running = max(running, value)
        adjusted[idx] = min(1.0, running)
    return adjusted.tolist()


def fit_primary_p99_mixed_model(summary_df: pd.DataFrame):
    """Chapter 3 primary model for matched atomic treatments.

    Diagnostic FIFO is excluded because it does not share atomic semantics.
    The caller should inspect residual diagnostics before interpreting the model.
    """
    atomic = summary_df[summary_df["scheduler"] != "diagnostic_fifo"].copy()
    atomic = atomic[atomic["p99_latency_s"].notna() & (atomic["p99_latency_s"] > 0)].copy()
    atomic["log_p99"] = np.log(atomic["p99_latency_s"].astype(float))
    atomic["shard_count"] = atomic["shard_count"].astype(str)
    atomic["cross_shard_ratio"] = atomic["cross_shard_ratio"].astype(str)
    atomic["workers"] = atomic["workers"].astype(str)
    formula = (
        "log_p99 ~ C(scheduler, Treatment(reference='static_atomic_fifo'))"
        " * C(shard_count, Treatment(reference='4'))"
        " + C(scheduler, Treatment(reference='static_atomic_fifo'))"
        " * C(cross_shard_ratio, Treatment(reference='0.1'))"
        " + C(scheduler, Treatment(reference='static_atomic_fifo'))"
        " * C(workers, Treatment(reference='2'))"
    )
    model = mixedlm(formula, atomic, groups=atomic["seed"])
    return model.fit(reml=False)


def fit_rq2_waiting_mixed_model(
    transactions_df: pd.DataFrame,
    *,
    warmup_s: float = 180.0,
    duration_s: float = 1800.0,
):
    """Chapter 3 RQ2 model for Static Atomic FIFO transaction records only.

    Transactions are included by the same arrival-based measurement window used
    by the latency analysis. The simulation run remains the clustering unit.
    """
    df = transactions_df[
        (transactions_df["scheduler"] == "static_atomic_fifo")
        & (transactions_df["is_cross_shard"] == True)
        & (transactions_df["arrival_time"] >= warmup_s)
        & (transactions_df["arrival_time"] < duration_s)
        & transactions_df["waiting_time"].notna()
    ].copy()
    if "run_id" not in df:
        raise ValueError("transactions_df must contain run_id")
    df["log1p_wait"] = np.log1p(df["waiting_time"].astype(float))
    formula = (
        "log1p_wait ~ arrival_rate_at_entry + queue_length_at_entry"
        " + dependency_degree + active_lock_conflicts_at_entry"
        " + C(workload_state) + C(shard_count) + C(cross_shard_ratio) + C(workers)"
    )
    missing = [c for c in ("shard_count", "cross_shard_ratio", "workers") if c not in df]
    if missing:
        raise ValueError(f"RQ2 model requires condition columns: {', '.join(missing)}")
    model = mixedlm(formula, df, groups=df["run_id"])
    return model.fit(reml=False)
