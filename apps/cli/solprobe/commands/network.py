"""solprobe network — network-level diagnostics.

Provides an overview of the cluster (supply, vote accounts, performance
samples), a health check, and a live performance monitor.
"""

from __future__ import annotations

import time

import typer
from rich.console import Console
from rich.table import Table
from rich.live import Live

from solprobe.clients.rpc import RpcClient
from solprobe.diagnostics.health import check_health

console = Console()
network_group = typer.Typer(help="Network-level diagnostics.")


@network_group.command("health")
def health() -> None:
    """Report the health score of the configured cluster."""
    result = check_health()
    color = "green" if result.score >= 80 else ("yellow" if result.score >= 50 else "red")
    console.print(
        f"[bold {color}]status:[/bold {color}] {result.status}  "
        f"[bold {color}]score:[/bold {color}] {result.score}/100"
    )


@network_group.command("overview")
def overview() -> None:
    """Show cluster supply, validator counts, and recent performance."""
    client = RpcClient.from_env()
    supply = client.get_supply()
    votes = client.get_vote_accounts()
    samples = client.get_recent_performance_samples(limit=5)

    table = Table(title="Network overview")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")

    circulating = supply.get("value", {}).get("circulating", 0)
    total = supply.get("value", {}).get("total", 0)
    table.add_row("Circulating supply (SOL)", f"{circulating / 1e9:.2f}")
    table.add_row("Total supply (SOL)", f"{total / 1e9:.2f}")
    table.add_row(
        "Validators (current/delinquent)",
        f"{len(votes.get('current', []))}/{len(votes.get('delinquent', []))}",
    )

    if samples:
        last = samples[0]
        table.add_row("TPS (recent)", f"{last.get('numTransactions', 0) / max(last.get('samplePeriodSecs', 1), 1):.1f}")
        table.add_row("Slots (recent)", str(last.get("numSlots", 0)))

    console.print(table)


@network_group.command("performance")
def performance(
    interval: float = typer.Option(1.0, "--interval", help="Refresh interval (seconds)."),
    count: int = typer.Option(30, "--count", help="Number of samples to collect."),
) -> None:
    """Continuously poll and display recent performance samples."""
    client = RpcClient.from_env()
    console.print("[bold]Sampling cluster performance... (ctrl-c to stop)[/bold]")

    def render() -> Table:
        samples = client.get_recent_performance_samples(limit=10)
        table = Table(title=f"Recent performance — {client.cluster}")
        table.add_column("Slot", style="cyan")
        table.add_column("Transactions", style="white")
        table.add_column("Period (s)", style="white")
        table.add_column("TPS", style="green")
        for s in samples:
            period = max(s.get("samplePeriodSecs", 1), 1)
            tps = s.get("numTransactions", 0) / period
            table.add_row(
                str(s.get("slot", "")),
                f"{s.get('numTransactions', 0):,}",
                f"{period}",
                f"{tps:.1f}",
            )
        return table

    with Live(render(), refresh_per_second=4) as live:
        for _ in range(count):
            time.sleep(interval)
            live.update(render())
