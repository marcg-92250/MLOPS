# Level 2: Deploy Docker Container on Cloud VM

Deploy your Dockerized web service on a cloud virtual machine.

## 🎯 Objectives

1. Connect to cloud VM
2. Create your personal folder
3. Deploy Docker container on VM
4. Test access from external machines
5. Share with colleagues

---

## 📋 VM Information

**SSH Access**:
```
Host: 74.234.179.93
User: ubuntu
Password: Supermotdepasse!42
```

---

## 🚀 Deployment Methods

You have **3 options** to deploy your Docker container:

### Option 1: Build on VM (Recommended)
Transfer code and build image directly on VM

### Option 2: Export/Import Image
Save image locally, transfer, and load on VM

### Option 3: Docker Registry
Push to Docker Hub, pull on VM

We'll focus on **Option 1** (easiest) and **Option 3** (most professional).

---

## 🔧 Method 1: Build on VM (Recommended)

### STEP 1: Connect to VM

```bash
ssh ubuntu@74.234.179.93
# Password: Supermotdepasse!42
```

### STEP 2: Create Your Folder

```bash
# On the VM
cd /home/ubuntu

# Create folder with your initials (e.g., gma)
mkdir -p gma
cd gma
```

### STEP 3: Transfer Docker Files

**From your local machine** (new terminal):

```bash
cd /home/gma/MLOPS/production_deployment/level1_docker

# Transfer all necessary files
scp -r Dockerfile main.py requirements.txt models/ \
  ubuntu@74.234.179.93:/home/ubuntu/gma/

# Or use rsync
rsync -avz -e ssh \
  Dockerfile main.py requirements.txt models/ \
  ubuntu@74.234.179.93:/home/ubuntu/gma/
```

### STEP 4: Install Docker on VM (if needed)

**On the VM**:

```bash
# Check if Docker is installed
docker --version

# If not installed:
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# IMPORTANT: Log out and log back in for group changes
exit
ssh ubuntu@74.234.179.93
```

### STEP 5: Build Image on VM

**On the VM**:

```bash
cd /home/ubuntu/gma

# Build the image
docker build -t house-price-api:v1 .

# Verify image was created
docker images
```

### STEP 6: Run Container on VM

```bash
# Run on port 8001 (use your assigned port)
docker run -d -p 8001:8000 --name house-api house-price-api:v1

# Verify it's running
docker ps

# Check logs
docker logs house-api
```

**⚠️ Important**: Use a unique port (e.g., 8001, 8002, 8003) to avoid conflicts with colleagues!

### STEP 7: Test from Your Local Machine

```bash
# From your local machine
curl http://74.234.179.93:8001/predict

# Expected: {"y_pred":2}

# Test POST
curl -X POST http://74.234.179.93:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"size": 100, "bedrooms": 3, "garden": 1}'
```

### STEP 8: Share with a Friend

Give them your URL:
```
http://74.234.179.93:8001/predict
http://74.234.179.93:8001/docs
```

They should be able to access it from anywhere!

---

## 🐳 Method 2: Docker Hub (Professional Way)

### STEP 1: Push to Docker Hub

**From your local machine**:

```bash
# Login to Docker Hub
docker login

# Tag your image
docker tag house-price-api:v1 <your-dockerhub-username>/house-price-api:v1

# Push to Docker Hub
docker push <your-dockerhub-username>/house-price-api:v1
```

### STEP 2: Pull on VM

**On the VM**:

```bash
cd /home/ubuntu/gma

# Pull the image
docker pull <your-dockerhub-username>/house-price-api:v1

# Run container
docker run -d -p 8001:8000 \
  --name house-api \
  <your-dockerhub-username>/house-price-api:v1
```

---

## 🛠️ Container Management on VM

### View Running Containers

```bash
# On VM
docker ps
docker ps -a
```

### View Logs

```bash
docker logs house-api
docker logs -f house-api  # Follow logs
```

### Restart Container

```bash
docker restart house-api
```

### Stop and Remove

```bash
docker stop house-api
docker rm house-api
```

### Update Container

```bash
# Stop and remove old container
docker stop house-api
docker rm house-api

# Pull new image or rebuild
docker build -t house-price-api:v1 .

# Run new container
docker run -d -p 8001:8000 --name house-api house-price-api:v1
```

---

## 🔍 Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
sudo lsof -i :8001

# Use a different port
docker run -d -p 8002:8000 --name house-api house-price-api:v1
```

### Container Not Accessible from Outside

**Check firewall**:
```bash
# On VM
sudo ufw status

# If firewall is blocking (ask trainer first)
sudo ufw allow 8001
```

**Make sure container is running**:
```bash
docker ps
curl localhost:8001/predict  # Test from VM
```

### Docker Permission Denied

```bash
# Add user to docker group
sudo usermod -aG docker ubuntu

# Log out and back in
exit
ssh ubuntu@74.234.179.93
```

### Model Not Found

```bash
# Make sure models directory was transferred
ls -la models/

# If missing, transfer again
scp -r models/ ubuntu@74.234.179.93:/home/ubuntu/gma/
```

---

## 🧪 Testing Script

Create `test_cloud.py` on your local machine:

```python
import requests

# Your assigned port
VM_HOST = "74.234.179.93"
VM_PORT = 8001  # Change to your port
BASE_URL = f"http://{VM_HOST}:{VM_PORT}"

# Test GET
response = requests.get(f"{BASE_URL}/predict")
print(f"GET /predict: {response.json()}")

# Test POST
data = {"size": 100, "bedrooms": 3, "garden": 1}
response = requests.post(f"{BASE_URL}/predict", json=data)
print(f"POST /predict: {response.json()}")

print(f"\n✅ Your service is live at: {BASE_URL}")
print(f"📖 Share with friends: {BASE_URL}/docs")
```

---

## 📊 Port Assignment

To avoid conflicts:
- **Port 8001**: First student (gma)
- **Port 8002**: Second student
- **Port 8003**: Third student
- etc.

**Ask trainer for your assigned port!**

---

## ✅ Verification Checklist

- [ ] Connected to VM (74.234.179.93)
- [ ] Created personal folder (/home/ubuntu/gma)
- [ ] Docker installed on VM
- [ ] Files transferred to VM
- [ ] Image built successfully
- [ ] Container running on unique port
- [ ] Accessible from local machine
- [ ] Accessible from browser
- [ ] Friend can access the service
- [ ] Interactive docs working

---

## 🔐 Security Notes

⚠️ **For learning purposes only!**

In production:
- Use SSH keys
- Configure proper firewall rules
- Use HTTPS/SSL certificates
- Implement authentication
- Use container orchestration (Kubernetes)
- Set resource limits
- Use secrets management

---

## 🎓 What You Learned

- ✅ Deploying Docker containers on remote machines
- ✅ Building images on cloud VMs
- ✅ Port mapping for external access
- ✅ Container management on remote servers
- ✅ Testing deployed services
- ✅ Sharing services with others

---

## 📖 Quick Commands Summary

```bash
# Local: Transfer files
scp -r Dockerfile main.py requirements.txt models/ \
  ubuntu@74.234.179.93:/home/ubuntu/gma/

# VM: Build and run
ssh ubuntu@74.234.179.93
cd /home/ubuntu/gma
docker build -t house-price-api:v1 .
docker run -d -p 8001:8000 --name house-api house-price-api:v1

# Local: Test
curl http://74.234.179.93:8001/predict
```

---

**Next**: Level 3 - Automate with CI/CD! 🚀

