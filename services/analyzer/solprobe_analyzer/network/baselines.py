"""Network baselines, trends, and degradation detection."""

from __future__ import annotations

import pandas as pd


def rolling_baseline(series: pd.Series, window: int = 30) -> pd.Series:
    """Compute a rolling mean baseline, excluding the current point."""
    return series.rolling(window=window, center=False, min_periods=1).mean().shift(1)


def rolling_std(series: pd.Series, window: int = 30) -> pd.Series:
    """Compute a rolling standard deviation baseline."""
    return series.rolling(window=window, center=False, min_periods=1).std().shift(1)


def degradation_vs_baseline(series: pd.Series, window: int = 30) -> pd.Series:
    """Return how many stddevs the current value sits above its baseline.

    Positive values indicate degradation; 0/negative indicate normal or
    improving performance.
    """
    baseline = rolling_baseline(series, window)
    std = rolling_std(series, window).replace(0, pd.NA)
    return (series - baseline) / std


def classify_degradation(zscore: pd.Series) -> pd.Series:
    """Map z-scores to human-readable severity labels."""
    return pd.cut(
        zscore,
        bins=[-float("inf"), 1.5, 3.0, float("inf")],
        labels=["normal", "degraded", "critical"],
        include_lowest=True,
    )
