"""Health scoring unit tests."""

from solprobe.diagnostics.health import check_health


def test_check_health_returns_result_shape():
    result = check_health()
    assert result.status in ("healthy", "degraded", "unhealthy")
    assert 0 <= result.score <= 100
