# Part 2: Model Deployment Web Service

Deploy ML models from MLflow as a web service using FastAPI.

## Features

- ✅ Load models from MLflow at runtime
- ✅ `/predict` endpoint for predictions
- ✅ `/update-model` endpoint to change model version
- ✅ `/model-info` endpoint for model information
- ✅ Docker containerization
- ✅ No COPY of model in Dockerfile (loads from MLflow)

## Local Development

### 1. Start MLflow Server

```bash
# In one terminal
cd ../part0_installation
mlflow server --host 0.0.0.0 --port 5000
```

### 2. Train a Model (if not done)

```bash
# In another terminal
cd ../part1_tracking
python train_model.py
```

### 3. Start the Model Service

```bash
cd ../part2_deployment
pip install -r requirements.txt
uvicorn model_service:app --reload
```

Access at: http://localhost:8000

### 4. Test the Service

```bash
python test_service.py
```

## API Endpoints

### GET /
Service information and available endpoints

### GET /health
Health check

```bash
curl http://localhost:8000/health
```

### GET /model-info
Get current model information

```bash
curl http://localhost:8000/model-info
```

### POST /update-model
Update the loaded model

```bash
# Load latest version
curl -X POST http://localhost:8000/update-model \
  -H "Content-Type: application/json" \
  -d '{"model_name": "wine_classification_model"}'

# Load specific version
curl -X POST http://localhost:8000/update-model \
  -H "Content-Type: application/json" \
  -d '{"model_name": "wine_classification_model", "version": 1}'

# Load from run ID
curl -X POST http://localhost:8000/update-model \
  -H "Content-Type: application/json" \
  -d '{"run_id": "YOUR_RUN_ID"}'
```

### POST /predict
Make predictions

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[14.23, 1.71, 2.43, 15.6, 127.0, 2.8, 3.06, 0.28, 2.29, 5.64, 1.04, 3.92, 1065.0]]}'
```

## Docker Deployment

### Build and Run with Docker Compose

```bash
docker-compose up --build
```

This starts both:
- MLflow server on port 5000
- Model service on port 8000

### Test Docker Deployment

```bash
# Update model
curl -X POST http://localhost:8000/update-model \
  -H "Content-Type: application/json" \
  -d '{"model_name": "wine_classification_model"}'

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[14.23, 1.71, 2.43, 15.6, 127.0, 2.8, 3.06, 0.28, 2.29, 5.64, 1.04, 3.92, 1065.0]]}'
```

### Stop Services

```bash
docker-compose down
```

## Important Notes

### Why No COPY in Dockerfile?

The Dockerfile does NOT copy the model file because:
1. Models are loaded dynamically from MLflow at runtime
2. Allows updating models without rebuilding the container
3. Follows MLOps best practices for model versioning

### Model Loading Flow

1. Service starts (no model loaded)
2. Call `/update-model` with model name/version
3. Service fetches model from MLflow server
4. Model is ready for predictions
5. Can update to new version anytime with another `/update-model` call

## Automated Testing

The `test_service.py` script tests:
- Health endpoint
- Model update endpoint
- Model info endpoint
- Prediction endpoint
- Complete update workflow

Run with:
```bash
python test_service.py
```

## Interactive API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Next Steps

Proceed to Part 3 for canary deployment implementation.

