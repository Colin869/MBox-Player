@echo off
title Mbox Player - Media Center
echo.
echo ========================================
echo    Mbox Player - Media Center
echo ========================================
echo.
echo Starting Mbox Player...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Try to run the launcher script
python run_mbox.py

REM If launcher script fails, try running main.py directly
if errorlevel 1 (
    echo.
    echo Trying to run main.py directly...
    python main.py
)

echo.
echo Mbox Player has closed.
pause
