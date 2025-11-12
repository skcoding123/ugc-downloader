@echo off
title YT Downloader - Server
color 0A

echo.
echo ========================================
echo    YT DOWNLOADER - STARTING...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from python.org
    pause
    exit
)

REM Check if required packages are installed
echo Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install flask flask-cors yt-dlp
)

echo.
echo Starting server...
echo.

REM Start the Python server
python server.py

pause