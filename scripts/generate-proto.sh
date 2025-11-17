#!/usr/bin/env bash
# Regenerate language bindings from the Protobuf schemas.
set -euo pipefail

PROTO_DIR="proto"
OUT_DIR="generated"

mkdir -p "$OUT_DIR"

if command -v protoc >/dev/null 2>&1; then
  for f in "$PROTO_DIR"/*.proto; do
    protoc --python_out="$OUT_DIR" --go_out="$OUT_DIR" --go-grpc_out="$OUT_DIR" \
      --rust_out="$OUT_DIR" -I "$PROTO_DIR" "$f"
  done
  echo "generated bindings in $OUT_DIR"
else
  echo "protoc not found; install protoc or generate in CI" >&2
  exit 1
fi
