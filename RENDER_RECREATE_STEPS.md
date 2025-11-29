# RENDER SERVICE RECREATION STEPS

## Problem
Render won't switch from Python runtime to Docker runtime on an existing service.
You MUST delete and recreate the service.

## Step-by-Step Instructions

### 1. Delete Current Service
1. Go to: https://dashboard.render.com
2. Find service: **llm-analysis-quiz**
3. Click on it
4. Go to **Settings** tab (bottom left)
5. Scroll to bottom → Click **"Delete Web Service"**
6. Type the service name to confirm
7. Click **"Delete"**

### 2. Create New Docker Service
1. Click **"New +"** → **"Web Service"**
2. Select **"Build and deploy from a Git repository"**
3. Click **"Connect"** next to your GitHub repo:
   - **Repository**: `BOGGULABHARGAVA/llm-analysis-quiz`
4. Fill in the form:
   - **Name**: `llm-analysis-quiz`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: It will AUTO-DETECT Docker from render.yaml ✓
   - **Instance Type**: Free

5. **Environment Variables** - Add these:
   ```
   OPENAI_API_KEY = <your-openai-api-key>
   SECRET_KEY = Bhargava123
   EMAIL = 23f2003741@ds.study.iitm.ac.in
   OPENAI_MODEL = gpt-4o-mini
   HEADLESS = True
   QUIZ_TIMEOUT = 170
   BROWSER_TIMEOUT = 30000
   ```

6. Click **"Create Web Service"**

### 3. Monitor Build
Watch the logs. You should see:

```
==> Building Docker image...
Step 1/10 : FROM python:3.13-slim
Step 2/10 : WORKDIR /app
Step 3/10 : RUN apt-get update && apt-get install -y...
✓ System dependencies installed
Step 4/10 : COPY requirements.txt .
Step 5/10 : RUN pip install...
✓ Python packages installed
Step 6/10 : RUN playwright install chromium
Downloading Chromium...
✓ Chromium installed at /root/.cache/ms-playwright/...
Step 7/10 : COPY . .
✓ Build succeeded
==> Deploying...
==> Your service is live 🎉
```

### 4. Test Deployment
Once live, run:

```powershell
cd "D:\TDS P2"
& "D:/TDS P2/venv/Scripts/python.exe" check_deployment.py
```

Or test manually:
```powershell
# Test health
Invoke-WebRequest -Uri https://llm-analysis-quiz-z1m2.onrender.com/health

# Test quiz
$body = @{
    email = "23f2003741@ds.study.iitm.ac.in"
    secret = "Bhargava123"
    url = "https://tds-llm-analysis.s-anand.net/demo"
} | ConvertTo-Json

Invoke-WebRequest -Uri https://llm-analysis-quiz-z1m2.onrender.com/quiz -Method POST -Body $body -ContentType "application/json"
```

## Expected Result
✅ Health endpoint returns 200
✅ Quiz endpoint successfully solves quiz
✅ No browser errors

## Your API Endpoint
**URL**: `https://llm-analysis-quiz-z1m2.onrender.com/quiz`
**Method**: POST
**Body**: 
```json
{
  "email": "23f2003741@ds.study.iitm.ac.in",
  "secret": "Bhargava123",
  "url": "<quiz-url>"
}
```

## Timeline
- Delete service: 1 minute
- Create service: 1 minute
- Docker build: 10-15 minutes
- Total: ~15-20 minutes

---

**ACTION REQUIRED NOW**: Delete the service and recreate it with Docker!
