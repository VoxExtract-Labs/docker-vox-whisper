#!/bin/bash
set -e

# Parse variant
VARIANT="$1"

if [[ "$VARIANT" == "--cpu" ]]; then
  DOCKERFILE="docker/Dockerfile.cpu"
elif [[ "$VARIANT" == "--cuda" ]]; then
  DOCKERFILE="docker/Dockerfile.cuda"
else
  echo "Usage: $0 [--cpu | --cuda]"
  exit 1
fi

# Check if file exists
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
