"""
Core transpiler module for converting ML models to C code.
"""

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import subprocess
import os


class ModelTranspiler:
    """Transpile scikit-learn models to C code."""
    
    def __init__(self, model_path):
        """Load model from joblib file."""
        self.model = joblib.load(model_path)
        self.model_type = type(self.model).__name__
    
    def generate_c_code(self, test_data=None):
        """Generate C code for the model."""
        if isinstance(self.model, LinearRegression):
            return self._generate_linear_code(test_data)
        elif isinstance(self.model, LogisticRegression):
            return self._generate_logistic_code(test_data)
        elif isinstance(self.model, DecisionTreeClassifier):
            return self._generate_tree_code(test_data)
        else:
            raise ValueError(f"Model type {self.model_type} not supported")
    
    def _generate_linear_code(self, test_data):
        """Generate C code for linear regression."""
        intercept = self.model.intercept_
        coef = self.model.coef_
        n_features = len(coef)
        
        code = "#include <stdio.h>\n\n"
        code += "float prediction(float *features, int n_features) {\n"
        code += f"    float result = {intercept:.10f}f;\n"
        for i, c in enumerate(coef):
            code += f"    result += {c:.10f}f * features[{i}];\n"
        code += "    return result;\n}\n\n"
        code += self._generate_main(test_data, n_features)
        return code
    
    def _generate_logistic_code(self, test_data):
        """Generate C code for logistic regression."""
        intercept = self.model.intercept_[0]
        coef = self.model.coef_[0]
        n_features = len(coef)
        
        code = "#include <stdio.h>\n#include <math.h>\n\n"
        code += "float sigmoid(float x) {\n"
        code += "    return 1.0f / (1.0f + expf(-x));\n}\n\n"
        code += "float prediction(float *features, int n_features) {\n"
        code += f"    float z = {intercept:.10f}f;\n"
        for i, c in enumerate(coef):
            code += f"    z += {c:.10f}f * features[{i}];\n"
        code += "    return sigmoid(z);\n}\n\n"
        code += self._generate_main(test_data, n_features)
        return code
    
    def _generate_tree_code(self, test_data):
        """Generate C code for decision tree."""
        tree = self.model.tree_
        n_features = self.model.n_features_in_
        
        code = "#include <stdio.h>\n\n"
        code += "float prediction(float *features, int n_features) {\n"
        code += self._generate_tree_node(tree, 0, 1)
        code += "}\n\n"
        code += self._generate_main(test_data, n_features)
        return code
    
    def _generate_tree_node(self, tree, node_id, indent):
        """Recursively generate tree node code."""
        indent_str = "    " * indent
        
        if tree.children_left[node_id] == tree.children_right[node_id]:
            # Leaf node
            value = tree.value[node_id][0]
            predicted_class = np.argmax(value)
            return f"{indent_str}return {predicted_class}.0f;\n"
        
        # Decision node
        feature = tree.feature[node_id]
        threshold = tree.threshold[node_id]
        left = tree.children_left[node_id]
        right = tree.children_right[node_id]
        
        code = f"{indent_str}if (features[{feature}] <= {threshold:.10f}f) {{\n"
        code += self._generate_tree_node(tree, left, indent + 1)
        code += f"{indent_str}}} else {{\n"
        code += self._generate_tree_node(tree, right, indent + 1)
        code += f"{indent_str}}}\n"
        return code
    
    def _generate_main(self, test_data, n_features):
        """Generate main function with test data."""
        code = "int main() {\n"
        
        if test_data is None:
            test_data = np.ones(n_features)
        
        if len(test_data.shape) == 1:
            test_data = test_data.reshape(1, -1)
        
        for idx, sample in enumerate(test_data):
            code += f"    float test_{idx}[] = {{"
            code += ", ".join([f"{v:.6f}f" for v in sample])
            code += "};\n"
        
        for idx in range(len(test_data)):
            code += f"    float pred_{idx} = prediction(test_{idx}, {n_features});\n"
        
        code += '    printf("C Predictions:\\n");\n'
        for idx in range(len(test_data)):
            code += f'    printf("  Test {idx}: %f\\n", pred_{idx});\n'
        
        code += "    return 0;\n}\n"
        return code
    
    def save(self, output_file, test_data=None):
        """Save generated C code to file."""
        code = self.generate_c_code(test_data)
        with open(output_file, 'w') as f:
            f.write(code)
        return output_file
    
    def compile(self, c_file, output_binary=None):
        """Compile C code to binary."""
        if output_binary is None:
            output_binary = c_file.replace('.c', '')
        
        cmd = f"gcc -o {output_binary} {c_file} -lm"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return output_binary
        else:
            raise RuntimeError(f"Compilation failed: {result.stderr}")


def transpile_model(model_path, output_file=None, compile_code=True, test_data=None):
    """
    Quick function to transpile a model.
    
    Args:
        model_path: Path to .joblib model file
        output_file: Output C file (default: auto-generated)
        compile_code: Whether to compile the C code
        test_data: Optional test data array
    
    Returns:
        tuple: (c_file, binary_file or None)
    """
    transpiler = ModelTranspiler(model_path)
    
    if output_file is None:
        base = os.path.splitext(os.path.basename(model_path))[0]
        output_file = f"{base}_inference.c"
    
    c_file = transpiler.save(output_file, test_data)
    binary_file = None
    
    if compile_code:
        try:
            binary_file = transpiler.compile(c_file)
        except RuntimeError as e:
            print(f"Warning: {e}")
    
    return c_file, binary_file

