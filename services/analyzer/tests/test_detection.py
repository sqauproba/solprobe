"""Analyzer tests — detection, baselines, scoring, and reports."""

import pandas as pd
import pytest

from solprobe_analyzer.anomalies.detection import (
    iqr_anomalies,
    summarize_anomalies,
    zscore_anomalies,
)
from solprobe_analyzer.network.baselines import (
    degradation_vs_baseline,
    rolling_baseline,
    rolling_std,
)
from solprobe_analyzer.scoring.health import compute_health_score
from solprobe_analyzer.transactions.failures import failure_rate


def test_zscore_flags_extreme_outlier():
    s = pd.Series([10.0, 11.0, 10.5, 10.8, 500.0, 10.2, 10.9])
    flagged = zscore_anomalies(s, threshold=3.0)
    assert flagged.iloc[4] is True
    assert flagged.sum() >= 1


def test_iqr_detects_outliers():
    s = pd.Series([1, 2, 2, 3, 3, 3, 4, 4, 5, 100])
    flagged = iqr_anomalies(s)
    assert flagged.iloc[-1] is True


def test_rolling_baseline_shifts():
    s = pd.Series([1, 2, 3, 4, 5], dtype="float64")
    base = rolling_baseline(s, window=2)
    assert pd.isna(base.iloc[0])


def test_rolling_std_present():
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    std = rolling_std(s, window=3)
    assert not std.isna().all()


def test_degradation_sign():
    s = pd.Series([10.0] * 50 + [50.0, 50.0])
    z = degradation_vs_baseline(s, window=5)
    assert z.iloc[-1] > 1.5


def test_failure_rate_computation():
    frame = pd.DataFrame(
        {
            "bucket": ["a", "a", "a", "b", "b"],
            "ok": [True, True, False, True, True],
        }
    )
    rates = failure_rate(frame)
    assert rates["a"] == pytest.approx(1 / 3)
    assert rates["b"] == pytest.approx(0.0)


def test_health_score_bounds():
    good = compute_health_score(slot_lag=0, rpc_latency_ms=50, failure_rate=0.0)
    assert good.score >= 90
    bad = compute_health_score(slot_lag=100, rpc_latency_ms=5000, failure_rate=0.5)
    assert bad.score == 0
    assert bad.status == "critical"


def test_summarize_anomalies():
    s = pd.Series([1, 2, 3, 100, 4, 5])
    mask = pd.Series([False] * 6)
    mask.iloc[3] = True
    summary = summarize_anomalies(s, mask)
    assert summary["count"] == 1
    assert summary["max_value"] == 100
