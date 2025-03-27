# docker-vox-whisper

Minimal Docker image for [faster-whisper](https://github.com/guillaumekln/faster-whisper) with a built-in CLI for voice transcription.  
Supports both CPU and CUDA images, with validation logic to guide usage. Part of the VoiceExtractor project.

**Maintainer:** VoxExtract Labs <voxextractlabs@gmail.com>

---

## Features

- CPU and GPU (CUDA) Docker builds
- Custom CLI with device compatibility checks
- Output in plain text, JSON, or SRT
- Lightweight and production-ready

---

## 🐳 Images

Using the published Docker images is the **recommended way** to use this tool.

### DockerHub
- https://hub.docker.com/r/voxextractlabs/vox-whisper

### CPU-Only Image
- **Tag:** `voxextractlabs/vox-whisper:cpu-latest`
- **Dockerfile:** `docker/Dockerfile.cpu`
- **Base Image:** `python:3.10-slim`
- **Supports:** Inference on any system (no GPU required)

### CUDA-Enabled Image
- **Tag:** `voxextractlabs/vox-whisper:cuda-latest`
- **Dockerfile:** `docker/Dockerfile.cuda`
- **Base Image:** `nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04`
- **Supports:** GPU inference via NVIDIA runtime + cuDNN (requires `--gpus all`)

### 🔖 Tagging Strategy

- `cpu-v1.0.0`, `cuda-v2.2.1`, etc. — follows `<variant>-v<semver>` format
- `cpu-latest`, `cuda-latest` — track the latest stable version for each variant

---

## 🛠️ Build Instructions

```bash
# CPU Image
scripts/build-dev.sh --cpu

# CUDA Image
scripts/build-dev.sh --cuda
```

---

## ✅ Test Instructions

```bash
# CPU Test (run CLI inside the image and check transcription output)
scripts/test-image.sh --cpu

# CUDA Test (requires NVIDIA runtime)
scripts/test-image.sh --cuda
```

---

## 🚀 CLI Usage

```bash
docker run --rm \
  -v "$PWD/audio:/app/audio" \
  -v "$PWD/output:/app/output" \
  voxextractlabs/vox-whisper:cpu-latest \
  --input /app/audio/input.wav \
  --output /app/output/result.txt \
  --model base \
  --device cpu \
  --language en \
  --output_format txt
```

---

## 🔧 CLI Options

| Flag              | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `--input`         | **(Required)** Path to input audio file                                     |
| `--output`        | Path to output file (overrides `--output_dir`)                             |
| `--output_dir`    | Directory for output file (filename is auto-generated)                     |
| `--model`         | Model size: `tiny`, `base`, `small`, `medium`, `large-v1`, `large-v2`, `large-v3` |
| `--device`        | `cpu`, `cuda`, or `auto` (auto-detects if GPU is available)                |
| `--language`      | Language code for transcription (default: `en`)                            |
| `--output_format` | Output type: `txt`, `json`, `srt`                                           |
| `--timestamps`    | Include word-level timestamps in JSON output                               |
| `--threads`       | Number of CPU threads to use                                                |
| `--verbose`       | Print detailed logs                                                         |

---

## 📁 Project Structure

```
.
├── LICENSE
├── README.md
├── biome.json
├── bun.lockb
├── commitlint.config.cjs
├── docker
│   ├── Dockerfile.cpu
│   ├── Dockerfile.cuda
│   ├── audio
│   │   └── sample.mp3
│   ├── cli.py
│   └── test.py
├── docs
│   └── road-map.md
├── lefthook.yml
├── package.json
├── scripts
│   ├── build-dev.sh
│   ├── lint-image.sh
│   └── test-image.sh
├── tmp
│   └── test
└── tsconfig.json
```

> **Note:** The `bun.lockb`, `package.json`, and associated config files are included only for development tooling like Biome and CommitLint.

---

## 📦 Built With

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [ctranslate2](https://github.com/OpenNMT/CTranslate2)
- [NVIDIA CUDA Images](https://hub.docker.com/r/nvidia/cuda)

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

