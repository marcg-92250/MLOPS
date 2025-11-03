# Part 0: MLflow Installation

## Method 1: Local Installation (Recommended for development)

```bash
# Install dependencies
pip install -r ../requirements.txt

# Start MLflow server
mlflow server --host 0.0.0.0 --port 5000

# Or use the install script
chmod +x install.sh
./install.sh
```

Access UI at: http://localhost:5000

## Method 2: Docker Installation

```bash
# Using docker-compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f mlflow

# Stop
docker-compose down
```

Access UI at: http://localhost:5000

## Verify Installation

```python
import mlflow
print(f"MLflow version: {mlflow.__version__}")
```

## MLflow UI Overview

The MLflow UI provides:
- **Experiments**: View all experiments and runs
- **Models**: Registered models and versions
- **Artifacts**: Stored files (models, plots, etc.)
- **Metrics**: Performance metrics over time
- **Parameters**: Hyperparameters used

## Next Steps

Once MLflow is running, proceed to Part 1 for model tracking.

