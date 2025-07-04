"""solprobe wallet — wallet inspection and monitoring.

Inspects SOL and token balances for a wallet, lists its recent activity, and
can monitor a wallet over time.
"""

from __future__ import annotations

import time

import typer
from rich.console import Console
from rich.table import Table
from rich.live import Live

from solprobe.clients.rpc import RpcClient

console = Console()
wallet_group = typer.Typer(help="Wallet diagnostics.")

# Common SPL token programs.
SPL_TOKEN_PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
SPL_TOKEN_2022_PROGRAM = "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"


@wallet_group.command("inspect")
def inspect(address: str) -> None:
    """Inspect a wallet address: balances, largest accounts, and activity."""
    client = RpcClient.from_env()

    balance = client.get_balance(address)
    accounts = client.get_signatures_for_address(address, limit=5)

    table = Table(title=f"Wallet — {address}")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("SOL balance", f"{balance / 1e9:.9f} SOL")
    table.add_row("SOL balance (lamports)", f"{balance:,}")
    table.add_row("Recent transactions", f"{len(accounts)} (showing 5)")
    console.print(table)

    if accounts:
        activity = Table(title="Recent activity")
        activity.add_column("Signature", style="cyan", no_wrap=True)
        activity.add_column("Status", style="white")
        activity.add_column("Slot", style="white", justify="right")
        for tx in accounts:
            activity.add_row(
                tx.get("signature", ""),
                str(tx.get("confirmationStatus", "unknown")),
                f"{tx.get('slot', 0):,}",
            )
        console.print(activity)


@wallet_group.command("tokens")
def tokens(address: str) -> None:
    """List SPL token accounts owned by a wallet."""
    client = RpcClient.from_env()

    rows: list[tuple[str, str, str]] = []
    for program_id in (SPL_TOKEN_PROGRAM, SPL_TOKEN_2022_PROGRAM):
        accounts = client.get_token_accounts_by_owner(address, program_id)
        for account in accounts:
            info = account.get("account", {}).get("data", {}).get("parsed", {}).get("info", {})
            mint = info.get("mint", "unknown")
            amount = info.get("tokenAmount", {}).get("uiAmountString", "0")
            rows.append((mint, amount, account.get("pubkey", "")))

    table = Table(title=f"Token accounts for {address}")
    table.add_column("Mint", style="cyan", no_wrap=True)
    table.add_column("Amount", style="white", justify="right")
    table.add_column("Account", style="white", no_wrap=True)
    for mint, amount, pubkey in rows:
        table.add_row(mint, amount, pubkey)
    console.print(table)


@wallet_group.command("watch")
def watch(
    address: str,
    interval: float = typer.Option(2.0, "--interval", help="Poll interval (seconds)."),
    count: int = typer.Option(0, "--count", help="Number of samples (0 = forever)."),
) -> None:
    """Poll and display a wallet's SOL balance over time."""
    client = RpcClient.from_env()
    console.print(f"[bold]Watching wallet {address}... (ctrl-c to stop)[/bold]")

    last = None
    seen = 0

    def render() -> Table:
        nonlocal last, seen
        balance = client.get_balance(address)
        delta = ""
        if last is not None:
            delta = f"{(balance - last) / 1e9:+.9f} SOL"
        last = balance
        seen += 1
        table = Table(title="Live wallet balance")
        table.add_column("Sample", style="cyan", justify="right")
        table.add_column("Balance (SOL)", style="white", justify="right")
        table.add_column("Delta", style="green", justify="right")
        table.add_row(str(seen), f"{balance / 1e9:.9f}", delta)
        return table

    with Live(render(), refresh_per_second=4) as live:
        while count == 0 or seen < count:
            time.sleep(interval)
            live.update(render())
