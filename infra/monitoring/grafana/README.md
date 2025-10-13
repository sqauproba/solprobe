# Grafana

Pre-built dashboards and provisioning live here.

- `grafana-dashboards/` — JSON dashboard definitions
- `provisioning/` — datasource provisioning (Prometheus)

The Grafana container in `docker-compose.yml` is pre-configured with the
Prometheus datasource. Import the dashboards under `grafana-dashboards/` to
visualize collector and API metrics.
