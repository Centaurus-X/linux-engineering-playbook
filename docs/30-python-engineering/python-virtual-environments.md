# Python Virtual Environments

## Scope

This guide creates and manages isolated Python virtual environments on Ubuntu Linux.

## Prerequisites

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv build-essential libssl-dev libffi-dev python3-dev
```

## Create a Virtual Environment

```bash
python3 -m venv .venv
```

## Activate the Environment

```bash
source .venv/bin/activate
```

Your shell prompt should now include `.venv`.

## Upgrade pip

```bash
python -m pip install --upgrade pip
```

## Install Packages

```bash
python -m pip install requests
```

## Freeze Dependencies

```bash
python -m pip freeze > requirements.txt
```

## Deactivate the Environment

```bash
deactivate
```

## Delete the Environment

```bash
rm -rf .venv
```

## Automation Script

Use:

```text
scripts/python/create_virtualenv.sh
```

Example:

```bash
scripts/python/create_virtualenv.sh .venv
source .venv/bin/activate
```

## Best Practices

- Keep virtual environments out of Git.
- Commit `requirements.txt` or a stronger lock file when reproducibility matters.
- Use `python -m pip` instead of bare `pip`.
- Name local environments `.venv`.
