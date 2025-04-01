#!/usr/bin/env bash

# Install required dependencies
apt-get update && apt-get install -y \
    cmake build-essential \
    libopenblas-dev liblapack-dev libx11-dev \
    libgtk-3-dev python3-dev

# Upgrade pip
pip install --upgrade pip 

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt
