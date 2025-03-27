#!/bin/bash
set -e

echo "🔨 Building vox-whisper:cpu image with BuildKit..."
DOCKER_BUILDKIT=1 docker build -f docker/Dockerfile.cpu -t vox-whisper:cpu ./docker
echo "✅ Build complete!"
