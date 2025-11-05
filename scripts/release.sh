#!/usr/bin/env bash
# Cross-service version bump + tag.
# Usage: scripts/release.sh 0.2.0
set -euo pipefail

VERSION="${1:?usage: release.sh <version>}"

if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "invalid version: $VERSION" >&2
  exit 1
fi

echo "$VERSION" > VERSION
git add VERSION CHANGELOG.md
git commit -m "chore: release v${VERSION}"
git tag "v${VERSION}"
git push origin main --tags
echo "released v${VERSION}"
