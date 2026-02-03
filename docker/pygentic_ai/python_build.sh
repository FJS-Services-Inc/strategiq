#!/bin/bash

curl -LsSf https://astral.sh/uv/install.sh | sh
PATH="/root/.local/bin/:$PATH"
cd /opt/pygentic_ai || exit
uv venv .venv
source .venv/bin/activate
for FILE in core_requirements dev_requirements
do
	uv pip compile --upgrade $FILE.in -o $FILE.txt
done
uv pip sync core_requirements.txt
