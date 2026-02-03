#!/bin/bash

__dir="$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
cd ${__dir}/../.. || exit
source .venv/bin/activate
cd src || exit
gunicorn app:app -w ${WORKERS} -k uvicorn.workers.UvicornWorker \
--timeout "${TIMEOUT}" \
--forwarded-allow-ips "*" \
-b 0.0.0.0:"${PORT}"
