# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `apps/cli`: initial `solprobe` CLI scaffold with `status`, `network health`,
  `rpc benchmark`, `slots watch`, and `tui` commands.
- `services/collector`: Rust ingestion skeleton with slot/account/log
  subscription modules and reconnection backoff.
- `services/api`: Go gateway skeleton with `/v1/health`, `/v1/network`, and
  `/v1/slots/latest` endpoints.
- `services/analyzer`: Python analytics package scaffold (baselines, anomaly
  detection, health scoring).
- `services/alerts`: Node.js rule engine scaffold with Discord/Telegram/webhook
  channel adapters.
- `apps/dashboard`: Next.js (App Router) dashboard skeleton with live slot
  stream hook.
- `proto/`: initial `events`, `metrics`, `health`, and `rpc` schemas.
- `infra/`: Docker Compose, Kubernetes, Terraform, Helm, and
  Prometheus/Grafana monitoring scaffolding.
- Root governance files: `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`,
  `.pre-commit-config.yaml`, and GitHub Actions CI workflows.
