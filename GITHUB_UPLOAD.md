# GitHub Upload Checklist & Instructions

This file guides you through uploading the LLM Tutor project to GitHub.

## Pre-Upload Verification ✅

Before uploading, ensure:

- [x] `.env` file created locally (NOT in git)
- [x] `.env.example` created (IN git, as template)
- [x] `.gitignore` configured properly
- [x] All sensitive files excluded
- [x] README.md created
- [x] LICENSE (MIT) created
- [x] CONTRIBUTING.md created
- [x] CHANGELOG.md created
- [x] SECURITY.md created
- [x] CONFIG.md created
- [x] DEPLOYMENT.md created
- [x] ROADMAP.md created
- [x] GitHub templates created (.github/)
- [x] CI/CD workflows configured
- [x] requirements.txt with pinned versions
- [x] requirements-dev.txt with dev tools
- [x] Project code tested and working
- [x] All non-contributing files deleted
- [x] Knowledge base verified (15 documents)

---

## Step 1: Initialize Git Repository

If not already done:

```bash
cd f:\assignment
git init
git config --global user.name "Your Name"
git config --global user.email "your.email@github.com"
```

---

## Step 2: Verify .gitignore

Make sure your `.gitignore` includes:

```bash
cat .gitignore | grep -E "\.env|__pycache__|\.venv|\.pyc"
```

Should include (already set up):
- ✅ `.env` (keeping sensitive data safe)
- ✅ `__pycache__/`
- ✅ `*.pyc`
- ✅ `.streamlit/cache`
- ✅ `.venv/`

---

## Step 3: Create GitHub Repository

### Option A: Using GitHub Web Interface

1. Go to https://github.com/new
2. **Repository name**: `llm-tutor`
3. **Description**: 
   ```
   Educational LLM tutor with RAG, Groq API integration, and multi-turn conversations
   ```
4. **Visibility**: Select "Public" (or "Private")
5. **Initialize with**:
   - [ ] DO NOT check "Add a README" (we have one)
   - [ ] DO NOT check "Add .gitignore" (we have one)
   - [ ] DO check "Choose a license" → MIT (we have one)

6. Click **"Create repository"**

### Option B: Using GitHub CLI

```bash
gh repo create llm-tutor \
  --description "Educational LLM tutor with RAG, Groq API integration" \
  --public \
  --source=. \
  --remote=origin \
  --push
```

---

## Step 4: Add Remote and Initial Commit

```bash
# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/llm-tutor.git

# Verify
git remote -v
```

---

## Step 5: Stage Files for Commit

```bash
# Stage all files
git add .

# Verify staged files (should exclude .env, __pycache__, .venv)
git status
```

**Expected to see**:
- ✅ agent.py
- ✅ capstone_streamlit.py
- ✅ kb_data.py
- ✅ requirements.txt
- ✅ requirements-dev.txt
- ✅ README.md, LICENSE, CONTRIBUTING.md, etc.
- ✅ .github/workflows/ (CI/CD)
- ✅ .env.example
- ❌ .env (should NOT appear)
- ❌ .venv/ (should NOT appear)
- ❌ __pycache__/ (should NOT appear)

---

## Step 6: Make Initial Commit

```bash
git commit -m "Initial commit: LLM Tutor v1.0.0 with RAG pipeline and 15-topic KB"
```

