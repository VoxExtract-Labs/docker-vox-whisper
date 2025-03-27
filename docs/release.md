## Release Process for `docker-vox-whisper`

This guide outlines the recommended release workflow for the `docker-vox-whisper` project. It uses [`release-it`](https://github.com/release-it/release-it) to automate version bumps, tagging, and triggering Docker image builds.

---

### ✅ Requirements
- You have push access to the repository.
- You are ready to release a stable and tested version.
- The `main` branch is up-to-date.
- `bun` and `release-it` are already installed.

---

### 🚀 Release Workflow

#### 1. **Create a release branch**
```bash
git checkout main
git pull origin main
git checkout -b release/v1.0.0  # Adjust version accordingly
```

#### 2. **Run the release script**
This will:
- Bump `package.json` version
- Create a Git tag
- Push the tag to GitHub

```bash
bun run release
```

> `release-it` is configured to skip GitHub releases. It only bumps, commits, tags, and pushes.

#### 3. **Push the release branch and open a PR**
```bash
git push origin release/v1.0.0
```

Then open a pull request from `release/v1.0.0` → `main`.

#### 4. **GitHub Actions will handle the rest**
Once the PR is merged:
- The Git tag (e.g. `v1.0.0`) will trigger a workflow
- Both CPU and CUDA Docker images will be built and pushed to DockerHub:
    - `voxextractlabs/vox-whisper:cpu-v1.0.0`
    - `voxextractlabs/vox-whisper:cuda-v1.0.0`

---

### 📝 Notes
- Do **not** run `release-it` on `main` directly unless you're bypassing PRs.
- The `release.yml` GitHub Actions workflow will match the tag and determine which images to publish.
- Be sure to verify DockerHub tags and image content post-release.

---

### 🔁 Tagging Strategy
- Format: `<type>-vX.Y.Z`
- Examples:
    - `voxextractlabs/vox-whisper:cpu-v1.0.0`
    - `voxextractlabs/vox-whisper:cuda-v2.1.0`

---

### 📦 Optional: Publish to GHCR
This can be added as an additional step in the future to publish images to GitHub Container Registry.

---

**Maintainer:** VoxExtract Labs <voxextractlabs@gmail.com>

