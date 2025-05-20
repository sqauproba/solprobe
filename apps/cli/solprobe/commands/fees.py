"""solprobe fees — fee and compute diagnostics.

Reports current priority fees, fee estimates for a given compute budget, and
recent blockhash availability.
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from solprobe.clients.rpc import RpcClient

console = Console()


def fees() -> None:
    """Show recent priority fee market and blockhash information."""
    client = RpcClient.from_env()
    fees = client.get_recent_prioritization_fees()
    blockhash = client.get_recent_blockhash()

    table = Table(title="Fee market")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")

    table.add_row(
        "Latest priority fee (lamports/CU)",
        f"{fees[0]['prioritizationFee']:,}" if fees else "n/a",
    )
    table.add_row(
        "Median priority fee (lamports/CU)",
        f"{_median([f['prioritizationFee'] for f in fees]):,}" if fees else "n/a",
    )
    table.add_row("Blockhash", blockhash.get("blockhash", "n/a"))
    table.add_row("Last valid block height", f"{blockhash.get('lastValidBlockHeight', 0):,}")

    console.print(table)


def estimate(
    compute_units: int = typer.Option(
        200_000, "--cu", min=0, help="Compute unit budget to estimate fees for."
    ),
    priority_micro_lamports: int = typer.Option(
        0,
        "--priority-micro-lamports",
        help="Optional priority fee in micro-lamports per CU.",
    ),
) -> None:
    """Estimate the total fee for a transaction at a given compute budget."""
    base_fee_lamports = 5_000  # standard base fee
    rent = 0
    total = base_fee_lamports

    if priority_micro_lamports:
        priority = (compute_units * priority_micro_lamports) // 1_000_000
        total += priority

    table = Table(title="Fee estimate")
    table.add_column("Component", style="cyan")
    table.add_column("Lamports", style="white", justify="right")
    table.add_row("Base fee", f"{base_fee_lamports:,}")
    table.add_row("Priority fee", f"{max(total - base_fee_lamports, 0):,}")
    table.add_row("Rent (account rent, estimate)", f"{rent:,}")
    table.add_row("[bold]Total (estimate)[/bold]", f"[bold]{total:,}[/bold]")
    console.print(table)


def _median(values: list[int]) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) // 2
