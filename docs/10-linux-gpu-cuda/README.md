# Linux GPU CUDA

This category preserves and extends the original `Linux_GPU_CUDA` repository scope.

It covers NVIDIA driver installation, CUDA, cuDNN, and Python GPU validation on Ubuntu systems, especially when running inside a VM hosted on Proxmox.

## Guides

- [NVIDIA Driver and CUDA on Ubuntu 22.04](ubuntu-22-04-nvidia-driver-and-cuda.md)
- [cuDNN on Ubuntu 22.04](ubuntu-22-04-cudnn.md)
- [TensorFlow GPU Validation](tensorflow-gpu-validation.md)
- [PyTorch GPU Validation](pytorch-gpu-validation.md)

## Typical Workflow

1. Configure GPU passthrough in Proxmox.
2. Boot the Ubuntu VM.
3. Disable Secure Boot if required by your driver setup.
4. Install the NVIDIA driver.
5. Validate with `nvidia-smi`.
6. Install CUDA.
7. Validate with `nvcc --version`.
8. Install cuDNN if required.
9. Validate with TensorFlow or PyTorch.
