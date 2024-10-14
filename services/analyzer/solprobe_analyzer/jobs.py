"""Celery task definitions for the analyzer."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def run_network_rollup() -> None:
    """Compute and persist the latest network rollup (placeholder)."""
    logger.info("network rollup started")


def run_health_scoring() -> None:
    """Recompute health scores for watched targets (placeholder)."""
    logger.info("health scoring started")


def run_anomaly_scan() -> None:
    """Scan recent metrics for anomalies (placeholder)."""
    logger.info("anomaly scan started")
