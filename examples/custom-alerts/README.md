# Custom alerts

Add a rule file under `services/alerts/rules/`:

```yaml
name: my-custom-rule
when:
  metric: rpc_latency_ms
  operator: ">"
  value: 1000
  for: 5m
notify:
  - webhook
```

Restart the alerts service (or point `ALERTS_RULES_DIR` at your own
directory). See `services/alerts/rules/example.yml` for more.
