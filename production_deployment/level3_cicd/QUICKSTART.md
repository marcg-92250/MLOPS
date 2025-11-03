# Level 3 - QUICKSTART

## 🚀 5-Minute Setup

### 1. Docker Hub Token
```
hub.docker.com → Settings → Security → New Access Token
Save token!
```

### 2. Prepare Files
```bash
cd /home/gma/MLOPS/production_deployment/level3_cicd
cp ../level1_docker/{Dockerfile,main.py,requirements.txt} .
cp -r ../level1_docker/models .
```

### 3. Create GitHub Repo
```bash
git init
git add .
git commit -m "Initial commit"
gh repo create house-price-api --public --source=. --remote=origin
git push -u origin main
```

### 4. Add Secrets
```
GitHub repo → Settings → Secrets → Actions

Add:
- DOCKER_HUB_USERNAME: <username>
- DOCKER_HUB_TOKEN: <token>
- VM_PASSWORD: Supermotdepasse!42
```

### 5. Verify
```
GitHub → Actions tab → See workflow running
Wait 2-3 minutes
curl http://74.234.179.93:8001/predict
```

### 6. Test CI/CD
```bash
echo "test" >> README.md
git add .
git commit -m "Test"
git push
# Watch automatic deploy!
```

---

## ✅ That's It!

Every `git push` now automatically:
1. Builds Docker image
2. Pushes to Docker Hub
3. Deploys to Cloud VM
4. Updates production

---

## 🔗 Links

- **Repo**: github.com/<username>/house-price-api
- **Actions**: github.com/<username>/house-price-api/actions
- **Docker Hub**: hub.docker.com/r/<username>/house-price-api
- **Service**: http://74.234.179.93:8001/docs

