#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
export TZ='America/New York'

# Install software-properties-common for add-apt-repository
apt-get update && apt-get upgrade -y
apt-get install -y software-properties-common

# Add deadsnakes PPA for Python 3.13
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update

# Install Python 3.13 and other dependencies
apt-get install -y \
    openssh-client \
    python3.13 \
    python3.13-dev \
    python3.13-venv \
    python3.13-distutils \
    git \
    postgresql \
    supervisor \
    g++ \
    gcc \
    locales

# Set Python 3.13 as the default python3
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1
update-alternatives --set python3 /usr/bin/python3.13
