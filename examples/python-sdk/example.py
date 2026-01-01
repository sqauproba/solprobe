"""Example: using the SolProbe Python SDK.

Install first:
    pip install -e packages/sdk-python
"""

from sdk_python import SolProbeClient


def main() -> None:
    client = SolProbeClient(base_url="http://localhost:8080")

    health = client.health()
    print(f"status: {health['status']} score: {health['score']}")

    slot = client.latest_slot()
    print(f"latest slot: {slot['slot']}")

    result = client.benchmark("https://api.mainnet-beta.solana.com")
    print(f"latency: {result['latency_ms']:.1f}ms")


if __name__ == "__main__":
    main()
