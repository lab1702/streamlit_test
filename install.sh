#!/bin/bash

# Remove existing virtual environment if it exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "Creating new virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install packages from requirements.txt
echo "Installing packages from requirements.txt..."
pip install -r requirements.txt

echo "Installation complete! To activate the virtual environment, run:"
echo "source venv/bin/activate"