#!/bin/bash

echo "========================================"
echo " 🎬 VidaiBot Pro v2.0.0"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH."
    echo ""
    echo "Please install Python 3.7 or higher from:"
    echo "https://www.python.org/downloads/"
    echo ""
    exit 1
fi

# Check Python version
pyver=$(python3 --version 2>&1 | awk '{print $2}')
echo "[INFO] Python Version: $pyver"

# Install requirements
echo "[INFO] Installing required packages..."
echo ""
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to install requirements."
    echo ""
    exit 1
fi

echo ""
echo "[INFO] Starting VidaiBot Pro..."
echo ""
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Application crashed."
    echo "Check the error message above."
    echo ""
fi

echo ""
read -p "Press Enter to exit..."