# Level 4: CI/CD Pipeline

Automate build, test, and deployment with GitHub Actions.

## 🎯 Goals

When you push to the `main` branch:
1. **Build**: Docker image is automatically built
2. **Push**: Image is pushed to Docker Hub
3. **Deploy**: Image is deployed to VM
4. **Verify**: Deployment is verified

## 📋 Prerequisites

### 1. GitHub Repository

Create a repository and push your code:
```bash
cd /home/gma/MLOPS/production_deployment
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/house-price-api.git
git push -u origin main
```

### 2. Docker Hub Account

1. Create account at https://hub.docker.com
2. Create repository: `house-price-api`

### 3. GitHub Secrets

Go to: **Settings → Secrets and variables → Actions**

Add these secrets:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `DOCKER_USERNAME` | Docker Hub username | `yourusername` |
| `DOCKER_PASSWORD` | Docker Hub password/token | `dckr_pat_xxx` |
| `VM_HOST` | VM IP address | `123.45.67.89` |
| `VM_USER` | VM username | `ubuntu` |
| `SSH_PRIVATE_KEY` | SSH private key for VM | `-----BEGIN...` |

## 🔑 Setup SSH Key for VM

### Generate SSH key pair
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/vm_deploy_key -N ""
```

### Add public key to VM
```bash
ssh-copy-id -i ~/.ssh/vm_deploy_key.pub ubuntu@YOUR_VM_IP
```

### Add private key to GitHub Secrets
```bash
cat ~/.ssh/vm_deploy_key
# Copy the output and add as SSH_PRIVATE_KEY secret
```

## 📄 GitHub Actions Workflow

The workflow file `.github/workflows/deploy.yml` does:

### On every push:
1. Checkout code
2. Set up Python
3. Install dependencies
4. Run tests
5. Build Docker image
6. Push to Docker Hub

### On push to main:
7. Deploy to VM via SSH
8. Pull latest image
9. Stop old container
10. Start new container
11. Verify deployment

## 🚀 Trigger Deployment

### Automatic (on git push)
```bash
# Make changes
vim level1_fastapi/main.py

# Commit and push
git add .
git commit -m "Update API"
git push origin main

# GitHub Actions will automatically:
# - Build Docker image
# - Push to Docker Hub
# - Deploy to VM
```

### Manual (GitHub UI)
1. Go to repository
2. Click **Actions** tab
3. Select workflow
4. Click **Run workflow**

## 📊 Monitor Deployment

### GitHub Actions
- Go to **Actions** tab
- Click on the running workflow
- View logs in real-time

### Check Docker Hub
- Go to https://hub.docker.com
- Check your `house-price-api` repository
- Verify new image was pushed

### Verify on VM
```bash
ssh ubuntu@YOUR_VM_IP
docker ps | grep house-api
curl http://localhost:8000/health
```

## 🧪 Testing the Pipeline

### 1. Make a change
```bash
echo "# Test change" >> README.md
git add README.md
git commit -m "Test CI/CD pipeline"
git push origin main
```

### 2. Watch the build
Go to GitHub Actions tab and watch the workflow

### 3. Verify deployment
```bash
curl http://YOUR_VM_IP:8000/health
```

## 🔧 Workflow Customization

### Add tests
```yaml
- name: Run tests
  run: |
    pytest tests/
    pylint *.py
```

### Add notifications
```yaml
- name: Notify on Slack
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Multi-environment
```yaml
deploy-staging:
  if: github.ref == 'refs/heads/develop'
  # Deploy to staging

deploy-production:
  if: github.ref == 'refs/heads/main'
  # Deploy to production
```

## 📚 Learn GitHub Actions

Complete these exercises:
https://github.com/lcetinsoy/revision-git/blob/master/exercice5.md

## 🐛 Troubleshooting

### Build fails
- Check workflow syntax
- Verify secrets are set
- Check Dockerfile

### Push to Docker Hub fails
- Verify Docker Hub credentials
- Check repository exists
- Verify token permissions

### Deployment fails
- Verify SSH key is correct
- Check VM is accessible
- Verify Docker is installed on VM
- Check firewall rules

### Container won't start
- Check logs: `docker logs house-api`
- Verify port is available
- Check model file exists

## 🎓 Advanced Topics

### Blue/Green Deployment
```yaml
- name: Blue/Green Deploy
  run: |
    # Start green
    docker run -d -p 8001:8000 --name house-api-green ...
    # Test green
    curl http://localhost:8001/health
    # Switch traffic
    docker stop house-api-blue
    docker rename house-api-green house-api-blue
```

### Canary Deployment
```yaml
- name: Canary Deploy
  run: |
    # Deploy canary (10% traffic)
    docker run -d -p 8002:8000 --name house-api-canary ...
    # Monitor metrics
    # If OK, roll out to 100%
```

### Rollback
```yaml
- name: Rollback on failure
  if: failure()
  run: |
    docker pull ${{ secrets.DOCKER_USERNAME }}/house-price-api:previous
    docker stop house-api
    docker run -d -p 8000:8000 --name house-api \
      ${{ secrets.DOCKER_USERNAME }}/house-price-api:previous
```

## 🚀 Production Best Practices

✅ **Tag versions**: Use semantic versioning  
✅ **Run tests**: Comprehensive test suite  
✅ **Health checks**: Verify deployment health  
✅ **Monitoring**: Set up alerts  
✅ **Logging**: Centralized log management  
✅ **Rollback strategy**: Automated rollback on failure  
✅ **Security scanning**: Scan Docker images  
✅ **Documentation**: Keep README updated  

## 🏆 Level 5: Bonus Challenge

Adapt this deployment for:
- Image classification model
- Hugging Face BERT/T5 model
- Custom trained model from another course

## ✅ Complete CI/CD Checklist

- [ ] GitHub repository created
- [ ] Docker Hub account created
- [ ] GitHub Secrets configured
- [ ] SSH key added to VM
- [ ] Workflow file added
- [ ] First successful deployment
- [ ] Automatic deployment on push
- [ ] Health checks passing
- [ ] Accessible by colleagues
- [ ] Documentation updated

## 🎉 Congratulations!

You've completed all 5 levels of the Model Deployment project!

You now know how to:
- Build interactive ML apps with Streamlit
- Create REST APIs with FastAPI
- Containerize applications with Docker
- Deploy to cloud infrastructure
- Automate everything with CI/CD

**You're ready for production ML deployment!** 🚀

