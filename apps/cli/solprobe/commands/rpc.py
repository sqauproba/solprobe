"""solprobe rpc — RPC provider benchmarking and comparison.

Measures end-to-end latency of a set of common RPC methods against one or
more endpoints and renders a comparison table so operators can pick the best
provider for their workload.
"""

from __future__ import annotations

import statistics

import typer
from rich.console import Console
from rich.table import Table

from solprobe.clients.rpc import RpcClient
from solprobe.diagnostics.benchmark import (
    BenchmarkResult,
    benchmark_endpoint,
    benchmark_method,
    DEFAULT_METHODS,
)

console = Console()
rpc_group = typer.Typer(help="RPC provider diagnostics.")


@rpc_group.command("benchmark")
def benchmark(
    endpoint: str = typer.Option(
        "https://api.mainnet-beta.solana.com",
        "--endpoint",
        help="RPC endpoint to benchmark.",
    ),
    samples: int = typer.Option(10, "--samples", min=1, max=100, help="Samples per method."),
) -> None:
    """Benchmark a single RPC endpoint across common methods."""
    result = benchmark_endpoint(endpoint, samples=samples)

    table = Table(title=f"RPC benchmark — {endpoint}")
    table.add_column("Method", style="cyan")
    table.add_column("Avg (ms)", style="white", justify="right")
    table.add_column("P95 (ms)", style="white", justify="right")
    table.add_column("Min (ms)", style="white", justify="right")
    table.add_column("Max (ms)", style="white", justify="right")

    for method, stats in result.methods.items():
        table.add_row(
            method,
            f"{stats['avg']:.1f}",
            f"{stats['p95']:.1f}",
            f"{stats['min']:.1f}",
            f"{stats['max']:.1f}",
        )

    console.print(table)
    console.print(
        f"[bold]Overall:[/bold] avg {result.avg_latency_ms:.1f}ms  "
        f"p95 {result.p95_latency_ms:.1f}ms  "
        f"[green]throughput ~{result.throughput_tps:.1f} req/s[/green]"
    )


@rpc_group.command("compare")
def compare(
    endpoints: list[str] = typer.Option(
        ..., "--endpoint", help="Endpoints to compare (repeatable)."
    ),
    samples: int = typer.Option(8, "--samples", min=1, max=100),
) -> None:
    """Compare multiple RPC endpoints and rank them by latency."""
    if len(endpoints) < 2:
        typer.secho("Provide at least two --endpoint values to compare.", fg="red", err=True)
        raise typer.Exit(code=1)

    results: list[BenchmarkResult] = []
    with console.status("[bold cyan]Benchmarking endpoints...", spinner="dots"):
        for ep in endpoints:
            results.append(benchmark_endpoint(ep, samples=samples))

    results.sort(key=lambda r: r.avg_latency_ms)

    table = Table(title="RPC provider comparison (lower is better)")
    table.add_column("Rank", style="cyan")
    table.add_column("Endpoint", style="white")
    table.add_column("Avg (ms)", justify="right")
    table.add_column("P95 (ms)", justify="right")
    table.add_column("Min (ms)", justify="right")
    table.add_column("Max (ms)", justify="right")

    for i, r in enumerate(results, start=1):
        table.add_row(
            str(i),
            r.endpoint,
            f"{r.avg_latency_ms:.1f}",
            f"{r.p95_latency_ms:.1f}",
            f"{r.min_latency_ms:.1f}",
            f"{r.max_latency_ms:.1f}",
        )

    console.print(table)
    winner = results[0].endpoint
    console.print(f"[bold green]Recommended endpoint:[/bold green] {winner}")


@rpc_group.command("methods")
def methods() -> None:
    """List the RPC methods used by the benchmark suite."""
    console.print("Benchmark suite covers the following methods:")
    for method in DEFAULT_METHODS:
        console.print(f"  • {method}")
