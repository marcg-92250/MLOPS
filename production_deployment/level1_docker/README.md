# Level 1: Docker Containerization

Package the FastAPI web service in a Docker container.

## 🎯 Objectives

1. Create a Dockerfile
2. Build the Docker image
3. Run the container with port mapping
4. Test the containerized service

---

## 📋 Prerequisites

### Install Docker

**Check if Docker is installed**:
```bash
docker --version
```

**If not installed**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER
# Log out and back in for this to take effect
```

**Test Docker**:
```bash
docker run hello-world
```

---

## 🚀 STEP 1: Create Dockerfile

✅ **Done!** The `Dockerfile` is created with:
- Python 3.11 slim base image
- Dependencies installation
- Application code
- Model file
- Exposed port 8000
- Health check
- Uvicorn server command

**Review the Dockerfile**:
```bash
cat Dockerfile
```

---

## 🔨 STEP 2: Build the Docker Image

### Prepare the files

```bash
cd /home/gma/MLOPS/production_deployment/level1_docker

# Copy the trained model
mkdir -p models
cp ../models/house_model.joblib models/

# Verify files are present
ls -la
```

### Build the image

```bash
# Build the Docker image
docker build -t house-price-api:v1 .

# The -t flag tags the image with a name and version
# The . at the end means use current directory as build context
```

**Expected output**:
```
[+] Building 45.2s (12/12) FINISHED
...
=> => naming to docker.io/library/house-price-api:v1
```

### Verify the image was created

```bash
# List Docker images
docker images

# You should see:
# REPOSITORY          TAG       IMAGE ID       CREATED          SIZE
# house-price-api     v1        xxxxx          few seconds ago  ~500MB
```

---

## 🏃 STEP 3: Run the Container

### Basic run

```bash
# Run the container with port mapping
docker run -p 8000:8000 house-price-api:v1

# -p 8000:8000 maps port 8000 on host to port 8000 in container
# Format: -p HOST_PORT:CONTAINER_PORT
```

### Run in detached mode (background)

```bash
# Run in background
docker run -d -p 8000:8000 --name house-api house-price-api:v1

# -d: detached mode (background)
# --name: give the container a name
```

### Useful run options

```bash
# Run with custom port
docker run -d -p 8080:8000 --name house-api house-price-api:v1

# Run with logs
docker run -p 8000:8000 house-price-api:v1

# Run with auto-restart
docker run -d -p 8000:8000 --restart unless-stopped --name house-api house-price-api:v1
```

---

## ✅ STEP 4: Test the Service

### Method 1: curl

```bash
# Test GET /predict
curl http://localhost:8000/predict

# Expected: {"y_pred":2}

# Test POST /predict
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"size": 100, "bedrooms": 3, "garden": 1}'

# Expected: {"predicted_price":..., "input_features":{...}}
```

### Method 2: Browser

Open: http://localhost:8000/predict

**Interactive docs**: http://localhost:8000/docs

### Method 3: Python

```python
import requests

# Test GET
response = requests.get("http://localhost:8000/predict")
print(response.json())

# Test POST
data = {"size": 100, "bedrooms": 3, "garden": 1}
response = requests.post("http://localhost:8000/predict", json=data)
print(response.json())
```

---

## 🛠️ Docker Management Commands

### View running containers

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a
```

### View logs

```bash
# View logs
docker logs house-api

# Follow logs (live)
docker logs -f house-api

# Last 100 lines
docker logs --tail 100 house-api
```

### Stop/Start container

```bash
# Stop container
docker stop house-api

# Start container
docker start house-api

# Restart container
docker restart house-api
```

### Remove container

```bash
# Stop and remove
docker stop house-api
docker rm house-api

# Force remove (even if running)
docker rm -f house-api
```

### Access container shell

```bash
# Execute bash inside container
docker exec -it house-api /bin/bash

# Or sh if bash not available
docker exec -it house-api /bin/sh

# Inside container, you can check files:
ls -la
cat main.py
```

### Remove images

```bash
# Remove image
docker rmi house-price-api:v1

# Force remove
docker rmi -f house-price-api:v1
```

---

## 🧪 Complete Test Script

Create `test_docker.py`:

```python
#!/usr/bin/env python3
import requests
import time

BASE_URL = "http://localhost:8000"

print("Testing Dockerized API...")

# Wait for container to be ready
time.sleep(2)

# Test 1: Root endpoint
print("\n1. Testing root endpoint...")
response = requests.get(BASE_URL)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

# Test 2: GET /predict
print("\n2. Testing GET /predict...")
response = requests.get(f"{BASE_URL}/predict")
print(f"   Response: {response.json()}")
assert response.json()["y_pred"] == 2

# Test 3: POST /predict
print("\n3. Testing POST /predict...")
data = {"size": 100, "bedrooms": 3, "garden": 1}
response = requests.post(f"{BASE_URL}/predict", json=data)
result = response.json()
print(f"   Input: {data}")
print(f"   Predicted price: ${result['predicted_price']:,.2f}")

print("\n✅ All tests passed!")
```

Run it:
```bash
python test_docker.py
```

---

## 🐛 Troubleshooting

### Port already in use

```bash
# Check what's using port 8000
lsof -i :8000

# Use different port
docker run -p 8001:8000 house-price-api:v1
```

### Container exits immediately

```bash
# Check logs
docker logs house-api

# Run interactively to see errors
docker run -it house-price-api:v1
```

### Can't connect to Docker daemon

```bash
# Start Docker service
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

### Model not found error

```bash
# Make sure model is copied before building
cp ../models/house_model.joblib models/

# Rebuild image
docker build -t house-price-api:v1 .
```

### Image too large

```bash
# Check image size
docker images

# Use multi-stage builds or alpine base image
# Clean up unused images
docker system prune -a
```

---

## 📊 Quick Commands Reference

```bash
# Build
docker build -t house-price-api:v1 .

# Run
docker run -d -p 8000:8000 --name house-api house-price-api:v1

# Test
curl http://localhost:8000/predict

# Logs
docker logs -f house-api

# Stop
docker stop house-api

# Clean up
docker rm house-api
docker rmi house-price-api:v1
```

---

## ✅ Verification Checklist

- [ ] Dockerfile created
- [ ] Model copied to `models/` directory
- [ ] Image built successfully
- [ ] Container running on port 8000
- [ ] GET /predict returns `{"y_pred": 2}`
- [ ] POST /predict returns predictions
- [ ] Can access http://localhost:8000/docs
- [ ] Logs show no errors

---

## 🎓 What You Learned

- ✅ Created a Dockerfile for Python web service
- ✅ Built Docker images with `docker build`
- ✅ Ran containers with port mapping (`-p` flag)
- ✅ Managed containers (start, stop, logs)
- ✅ Tested containerized applications

---

## 📖 Next Steps

After Level 1, you'll learn:
- **Level 2**: Deploy on cloud VM
- **Level 3**: CI/CD with GitHub Actions
- **Level 4**: Advanced deployment strategies

---

**Your service is now containerized! 🐳**

