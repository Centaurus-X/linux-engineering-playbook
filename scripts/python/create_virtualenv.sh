#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="${1:-.venv}"

python3 -m venv "$ENV_NAME"
"$ENV_NAME/bin/python" -m pip install --upgrade pip

echo "Created virtual environment: $ENV_NAME"
echo "Activate it with:"
echo "source $ENV_NAME/bin/activate"
