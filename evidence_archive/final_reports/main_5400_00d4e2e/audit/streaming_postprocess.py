from pathlib import Path
from collections import Counter
import hashlib
import json
import subprocess
import sys
import time

import numpy as np
import pandas as pd

from capc_sim.analysis.paired import (
    starvation_threshold,
    starvation_incidence,
)
from capc_sim.analysis.preservation import capc_preservation_table
from capc_sim.config.loader import load_config

ROOT = Path("results/main_5400_00d4e2e")
OUT = ROOT / "analysis_streaming"
PARTS = OUT / "_starvation_parts"
OUT.mkdir(parents=True, exist_ok=True)
PARTS.mkdir(parents=True, exist_ok=True)

FROZEN_COMMIT = "00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6"
EXPECTED_YAML_SHA = "be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875"

CONDITION_KEYS = [
    "seed",
    "shard_count",
    "cross_shard_ratio",
    "workers",
]

RUN_KEYS = CONDITION_KEYS + ["scheduler"]

SCHEDULERS = [
    "diagnostic_fifo",
    "static_atomic_fifo",
    "capc",
    "capc_no_contention",
    "capc_no_priority",
]

BASELINE = "static_atomic_fifo"

# ------------------------------------------------------------
# 0. Guard: post-processing source/config must match frozen code
# ------------------------------------------------------------
diff_cmd = [
    "git", "diff", "--quiet",
    FROZEN_COMMIT, "HEAD", "--",
    "src/capc_sim/analysis",
    "src/capc_sim/config",
    "configs/primary.yaml",
]

diff_rc = subprocess.run(diff_cmd).returncode

if diff_rc != 0:
    raise SystemExit(
        "ERROR: analysis/config source differs from frozen execution revision."
    )

yaml_path = Path("configs/primary.yaml")
yaml_sha = hashlib.sha256(yaml_path.read_bytes()).hexdigest()

if yaml_sha != EXPECTED_YAML_SHA:
    raise SystemExit(
        f"ERROR: primary.yaml SHA mismatch: {yaml_sha}"
    )

config = load_config(yaml_path)
warmup = float(config.simulation.warmup_s)
duration = float(config.simulation.duration_s)

print("===== STREAMING POST-PROCESSING =====")
print("Frozen analysis source: PASS")
print("Primary YAML SHA: PASS")
print("Warmup:", warmup)
print("Duration:", duration)

# ------------------------------------------------------------
# 1. Load canonical 5400-row summary only
# ------------------------------------------------------------
summary_path = ROOT / "matrix_summary.csv"
summary = pd.read_csv(summary_path)

if len(summary) != 5400:
    raise SystemExit(
        f"ERROR: expected 5400 summary rows, got {len(summary)}"
    )

if summary["run_id"].nunique() != 5400:
    raise SystemExit("ERROR: canonical summary has duplicate run_id")

groups = list(
    summary.groupby(
        CONDITION_KEYS,
        sort=True,
        dropna=False,
    )
)

if len(groups) != 1080:
    raise SystemExit(
        f"ERROR: expected 1080 paired groups, got {len(groups)}"
    )

print("Canonical summary:", len(summary), "runs")
print("Paired groups:", len(groups))

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
NEEDED_COLUMNS = {
    "is_cross_shard",
    "arrival_time",
    "waiting_time",
    "priority",
    "status",
}

REQUIRED_COLUMNS = {
    "is_cross_shard",
    "arrival_time",
    "waiting_time",
    "priority",
}

def load_measured(run_id):
    path = ROOT / run_id / "transactions.csv"

    if not path.exists():
        raise FileNotFoundError(path)

    df = pd.read_csv(
        path,
        usecols=lambda c: c in NEEDED_COLUMNS,
    )

    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(
            f"{run_id}: missing transaction columns {sorted(missing)}"
        )

    measured = df[
        (df["is_cross_shard"] == True)
        & (df["arrival_time"] >= warmup)
        & (df["arrival_time"] < duration)
    ].copy()

    if "status" in measured.columns:
        measured = measured[
            measured["status"] != "REJECTED"
        ]

    return measured


