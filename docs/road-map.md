## `docker-vox-whisper`: Roadmap

### Short Description
Dockerized wrapper for [faster-whisper](https://github.com/SYSTRAN/faster-whisper) with a minimal CLI interface. Includes CPU and CUDA builds, tagging strategy, and CI/CD integration. Built for the **VoiceExtractor** project.

---

### Phase 1: Foundation
- [x] Decide on project direction: use custom CLI for smaller image
- [x] Create GitHub repo `docker-vox-whisper`
- [x] Add `.gitignore`, `LICENSE`, and initial `README.md`
- [x] Set up initial folder structure:
  - `/docker` → Dockerfiles, CLI, sample audio
  - `/scripts` → Build, lint, and test shell scripts
  - `/tmp/test` → Mounted output directory during container tests
  - `/docs` → Project documentation (e.g., `dockerhub.md`)

---

### Phase 2: Tooling Setup
- [x] Initialize project with Bun (for tooling only)
- [x] Add and configure dev tools:
  - [x] `@commitlint/cli` + `@commitlint/config-conventional`
  - [x] `lefthook` for Git hooks
  - [x] `@biomejs/biome` for linting
- [x] Add minimal `package.json` with dev-only dependencies
- [x] Add `prepare` script for CI-friendly install
- [x] Configure `lefthook.yml` and `commitlint.config.cjs`

---

### Phase 3: Docker Setup
- [x] Create two standalone Dockerfiles:
  - `Dockerfile.cpu` — lightweight CPU-only build
  - `Dockerfile.cuda` — full CUDA-compatible image
- [x] Set up model caching via `/models`
- [x] Add `ENV WHISPER_CACHE=/models` support
- [x] Create `/docker/cli.py`
  - [x] Full CLI with validation, error handling, and format options
  - [x] Supports `--input`, `--output`, `--device`, `--output_format`, `--timestamps`
  - [x] Supports SRT formatting, JSON word timestamps, error handling
- [x] Use CLI as Docker `ENTRYPOINT`
- [ ] ✨ (Optional) Add `scripts/transcribe.sh` for host-side wrapper

---

### Phase 4: Transcription & Testing
- [x] Add sample audio: `docker/audio/sample.mp3`
- [x] Add `docker/test.py` to:
  - [x] Transcribe with both CPU and CUDA (if detected)
  - [x] Validate output contents
- [x] Add `scripts/test-image.sh`:
  - [x] Takes `--cpu` or `--cuda`
  - [x] Mounts `tmp/test` and confirms result
  - [x] Handles GPU flags automatically
- [x] CI skips CUDA test (unless run on GPU host)

---

### Phase 5: Automation
- [x] Add `.github/workflows/pr-check.yml`
  - [x] Matrix build: `cpu`, `cuda`
  - [x] Bun setup + lint + Dockerfile lint via Hadolint
  - [x] Build image with BuildKit + cache
  - [x] Test `cpu` image in container
  - [x] Skip CUDA test on GitHub-hosted runners
- [x] Use GHCR cache for faster builds
- [x] Fix Dockerfile caching and build warnings

---

### Phase 6: DockerHub & Distribution
- [x] Tag images using format:
  - `voxextractlabs/vox-whisper:cpu-vX.Y.Z`
  - `voxextractlabs/vox-whisper:cuda-vX.Y.Z`
- [x] Push images to DockerHub
- [x] Create `docs/dockerhub-overview.md`
- [x] Create DockerHub Overview
  - [x] Link to GitHub
  - [x] Explain usage, features, tags, CLI
- [x] Note that **DockerHub install is preferred**

---

### Phase 7: Release Automation (Next PR)
- [x] Integrate `release-it`
  - [x] Manually bump version → Git tag
  - [x] Trigger build + push to DockerHub
  - [x] Autogenerate changelog (optional)
- [x] Add GitHub workflow for publishing on tag
- [ ] Optional: Push to GHCR alongside DockerHub

---

### CLI Feature Goals (`cli.py`)
- [x] Accept CLI args: `--input`, `--output`, `--model`, `--language`, `--device`, `--output_format`
- [x] Fail early on invalid/missing input
- [x] Auto-detect CUDA without importing `torch`
- [x] Export to:
  - [x] Plain text
  - [x] JSON (with optional word timestamps)
  - [x] SRT (with formatted timestamps)
- [x] Handle errors gracefully (file I/O, model errors)
- [x] Runs as non-root user
- [x] Tests and verifies both CPU and GPU logic
- [ ] ✨ Streamed or chunked transcription (Future)
- [ ] ✨ Optional metadata summary in output

