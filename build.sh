#!/usr/bin/env bash

# Install system dependencies for dlib & OpenCV
apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev

# Install Python dependencies
pip install -r requirements.txt