def starvation_row(key, scheduler, run_id, threshold):
    df = load_measured(run_id)

    waits = (
        df["waiting_time"]
        .dropna()
        .astype(float)
        .to_numpy()
    )

    row = {
        **key,
        "scheduler": scheduler,
        "starvation_threshold_s": float(threshold),
        "starvation_denominator": int(len(df)),
        "starvation_evaluable": int(len(waits)),
        "starvation_incidence":
            starvation_incidence(waits, threshold),
    }

    for priority in ("HIGH", "MEDIUM", "LOW"):
        priority_df = df[df["priority"] == priority]

        priority_waits = (
            priority_df["waiting_time"]
            .dropna()
            .astype(float)
            .to_numpy()
        )

        label = priority.lower()

        row[f"starvation_denominator_{label}"] = int(
            len(priority_df)
        )

        row[f"starvation_incidence_{label}"] = (
            starvation_incidence(
                priority_waits,
                threshold,
            )
        )

    return row


# ------------------------------------------------------------
# 2. Process each paired group independently and resumably
# ------------------------------------------------------------
start = time.time()

for index, (key_values, group) in enumerate(groups, start=1):
    key = dict(zip(CONDITION_KEYS, key_values))

    sh = int(key["shard_count"])
    ratio = float(key["cross_shard_ratio"])
    workers = int(key["workers"])
    seed = int(key["seed"])

    tag = (
        f"sh{sh}_x{int(round(ratio * 100)):02d}"
        f"_w{workers}_seed{seed:03d}"
    )

    part = PARTS / f"{tag}.csv"

    # Resumability: a valid completed 5-row part is reused.
    if part.exists():
        existing = pd.read_csv(part)

        if (
            len(existing) == 5
            and set(existing["scheduler"]) == set(SCHEDULERS)
        ):
            if index % 50 == 0 or index == 1080:
                print(
                    f"[{index:4d}/1080] reuse {tag}",
                    flush=True,
                )
            continue

        part.unlink()

    if len(group) != 5:
        raise SystemExit(
            f"ERROR: {tag} has {len(group)} runs, expected 5"
        )

    if set(group["scheduler"]) != set(SCHEDULERS):
        raise SystemExit(
            f"ERROR: scheduler mismatch in {tag}"
        )

    baseline_rows = group[
        group["scheduler"] == BASELINE
    ]

    if len(baseline_rows) != 1:
        raise SystemExit(
            f"ERROR: baseline missing/duplicated in {tag}"
        )

    baseline_run_id = baseline_rows.iloc[0]["run_id"]
    baseline_df = load_measured(baseline_run_id)

    baseline_wait = (
        baseline_df["waiting_time"]
        .dropna()
        .astype(float)
        .to_numpy()
    )

    if baseline_wait.size == 0:
        raise SystemExit(
            f"ERROR: no baseline waiting observations in {tag}"
        )

    threshold = starvation_threshold(baseline_wait)

    rows = []

    for scheduler in SCHEDULERS:
        scheduler_row = group[
            group["scheduler"] == scheduler
        ]

        if len(scheduler_row) != 1:
            raise SystemExit(
                f"ERROR: {scheduler} missing/duplicated in {tag}"
            )

        run_id = scheduler_row.iloc[0]["run_id"]

        rows.append(
            starvation_row(
                key,
                scheduler,
                run_id,
                threshold,
            )
        )

    part_df = pd.DataFrame(rows)
    part_df.to_csv(part, index=False)

    if index % 10 == 0 or index == 1:
        elapsed = time.time() - start
        print(
            f"[{index:4d}/1080] completed {tag} "
            f"| elapsed {elapsed/60:.1f} min",
            flush=True,
        )

# ------------------------------------------------------------
# 3. Reassemble deterministic starvation table
# ------------------------------------------------------------
part_files = sorted(PARTS.glob("*.csv"))

