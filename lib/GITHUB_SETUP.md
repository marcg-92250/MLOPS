# Setup GitHub Repository

## Étapes pour publier sur GitHub

### 1. Créer un repository sur GitHub

Allez sur https://github.com/new et créez un nouveau repository:
- **Name**: `ml2c-transpiler`
- **Description**: `Transpile scikit-learn models to C code for embedded systems`
- **Public/Private**: Public (recommandé)
- **Ne PAS** initialiser avec README, .gitignore ou license (déjà fait localement)

### 2. Connecter et pousser le code

```bash
cd /home/gma/MLOPS/Library

# Remplacez YOUR_USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/YOUR_USERNAME/ml2c-transpiler.git
git branch -M main
git push -u origin main
```

### 3. Votre lien GitHub sera

```
https://github.com/YOUR_USERNAME/ml2c-transpiler
```

## Alternative: Utiliser le GitHub CLI

```bash
# Installer gh (si pas déjà fait)
# Sur Ubuntu/Debian: sudo apt install gh
# Sur MacOS: brew install gh

# S'authentifier
gh auth login

# Créer et pousser directement
cd /home/gma/MLOPS/Library
gh repo create ml2c-transpiler --public --source=. --remote=origin --push
```

Votre repository sera créé automatiquement et le lien sera:
```
https://github.com/YOUR_USERNAME/ml2c-transpiler
```

## Structure du Repository

```
ml2c-transpiler/
├── __init__.py           # Package initialization
├── transpiler.py         # Core transpiler logic
├── setup.py             # Installation script
├── README.md            # Documentation
├── LICENSE              # MIT License
├── .gitignore           # Git ignore rules
└── example_usage.py     # Usage examples
```

## Badge pour README

Après publication, ajoutez ces badges au README.md:

```markdown
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
```

