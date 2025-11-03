# Level 2: Docker Container

Containerize the FastAPI service for consistent deployment.

## 📋 Steps

### 1. Create Dockerfile

✅ Dockerfile created with:
- Python 3.10 base image
- Dependencies installation
- Application code
- Health check
- Expose port 8000

### 2. Build Docker Image

```bash
cd level2_docker

# Copy necessary files
cp ../level1_fastapi/main.py .
cp -r ../models .

# Build image
docker build -t house-price-api:latest .
```

### 3. Run Container

```bash
# Run with port mapping (-p flag)
docker run -p 8000:8000 house-price-api:latest

# Or run in detached mode
docker run -d -p 8000:8000 --name house-api house-price-api:latest
```

### 4. Test the Container

```bash
# Check if running
docker ps

# Test API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"size": 100, "bedrooms": 3, "garden": 1}'
```

## 🐳 Docker Commands

### Build
```bash
docker build -t house-price-api:v1.0 .
```

### Run
```bash
# Basic
docker run -p 8000:8000 house-price-api:v1.0

# With name
docker run -d -p 8000:8000 --name my-api house-price-api:v1.0

# With volume mount (for model updates)
docker run -d -p 8000:8000 \
  -v $(pwd)/../models:/app/models \
  house-price-api:v1.0
```

### Manage
```bash
# List containers
docker ps

# View logs
docker logs house-api

# Stop
docker stop house-api

# Remove
docker rm house-api

# Remove image
docker rmi house-price-api:v1.0
```

## 🎼 Docker Compose

### Start services
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f
```

### Stop services
```bash
docker-compose down
```

### Rebuild
```bash
docker-compose up --build
```

## 📊 Dockerfile Explanation

```dockerfile
FROM python:3.10-slim          # Lightweight Python image
WORKDIR /app                   # Set working directory
COPY requirements.txt .        # Copy dependencies
RUN pip install ...            # Install dependencies
COPY main.py .                 # Copy application
COPY models/ ./models/         # Copy models
EXPOSE 8000                    # Document port
HEALTHCHECK ...                # Container health
CMD ["uvicorn", ...]           # Start command
```

## 🔍 Important Notes

### Port Mapping
- `-p 8000:8000` maps host port 8000 to container port 8000
- `-p 9000:8000` would make it accessible on host port 9000

### Volume Mounts
- `-v $(pwd)/models:/app/models` for dynamic model updates
- Allows updating models without rebuilding image

### Environment Variables
```bash
docker run -e MODEL_PATH=/app/models/regression.joblib ...
```

## 🧪 Testing

```bash
# Health check
curl http://localhost:8000/health

# Prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"size": 150, "bedrooms": 4, "garden": 1}'

# Model info
curl http://localhost:8000/model-info
```

## 🚀 Next Level

Proceed to **Level 3** to deploy this container on a cloud VM.

## 💡 Best Practices

✅ Use multi-stage builds for smaller images  
✅ Include health checks  
✅ Use `.dockerignore` file  
✅ Don't run as root  
✅ Pin dependency versions  
✅ Use environment variables for configuration  

## 🐛 Troubleshooting

**Port already in use?**
```bash
docker run -p 8001:8000 house-price-api:latest
```

**Can't connect to container?**
```bash
# Check container is running
docker ps

# Check logs
docker logs <container_id>

# Inspect network
docker network inspect bridge
```

**Image too large?**
```bash
# Use slim/alpine base
# Remove unnecessary files
# Multi-stage build
```

