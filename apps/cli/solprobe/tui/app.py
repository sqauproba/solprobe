"""Textual terminal UI for SolProbe.

A multi-panel full-screen dashboard: live slots, latest balances, network
health, and an event log. Requires the ``textual`` extra.
"""

from __future__ import annotations

import time
from collections import deque

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, Static, TabbedContent, TabPane

from solprobe.clients.rpc import RpcClient
from solprobe.diagnostics.health import check_health


class NetworkPanel(Static):
    """Live network health panel."""

    def on_mount(self) -> None:
        self.set_interval(5, self.refresh_health)

    def refresh_health(self) -> None:
        result = check_health()
        self.update(
            f"[bold]Health[/bold] {result.status} ({result.score}/100)\n"
            + "\n".join(
                f"  [{'green' if ok else 'red'}]{name}[/{'green' if ok else 'red'}]: {detail}"
                for name, (ok, detail) in result.checks.items()
            )
        )


class SlotsPanel(Static):
    """Live latest-slot ticker."""

    def on_mount(self) -> None:
        self.set_interval(1, self.refresh_slot)

    def refresh_slot(self) -> None:
        try:
            client = RpcClient.from_env()
            slot = client.get_latest_slot()
            self.update(f"[bold cyan]latest slot[/bold cyan]: {slot:,}")
        except Exception:  # noqa: BLE001
            self.update("[red]slot unavailable[/red]")


class EventLog(Static):
    """A bounded rolling event log."""

    def __init__(self, *args, max_lines: int = 50, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.lines: deque[str] = deque(maxlen=max_lines)

    def append(self, line: str) -> None:
        self.lines.append(f"[{time.strftime('%H:%M:%S')}] {line}")
        self.update("\n".join(self.lines))


class SolProbeApp(App):
    """SolProbe full-screen terminal UI."""

    TITLE = "SolProbe"
    SUB_TITLE = "Solana observability"
    BINDINGS = [("q", "quit", "Quit"), ("r", "refresh", "Refresh")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with VerticalScroll(id="left"):
                yield NetworkPanel()
                yield SlotsPanel()
            with VerticalScroll(id="right"):
                yield EventLog(id="log")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#log", EventLog).append("SolProbe TUI started")


def run() -> None:
    SolProbeApp().run()
