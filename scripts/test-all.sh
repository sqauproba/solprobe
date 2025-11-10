#!/usr/bin/env bash
# Run every service test suite.
set -euo pipefail

echo "==> CLI"
(cd apps/cli && python -m pytest)

echo "==> Collector"
(cd services/collector && cargo test)

echo "==> API"
(cd services/api && go test ./...)

echo "==> Dashboard"
(cd apps/dashboard && npm test)

echo "==> Analyzer"
(cd services/analyzer && python -m pytest)

echo "==> Alerts"
(cd services/alerts && npm test)

echo "==> All test suites passed."
