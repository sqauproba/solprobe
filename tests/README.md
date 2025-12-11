# Tests

Cross-service test collateral.

- `integration/` — end-to-end flows across multiple services
- `e2e/` — full-stack user journeys
- `fixtures/` — shared fixtures (sample transactions, accounts, metrics)
- `load/` — load/benchmark harnesses

Each service also has its own unit tests in its directory (see
`Makefile` → `make test-all`).
