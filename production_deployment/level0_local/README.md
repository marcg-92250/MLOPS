# Level 0: FastAPI on Local Machine

Deploy a web service running a machine learning model on your local machine.

## 🎯 Objectives

1. ✅ Create FastAPI server with GET /predict
2. ✅ Test with multiple HTTP clients
3. ⏳ Modify to accept POST requests
4. ⏳ Integrate house price prediction model
5. ⏳ Test the complete API

## 📋 Steps

### Prerequisites

```bash
# Install dependencies
pip install fastapi uvicorn scikit-learn pandas joblib requests
```

### STEP 0: Train the Model

```bash
cd /home/gma/MLOPS/production_deployment
python train_model.py
```

This creates `models/house_model.joblib`.

---

### ✅ STEP 1: Preamble - Simple GET Endpoint

**File**: `main.py`

```python
@app.get("/predict")
def predict_get():
    return {"y_pred": 2}
```

**Start the server**:
```bash
cd level0_local
python main.py
# Or: uvicorn main:app --reload
```

**Expected output**:
```
🚀 Starting FastAPI Server - Level 0
Server: http://localhost:8000
```

---

### ✅ STEP 2: Test the Server

#### Method 1: Browser
Open: http://localhost:8000/predict

**Expected**: `{"y_pred":2}`

#### Method 2: curl
```bash
curl http://localhost:8000/predict
```

#### Method 3: wget
```bash
wget -qO- http://localhost:8000/predict
```

#### Method 4: Python requests
```python
import requests
response = requests.get("http://localhost:8000/predict")
print(response.json())  # {'y_pred': 2}
```

#### Method 5: GUI HTTP Clients

**Postman**:
1. New Request → GET
2. URL: `http://localhost:8000/predict`
3. Send

**Insomnia**:
1. New Request → GET
2. URL: `http://localhost:8000/predict`
3. Send

**HTTPie** (command line):
```bash
http GET localhost:8000/predict
```

---

### ⏳ STEP 3: Add POST Endpoint

**TODO**: Modify `main.py` to accept POST requests.

```python
@app.post("/predict")
def predict_post(house: HouseRequest):
    # Will be implemented together
    pass
```

---

### ⏳ STEP 4: Integrate the Model

**TODO**: Load model and use it for predictions.

```python
@app.on_event("startup")
def load_model():
    global model
    model = joblib.load('../models/house_model.joblib')

@app.post("/predict")
def predict_post(house: HouseRequest):
    features = np.array([[house.size, house.bedrooms, house.garden]])
    prediction = model.predict(features)[0]
    return {"predicted_price": float(prediction)}
```

---

### ⏳ STEP 5: Test with POST

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"size": 100, "bedrooms": 3, "garden": 1}'
```

---

## 🔍 Verification Checklist

- [ ] STEP 1: GET /predict returns {"y_pred": 2}
- [ ] STEP 2: Tested with browser
- [ ] STEP 2: Tested with wget
- [ ] STEP 2: Tested with curl
- [ ] STEP 2: Tested with GUI client (Postman/Insomnia)
- [ ] STEP 2: Tested with Python requests
- [ ] STEP 3: POST endpoint implemented
- [ ] STEP 4: Model loaded and integrated
- [ ] STEP 5: Tested POST with predictions

## 📚 Interactive Documentation

FastAPI auto-generates interactive docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐛 Troubleshooting

**Port 8000 already in use?**
```bash
# Use a different port
uvicorn main:app --port 8001
```

**Module not found?**
```bash
pip install fastapi uvicorn
```

**Model not found?**
```bash
# Train the model first
cd ..
python train_model.py
```

## ✅ Current Status

- ✅ **STEP 1 DONE**: Simple GET endpoint created
- ⏳ **STEP 2 IN PROGRESS**: Ready to test together
- ⏸️  **STEP 3-5**: Waiting

---

**Next**: Let's test STEP 1 & 2 together! 🚀

