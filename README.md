# Linux Engineering Playbook

A practical, version-controlled Linux systems engineering documentation collection.

This repository contains curated guides, notes, and operational playbooks for:

- Linux GPU and CUDA setups
- Proxmox virtualization and GPU passthrough
- Python environments and advanced Python builds
- Linux administration notes
- Linux service integration notes

The former `Linux_GPU_CUDA` scope is preserved as a dedicated documentation category under:

```text
docs/10-linux-gpu-cuda/
```

## Documentation Index

Start here:

- [Documentation Home](docs/README.md)
- [Documentation Map](docs/00-overview/documentation-map.md)
- [Writing and Style Guide](docs/00-overview/writing-and-style-guide.md)

## Main Categories

| Category | Path | Purpose |
|---|---|---|
| Linux GPU CUDA | [`docs/10-linux-gpu-cuda/`](docs/10-linux-gpu-cuda/) | NVIDIA driver, CUDA, cuDNN, TensorFlow and PyTorch GPU validation |
| Proxmox Virtualization | [`docs/20-proxmox-virtualization/`](docs/20-proxmox-virtualization/) | GPU passthrough and virtualization notes |
| Python Engineering | [`docs/30-python-engineering/`](docs/30-python-engineering/) | pip, virtual environments, requirements files, multiple Python versions, Python 3.13 free-threading |
| Linux Administration | [`docs/40-linux-administration/`](docs/40-linux-administration/) | sudo policy notes and local admin experiments |
| Linux Services | [`docs/50-linux-services/`](docs/50-linux-services/) | PostgreSQL LISTEN/NOTIFY, RustDesk audio, Tor proxy notes |
| Archive | [`docs/90-archive/`](docs/90-archive/) | Legacy wiki page mapping and migration notes |

## Repository Philosophy

This repository is not only a wiki replacement. It is a maintainable engineering knowledge base:

- Markdown files live in the main Git history.
- Scripts live outside Markdown under `scripts/`.
- The GitHub Wiki is reduced to a small landing page that links back to `docs/`.
- Dangerous or security-sensitive guides contain explicit warnings and safer defaults.
- Each guide has a clear title, scope, prerequisites, commands, validation steps, and rollback notes.

## Suggested Repository Name

Recommended repository name:

```text
linux-engineering-playbook
```

Alternative display title:

```text
Linux Engineering Playbook
```

## License

Keep the existing repository license unless you intentionally change the project license.
