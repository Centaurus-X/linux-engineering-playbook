# Documentation Home

This directory is the primary documentation source for the repository.

The former GitHub Wiki content has been reorganized into English Markdown files and grouped by engineering domain.

## Reading Order

For the original GPU/CUDA use case:

1. [Proxmox GPU Passthrough](20-proxmox-virtualization/proxmox-gpu-passthrough.md)
2. [NVIDIA Driver and CUDA on Ubuntu 22.04](10-linux-gpu-cuda/ubuntu-22-04-nvidia-driver-and-cuda.md)
3. [cuDNN on Ubuntu 22.04](10-linux-gpu-cuda/ubuntu-22-04-cudnn.md)
4. [TensorFlow GPU Validation](10-linux-gpu-cuda/tensorflow-gpu-validation.md)
5. [PyTorch GPU Validation](10-linux-gpu-cuda/pytorch-gpu-validation.md)

For Python environments:

1. [pip on Ubuntu 22.04](30-python-engineering/pip-on-ubuntu-22-04.md)
2. [Python Virtual Environments](30-python-engineering/python-virtual-environments.md)
3. [requirements.txt Workflow](30-python-engineering/requirements-txt-workflow.md)
4. [Multiple Python Versions on Ubuntu 22.04](30-python-engineering/multiple-python-versions-on-ubuntu-22-04.md)
5. [Python 3.13 Free-Threading on Ubuntu 24.04](30-python-engineering/python-313-free-threading-on-ubuntu-2404.md)

## Categories

| Category | Directory |
|---|---|
| Overview | [`00-overview/`](00-overview/) |
| Linux GPU CUDA | [`10-linux-gpu-cuda/`](10-linux-gpu-cuda/) |
| Proxmox Virtualization | [`20-proxmox-virtualization/`](20-proxmox-virtualization/) |
| Python Engineering | [`30-python-engineering/`](30-python-engineering/) |
| Linux Administration | [`40-linux-administration/`](40-linux-administration/) |
| Linux Services | [`50-linux-services/`](50-linux-services/) |
| Archive | [`90-archive/`](90-archive/) |

## Documentation Rules

Each operational guide should include:

- Scope
- Tested environment
- Prerequisites
- Installation or configuration steps
- Validation commands
- Troubleshooting notes
- Rollback or cleanup steps
- Security considerations when applicable
