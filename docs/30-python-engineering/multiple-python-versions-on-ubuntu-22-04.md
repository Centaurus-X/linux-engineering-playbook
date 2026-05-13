# Multiple Python Versions on Ubuntu 22.04

## Scope

This guide explains how to install and manage multiple Python versions on Ubuntu 22.04 without breaking the system Python.

> [!WARNING]
> Do not replace `/usr/bin/python3` on Ubuntu systems unless you fully understand the consequences.
> Many system tools depend on the distribution-provided Python version.

## Recommended Strategy

Prefer side-by-side installations under `/opt`:

```text
/opt/python3.11/
/opt/python3.12/
/opt/python3.13/
```

Use explicit interpreter paths:

```bash
/opt/python3.12/bin/python3.12 -m venv .venv
```

## Build Dependencies

```bash
sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
  libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget \
  libbz2-dev liblzma-dev tk-dev
```

## Compile Python from Source

Example for Python 3.12.x:

```bash
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
sudo tar xzf Python-3.12.0.tgz
cd Python-3.12.0

sudo ./configure --enable-optimizations --with-lto --prefix=/opt/python3.12
sudo make -j"$(nproc)"
sudo make altinstall
```

Validate:

```bash
/opt/python3.12/bin/python3.12 --version
```

## Create a Project Environment

```bash
/opt/python3.12/bin/python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## Optional: update-alternatives

Use this only on lab systems.

```bash
sudo update-alternatives --install /usr/local/bin/python-local python-local /opt/python3.12/bin/python3.12 12
sudo update-alternatives --config python-local
```

Then call:

```bash
python-local --version
```

This avoids modifying the distribution `python3`.

## Validate pip for Each Version

```bash
/opt/python3.12/bin/python3.12 -m pip --version
/opt/python3.12/bin/python3.12 -m pip install --upgrade pip
```

## Rollback

Remove the custom installation directory:

```bash
sudo rm -rf /opt/python3.12
```
