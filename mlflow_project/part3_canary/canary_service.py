#!/usr/bin/env python3
"""
Part 3: Canary Deployment Service
FastAPI service with canary deployment for ML models
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import mlflow
import mlflow.sklearn
import numpy as np
import random
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="MLflow Canary Deployment Service",
    description="Model service with canary deployment support",
    version="2.0.0"
)

# Global model variables
current_model = None
next_model = None
current_model_info = {}
next_model_info = {}
canary_ratio = 0.0  # Probability of using next_model (0.0 to 1.0)

# Statistics
stats = {
    "total_predictions": 0,
    "current_model_predictions": 0,
    "next_model_predictions": 0,
    "start_time": datetime.now().isoformat()
}


class PredictionRequest(BaseModel):
    """Request model for predictions"""
    features: List[List[float]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": [[14.23, 1.71, 2.43, 15.6, 127.0, 2.8, 3.06, 0.28, 2.29, 5.64, 1.04, 3.92, 1065.0]]
            }
        }


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    predictions: List[int]
    model_used: str  # "current" or "next"
    model_name: str
    model_version: str


class UpdateModelRequest(BaseModel):
    """Request for updating a model"""
    model_name: str
    version: Optional[int] = None
    run_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "wine_classification_model",
                "version": 2
            }
        }


class CanaryRatioRequest(BaseModel):
    """Request for setting canary ratio"""
    ratio: float = Field(..., ge=0.0, le=1.0, description="Ratio for next model (0.0 to 1.0)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ratio": 0.1
            }
        }


class ModelInfo(BaseModel):
    """Model information"""
    name: str
    version: str
    loaded: bool
    mlflow_uri: str


class CanaryStatus(BaseModel):
    """Canary deployment status"""
    canary_ratio: float
    current_model: Optional[ModelInfo]
    next_model: Optional[ModelInfo]
    statistics: dict


def load_model_from_mlflow(model_name: str = None, version: int = None, 
                           run_id: str = None):
    """Load model from MLflow."""
    try:
        if run_id:
            model_uri = f"runs:/{run_id}/model"
        elif model_name and version:
            model_uri = f"models:/{model_name}/{version}"
        elif model_name:
            model_uri = f"models:/{model_name}/latest"
        else:
            raise ValueError("Must provide either model_name or run_id")
        
        model = mlflow.sklearn.load_model(model_uri)
        
        model_info = {
            "name": model_name or "unknown",
            "version": str(version) if version else "latest",
            "mlflow_uri": model_uri,
            "loaded": True,
            "loaded_at": datetime.now().isoformat()
        }
        
        logger.info(f"✓ Model loaded: {model_uri}")
        return model, model_info
        
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise


@app.on_event("startup")
async def startup_event():
    """Initialize service on startup."""
    global current_model, next_model
    
    logger.info("Starting Canary Deployment Service...")
    mlflow.set_tracking_uri("http://localhost:5000")
    
    logger.info("Service started. Both current and next models are unloaded.")
    logger.info("Use /update-model to load models.")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "MLflow Canary Deployment Service",
        "version": "2.0.0",
        "canary_ratio": canary_ratio,
        "endpoints": {
            "GET /": "This help",
            "GET /health": "Health check",
            "GET /canary-status": "Canary deployment status",
            "POST /predict": "Make predictions (uses canary routing)",
            "POST /update-model": "Update next model",
            "POST /accept-next-model": "Promote next to current",
            "POST /set-canary-ratio": "Set canary routing ratio"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "current_model_loaded": current_model is not None,
        "next_model_loaded": next_model is not None,
        "canary_ratio": canary_ratio
    }


@app.get("/canary-status", response_model=CanaryStatus)
async def get_canary_status():
    """Get detailed canary deployment status"""
    current_info = None
    if current_model:
        current_info = ModelInfo(
            name=current_model_info.get("name", "unknown"),
            version=current_model_info.get("version", "unknown"),
            loaded=True,
            mlflow_uri=current_model_info.get("mlflow_uri", "unknown")
        )
    
    next_info = None
    if next_model:
        next_info = ModelInfo(
            name=next_model_info.get("name", "unknown"),
            version=next_model_info.get("version", "unknown"),
            loaded=True,
            mlflow_uri=next_model_info.get("mlflow_uri", "unknown")
        )
    
    return CanaryStatus(
        canary_ratio=canary_ratio,
        current_model=current_info,
        next_model=next_info,
        statistics=stats
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Make predictions using canary routing.
    Uses next_model with probability = canary_ratio,
    otherwise uses current_model.
    """
    global stats
    
    if current_model is None and next_model is None:
        raise HTTPException(
            status_code=400,
            detail="No models loaded. Use /update-model to load a model."
        )
    
    try:
        X = np.array(request.features)
        
        # Canary routing logic
        use_next = (next_model is not None and 
                   random.random() < canary_ratio)
        
        if use_next:
            # Use next model (canary)
            model = next_model
            model_info = next_model_info
            model_used = "next"
            stats["next_model_predictions"] += 1
        else:
            # Use current model
            if current_model is None:
                # Fallback to next if current is not loaded
                model = next_model
                model_info = next_model_info
                model_used = "next"
                stats["next_model_predictions"] += 1
            else:
                model = current_model
                model_info = current_model_info
                model_used = "current"
                stats["current_model_predictions"] += 1
        
        # Make prediction
        predictions = model.predict(X)
        stats["total_predictions"] += 1
        
        logger.info(f"Prediction made using {model_used} model")
        
        return PredictionResponse(
            predictions=predictions.tolist(),
            model_used=model_used,
            model_name=model_info.get("name", "unknown"),
            model_version=model_info.get("version", "unknown")
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/update-model")
async def update_model(request: UpdateModelRequest):
    """
    Update the NEXT model (canary).
    This does not affect the current model.
    """
    global next_model, next_model_info
    
    try:
        next_model, next_model_info = load_model_from_mlflow(
            model_name=request.model_name,
            version=request.version,
            run_id=request.run_id
        )
        
        logger.info(f"Next model updated to: {next_model_info['mlflow_uri']}")
        
        return {
            "status": "success",
            "message": "Next model updated successfully",
            "model_info": next_model_info,
            "note": "This is the canary model. Use /accept-next-model to promote it to current."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/accept-next-model")
async def accept_next_model():
    """
    Promote next model to current model.
    Both current and next will point to the same model after this.
    """
    global current_model, current_model_info
    
    if next_model is None:
        raise HTTPException(
            status_code=400,
            detail="No next model to accept. Load one with /update-model first."
        )
    
    # Promote next to current
    current_model = next_model
    current_model_info = next_model_info.copy()
    current_model_info["promoted_at"] = datetime.now().isoformat()
    
    logger.info(f"Next model accepted as current: {current_model_info['mlflow_uri']}")
    
    return {
        "status": "success",
        "message": "Next model promoted to current successfully",
        "current_model_info": current_model_info,
        "note": "Both current and next models are now the same. You can update next with a new version."
    }


@app.post("/set-canary-ratio")
async def set_canary_ratio(request: CanaryRatioRequest):
    """
    Set the canary ratio (probability of using next model).
    - 0.0 = 100% current model
    - 0.1 = 90% current, 10% next
    - 0.5 = 50% current, 50% next
    - 1.0 = 100% next model
    """
    global canary_ratio
    
    old_ratio = canary_ratio
    canary_ratio = request.ratio
    
    logger.info(f"Canary ratio updated: {old_ratio} → {canary_ratio}")
    
    current_pct = (1 - canary_ratio) * 100
    next_pct = canary_ratio * 100
    
    return {
        "status": "success",
        "old_ratio": old_ratio,
        "new_ratio": canary_ratio,
        "distribution": {
            "current_model": f"{current_pct:.1f}%",
            "next_model": f"{next_pct:.1f}%"
        }
    }


@app.post("/reset-stats")
async def reset_stats():
    """Reset prediction statistics"""
    global stats
    
    old_stats = stats.copy()
    stats = {
        "total_predictions": 0,
        "current_model_predictions": 0,
        "next_model_predictions": 0,
        "start_time": datetime.now().isoformat()
    }
    
    return {
        "status": "success",
        "message": "Statistics reset",
        "previous_stats": old_stats
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

