# Python 3.13 Free-Threading on Ubuntu 24.04

## Scope

This guide builds Python 3.13 with the experimental free-threading configuration on Ubuntu 24.04.

Free-threading means building CPython with the Global Interpreter Lock disabled.

> [!WARNING]
> Python free-threading is still an advanced and compatibility-sensitive runtime configuration.
> Use it for experiments, benchmarking, and selected workloads before considering production use.

## Prerequisites

```bash
sudo apt update
sudo apt install -y build-essential wget libssl-dev zlib1g-dev \
  libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
  libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev \
  tk-dev libffi-dev libgmp-dev
```

## 1. Download Python 3.13 Source

```bash
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz
sudo tar xzf Python-3.13.0.tgz
cd Python-3.13.0
```

## 2. Build Standard Python 3.13

```bash
sudo ./configure --enable-optimizations --with-lto --prefix=/opt/python3.13
sudo make -j"$(nproc)"
sudo make altinstall
```

Validate:

```bash
/opt/python3.13/bin/python3.13 --version
```

## 3. Build Python 3.13 with Free-Threading

Clean previous build output:

```bash
cd /usr/src/Python-3.13.0
sudo make clean
```

Configure with GIL disabled:

```bash
sudo ./configure --enable-optimizations --with-lto \
  --prefix=/opt/python3.13-free-threading \
  --disable-gil

sudo make -j"$(nproc)"
sudo make altinstall
```

Validate:

```bash
/opt/python3.13-free-threading/bin/python3.13 --version
```

## 4. Create a Virtual Environment

```bash
mkdir -p ~/python3.13-envs
cd ~/python3.13-envs

/opt/python3.13-free-threading/bin/python3.13 -m venv free-threading-env
source free-threading-env/bin/activate
```

## 5. Check Runtime Status

```bash
python -VV
python -c "import sys; print('GIL enabled:', sys._is_gil_enabled())"
```

Expected:

```text
GIL enabled: False
```

## 6. Run Benchmark Scripts

Use:

```text
scripts/python/free_threading_basic_test.py
scripts/python/free_threading_intensive_test.py
```

Run:

```bash
python -X gil=0 scripts/python/free_threading_basic_test.py
python -X gil=0 scripts/python/free_threading_intensive_test.py
```

## Interpretation

CPU-bound pure Python workloads may benefit from true parallel threads when the GIL is disabled.

However:

- Native extensions may not be ready for this runtime.
- Some dependencies may assume traditional GIL behavior.
- Multiprocessing remains a stable baseline for CPU-bound workloads.

## Rollback

```bash
sudo rm -rf /opt/python3.13-free-threading
rm -rf ~/python3.13-envs/free-threading-env
```

## References

- Python 3.13 documentation
- PEP 703: Making the Global Interpreter Lock Optional in CPython
