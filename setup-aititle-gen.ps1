# AI Title Generator Setup Script for YouTube Uploader
# This script automates the installation of Ollama, Mistral model, and Python dependencies

param(
    [switch]$SkipOllama = $false
)

Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     AI Title Generator - Installation Setup       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]"Administrator")
if (-not $isAdmin) {
    Write-Host "⚠️  This script should be run as Administrator for best results." -ForegroundColor Yellow
    Write-Host "   Continuing anyway, but some operations may fail..." -ForegroundColor Yellow
    Write-Host ""
    Start-Sleep -Seconds 2
}

# ==================== STEP 1: Check/Install Ollama ====================
Write-Host "📦 STEP 1: Checking Ollama Installation..." -ForegroundColor Yellow

$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
$ollamaInstalled = Test-Path $ollamaPath

if ($ollamaInstalled) {
    Write-Host "✓ Ollama is already installed at: $ollamaPath" -ForegroundColor Green
} else {
    Write-Host "✗ Ollama not found. Installing..." -ForegroundColor Yellow
    
    $ollamaUrl = "https://ollama.ai/download/OllamaSetup.exe"
    $ollamaInstaller = "$env:TEMP\OllamaSetup.exe"
    
    Write-Host "  Downloading Ollama installer (~200MB)..." -ForegroundColor Cyan
    try {
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $ollamaUrl -OutFile $ollamaInstaller -TimeoutSec 300
        $ProgressPreference = 'Continue'
        Write-Host "  ✓ Download complete" -ForegroundColor Green
        
        Write-Host "  Installing Ollama (this may take a minute)..." -ForegroundColor Cyan
        & $ollamaInstaller /install /quiet /norestart
        Start-Sleep -Seconds 5
        
        # Verify installation
        if (Test-Path $ollamaPath) {
            Write-Host "✓ Ollama installed successfully!" -ForegroundColor Green
        } else {
            Write-Host "✗ Ollama installation failed. Please install manually from https://ollama.ai" -ForegroundColor Red
            Write-Host ""
            exit 1
        }
        
        # Cleanup installer
        Remove-Item $ollamaInstaller -Force -ErrorAction SilentlyContinue
    } catch {
        Write-Host "✗ Failed to download Ollama: $_" -ForegroundColor Red
        Write-Host "  Please download manually from: https://ollama.ai" -ForegroundColor Yellow
        exit 1
    }
}

# ==================== STEP 2: Start Ollama Service ====================
Write-Host ""
Write-Host "🚀 STEP 2: Starting Ollama Service..." -ForegroundColor Yellow

try {
    # Check if Ollama process is already running
    $ollamaProcess = Get-Process ollama -ErrorAction SilentlyContinue
    
    if ($ollamaProcess) {
        Write-Host "✓ Ollama is already running" -ForegroundColor Green
    } else {
        Write-Host "  Starting Ollama in background..." -ForegroundColor Cyan
        Start-Process $ollamaPath -WindowStyle Minimized
        Write-Host "  Waiting for Ollama to start (this takes ~5 seconds)..." -ForegroundColor Cyan
        Start-Sleep -Seconds 5
        
        # Verify it's running
        $ollamaProcess = Get-Process ollama -ErrorAction SilentlyContinue
        if ($ollamaProcess) {
            Write-Host "✓ Ollama started successfully" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Could not verify Ollama is running. It may still be starting..." -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "⚠️  Could not start Ollama: $_" -ForegroundColor Yellow
}

# ==================== STEP 3: Pull Mistral Model ====================
Write-Host ""
Write-Host "📥 STEP 3: Pulling Mistral AI Model..." -ForegroundColor Yellow

# Wait a bit more to ensure Ollama is ready
Start-Sleep -Seconds 3

Write-Host "  Checking if Mistral model is available..." -ForegroundColor Cyan
try {
    $tagResponse = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 5 -ErrorAction SilentlyContinue
    $mistralExists = $tagResponse.models | Where-Object { $_.name -like "mistral*" }
    
    if ($mistralExists) {
        Write-Host "✓ Mistral model is already downloaded" -ForegroundColor Green
    } else {
        Write-Host "  Downloading Mistral model (this may take 5-15 minutes, ~4GB)..." -ForegroundColor Cyan
        Write-Host "  Please be patient..." -ForegroundColor Cyan
        
        & $ollamaPath pull mistral
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Mistral model downloaded successfully!" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Mistral download may not have completed. You can run 'ollama pull mistral' manually." -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "⚠️  Could not verify model: $_" -ForegroundColor Yellow
    Write-Host "  You can run 'ollama pull mistral' manually in a terminal" -ForegroundColor Yellow
}

# ==================== STEP 4: Install Python Dependencies ====================
Write-Host ""
Write-Host "🐍 STEP 4: Installing Python Dependencies..." -ForegroundColor Yellow

# Find Python executable
$pythonExe = ".\.venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "✗ Virtual environment not found at $pythonExe" -ForegroundColor Red
    Write-Host "  Creating virtual environment..." -ForegroundColor Cyan
    
    python -m venv .venv
    
    if (-not (Test-Path $pythonExe)) {
        Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        Write-Host "  Please ensure Python 3.7+ is installed and in PATH" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "  Installing packages from requirements.txt..." -ForegroundColor Cyan
& $pythonExe -m pip install --upgrade pip --quiet
& $pythonExe -m pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# ==================== COMPLETION ====================
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║          ✓ Setup Complete!                        ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "You're all set! Here's what was installed:" -ForegroundColor Cyan
Write-Host "  ✓ Ollama - Local AI engine" -ForegroundColor Green
Write-Host "  ✓ Mistral - AI model for text generation" -ForegroundColor Green
Write-Host "  ✓ Python dependencies - Required packages" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Keep Ollama running in the background" -ForegroundColor White
Write-Host "  2. Run the uploader: python uploader.py" -ForegroundColor White
Write-Host "  3. Enjoy AI-generated titles and descriptions!" -ForegroundColor White
Write-Host ""
Write-Host "📝 Note: Make sure 'use_ollama' is set to true in config.json" -ForegroundColor Cyan
Write-Host ""
