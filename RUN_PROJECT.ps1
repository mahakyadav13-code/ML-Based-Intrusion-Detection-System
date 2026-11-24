# Complete Project Setup and Run Script
# ML-Based Intrusion Detection System

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "ML-BASED INTRUSION DETECTION SYSTEM" -ForegroundColor Cyan
Write-Host "Complete Setup and Execution" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[Step 1/8] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found!" -ForegroundColor Red
    Write-Host "  Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Create virtual environment if needed
Write-Host "[Step 2/8] Setting up virtual environment..." -ForegroundColor Yellow
if (!(Test-Path ".venv")) {
    Write-Host "  Creating virtual environment..." -ForegroundColor Cyan
    python -m venv .venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "  ✓ Virtual environment already exists" -ForegroundColor Green
}

Write-Host ""

# Activate virtual environment
Write-Host "[Step 3/8] Activating virtual environment..." -ForegroundColor Yellow
try {
    & .\.venv\Scripts\Activate.ps1
    Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "  Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Install dependencies
Write-Host "[Step 4/8] Installing dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ All dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  ✗ Some dependencies failed to install" -ForegroundColor Red
    Write-Host "  Check requirements.txt and try manual installation" -ForegroundColor Yellow
}

Write-Host ""

# Generate sample data
Write-Host "[Step 5/8] Generating sample data..." -ForegroundColor Yellow
if (!(Test-Path "data\sample\sample_network_traffic_SYNTHETIC.csv")) {
    Write-Host "  Generating synthetic network traffic data..." -ForegroundColor Cyan
    python scripts\generate_sample_data.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Sample data generated" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Sample data generation failed" -ForegroundColor Red
    }
} else {
    Write-Host "  ✓ Sample data already exists" -ForegroundColor Green
}

Write-Host ""

# Preprocess data
Write-Host "[Step 6/8] Preprocessing data..." -ForegroundColor Yellow
if (!(Test-Path "data\processed\train_data.csv")) {
    Write-Host "  Moving sample data to raw directory..." -ForegroundColor Cyan
    Copy-Item "data\sample\sample_network_traffic_SYNTHETIC.csv" "data\raw\" -Force
    
    Write-Host "  Running preprocessing pipeline..." -ForegroundColor Cyan
    python src\data_preprocessing.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Data preprocessed successfully" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Preprocessing failed" -ForegroundColor Red
    }
} else {
    Write-Host "  ✓ Preprocessed data already exists" -ForegroundColor Green
}

Write-Host ""

# Train models
Write-Host "[Step 7/8] Training models..." -ForegroundColor Yellow
if (!(Test-Path "models\random_forest_model.joblib")) {
    Write-Host "  Training ML models (this may take a minute)..." -ForegroundColor Cyan
    python src\train_model.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Models trained successfully" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Model training failed" -ForegroundColor Red
    }
} else {
    Write-Host "  ✓ Models already trained" -ForegroundColor Green
}

Write-Host ""

# Evaluate models
Write-Host "[Step 8/8] Evaluating models..." -ForegroundColor Yellow
if (!(Test-Path "reports\evaluation_report.json")) {
    Write-Host "  Running model evaluation..." -ForegroundColor Cyan
    python src\evaluate_model.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Models evaluated successfully" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Model evaluation failed" -ForegroundColor Red
    }
} else {
    Write-Host "  ✓ Evaluation results already exist" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

# Launch dashboard
Write-Host "Would you like to launch the Streamlit dashboard now? (Y/N)" -ForegroundColor Yellow
$response = Read-Host

if ($response -eq "Y" -or $response -eq "y") {
    Write-Host ""
    Write-Host "Launching Streamlit dashboard..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    streamlit run app.py
} else {
    Write-Host ""
    Write-Host "To launch the dashboard later, run:" -ForegroundColor Cyan
    Write-Host "  streamlit run app.py" -ForegroundColor White
    Write-Host ""
}
