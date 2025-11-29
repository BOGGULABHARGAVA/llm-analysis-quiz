# Deployment Guide for Render.com

This guide provides step-by-step instructions for deploying the LLM Analysis Quiz application on Render.com.

## Prerequisites

1. **GitHub Account** with the code pushed to your repository
2. **Render.com Account** (free tier available)
3. **OpenAI API Key** with credits
4. **Your secret string** and **email address** for the quiz

## Step-by-Step Deployment

### 1. Prepare Your GitHub Repository

First, push your code to GitHub:

```bash
cd "d:\TDS P2"
git init
git add .
git commit -m "Initial commit - LLM Analysis Quiz Project"
git branch -M main
git remote add origin https://github.com/BOGGULABHARGAVA/llm-analysis-quiz.git
git push -u origin main
```

Make sure your repository is **public** (required for evaluation).

### 2. Sign Up / Log In to Render.com

1. Go to [https://render.com](https://render.com)
2. Click "Get Started" or "Sign In"
3. Sign up with your GitHub account (recommended for easy integration)

### 3. Create a New Web Service

1. From your Render dashboard, click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub account if not already connected
4. Find and select your repository: `BOGGULABHARGAVA/llm-analysis-quiz`

### 4. Configure the Web Service

Fill in the configuration:

#### Basic Settings
- **Name:** `llm-analysis-quiz` (or your preferred name)
- **Region:** Choose closest to you (e.g., Oregon USA, Frankfurt EU, Singapore)
- **Branch:** `main`
- **Root Directory:** Leave empty (or `.` if needed)

#### Build Settings
- **Runtime:** `Python 3`
- **Build Command:**
  ```bash
  pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
  ```

#### Start Settings
- **Start Command:**
  ```bash
  gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 180 app:app
  ```

#### Instance Type
- **Free** tier is sufficient for testing
- **Starter** ($7/month) recommended for production (better performance, no sleep)

### 5. Add Environment Variables

Click on **"Environment"** tab and add these variables:

| Key | Value | Notes |
|-----|-------|-------|
| `OPENAI_API_KEY` | `sk-...` | Your OpenAI API key |
| `SECRET_KEY` | `your_secret` | Your chosen secret string |
| `EMAIL` | `your@email.com` | Your email address |
| `OPENAI_MODEL` | `gpt-4-turbo-preview` | Model to use |
| `HEADLESS` | `True` | Browser mode |
| `QUIZ_TIMEOUT` | `170` | Timeout in seconds |
| `BROWSER_TIMEOUT` | `30000` | Browser timeout (ms) |
| `PORT` | `10000` | Render's default port |

**Important:** Mark `OPENAI_API_KEY` and `SECRET_KEY` as sensitive (click the 🔒 icon).

### 6. Deploy

1. Click **"Create Web Service"** at the bottom
2. Render will start building your application
3. Wait for the build to complete (5-10 minutes first time)
4. Monitor the logs for any errors

### 7. Verify Deployment

Once deployed, your service will be available at:
```
https://llm-analysis-quiz.onrender.com
```

Test the health endpoint:
```bash
curl https://llm-analysis-quiz.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "openai_configured": true,
  "secret_configured": true
}
```

### 8. Test the Quiz Endpoint

Test with the demo quiz:

```bash
curl -X POST https://llm-analysis-quiz.onrender.com/quiz \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "secret": "your_secret",
    "url": "https://tds-llm-analysis.s-anand.net/demo"
  }'
```

## Troubleshooting

### Build Fails

**Issue:** Playwright installation fails

**Solution:** Make sure the build command includes:
```bash
playwright install chromium && playwright install-deps chromium
```

### Application Crashes

**Issue:** Out of memory error

**Solution:** 
1. Upgrade to Starter plan (more RAM)
2. Reduce workers in start command: `--workers 1`

### Timeouts

**Issue:** Request timeout errors

**Solution:**
1. Increase timeout in start command: `--timeout 300`
2. Check if OpenAI API is responding slowly

### Environment Variables Not Working

**Issue:** Config errors on startup

**Solution:**
1. Verify all required env vars are set
2. Check for typos in variable names
3. Redeploy after adding/changing variables

### Browser Not Starting

**Issue:** Playwright browser fails to launch

**Solution:**
1. Check logs for missing dependencies
2. Verify build command installed chromium
3. Make sure `HEADLESS=True` is set

## Monitoring

### View Logs

1. Go to your service in Render dashboard
2. Click **"Logs"** tab
3. Monitor real-time logs during quiz solving

### Check Metrics

1. Click **"Metrics"** tab
2. View CPU, Memory, and Request metrics
3. Monitor for issues

### Set Up Alerts

1. Click **"Settings"** → **"Alerts"**
2. Add email notifications for:
   - Service health checks
   - Build failures
   - High memory usage

## Scaling

### Horizontal Scaling
- Increase number of instances in Settings
- Requires Starter plan or higher

### Vertical Scaling
- Upgrade instance type (Standard, Pro)
- More CPU and RAM

## Cost Optimization

### Free Tier
- Services sleep after 15 minutes of inactivity
- 750 hours/month free
- Slower cold starts

### Starter Tier ($7/month)
- Always on (no sleep)
- Faster performance
- Custom domains
- Better for production

## Custom Domain (Optional)

1. Go to **"Settings"** → **"Custom Domains"**
2. Click **"Add Custom Domain"**
3. Enter your domain name
4. Follow DNS configuration instructions

## Automatic Deploys

Render automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render will detect the push and redeploy automatically.

## Manual Deploy

To manually trigger a deploy:

1. Go to your service in dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

## Rollback

To rollback to a previous version:

1. Click **"Deploys"** tab
2. Find the previous successful deploy
3. Click **"Redeploy"**

## Environment-Specific Configuration

For different environments (dev, staging, prod):

1. Create separate branches
2. Create separate Render services
3. Use different environment variables for each

## Security Best Practices

1. **Never commit `.env` file** (already in `.gitignore`)
2. **Rotate secrets regularly**
3. **Use Render's secret management** (encrypted at rest)
4. **Enable HTTPS** (automatic with Render)
5. **Monitor logs for suspicious activity**

## Performance Tips

1. **Use caching** where possible
2. **Optimize LLM prompts** to reduce tokens
3. **Limit file sizes** in data processing
4. **Use connection pooling** for databases (if added)
5. **Monitor response times** in Render dashboard

## Maintenance

### Regular Updates

```bash
# Update dependencies
pip install --upgrade openai playwright flask

# Update requirements.txt
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

### Database Backups

If you add a database:
1. Use Render's automated backups
2. Schedule regular manual backups
3. Test restore procedures

## Support

- **Render Documentation:** [https://render.com/docs](https://render.com/docs)
- **Render Community:** [https://community.render.com](https://community.render.com)
- **GitHub Issues:** Report bugs in your repository

---

## Quick Reference

### Your URLs
- **Service URL:** `https://llm-analysis-quiz.onrender.com`
- **Health Check:** `https://llm-analysis-quiz.onrender.com/health`
- **Quiz Endpoint:** `https://llm-analysis-quiz.onrender.com/quiz`

### Important Commands
```bash
# Test locally
python app.py

# Push to GitHub
git push origin main

# View logs
# (use Render dashboard)

# Redeploy
# (automatic on push or manual via dashboard)
```

---

**Last Updated:** November 28, 2025