if len(part_files) != 1080:
    raise SystemExit(
        f"ERROR: expected 1080 completed parts, "
        f"found {len(part_files)}"
    )

starvation = pd.concat(
    (pd.read_csv(p) for p in part_files),
    ignore_index=True,
)

if len(starvation) != 5400:
    raise SystemExit(
        f"ERROR: starvation table has {len(starvation)} rows"
    )

if starvation[RUN_KEYS].duplicated().any():
    raise SystemExit(
        "ERROR: duplicate starvation run keys"
    )

starvation = starvation.sort_values(
    [
        "shard_count",
        "cross_shard_ratio",
        "workers",
        "seed",
        "scheduler",
    ]
).reset_index(drop=True)

starvation.to_csv(
    OUT / "starvation_by_run.csv",
    index=False,
)

# ------------------------------------------------------------
# 4. Exact small-table merge used by frozen analysis
# ------------------------------------------------------------
enriched = summary.merge(
    starvation,
    on=RUN_KEYS,
    how="left",
    validate="one_to_one",
)

if len(enriched) != 5400:
    raise SystemExit(
        "ERROR: enriched matrix is not 5400 rows"
    )

if enriched["starvation_threshold_s"].isna().any():
    raise SystemExit(
        "ERROR: unmatched starvation rows after merge"
    )

enriched.to_csv(
    OUT / "matrix_summary_enriched.csv",
    index=False,
)

# ------------------------------------------------------------
# 5. Frozen preservation calculation
# ------------------------------------------------------------
preservation = capc_preservation_table(enriched)

if len(preservation) != 1080:
    raise SystemExit(
        f"ERROR: preservation table has "
        f"{len(preservation)} rows, expected 1080"
    )

preservation.to_csv(
    OUT / "capc_vs_baseline_preservation.csv",
    index=False,
)

# ------------------------------------------------------------
# 6. Provenance manifest
# ------------------------------------------------------------
manifest = {
    "analysis_type":
        "memory-safe streaming equivalent of frozen deterministic post-processing",

    "frozen_execution_commit": FROZEN_COMMIT,
    "primary_yaml_sha256": EXPECTED_YAML_SHA,

    "warmup_s": warmup,
    "duration_s": duration,

    "baseline": BASELINE,
    "treatment": "capc",

    "input_run_count": 5400,
    "paired_condition_seed_count": 1080,

    "starvation_rows": int(len(starvation)),
    "enriched_summary_rows": int(len(enriched)),
    "preservation_rows": int(len(preservation)),

    "starvation_rule":
        "max(0.50 s, 5 x paired-baseline median waiting time)",

    "preservation_thresholds": {
        "p99_reduction_pct": 10.0,
        "throughput_min_change_pct": -5.0,
        "jain_min_change": -0.02,
        "starvation_max_increase_pp": 1.0,
        "low_priority_p95_wait_max_increase_pct": 25.0,
        "queue_stability_required": True,
    },

    "implementation_note":
        "Transactions were processed one paired condition-seed group "
        "at a time because the frozen in-memory loader would require "
        "loading approximately 50.34 GB of transaction CSV input. "
        "The research definitions and frozen analysis functions were "
        "not changed.",

    "important":
        "These deterministic preservation tables do not alone establish "
        "overall CAPC success. Final conclusions require the predeclared "
        "paired uncertainty and inferential analyses.",
}

(OUT / "analysis_manifest.json").write_text(
    json.dumps(
        manifest,
        indent=2,
        sort_keys=True,
    ) + "\n",
    encoding="utf-8",
)

print()
print("===== STREAMING POST-PROCESSING COMPLETE =====")
print("starvation_by_run.csv:", len(starvation), "rows")
print("matrix_summary_enriched.csv:", len(enriched), "rows")
print(
    "capc_vs_baseline_preservation.csv:",
    len(preservation),
    "rows",
)
print("analysis_manifest.json: written")
print()
print("===== VERDICT =====")
print("DETERMINISTIC POST-PROCESSING: PASS")
