#!/usr/bin/env python3
"""
Level 0: FastAPI Web Service - Local Machine
Step-by-step implementation
"""

from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI(
    title="House Price Prediction API",
    description="Level 0 - Local Machine",
    version="1.0.0"
)

# Global variable for model
model = None


# ============================================================================
# STEP 1: PREAMBLE - Simple GET endpoint
# ============================================================================

@app.get("/predict")
def predict_get():
    """
    STEP 1 (Preamble): Simple GET endpoint returning {"y_pred": 2}
    
    Test with:
    - Browser: http://localhost:8000/predict
    - curl: curl http://localhost:8000/predict
    - wget: wget -qO- http://localhost:8000/predict
    """
    return {"y_pred": 2}


# ============================================================================
# STEP 3: POST endpoint (will be implemented)
# ============================================================================

# Request model for POST
class HouseRequest(BaseModel):
    size: float
    bedrooms: int
    garden: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "size": 100,
                "bedrooms": 3,
                "garden": 1
            }
        }


# TODO: Implement POST endpoint in Step 3
# TODO: Load model and use it in Step 4


# ============================================================================
# Additional endpoints
# ============================================================================

@app.get("/")
def root():
    """Root endpoint with API info"""
    return {
        "message": "House Price Prediction API - Level 0",
        "status": "Step 1 completed",
        "endpoints": {
            "GET /predict": "Returns {\"y_pred\": 2} (preamble)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 Starting FastAPI Server - Level 0")
    print("="*60)
    print("\nServer: http://localhost:8000")
    print("Docs:   http://localhost:8000/docs")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

