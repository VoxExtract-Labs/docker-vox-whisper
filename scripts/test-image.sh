#!/bin/bash
set -e

# Parse variant
VARIANT="$1"

if [[ "$VARIANT" == "--cpu" ]]; then
  IMAGE="vox-whisper:cpu"
elif [[ "$VARIANT" == "--cuda" ]]; then
  IMAGE="vox-whisper:cuda"
else
  echo "Usage: $0 [--cpu | --cuda]"
  exit 1
fi

OUTPUT_DIR="tmp/test"
OUTPUT_FILE="$OUTPUT_DIR/transcript.txt"

# Prepare clean output directory
mkdir -p "$OUTPUT_DIR"
chmod 777 "$OUTPUT_DIR"  # 🔐 Ensure container has write access
rm -f "$OUTPUT_FILE"

echo "🚀 Running containerized test with image $IMAGE..."
docker run --rm \
  -v "$PWD/$OUTPUT_DIR:/app/output" \
  --entrypoint python3 \
  "$IMAGE" \
  /app/test.py

# Confirm file was created
if [ -f "$OUTPUT_FILE" ]; then
  echo "✅ Transcript generated at $OUTPUT_FILE"
else
  echo "❌ Test failed: No transcript file found"
  exit 1
fi
