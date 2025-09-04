"""Pydantic settings model for the CLI."""

from __future__ import annotations

import os

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Runtime configuration for the CLI, resolved from the environment."""

    cluster: str = Field(default="mainnet-beta")
    rpc_endpoint: str = Field(default="https://api.mainnet-beta.solana.com")
    ws_endpoint: str = Field(default="wss://api.mainnet-beta.solana.com/")
    api_endpoint: str | None = Field(default=None)
    log_level: str = Field(default="info")
    timeout_seconds: float = Field(default=30.0)
    retries: int = Field(default=2)
    metrics_enabled: bool = Field(default=True)

    @classmethod
    def from_env(cls) -> "Settings":
        """Build settings from the process environment with sane defaults."""
        return cls(
            cluster=os.environ.get("SOLPROBE_CLUSTER", "mainnet-beta"),
            rpc_endpoint=os.environ.get(
                "SOLANA_RPC_ENDPOINT", "https://api.mainnet-beta.solana.com"
            ),
            ws_endpoint=os.environ.get(
                "SOLANA_WS_ENDPOINT", "wss://api.mainnet-beta.solana.com/"
            ),
            api_endpoint=os.environ.get("SOLPROBE_API_ENDPOINT"),
            log_level=os.environ.get("LOG_LEVEL", "info"),
            timeout_seconds=float(os.environ.get("SOLPROBE_RPC_TIMEOUT", "30")),
            retries=int(os.environ.get("SOLPROBE_RPC_RETRIES", "2")),
            metrics_enabled=os.environ.get("METRICS_ENABLED", "true").lower()
            in ("1", "true", "yes"),
        )
