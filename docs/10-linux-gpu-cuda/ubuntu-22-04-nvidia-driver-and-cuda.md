# NVIDIA Driver and CUDA on Ubuntu Server 22.04

## Scope

This guide installs and validates NVIDIA drivers and CUDA on Ubuntu Server 22.04.

It is especially useful for a Linux VM hosted under Proxmox with GPU passthrough.

## Tested Environment

| Component | Value |
|---|---|
| OS | Ubuntu Server 22.04 LTS |
| GPU | NVIDIA GPU |
| Virtualization | Proxmox VM or bare-metal Linux |
| Validation | `nvidia-smi`, `nvcc`, TensorFlow, PyTorch |

## Prerequisites

- Ubuntu Server 22.04 installed.
- NVIDIA GPU available to the system.
- For a VM: GPU passthrough already configured.
- `sudo` privileges.
- Secure Boot disabled or correctly configured for signed NVIDIA modules.

## 1. Update the System

```bash
sudo apt update
sudo apt upgrade -y
sudo reboot
```

## 2. Check Recommended NVIDIA Drivers

```bash
ubuntu-drivers devices
```

## 3. Install the Recommended Driver

Automatic installation:

```bash
sudo ubuntu-drivers autoinstall
sudo reboot
```

Manual installation, when you need a specific version:

```bash
sudo apt install -y nvidia-driver-XXX
sudo reboot
```

Replace `XXX` with the required driver branch.

## 4. Validate the Driver

```bash
nvidia-smi
```

Expected result:

- The GPU is listed.
- Driver version is visible.
- CUDA compatibility version is visible.
- No `No devices were found` error appears.

## 5. Optional: Blacklist Conflicting Drivers

Use this only when Nouveau or another conflicting driver interferes with NVIDIA.

```bash
sudo nano /etc/modprobe.d/blacklist-nouveau.conf
```

Add:

```text
blacklist nouveau
options nouveau modeset=0
```

If the host contains AMD GPU drivers that must not bind to this device, add a targeted blacklist only when required:

```text
blacklist radeon
```

Then rebuild initramfs and reboot:

```bash
sudo update-initramfs -u
sudo reboot
```

## 6. Install CUDA

Prefer the current NVIDIA repository method for your Ubuntu release.

For Ubuntu 22.04 x86_64:

```bash
cd /tmp
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install -y cuda
```

## 7. Configure Environment Variables

```bash
cat <<'EOF' >> ~/.bashrc

# CUDA
export PATH="/usr/local/cuda/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH:-}"
EOF

source ~/.bashrc
```

## 8. Validate CUDA

```bash
nvcc --version
```

Optional:

```bash
nvidia-smi
```

## 9. Fix CUDA Repository Key Problems

If repository keys are broken, refresh the keyring explicitly:

```bash
wget -O ~/cuda-repo-key.gpg https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub

sudo gpg --no-default-keyring \
  --keyring /usr/share/keyrings/cuda-repo-keyring.gpg \
  --import ~/cuda-repo-key.gpg

echo "deb [signed-by=/usr/share/keyrings/cuda-repo-keyring.gpg] http://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /" \
  | sudo tee /etc/apt/sources.list.d/cuda.list

sudo apt update
```

## 10. Python GPU Validation

Use the dedicated validation guides:

- [TensorFlow GPU Validation](tensorflow-gpu-validation.md)
- [PyTorch GPU Validation](pytorch-gpu-validation.md)

## Troubleshooting

### `nvidia-smi` does not show the GPU

Check:

```bash
lspci | grep -i nvidia
lsmod | grep nvidia
dmesg | grep -i nvidia
```

For Proxmox VMs, also check the passthrough configuration.

### Secure Boot Blocks the NVIDIA Driver

Either disable Secure Boot or configure module signing correctly.

### CUDA Toolkit Installs but `nvcc` Is Missing

Check:

```bash
ls -l /usr/local/cuda/bin/nvcc
echo "$PATH"
```

Add `/usr/local/cuda/bin` to your shell profile.

## Rollback

```bash
sudo apt purge -y 'nvidia-*' 'cuda-*'
sudo apt autoremove -y
sudo reboot
```
