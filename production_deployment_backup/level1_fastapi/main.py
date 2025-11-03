#!/usr/bin/env python3
"""
Level 1: FastAPI Web Service for House Price Prediction
Preamble + Full Implementation
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import joblib
import numpy as np
import os

# Initialize FastAPI app
app = FastAPI(
    title="House Price Prediction API",
    description="REST API for house price prediction using ML model",
    version="1.0.0"
)

# Global model variable
model = None

# Request/Response models
class HouseFeatures(BaseModel):
    """House features for prediction"""
    size: float = Field(..., gt=0, description="Size in m²")
    bedrooms: int = Field(..., gt=0, le=10, description="Number of bedrooms")
    garden: int = Field(..., ge=0, le=1, description="Has garden (0 or 1)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "size": 100.0,
                "bedrooms": 3,
                "garden": 1
            }
        }

class PredictionResponse(BaseModel):
    """Prediction response"""
    predicted_price: float
    features: dict

class BatchPredictionRequest(BaseModel):
    """Batch prediction request"""
    houses: List[HouseFeatures]

class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    predictions: List[float]
    count: int


# Load model on startup
@app.on_event("startup")
async def load_model():
    """Load the trained model"""
    global model
    model_path = '../models/regression.joblib'
    
    if not os.path.exists(model_path):
        print(f"WARNING: Model not found at {model_path}")
        print("Run train_model.py to generate the model")
    else:
        model = joblib.load(model_path)
        print("✓ Model loaded successfully")


# PREAMBLE: Simple GET endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "House Price Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This message",
            "GET /predict": "Simple prediction (preamble)",
            "POST /predict": "Make prediction",
            "POST /predict-batch": "Batch predictions",
            "GET /health": "Health check",
            "GET /model-info": "Model information"
        }
    }


# STEP 1: Simple GET /predict (preamble)
@app.get("/predict")
async def predict_get():
    """
    Simple GET endpoint returning static JSON
    (Preamble step)
    """
    return {"y_pred": 2}


# STEP 3-4: POST /predict with model
@app.post("/predict", response_model=PredictionResponse)
async def predict_post(house: HouseFeatures):
    """
    Make a house price prediction
    
    Args:
        house: House features (size, bedrooms, garden)
    
    Returns:
        Predicted price
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first."
        )
    
    try:
        # Prepare features
        features = np.array([[house.size, house.bedrooms, house.garden]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        return PredictionResponse(
            predicted_price=float(prediction),
            features={
                "size": house.size,
                "bedrooms": house.bedrooms,
                "garden": house.garden
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict-batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """
    Make predictions for multiple houses
    
    Args:
        request: List of house features
    
    Returns:
        List of predicted prices
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )
    
    try:
        # Prepare all features
        features_list = [
            [h.size, h.bedrooms, h.garden]
            for h in request.houses
        ]
        features = np.array(features_list)
        
        # Make predictions
        predictions = model.predict(features)
        
        return BatchPredictionResponse(
            predictions=predictions.tolist(),
            count=len(predictions)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.get("/model-info")
async def model_info():
    """Get model information"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        return {
            "model_type": "Linear Regression",
            "features": ["size", "bedrooms", "garden"],
            "coefficients": {
                "size": float(model.coef_[0]),
                "bedrooms": float(model.coef_[1]),
                "garden": float(model.coef_[2])
            },
            "intercept": float(model.intercept_)
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

