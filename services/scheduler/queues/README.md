# Queues

Named Redis streams used by the scheduler.

| Queue | Purpose |
|---|---|
| `analytics.rollup` | Periodic analytics computations |
| `alerts.match` | Rule-matching work for the alerts service |
| `maintenance.cleanup` | Retention/cleanup of old events |
