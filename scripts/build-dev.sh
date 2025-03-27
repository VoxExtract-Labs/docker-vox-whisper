#!/bin/bash
set -e

echo "🔨 Building vox-whisper:cpu image..."
docker build -f docker/Dockerfile.cpu -t vox-whisper:cpu ./docker
echo "✅ Build complete!"
