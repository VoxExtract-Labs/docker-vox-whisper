# docker-vox-whisper

Minimal Docker image for [faster-whisper](https://github.com/SYSTRAN/faster-whisper) with a built-in CLI for voice transcription. Supports both CPU and GPU (CUDA) inference using separate image tags.

## 🚀 Quick Start

CPU-only:
```bash
docker run --rm \
  -v "$PWD/audio:/app/audio" \
  -v "$PWD/output:/app/output" \
  voxextractlabs/vox-whisper:cpu-v1.0.0 \
  --input /app/audio/input.wav \
  --output /app/output/result.txt
```

GPU (CUDA):
```bash
docker run --rm --gpus all \
  -v "$PWD/audio:/app/audio" \
  -v "$PWD/output:/app/output" \
  voxextractlabs/vox-whisper:cuda-v1.0.0 \
  --input /app/audio/input.wav \
  --output /app/output/result.txt \
  --device cuda
```

## 🔧 Features
- Supports `txt`, `json`, and `srt` outputs
- Automatically detects GPU support (with `--device auto`)
- Models downloaded and cached in `/models`
- Runs as non-root user

## 🏷️ Tagging Strategy
DockerHub images follow this tag format:

- `cpu-vX.Y.Z` — CPU-only image
- `cuda-vX.Y.Z` — CUDA-enabled image (requires NVIDIA runtime)

Example:
```bash
docker pull voxextractlabs/vox-whisper:cpu-v1.0.0
```

💡 *The recommended way to use this image is via [DockerHub](https://hub.docker.com/r/voxextractlabs/vox-whisper). See tag strategy above for version selection.*

## 🌐 CLI Options
```bash
--input <path>         # Required input audio file
--output <path>        # Output file path
--model <size>         # tiny, base, small, medium, large-*
--device <cpu|cuda>    # Inference device
--language <code>      # Default is 'en'
--output_format <fmt>  # txt, json, srt
--timestamps           # Include word-level timestamps (JSON only)
--threads <int>        # Number of CPU threads
--verbose              # Enable debug logging
```

## 💪 Maintained By
VoxExtract Labs <voxextractlabs@gmail.com>

---

Source code available at: https://github.com/VoxExtract-Labs/docker-vox-whisper

