"""HTTP client for the SolProbe API."""

from __future__ import annotations

import httpx


class SolProbeClient:
    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        self._client = httpx.Client(base_url=base_url, headers=headers, timeout=30.0)

    def health(self) -> dict:
        return self._client.get("/v1/health").json()

    def network(self) -> dict:
        return self._client.get("/v1/network").json()

    def latest_slot(self) -> dict:
        return self._client.get("/v1/slots/latest").json()

    def benchmark(self, endpoint: str) -> dict:
        return self._client.get(
            "/v1/rpc/benchmark", params={"endpoint": endpoint}
        ).json()

    def wallet(self, address: str) -> dict:
        return self._client.get(f"/v1/wallets/{address}").json()
