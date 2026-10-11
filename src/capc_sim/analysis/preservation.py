from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from capc_sim.analysis.loaders import load_matrix_summaries, load_matrix_transactions
from capc_sim.analysis.paired import starvation_incidence, starvation_threshold


CONDITION_KEYS = ["seed", "shard_count", "cross_shard_ratio", "workers"]
RUN_KEYS = CONDITION_KEYS + ["scheduler"]
BASELINE = "static_atomic_fifo"
TREATMENT = "capc"


def _measurement_transactions(
    df: pd.DataFrame,
    *,
    warmup_s: float,
    duration_s: float,
) -> pd.DataFrame:
    """Return non-rejected cross-shard transactions in the arrival-based window."""
    measured = df[
        (df["is_cross_shard"] == True)
        & (df["arrival_time"] >= warmup_s)
        & (df["arrival_time"] < duration_s)
    ].copy()
    if "status" in measured.columns:
        measured = measured[measured["status"] != "REJECTED"]
    return measured


def starvation_by_run(
    transactions_df: pd.DataFrame,
    *,
    warmup_s: float,
    duration_s: float,
    baseline: str = BASELINE,
) -> pd.DataFrame:
    """Compute the Chapter 3 starvation rule for every paired run.

    The threshold is condition/seed-specific and is derived only from the paired
    Static Atomic FIFO baseline: max(0.50 s, 5 x baseline median waiting time).
    The same threshold is then applied to every treatment in the matched pair.
    Transactions are included by arrival time and use their final observed
    coordination waiting time after the drain phase.
    """
    required = set(RUN_KEYS + ["is_cross_shard", "arrival_time", "waiting_time", "priority"])
    missing = sorted(required.difference(transactions_df.columns))
    if missing:
        raise ValueError("transactions_df missing required columns: " + ", ".join(missing))

    measured = _measurement_transactions(
        transactions_df,
        warmup_s=warmup_s,
        duration_s=duration_s,
    )
    rows: list[dict] = []

    for key_values, condition_df in measured.groupby(CONDITION_KEYS, sort=True, dropna=False):
        key = dict(zip(CONDITION_KEYS, key_values))
        baseline_df = condition_df[condition_df["scheduler"] == baseline]
        baseline_wait = baseline_df["waiting_time"].dropna().astype(float).to_numpy()
        if baseline_wait.size == 0:
            raise ValueError(
                "Cannot derive starvation threshold because paired baseline waiting "
                f"data are missing for condition {key}"
            )
        threshold_s = starvation_threshold(baseline_wait)

        for scheduler, run_df in condition_df.groupby("scheduler", sort=True):
            waits = run_df["waiting_time"].dropna().astype(float).to_numpy()
            row = {
                **key,
                "scheduler": scheduler,
                "starvation_threshold_s": float(threshold_s),
                "starvation_denominator": int(len(run_df)),
                "starvation_evaluable": int(len(waits)),
                "starvation_incidence": starvation_incidence(waits, threshold_s),
            }
            for priority in ("HIGH", "MEDIUM", "LOW"):
                priority_df = run_df[run_df["priority"] == priority]
                priority_waits = priority_df["waiting_time"].dropna().astype(float).to_numpy()
                label = priority.lower()
                row[f"starvation_denominator_{label}"] = int(len(priority_df))
                row[f"starvation_incidence_{label}"] = starvation_incidence(
                    priority_waits, threshold_s
                )
            rows.append(row)

    return pd.DataFrame(rows)


def enrich_matrix_summary(
    summary_df: pd.DataFrame,
    starvation_df: pd.DataFrame,
) -> pd.DataFrame:
    """Attach paired-baseline starvation fields to the run-level summary."""
    if starvation_df.empty:
        return summary_df.copy()
    return summary_df.merge(starvation_df, on=RUN_KEYS, how="left", validate="one_to_one")


def _safe_percent_change(treatment: pd.Series, baseline: pd.Series) -> pd.Series:
    b = baseline.astype(float)
    t = treatment.astype(float)
    return pd.Series(np.where(b != 0, 100.0 * (t - b) / b, np.nan), index=treatment.index)


