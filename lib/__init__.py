"""
ML2C - Machine Learning to C Transpiler Library
Converts scikit-learn models to standalone C code for embedded systems.
"""

__version__ = "1.0.0"
__author__ = "MLOPS Project"

from .transpiler import ModelTranspiler, transpile_model

__all__ = ['ModelTranspiler', 'transpile_model']

