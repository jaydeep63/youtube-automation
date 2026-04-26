@echo off
REM AI Title Generator Setup - Batch Launcher
REM This file makes it easy for non-technical users to run the setup

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   AI Title Generator for YouTube Uploader         ║
echo ║              Setup Starting...                     ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Check if PowerShell can run scripts
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '%~dp0setup-aititle-gen.ps1'"

if errorlevel 1 (
    echo.
    echo ✗ Setup encountered an error. Please check the output above.
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo Setup completed successfully!
    echo.
    pause
    exit /b 0
)
