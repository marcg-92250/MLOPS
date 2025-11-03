#!/usr/bin/env python3
"""
Level 1: FastAPI Web Service - Dockerized
Complete implementation with model
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
import os

# Create FastAPI app
app = FastAPI(
    title="House Price Prediction API - Docker",
    description="Level 1 - Dockerized Service",
    version="1.0.0"
)

# Global variable for model
model = None


# ============================================================================
# Request/Response Models
# ============================================================================

class HouseRequest(BaseModel):
    """House features for prediction"""
    size: float = Field(..., gt=0, description="Size in m²")
    bedrooms: int = Field(..., gt=0, le=10, description="Number of bedrooms")
    garden: int = Field(..., ge=0, le=1, description="Has garden (0=no, 1=yes)")
    
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
    input_features: dict


# ============================================================================
# Startup: Load Model
# ============================================================================

@app.on_event("startup")
async def load_model():
    """Load the trained model on startup"""
    global model
    model_path = 'models/house_model.joblib'
    
    if not os.path.exists(model_path):
        print(f"⚠️  WARNING: Model not found at {model_path}")
    else:
        model = joblib.load(model_path)
        print("✅ Model loaded successfully")


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "House Price Prediction API - Docker",
        "version": "1.0.0",
        "level": "Level 1 - Dockerized",
        "status": "running",
        "model_loaded": model is not None,
        "endpoints": {
            "GET /": "This help message",
            "GET /health": "Health check",
            "GET /predict": "Simple prediction (returns y_pred=2)",
            "POST /predict": "Make real prediction",
            "GET /docs": "Interactive API documentation"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.get("/predict")
async def predict_get():
    """
    Simple GET endpoint (preamble)
    Returns static value for testing
    """
    return {"y_pred": 2}


@app.post("/predict", response_model=PredictionResponse)
async def predict_post(house: HouseRequest):
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
            detail="Model not loaded. Please check server logs."
        )
    
    try:
        # Prepare features as numpy array
        features = np.array([[house.size, house.bedrooms, house.garden]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        return PredictionResponse(
            predicted_price=float(prediction),
            input_features={
                "size": house.size,
                "bedrooms": house.bedrooms,
                "garden": house.garden
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )


@app.get("/model-info")
async def model_info():
    """Get model information"""
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )
    
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


# ============================================================================
# Run locally (not used in Docker)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 Starting FastAPI Server")
    print("="*60)
    print("\nServer: http://localhost:8000")
    print("Docs:   http://localhost:8000/docs")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

