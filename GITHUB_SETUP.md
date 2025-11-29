# GitHub Setup Guide

Complete guide to setting up your GitHub repository for the LLM Analysis Quiz project.

## Prerequisites

- Git installed on your system
- GitHub account created
- Repository access configured

## Step-by-Step Setup

### 1. Create GitHub Repository

#### Option A: Via GitHub Website (Recommended)

1. Go to [https://github.com/new](https://github.com/new)
2. Fill in details:
   - **Owner:** BOGGULABHARGAVA
   - **Repository name:** `llm-analysis-quiz`
   - **Description:** "LLM Analysis Quiz - Automated quiz solver using GPT-4 and data analysis"
   - **Visibility:** ✅ **PUBLIC** (very important!)
   - **Initialize:** ❌ Do NOT add README, .gitignore, or license (we already have these)
3. Click **"Create repository"**

#### Option B: Via GitHub CLI

```powershell
# Install GitHub CLI if not already installed
# winget install GitHub.cli

# Login
gh auth login

# Create repo
gh repo create llm-analysis-quiz --public --source=. --remote=origin
```

### 2. Initialize Git Locally

```powershell
# Navigate to project directory
cd "d:\TDS P2"

# Initialize git repository
git init

# Configure git (if not already done)
git config --global user.name "BOGGULABHARGAVA"
git config --global user.email "your.email@example.com"
```

### 3. Add Remote Repository

```powershell
# Add GitHub remote
git remote add origin https://github.com/BOGGULABHARGAVA/llm-analysis-quiz.git

# Verify remote
git remote -v
```

Expected output:
```
origin  https://github.com/BOGGULABHARGAVA/llm-analysis-quiz.git (fetch)
origin  https://github.com/BOGGULABHARGAVA/llm-analysis-quiz.git (push)
```

### 4. Prepare Files for Commit

```powershell
# Check what files will be added
git status

# Review .gitignore to ensure sensitive files are excluded
cat .gitignore
```

**CRITICAL:** Ensure `.env` is in `.gitignore` and NOT committed!

```powershell
# Verify .env is ignored
git check-ignore .env
# Should output: .env
```

### 5. Stage and Commit Files

```powershell
# Stage all files
git add .

# Check staged files
git status

# Commit
git commit -m "Initial commit: LLM Analysis Quiz application

- Flask API server with authentication
- Quiz solver with GPT-4 integration
- Playwright browser automation
- Multi-format data processing (PDF, CSV, Excel, JSON, images)
- Comprehensive documentation
- Deployment configuration for Render.com
- MIT License"
```

### 6. Set Main Branch

```powershell
# Rename branch to main (if needed)
git branch -M main
```

### 7. Push to GitHub

```powershell
# Push to GitHub
git push -u origin main
```

If you encounter authentication issues:

#### For HTTPS (Recommended):
```powershell
# Use Personal Access Token
# Go to GitHub → Settings → Developer Settings → Personal Access Tokens
# Generate new token with 'repo' scope
# Use token as password when prompted
```

#### For SSH:
```powershell
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add SSH key to ssh-agent
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key

# Change remote to SSH
git remote set-url origin git@github.com:BOGGULABHARGAVA/llm-analysis-quiz.git
```

### 8. Verify Repository

1. Go to `https://github.com/BOGGULABHARGAVA/llm-analysis-quiz`
2. Check that all files are present:
   - ✅ README.md
   - ✅ LICENSE
   - ✅ app.py
   - ✅ quiz_solver.py
   - ✅ browser_handler.py
   - ✅ data_processor.py
   - ✅ config.py
   - ✅ utils.py
   - ✅ requirements.txt
   - ✅ Dockerfile
   - ✅ render.yaml
   - ✅ Documentation files
   - ❌ .env (should NOT be present)
   - ❌ __pycache__ (should NOT be present)

3. Check repository settings:
   - ✅ Repository is **PUBLIC**
   - ✅ MIT License is visible
   - ✅ README renders correctly

### 9. Add Repository Description and Topics

On GitHub repository page:

1. Click **"About"** gear icon (top right)
2. Add **Description:**
   ```
   LLM Analysis Quiz - Automated quiz solver using GPT-4, Playwright, and data analysis. Handles data sourcing, processing, analysis, and visualization.
   ```
3. Add **Topics:**
   ```
   llm, gpt-4, quiz-solver, data-analysis, flask, playwright, automation, openai, python
   ```
4. Click **"Save changes"**

### 10. Create README Badge (Optional)

Add status badges to your README:

```markdown
# LLM Analysis Quiz Project

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production-success.svg)
```

---

## Repository Structure

Your repository should look like this:

```
llm-analysis-quiz/
├── .github/                    # GitHub-specific files
│   └── workflows/              # CI/CD workflows (optional)
├── app.py                      # Main Flask application
├── quiz_solver.py              # Quiz solving logic
├── browser_handler.py          # Browser automation
├── data_processor.py           # Data processing
├── config.py                   # Configuration
├── utils.py                    # Utilities
├── requirements.txt            # Dependencies
├── Dockerfile                  # Docker configuration
├── render.yaml                 # Render deployment config
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── README.md                   # Main documentation
├── QUICKSTART.md              # Quick start guide
├── DEPLOYMENT.md              # Deployment guide
├── TESTING.md                 # Testing guide
├── DESIGN_CHOICES.md          # Design decisions
├── GITHUB_SETUP.md            # This file
└── prompts.txt                # System/user prompts
```

---

## Ongoing Git Workflow

### Making Changes

```powershell
# Check status
git status

# Add specific file
git add app.py

# Or add all changes
git add .

# Commit with message
git commit -m "Fix: improved error handling in quiz solver"

# Push to GitHub
git push origin main
```

### Viewing History

```powershell
# View commit history
git log --oneline

# View changes
git diff

# View specific file history
git log -p app.py
```

### Branching (Optional)

```powershell
# Create feature branch
git checkout -b feature/enhanced-error-handling

# Make changes and commit
git add .
git commit -m "Add enhanced error handling"

# Push branch
git push origin feature/enhanced-error-handling

# Create Pull Request on GitHub
# Then merge via GitHub UI
```

### Syncing with Remote

```powershell
# Fetch changes
git fetch origin

# Pull latest changes
git pull origin main

# View remote status
git remote show origin
```

---

## Security Best Practices

### ✅ DO:
- Keep `.env` in `.gitignore`
- Use environment variables for secrets
- Review files before committing (`git status`, `git diff`)
- Use meaningful commit messages
- Keep repository public for evaluation
- Add MIT License

### ❌ DON'T:
- Commit `.env` file
- Hardcode API keys in code
- Commit `__pycache__` directories
- Commit large binary files
- Push sensitive data
- Make repository private during evaluation

---

## Troubleshooting

### Issue: "Permission denied"

**Solution:**
```powershell
# Check remote URL
git remote -v

# If HTTPS, ensure you're using correct credentials
# If SSH, ensure key is added to GitHub
ssh -T git@github.com
```

### Issue: "Repository not found"

**Solution:**
```powershell
# Verify repository exists on GitHub
# Check remote URL is correct
git remote set-url origin https://github.com/BOGGULABHARGAVA/llm-analysis-quiz.git
```

### Issue: "Already up to date" but files not updated

**Solution:**
```powershell
# Force pull (careful!)
git fetch origin
git reset --hard origin/main
```

### Issue: "Accidentally committed .env file"

**Solution:**
```powershell
# Remove from tracking
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from tracking"

# Push
git push origin main

# Note: File history still contains it!
# For complete removal, use: git filter-branch or BFG Repo-Cleaner
```

### Issue: "Merge conflicts"

**Solution:**
```powershell
# Pull latest changes
git pull origin main

# Resolve conflicts in files
# Edit files to fix conflicts

# Add resolved files
git add .

# Complete merge
git commit -m "Resolve merge conflicts"

# Push
git push origin main
```

---

## Pre-Submission Verification

Before submitting to Google Form, verify:

```powershell
# 1. Repository is public
# Check on GitHub website

# 2. All files are present
git ls-files

# 3. No sensitive files committed
git ls-files | Select-String -Pattern ".env"
# Should return nothing

# 4. License is present
git ls-files | Select-String -Pattern "LICENSE"
# Should return: LICENSE

# 5. Latest changes pushed
git status
# Should say: "nothing to commit, working tree clean"
```

---

## Repository URL for Google Form

Your final repository URL:
```
https://github.com/BOGGULABHARGAVA/llm-analysis-quiz
```

Copy this exactly into the Google Form!

---

## Advanced: GitHub Actions CI/CD (Optional)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        playwright install chromium
    
    - name: Run tests
      run: |
        python -m pytest tests/
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

---

## Quick Reference

### Common Commands

```powershell
# Status
git status

# Add files
git add .

# Commit
git commit -m "message"

# Push
git push origin main

# Pull
git pull origin main

# View log
git log --oneline

# View diff
git diff

# Create branch
git checkout -b branch-name

# Switch branch
git checkout main

# View remotes
git remote -v
```

---

**Your repository is now ready for submission! 🎉**

**Last Updated:** November 28, 2025
