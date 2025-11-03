# Part 1: Model Tracking with MLflow

This part demonstrates how to track machine learning experiments using MLflow.

## What We Track

1. **Hyperparameters**: Model configuration (n_estimators, max_depth, etc.)
2. **Metrics**: Performance metrics (accuracy, F1, precision, recall)
3. **Models**: The trained model itself
4. **Dataset Info**: Training/test split sizes, features, classes

## Usage

### Step 1.1-1.2: First Training Run

```bash
python train_model.py
```

This will:
- Train a Random Forest classifier on the Wine dataset
- Track all hyperparameters
- Track performance metrics
- Save the model in MLflow

### Step 1.3: Run with Different Hyperparameters

```bash
# Run with 200 trees
python train_model.py --n-estimators 200

# Run with different max depth
python train_model.py --max-depth 15

# Run with multiple parameters
python train_model.py --n-estimators 50 --max-depth 5 --min-samples-split 5
```

### Step 1.4: Verify Model is Saved

Check the MLflow UI at http://localhost:5000:
1. Go to the experiment "wine_classification"
2. Click on any run
3. Scroll to "Artifacts" section
4. You should see the saved model

## All Available Options

```bash
python train_model.py --help

Options:
  --n-estimators INT        Number of trees (default: 100)
  --max-depth INT          Maximum depth (default: 10)
  --min-samples-split INT  Min samples to split (default: 2)
  --dataset STR            Dataset: wine or synthetic (default: wine)
  --experiment STR         Experiment name (default: wine_classification)
```

## Automated Testing

Run all tests automatically:

```bash
chmod +x test_tracking.sh
./test_tracking.sh
```

This will create 3 runs with different hyperparameters for comparison.

## Viewing Results in MLflow UI

1. Open http://localhost:5000
2. Select the "wine_classification" experiment
3. Compare runs side-by-side
4. Sort by metrics to find best model
5. View detailed metrics and parameters for each run

## Expected Output

Each run should show:
- Run ID and timestamp
- All hyperparameters
- Training and test metrics
- Artifact location (model saved)

## Compare Runs

In MLflow UI:
1. Select multiple runs (checkbox)
2. Click "Compare"
3. View parallel coordinates plot
4. Analyze which hyperparameters affect performance

## Next Steps

Proceed to Part 2 to deploy these models as a web service.

