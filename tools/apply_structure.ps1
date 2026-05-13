$ErrorActionPreference = "Stop"

$directories = @(
    "docs/00-overview",
    "docs/10-linux-gpu-cuda",
    "docs/20-proxmox-virtualization",
    "docs/30-python-engineering",
    "docs/40-linux-administration",
    "docs/50-linux-services",
    "docs/90-archive",
    "scripts/gpu",
    "scripts/audio",
    "scripts/tor",
    "scripts/python",
    "tools",
    "wiki"
)

foreach ($directory in $directories) {
    New-Item -ItemType Directory -Force -Path $directory | Out-Null
}

Write-Host "Repository documentation structure created."
