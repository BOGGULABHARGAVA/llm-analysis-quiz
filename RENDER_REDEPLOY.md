# Force Render Redeploy - Fix OpenAI Error

## Problem
Render is using cached packages with old OpenAI version causing:
```
TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```

## Solution Applied
✅ Updated `requirements.txt`:
- Changed `openai==1.54.0` to `openai>=1.54.0`
- Added `httpx>=0.27.0` for compatibility
- Changed exact versions to `>=` for flexibility

✅ Updated `render.yaml`:
- Added `--no-cache-dir` flag to force fresh package install
- Added `pip install --upgrade pip` to ensure latest pip

## Steps to Force Redeploy on Render

### Option 1: Manual Deploy (Fastest - 2 minutes)

1. **Go to Render Dashboard:**
   ```
   https://dashboard.render.com
   ```

2. **Select your service:**
   - Click on `llm-analysis-quiz`

3. **Clear Build Cache:**
   - Click **Settings** (left sidebar)
   - Scroll down to **"Danger Zone"**
   - Click **"Clear build cache"**
   - Confirm

4. **Trigger Manual Deploy:**
   - Click **Manual Deploy** button (top right)
   - Select **"Deploy latest commit"**
   - Click **"Deploy"**

5. **Monitor the build:**
   - Click **"Logs"** tab
   - Watch for: `pip install --no-cache-dir -r requirements.txt`
   - Should see: `Successfully installed openai-1.54.0` (or higher)
   - Wait for: `Build successful` message
   - Service should restart automatically

### Option 2: Automatic (Slower - may take 5-10 min)

Render should automatically detect the push and redeploy. Just wait and monitor the Logs tab.

### Option 3: Force Push (If automatic fails)

```powershell
# Make a trivial change to force rebuild
echo "# Force rebuild" >> README.md
git add README.md
git commit -m "Force rebuild"
git push origin main
```

Then follow Option 1 steps 3-5.

## Verify the Fix

Once deployment completes (you'll see "Live" status):

### Test 1: Health Check
```powershell
curl https://llm-analysis-quiz-z1m2.onrender.com/health
```

Expected:
```json
{
  "status": "healthy",
  "openai_configured": true,
  "secret_configured": true
}
```

### Test 2: Quiz Endpoint
```powershell
curl -X POST https://llm-analysis-quiz-z1m2.onrender.com/quiz `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"23f2003741@ds.study.iitm.ac.in\",\"secret\":\"your-secret\",\"url\":\"https://tds-llm-analysis.s-anand.net/demo\"}'
```

Expected: Should NOT see the `proxies` error anymore.

## Check Logs for Success

In Render Logs, you should see:
```
Successfully installed openai-1.54.0 (or higher)
Successfully installed httpx-0.27.0 (or higher)
...
Build successful
...
[INFO] Starting Flask app on 0.0.0.0:10000
[INFO] Configuration validated successfully
```

## Troubleshooting

### If error persists after redeploy:

1. **Check installed version in logs:**
   Look for line: `Successfully installed openai-X.X.X`
   - Should be >= 1.54.0

2. **If old version still showing:**
   - Go to Settings → Danger Zone
   - Click "Clear build cache" again
   - Delete the service and recreate it (last resort)

3. **Environment variables:**
   Verify `OPENAI_API_KEY` is set correctly:
   - Go to Environment tab
   - Check that `OPENAI_API_KEY` has a value (sk-...)

### Common Issues:

**Issue:** "No module named 'openai'"
**Fix:** Build failed, check logs for errors

**Issue:** Still seeing old version
**Fix:** Clear build cache and redeploy

**Issue:** "Invalid API key"
**Fix:** Check OPENAI_API_KEY environment variable

## Timeline

- ⏱️ **Clear cache:** ~30 seconds
- ⏱️ **Build:** ~5-8 minutes (with playwright)
- ⏱️ **Deploy:** ~30 seconds
- ⏱️ **Total:** ~6-10 minutes

## Current Status

✅ Code pushed to GitHub: **ab75c64**
✅ Changes include:
  - requirements.txt with `openai>=1.54.0`
  - render.yaml with `--no-cache-dir`
  - Added `httpx>=0.27.0` dependency

⏳ **Waiting for:** Render to pick up changes and redeploy

---

**Next Step:** Go to Render dashboard and manually trigger deploy with cache clear!

**Last Updated:** November 29, 2025
