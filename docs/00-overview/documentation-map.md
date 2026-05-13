# Documentation Map

## Repository Scope

`linux-engineering-playbook` is a structured technical documentation repository for practical Linux systems engineering.

It replaces a mixed GitHub Wiki with versioned Markdown files in the main repository.

## Topic Map

```text
linux-engineering-playbook/
├─ docs/
│  ├─ 00-overview/
│  │  ├─ documentation-map.md
│  │  └─ writing-and-style-guide.md
│  ├─ 10-linux-gpu-cuda/
│  │  ├─ ubuntu-22-04-nvidia-driver-and-cuda.md
│  │  ├─ ubuntu-22-04-cudnn.md
│  │  ├─ tensorflow-gpu-validation.md
│  │  └─ pytorch-gpu-validation.md
│  ├─ 20-proxmox-virtualization/
│  │  └─ proxmox-gpu-passthrough.md
│  ├─ 30-python-engineering/
│  │  ├─ pip-on-ubuntu-22-04.md
│  │  ├─ python-virtual-environments.md
│  │  ├─ requirements-txt-workflow.md
│  │  ├─ multiple-python-versions-on-ubuntu-22-04.md
│  │  └─ python-313-free-threading-on-ubuntu-2404.md
│  ├─ 40-linux-administration/
│  │  ├─ sudo-nopasswd-safe-usage.md
│  │  └─ keyboard-lock-python-notes.md
│  ├─ 50-linux-services/
│  │  ├─ postgresql-listen-notify.md
│  │  ├─ rustdesk-audio-bridge-ubuntu-2404.md
│  │  └─ tor-proxy-ip-rotation-ubuntu-2404.md
│  └─ 90-archive/
│     └─ legacy-wiki-page-map.md
├─ scripts/
│  ├─ gpu/
│  ├─ audio/
│  ├─ tor/
│  └─ python/
├─ tools/
└─ wiki/
```

## Naming Rules

Use lowercase filenames with hyphens:

```text
ubuntu-22-04-nvidia-driver-and-cuda.md
python-virtual-environments.md
postgresql-listen-notify.md
```

Avoid spaces, underscores, emojis, and mixed casing in filenames. Use clean titles inside the Markdown document.

## Documentation Ownership

The main Git repository is the source of truth.

The GitHub Wiki should only contain a short landing page that redirects readers to `docs/`.
