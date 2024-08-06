-- Schema migration 0001: initial slots table.
CREATE TABLE IF NOT EXISTS slots (
    slot          BIGINT PRIMARY KEY,
    parent        BIGINT,
    root          BIGINT,
    status        TEXT NOT NULL DEFAULT 'confirmed',
    received_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_slots_received_at ON slots (received_at);
