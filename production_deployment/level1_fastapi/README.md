# Level 1: FastAPI Web Service

REST API for house price prediction with GET and POST endpoints.

## 📋 Steps

### Step 1: Preamble - Simple GET Endpoint

✅ Created `/predict` GET endpoint returning `{"y_pred": 2}`

```bash
cd level1_fastapi
uvicorn main:app --reload
```

### Step 2: Test with Different Methods

✅ **Browser**: http://localhost:8000/predict  
✅ **wget**: `wget -qO- http://localhost:8000/predict`  
✅ **curl**: `curl http://localhost:8000/predict`  
✅ **Python requests**: See `test_api.py`  
✅ **GUI clients**: Postman, Insomnia, HTTPie

### Step 3: Modify to Accept POST

✅ POST endpoint implemented with request validation

### Step 4: Integrate House Price Model

✅ Model loaded from `../models/regression.joblib`  
✅ `/predict` POST endpoint uses the actual model

###Step 5: Test with HTTP Client

```bash
python test_api.py
```

## 🚀 Quick Start

```bash
# 1. Make sure model is trained
cd ..
python train_model.py

# 2. Start the API
cd level1_fastapi
uvicorn main:app --reload

# 3. Test the API
python test_api.py
```

## 📡 API Endpoints

### GET `/`
Service information

```bash
curl http://localhost:8000/
```

### GET `/predict` (Preamble)
Simple static response

```bash
curl http://localhost:8000/predict
```

### POST `/predict`
Make a prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"size": 100, "bedrooms": 3, "garden": 1}'
```

### POST `/predict-batch`
Batch predictions

```bash
curl -X POST http://localhost:8000/predict-batch \
  -H "Content-Type: application/json" \
  -d '{
    "houses": [
      {"size": 50, "bedrooms": 1, "garden": 0},
      {"size": 100, "bedrooms": 3, "garden": 1}
    ]
  }'
```

### GET `/health`
Health check

```bash
curl http://localhost:8000/health
```

### GET `/model-info`
Model coefficients and information

```bash
curl http://localhost:8000/model-info
```

## 📚 Interactive Documentation

FastAPI automatically generates interactive docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Automated Tests

```bash
python test_api.py
```

### Manual Tests with curl

```bash
# Simple prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"size": 150, "bedrooms": 4, "garden": 1}'

# Check health
curl http://localhost:8000/health

# Get model info
curl http://localhost:8000/model-info
```

### With Python

```python
import requests

# Make prediction
response = requests.post(
    "http://localhost:8000/predict",
    json={"size": 100, "bedrooms": 3, "garden": 1}
)
print(response.json())
```

## 🐛 Troubleshooting

**Port already in use?**
```bash
uvicorn main:app --reload --port 8001
```

**Model not found?**
```bash
cd ..
python train_model.py
```

**FastAPI not installed?**
```bash
pip install fastapi uvicorn
```

## 🚀 Next Level

Proceed to **Level 2** to containerize this service with Docker.

## 💡 Key Features

- ✅ Input validation with Pydantic
- ✅ Automatic API documentation
- ✅ Batch predictions support
- ✅ Health check endpoint
- ✅ Model information endpoint
- ✅ Error handling
- ✅ CORS support (if needed)

## 📊 Example Responses

**Prediction:**
```json
{
  "predicted_price": 250000.0,
  "features": {
    "size": 100.0,
    "bedrooms": 3,
    "garden": 1
  }
}
```

**Health:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

