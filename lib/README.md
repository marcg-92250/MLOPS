# ML2C - Machine Learning to C Transpiler

Convert scikit-learn models to standalone C code for embedded systems.

## Installation

```bash
# From the MLOPS directory
cd Library
pip install -e .
```

Or simply use it without installation by importing from the directory.

## Quick Start

```python
from Library import transpile_model

# Transpile a model
c_file, binary = transpile_model('my_model.joblib')

# Run the generated binary
# ./my_model_inference
```

## Usage

### Basic Example

```python
from Library import ModelTranspiler

# Load and transpile
transpiler = ModelTranspiler('linear_regression_model.joblib')

# Generate C code
c_code = transpiler.generate_c_code()

# Save to file
transpiler.save('output.c')

# Compile
binary = transpiler.compile('output.c')
```

### With Test Data

```python
import numpy as np
from Library import transpile_model

# Your test data
test_data = np.array([[1.0, 2.0, 3.0]])

# Transpile with test data included
c_file, binary = transpile_model('model.joblib', test_data=test_data)
```

### Using the ModelTranspiler Class

```python
from Library import ModelTranspiler

# Initialize
transpiler = ModelTranspiler('logistic_model.joblib')

# Generate code
c_code = transpiler.generate_c_code()

# Save
c_file = transpiler.save('logistic_inference.c')

# Compile
binary = transpiler.compile(c_file)

# Now run: ./logistic_inference
```

## Supported Models

- ✅ **LinearRegression** - Linear regression models
- ✅ **LogisticRegression** - Binary classification
- ✅ **DecisionTreeClassifier** - Decision tree classification

## API Reference

### `ModelTranspiler(model_path)`

Main class for model transpilation.

**Methods:**
- `generate_c_code(test_data=None)` - Generate C code
- `save(output_file, test_data=None)` - Save C code to file
- `compile(c_file, output_binary=None)` - Compile C code

### `transpile_model(model_path, output_file=None, compile_code=True, test_data=None)`

Quick function to transpile in one line.

**Returns:** `(c_file_path, binary_path)`

## Example Workflow

```python
# 1. Train a model in Python
from sklearn.linear_model import LinearRegression
import joblib
import numpy as np

X = np.random.rand(100, 3)
y = X.sum(axis=1)
model = LinearRegression()
model.fit(X, y)
joblib.dump(model, 'model.joblib')

# 2. Transpile to C
from Library import transpile_model
c_file, binary = transpile_model('model.joblib')

# 3. Generated files:
#    - model_inference.c (C source)
#    - model_inference (executable)

# 4. Deploy to embedded device
```

## Features

- 🚀 **Zero Dependencies** - Generated C code has no external dependencies
- 📦 **Compact** - Small binary size (~15KB)
- ⚡ **Fast** - Native C performance
- 🔧 **Easy to Use** - Simple Python API
- 🎯 **Embedded Ready** - Perfect for microcontrollers

## Requirements

- Python 3.6+
- scikit-learn
- numpy
- joblib
- gcc (for compilation)

## License

Open source - MIT License

