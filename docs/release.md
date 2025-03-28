## `docker-vox-whisper`: Release Guide

### Overview
This document outlines the steps for publishing and releasing new versions of the Docker images (`cpu` and `cuda`) for the `docker-vox-whisper` project.

---

### 🧩 Prerequisites
- DockerHub account with access to `voxextractlabs/vox-whisper`
- `release-it` installed via devDependencies
- Logged in to DockerHub locally via `docker login`

---

### 🚀 Release Workflow (Manual)

1. **Ensure main is up-to-date**
```bash
git checkout main
git pull origin main
```

2. **Run release-it** (bumps version, creates tag, commits)
```bash
bun run release
```

3. **Push the tag + version bump commit**
```bash
git push --follow-tags
```

4. **GitHub Actions builds and pushes images**
- A `release.yml` workflow will build both images and publish them to **DockerHub**.
- Each image is tagged using format:
  - `voxextractlabs/vox-whisper:cpu-vX.Y.Z`
  - `voxextractlabs/vox-whisper:cuda-vX.Y.Z`

---

### 🧪 Testing Before Releasing

```bash
./scripts/build-dev.sh --cpu
./scripts/test-image.sh --cpu

./scripts/build-dev.sh --cuda
./scripts/test-image.sh --cuda
```

Ensure both pass before running `release-it`.

---

### 🐳 Publish to GHCR (Optional)

GHCR (GitHub Container Registry) is a powerful alternative or supplement to DockerHub:

#### ✅ Benefits of GHCR
- **Seamless GitHub integration**: Uses `GITHUB_TOKEN` for auth.
- **Free private repos** (great for early-stage/internal builds).
- **Fine-grained permissions**: org, team, or repo-based.
- **Traceability**: Tied to repo tags/releases.
- **Faster GitHub CI pulls**: Optimized for use with GitHub Actions.
- **Cleaner monorepo workflows**: Keep everything in GitHub.

#### When to Prefer DockerHub
- Broader discoverability.
- Zero-auth public pulls.
- More familiar to general Docker users.

✅ **Dual-publishing is ideal** — support both `docker pull` from DockerHub and GHCR.

---

### 🔖 Tagging Strategy
Use the following tag structure:

- `cpu-vX.Y.Z` → CPU-only image
- `cuda-vX.Y.Z` → GPU (CUDA) image

Examples:
```bash
voxextractlabs/vox-whisper:cpu-v1.0.0
voxextractlabs/vox-whisper:cuda-v1.1.2
```

---

### 📝 Notes
- Do **not** use `latest` tags to avoid ambiguity.
- CI uses `ci-cache` tags and does **not** publish to public registries.
- Only stable, tagged releases should be published to DockerHub/GHCR.

---

Maintainer: **VoxExtract Labs** (<voxextractlabs@gmail.com>)

