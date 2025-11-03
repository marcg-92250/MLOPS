# Level 3 - Quick Setup Guide

## 🚀 Quick Start (5 minutes)

### Prerequisites

- [ ] GitHub account
- [ ] Docker Hub account
- [ ] Git installed locally

---

## Step-by-Step Setup

### 1️⃣ Create Docker Hub Access Token

```
1. Go to https://hub.docker.com/
2. Login
3. Profile → Account Settings → Security
4. "New Access Token"
5. Name: github-actions
6. Copy token (you won't see it again!)
```

### 2️⃣ Prepare Project Files

```bash
cd /home/gma/MLOPS/production_deployment/level3_cicd

# Copy files from level1_docker
cp ../level1_docker/Dockerfile .
cp ../level1_docker/main.py .
cp ../level1_docker/requirements.txt .
cp -r ../level1_docker/models .

# Verify files
ls -la
# Should see: Dockerfile, main.py, requirements.txt, models/, .github/
```

### 3️⃣ Initialize Git Repository

```bash
# Initialize
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: House Price API with CI/CD"
```

### 4️⃣ Create GitHub Repository

**Option A: GitHub Website**
```
1. Go to github.com
2. Click "+" → "New repository"
3. Name: house-price-api
4. Public
5. Don't initialize with README
6. Create repository
7. Follow instructions to push existing repo
```

**Option B: GitHub CLI**
```bash
gh repo create house-price-api --public --source=. --remote=origin
git push -u origin main
```

### 5️⃣ Add GitHub Secrets

```
1. Go to your repo on GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"

Add 3 secrets:

Secret 1:
Name: DOCKER_HUB_USERNAME
Value: <your-docker-hub-username>

Secret 2:
Name: DOCKER_HUB_TOKEN
Value: <token-from-step-1>

Secret 3:
Name: VM_PASSWORD
Value: Supermotdepasse!42
```

### 6️⃣ Verify Workflow File

```bash
# Check workflow exists
cat .github/workflows/deploy.yml

# Should contain:
# - on: push: branches: [main]
# - build-and-push job
# - deploy job
```

### 7️⃣ Trigger First Deployment

```bash
# Make sure you're on main branch
git branch -M main

# Push (this triggers the workflow!)
git push -u origin main
```

### 8️⃣ Watch Deployment

```
1. Go to GitHub repository
2. Click "Actions" tab
3. See "Build and Deploy to Cloud VM" running
4. Click on the workflow run to see details
5. Watch the magic happen! ✨
```

### 9️⃣ Verify Deployment

```bash
# Wait for workflow to complete (2-3 minutes)

# Test the service
curl http://74.234.179.93:8001/predict

# Expected: {"y_pred":2}

# Check Docker Hub
# Go to hub.docker.com → Repositories
# You should see: <username>/house-price-api
```

### 🔟 Test Automatic Update

```bash
# Make a change
echo "# CI/CD Test" >> README.md

# Commit and push
git add README.md
git commit -m "Test CI/CD pipeline"
git push

# Go to GitHub Actions
# Watch automatic rebuild and deploy!
```

---

## 🎯 Success Criteria

✅ Workflow appears in GitHub Actions  
✅ Builds without errors  
✅ Image appears on Docker Hub  
✅ Container runs on VM  
✅ Service responds at http://74.234.179.93:8001  
✅ Second push triggers automatic update  

---

## 🐛 Quick Troubleshooting

### "Error: buildx failed"
```bash
# Check Dockerfile syntax
docker build -t test .
```

### "Error: invalid username or password"
```bash
# Check secrets:
# - DOCKER_HUB_USERNAME (not email!)
# - DOCKER_HUB_TOKEN (not password!)
# Must be access token from Docker Hub
```

### "Error: SSH connection failed"
```bash
# Check VM_PASSWORD secret
# Should be: Supermotdepasse!42

# Test SSH manually:
ssh ubuntu@74.234.179.93
```

### "Workflow doesn't trigger"
```bash
# Make sure:
# 1. File is in .github/workflows/deploy.yml
# 2. Pushed to 'main' branch
# 3. Workflow has correct syntax (YAML)

# Check current branch
git branch

# Switch to main if needed
git checkout main
```

---

## 📋 Command Summary

```bash
# Setup
cd /home/gma/MLOPS/production_deployment/level3_cicd
cp ../level1_docker/{Dockerfile,main.py,requirements.txt} .
cp -r ../level1_docker/models .

# Git
git init
git add .
git commit -m "Initial commit"
gh repo create house-price-api --public --source=. --remote=origin
git push -u origin main

# Test
curl http://74.234.179.93:8001/predict

# Update
git add .
git commit -m "Update"
git push
```

---

## 🔗 Important Links

- **Your Repo**: https://github.com/<username>/house-price-api
- **Actions**: https://github.com/<username>/house-price-api/actions
- **Docker Hub**: https://hub.docker.com/r/<username>/house-price-api
- **Service**: http://74.234.179.93:8001/docs

---

## 💡 Tips

1. **Always check Actions tab** for workflow status
2. **Read error logs** carefully in failed workflows
3. **Test locally** before pushing (docker build .)
4. **Use workflow_dispatch** to manually trigger workflows
5. **Keep secrets safe** - never commit them to git!

---

**You're all set! Every push to main now automatically deploys to production! 🚀**

