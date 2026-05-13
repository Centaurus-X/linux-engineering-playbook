# requirements.txt Workflow

## Scope

This guide explains how to create, use, and maintain `requirements.txt` files for Python projects.

## Basic Format

```text
numpy==1.26.4
pandas>=2.2
matplotlib
scipy
```

Common patterns:

| Pattern | Meaning |
|---|---|
| `package==1.2.3` | Install exactly this version |
| `package>=1.2.3` | Install this version or newer |
| `package` | Install the latest compatible version |

## Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Create requirements.txt from Current Environment

```bash
python -m pip freeze > requirements.txt
```

## Reproducible Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Automation Script

Use:

```text
scripts/python/install_requirements.py
```

Run:

```bash
python scripts/python/install_requirements.py --file requirements.txt
```

## Security Notes

> [!WARNING]
> Install dependencies only from trusted projects and trusted requirement files.
> A malicious dependency can execute code during installation.

Recommended checks:

```bash
python -m pip install --upgrade pip
python -m pip check
```

For production-grade dependency management, consider hash-pinned requirements or a lockfile workflow.
