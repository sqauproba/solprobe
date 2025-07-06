"""solprobe tui — launch the terminal UI."""

import typer


def tui() -> None:
    """Launch the full-screen terminal UI."""
    from solprobe.tui.app import run

    run()