Better commit message following [conventional commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat: LLM Tutor v1.0.0 with RAG pipeline, Groq API, and evaluation"
```

---

## Step 7: Create and Switch to Main Branch

```bash
# If you're on 'master', rename to 'main'
git branch -M main

# Verify
git branch
```

---

## Step 8: Push to GitHub

```bash
# First push (sets upstream)
git push -u origin main

# Verify
git remote -v
```

---

## Step 9: Configure GitHub Repository Settings

### 1. Repository Settings
Go to https://github.com/USERNAME/llm-tutor/settings

**General**:
- [x] Make it a template: Optional (enables "Use this template")
- [x] Auto-delete head branches: Recommended

**Branches**:
- Default branch: `main` ✅

### 2. Add Topics
Add tags for discoverability:
- llm
- langchain
- langgraph
- rag
- groq
- education
- chatbot
- ai
- streamlit

### 3. Enable Features
Under "Features":
- [x] Discussions (for community Q&A)
- [x] Wiki (optional, for extended docs)
- [ ] Projects (optional, for tracking)

### 4. Add Secrets (for CI/CD)
Go to Settings → Secrets and variables → Actions

Add these for automated tests:
```bash
# Optional: Only if running GitHub Actions that need them
GROQ_API_KEY = "gsk_test_key_or_leave_empty"
```

---

## Step 10: Verify Deployment Files

Ensure these files are in the root:
```bash
ls -la | grep -E "README|LICENSE|CONTRIBUTING|CHANGELOG|CONFIG|SECURITY|DEPLOYMENT|ROADMAP|\.gitignore|\.env\.example"
```

All should be present:
- ✅ README.md (1000+ lines)
- ✅ LICENSE (MIT)
- ✅ CONTRIBUTING.md (300+ lines)
- ✅ CHANGELOG.md (version history)
- ✅ CONFIG.md (setup guide)
- ✅ SECURITY.md (security policy)
- ✅ DEPLOYMENT.md (deployment guide)
- ✅ ROADMAP.md (future plans)
- ✅ .gitignore (patterns)
- ✅ .env.example (template)
- ✅ .github/ (templates + workflows)

---

## Step 11: Add GitHub Badges to README

Optional: Update README.md with status badges

```markdown
# LLM Tutor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests: Python CI](https://github.com/USERNAME/llm-tutor/workflows/Python%20CI/badge.svg)](https://github.com/USERNAME/llm-tutor/actions)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://llm-tutor-app.streamlit.app)

...rest of README...
```

---

## Step 12: Set Up Branch Protection (Recommended)

Go to Settings → Branches → Add rule

**Branch name pattern**: `main`

- [x] Require pull request reviews before merging (2 reviews)
- [x] Require status checks to pass (CI/CD)
- [x] Require branches to be up to date
- [x] Enforce all configured restrictions

---

## Step 13: Create Release Notes

```bash
# After pushing, create a release on GitHub
# Go to: https://github.com/USERNAME/llm-tutor/releases

# Click "Create a new release"
# Tag: v1.0.0
# Title: LLM Tutor v1.0.0
# Description: Copy from CHANGELOG.md [1.0.0] section
```

---

## Step 14: Test Deployment

### Local Test
```bash
# Verify .env is NOT in git
git ls-files | grep "\.env$"  # Should return nothing

# If it shows, remove immediately:
git rm --cached .env
git commit -m "chore: remove .env from git"
```

### Remote Test
```bash
# Clone from your own repo to test
git clone https://github.com/USERNAME/llm-tutor.git llm-tutor-test
cd llm-tutor-test

# Should have all files EXCEPT .env and .venv
ls -la | grep "\.env\|\.venv"  # Should return nothing

# Test setup
python -m venv venv
source venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## Step 15: First GitHub Actions Run

Push a test commit to trigger CI/CD:

```bash
git commit --allow-empty -m "ci: trigger initial CI/CD"
git push origin main
```

Monitor at: https://github.com/USERNAME/llm-tutor/actions

Expected run:
- Python 3.10, 3.11, 3.12 lint checks
- Tests (if tests/ directory exists)
- Security scan

---

## Troubleshooting

### Issue: `.env` accidentally pushed?

```bash
# Remove from history
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Remove .env from git history"
git push origin main

# Rotate your API keys!
# Go to https://console.groq.com/keys and regenerate
```

### Issue: .venv too large to push?

Should be auto-ignored, but verify:
```bash
git status | grep venv  # Should show nothing

# If it shows, it's not in .gitignore. Add:
echo ".venv/" >> .gitignore
git add .gitignore
git commit -m "Ensure .venv is ignored"
```

### Issue: Large files rejected?

GitHub has 100MB file limit. Check:
```bash
find . -size +100M -type f  # Find large files
```

### Issue: CI/CD tests failing?

Check `.github/workflows/ci.yml`:
- Correct Python version
- All dependencies in requirements.txt
- Tests in `tests/` directory (create if missing)

---

## Post-Upload: Promote the Project

Once uploaded, share it:

1. **GitHub Stars** 
   - Ask friends/colleagues to star

2. **Social Media**
   - Share on Twitter, LinkedIn, Reddit
   - Include: GitHub link, brief description, live demo URL

3. **Communities**
   - r/MachineLearning
   - r/learnprogramming
   - r/Python
   - HuggingFace Spaces
   - Dev.to (write a post)

4. **Streamlit Cloud**
   - Deploy to Streamlit Cloud for live demo
   - URL: https://share.streamlit.io

5. **Documentation**
   - Ensure README is clear for first-time users
   - Add contributing guidelines
   - Create discussions for Q&A

---

## Final Checklist Before Pushing

```bash
# Run these checks locally
make check  # Or run manually:

# 1. Syntax check
python -m py_compile *.py

# 2. Linting
black --check .
flake8 .

# 3. No secrets
grep -r "gsk_" . --exclude-dir=.git  # Should return 0 results
grep -r "sk_" . --exclude-dir=.git   # Should return 0 results

# 4. Required files exist
ls README.md LICENSE CONTRIBUTING.md CHANGELOG.md .gitignore .env.example

# 5. All staged
git status
```

---

## Success! 🎉

Your LLM Tutor project is now on GitHub!

**Next Steps**:
1. ✅ Monitor GitHub Actions
2. ✅ Deploy to Streamlit Cloud or other platform
3. ✅ Collect stars and feedback
4. ✅ Address issues and PRs
5. ✅ Plan v1.1.0 release

---

**Questions?**
- GitHub Issues: Report problems
- GitHub Discussions: Ask questions
- README.md: User guide
- CONTRIBUTING.md: Developer guide

---

**Date**: April 20, 2026
**Version**: 1.0.0
