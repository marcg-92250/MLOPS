# MLflow Model Lifecycle Management Project

This project demonstrates complete ML model lifecycle management using MLflow, including training tracking, model serving, and canary deployment.

## Project Structure

```
mlflow_project/
├── part0_installation/      # MLflow installation scripts
├── part1_tracking/          # Model training and tracking
├── part2_deployment/        # Web service for model serving
├── part3_canary/           # Canary deployment implementation
├── docker-compose.yml       # Docker orchestration
└── README.md               # This file
```

## Parts Overview

### Part 0: MLflow Installation
- Local installation or Docker setup
- MLflow UI access

### Part 1: Model Tracking
- Track hyperparameters
- Track metrics (MSE, accuracy, etc.)
- Version models in MLflow

### Part 2: Model Deployment
- FastAPI web service
- `/predict` endpoint
- `/update-model` endpoint
- Docker containerization

### Part 3: Canary Deployment
- Two model versions: current and next
- Probabilistic routing (p% current, (1-p)% next)
- Model update and acceptance endpoints

## Quick Start

See individual part directories for detailed instructions.

