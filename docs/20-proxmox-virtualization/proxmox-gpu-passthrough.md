# Proxmox GPU Passthrough

## Scope

This guide describes the typical steps for passing an NVIDIA GPU through to a virtual machine on Proxmox VE.

## Tested Environment

| Component | Value |
|---|---|
| Hypervisor | Proxmox VE |
| Guest OS | Ubuntu Server or Desktop |
| Use Case | CUDA, GPU compute, graphics acceleration |

## Prerequisites

- CPU and mainboard support IOMMU.
- IOMMU enabled in BIOS/UEFI.
- A dedicated GPU for passthrough is recommended.
- Proxmox host shell access.
- VM uses OVMF/UEFI when required by the GPU.

## 1. Enable IOMMU in BIOS/UEFI

Enable one of:

- Intel VT-d
- AMD-Vi / IOMMU

## 2. Enable IOMMU in GRUB

Edit:

```bash
sudo nano /etc/default/grub
```

Intel:

```text
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt"
```

AMD:

```text
GRUB_CMDLINE_LINUX_DEFAULT="quiet amd_iommu=on iommu=pt"
```

Apply and reboot:

```bash
sudo update-grub
sudo reboot
```

## 3. Validate IOMMU

```bash
dmesg | grep -e DMAR -e IOMMU
find /sys/kernel/iommu_groups/ -type l
```

## 4. Identify GPU PCI IDs

```bash
lspci -nn | grep -Ei 'nvidia|vga|3d|audio'
```

You usually need to pass through both:

- GPU function
- HDMI/DisplayPort audio function

Example:

```text
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation ...
01:00.1 Audio device [0403]: NVIDIA Corporation ...
```

## 5. Bind GPU to VFIO

Create or edit:

```bash
sudo nano /etc/modprobe.d/vfio.conf
```

Example:

```text
options vfio-pci ids=10de:1c82,10de:0fb9
```

Replace the IDs with your actual GPU and audio IDs.

Load modules:

```bash
cat <<'EOF' | sudo tee /etc/modules
vfio
vfio_iommu_type1
vfio_pci
vfio_virqfd
EOF
```

Rebuild initramfs:

```bash
sudo update-initramfs -u -k all
sudo reboot
```

## 6. VM Configuration

Edit the VM configuration:

```bash
sudo nano /etc/pve/qemu-server/<VMID>.conf
```

Typical entries:

```text
machine: q35
bios: ovmf
hostpci0: 0000:01:00.0,pcie=1,x-vga=1
hostpci1: 0000:01:00.1,pcie=1
```

Use your real PCI addresses.

## 7. Guest Driver Installation

Inside the guest:

```bash
sudo apt update
ubuntu-drivers devices
sudo ubuntu-drivers autoinstall
sudo reboot
```

Validate:

```bash
nvidia-smi
```

## Troubleshooting

### Black Screen

Check:

- VM uses `q35`.
- VM uses OVMF/UEFI if needed.
- GPU audio function is passed through.
- No host driver binds to the GPU.
- The GPU is in a clean IOMMU group.

### `nvidia-smi` Fails in the Guest

Check:

```bash
lspci | grep -i nvidia
dmesg | grep -i nvidia
```

### Host Still Uses the GPU

Check host bindings:

```bash
lspci -nnk -s 01:00.0
```

Expected driver for passthrough device:

```text
Kernel driver in use: vfio-pci
```

## Rollback

Remove the `vfio-pci ids=...` entry, rebuild initramfs, and reboot:

```bash
sudo rm -f /etc/modprobe.d/vfio.conf
sudo update-initramfs -u -k all
sudo reboot
```
