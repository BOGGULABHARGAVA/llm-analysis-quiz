# Testing Guide

Comprehensive testing instructions for the LLM Analysis Quiz application.

## Table of Contents
1. [Local Testing](#local-testing)
2. [API Testing](#api-testing)
3. [Component Testing](#component-testing)
4. [Integration Testing](#integration-testing)
5. [Performance Testing](#performance-testing)
6. [Troubleshooting](#troubleshooting)

---

## Local Testing

### Setup

1. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Install Playwright browsers:**
   ```powershell
   playwright install chromium
   ```

3. **Create `.env` file:**
   ```powershell
   cp .env.example .env
   ```
   
   Edit `.env` with your credentials:
   ```
   OPENAI_API_KEY=sk-your-key-here
   SECRET_KEY=your-secret-string
   EMAIL=your@email.com
   ```

4. **Run the application:**
   ```powershell
   python app.py
   ```

   Expected output:
   ```
   INFO - Starting Flask app on 0.0.0.0:8000
   INFO - Browser initialized successfully
   * Running on http://0.0.0.0:8000
   ```

### Verify Installation

```powershell
# Test health endpoint
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "openai_configured": true,
  "secret_configured": true
}
```

---

## API Testing

### 1. Health Check

```powershell
curl http://localhost:8000/
```

Expected:
```json
{
  "status": "online",
  "service": "LLM Analysis Quiz Solver",
  "version": "1.0.0"
}
```

### 2. Invalid JSON Test

```powershell
curl -X POST http://localhost:8000/quiz `
  -H "Content-Type: application/json" `
  -d "invalid json"
```

Expected: `400 Bad Request`

### 3. Missing Fields Test

```powershell
curl -X POST http://localhost:8000/quiz `
  -H "Content-Type: application/json" `
  -d '{"email":"test@test.com"}'
```

Expected: `400` with error message about missing fields

### 4. Invalid Secret Test

```powershell
curl -X POST http://localhost:8000/quiz `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@test.com\",\"secret\":\"wrong\",\"url\":\"https://example.com\"}'
```

Expected: `403 Forbidden`

### 5. Valid Demo Request

```powershell
curl -X POST http://localhost:8000/quiz `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"your@email.com\",\"secret\":\"your-secret\",\"url\":\"https://tds-llm-analysis.s-anand.net/demo\"}'
```

Expected: `200` with success message

---

## Component Testing

### Test Browser Handler

Create `test_browser.py`:

```python
import asyncio
from browser_handler import render_quiz_page

async def test_browser():
    url = "https://example.com"
    html, text = await render_quiz_page(url)
    print(f"HTML length: {len(html)}")
    print(f"Text length: {len(text)}")
    print(f"Text preview: {text[:200]}")

asyncio.run(test_browser())
```

Run:
```powershell
python test_browser.py
```

### Test Data Processor

Create `test_data_processor.py`:

```python
from data_processor import DataProcessor

processor = DataProcessor()

# Test CSV download
csv_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
content = processor.download_file(csv_url)

if content:
    df = processor.read_csv(content)
    if df is not None:
        print(f"✓ CSV loaded: {df.shape}")
        analysis = processor.analyze_dataframe(df)
        print(f"✓ Analysis: {analysis['shape']}")
    else:
        print("✗ Failed to parse CSV")
else:
    print("✗ Failed to download")
```

Run:
```powershell
python test_data_processor.py
```

### Test Utilities

Create `test_utils.py`:

```python
from utils import *

# Test URL validation
assert is_valid_url("https://example.com") == True
assert is_valid_url("not a url") == False
print("✓ URL validation works")

# Test email validation
assert is_valid_email("test@example.com") == True
assert is_valid_email("invalid") == False
print("✓ Email validation works")

# Test base64 decoding
encoded = "SGVsbG8gV29ybGQ="  # "Hello World"
decoded = decode_base64(encoded)
assert decoded == "Hello World"
print("✓ Base64 decoding works")

# Test number extraction
text = "The answer is 12345"
num = extract_number(text)
assert num == 12345
print("✓ Number extraction works")

print("\n✓ All utility tests passed!")
```

Run:
```powershell
python test_utils.py
```

### Test Quiz Solver (without actual solving)

Create `test_quiz_solver.py`:

```python
import asyncio
from quiz_solver import QuizSolver

async def test_analysis():
    solver = QuizSolver()
    
    # Test manual extraction
    content = """
    Q123. Download the file from https://example.com/data.csv
    Submit your answer to https://example.com/submit
    """
    
    result = solver._manual_extract(content)
    print(f"Extracted URLs: {result}")
    print(f"✓ Manual extraction works")

asyncio.run(test_analysis())
```

Run:
```powershell
python test_quiz_solver.py
```

---

## Integration Testing

### Full Quiz Flow Test

```powershell
# Start the server
python app.py

# In another terminal, send request
curl -X POST http://localhost:8000/quiz `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"your@email.com\",\"secret\":\"your-secret\",\"url\":\"https://tds-llm-analysis.s-anand.net/demo\"}'
```

**Monitor the logs** for:
- ✓ Request received
- ✓ Browser initialized
- ✓ Page rendered
- ✓ LLM analysis completed
- ✓ File downloaded (if applicable)
- ✓ Answer submitted
- ✓ Response received

---

## Performance Testing

### Response Time Test

Create `test_performance.py`:

```python
import requests
import time

url = "http://localhost:8000/quiz"
payload = {
    "email": "your@email.com",
    "secret": "your-secret",
    "url": "https://tds-llm-analysis.s-anand.net/demo"
}

start = time.time()
response = requests.post(url, json=payload)
elapsed = time.time() - start

print(f"Status: {response.status_code}")
print(f"Time: {elapsed:.2f}s")
print(f"Response: {response.json()}")

# Should complete within 3 minutes
assert elapsed < 180, "Too slow!"
print("✓ Performance acceptable")
```

Run:
```powershell
python test_performance.py
```

### Load Test (Optional)

Using Apache Bench:
```powershell
# Install Apache Bench first
# Then run:
ab -n 10 -c 2 -p request.json -T application/json http://localhost:8000/quiz
```

Where `request.json`:
```json
{"email":"test@test.com","secret":"your-secret","url":"https://tds-llm-analysis.s-anand.net/demo"}
```

---

## Production Testing (After Deployment)

### Test Deployed Endpoint

Replace `localhost:8000` with your Render URL:

```powershell
$url = "https://llm-analysis-quiz.onrender.com"

# Health check
curl "$url/health"

# Quiz test
curl -X POST "$url/quiz" `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"your@email.com\",\"secret\":\"your-secret\",\"url\":\"https://tds-llm-analysis.s-anand.net/demo\"}'
```

### Monitor Render Logs

1. Go to Render dashboard
2. Select your service
3. Click "Logs" tab
4. Watch real-time logs during testing

---

## Troubleshooting

### Issue: Browser fails to start

**Symptoms:**
- Error: "Executable doesn't exist"
- Browser timeout errors

**Solutions:**
```powershell
# Reinstall Playwright
playwright install chromium

# Install system dependencies (Windows)
# Usually not needed on Windows

# Check if chromium installed
playwright --version
```

### Issue: OpenAI API errors

**Symptoms:**
- "Invalid API key"
- "Rate limit exceeded"

**Solutions:**
```powershell
# Verify API key
echo $env:OPENAI_API_KEY

# Check OpenAI status
curl https://status.openai.com/

# Test API key directly
curl https://api.openai.com/v1/models `
  -H "Authorization: Bearer $env:OPENAI_API_KEY"
```

### Issue: Import errors

**Symptoms:**
- "ModuleNotFoundError"

**Solutions:**
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check installed packages
pip list

# Verify Python version
python --version  # Should be 3.9+
```

### Issue: Timeout errors

**Symptoms:**
- Quiz not completing in time
- "Timeout" in logs

**Solutions:**
1. Increase `QUIZ_TIMEOUT` in config
2. Optimize LLM prompts
3. Check network speed
4. Verify OpenAI API response time

### Issue: JSON parsing errors

**Symptoms:**
- "Failed to parse JSON"
- "Invalid JSON response from LLM"

**Solutions:**
1. Check LLM response in logs
2. Adjust prompt for better JSON formatting
3. Add fallback parsing logic
4. Retry with different prompt

---

## Automated Testing Script

Create `run_tests.py`:

```python
import subprocess
import sys

tests = [
    ("Health Check", "curl http://localhost:8000/health"),
    ("Browser Test", "python test_browser.py"),
    ("Data Processor Test", "python test_data_processor.py"),
    ("Utils Test", "python test_utils.py"),
]

print("Running automated tests...\n")

failed = []
for name, command in tests:
    print(f"Running: {name}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, timeout=60)
        if result.returncode == 0:
            print(f"✓ {name} passed\n")
        else:
            print(f"✗ {name} failed")
            print(result.stderr.decode())
            failed.append(name)
    except Exception as e:
        print(f"✗ {name} error: {e}\n")
        failed.append(name)

print("\n" + "="*50)
if not failed:
    print("✓ All tests passed!")
    sys.exit(0)
else:
    print(f"✗ {len(failed)} test(s) failed:")
    for name in failed:
        print(f"  - {name}")
    sys.exit(1)
```

Run:
```powershell
python run_tests.py
```

---

## Pre-Deployment Checklist

Before submitting to the Google Form:

- [ ] All local tests pass
- [ ] Browser rendering works
- [ ] LLM integration works
- [ ] File downloads work
- [ ] Demo quiz completes successfully
- [ ] Environment variables set in Render
- [ ] Deployment successful on Render
- [ ] Production endpoint responds
- [ ] Logs show no errors
- [ ] GitHub repo is public
- [ ] MIT LICENSE added
- [ ] README is comprehensive

---

**Last Updated:** November 28, 2025
