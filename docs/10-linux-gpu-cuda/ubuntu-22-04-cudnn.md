# NVIDIA cuDNN on Ubuntu Server 22.04

## Scope

This guide installs NVIDIA cuDNN on Ubuntu Server 22.04 after the NVIDIA driver and CUDA are already working.

## Prerequisites

- Ubuntu Server 22.04.
- NVIDIA driver installed and validated with `nvidia-smi`.
- CUDA installed and validated with `nvcc --version`.
- `sudo` privileges.

## 1. Install the NVIDIA CUDA Repository Keyring

```bash
cd /tmp
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
```

## 2. Install cuDNN

Generic cuDNN package:

```bash
sudo apt install -y cudnn
```

For CUDA 12-specific packages:

```bash
sudo apt install -y cudnn-cuda-12
```

For CUDA 11-specific packages:

```bash
sudo apt install -y cudnn-cuda-11
```

## 3. Configure Runtime Library Paths

```bash
cat <<'EOF' >> ~/.bashrc

# CUDA/cuDNN
export CUDA_HOME="/usr/local/cuda"
export LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH:-}"
EOF

source ~/.bashrc
```

## 4. Validate Installation

Check installed packages:

```bash
dpkg -l | grep -i cudnn
```

Check CUDA library path:

```bash
ls -la /usr/local/cuda/lib64 | grep -i cudnn || true
```

Run framework-level tests:

- [TensorFlow GPU Validation](tensorflow-gpu-validation.md)
- [PyTorch GPU Validation](pytorch-gpu-validation.md)

## Troubleshooting

### Repository Key Error

```bash
wget -O ~/cuda-repo-key.gpg https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub

sudo gpg --no-default-keyring \
  --keyring /usr/share/keyrings/cuda-repo-keyring.gpg \
  --import ~/cuda-repo-key.gpg

echo "deb [signed-by=/usr/share/keyrings/cuda-repo-keyring.gpg] http://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /" \
  | sudo tee /etc/apt/sources.list.d/cuda.list

sudo apt update
```

### TensorFlow Finds CUDA but Not cuDNN

Check:

```bash
python3 -m pip show tensorflow
echo "$LD_LIBRARY_PATH"
dpkg -l | grep -E 'cuda|cudnn'
```

Framework binaries often require specific CUDA/cuDNN compatibility. Match the framework version to the installed CUDA/cuDNN version.
