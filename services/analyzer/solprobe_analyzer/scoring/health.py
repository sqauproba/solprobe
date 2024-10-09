"""Health scoring — composite scores across signals."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class HealthScore:
    score: int
    status: str
    components: dict[str, int] = field(default_factory=dict)


def compute_health_score(
    slot_lag: float,
    rpc_latency_ms: float,
    failure_rate: float,
    skip_rate: float = 0.0,
) -> HealthScore:
    """Blend key metrics into a 0-100 health score.

    Each signal contributes a weighted component; the composite is clamped
    to [0, 100].
    """
    components: dict[str, int] = {}

    # Slot lag: 0 slots = perfect, > 60 slots = severe.
    slot_comp = max(0, 40 - int(min(slot_lag, 60) * (40 / 60)))
    components["slot_lag"] = slot_comp

    # RPC latency: < 100ms = perfect, > 2000ms = zero.
    latency_comp = max(0, 30 - int(min(rpc_latency_ms, 2000) * (30 / 2000)))
    components["rpc_latency"] = latency_comp

    # Failure rate: 0% = perfect, 10%+ = zero.
    failure_comp = max(0, 20 - int(min(failure_rate, 0.10) * 200))
    components["failure_rate"] = failure_comp

    # Skip rate: 0% = perfect, 20%+ = zero.
    skip_comp = max(0, 10 - int(min(skip_rate, 0.20) * 50))
    components["skip_rate"] = skip_comp

    score = max(0, min(100, sum(components.values())))

    status = "healthy"
    if score < 80:
        status = "degraded"
    if score < 50:
        status = "critical"
    return HealthScore(score=score, status=status, components=components)


def average_health(scores: list[HealthScore]) -> HealthScore:
    """Aggregate multiple health scores into a single average."""
    if not scores:
        return HealthScore(score=0, status="unknown")
    avg = sum(s.score for s in scores) // len(scores)
    status = "healthy" if avg >= 80 else ("degraded" if avg >= 50 else "critical")
    return HealthScore(score=avg, status=status)
