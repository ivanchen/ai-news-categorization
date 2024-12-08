#!/bin/bash

# Remove old venv if exists
rm -rf venv

# Create new venv
python -m venv venv

# Activate venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt 