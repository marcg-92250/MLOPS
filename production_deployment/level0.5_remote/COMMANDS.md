# Level 0.5 - Quick Command Reference

## 🚀 Quick Start

### 1. Deploy to Remote Machine

```bash
cd /home/gma/MLOPS/production_deployment/level0.5_remote
bash deploy.sh
# Enter password when prompted: Supermotdepasse!42
```

### 2. Connect to Remote Machine

```bash
ssh ubuntu@74.234.179.93
# Password: Supermotdepasse!42
```

### 3. On Remote Machine - First Time Setup

```bash
# Create your folder
cd /home/ubuntu
mkdir -p gma
cd gma

# Receive the deployment (if using SCP from another terminal)
# Or wait for rsync to complete
```

### 4. On Remote Machine - Install Dependencies

```bash
cd /home/ubuntu/gma/deployment/level0_local

# Install packages
pip install fastapi uvicorn joblib scikit-learn numpy pandas
```

### 5. On Remote Machine - Start Service

```bash
# Option A: Foreground (for testing)
uvicorn main:app --host 0.0.0.0 --port 8001

# Option B: Background (persistent)
nohup uvicorn main:app --host 0.0.0.0 --port 8001 > server.log 2>&1 &

# Check it's running
ps aux | grep uvicorn
```

### 6. Test from Your Local Machine

```bash
# Test GET
curl http://74.234.179.93:8001/predict

# Test POST (if implemented)
curl -X POST http://74.234.179.93:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"size": 100, "bedrooms": 3, "garden": 1}'

# Or use the test script
cd /home/gma/MLOPS/production_deployment/level0.5_remote
python test_remote.py
```

---

## 📋 Essential Commands

### Deploy Code (from local machine)

```bash
# Using the script
cd /home/gma/MLOPS/production_deployment/level0.5_remote
bash deploy.sh

# Manual rsync
rsync -avz /home/gma/MLOPS/production_deployment/ \
  ubuntu@74.234.179.93:/home/ubuntu/gma/deployment/

# Manual SCP
scp -r /home/gma/MLOPS/production_deployment/* \
  ubuntu@74.234.179.93:/home/ubuntu/gma/deployment/
```

### SSH to Remote

```bash
ssh ubuntu@74.234.179.93
```

### On Remote: Manage Service

```bash
# Start
uvicorn main:app --host 0.0.0.0 --port 8001

# Start in background
nohup uvicorn main:app --host 0.0.0.0 --port 8001 > server.log 2>&1 &

# Check if running
ps aux | grep uvicorn
netstat -tuln | grep 8001

# View logs
tail -f server.log
tail -f nohup.out

# Stop
pkill -f "uvicorn main:app"

# Restart
pkill -f "uvicorn main:app"
nohup uvicorn main:app --host 0.0.0.0 --port 8001 > server.log 2>&1 &
```

### Test from Local

```bash
# Simple GET
curl http://74.234.179.93:8001/predict

# With browser
firefox http://74.234.179.93:8001/predict

# API docs
firefox http://74.234.179.93:8001/docs

# Python test script
python test_remote.py
```

---

## 🐛 Troubleshooting

### Can't connect to remote

```bash
# Test connection
ping 74.234.179.93

# Verbose SSH
ssh -v ubuntu@74.234.179.93
```

### Service not accessible

```bash
# On remote: check if bound to 0.0.0.0
netstat -tuln | grep 8001

# Should show: 0.0.0.0:8001 (not 127.0.0.1:8001)

# Restart with correct host
uvicorn main:app --host 0.0.0.0 --port 8001
```

### Port in use

```bash
# Check what's using it
lsof -i :8001

# Use different port
uvicorn main:app --host 0.0.0.0 --port 8002
```

### Module not found on remote

```bash
# On remote machine
pip install fastapi uvicorn joblib scikit-learn numpy
```

---

## ✅ Verification Checklist

- [ ] Can SSH to 74.234.179.93
- [ ] Created folder `/home/ubuntu/gma`
- [ ] Deployed code to remote
- [ ] Installed dependencies
- [ ] Started service with `--host 0.0.0.0`
- [ ] Service running on unique port (8001)
- [ ] Can access from local: `curl http://74.234.179.93:8001/predict`
- [ ] Colleague can also access it
- [ ] Returns `{"y_pred": 2}` for GET request

---

## 🎯 URLs to Share

Once deployed, share these with colleagues:

- **API**: http://74.234.179.93:8001/predict
- **Docs**: http://74.234.179.93:8001/docs
- **Health**: http://74.234.179.93:8001/ (if you have root endpoint)

They should be able to access from anywhere!

