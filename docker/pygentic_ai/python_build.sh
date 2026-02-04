#!/bin/bash

curl -LsSf https://astral.sh/uv/install.sh | sh
PATH="/root/.local/bin/:$PATH"
cd /opt/pygentic_ai || exit

# Verify Python version
python3 --version

# Create venv with Python 3.13
uv venv .venv --python python3.13
source .venv/bin/activate

# Verify venv Python version
python --version

for FILE in core_requirements dev_requirements
do
	uv pip compile --upgrade $FILE.in -o $FILE.txt
done
uv pip sync core_requirements.txt
