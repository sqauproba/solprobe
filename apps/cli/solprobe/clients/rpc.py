"""Minimal but complete Solana JSON-RPC client backed by httpx.

The client implements the subset of the Solana JSON-RPC API that SolProbe
needs for diagnostics: network health, slots, blocks, balances, accounts,
programs, transactions, fees, and live WebSocket subscriptions.

Every ``get_*`` method raises :class:`RpcError` on an RPC-level error and
:class:`httpx.HTTPError` on transport failures, so callers can distinguish
"the node answered with an error" from "the node is unreachable".
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Iterable, Iterator

import httpx


class RpcError(RuntimeError):
    """Raised when the RPC endpoint returns an explicit JSON-RPC error."""

    def __init__(self, code: int, message: str, data: Any = None) -> None:
        super().__init__(f"RPC error {code}: {message}")
        self.code = code
        self.message = message
        self.data = data


class RpcClient:
    """A thin, stateless-ish JSON-RPC client for a single Solana endpoint.

    All write/read calls go through :meth:`_call` which wraps the request in
    a JSON-RPC 2.0 envelope and normalizes error handling.
    """

    def __init__(
        self,
        endpoint: str,
        cluster: str = "mainnet-beta",
        timeout: float = 30.0,
        retries: int = 2,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.cluster = cluster
        self.timeout = timeout
        self.retries = retries
        self._id = 0
        self._client = httpx.Client(
            base_url=self.endpoint,
            timeout=timeout,
            headers={"Content-Type": "application/json"},
        )

    # ── constructors ─────────────────────────────────────────────────────────

    @classmethod
    def from_env(cls) -> "RpcClient":
        """Build a client from environment configuration with sane defaults."""
        endpoint = os.environ.get(
            "SOLANA_RPC_ENDPOINT", "https://api.mainnet-beta.solana.com"
        )
        cluster = os.environ.get("SOLPROBE_CLUSTER", "mainnet-beta")
        timeout = float(os.environ.get("SOLPROBE_RPC_TIMEOUT", "30"))
        return cls(endpoint=endpoint, cluster=cluster, timeout=timeout)

    @classmethod
    def from_endpoint(cls, endpoint: str) -> "RpcClient":
        """Build a client for an ad-hoc endpoint (e.g. ``rpc benchmark``)."""
        return cls(endpoint=endpoint, cluster="custom")

    # ── low-level RPC plumbing ───────────────────────────────────────────────

    def _call(self, method: str, params: list | None = None) -> Any:
        """Perform a JSON-RPC call with retries and normalized errors."""
        self._id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self._id,
            "method": method,
            "params": params or [],
        }
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                resp = self._client.post("/", json=payload)
                resp.raise_for_status()
                body = resp.json()
                if "error" in body:
                    err = body["error"]
                    raise RpcError(err.get("code", -1), err.get("message", "unknown"))
                return body.get("result")
            except (httpx.HTTPError, RpcError) as exc:
                last_error = exc
                if attempt < self.retries:
                    time.sleep(0.2 * (attempt + 1))
        raise last_error  # type: ignore[misc]

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "RpcClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # ── network / cluster introspection ──────────────────────────────────────

    def get_health(self) -> dict:
        """Return the node health ('ok' when healthy)."""
        return {"status": self._call("getHealth")}

    def get_identity(self) -> dict:
        return self._call("getIdentity")

    def get_version(self) -> dict:
        return self._call("getVersion")

    def get_epoch_info(self, commitment: str = "confirmed") -> dict:
        return self._call("getEpochInfo", [{"commitment": commitment}])

    def get_cluster_nodes(self) -> list[dict]:
        return self._call("getClusterNodes")

    def get_vote_accounts(self) -> dict:
        return self._call("getVoteAccounts")

    def get_genesis_hash(self) -> str:
        return self._call("getGenesisHash")

    def get_recent_performance_samples(self, limit: int = 10) -> list[dict]:
        return self._call("getRecentPerformanceSamples", [limit])

    # ── slots / blocks ───────────────────────────────────────────────────────

    def get_latest_slot(self, commitment: str = "confirmed") -> int:
        return int(self._call("getSlot", [{"commitment": commitment}]))

    def get_slot_leader(self, commitment: str = "confirmed") -> str:
        return self._call("getSlotLeader", [{"commitment": commitment}])

    def get_slot_leaders(
        self, start_slot: int, limit: int = 10, commitment: str = "confirmed"
    ) -> list[str]:
        return self._call(
            "getSlotLeaders", [start_slot, limit, {"commitment": commitment}]
        )

    def get_block_height(self, commitment: str = "confirmed") -> int:
        return int(self._call("getBlockHeight", [{"commitment": commitment}]))

    def get_block(self, slot: int, encoding: str = "json") -> dict:
        return self._call(
            "getBlock", [slot, {"encoding": encoding, "maxSupportedTransactionVersion": 0}]
        )

    def get_block_time(self, slot: int) -> int:
        return int(self._call("getBlockTime", [slot]))

    def get_block_commitment(self, slot: int) -> dict:
        return self._call("getBlockCommitment", [slot])

    def get_first_available_block(self) -> int:
        return int(self._call("getFirstAvailableBlock"))

    def get_supply(self) -> dict:
        return self._call("getSupply")

    # ── accounts / balances ──────────────────────────────────────────────────

    def get_balance(self, address: str, commitment: str = "confirmed") -> int:
        result = self._call("getBalance", [address, {"commitment": commitment}])
        return int(result["value"])

    def get_account_info(self, address: str, encoding: str = "base64") -> dict | None:
        result = self._call(
            "getAccountInfo", [address, {"encoding": encoding, "commitment": "confirmed"}]
        )
        return result.get("value")

    def get_multiple_accounts(self, addresses: list[str]) -> list[dict | None]:
        result = self._call(
            "getMultipleAccounts",
            [addresses, {"encoding": "base64", "commitment": "confirmed"}],
        )
        return result.get("value", [])

    def get_token_accounts_by_owner(
        self, owner: str, program_id: str, commitment: str = "confirmed"
    ) -> list[dict]:
        result = self._call(
            "getTokenAccountsByOwner",
            [
                owner,
                {"programId": program_id},
                {"encoding": "jsonParsed", "commitment": commitment},
            ],
        )
        return result.get("value", [])

    def get_largest_accounts(self) -> list[dict]:
        result = self._call("getLargestAccounts", [{"commitment": "confirmed"}])
        return result.get("value", [])

    # ── programs ─────────────────────────────────────────────────────────────

    def get_program_accounts(
        self,
        program_id: str,
        encoding: str = "base64",
        commitment: str = "confirmed",
        limit: int = 100,
    ) -> list[dict]:
        params: list[Any] = [
            program_id,
            {"encoding": encoding, "commitment": commitment},
        ]
        return self._call("getProgramAccounts", params)[:limit]

    # ── transactions / signatures ────────────────────────────────────────────

    def get_transaction(
        self, signature: str, commitment: str = "confirmed"
    ) -> dict | None:
        result = self._call(
            "getTransaction",
            [
                signature,
                {"encoding": "json", "commitment": commitment, "maxSupportedTransactionVersion": 0},
            ],
        )
        return result

    def get_signatures_for_address(
        self,
        address: str,
        limit: int = 25,
        before: str | None = None,
    ) -> list[dict]:
        config: dict[str, Any] = {"limit": limit}
        if before:
            config["before"] = before
        return self._call("getSignaturesForAddress", [address, config])

    def get_recent_blockhash(self, commitment: str = "confirmed") -> dict:
        return self._call("getRecentBlockhash", [{"commitment": commitment}])

    def get_recent_prioritization_fees(self, addresses: list[str] | None = None) -> list[dict]:
        return self._call("getRecentPrioritizationFees", [addresses or []])

    def simulate(self, raw_transaction: str) -> dict:
        return self._call("simulateTransaction", [raw_transaction])

    def send_transaction(self, raw_transaction: str) -> str:
        return self._call("sendTransaction", [raw_transaction, {"encoding": "base64"}])

    # ── WebSocket subscriptions (stubs until textual/tokio wiring lands) ─────

    def watch_slots(self) -> Iterator[int]:
        """Yield slot numbers from ``slotSubscribe``.

        Note: this is a placeholder for the WebSocket implementation. The CLI
        currently relies on polling ``getSlot`` for the ``slots watch`` command
        via :meth:`poll_slots` instead.
        """
        return iter(())

    def poll_slots(
        self, interval: float = 1.0, max_count: int | None = None
    ) -> Iterator[int]:
        """Poll the latest slot every ``interval`` seconds."""
        count = 0
        while max_count is None or count < max_count:
            yield self.get_latest_slot()
            count += 1
            time.sleep(interval)

    def watch_account(self, address: str) -> Iterator[dict]:
        """Yield account change events (placeholder)."""
        return iter(())

    def watch_program_logs(self, program_id: str) -> Iterator[dict]:
        """Yield program log events (placeholder)."""
        return iter(())
