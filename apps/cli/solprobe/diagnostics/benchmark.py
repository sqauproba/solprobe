"""RPC endpoint benchmarking.

Measures end-to-end latency for a curated set of RPC methods and aggregates
per-method statistics, so operators can compare providers on the workloads
SolProbe actually issues.
"""

from __future__ import annotations

import statistics
import time
from dataclasses import dataclass, field

import httpx

# Methods exercised by the benchmark suite, representative of real workloads:
# a health check, two lightweight reads, and one heavier read.
DEFAULT_METHODS: tuple[str, ...] = (
    "getHealth",
    "getSlot",
    "getEpochInfo",
    "getLatestBlockhash",
)


@dataclass
class BenchmarkResult:
    endpoint: str
    methods: dict[str, dict] = field(default_factory=dict)
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    min_latency_ms: float = 0.0
    max_latency_ms: float = 0.0
    throughput_tps: float = 0.0


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = min(len(ordered) - 1, int(len(ordered) * 0.95))
    return ordered[idx]


def benchmark_method(
    client: httpx.Client, method: str, samples: int = 10
) -> list[float]:
    """Return the per-sample latency (ms) for a single RPC method."""
    latencies: list[float] = []
    params: list = []
    if method == "getEpochInfo":
        params = [{"commitment": "confirmed"}]
    elif method == "getLatestBlockhash":
        params = [{"commitment": "confirmed"}]

    for _ in range(samples):
        start = time.perf_counter()
        resp = client.post(
            "/",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params,
            },
        )
        resp.raise_for_status()
        resp.json()
        latencies.append((time.perf_counter() - start) * 1000)

    return latencies


def benchmark_endpoint(endpoint: str, samples: int = 10) -> BenchmarkResult:
    """Benchmark an endpoint across all default methods."""
    endpoint = endpoint.rstrip("/")
    result = BenchmarkResult(endpoint=endpoint)
    all_latencies: list[float] = []

    with httpx.Client(base_url=endpoint, timeout=15.0) as client:
        for method in DEFAULT_METHODS:
            latencies = benchmark_method(client, method, samples=samples)
            result.methods[method] = {
                "avg": statistics.fmean(latencies),
                "p95": _p95(latencies),
                "min": min(latencies),
                "max": max(latencies),
            }
            all_latencies.extend(latencies)

    result.avg_latency_ms = statistics.fmean(all_latencies)
    result.p95_latency_ms = _p95(all_latencies)
    result.min_latency_ms = min(all_latencies)
    result.max_latency_ms = max(all_latencies)
    result.throughput_tps = 1000.0 / max(result.avg_latency_ms, 0.001)
    return result
