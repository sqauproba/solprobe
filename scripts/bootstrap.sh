#!/usr/bin/env bash
# One-shot local environment setup: installs tooling for every service.
set -euo pipefail

echo "==> SolProbe bootstrap"

echo "==> CLI (Python)"
python3 -m venv apps/cli/.venv
apps/cli/.venv/bin/pip install -e "apps/cli[dev]"

echo "==> Analyzer (Python)"
python3 -m venv services/analyzer/.venv
services/analyzer/.venv/bin/pip install -e "services/analyzer[dev]"

echo "==> Collector (Rust)"
(cd services/collector && cargo build)

echo "==> API (Go)"
(cd services/api && go mod download)

echo "==> Dashboard + Alerts (Node)"
(cd apps/dashboard && npm install)
(cd services/alerts && npm install)

echo "==> Done. Run 'make dev' to start the stack."
