# Shared types

Cross-service type contracts. Event shapes are defined in `proto/` and
generated into each language binding. This package holds hand-authored
TypeScript mirror types for the dashboard and SDK.

- `SlotEvent` — slot subscription notification
- `LogEvent` — log subscription notification
- `NetworkMetrics` — aggregated network metrics
