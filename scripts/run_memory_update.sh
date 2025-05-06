#!/bin/bash

# Script to run the memory update with uv

# Change to the project directory
cd $(dirname "$0")/..

# Install required packages with uv
uv pip install httpx

# Run the memory update script
uv run scripts/update_memory.py