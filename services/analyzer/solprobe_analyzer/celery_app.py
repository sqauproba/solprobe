"""Celery application for scheduled analytics jobs."""

from __future__ import annotations

import os

from celery import Celery

from solprobe_analyzer.jobs import rollup

app = Celery(
    "solprobe_analyzer",
    broker=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.environ.get("REDIS_URL", "redis://localhost:6379/1"),
)

app.conf.beat_schedule = {
    "network-rollup-hourly": {
        "task": "solprobe_analyzer.jobs.rollup.run_network_rollup",
        "schedule": 3600.0,
    },
    "health-score-hourly": {
        "task": "solprobe_analyzer.jobs.rollup.run_health_scoring",
        "schedule": 3600.0,
    },
    "anomaly-scan-daily": {
        "task": "solprobe_analyzer.jobs.rollup.run_anomaly_scan",
        "schedule": 86400.0,
    },
}

app.conf.timezone = "UTC"
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json"]


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    """Register periodic tasks at runtime (belt-and-braces with beat_schedule)."""
    sender.add_periodic_task(
        3600.0,
        rollup.run_network_rollup.s(),
        name="network-rollup-hourly",
    )
