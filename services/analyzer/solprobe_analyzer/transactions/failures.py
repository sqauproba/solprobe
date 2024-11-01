"""Transaction failure and compute analysis."""

from __future__ import annotations

import pandas as pd


def failure_rate(frame: pd.DataFrame) -> pd.Series:
    """Compute the failure rate per bucket of transactions.

    Expects columns: ``bucket`` and ``ok`` (boolean).
    """
    grouped = frame.groupby("bucket")
    total = grouped.size()
    failed = grouped.apply(lambda g: (~g["ok"]).sum())
    return failed / total.replace(0, pd.NA)


def compute_usage_stats(frame: pd.DataFrame) -> pd.DataFrame:
    """Compute per-program compute-unit and fee statistics.

    Expects columns: ``program``, ``compute_units``, ``fee_lamports``.
    """
    if frame.empty:
        return pd.DataFrame()
    return (
        frame.groupby("program")
        .agg(
            tx_count=("compute_units", "size"),
            avg_compute_units=("compute_units", "mean"),
            p95_compute_units=("compute_units", lambda s: s.quantile(0.95)),
            avg_fee_lamports=("fee_lamports", "mean"),
            total_fee_lamports=("fee_lamports", "sum"),
        )
        .reset_index()
    )


def failure_spike_days(frame: pd.DataFrame, threshold: float = 0.05) -> pd.Series:
    """Return the days whose failure rate exceeded ``threshold``."""
    rates = failure_rate(frame)
    return rates[rates > threshold]
