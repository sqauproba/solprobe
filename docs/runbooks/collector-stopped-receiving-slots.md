# Runbook: Collector stopped receiving slot updates

**Severity**: P2 (medium) — live data stalls; dashboards go stale.

## Symptoms

- Dashboard slot counter freezes.
- Prometheus `solprobe_events_ingested_total` flatlines.
- API `/v1/health` reports collector degraded.

## Likely causes

1. RPC WebSocket disconnected (network blip, provider outage).
2. Subscription cap reached (`COLLECTOR_MAX_SUBSCRIPTIONS`).
3. RPC provider rate-limited the collector.

## Steps

1. Check collector logs for reconnect messages:
   ```bash
   docker compose logs -f collector
   ```
2. Verify connectivity to the RPC endpoint:
   ```bash
   solprobe rpc benchmark --endpoint <endpoint>
   ```
3. Confirm subscription count against the configured cap:
   ```bash
   curl http://localhost:9090/metrics | grep solprobe_active_subscriptions
   ```
4. If capped, reduce watch targets or raise `COLLECTOR_MAX_SUBSCRIPTIONS`.
5. If provider-specific, rotate to a secondary endpoint via `.env` and restart.

## Prevention

- Configure at least two RPC endpoints and fail over.
- Alert on `solprobe_events_ingested_total` stalling (see alerts rules).
