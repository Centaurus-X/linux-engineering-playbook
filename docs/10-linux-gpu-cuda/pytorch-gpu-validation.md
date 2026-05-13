# PyTorch GPU Validation

## Scope

This guide validates that PyTorch can see and use the NVIDIA GPU.

## Prerequisites

- NVIDIA driver works.
- CUDA-compatible PyTorch build installed.
- Python and pip are available.

## Recommended Setup

```bash
python3 -m venv .venv-pytorch
source .venv-pytorch/bin/activate
python -m pip install --upgrade pip
python -m pip install torch
```

Depending on your CUDA version, you may need the PyTorch installation command from the official PyTorch selector.

## Validation Script

Use:

```text
scripts/gpu/test_pytorch_gpu.py
```

Run:

```bash
python scripts/gpu/test_pytorch_gpu.py
```

Expected result:

- `Is CUDA available: True`
- CUDA version is printed.
- Tensor operation completes on `cuda:0`.

## Troubleshooting

### CUDA Not Available

```bash
python -c "import torch; print(torch.cuda.is_available()); print(torch.version.cuda)"
nvidia-smi
```

If PyTorch was installed as a CPU-only build, reinstall the correct CUDA build.
