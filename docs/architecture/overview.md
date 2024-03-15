# Architecture Overview

SolProbe is an open-source observability and diagnostic platform for Solana,
built as a set of composable, polyglot services. This document describes the
high-level architecture; see `data-flow.md` for the runtime data path and the
`adr/` directory for the reasoning behind major decisions.

## Components

| Service | Language | Responsibility |
|---|---|---|
| `apps/cli` | Python | Terminal-first diagnostics and TUI |
| `services/collector` | Rust | High-throughput event ingestion |
| `services/api` | Go | Public API gateway, auth, rate limiting |
| `apps/dashboard` | TypeScript / Next.js | Real-time UI |
| `services/analyzer` | Python | Trends, scoring, anomaly detection |
| `services/alerts` | Node.js | Rule engine and notification fan-out |
| `services/scheduler` | Python | Background jobs |

## Communication

- Collector → downstream: **gRPC / Protobuf** (schemas in `proto/`).
- API → dashboard: **REST + WebSocket** relay.
- Analyzer / scheduler: **Celery + Redis** for periodic work.
- Storage: **PostgreSQL** (historical events) + **Redis** (queues/cache).

## Design principles

- Terminal-first, not terminal-only.
- No polling for live data — persistent WebSocket subscriptions.
- Bounded, backpressure-aware queues instead of unbounded buffers.
- Typed contracts between services (Protobuf).
- Every service ships health checks, structured logs, and metrics.
