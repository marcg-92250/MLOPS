# Level 3: CI/CD with GitHub Actions

Automatically build and deploy your Docker container using GitHub Actions.

## 🎯 Objectives

1. Learn GitHub Actions basics
2. Automatically build Docker image on git push
3. Push image to Docker Hub
4. Automatically deploy to Cloud VM
5. Update production service automatically

---

## 📚 Part 1: Learn GitHub Actions

### Exercise 5 from revision-git

Before starting, complete the GitHub Actions tutorial:
https://github.com/lcetinsoy/revision-git/blob/master/exercice5.md

**Key concepts to understand:**
- Workflows and jobs
- Triggers (on push, pull_request, etc.)
- Steps and actions
- Secrets and environment variables
- Artifacts and caching

---

## 🚀 Part 2: Setup CI/CD Pipeline

### Overview

When you `git push` to main branch:
1. ✅ GitHub Actions triggers automatically
2. ✅ Builds Docker image
3. ✅ Pushes image to Docker Hub
4. ✅ Deploys to Cloud VM
5. ✅ Restarts service with new image

---

## 🔧 Setup Instructions

### Step 1: Create Docker Hub Account

1. Go to https://hub.docker.com/
2. Sign up or log in
3. Create an access token:
   - Profile → Account Settings → Security
   - Click "New Access Token"
   - Name: `github-actions`
   - Save the token (you won't see it again!)

### Step 2: Create GitHub Repository

```bash
cd /home/gma/MLOPS/production_deployment/level3_cicd

# Copy necessary files
cp ../level1_docker/Dockerfile .
cp ../level1_docker/main.py .
cp ../level1_docker/requirements.txt .
cp -r ../level1_docker/models .

# Initialize git
git init
git add .
git commit -m "Initial commit: House Price API with CI/CD"

# Create repo on GitHub
# Option 1: Via website
# Go to github.com → New repository → "house-price-api"

# Option 2: Via GitHub CLI (if installed)
gh repo create house-price-api --public --source=. --remote=origin --push
```

### Step 3: Configure GitHub Secrets

Go to your GitHub repository:
`Settings → Secrets and variables → Actions → New repository secret`

Add these secrets:

| Secret Name | Value | Where to find |
|------------|-------|---------------|
| `DOCKER_HUB_USERNAME` | Your Docker Hub username | hub.docker.com profile |
| `DOCKER_HUB_TOKEN` | Your Docker Hub access token | Generated in Step 1 |
| `VM_PASSWORD` | `Supermotdepasse!42` | Provided VM password |

### Step 4: Add GitHub Actions Workflow

The workflow file is already created at:
`.github/workflows/deploy.yml`

**What it does:**

```yaml
# Trigger: On push to main
on:
  push:
    branches: [main]

# Job 1: Build and Push
- Checkout code
- Login to Docker Hub
- Build Docker image
- Push to Docker Hub

# Job 2: Deploy to VM
- Connect to VM via SSH
- Pull latest image
- Stop old container
- Start new container
- Verify deployment
```

### Step 5: Push to GitHub

```bash
# Add workflow file
git add .github/workflows/deploy.yml
git add README.md
git commit -m "Add CI/CD workflow"

# Push to main branch (triggers the workflow!)
git branch -M main
git push -u origin main
```

### Step 6: Watch the Magic! ✨

1. Go to GitHub repository
2. Click "Actions" tab
3. See your workflow running in real-time!
4. Watch as it:
   - Builds the image
   - Pushes to Docker Hub
   - Deploys to VM
   - Verifies deployment

---

## 📋 Workflow Breakdown

### Job 1: Build and Push

```yaml
build-and-push:
  runs-on: ubuntu-latest
  steps:
    - Checkout code
    - Setup Docker Buildx
    - Login to Docker Hub (using secrets)
    - Build Docker image
    - Push to Docker Hub
    - Tag as 'latest' and with commit SHA
```

### Job 2: Deploy

```yaml
deploy:
  needs: build-and-push  # Waits for build to complete
  runs-on: ubuntu-latest
  steps:
    - SSH to VM
    - Pull latest image from Docker Hub
    - Stop old container
    - Start new container
    - Verify service is running
```

---

## 🧪 Testing the Pipeline

### Test 1: Make a Change

```bash
# Edit main.py - change version number
sed -i 's/version="1.0.0"/version="1.0.1"/' main.py

# Commit and push
git add main.py
git commit -m "Update version to 1.0.1"
git push
```

**Expected result:**
- Workflow triggers automatically
- New image built with v1.0.1
- Deployed to VM
- Service updated in production

### Test 2: Verify Deployment

```bash
# Check Docker Hub
# Go to hub.docker.com → Your repositories
# You should see: <username>/house-price-api with 'latest' tag

# Test the deployed service
curl http://74.234.179.93:8001/predict

# Check the docs
firefox http://74.234.179.93:8001/docs
```

### Test 3: Check VM

```bash
# SSH to VM
ssh ubuntu@74.234.179.93

# Check container
docker ps | grep house-api

# Check image
docker images | grep house-price-api

# Check logs
docker logs house-api
```

---

## 🔍 Monitoring Workflows

### View Workflow Runs

**On GitHub:**
1. Go to "Actions" tab
2. See all workflow runs
3. Click on a run to see details
4. View logs for each step

### Workflow Status

- ✅ **Green check**: Success
- ❌ **Red X**: Failed
- 🟡 **Yellow circle**: Running
- ⚪ **Gray circle**: Queued

### View Logs

```bash
# GitHub Actions logs are available in the UI
# Click on a workflow run → Click on a job → See logs

# On VM, check container logs
ssh ubuntu@74.234.179.93
docker logs house-api
```

---

## 🐛 Troubleshooting

### Workflow Fails at "Login to Docker Hub"

**Problem:** Invalid credentials

**Solution:**
```bash
# Check secrets are set correctly:
# GitHub repo → Settings → Secrets → Actions
# - DOCKER_HUB_USERNAME
# - DOCKER_HUB_TOKEN (must be access token, not password!)
```

### Workflow Fails at "Deploy to VM"

**Problem:** SSH connection failed

**Solution:**
```bash
# Check VM_PASSWORD secret is correct
# Test SSH manually:
ssh ubuntu@74.234.179.93
# Password: Supermotdepasse!42
```

### Image Not Found on VM

**Problem:** Pull failed

**Solution:**
```bash
# Check if image exists on Docker Hub
# Go to hub.docker.com

# Manually pull on VM
ssh ubuntu@74.234.179.93
docker pull <your-username>/house-price-api:latest
```

### Container Starts but Service Doesn't Work

**Problem:** Model file missing or port conflict

**Solution:**
```bash
# Check container logs
ssh ubuntu@74.234.179.93
docker logs house-api

# Make sure model file is in Dockerfile
# Check Dockerfile:
# COPY models/house_model.joblib ./models/house_model.joblib
```

---

## 🎨 Customization

### Change Trigger

```yaml
# Only on main branch
on:
  push:
    branches: [main]

# On main and develop
on:
  push:
    branches: [main, develop]

# On tag
on:
  push:
    tags:
      - 'v*'

# Manual trigger
on:
  workflow_dispatch:
```

### Add Slack Notifications

```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Add Tests Before Deploy

```yaml
- name: Run tests
  run: |
    pip install pytest requests
    pytest tests/
```

### Use Environment Variables

```yaml
- name: Deploy to staging
  if: github.ref == 'refs/heads/develop'
  # Deploy to staging VM

- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  # Deploy to production VM
```

---

## 📊 Best Practices

### 1. Semantic Versioning

```bash
# Tag releases
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 2. Environment-Specific Configs

```yaml
environments:
  production:
    url: http://74.234.179.93:8001
```

### 3. Rollback Strategy

```bash
# If deployment fails, rollback
docker run -d -p 8001:8000 \
  --name house-api \
  <username>/house-price-api:previous-tag
```

### 4. Health Checks

```yaml
- name: Health check
  run: |
    for i in {1..10}; do
      curl -f http://$VM_HOST:$VM_PORT/health && break
      sleep 5
    done
```

### 5. Backup Before Deploy

```bash
# Backup current container
docker commit house-api house-api-backup
```

---

## ✅ Verification Checklist

- [ ] Docker Hub account created
- [ ] Access token generated
- [ ] GitHub repository created
- [ ] Secrets configured (DOCKER_HUB_USERNAME, DOCKER_HUB_TOKEN, VM_PASSWORD)
- [ ] Workflow file added (.github/workflows/deploy.yml)
- [ ] Dockerfile, main.py, requirements.txt, models/ copied
- [ ] Pushed to GitHub main branch
- [ ] Workflow triggered automatically
- [ ] Image built and pushed to Docker Hub
- [ ] Container deployed to VM
- [ ] Service accessible at http://74.234.179.93:8001
- [ ] Made a change and pushed (workflow triggered again)
- [ ] Production updated automatically

---

## 🎓 What You Learned

- ✅ GitHub Actions workflows
- ✅ CI/CD pipeline setup
- ✅ Docker Hub integration
- ✅ Automated testing
- ✅ SSH-based deployment
- ✅ Secrets management
- ✅ Production deployment automation

---

## 📖 Resources

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Docker Build Push Action**: https://github.com/docker/build-push-action
- **SSH Action**: https://github.com/appleboy/ssh-action
- **Exercise 5**: https://github.com/lcetinsoy/revision-git/blob/master/exercice5.md

---

## 🚀 Next Level

Now every time you:
```bash
git add .
git commit -m "Update model"
git push
```

Your entire production service updates automatically! 🎉

**That's the power of CI/CD!**

