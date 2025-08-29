"""solprobe slots — slot-level diagnostics.

Query the latest slot, inspect block times and leaders, or stream live slot
updates with a lightweight polling loop.
"""

from __future__ import annotations

import time

import typer
from rich.console import Console
from rich.table import Table
from rich.live import Live

from solprobe.clients.rpc import RpcClient

console = Console()
slots_group = typer.Typer(help="Slot-level diagnostics.")


@slots_group.command("latest")
def latest() -> None:
    """Show the latest confirmed slot, height, leader, and block time."""
    client = RpcClient.from_env()
    slot = client.get_latest_slot()
    height = client.get_block_height()
    leader = client.get_slot_leader()
    block_time = client.get_block_time(slot)

    table = Table(title="Latest slots")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Latest confirmed slot", f"{slot:,}")
    table.add_row("Block height", f"{height:,}")
    table.add_row("Slot leader", leader)
    table.add_row("Block time", time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(block_time)))
    console.print(table)


@slots_group.command("leaders")
def leaders(
    start_slot: int = typer.Option(None, "--start-slot", help="Start slot (defaults to latest)."),
    count: int = typer.Option(10, "--count", min=1, max=50, help="Number of leaders to list."),
) -> None:
    """Show the upcoming slot leaders from a given slot."""
    client = RpcClient.from_env()
    if start_slot is None:
        start_slot = client.get_latest_slot()
    leaders = client.get_slot_leaders(start_slot, limit=count)

    table = Table(title=f"Slot leaders from slot {start_slot:,}")
    table.add_column("Offset", style="cyan")
    table.add_column("Leader", style="white")
    for i, leader in enumerate(leaders):
        table.add_row(f"+{i}", leader)
    console.print(table)


@slots_group.command("watch")
def watch(
    interval: float = typer.Option(1.0, "--interval", help="Poll interval (seconds)."),
    count: int = typer.Option(0, "--count", help="Number of slots to sample (0 = forever)."),
) -> None:
    """Stream live slot updates from the configured RPC endpoint."""
    client = RpcClient.from_env()
    console.print(f"[bold]Watching slots on {client.cluster}... (ctrl-c to stop)[/bold]")

    last = None
    seen = 0

    def render() -> Table:
        nonlocal last, seen
        current = client.get_latest_slot()
        delta = ""
        if last is not None:
            delta = f"{current - last:+d}"
        last = current
        seen += 1
        table = Table(title="Live slots")
        table.add_column("Sample", style="cyan", justify="right")
        table.add_column("Slot", style="white", justify="right")
        table.add_column("Delta", style="green", justify="right")
        table.add_row(str(seen), f"{current:,}", delta)
        return table

    with Live(render(), refresh_per_second=4) as live:
        while count == 0 or seen < count:
            time.sleep(interval)
            live.update(render())
