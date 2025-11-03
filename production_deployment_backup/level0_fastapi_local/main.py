#!/usr/bin/env python3
"""
Level 0: FastAPI Web Service - Local Machine
Complete implementation with all steps
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import joblib
import numpy as np
import os

# Initialize FastAPI app
app = FastAPI(
    title="House Price Prediction API - Level 0",
    description="REST API for house price prediction",
    version="1.0.0"
)

# Global model variable
model = None


# ============================================================================
# STEP 1: PREAMBLE - Simple GET endpoint returning static JSON
# ============================================================================

@app.get("/predict")
async def predict_get():
    """
    STEP 1 (Preamble): Simple GET endpoint returning {"y_pred": 2}
    
    Test with:
    - Browser: http://localhost:8000/predict
    - curl: curl http://localhost:8000/predict
    - wget: wget -qO- http://localhost:8000/predict
    """
    return {"y_pred": 2}


# ============================================================================
# STEP 3: Add POST endpoint
# ============================================================================

# Request model for POST
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


# Response model
class PredictionResponse(BaseModel):
    """Prediction response"""
    predicted_price: float
    features: dict


# ============================================================================
# STEP 4: Integrate the house prediction model
# ============================================================================

@app.on_event("startup")
async def load_model():
    """Load the trained model on startup"""
    global model
    model_path = '../models/regression.joblib'
    
    if not os.path.exists(model_path):
        print(f"⚠️  WARNING: Model not found at {model_path}")
        print("   Run: python train_model.py")
    else:
        model = joblib.load(model_path)
        print("✓ Model loaded successfully")


@app.post("/predict", response_model=PredictionResponse)
async def predict_post(house: HouseFeatures):
    """
    STEP 3-4: POST endpoint using the trained model
    
    Test with curl:
    curl -X POST http://localhost:8000/predict \
      -H "Content-Type: application/json" \
      -d '{"size": 100, "bedrooms": 3, "garden": 1}'
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Run train_model.py first."
        )
    
    try:
        # Prepare features as numpy array
        features = np.array([[house.size, house.bedrooms, house.garden]])
        
        # Make prediction with the model
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
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )


# ============================================================================
# Additional helpful endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "House Price Prediction API - Level 0",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This help message",
            "GET /predict": "Simple prediction (returns y_pred=2)",
            "POST /predict": "Make real prediction with model",
            "GET /health": "Health check",
            "GET /model-info": "Model information",
            "GET /docs": "Interactive API documentation"
        },
        "test_with": [
            "Browser: http://localhost:8000/predict",
            "curl: curl http://localhost:8000/predict",
            "wget: wget -qO- http://localhost:8000/predict",
            "Python requests: see test_api.py",
            "GUI: Postman, Insomnia, HTTPie"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.get("/model-info")
async def model_info():
    """Get model coefficients and information"""
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )
    
    try:
        return {
            "model_type": "Linear Regression",
            "features": ["size (m²)", "bedrooms", "garden (0/1)"],
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
# Run the server
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("Starting FastAPI Server - Level 0")
    print("=" * 60)
    print("\nAccess the API at: http://localhost:8000")
    print("Interactive docs at: http://localhost:8000/docs")
    print("\n" + "=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

