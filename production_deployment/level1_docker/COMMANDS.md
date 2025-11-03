# Level 1 Docker - Quick Commands

## 🚀 Quick Start

```bash
cd /home/gma/MLOPS/production_deployment/level1_docker

# 1. Copy model
mkdir -p models
cp ../models/house_model.joblib models/

# 2. Build image
docker build -t house-price-api:v1 .

# 3. Run container
docker run -d -p 8000:8000 --name house-api house-price-api:v1

# 4. Test
curl http://localhost:8000/predict
python test_docker.py
```

---

## 🔨 Build Commands

```bash
# Build image
docker build -t house-price-api:v1 .

# Build with no cache
docker build --no-cache -t house-price-api:v1 .

# Build with different tag
docker build -t house-price-api:latest .

# View images
docker images
```

---

## 🏃 Run Commands

```bash
# Run in foreground
docker run -p 8000:8000 house-price-api:v1

# Run in background (detached)
docker run -d -p 8000:8000 --name house-api house-price-api:v1

# Run with custom port
docker run -d -p 8080:8000 --name house-api house-price-api:v1

# Run with auto-restart
docker run -d -p 8000:8000 --restart unless-stopped --name house-api house-price-api:v1

# Run with environment variables
docker run -d -p 8000:8000 -e LOG_LEVEL=debug --name house-api house-price-api:v1
```

---

## 🔍 Inspect & Debug

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# View logs
docker logs house-api

# Follow logs (live)
docker logs -f house-api

# Last 50 lines
docker logs --tail 50 house-api

# Execute command in container
docker exec -it house-api /bin/bash

# Inspect container
docker inspect house-api

# View container stats
docker stats house-api
```

---

## 🛑 Stop & Clean

```bash
# Stop container
docker stop house-api

# Start stopped container
docker start house-api

# Restart container
docker restart house-api

# Remove container
docker rm house-api

# Force remove (even if running)
docker rm -f house-api

# Remove image
docker rmi house-price-api:v1

# Clean up everything
docker system prune -a
```

---

## 🧪 Test Commands

```bash
# Test GET
curl http://localhost:8000/predict

# Test POST
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"size": 100, "bedrooms": 3, "garden": 1}'

# Test health
curl http://localhost:8000/health

# Run test script
python test_docker.py

# Open docs in browser
firefox http://localhost:8000/docs
```

---

## 🐛 Troubleshooting

```bash
# Port already in use
lsof -i :8000
docker run -p 8001:8000 house-price-api:v1

# Container exits immediately
docker logs house-api
docker run -it house-price-api:v1

# Check Docker daemon
sudo systemctl status docker
sudo systemctl start docker

# View container processes
docker top house-api
```

---

## ⚡ Complete Workflow

```bash
# Full rebuild and restart
docker rm -f house-api
docker rmi house-price-api:v1
docker build -t house-price-api:v1 .
docker run -d -p 8000:8000 --name house-api house-price-api:v1
docker logs -f house-api
```

