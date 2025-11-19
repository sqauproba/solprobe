#!/usr/bin/env bash
# Lint every service.
set -euo pipefail

echo "==> CLI"
(cd apps/cli && black --check . && ruff check .)

echo "==> Collector"
(cd services/collector && cargo fmt --check && cargo clippy -- -D warnings)

echo "==> API"
(cd services/api && go vet ./...)

echo "==> Dashboard"
(cd apps/dashboard && npx eslint . && npx tsc --noEmit)

echo "==> Analyzer"
(cd services/analyzer && black --check . && ruff check .)

echo "==> Alerts"
(cd services/alerts && npx eslint .)

echo "==> All linters clean."
