#!/bin/bash
set -e

DOCKERFILE="docker/Dockerfile.cpu"

if [[ ! -f "$DOCKERFILE" ]]; then
  echo "❌ Dockerfile not found: $DOCKERFILE"
  exit 1
fi

echo "🔍 Linting $DOCKERFILE with Hadolint..."

docker run --rm -i \
  -v "$PWD/docker:/mnt" \
  hadolint/hadolint \
  hadolint "/mnt/$(basename "$DOCKERFILE")" \
  --failure-threshold=error

echo "✅ Lint passed for $DOCKERFILE"
