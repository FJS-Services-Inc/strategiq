#!/bin/bash

__dir="$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
cd ${__dir}/../../ || exit
source .venv/bin/activate
cd src || exit
# python -m backend.utils
gunicorn main:app -w ${WORKERS:-4} -k uvicorn.workers.UvicornWorker \
--timeout "${TIMEOUT:-120}" \
--forwarded-allow-ips "*" \
-b 0.0.0.0:"${PORT:-5051}"
