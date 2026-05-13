# TensorFlow GPU Validation

## Scope

This guide validates that TensorFlow can see and use the NVIDIA GPU.

## Prerequisites

- NVIDIA driver works.
- CUDA is installed.
- Python and pip are available.
- Optional: cuDNN installed.

## Recommended Setup

Create a virtual environment:

```bash
python3 -m venv .venv-tensorflow
source .venv-tensorflow/bin/activate
python -m pip install --upgrade pip
```

Install TensorFlow with CUDA extras where supported:

```bash
python -m pip install "tensorflow[and-cuda]"
```

## Validation Script

Use the script:

```text
scripts/gpu/test_tensorflow_gpu.py
```

Run:

```bash
python scripts/gpu/test_tensorflow_gpu.py
```

Expected result:

- `Is built with CUDA: True`
- At least one GPU listed.
- Matrix multiplication completes successfully.

## Benchmark Script

Use:

```text
scripts/gpu/tensorflow_gpu_benchmark.py
```

Run:

```bash
python scripts/gpu/tensorflow_gpu_benchmark.py --size 4096
```

## Common Warnings

TensorFlow may print warnings about cuDNN, cuFFT, cuBLAS, TensorRT, NUMA nodes, or CPU instruction optimization.

Not all warnings are fatal. Focus on:

- GPU visibility.
- Successful device creation.
- Successful GPU operation.

## Troubleshooting

### No GPU Detected

```bash
nvidia-smi
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

### Local Python Scripts Not on PATH

If pip installs command-line tools under `~/.local/bin`, add it to the PATH:

```bash
cat <<'EOF' >> ~/.bashrc

# User Python binaries
export PATH="$HOME/.local/bin:$PATH"
EOF

source ~/.bashrc
```
