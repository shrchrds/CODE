#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- Building backend ---"
pip install -r backend/requirements.txt