"""Anomaly detection — statistical and model-based methods."""

from __future__ import annotations

import numpy as np
import pandas as pd


def zscore_anomalies(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    """Flag points whose z-score exceeds the threshold."""
    mean = series.mean()
    std = series.std(ddof=0)
    if std == 0:
        return pd.Series(False, index=series.index)
    return ((series - mean) / std).abs() > threshold


def iqr_anomalies(series: pd.Series, k: float = 1.5) -> pd.Series:
    """Flag points outside the interquartile range fence."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    return (series < lower) | (series > upper)


def isolation_forest_anomalies(
    frame: pd.DataFrame, contamination: float = 0.01
) -> np.ndarray:
    """Flag anomalies using an isolation forest (scikit-learn)."""
    from sklearn.ensemble import IsolationForest

    model = IsolationForest(contamination=contamination, random_state=42)
    return model.fit_predict(frame) == -1


def one_class_svm_anomalies(
    frame: pd.DataFrame, nu: float = 0.01
) -> np.ndarray:
    """Flag anomalies using a one-class SVM (scikit-learn)."""
    from sklearn.svm import OneClassSVM

    model = OneClassSVM(kernel="rbf", nu=nu)
    return model.fit_predict(frame) == -1


def summarize_anomalies(series: pd.Series, mask: pd.Series) -> dict:
    """Summarize the anomalies in a series for reporting."""
    anomalous = series[mask]
    return {
        "count": int(mask.sum()),
        "fraction": float(mask.mean()) if len(mask) else 0.0,
        "min_value": float(anomalous.min()) if len(anomalous) else None,
        "max_value": float(anomalous.max()) if len(anomalous) else None,
        "indexes": [str(i) for i in anomalous.index[:20]],
    }
