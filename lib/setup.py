from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ml2c",
    version="1.0.0",
    author="MLOPS Project",
    description="Transpile scikit-learn models to C code for embedded systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ml2c",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.18.0",
        "scikit-learn>=0.22.0",
        "joblib>=0.14.0",
    ],
)

