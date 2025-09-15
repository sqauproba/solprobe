"""solprobe program — on-chain program inspection.

Inspects program metadata, lists accounts owned by a program, and can stream
program activity.
"""

from __future__ import annotations

import base64
import time

import typer
from rich.console import Console
from rich.table import Table

from solprobe.clients.rpc import RpcClient

console = Console()
program_group = typer.Typer(help="Program diagnostics.")


@program_group.command("inspect")
def inspect(program_id: str) -> None:
    """Inspect a program id: owner, size, and recent activity."""
    client = RpcClient.from_env()
    info = client.get_account_info(program_id)

    table = Table(title=f"Program — {program_id}")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")

    if info is None:
        table.add_row("Status", "not found on this cluster")
        console.print(table)
        return

    table.add_row("Owner", info.get("owner", "unknown"))
    table.add_row("Executable", str(info.get("executable", False)))
    data = info.get("data", [])
    data_len = len(data[0]) if isinstance(data, list) and data else 0
    table.add_row("Data length", f"{data_len:,} bytes")
    lamports = info.get("lamports", 0)
    table.add_row("Rent-exempt balance", f"{lamports:,} lamports")
    console.print(table)


@program_group.command("accounts")
def accounts(
    program_id: str,
    limit: int = typer.Option(50, "--limit", min=1, max=1000, help="Max accounts to list."),
) -> None:
    """List accounts owned by a program."""
    client = RpcClient.from_env()
    result = client.get_program_accounts(program_id, limit=limit)

    table = Table(title=f"Accounts owned by {program_id} (showing {len(result)})")
    table.add_column("Address", style="cyan", no_wrap=True)
    table.add_column("Data length", style="white", justify="right")
    table.add_column("Lamports", style="white", justify="right")

    for item in result:
        pubkey = item.get("pubkey", "")
        account = item.get("account", {})
        data = account.get("data", [])
        data_len = len(data[0]) if isinstance(data, list) and data else 0
        table.add_row(pubkey, f"{data_len:,}", f"{account.get('lamports', 0):,}")

    console.print(table)


@program_group.command("logs")
def logs(
    program_id: str,
    count: int = typer.Option(20, "--count", min=1, max=200, help="Signatures to scan."),
) -> None:
    """Scan recent transactions that invoked a program and print their logs."""
    client = RpcClient.from_env()
    signatures = client.get_signatures_for_address(program_id, limit=count)

    if not signatures:
        console.print("[yellow]No recent signatures found for this program.[/yellow]")
        return

    table = Table(title=f"Recent program invocations — {program_id}")
    table.add_column("Signature", style="cyan", no_wrap=True)
    table.add_column("Slot", style="white", justify="right")
    table.add_column("Status", style="white")

    for sig in signatures:
        table.add_row(
            sig.get("signature", ""),
            f"{sig.get('slot', 0):,}",
            str(sig.get("confirmationStatus", "unknown")),
        )
    console.print(table)

    # Also print decoded logs for the most recent successful transaction.
    tx = client.get_transaction(signatures[0]["signature"])
    logs = (tx or {}).get("meta", {}).get("logMessages", [])
    if logs:
        console.print("[bold]Logs from the most recent transaction:[/bold]")
        for line in logs[:40]:
            console.print(f"  {line}")
