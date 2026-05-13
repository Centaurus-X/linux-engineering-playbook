# Changelog

## 2026-05-12 - Documentation Restructure Draft

### Added

- New repository structure for `linux-engineering-playbook`.
- English Markdown documentation under `docs/`.
- `Linux_GPU_CUDA` preserved as the `docs/10-linux-gpu-cuda/` category.
- Dedicated script directory under `scripts/`.
- Wiki landing page replacement under `wiki/Home.md`.
- Migration checklist and rename guide under `tools/`.

### Changed

- Converted the former mixed wiki/notebook style into a structured documentation playbook.
- Split GPU/CUDA validation scripts into standalone Python files.
- Moved service automation snippets into dedicated script files where appropriate.
- Reworked security-sensitive notes with safer defaults.

### Security

- The sudo no-password note now recommends command-specific `NOPASSWD` rules instead of global passwordless sudo.
- The Tor guide now defaults to loopback-only control access and explicitly warns against exposing the control port without strict firewalling and authentication.
