# ADR-0003: Polyglot Services

- **Status**: Accepted
- **Date**: 2026-08-01

## Context

Each SolProbe component has different performance, ecosystem, and iteration
requirements.

## Decision

Use the best-fit language per component:

| Concern | Language | Rationale |
|---|---|---|
| CLI & diagnostics | Python | Rich terminal ecosystem (Rich/Textual), fast iteration |
| Event ingestion | Rust | Predictable latency, low overhead, native Solana SDK |
| API gateway | Go | Simple concurrency, fast cold starts |
| Dashboard | TypeScript | Best-in-class reactive UI ecosystem |
| Analytics | Python | Pandas/scikit-learn |
| Alerting | Node.js | Huge integration ecosystem (Discord.js, Telegraf) |

## Consequences

- Each service is independently maintainable.
- Higher onboarding cost than a monolith.
- Mitigated by typed Protobuf contracts and shared docs.
