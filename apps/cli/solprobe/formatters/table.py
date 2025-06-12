"""Terminal output formatters for consistent, readable output."""

from rich.table import Table
from rich.panel import Panel


def kv_table(title: str, rows: list[tuple[str, str]]) -> Table:
    """Render a two-column key/value table."""
    table = Table(title=title, title_justify="left")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")
    for key, value in rows:
        table.add_row(key, value)
    return table


def panel(title: str, body: str) -> Panel:
    """Render a titled panel around a body of text."""
    return Panel(body, title=title, border_style="cyan")


def human_bytes(size: int) -> str:
    """Format a byte count as a human-readable string."""
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if abs(size) < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PiB"
