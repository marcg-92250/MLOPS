# Installation Guide

## Method 1: Direct Use (No Installation)

```python
# From any Python script
import sys
sys.path.insert(0, '/path/to/MLOPS/Library')

from transpiler import transpile_model

# Use the library
c_file, binary = transpile_model('model.joblib')
```

## Method 2: Install as Package

```bash
cd /home/gma/MLOPS/Library
pip install -e .
```

Then use anywhere:

```python
from Library import transpile_model
c_file, binary = transpile_model('model.joblib')
```

## Method 3: System-wide Installation

```bash
cd /home/gma/MLOPS/Library
pip install .
```

Or from GitHub (after publishing):

```bash
pip install git+https://github.com/YOUR_USERNAME/ml2c-transpiler.git
```

## Requirements

The library will automatically install:
- numpy >= 1.18.0
- scikit-learn >= 0.22.0
- joblib >= 0.14.0

You also need GCC installed for C compilation:

```bash
# Ubuntu/Debian
sudo apt install gcc

# MacOS
xcode-select --install

# Windows
# Install MinGW or use WSL
```

## Verify Installation

```python
from Library import ModelTranspiler
print("ML2C Library installed successfully!")
```

