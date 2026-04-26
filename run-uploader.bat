@echo off
REM YouTube AI Title Generator - Uploader Launcher
REM Double-click this to run the uploader. Ollama will auto-start if needed.

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║         YouTube AI Title Generator                ║
echo ║              Loading Uploader...                  ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Check if PowerShell can run scripts
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '%~dp0run-uploader.ps1'"

if errorlevel 1 (
    echo.
    echo ✗ Uploader encountered an error.
    echo.
    pause
    exit /b 1
) else (
    exit /b 0
)
