# Monitoring

Observability stack for SolProbe itself: Prometheus for metrics collection
and Grafana for dashboards.

## Metrics collected

- Event ingestion rate
- RPC latency
- WebSocket reconnects
- Subscription counts
- Queue depth
- API request latency
- Database latency
- Alert delivery success rate

## Health

Every service exposes a `/v1/health` (API) or gRPC health endpoint
(collector). Kubernetes uses these as liveness/readiness probes.
