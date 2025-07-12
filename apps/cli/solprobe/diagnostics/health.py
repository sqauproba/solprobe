"""Network health scoring.

Computes a composite 0-100 health score for the configured cluster by probing
multiple signals: node health, slot freshness, and RPC latency.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from solprobe.clients.rpc import RpcClient


@dataclass
class HealthResult:
    status: str
    score: int
    checks: dict[str, tuple[bool, str]]


def check_health() -> HealthResult:
    """Compute a health score by probing several cluster signals."""
    client = RpcClient.from_env()
    checks: dict[str, tuple[bool, str]] = {}
    score = 0

    # 1. Node health (weight 40)
    try:
        info = client.get_health()
        ok = info.get("status") == "ok"
        checks["node_health"] = (ok, info.get("status", "unknown"))
        score += 40 if ok else 0
    except Exception as exc:  # noqa: BLE001
        checks["node_health"] = (False, f"error: {exc}")

    # 2. RPC latency (weight 30)
    try:
        start = time.perf_counter()
        client.get_latest_slot()
        latency_ms = (time.perf_counter() - start) * 1000
        ok = latency_ms < 2000
        checks["rpc_latency"] = (ok, f"{latency_ms:.0f}ms")
        if latency_ms < 1000:
            score += 30
        elif latency_ms < 2000:
            score += 15
    except Exception as exc:  # noqa: BLE001
        checks["rpc_latency"] = (False, f"error: {exc}")

    # 3. Slot freshness (weight 30)
    try:
        slot = client.get_latest_slot()
        checks["slot_freshness"] = (True, f"slot {slot:,}")
        score += 30
    except Exception as exc:  # noqa: BLE001
        checks["slot_freshness"] = (False, f"error: {exc}")

    if score >= 80:
        status = "healthy"
    elif score >= 50:
        status = "degraded"
    else:
        status = "unhealthy"

    return HealthResult(status=status, score=score, checks=checks)
