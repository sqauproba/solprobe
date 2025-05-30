"""SolProbe CLI — Typer application entrypoint.

This module wires together every command group exposed by the ``solprobe``
executable. Command implementations live in ``solprobe.commands`` and shared
infrastructure (RPC clients, diagnostics, formatters, config, TUI) lives in
their respective packages.
"""

from __future__ import annotations

import os
import sys

import typer

from solprobe import __version__
from solprobe.commands import (
    fees,
    network,
    program,
    rpc,
    slots,
    status,
    tx,
    wallet,
)
from solprobe.config.settings import Settings

app = typer.Typer(
    name="solprobe",
    help=(
        "SolProbe - production-grade Solana observability and diagnostics. "
        "Query network health, benchmark RPC providers, inspect wallets and "
        "programs, and watch live slot/account activity from the terminal."
    ),
    no_args_is_help=True,
    add_completion=False,
)


def _print_version(value: bool) -> None:
    if value:
        typer.echo(f"solprobe {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Print the solprobe version and exit.",
        callback=_print_version,
        is_eager=True,
    ),
    endpoint: str | None = typer.Option(
        None,
        "--endpoint",
        "-e",
        help=(
            "Override the Solana RPC endpoint for this invocation "
            "(overrides $SOLANA_RPC_ENDPOINT)."
        ),
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose (debug) logging.",
    ),
) -> None:
    """Shared options for every solprobe invocation."""
    if endpoint:
        os.environ["SOLANA_RPC_ENDPOINT"] = endpoint
    if verbose:
        os.environ["LOG_LEVEL"] = "debug"
    ctx.obj = Settings.from_env()


# ── top-level commands ──────────────────────────────────────────────────────

app.command("status")(status.status)
app.command("config")(status.config)
app.command()(network.network_group)
app.command()(rpc.rpc_group)
app.command()(slots.slots_group)
app.command("fees")(fees.fees)
app.command("fees.estimate")(fees.estimate)
app.command()(wallet.wallet_group)
app.command()(program.program_group)
app.command()(tx.tx_group)
app.command("tui")(tui_command)


def tui_command() -> None:
    """Launch the full-screen terminal UI (requires textual)."""
    try:
        from solprobe.tui.app import run
    except ImportError:
        typer.secho(
            "The TUI requires the 'textual' extra: pip install 'solprobe[tui]'",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)
    run()


if __name__ == "__main__":
    app()
