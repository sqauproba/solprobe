"""Automated incident report rendering."""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def render_markdown(
    incident_id: str,
    window: tuple[datetime, datetime],
    notes: str,
    summary: dict | None = None,
) -> str:
    """Render a markdown incident report."""
    start, end = window
    lines = [
        f"# Incident {incident_id}",
        "",
        f"- **Window**: {start.isoformat()} → {end.isoformat()}",
        f"- **Reported**: {_utcnow().isoformat()}",
        f"- **Notes**: {notes}",
        "",
        "## Summary",
        "",
    ]
    if summary:
        for key, value in summary.items():
            lines.append(f"- **{key}**: {value}")
    lines.append("")
    lines.append("## Details")
    lines.append("")
    lines.append("Generated automatically by the SolProbe analyzer.")
    lines.append("")
    return "\n".join(lines)


def render_csv(frame: pd.DataFrame, path: str) -> None:
    """Persist an incident-related dataframe to CSV."""
    frame.to_csv(path, index=False)


def severity_label(score: int) -> str:
    """Map a health score to an incident severity label."""
    if score >= 80:
        return "info"
    if score >= 50:
        return "warning"
    return "critical"
