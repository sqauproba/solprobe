"""solprobe tx — transaction inspection and simulation.

Fetches transaction details by signature, decodes key fields, and can
simulate a raw transaction from a JSON file.
"""

from __future__ import annotations

import json
import pathlib
import time

import typer
from rich.console import Console
from rich.table import Table

from solprobe.clients.rpc import RpcClient

console = Console()
tx_group = typer.Typer(help="Transaction diagnostics.")


@tx_group.command("inspect")
def inspect(signature: str) -> None:
    """Inspect a transaction by signature: status, fee, slots, and logs."""
    client = RpcClient.from_env()
    tx = client.get_transaction(signature)

    if tx is None:
        console.print(f"[red]Transaction {signature} not found.[/red]")
        raise typer.Exit(code=1)

    meta = tx.get("meta", {})
    err = meta.get("err")
    table = Table(title=f"Transaction — {signature[:32]}...")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Status", "success" if err is None else f"error: {err}")
    table.add_row("Slot", f"{tx.get('slot', 0):,}")
    table.add_row("Fee (lamports)", f"{meta.get('fee', 0):,}")
    table.add_row(
        "Block time",
        time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(tx.get("blockTime", 0))),
    )
    table.add_row("Compute units consumed", f"{meta.get('computeUnitsConsumed', 0):,}")
    table.add_row("Log messages", str(len(meta.get("logMessages", []))))
    console.print(table)

    logs = meta.get("logMessages", [])
    if logs:
        console.print("[bold]Logs:[/bold]")
        for line in logs[:60]:
            console.print(f"  {line}")


@tx_group.command("simulate")
def simulate(file: pathlib.Path) -> None:
    """Simulate a transaction from a JSON file.

    The file must contain a base64-encoded raw transaction string, either as
    a bare string or under a ``"rawTransaction"`` key.
    """
    if not file.exists():
        typer.secho(f"File not found: {file}", fg="red", err=True)
        raise typer.Exit(code=1)

    data = json.loads(file.read_text("utf-8"))
    raw = data if isinstance(data, str) else data.get("rawTransaction")

    if not raw:
        typer.secho(
            "Expected a base64 raw transaction string or a {rawTransaction: ...} object.",
            fg="red",
            err=True,
        )
        raise typer.Exit(code=1)

    client = RpcClient.from_env()
    result = client.simulate(raw)
    value = result.get("value", {})

    console.print("[bold]Simulation result:[/bold]")
    console.print(f"  err       : {value.get('err') or 'none (would succeed)'}")
    console.print(f"  logs      : {len(value.get('logs', []))} messages")
    console.print(f"  accounts  : {len(value.get('accounts', []))} accounts affected")
    units = value.get("unitsConsumed", 0)
    console.print(f"  units     : {units:,} compute units")
