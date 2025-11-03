#!/usr/bin/env python3
"""
Part 2: Model Deployment Web Service
FastAPI service to serve ML models from MLflow
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import mlflow
import mlflow.sklearn
import numpy as np
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="MLflow Model Service",
    description="Web service to serve ML models from MLflow",
    version="1.0.0"
)

# Global model variable
current_model = None
current_model_info = {}


class PredictionRequest(BaseModel):
    """Request model for predictions"""
    features: List[List[float]] = Field(..., description="Input features for prediction")
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": [[1.0, 2.0, 3.0, 4.0]]
            }
        }


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    predictions: List[int]
    model_version: str
    model_name: str


class UpdateModelRequest(BaseModel):
    """Request model for updating the model"""
    model_name: str = Field(..., description="Name of the registered model in MLflow")
    version: Optional[int] = Field(None, description="Model version (latest if not specified)")
    run_id: Optional[str] = Field(None, description="Run ID to load model from")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "wine_classification_model",
                "version": 1
            }
        }


class ModelInfo(BaseModel):
    """Model information"""
    model_name: str
    version: str
    loaded: bool
    mlflow_uri: str


def load_model_from_mlflow(model_name: str = None, version: int = None, 
                           run_id: str = None):
    """Load model from MLflow."""
    global current_model, current_model_info
    
    try:
        if run_id:
            # Load from specific run
            model_uri = f"runs:/{run_id}/model"
            logger.info(f"Loading model from run: {run_id}")
            
        elif model_name and version:
            # Load specific version
            model_uri = f"models:/{model_name}/{version}"
            logger.info(f"Loading model: {model_name} version {version}")
            
        elif model_name:
            # Load latest version
            model_uri = f"models:/{model_name}/latest"
            logger.info(f"Loading latest version of model: {model_name}")
            
        else:
            raise ValueError("Must provide either model_name or run_id")
        
        # Load the model
        current_model = mlflow.sklearn.load_model(model_uri)
        
        # Store model info
        current_model_info = {
            "model_name": model_name or "unknown",
            "version": str(version) if version else "latest",
            "model_uri": model_uri,
            "loaded": True
        }
        
        logger.info(f"✓ Model loaded successfully: {model_uri}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        current_model_info = {"loaded": False, "error": str(e)}
        return False


@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    logger.info("Starting Model Service...")
    
    # Try to load default model
    # This will be updated via /update-model endpoint
    mlflow.set_tracking_uri("http://mlflow:5000")
    
    logger.info("Model Service started. Use /update-model to load a model.")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "MLflow Model Service",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This help message",
            "POST /predict": "Make predictions",
            "POST /update-model": "Update the model",
            "GET /model-info": "Get current model information",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": current_model is not None
    }


@app.get("/model-info", response_model=ModelInfo)
async def get_model_info():
    """Get information about the currently loaded model"""
    if not current_model:
        raise HTTPException(status_code=404, detail="No model loaded")
    
    return ModelInfo(
        model_name=current_model_info.get("model_name", "unknown"),
        version=current_model_info.get("version", "unknown"),
        loaded=True,
        mlflow_uri=current_model_info.get("model_uri", "unknown")
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make predictions using the loaded model"""
    if current_model is None:
        raise HTTPException(
            status_code=400, 
            detail="No model loaded. Use /update-model to load a model first."
        )
    
    try:
        # Convert to numpy array
        X = np.array(request.features)
        
        # Make predictions
        predictions = current_model.predict(X)
        
        return PredictionResponse(
            predictions=predictions.tolist(),
            model_version=current_model_info.get("version", "unknown"),
            model_name=current_model_info.get("model_name", "unknown")
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/update-model")
async def update_model(request: UpdateModelRequest):
    """Update the model from MLflow"""
    success = load_model_from_mlflow(
        model_name=request.model_name,
        version=request.version,
        run_id=request.run_id
    )
    
    if success:
        return {
            "status": "success",
            "message": "Model updated successfully",
            "model_info": current_model_info
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load model: {current_model_info.get('error', 'Unknown error')}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

