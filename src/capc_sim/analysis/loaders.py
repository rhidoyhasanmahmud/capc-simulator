from __future__ import annotations

from pathlib import Path

import pandas as pd


def _csvs(root: str | Path, filename: str) -> list[Path]:
    root = Path(root)
    return sorted(p for p in root.rglob(filename) if p.is_file())


def load_matrix_transactions(root: str | Path) -> pd.DataFrame:
    """Load and concatenate per-run transaction records from a matrix directory.

    Each current transaction CSV already contains its condition columns.  The
    loader keeps this logic in one place for the RQ2 analysis scripts and fails
    explicitly when no files are found.
    """
    paths = _csvs(root, "transactions.csv")
    if not paths:
        raise FileNotFoundError(f"No transactions.csv files found under {root}")
    return pd.concat((pd.read_csv(p) for p in paths), ignore_index=True)


def load_matrix_summaries(root: str | Path) -> pd.DataFrame:
    """Load the run-level matrix summary produced by the experiment runner."""
    path = Path(root) / "matrix_summary.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)
