# Setup Automation Script for LLM Analysis Quiz
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LLM Analysis Quiz - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python version
Write-Host "[1/7] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.([9]|[1-9][0-9])") {
    Write-Host "OK Python version: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "ERROR Python 3.9+ required. Found: $pythonVersion" -ForegroundColor Red
    exit 1
}

# Step 2: Create virtual environment
Write-Host ""
Write-Host "[2/7] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "OK Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "OK Virtual environment created" -ForegroundColor Green
}

# Step 3: Activate virtual environment
Write-Host ""
Write-Host "[3/7] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "OK Virtual environment activated" -ForegroundColor Green

# Step 4: Install dependencies
Write-Host ""
Write-Host "[4/7] Installing Python packages (this may take a few minutes)..." -ForegroundColor Yellow
pip install -q -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "OK Python packages installed" -ForegroundColor Green
} else {
    Write-Host "ERROR Failed to install packages" -ForegroundColor Red
    exit 1
}

# Step 5: Install Playwright browsers
Write-Host ""
Write-Host "[5/7] Installing Playwright browsers (this may take a few minutes)..." -ForegroundColor Yellow
playwright install chromium
if ($LASTEXITCODE -eq 0) {
    Write-Host "OK Playwright chromium installed" -ForegroundColor Green
} else {
    Write-Host "ERROR Failed to install Playwright" -ForegroundColor Red
    exit 1
}

# Step 6: Create .env file
Write-Host ""
Write-Host "[6/7] Setting up environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "OK .env file already exists" -ForegroundColor Green
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "OK Created .env file from template" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: Edit .env file with your credentials!" -ForegroundColor Yellow
    Write-Host "  - OPENAI_API_KEY" -ForegroundColor Yellow
    Write-Host "  - SECRET_KEY" -ForegroundColor Yellow
    Write-Host "  - EMAIL" -ForegroundColor Yellow
    Write-Host ""
    $editNow = Read-Host "Open .env file now? (y/n)"
    if ($editNow -eq "y") {
        notepad .env
    }
}

# Step 7: Initialize Git
Write-Host ""
Write-Host "[7/7] Setting up Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "OK Git repository already initialized" -ForegroundColor Green
} else {
    git init
    git branch -M main
    Write-Host "OK Git repository initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your credentials" -ForegroundColor White
Write-Host "2. Run: python app.py" -ForegroundColor White
Write-Host "3. Test: curl http://localhost:8000/health" -ForegroundColor White
Write-Host "4. Read QUICKSTART.md for deployment" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
