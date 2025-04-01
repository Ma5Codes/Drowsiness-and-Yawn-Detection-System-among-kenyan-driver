#!/usr/bin/env bash

# Update package list
apt-get update

# Install dependencies for dlib
apt-get install -y cmake build-essential \
    libopenblas-dev liblapack-dev libx11-dev \
    libgtk-3-dev python3-dev python3-pip

# Upgrade pip
pip install --upgrade pip 

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt
pip install dlib-bin
pip install gunicorn
pip install Django


