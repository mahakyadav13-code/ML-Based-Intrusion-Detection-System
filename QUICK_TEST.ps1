# Quick Test Script - Generate sample data and launch dashboard
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "QUICK TEST - ML-Based IDS" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# Activate environment
Write-Host "`n[1/4] Activating environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Generate sample data
Write-Host "`n[2/4] Generating sample data..." -ForegroundColor Yellow
python scripts\generate_sample_data.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Failed to generate data" -ForegroundColor Red
    exit 1
}

# Copy to raw for preprocessing
Write-Host "`n[3/4] Preparing for preprocessing..." -ForegroundColor Yellow
Copy-Item "data\sample\sample_network_traffic_SYNTHETIC.csv" "data\raw\" -Force

# Launch dashboard
Write-Host "`n[4/4] Launching Streamlit dashboard..." -ForegroundColor Green
Write-Host "  Opening http://localhost:8501" -ForegroundColor Cyan
Write-Host "  Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py
