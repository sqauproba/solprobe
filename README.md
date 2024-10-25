# 🔎 SolProbe

> **Production-grade Solana observability, diagnostics, and developer tooling — from your terminal to a real-time dashboard.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/CLI-Python-3776AB?logo=python&logoColor=white)](#-architecture)
[![Rust](https://img.shields.io/badge/collector-Rust-orange?logo=rust)](#services)
[![Go](https://img.shields.io/badge/API-Go-00ADD8?logo=go&logoColor=white)](#services)
[![TypeScript](https://img.shields.io/badge/dashboard-TypeScript-3178C6?logo=typescript&logoColor=white)](#services)
[![Node.js](https://img.shields.io/badge/alerts-Node.js-339933?logo=node.js&logoColor=white)](#services)
[![Solana](https://img.shields.io/badge/blockchain-Solana-9945FF?logo=solana)](https://solana.com)
[![Docker](https://img.shields.io/badge/deploy-Docker-2496ED?logo=docker&logoColor=white)](#-quick-start)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen)](#-cicd)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blueviolet.svg)](CONTRIBUTING.md)

---

## 📚 Table of Contents

- [Overview](#overview)
- [Why SolProbe](#-why-solprobe)
- [Architecture](#-architecture)
- [Repository Structure](#-repository-structure)
- [Services](#-services)
  - [CLI (Python)](#1-appscli--python)
  - [Collector (Rust)](#2-servicescollector--rust)
  - [API (Go)](#3-servicesapi--go)
  - [Dashboard (TypeScript / Next.js)](#4-appsdashboard--typescript--nextjs)
  - [Analyzer (Python)](#5-servicesanalyzer--python)
  - [Alerts (Node.js)](#6-servicesalerts--nodejs)
- [Quick Start (Docker Compose)](#-quick-start-docker-compose)
- [Local Development (per service)](#-local-development-per-service)
- [Configuration](#-configuration)
- [CLI Usage](#-cli-usage)
- [API Reference](#-api-reference)
- [Data Flow](#-data-flow)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Observability](#-observability)
- [Security](#-security)
- [CI/CD](#-cicd)
- [Performance](#-performance)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## Overview

Solana moves fast — 400ms slots, thousands of transactions per second, and a sprawling network of RPC providers, programs, and wallets. When something breaks or slows down, developers need answers *now*, not after refreshing a block explorer for the fifth time.

**SolProbe** is an open-source observability and diagnostic platform built specifically for Solana. It combines a fast terminal CLI for instant diagnostics with a real-time backend stack for continuous monitoring, alerting, and analytics.

The project is deliberately polyglot — each component is written in the language best suited to its job:

| Concern | Language | Why |
|---|---|---|
| Developer CLI & diagnostics | **Python** | Rapid iteration, rich terminal libraries (Rich, Textual), broad ecosystem |
| High-throughput event ingestion | **Rust** | Zero-cost abstractions, predictable latency under load, native Solana SDK |
| Public API / auth / rate limiting | **Go** | Simple concurrency model, fast cold starts, easy to operate at scale |
| Real-time dashboard | **TypeScript / Next.js** | Best-in-class ecosystem for reactive, real-time UI |
| Historical analysis & anomaly detection | **Python** | Pandas, NumPy, scikit-learn ecosystem for time-series intelligence |
| Alerting & webhook fan-out | **Node.js** | Lightweight, huge integration ecosystem (Discord.js, Telegraf) |

---

## 🎯 Why SolProbe

- **Terminal-first, not terminal-only.** The CLI gives you instant answers (`solprobe status`, `solprobe rpc benchmark`), while the full stack provides continuous observability.
- **No polling, ever.** The collector subscribes to live WebSocket feeds; nothing loops on REST endpoints.
- **Composable services**, not a monolith — run only the pieces you need.
- **Typed contracts between services** via Protobuf, so the Rust collector, Go API, and TypeScript dashboard all agree on event shapes.
- **Built to run in production** — includes health checks, structured logging, metrics export, horizontal scaling guidance, and operational runbooks.

---

## 🏗 Architecture

```text
                              ┌─────────────────────────┐
                              │    Solana RPC Network    │
                              │                         │
                              │  Mainnet / Devnet / Test │
                              └────────────┬────────────┘
                                           │
                          HTTP RPC + WebSocket subscriptions
                                           │
                                           ▼
                              ┌─────────────────────────┐
                              │   COLLECTOR (Rust)       │
                              │                          │
                              │  slots / logs / blocks   │
                              │  accounts / events       │
                              │  backpressure-aware queue│
                              └────────────┬────────────┘
                                           │
                                gRPC / Protobuf events
                                           │
              ┌────────────────────────────┼────────────────────────────┐
              │                            │                            │
              ▼                            ▼                            ▼
     ┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
     │ API (Go)         │       │ Analyzer (Python)│       │ Alerts (Node.js) │
     │ REST / WebSocket │       │ Trends / scoring │       │ Rules / webhooks │
     │ Auth / limits    │       │ Anomalies        │       │ Telegram/Discord │
     └────────┬─────────┘       └────────┬─────────┘       └──────────────────┘
              │                          │
              ▼                          ▼
     ┌──────────────────┐       ┌──────────────────┐
     │ Dashboard        │       │ PostgreSQL       │
     │ Next.js / TS     │       │ Redis / metrics  │
     │ Live monitoring  │       │ Historical data  │
     └──────────────────┘       └──────────────────┘

                    ┌─────────────────────────────┐
                    │ CLI (Python + Rich/Textual) │
                    │ Direct diagnostics + TUI    │
                    └─────────────────────────────┘
```

---

## 📁 Repository Structure

```text
solprobe/
├── apps/
│   ├── cli/                         # Python CLI + TUI
│   │   ├── solprobe/
│   │   │   ├── commands/
│   │   │   ├── clients/
│   │   │   ├── diagnostics/
│   │   │   ├── formatters/
│   │   │   ├── config/
│   │   │   └── tui/
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   ├── README.md
│   │   └── CHANGELOG.md
│   │
│   └── dashboard/                   # Next.js real-time dashboard
│       ├── app/
│       ├── components/
│       ├── hooks/
│       ├── lib/
│       ├── stores/
│       ├── types/
│       ├── tests/
│       ├── package.json
│       └── Dockerfile
│
├── services/
│   ├── collector/                   # Rust event ingestion
│   │   ├── src/
│   │   │   ├── rpc/
│   │   │   ├── websocket/
│   │   │   ├── subscriptions/
│   │   │   ├── decoders/
│   │   │   ├── metrics/
│   │   │   └── health/
│   │   ├── tests/
│   │   ├── benches/
│   │   ├── Cargo.toml
│   │   └── Dockerfile
│   │
│   ├── api/                         # Go API gateway
│   │   ├── cmd/server/
│   │   ├── internal/
│   │   │   ├── handlers/
│   │   │   ├── middleware/
│   │   │   ├── auth/
│   │   │   ├── ratelimit/
│   │   │   ├── services/
│   │   │   └── repositories/
│   │   ├── migrations/
│   │   ├── go.mod
│   │   └── Dockerfile
│   │
│   ├── analyzer/                    # Python analytics
│   │   ├── solprobe_analyzer/
│   │   │   ├── network/
│   │   │   ├── transactions/
│   │   │   ├── anomalies/
│   │   │   ├── scoring/
│   │   │   └── reports/
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── Dockerfile
│   │
│   ├── alerts/                      # Node.js notification workers
│   │   ├── src/
│   │   │   ├── rules/
│   │   │   ├── channels/
│   │   │   └── workers/
│   │   ├── package.json
│   │   └── Dockerfile
│   │
│   └── scheduler/                   # Background jobs
│       ├── jobs/
│       ├── queues/
│       └── workers/
│
├── packages/
│   ├── sdk-python/
│   ├── sdk-typescript/
│   ├── sdk-go/
│   ├── config/
│   └── shared-types/
│
├── proto/
│   ├── events.proto
│   ├── metrics.proto
│   ├── health.proto
│   └── rpc.proto
│
├── contracts/
│   └── programs/
│       └── solprobe_registry/       # Optional Anchor program
│
├── infra/
│   ├── docker/
│   ├── kubernetes/
│   ├── terraform/
│   ├── helm/
│   ├── monitoring/
│   │   ├── prometheus/
│   │   └── grafana/
│   └── docker-compose.yml
│
├── docs/
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── data-flow.md
│   │   └── adr/
│   │       ├── 0001-event-driven-architecture.md
│   │       ├── 0002-rpc-provider-abstraction.md
│   │       └── 0003-polyglot-services.md
│   ├── guides/
│   ├── api/
│   ├── cli/
│   ├── deployment/
│   └── runbooks/
│
├── examples/
│   ├── basic-cli/
│   ├── python-sdk/
│   ├── typescript-sdk/
│   ├── wallet-monitoring/
│   ├── custom-alerts/
│   └── docker-deployment/
│
├── tests/
│   ├── integration/
│   ├── e2e/
│   ├── fixtures/
│   └── load/
│
├── benchmarks/
│   ├── rpc/
│   ├── websocket/
│   └── transaction/
│
├── scripts/
│   ├── bootstrap.sh                 # one-shot local env setup
│   ├── dev.sh
│   ├── test-all.sh
│   ├── lint-all.sh
│   ├── release.sh                   # cross-service version bump + tag
│   ├── generate-proto.sh
│   └── seed-dev-data.sh
│
├── .github/
│   ├── workflows/                   # CI/CD pipelines (per-service + release)
│   │   ├── cli-ci.yml
│   │   ├── collector-ci.yml
│   │   ├── api-ci.yml
│   │   ├── dashboard-ci.yml
│   │   ├── analyzer-ci.yml
│   │   ├── security.yml
│   │   ├── release.yml
│   │   └── docker.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── CODEOWNERS
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── dependabot.yml
│
├── .env.example
├── .editorconfig
├── .gitignore
├── .dockerignore
├── .pre-commit-config.yaml
├── Makefile                         # make dev / make test-all / make release
├── CHANGELOG.md                     # root-level, aggregates per-service releases
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
├── VERSION
└── README.md
```

### Root-level files at a glance

| File | Purpose |
|---|---|
| `CODEOWNERS` | Auto-assigns reviewers per directory (e.g. `/services/collector/` → Rust maintainers) |
| `dependabot.yml` | Automated dependency update PRs across all five package ecosystems |
| `.pre-commit-config.yaml` | Runs formatters/linters (`black`, `rustfmt`, `gofmt`, `eslint`) before every commit |
| `CHANGELOG.md` | Root-level changelog aggregating notable changes across all services, [Keep a Changelog](https://keepachangelog.com/) format |
| `SECURITY.md` | Vulnerability disclosure policy and supported version table |
| `CODE_OF_CONDUCT.md` | [Contributor Covenant](https://www.contributor-covenant.org/) v2.1 |
| `VERSION` | Current release version, read by `scripts/release.sh` for tagging |
| `Makefile` | Single entrypoint for common tasks across all services (`make test-all`, `make lint-all`, `make dev`) |
| `docs/architecture/adr/` | Architecture Decision Records — the *why* behind major structural choices |
| `docs/runbooks/` | Step-by-step operational guides for on-call (e.g. "collector stopped receiving slot updates") |

---

## 🧩 Services

### 1. `apps/cli` — Python

The primary developer interface. Built around a fast command architecture with rich terminal output and an optional full-screen terminal UI.

- CLI framework: `typer`
- Terminal rendering: `rich`
- TUI framework: `textual`
- HTTP client: `httpx`
- Validation: `pydantic`

**Commands:**

```bash
solprobe status
solprobe network health
solprobe rpc benchmark
solprobe rpc compare
solprobe slots latest
solprobe slots watch
solprobe fees
solprobe wallet inspect <ADDRESS>
solprobe wallet watch <ADDRESS>
solprobe program inspect <PROGRAM_ID>
solprobe program logs <PROGRAM_ID>
solprobe tx inspect <SIGNATURE>
solprobe tx simulate <FILE>
solprobe tui
```

---

### 2. `services/collector` — Rust

The high-throughput ingestion layer. Maintains persistent RPC and WebSocket connections, manages subscriptions, normalizes incoming Solana events, and publishes typed events to downstream services.

- Async runtime: `tokio`
- WebSocket client: `tokio-tungstenite`
- Solana SDK: `solana-client`, `solana-sdk`
- Backpressure-aware bounded channel to prevent memory blowup under bursty load
- Automatic reconnect with exponential backoff on RPC disconnects

**Responsibilities:**

- Slot subscriptions
- Block subscriptions
- Account subscriptions
- Program subscriptions
- Log subscriptions
- Reconnection and backoff
- Subscription health checks
- Event normalization
- Metrics emission

---

### 3. `services/api` — Go

The public API gateway. Exposes REST and WebSocket endpoints over data produced by `collector`, handles authentication, and enforces per-client rate limits.

- HTTP framework: `chi`
- GraphQL: `gqlgen` *(planned)*
- Auth: JWT + API key middleware
- Structured logging: `zap`

**Example endpoints:**

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v1/health` | Overall platform health |
| `GET` | `/v1/network` | Network metrics (TPS, slot time, skip rate) |
| `GET` | `/v1/slots/latest` | Latest processed slot and finality status |
| `GET` | `/v1/slots/stream` | WebSocket relay of live slot events |
| `GET` | `/v1/rpc/benchmark` | RPC benchmark results |
| `GET` | `/v1/wallets/{address}` | Wallet inspection (balances, activity) |
| `GET` | `/v1/programs/{id}` | Program metadata and details |
| `GET` | `/v1/programs/{id}/logs` | Recent program logs |
| `GET` | `/v1/transactions/{signature}` | Transaction diagnostics |
| `POST` | `/v1/alerts` | Create alert rule |
| `GET` | `/v1/stream` | WebSocket stream of live events |

Full OpenAPI spec: [`docs/api/openapi.yaml`](docs/api/openapi.yaml) *(generated from `services/api/`)*.

---

### 4. `apps/dashboard` — TypeScript / Next.js

The live UI. Connects to `api`'s WebSocket relay and renders real-time feeds, charts, and alerts.

- Framework: Next.js 14 (App Router)
- State/data: React Query + lightweight WebSocket hook
- Charts: `recharts`
- Styling: Tailwind CSS

---

### 5. `services/analyzer` — Python

The intelligence layer. Processes collected metrics and historical data to identify RPC degradation, slot lag, transaction failure spikes, abnormal compute consumption, and network anomalies.

- Data: `pandas`, `numpy`
- Modeling: `scikit-learn`
- Scheduling: `celery` + Redis for periodic jobs
- Notebooks in `services/analyzer/notebooks/` for exploratory work

---

### 6. `services/alerts` — Node.js

The notification layer. Subscribes to rule-matched events and fans them out to Discord, Telegram, or arbitrary webhooks.

- `discord.js` for Discord integration
- `telegraf` for Telegram bots
- Rule engine: simple declarative YAML rules matched against incoming event streams

**Example rule:**

```yaml
name: rpc-degradation
when:
  metric: rpc_latency_ms
  operator: ">"
  value: 500
  for: 60s

notify:
  - discord
  - webhook
```

---

## 🚀 Quick Start (Docker Compose)

The fastest way to run the full stack locally:

```bash
git clone https://github.com/<your-username>/solprobe.git
cd solprobe
cp .env.example .env   # fill in your RPC endpoint and secrets
docker compose -f infra/docker-compose.yml up --build
```

This brings up:

| Service | Port |
|---|---|
| `dashboard` | `3000` |
| `api` (REST/GraphQL) | `8080` |
| `collector` (gRPC) | `50051` |
| PostgreSQL | `5432` |
| Redis | `6379` |
| Prometheus | `9090` |
| Grafana | `3001` |

Open `http://localhost:3000` once containers are healthy.

---

## 🛠 Local Development (per service)

<details>
<summary><strong>CLI (Python)</strong></summary>

```bash
cd apps/cli
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
solprobe --help
```

Requires Python `>= 3.11`.
</details>

<details>
<summary><strong>Collector (Rust)</strong></summary>

```bash
cd services/collector
cargo build
cargo run
```

Requires Rust `>= 1.75` (`rustup update stable`).
</details>

<details>
<summary><strong>API (Go)</strong></summary>

```bash
cd services/api
go mod download
go run ./cmd/server
```

Requires Go `>= 1.22`.
</details>

<details>
<summary><strong>Dashboard (TypeScript / Next.js)</strong></summary>

```bash
cd apps/dashboard
npm install
npm run dev
```

Requires Node.js `>= 18`.
</details>

<details>
<summary><strong>Analyzer (Python)</strong></summary>

```bash
cd services/analyzer
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Requires Python `>= 3.11`.
</details>

<details>
<summary><strong>Alerts (Node.js)</strong></summary>

```bash
cd services/alerts
npm install
npm run dev
```

Requires Node.js `>= 18`.
</details>

---

## ⚙️ Configuration

Root-level `.env` (referenced by `docker-compose.yml`):

```env
# Solana
SOLPROBE_CLUSTER=mainnet-beta
SOLANA_RPC_ENDPOINT=https://your-rpc-provider.com
SOLANA_WS_ENDPOINT=wss://your-rpc-provider.com/ws

# Watch targets (optional, comma-separated)
WATCH_ADDRESSES=
WATCH_PROGRAM_IDS=

# Storage
DATABASE_URL=postgres://solprobe:solprobe@postgres:5432/solprobe
REDIS_URL=redis://redis:6379

# API
API_HOST=0.0.0.0
API_PORT=8080
JWT_SECRET=
API_RATE_LIMIT_PER_MINUTE=120

# Collector
COLLECTOR_MAX_SUBSCRIPTIONS=500
COLLECTOR_RECONNECT_MAX_SECONDS=60

# Alerts
DISCORD_WEBHOOK_URL=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Observability
LOG_LEVEL=info
METRICS_ENABLED=true
```

Each service also supports a local `.env` inside its own directory for service-specific overrides during development.

**Never commit real secrets or production credentials.**

---

## 💻 CLI Usage

Check network health:

```bash
solprobe network health
```

Benchmark an RPC:

```bash
solprobe rpc benchmark   --endpoint https://api.mainnet-beta.solana.com
```

Compare endpoints:

```bash
solprobe rpc compare   --endpoint https://rpc-1.example.com   --endpoint https://rpc-2.example.com
```

Watch slots:

```bash
solprobe slots watch
```

Inspect a wallet:

```bash
solprobe wallet inspect <SOLANA_ADDRESS>
```

Launch the terminal UI:

```bash
solprobe tui
```

---

## 📡 API Reference

Base URL (local): `http://localhost:8080`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v1/health` | Overall platform health |
| `GET` | `/v1/network` | Network metrics (TPS, slot time, skip rate) |
| `GET` | `/v1/slots/latest` | Latest processed slot and finality status |
| `GET` | `/v1/slots/stream` | WebSocket relay of live slot events |
| `GET` | `/v1/rpc/benchmark` | RPC benchmark results |
| `GET` | `/v1/wallets/{address}` | Wallet inspection (balances, activity) |
| `GET` | `/v1/programs/{id}` | Program metadata and details |
| `GET` | `/v1/programs/{id}/logs` | Recent program logs |
| `GET` | `/v1/transactions/{signature}` | Transaction diagnostics |
| `POST` | `/v1/alerts` | Create alert rule |
| `GET` | `/v1/stream` | WebSocket stream of live events |

Full OpenAPI spec: [`docs/api/openapi.yaml`](docs/api/openapi.yaml).

---

## 🔄 Data Flow

1. `collector` opens WebSocket subscriptions to the configured Solana RPC (`slotSubscribe`, `accountSubscribe`, `logsSubscribe`, `programSubscribe`).
2. Raw events are decoded into typed Protobuf messages (schema in `proto/`).
3. Events are published over gRPC to `api`, `alerts`, and `analyzer` simultaneously.
4. `api` relays live events to `dashboard` over WebSocket and serves historical queries from PostgreSQL.
5. `analyzer` runs scheduled jobs (via Celery) to compute rolling baselines and flag anomalies, writing results back to Postgres for `api` to serve.
6. `alerts` matches events against declarative YAML rules and dispatches to Discord, Telegram, or webhooks.
7. `cli` can work standalone (direct RPC calls) or connect to `api` for enriched data and historical context.

---

## ✅ Testing

| Service | Command | Framework |
|---|---|---|
| CLI | `pytest` | Pytest |
| Collector | `cargo test` | Rust built-in test harness |
| API | `go test ./...` | Go built-in `testing` |
| Dashboard | `npm run test` | Vitest + React Testing Library |
| Analyzer | `pytest` | Pytest |
| Alerts | `npm test` | Jest |

Run everything at once from the repo root:

```bash
make test-all
```

Lint everything:

```bash
make lint-all
```

---

## 🚢 Deployment

- **Docker:** each service ships its own `Dockerfile`; `infra/docker-compose.yml` covers local/staging use.
- **Kubernetes:** manifests in `infra/kubernetes/` (Deployments, Services, HPA for `collector` and `api`).
- **Terraform:** `infra/terraform/` provisions managed Postgres, Redis, and container hosting on your cloud provider of choice.
- **Helm:** `infra/helm/` supports repeatable cluster deployment.

```bash
# Example: deploy to an existing k8s cluster
kubectl apply -f infra/kubernetes/
```

---

## 📊 Observability

SolProbe monitors itself.

### Metrics

- Event ingestion rate
- RPC latency
- WebSocket reconnects
- Subscription counts
- Queue depth
- API request latency
- Database latency
- Alert delivery success rate

### Monitoring stack

- **Prometheus** — metrics collection
- **Grafana** — dashboards and visualizations
- **Structured logs** — JSON logging across all services
- **Health endpoints** — per-service liveness/readiness probes

Health check:

```bash
curl http://localhost:8080/v1/health
```

Example response:

```json
{
  "status": "healthy",
  "score": 98,
  "services": {
    "collector": "healthy",
    "api": "healthy",
    "database": "healthy",
    "redis": "healthy"
  }
}
```

---

## 🔐 Security

SolProbe is designed to be safe for read-only infrastructure monitoring.

- **No private key is required** for normal monitoring — `collector` only subscribes to public chain data.
- Secrets are loaded from environment variables only; nothing is committed to the repo. See [`.env.example`](.env.example).
- API authentication is optional for local development and configurable for production.
- Rate limiting protects public endpoints.
- Input validation is applied at API and CLI boundaries.
- Dependencies are checked through automated security workflows.
- Report vulnerabilities privately per [`SECURITY.md`](SECURITY.md) rather than opening a public issue.

### Important

Never place these values in Git:

```text
PRIVATE_KEY
SEED_PHRASE
JWT_SECRET
DATABASE_PASSWORD
TELEGRAM_BOT_TOKEN
PROVIDER_API_KEY
```

---

## 🔁 CI/CD

GitHub Actions workflows in `.github/workflows/`:

- `cli-ci.yml` — `black`, `ruff`, `pytest`
- `collector-ci.yml` — `cargo fmt --check`, `clippy`, `cargo test`
- `api-ci.yml` — `go vet`, `golangci-lint`, `go test`
- `dashboard-ci.yml` — `eslint`, `tsc --noEmit`, `vitest`
- `analyzer-ci.yml` — `black`, `ruff`, `pytest`
- `alerts-ci.yml` — `eslint`, `jest`
- `security.yml` — dependency vulnerability scanning
- `docker.yml` — builds and pushes images on tagged releases
- `release.yml` — cross-service version bump + tag automation

---

## ⚡ Performance

SolProbe is designed around several principles:

- Prefer persistent connections for live data.
- Use bounded queues to prevent memory growth.
- Apply backpressure instead of silently dropping critical events.
- Keep hot ingestion paths lightweight.
- Separate collection from analysis.
- Avoid unnecessary polling.
- Batch historical writes.
- Cache expensive repeated reads.

Performance benchmarks belong in:

```text
benchmarks/
```

Benchmark categories include:

- RPC latency
- WebSocket reconnect behavior
- Event throughput
- Transaction inspection
- API throughput

Actual benchmark results should be generated from reproducible test runs rather than hard-coded marketing numbers.

---

## 🗺 Roadmap

### v0.1 — Foundation
- [x] Python CLI with `status`, `rpc benchmark`, `slots watch`
- [x] Rich terminal output and configuration system
- [x] Direct RPC diagnostics (no backend required)

### v0.2 — Diagnostics
- [x] Wallet inspection
- [x] Transaction inspection and simulation
- [x] Program inspection and log streaming
- [x] Compute diagnostics and priority fee analysis
- [x] Interactive TUI (`solprobe tui`)

### v0.3 — Full Platform
- [ ] Rust collector with live WebSocket ingestion
- [ ] Go API with REST and WebSocket relay
- [ ] PostgreSQL + Redis storage layer
- [ ] Next.js real-time dashboard
- [ ] Python SDK and TypeScript SDK

### v0.4 — Intelligence
- [ ] Historical analytics and trend detection
- [ ] Network anomaly detection
- [ ] Health scoring algorithm
- [ ] RPC provider comparison reports
- [ ] Automated incident reports

### v1.0 — Production
- [ ] Stable public API
- [ ] Complete Helm charts and Terraform modules
- [ ] Prometheus/Grafana observability stack
- [ ] Production deployment guides
- [ ] Community plugin ecosystem

---

## 🤝 Contributing

Contributions are welcome across any of the six services. Please open an issue to discuss significant changes before submitting a PR.

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Make your changes in the relevant service directory
4. Run that service's test suite (see [Testing](#-testing))
5. Commit using [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `ci:`, `perf:`)
6. Open a Pull Request

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full guidelines, including per-language style conventions.

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

## 🙏 Acknowledgments

- [Solana Labs](https://solana.com) for the core protocol
- [Anchor](https://www.anchor-lang.com/) for on-chain program tooling
- [Helius](https://helius.dev) / [QuickNode](https://quicknode.com) for RPC infrastructure
- The maintainers of `tokio`, `chi`, `typer`, `rich`, `textual`, `pandas`, and `recharts` — the backbone of this project's polyglot stack

---

<div align="center">

### 🔎 SolProbe

**Observe. Diagnose. Understand Solana.**

</div>
