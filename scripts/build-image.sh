#!/bin/bash
set -e

# Default to CPU if no argument is passed
VARIANT="$1"

if [[ "$VARIANT" == "--cpu" ]]; then
  TAG="vox-whisper:cpu"
  DOCKERFILE="docker/Dockerfile.cpu"
elif [[ "$VARIANT" == "--cuda" ]]; then
  TAG="vox-whisper:cuda"
  DOCKERFILE="docker/Dockerfile.cuda"
else
  echo "Usage: $0 [--cpu | --cuda]"
  exit 1
fi

echo "🔨 Building $TAG using $DOCKERFILE with BuildKit..."
DOCKER_BUILDKIT=1 docker build -f "$DOCKERFILE" -t "$TAG" ./docker
echo "✅ Build complete!"
