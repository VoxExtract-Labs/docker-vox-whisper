## docker-vox-whisper: Roadmap

### Short Description
Dockerized wrapper for faster-whisper with a minimal CLI interface. Includes CPU and GPU builds, CLI validation, and testing support. Built for VoiceExtractor.

---

### Phase 1: Foundation
- [x] Decide on project direction: use custom CLI for smaller image
- [x] Create GitHub repo `docker-vox-whisper`
- [x] Add `.gitignore`, `LICENSE`, and `README.md`
- [ ] Set up initial folder structure:
  - `/docker` (for Dockerfiles)
  - `/scripts` (for CLI + helpers)
  - `/test` (for audio samples + test code)

---

### Phase 2: Tooling Setup
- [x] Initialize `bun` project with `bun init`
- [x] Add and configure:
  - [x] `@commitlint/cli` and `@commitlint/config-conventional`
  - [x] `lefthook` for Git hooks
  - [x] `Biome` for linting
- [x] Create `commitlint.config.js`
- [x] Create `.lefthook.yml` config
- [x] Run `bun install` and `npx lefthook install`
- [x] Verify Conventional Commits are enforced on commit

---

### Phase 3: Docker Setup
- [ ] Create two separate Dockerfiles:
  - `Dockerfile.cpu` → Lean image, for CI/dev/fallback
  - `Dockerfile.cuda` → Full CUDA image, for GPU-accelerated production
- [x] Pre-download default model (e.g., `base`) in the image for faster CI runs
- [x] Allow overriding model and cache directory via environment variable or volume mount
- [x] Write `scripts/cli.py` — custom CLI for faster-whisper
  - [x] Accepts: `--input`, `--output`, `--device`, `--model`, `--language`, `--output_format`
  - [ ] Detect device compatibility and throw an error if `cuda` is requested in CPU-only build
  - [ ] Basic stdout + file export (TXT/JSON/SRT)
- [ ] Add `scripts/transcribe.sh` wrapper (optional)
- [x] Use CLI as Docker `ENTRYPOINT`

---

### Phase 4: Transcription & Testing
- [x] Add sample audio file (`test/audio/sample.mp3`)
- [x] Write `test/test.py` to:
  - [x] Run CLI on sample audio
  - [x] Validate output file or stdout
  - [ ] Confirm behavior in both CPU and CUDA builds
- [ ] Use shell scripts for test orchestration (Bun still available as needed)

---

### Phase 5: Automation
- [x] Create GitHub Actions workflow (`.github/workflows/pr-check.yml`)
  - [x] Install and lint with Bun
  - [x] Set up Docker Buildx (caching infra in place)
  - [ ] Lint Dockerfiles
  - [x] Build Docker image (CPU) and test it
  - [x] Run `test/test.py` in container to validate CLI

---

### Phase 6: Polish & Release
- [ ] Update `README.md` with:
  - [ ] CLI usage examples
  - [ ] CPU vs CUDA image behavior
  - [ ] Docker build/run instructions
  - [ ] Sample output
- [ ] Tag initial version

---

### CLI Feature Goals (`scripts/cli.py`)
- [x] Accept CLI arguments: `--input`, `--output`, `--model`, `--language`, `--device`, `--output_format`
- [x] Validate device availability (e.g., fail on `--device cuda` if no GPU)
- [x] Export to text, JSON, or SRT
- [x] Print summary or stats
- [ ] Stream or batch transcription support

