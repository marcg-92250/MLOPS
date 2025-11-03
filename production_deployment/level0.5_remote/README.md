# Level 0.5: FastAPI on Remote Machine

Deploy your web service on a remote VM and make it accessible to others.

## 🎯 Objectives

1. Connect via SSH to remote machine
2. Create your personal folder
3. Deploy code using SCP or Git
4. Launch web service on remote machine
5. Test access from multiple locations

---

## 📋 Remote Machine Info

**SSH Access**:
```
Host: 74.234.179.93
User: ubuntu
Password: Supermotdepasse!42
```

**Connection**:
```bash
ssh ubuntu@74.234.179.93
# Password: Supermotdepasse!42
```

---

## 🚀 Deployment Steps

### STEP 1: Connect to Remote Machine

```bash
ssh ubuntu@74.234.179.93
```

Enter password when prompted: `Supermotdepasse!42`

---

### STEP 2: Create Your Folder

```bash
# On the remote machine
cd /home/ubuntu

# Create folder with your initials (example: gma for your case)
mkdir -p gma
cd gma
```

**Note**: Use your initials (e.g., `gma`, `td` for Tom Dupont, etc.)

---

### STEP 3: Deploy Your Code

#### Option A: Using SCP (Simple Copy)

**From your local machine** (new terminal):

```bash
# Navigate to project root
cd /home/gma/MLOPS/production_deployment

# Copy files to remote machine
scp -r level0_local data models train_model.py ubuntu@74.234.179.93:/home/ubuntu/gma/

# Or copy everything
scp -r . ubuntu@74.234.179.93:/home/ubuntu/gma/deployment/
```

#### Option B: Using Git Clone

**On your local machine first**:
```bash
cd /home/gma/MLOPS/production_deployment
git init
git add .
git commit -m "Initial deployment"
# Push to GitHub/GitLab
```

**Then on remote machine**:
```bash
ssh ubuntu@74.234.179.93
cd /home/ubuntu/gma
git clone <your-repo-url> deployment
cd deployment
```

#### Option C: Using rsync (Recommended)

**From your local machine**:
```bash
rsync -avz -e ssh /home/gma/MLOPS/production_deployment/ \
  ubuntu@74.234.179.93:/home/ubuntu/gma/deployment/
```

---

### STEP 4: Launch Web Service on Remote Machine

**On the remote machine**:

```bash
# Navigate to deployment folder
cd /home/ubuntu/gma/deployment/level0_local

# Install dependencies (if needed)
pip install fastapi uvicorn joblib scikit-learn numpy

# Start the service on a specific port
# IMPORTANT: Use a unique port (e.g., 8000 + last 2 digits of your initials)
python main.py

# Or with custom port:
uvicorn main:app --host 0.0.0.0 --port 8001

# Or run in background:
nohup uvicorn main:app --host 0.0.0.0 --port 8001 > server.log 2>&1 &
```

**⚠️ Important**: 
- Use `--host 0.0.0.0` to allow external access
- Choose a unique port to avoid conflicts with colleagues
- Suggested port: `8000 + XX` where XX are your initials (e.g., 8001, 8002, etc.)

---

### STEP 5: Test Access

#### From Your Local Machine

```bash
# Test GET endpoint
curl http://74.234.179.93:8001/predict

# Expected: {"y_pred": 2}

# Test POST endpoint (if implemented)
curl -X POST http://74.234.179.93:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"size": 100, "bedrooms": 3, "garden": 1}'
```

#### From Browser

Open: `http://74.234.179.93:8001/predict`

**API Docs**: `http://74.234.179.93:8001/docs`

#### With Python

```python
import requests

# Your service URL
BASE_URL = "http://74.234.179.93:8001"

# Test GET
response = requests.get(f"{BASE_URL}/predict")
print(response.json())  # {'y_pred': 2}

# Test POST (if implemented)
data = {"size": 100, "bedrooms": 3, "garden": 1}
response = requests.post(f"{BASE_URL}/predict", json=data)
print(response.json())
```

#### Ask a Colleague to Test

Share your service URL:
```
http://74.234.179.93:8001/predict
```

They should be able to access it from anywhere!

---

## 🔍 Verification Checklist

- [ ] Connected to remote machine via SSH
- [ ] Created personal folder (with initials)
- [ ] Deployed code to remote machine
- [ ] Installed dependencies
- [ ] Started web service on unique port
- [ ] Tested GET /predict from local machine
- [ ] Tested from browser
- [ ] Colleague can access the service
- [ ] Service returns correct predictions

---

## 🛠️ Useful Commands

### Check if Service is Running

```bash
# On remote machine
ps aux | grep uvicorn

# Check port usage
netstat -tuln | grep 8001
```

### Stop the Service

```bash
# Find process ID
ps aux | grep uvicorn

# Kill process
kill <PID>

# Or kill all uvicorn processes (careful!)
pkill -f uvicorn
```

### View Logs

```bash
# If running with nohup
tail -f server.log

# Follow logs in real-time
tail -f nohup.out
```

### Restart Service

```bash
# Kill old process
pkill -f "uvicorn main:app"

# Start new one
nohup uvicorn main:app --host 0.0.0.0 --port 8001 > server.log 2>&1 &
```

---

## 🐛 Troubleshooting

### Can't Connect via SSH

```bash
# Check SSH connection
ping 74.234.179.93

# Verbose SSH output
ssh -v ubuntu@74.234.179.93
```

### Port Already in Use

```bash
# Check what's using the port
lsof -i :8001

# Use a different port
uvicorn main:app --host 0.0.0.0 --port 8002
```

### Service Not Accessible from Outside

**Check firewall**:
```bash
# On remote machine
sudo ufw status

# If firewall is blocking, allow port (ask trainer first)
sudo ufw allow 8001
```

**Check if binding to all interfaces**:
```bash
# Make sure you use --host 0.0.0.0
uvicorn main:app --host 0.0.0.0 --port 8001
```

### Module Not Found

```bash
# Install Python packages
pip install fastapi uvicorn joblib scikit-learn numpy pandas

# Or use requirements.txt
pip install -r requirements.txt
```

---

## 📝 Quick Deployment Script

Create `deploy_remote.sh` on your local machine:

```bash
#!/bin/bash
REMOTE="ubuntu@74.234.179.93"
REMOTE_DIR="/home/ubuntu/gma/deployment"
LOCAL_DIR="/home/gma/MLOPS/production_deployment"

echo "Deploying to remote machine..."
rsync -avz -e ssh $LOCAL_DIR/ $REMOTE:$REMOTE_DIR/
echo "Deployment complete!"
echo "Now SSH to remote and start the service"
```

---

## 🎯 Success Criteria

✅ Service running on remote machine  
✅ Accessible via public IP  
✅ You can get predictions from your laptop  
✅ A colleague can access it from their machine  
✅ Service persists (runs in background)

---

## 📊 Port Assignment Strategy

To avoid conflicts with colleagues:
- Port 8001: First student
- Port 8002: Second student  
- Port 8003: Third student
- etc.

**Ask trainer for your assigned port!**

---

## 🔐 Security Notes

⚠️ **This is for learning purposes only!**

In production, you should:
- Use SSH keys instead of passwords
- Set up proper firewall rules
- Use environment variables for secrets
- Implement authentication/authorization
- Use HTTPS with SSL certificates
- Run services with process managers (systemd, supervisor)

---

**Next**: Let's deploy together! 🚀

