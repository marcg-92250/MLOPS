#!/usr/bin/env python3
"""
Train a simple regression model for house price prediction
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

def train_house_price_model():
    """Train and save the house price prediction model"""
    
    print("=" * 60)
    print("Training House Price Prediction Model")
    print("=" * 60)
    
    # Load data
    print("\n1. Loading data...")
    df = pd.read_csv('data/houses.csv')
    print(f"   Dataset shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    
    # Prepare features and target
    X = df[['size', 'bedrooms', 'garden']]
    y = df['price']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    # Train model
    print("\n2. Training model...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate
    print("\n3. Evaluating model...")
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    train_mse = mean_squared_error(y_train, y_pred_train)
    test_mse = mean_squared_error(y_test, y_pred_test)
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    
    print(f"   Train MSE: {train_mse:.2f}")
    print(f"   Test MSE: {test_mse:.2f}")
    print(f"   Train R²: {train_r2:.4f}")
    print(f"   Test R²: {test_r2:.4f}")
    
    # Show coefficients
    print("\n4. Model coefficients:")
    print(f"   Intercept: {model.intercept_:.2f}")
    for feature, coef in zip(['size', 'bedrooms', 'garden'], model.coef_):
        print(f"   {feature}: {coef:.2f}")
    
    # Save model
    print("\n5. Saving model...")
    os.makedirs('models', exist_ok=True)
    model_path = 'models/regression.joblib'
    joblib.dump(model, model_path)
    print(f"   Model saved to: {model_path}")
    
    # Test prediction
    print("\n6. Test prediction:")
    test_house = [[100, 3, 1]]  # 100m², 3 bedrooms, has garden
    prediction = model.predict(test_house)[0]
    print(f"   House: 100m², 3 bedrooms, garden")
    print(f"   Predicted price: ${prediction:,.2f}")
    
    print("\n" + "=" * 60)
    print("✓ Model training complete!")
    print("=" * 60)
    
    return model

if __name__ == "__main__":
    train_house_price_model()

