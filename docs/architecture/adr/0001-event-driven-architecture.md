# ADR-0001: Event-Driven Architecture

- **Status**: Accepted
- **Date**: 2026-08-01

## Context

Solana produces a high-volume, continuous stream of events. The platform needs
multiple consumers (dashboard, analytics, alerting) of the same data without
duplicate collection or unbounded resource use.

## Decision

Adopt an event-driven architecture: the Rust collector is the single ingestion
point; it normalizes events and publishes them over gRPC to all consumers.

## Consequences

- Single point of collection simplifies normalization and metrics.
- Consumers are decoupled and independently scalable.
- Requires a reliable transport (gRPC) and backpressure handling.
