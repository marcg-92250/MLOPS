#!/usr/bin/env python3
"""
Example usage of the ML2C library
"""

import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
import joblib
import sys
import os

# Add library to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from transpiler import ModelTranspiler, transpile_model


def example_linear_regression():
    """Example: Linear Regression"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Linear Regression")
    print("="*60)
    
    # Train a simple model
    X = np.random.rand(100, 3)
    y = 2 + 3*X[:, 0] + 1.5*X[:, 1] - 0.5*X[:, 2]
    
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, 'temp_linear.joblib')
    
    # Transpile
    c_file, binary = transpile_model('temp_linear.joblib')
    
    print(f"✓ Model transpiled to: {c_file}")
    print(f"✓ Binary compiled to: {binary}")
    
    # Test
    test_X = np.array([[1.0, 2.0, 3.0]])
    pred_python = model.predict(test_X)[0]
    print(f"\nPython prediction: {pred_python:.6f}")
    
    # Clean up
    os.remove('temp_linear.joblib')
    

def example_logistic_regression():
    """Example: Logistic Regression"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Logistic Regression")
    print("="*60)
    
    # Train a classification model
    X, y = make_classification(n_samples=200, n_features=4, random_state=42)
    
    model = LogisticRegression()
    model.fit(X, y)
    joblib.dump(model, 'temp_logistic.joblib')
    
    # Transpile with test data
    test_X = X[:1]
    c_file, binary = transpile_model('temp_logistic.joblib', test_data=test_X)
    
    print(f"✓ Model transpiled to: {c_file}")
    print(f"✓ Binary compiled to: {binary}")
    
    pred_python = model.predict_proba(test_X)[0][1]
    print(f"\nPython prediction (probability): {pred_python:.6f}")
    
    # Clean up
    os.remove('temp_logistic.joblib')


def example_decision_tree():
    """Example: Decision Tree"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Decision Tree")
    print("="*60)
    
    # Train a tree model
    X, y = make_classification(n_samples=100, n_features=5, random_state=42)
    
    model = DecisionTreeClassifier(max_depth=3, random_state=42)
    model.fit(X, y)
    joblib.dump(model, 'temp_tree.joblib')
    
    # Transpile using class API
    transpiler = ModelTranspiler('temp_tree.joblib')
    c_file = transpiler.save('tree_model.c')
    binary = transpiler.compile(c_file)
    
    print(f"✓ Model transpiled to: {c_file}")
    print(f"✓ Binary compiled to: {binary}")
    print(f"✓ Tree depth: {model.get_depth()}")
    print(f"✓ Tree leaves: {model.get_n_leaves()}")
    
    # Clean up
    os.remove('temp_tree.joblib')


if __name__ == "__main__":
    print("\n" + "="*60)
    print("ML2C Library - Usage Examples")
    print("="*60)
    
    example_linear_regression()
    example_logistic_regression()
    example_decision_tree()
    
    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60)
    print("\nGenerated files:")
    print("  - temp_linear_inference.c / temp_linear_inference")
    print("  - temp_logistic_inference.c / temp_logistic_inference")
    print("  - tree_model.c / tree_model")
    print()

