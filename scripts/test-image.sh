#!/bin/bash
set -e

OUTPUT_DIR="tmp/test"
OUTPUT_FILE="$OUTPUT_DIR/transcript.txt"

# Prepare clean output directory
mkdir -p "$OUTPUT_DIR"
chmod 777 "$OUTPUT_DIR"  # 🔐 Ensure container has write access
rm -f "$OUTPUT_FILE"

echo "🚀 Running containerized test..."
docker run --rm \
  -v "$PWD/$OUTPUT_DIR:/app/output" \
  --entrypoint python3 \
  vox-whisper:cpu \
  /app/test.py

# Confirm file was created
if [ -f "$OUTPUT_FILE" ]; then
  echo "✅ Transcript generated at $OUTPUT_FILE"
else
  echo "❌ Test failed: No transcript file found"
  exit 1
fi
