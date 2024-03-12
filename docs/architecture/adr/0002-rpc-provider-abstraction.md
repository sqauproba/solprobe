# ADR-0002: RPC Provider Abstraction

- **Status**: Accepted
- **Date**: 2026-08-01

## Context

RPC providers differ in latency, rate limits, and reliability. SolProbe needs
to benchmark and switch between them.

## Decision

Abstract RPC access behind a client interface (`solprobe/clients/rpc.py` in the
CLI, `RpcConfig` in the collector). All providers implement the same JSON-RPC
surface; the benchmark tooling measures and compares endpoints.

## Consequences

- Providers are swappable via configuration.
- Benchmarking provides an evidence-based way to pick endpoints.
- A common JSON-RPC surface limits vendor lock-in.
