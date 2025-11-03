# Model Deployment in Production

Progressive deployment project from local to cloud with CI/CD automation.

## 🎯 Project Overview

This project demonstrates different approaches to deploy ML models in production:
- **Streamlit**: Interactive web app
- **FastAPI**: REST API web service
- **Docker**: Containerization
- **Cloud**: VM deployment
- **CI/CD**: Automated deployment pipeline

## 📁 Project Structure

```
production_deployment/
├── level0_streamlit/        # Streamlit app
├── level1_fastapi/          # FastAPI web service
├── level2_docker/           # Docker containerization
├── level3_cloud/            # Cloud deployment scripts
├── level4_cicd/             # CI/CD pipelines
├── data/                    # Dataset
│   └── houses.csv
├── models/                  # Trained models
│   └── regression.joblib
└── README.md
```

## 🚀 Quick Start

Each level builds on the previous one. Start with Level 0 and progress through the levels.

### Prerequisites

```bash
pip install -r requirements.txt
```

## 📊 Deployment Strategies

### Batch Processing
- ✅ Simple to set up
- ✅ Handles large datasets efficiently
- ❌ No real-time predictions
- ❌ High latency

### Web Services
- ✅ Real-time predictions
- ✅ RESTful API
- ❌ Can suffer under heavy load
- ❌ Requires elastic infrastructure

### Streaming Systems
- ✅ Real-time processing
- ✅ Handles high throughput
- ❌ Complex setup
- ❌ Requires specialized infrastructure

**This project focuses on Web Services deployment.**

## 📝 Levels Overview

### Level 0: Streamlit App
Simple interactive web application for model predictions.

### Level 1: FastAPI Service (Local)
RESTful API with GET/POST endpoints for predictions.

### Level 2: Docker Container (Local)
Containerized web service for consistent deployment.

### Level 3: Cloud Deployment
Deploy Docker container to cloud VM.

### Level 4: CI/CD Pipeline
Automated build, test, and deployment with GitHub Actions.

## 🎓 Learning Objectives

- Understand different deployment strategies
- Build REST APIs with FastAPI
- Containerize applications with Docker
- Deploy to cloud infrastructure
- Implement CI/CD pipelines
- Monitor and maintain production models

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🏆 Bonus: Level 5

Adapt the deployment for more complex models:
- Image classification models
- Hugging Face transformers (BERT, T5)
- Custom trained models

---

**Start with Level 0 and work your way up!**

