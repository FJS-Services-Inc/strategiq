#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
export TZ='America/New York'

apt-get update && apt-get upgrade -y
apt-get install openssh-client \
    python3-dev \
    python3-full \
    python3-venv \
    python3-pip \
    git \
    postgresql \
    supervisor \
    g++ \
    gcc \
    locales -y
