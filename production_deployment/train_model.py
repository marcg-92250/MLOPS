#!/usr/bin/env python3
"""
Train a simple house price prediction model
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

print("="*60)
print("Training House Price Prediction Model")
print("="*60)

# Load data
df = pd.read_csv('data/houses.csv')
print(f"\n✓ Dataset loaded: {len(df)} samples")
print(f"  Columns: {list(df.columns)}")

# Prepare features and target
X = df[['size', 'bedrooms', 'garden']]
y = df['price']

# Train model
model = LinearRegression()
model.fit(X, y)

print(f"\n✓ Model trained")
print(f"  Intercept: {model.intercept_:.2f}")
print(f"  Coefficients: {model.coef_}")

# Test prediction
test_house = [[100, 3, 1]]  # 100m², 3 bedrooms, has garden
prediction = model.predict(test_house)[0]
print(f"\n✓ Test prediction:")
print(f"  Input: 100m², 3 bedrooms, garden")
print(f"  Predicted price: ${prediction:,.2f}")

# Save model
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/house_model.joblib')
print(f"\n✓ Model saved to: models/house_model.joblib")
print("="*60)
