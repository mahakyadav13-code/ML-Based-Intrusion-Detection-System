# Launch Professional Flask IDS Dashboard
# ML-Based Intrusion Detection System

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "ML-BASED INTRUSION DETECTION SYSTEM" -ForegroundColor Cyan
Write-Host "Professional Flask Dashboard" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/3] Checking environment..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Activate virtual environment
Write-Host "[2/3] Activating virtual environment..." -ForegroundColor Yellow
try {
    & .\.venv\Scripts\Activate.ps1
    Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Launch Flask
Write-Host "[3/3] Launching Flask application..." -ForegroundColor Green
Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "Dashboard is starting..." -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Access the dashboard at:" -ForegroundColor Yellow
Write-Host "   Local:   http://localhost:5000" -ForegroundColor White
Write-Host "   Network: http://192.168.29.51:5000" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python flask_app.py
