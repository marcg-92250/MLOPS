# GitHub Actions Exercises

Before setting up CI/CD, learn GitHub Actions basics.

## 📚 Exercise 5: GitHub Actions

Complete this tutorial first:
https://github.com/lcetinsoy/revision-git/blob/master/exercice5.md

---

## 📖 What You'll Learn

### 1. Basic Workflow Structure

```yaml
name: My First Workflow

on:
  push:
    branches: [main]

jobs:
  hello-world:
    runs-on: ubuntu-latest
    steps:
      - name: Say hello
        run: echo "Hello, GitHub Actions!"
```

### 2. Checkout Code

```yaml
steps:
  - name: Checkout repository
    uses: actions/checkout@v3
  
  - name: List files
    run: ls -la
```

### 3. Run Tests

```yaml
steps:
  - name: Setup Python
    uses: actions/setup-python@v4
    with:
      python-version: '3.11'
  
  - name: Install dependencies
    run: pip install pytest
  
  - name: Run tests
    run: pytest
```

### 4. Use Secrets

```yaml
steps:
  - name: Use secret
    run: echo "Secret value: ${{ secrets.MY_SECRET }}"
```

### 5. Conditional Steps

```yaml
steps:
  - name: Only on main
    if: github.ref == 'refs/heads/main'
    run: echo "This is main branch"
```

---

## 🧪 Practice Exercises

### Exercise 1: Hello World

Create `.github/workflows/hello.yml`:

```yaml
name: Hello World

on: [push]

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - name: Greet
        run: echo "Hello from GitHub Actions!"
```

**Test**: Push and check Actions tab

---

### Exercise 2: Multi-Step Job

```yaml
name: Multi-Step

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Step 1
        run: echo "Step 1"
      
      - name: Step 2
        run: |
          echo "Step 2"
          pwd
          ls -la
      
      - name: Step 3
        run: date
```

---

### Exercise 3: Checkout and Build

```yaml
name: Build Project

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: List files
        run: ls -la
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
```

---

### Exercise 4: Run Tests

```yaml
name: Run Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install pytest requests
      
      - name: Run tests
        run: pytest tests/
```

---

### Exercise 5: Build Docker Image

```yaml
name: Docker Build

on: [push]

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t myapp:latest .
      
      - name: List images
        run: docker images
```

---

### Exercise 6: Use Secrets

```yaml
name: Use Secrets

on: [push]

jobs:
  secret-test:
    runs-on: ubuntu-latest
    steps:
      - name: Login
        run: |
          echo "Username: ${{ secrets.USERNAME }}"
          echo "Token: ***" # Never echo actual secrets!
      
      - name: Use secret in command
        env:
          MY_SECRET: ${{ secrets.MY_SECRET }}
        run: |
          # Secret is available as environment variable
          echo "Secret is set"
```

---

### Exercise 7: Matrix Strategy

```yaml
name: Matrix Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Test
        run: python --version
```

---

### Exercise 8: Conditional Deployment

```yaml
name: Deploy

on:
  push:
    branches: [main, develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to staging
        if: github.ref == 'refs/heads/develop'
        run: echo "Deploying to staging"
      
      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        run: echo "Deploying to production"
```

---

### Exercise 9: Manual Trigger

```yaml
name: Manual Deploy

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: |
          echo "Deploying to ${{ inputs.environment }}"
```

---

### Exercise 10: Artifact Upload

```yaml
name: Build and Upload

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build
        run: |
          mkdir output
          echo "Build result" > output/result.txt
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: build-output
          path: output/
```

---

## ✅ Quiz

After completing exercises, answer:

1. What triggers a workflow?
2. What is a job?
3. What is a step?
4. How do you use secrets?
5. What is `uses` vs `run`?
6. How to make a step conditional?
7. What is a matrix strategy?
8. How to manually trigger a workflow?

---

## 🎓 Answers

1. **Triggers**: `on: push`, `on: pull_request`, `on: schedule`, `workflow_dispatch`
2. **Job**: A set of steps that execute on the same runner
3. **Step**: An individual task within a job
4. **Secrets**: `${{ secrets.SECRET_NAME }}` - set in repo settings
5. **uses**: Use a pre-made action; **run**: Execute shell commands
6. **Conditional**: `if: condition` on step or job
7. **Matrix**: Run job multiple times with different configurations
8. **Manual**: Add `workflow_dispatch` trigger

---

## 📚 Resources

- **Docs**: https://docs.github.com/en/actions
- **Marketplace**: https://github.com/marketplace?type=actions
- **Starter Workflows**: https://github.com/actions/starter-workflows
- **Exercise 5**: https://github.com/lcetinsoy/revision-git/blob/master/exercice5.md

---

**Once you're comfortable with these concepts, proceed to setup the full CI/CD pipeline! 🚀**

