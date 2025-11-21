#!/usr/bin/env bash
# Seed development data into Postgres (fixtures from tests/fixtures).
set -euo pipefail

DB_URL="${DATABASE_URL:-postgres://solprobe:solprobe@localhost:5432/solprobe}"

psql "$DB_URL" <<'SQL'
INSERT INTO slots (slot, parent, root, status)
SELECT g, g - 1, g - 100, 'confirmed'
FROM generate_series(305000000, 305001000) AS g
ON CONFLICT (slot) DO NOTHING;
SQL

echo "seeded 1001 slot rows"
