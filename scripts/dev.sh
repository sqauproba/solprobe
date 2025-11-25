#!/usr/bin/env bash
# Start the full stack via Docker Compose.
set -euo pipefail

docker compose -f infra/docker-compose.yml up --build "$@"
