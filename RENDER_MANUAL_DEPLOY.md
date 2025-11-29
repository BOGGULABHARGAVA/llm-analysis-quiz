# URGENT: Manual Render Redeploy Instructions

## Current Issue
The Render service is **still running the OLD build** from before commit `c9b90a4`. 
The browser installation fix has NOT been deployed yet.

## Error in Current Deployment
```
Executable doesn't exist at /opt/render/.cache/ms-playwright/chromium_headless_shell-1194/chrome-linux/headless_shell
```

This means the build command is still the OLD version without `--with-deps`.

## Solution: Force Manual Redeploy

### Step 1: Open Render Dashboard
1. Go to: https://dashboard.render.com
2. Login with your credentials
3. Find service: **llm-analysis-quiz**

### Step 2: Trigger Manual Deploy
**Option A: Clear Build Cache + Deploy**
1. Click on service `llm-analysis-quiz`
2. Go to **"Settings"** tab
3. Scroll down to **"Build & Deploy"** section
4. Click **"Clear build cache"** button
5. Go back to **"Events"** or **"Manual Deploy"** tab
6. Click **"Deploy latest commit"** or **"Manual Deploy"**
7. Select branch: `main`
8. Click **"Deploy"**

**Option B: Quick Manual Deploy**
1. Click on service `llm-analysis-quiz`
2. Click **"Manual Deploy"** button (top right)
3. Select branch: `main`
4. Click **"Deploy"**

### Step 3: Monitor Build Progress
Watch the build logs for these key indicators:

#### ✅ SUCCESS Indicators:
```
==> Cloning from https://github.com/BOGGULABHARGAVA/llm-analysis-quiz
==> Checking out commit c9b90a4...
==> Running build command 'pip install --upgrade pip && pip install --prefer-binary --no-cache-dir -r requirements.txt && playwright install --with-deps chromium'...
...
Installing Chromium 131.0.6812.1 (playwright build v1194)...
Chromium 131.0.6812.1 downloaded to /opt/render/.cache/ms-playwright/chromium_headless_shell-1194/chrome-linux/headless_shell
Installing system dependencies...
...
==> Build succeeded 😎
```

#### ❌ FAILURE Indicators:
```
==> Checking out commit 949d51b... (OLD COMMIT!)
==> Running build command 'pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && playwright install chromium && playwright install-deps chromium'...
(Note: Wrong command - missing --with-deps)
```

### Step 4: Verify Deployment
Once build shows **"Live"**, test the endpoint:

```powershell
# Test health
Invoke-WebRequest -Uri https://llm-analysis-quiz-z1m2.onrender.com/health -Method GET

# Test quiz (this should now work)
$body = @{
    email = "23f2003741@ds.study.iitm.ac.in"
    secret = "Bhargava123"
    quiz_url = "https://tds-llm-analysis.s-anand.net/demo"
} | ConvertTo-Json

Invoke-WebRequest -Uri https://llm-analysis-quiz-z1m2.onrender.com/quiz -Method POST -Body $body -ContentType "application/json"
```

## Why This Happened
Render uses **auto-deploy** but sometimes caches builds. The latest commit `c9b90a4` was pushed but Render might be:
1. Still building the previous commit
2. Using cached build environment
3. Waiting for manual trigger

## Expected Build Time
- **With cache clear:** 8-12 minutes
- **Normal deploy:** 5-8 minutes

## Verification Checklist
- [ ] Render dashboard shows commit `c9b90a4`
- [ ] Build logs show `playwright install --with-deps chromium`
- [ ] Build logs show "Chromium 131.0.6812.1 downloaded"
- [ ] Service status shows "Live" (green)
- [ ] Health endpoint returns 200 OK
- [ ] Quiz endpoint works without browser errors

## Alternative: Check Auto-Deploy Settings
If manual deploy doesn't work:
1. Go to service **Settings**
2. Check **"Auto-Deploy"** is set to **"Yes"**
3. Verify **"Branch"** is set to **"main"**
4. If disabled, enable it and save

## Current Commit Information
```
Latest: c9b90a4 - "Fix: Use 'playwright install --with-deps' and update to gpt-4o-mini model"
Fixed: Browser installation command
Updated: OpenAI model to gpt-4o-mini
Status: Pushed to GitHub ✓
Status: Deployed to Render? ✗ (needs manual trigger)
```

---

**ACTION REQUIRED:** Go to Render dashboard NOW and trigger manual deploy!
