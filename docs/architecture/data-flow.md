# Data Flow

## Collection

1. `services/collector` opens WebSocket subscriptions to the configured Solana
   RPC (`slotSubscribe`, `accountSubscribe`, `logsSubscribe`,
   `programSubscribe`).
2. Raw events are decoded into typed Protobuf messages (schemas in `proto/`).
3. Events are published over gRPC to the API, alerts, and analyzer services
   simultaneously.

## Serving

4. `services/api` relays live events to the dashboard over WebSocket and
   serves historical queries from PostgreSQL.
5. `services/analyzer` runs scheduled jobs (via Celery) to compute rolling
   baselines and flag anomalies, writing results back to Postgres for the API
   to serve.
6. `services/alerts` matches events against declarative YAML rules and
   dispatches to Discord, Telegram, or webhooks.

## Client

7. `apps/cli` can work standalone (direct RPC calls) or connect to the API
   for enriched data and historical context.

```text
Solana RPC ──WS──> collector ──gRPC──> api ──WS──> dashboard
                                ├───> analyzer ──> postgres
                                └───> alerts ──> discord/telegram/webhook
```
