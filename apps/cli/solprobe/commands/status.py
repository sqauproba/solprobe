"""solprobe status / config — quick network overview and configuration dump."""

from __future__ import annotations

import os

import typer
from rich.console import Console
from rich.table import Table

from solprobe.clients.rpc import RpcClient
from solprobe.config.settings import Settings
from solprobe.formatters.table import kv_table

console = Console()


def status() -> None:
    """Show a quick overview of the configured cluster."""
    client = RpcClient.from_env()

    with console.status("[bold cyan]Contacting cluster...", spinner="dots"):
        try:
            health = client.get_health()
            version = client.get_version()
            identity = client.get_identity()
            epoch = client.get_epoch_info()
            slot = client.get_latest_slot()
            block_height = client.get_block_height()
            leader = client.get_slot_leader()
        except Exception as exc:  # noqa: BLE001
            console.print(f"[bold red]Could not reach {client.endpoint}:[/bold red] {exc}")
            raise typer.Exit(code=1)

    table = Table(title=f"SolProbe — {client.cluster}", title_justify="left")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    table.add_row("Cluster", client.cluster)
    table.add_row("RPC endpoint", client.endpoint)
    table.add_row("Node health", health.get("status", "unknown"))
    table.add_row("Solana version", version.get("solana-core", "unknown"))
    table.add_row("Node identity", identity.get("identity", "unknown"))
    table.add_row("Latest confirmed slot", f"{slot:,}")
    table.add_row("Block height", f"{block_height:,}")
    table.add_row("Epoch", f"{epoch.get('epoch')} (progress {epoch.get('slotIndex')}/{epoch.get('slotsInEpoch')})")
    table.add_row("Slot leader", leader)

    console.print(table)


def config() -> None:
    """Show the resolved configuration solprobe is using."""
    settings = Settings.from_env()

    rows = [
        ("cluster", settings.cluster),
        ("rpc_endpoint", settings.rpc_endpoint),
        ("ws_endpoint", settings.ws_endpoint),
        ("api_endpoint", str(settings.api_endpoint or "(unset)")),
        ("log_level", settings.log_level),
        ("timeout_seconds", str(settings.timeout_seconds)),
        ("retries", str(settings.retries)),
    ]
    console.print(kv_table("SolProbe configuration", rows))

    env_override = os.environ.get("SOLANA_RPC_ENDPOINT")
    if env_override and env_override != settings.rpc_endpoint:
        console.print(
            f"[yellow]note: $SOLANA_RPC_ENDPOINT is set but was overridden "
            f"at runtime: {env_override}[/yellow]"
        )
