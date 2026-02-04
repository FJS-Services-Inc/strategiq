#!/bin/bash

curl -LsSf https://astral.sh/uv/install.sh | sh
PATH="/root/.local/bin/:$PATH"
cd /opt/pygentic_ai || exit

# Verify Python version
python3 --version

# Install dependencies from pyproject.toml
# Creates venv automatically if it doesn't exist
uv sync --no-dev

# Activate venv
source .venv/bin/activate

# Verify venv Python version
python --version
