# Level 2 Cloud - Quick Commands

## 🚀 Quick Deployment

### Automated (Recommended)

```bash
cd /home/gma/MLOPS/production_deployment/level2_cloud
bash deploy_cloud.sh
# Enter password when prompted: Supermotdepasse!42
```

### Manual Steps

```bash
# 1. Transfer files
cd /home/gma/MLOPS/production_deployment/level1_docker
scp -r Dockerfile main.py requirements.txt models/ \
  ubuntu@74.234.179.93:/home/ubuntu/gma/

# 2. Connect to VM
ssh ubuntu@74.234.179.93

# 3. Build and run
cd /home/ubuntu/gma
docker build -t house-price-api:v1 .
docker run -d -p 8001:8000 --name house-api house-price-api:v1

# 4. Test from local
curl http://74.234.179.93:8001/predict
```

---

## 📋 VM Commands

### Connect to VM

```bash
ssh ubuntu@74.234.179.93
# Password: Supermotdepasse!42
```

### Setup on VM (First Time)

```bash
# Create folder
cd /home/ubuntu
mkdir -p gma
cd gma

# Check Docker
docker --version

# If Docker not installed
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker ubuntu
# Log out and back in
```

### Build on VM

```bash
cd /home/ubuntu/gma

# Build image
docker build -t house-price-api:v1 .

# Verify
docker images
```

### Run Container on VM

```bash
# Run on port 8001
docker run -d -p 8001:8000 --name house-api house-price-api:v1

# Check status
docker ps

# View logs
docker logs house-api
docker logs -f house-api
```

### Manage Container on VM

```bash
# Stop
docker stop house-api

# Start
docker start house-api

# Restart
docker restart house-api

# Remove
docker rm -f house-api

# Rebuild and rerun
docker stop house-api && docker rm house-api
docker build -t house-price-api:v1 .
docker run -d -p 8001:8000 --name house-api house-price-api:v1
```

---

## 🧪 Test from Local Machine

```bash
# Simple test
curl http://74.234.179.93:8001/predict

# POST test
curl -X POST http://74.234.179.93:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"size": 100, "bedrooms": 3, "garden": 1}'

# Full test suite
cd /home/gma/MLOPS/production_deployment/level2_cloud
python test_cloud.py

# Test with custom port
python test_cloud.py 8002
```

---

## 🔄 Update Deployment

```bash
# From local machine
cd /home/gma/MLOPS/production_deployment/level2_cloud

# Run deployment script (transfers + rebuilds + restarts)
bash deploy_cloud.sh
```

---

## 🐛 Troubleshooting

### Check if running

```bash
# On VM
docker ps | grep house-api

# Check logs
docker logs house-api

# Test locally on VM
curl localhost:8001/predict
```

### Port in use

```bash
# On VM
sudo lsof -i :8001

# Use different port
docker run -d -p 8002:8000 --name house-api house-price-api:v1
```

### Firewall

```bash
# On VM
sudo ufw status

# Allow port (ask trainer first)
sudo ufw allow 8001
```

### Can't connect from outside

```bash
# On VM - test internally
curl localhost:8001/predict

# If works internally but not externally:
# 1. Check firewall
# 2. Verify port mapping: -p 8001:8000
# 3. Check VM security groups (cloud provider)
```

---

## 📊 Monitoring

```bash
# On VM

# Container stats
docker stats house-api

# Disk usage
docker system df

# Container details
docker inspect house-api

# Resource usage
docker top house-api
```

---

## ✅ Quick Verification

```bash
# Local: Can you access?
curl http://74.234.179.93:8001/predict

# Browser
firefox http://74.234.179.93:8001/docs

# Ask friend to test
# Send them: http://74.234.179.93:8001/predict
```

---

## 🌐 URLs to Share

```
API: http://74.234.179.93:8001/predict
Docs: http://74.234.179.93:8001/docs
Health: http://74.234.179.93:8001/health
```

Replace `8001` with your assigned port!

