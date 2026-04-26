# AI Title Generator - Uploader Runner Script
# This script ensures Ollama is running before launching the uploader

param(
    [switch]$NoOllama = $false
)

Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         YouTube AI Title Generator                ║" -ForegroundColor Cyan
Write-Host "║              Uploader Starting...                 ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ==================== Check/Start Ollama ====================
if (-not $NoOllama) {
    Write-Host "🔍 Checking if Ollama is running..." -ForegroundColor Yellow
    
    $ollamaProcess = Get-Process ollama -ErrorAction SilentlyContinue
    
    if ($ollamaProcess) {
        Write-Host "✓ Ollama is running" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Ollama is not running. Starting it now..." -ForegroundColor Yellow
        
        $ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
        
        if (Test-Path $ollamaPath) {
            try {
                Start-Process $ollamaPath -WindowStyle Minimized
                Write-Host "✓ Ollama started in background" -ForegroundColor Green
                Write-Host "  Waiting for Ollama to initialize (5 seconds)..." -ForegroundColor Cyan
                Start-Sleep -Seconds 5
            } catch {
                Write-Host "⚠️  Could not start Ollama: $_" -ForegroundColor Yellow
                Write-Host "  Continuing anyway, but AI features may not work" -ForegroundColor Yellow
            }
        } else {
            Write-Host "⚠️  Ollama not found. Run setup-aititle-gen.bat first." -ForegroundColor Red
            Write-Host ""
            Write-Host "To enable AI-powered titles and descriptions:" -ForegroundColor Yellow
            Write-Host "  1. Run: setup-aititle-gen.bat" -ForegroundColor White
            Write-Host "  2. Then run this script again" -ForegroundColor White
            Write-Host ""
            Write-Host "Continuing with template-based generation (no AI)..." -ForegroundColor Cyan
            Start-Sleep -Seconds 2
        }
    }
    Write-Host ""
}

# ==================== Launch Uploader ====================
Write-Host "🚀 Launching YouTube Uploader..." -ForegroundColor Green
Write-Host ""

# Find Python executable
$pythonExe = ".\.venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "✗ Virtual environment not found!" -ForegroundColor Red
    Write-Host "  Please run setup-aititle-gen.bat first" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Launch the uploader
try {
    & $pythonExe uploader.py
} catch {
    Write-Host "✗ Error running uploader: $_" -ForegroundColor Red
    pause
    exit 1
}