def capc_preservation_table(
    enriched_summary_df: pd.DataFrame,
    *,
    treatment: str = TREATMENT,
    baseline: str = BASELINE,
) -> pd.DataFrame:
    """Create per-condition/seed CAPC preservation checks.

    This table intentionally does not declare overall research success because the
    Chapter 3 success rule also requires paired uncertainty across seeds. It only
    evaluates deterministic per-run practical/preservation thresholds.
    """
    metrics = [
        "p99_latency_s",
        "throughput_tx_per_s",
        "jain_completion_ratio",
        "starvation_incidence",
        "p95_waiting_low_s",
        "queue_stable",
    ]
    missing = [c for c in metrics if c not in enriched_summary_df.columns]
    if missing:
        raise ValueError("enriched summary missing metrics: " + ", ".join(missing))

    left = enriched_summary_df[enriched_summary_df["scheduler"] == treatment][
        CONDITION_KEYS + metrics
    ].copy()
    right = enriched_summary_df[enriched_summary_df["scheduler"] == baseline][
        CONDITION_KEYS + metrics
    ].copy()
    left = left.rename(columns={m: f"treatment_{m}" for m in metrics})
    right = right.rename(columns={m: f"baseline_{m}" for m in metrics})
    paired = left.merge(right, on=CONDITION_KEYS, validate="one_to_one")

    paired["p99_change_pct"] = _safe_percent_change(
        paired["treatment_p99_latency_s"], paired["baseline_p99_latency_s"]
    )
    paired["p99_reduction_pct"] = -paired["p99_change_pct"]
    paired["throughput_change_pct"] = _safe_percent_change(
        paired["treatment_throughput_tx_per_s"], paired["baseline_throughput_tx_per_s"]
    )
    paired["jain_change"] = (
        paired["treatment_jain_completion_ratio"].astype(float)
        - paired["baseline_jain_completion_ratio"].astype(float)
    )
    paired["starvation_change_pp"] = 100.0 * (
        paired["treatment_starvation_incidence"].astype(float)
        - paired["baseline_starvation_incidence"].astype(float)
    )
    paired["low_priority_p95_wait_change_pct"] = _safe_percent_change(
        paired["treatment_p95_waiting_low_s"], paired["baseline_p95_waiting_low_s"]
    )

    paired["p99_practical_threshold_pass"] = paired["p99_reduction_pct"] >= 10.0
    paired["throughput_preserved"] = paired["throughput_change_pct"] >= -5.0
    paired["jain_preserved"] = paired["jain_change"] >= -0.02
    paired["starvation_preserved"] = paired["starvation_change_pp"] <= 1.0
    paired["low_priority_wait_preserved"] = (
        paired["low_priority_p95_wait_change_pct"] <= 25.0
    )
    paired["queue_stability_preserved"] = paired["treatment_queue_stable"].astype(bool)
    paired["all_preservation_constraints_pass"] = (
        paired["throughput_preserved"]
        & paired["jain_preserved"]
        & paired["starvation_preserved"]
        & paired["low_priority_wait_preserved"]
        & paired["queue_stability_preserved"]
    )
    return paired


def analyze_matrix(
    matrix_dir: str | Path,
    *,
    warmup_s: float,
    duration_s: float,
    output_dir: str | Path | None = None,
) -> dict[str, pd.DataFrame | dict]:
    """Run deterministic post-processing needed before inferential analysis."""
    matrix_dir = Path(matrix_dir)
    output_dir = Path(output_dir) if output_dir is not None else matrix_dir / "analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = load_matrix_summaries(matrix_dir)
    transactions = load_matrix_transactions(matrix_dir)
    starvation = starvation_by_run(
        transactions,
        warmup_s=warmup_s,
        duration_s=duration_s,
    )
    enriched = enrich_matrix_summary(summary, starvation)
    preservation = capc_preservation_table(enriched)

    starvation.to_csv(output_dir / "starvation_by_run.csv", index=False)
    enriched.to_csv(output_dir / "matrix_summary_enriched.csv", index=False)
    preservation.to_csv(output_dir / "capc_vs_baseline_preservation.csv", index=False)

    manifest = {
        "matrix_dir": str(matrix_dir),
        "warmup_s": float(warmup_s),
        "duration_s": float(duration_s),
        "baseline": BASELINE,
        "treatment": TREATMENT,
        "starvation_rule": "max(0.50 s, 5 x paired-baseline median waiting time)",
        "preservation_thresholds": {
            "p99_reduction_pct": 10.0,
            "throughput_min_change_pct": -5.0,
            "jain_min_change": -0.02,
            "starvation_max_increase_pp": 1.0,
            "low_priority_p95_wait_max_increase_pct": 25.0,
            "queue_stability_required": True,
        },
        "important": (
            "This deterministic table does not establish overall CAPC success. "
            "The final decision also requires the predeclared paired uncertainty analysis."
        ),
        "run_count": int(len(enriched)),
        "paired_capc_baseline_count": int(len(preservation)),
    }
    (output_dir / "analysis_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "starvation": starvation,
        "enriched_summary": enriched,
        "preservation": preservation,
        "manifest": manifest,
    }
