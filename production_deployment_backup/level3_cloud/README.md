# Level 3: Cloud Deployment

Deploy the Docker container to a remote virtual machine.

## 📋 Prerequisites

- Access to a cloud VM (provided by trainer)
- SSH credentials
- Docker installed on remote VM

## 🔑 Connection Information

```
Host: [PROVIDED_BY_TRAINER]
User: ubuntu
Password: Supermotdepasse!42
```

## 📝 Steps

### Step 1: Connect via SSH

```bash
ssh ubuntu@YOUR_VM_IP
# Password: Supermotdepasse!42
```

### Step 2: Create Your Folder

```bash
# Use your initials (e.g., td for Tom Dupont)
mkdir /home/ubuntu/YOUR_INITIALS
cd /home/ubuntu/YOUR_INITIALS
```

### Step 3: Deploy Code

**Option A: Using SCP**
```bash
# From your local machine
scp -r ../level2_docker ubuntu@YOUR_VM_IP:/home/ubuntu/YOUR_INITIALS/
```

**Option B: Using Git**
```bash
# On remote VM
cd /home/ubuntu/YOUR_INITIALS
git clone YOUR_REPO_URL
```

### Step 4: Build and Run on VM

```bash
# On remote VM
cd /home/ubuntu/YOUR_INITIALS/level2_docker

# Make sure model is copied
cp -r ../../models .

# Build image
docker build -t house-price-api:latest .

# Run container
docker run -d -p 8000:8000 --name house-api house-price-api:latest
```

### Step 5: Verify Deployment

```bash
# Check container is running
docker ps

# Test from remote VM
curl http://localhost:8000/health

# Test from your machine
curl http://YOUR_VM_IP:8000/health
```

### Step 6: Share with Colleague

Share your VM IP and initials with a colleague:
```
http://YOUR_VM_IP:8000/predict
```

They can test:
```bash
curl -X POST http://YOUR_VM_IP:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"size": 100, "bedrooms": 3, "garden": 1}'
```

## 🚀 Automated Deployment

Use the provided script:

```bash
# Edit deploy.sh with your VM IP and initials
chmod +x deploy.sh
./deploy.sh
```

## 🔧 Manual Deployment Steps

### 1. Prepare locally
```bash
cd level2_docker
docker build -t house-price-api:latest .
docker save -o house-price-api.tar house-price-api:latest
```

### 2. Transfer to VM
```bash
scp house-price-api.tar ubuntu@YOUR_VM_IP:/home/ubuntu/YOUR_INITIALS/
```

### 3. Load and run on VM
```bash
ssh ubuntu@YOUR_VM_IP
cd /home/ubuntu/YOUR_INITIALS
docker load -i house-price-api.tar
docker run -d -p 8000:8000 --name house-api house-price-api:latest
```

## 📊 Container Management

### View logs
```bash
docker logs house-api
docker logs -f house-api  # Follow logs
```

### Restart container
```bash
docker restart house-api
```

### Stop container
```bash
docker stop house-api
```

### Update deployment
```bash
# Stop old container
docker stop house-api
docker rm house-api

# Run new version
docker run -d -p 8000:8000 --name house-api house-price-api:latest
```

## 🌐 Network Configuration

### Check firewall
```bash
# On VM, allow port 8000
sudo ufw allow 8000/tcp
sudo ufw status
```

### Check container network
```bash
docker network inspect bridge
```

## 🧪 Testing

### From VM
```bash
curl http://localhost:8000/health
```

### From your machine
```bash
curl http://YOUR_VM_IP:8000/health
```

### From browser
```
http://YOUR_VM_IP:8000/docs
```

## 🔐 Security Considerations

- ⚠️ Don't expose sensitive ports
- ✅ Use HTTPS in production
- ✅ Implement authentication
- ✅ Use environment variables for secrets
- ✅ Keep Docker and system updated

## 🐛 Troubleshooting

**Can't connect to VM?**
```bash
# Check SSH connection
ssh -v ubuntu@YOUR_VM_IP

# Check if port is open
telnet YOUR_VM_IP 22
```

**Container not accessible from outside?**
```bash
# Check container is running
docker ps

# Check port is exposed
docker port house-api

# Check firewall
sudo ufw status
```

**Permission denied?**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Logout and login again
```

## 🚀 Next Level

Proceed to **Level 4** to automate deployment with CI/CD pipelines.

## 💡 Production Tips

- Use Docker Compose for multi-container setups
- Implement logging and monitoring
- Set up automatic restarts
- Use reverse proxy (nginx) for SSL
- Implement rate limiting
- Set up automated backups

