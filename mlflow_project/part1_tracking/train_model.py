#!/usr/bin/env python3
"""
Part 1: MLflow Model Tracking
Train a model and track hyperparameters, metrics, and the model itself.
"""

import mlflow
import mlflow.sklearn
from sklearn.datasets import make_classification, load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import numpy as np
import argparse


def load_dataset(dataset_name="wine"):
    """Load a dataset for training."""
    if dataset_name == "wine":
        data = load_wine()
        X, y = data.data, data.target
    elif dataset_name == "synthetic":
        X, y = make_classification(n_samples=1000, n_features=20, 
                                   n_informative=15, n_redundant=5,
                                   n_classes=3, random_state=42)
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")
    
    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_and_track(n_estimators=100, max_depth=10, min_samples_split=2, 
                   dataset="wine", experiment_name="wine_classification"):
    """Train a model and track everything in MLflow."""
    
    # Set MLflow experiment
    mlflow.set_experiment(experiment_name)
    
    # Start MLflow run
    with mlflow.start_run():
        
        # Log hyperparameters
        params = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "min_samples_split": min_samples_split,
            "dataset": dataset
        }
        mlflow.log_params(params)
        
        # Load data
        print(f"Loading {dataset} dataset...")
        X_train, X_test, y_train, y_test = load_dataset(dataset)
        
        # Log dataset info
        mlflow.log_param("train_samples", len(X_train))
        mlflow.log_param("test_samples", len(X_test))
        mlflow.log_param("n_features", X_train.shape[1])
        mlflow.log_param("n_classes", len(np.unique(y_train)))
        
        # Train model
        print("Training model...")
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Calculate metrics
        train_accuracy = accuracy_score(y_train, y_pred_train)
        test_accuracy = accuracy_score(y_test, y_pred_test)
        test_f1 = f1_score(y_test, y_pred_test, average='weighted')
        test_precision = precision_score(y_test, y_pred_test, average='weighted')
        test_recall = recall_score(y_test, y_pred_test, average='weighted')
        
        # Log metrics
        metrics = {
            "train_accuracy": train_accuracy,
            "test_accuracy": test_accuracy,
            "test_f1_score": test_f1,
            "test_precision": test_precision,
            "test_recall": test_recall
        }
        mlflow.log_metrics(metrics)
        
        # Log the model
        mlflow.sklearn.log_model(
            model, 
            "model",
            registered_model_name=f"{experiment_name}_model"
        )
        
        # Print summary
        print("\n" + "="*50)
        print("Training Complete!")
        print("="*50)
        print(f"\nHyperparameters:")
        for k, v in params.items():
            print(f"  {k}: {v}")
        print(f"\nMetrics:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")
        print(f"\nRun ID: {mlflow.active_run().info.run_id}")
        print(f"Artifact URI: {mlflow.get_artifact_uri()}")
        print("\nCheck MLflow UI at http://localhost:5000")
        print("="*50 + "\n")
        
        return mlflow.active_run().info.run_id


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and track ML model with MLflow")
    parser.add_argument("--n-estimators", type=int, default=100, 
                       help="Number of trees in random forest")
    parser.add_argument("--max-depth", type=int, default=10,
                       help="Maximum depth of trees")
    parser.add_argument("--min-samples-split", type=int, default=2,
                       help="Minimum samples required to split")
    parser.add_argument("--dataset", type=str, default="wine",
                       choices=["wine", "synthetic"],
                       help="Dataset to use")
    parser.add_argument("--experiment", type=str, default="wine_classification",
                       help="MLflow experiment name")
    
    args = parser.parse_args()
    
    # Set MLflow tracking URI
    mlflow.set_tracking_uri("http://localhost:5000")
    
    # Train and track
    run_id = train_and_track(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        min_samples_split=args.min_samples_split,
        dataset=args.dataset,
        experiment_name=args.experiment
    )
    
    print(f"✓ Model tracked successfully! Run ID: {run_id}")

