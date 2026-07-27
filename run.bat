@echo off
title VidaiBot Pro - YouTube View Booster

echo ========================================
echo  🎬 VidaiBot Pro v2.0.0
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%I in ('python --version 2^>^&1') do set pyver=%%I
echo [INFO] Python Version: %pyver%

REM Install requirements
echo [INFO] Installing required packages...
echo.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install requirements.
    echo.
    pause
    exit /b 1
)

echo.
echo [INFO] Starting VidaiBot Pro...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application crashed.
    echo Check the error message above.
    echo.
)

echo.
echo Press any key to exit...
pause >nul