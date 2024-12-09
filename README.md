# CMPT 439 Final Project

## Installation

1. Create and activate a virtual environment (recommended):

```bash
python3 -m .venv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Function Usage

### Gauss-Jordan Elimination

```python
from src.gauss_jordan import gauss_jordan

coefficients = [
    [3, 1, -4],
    [-2, 3, 1],
    [2, 0, 5]
]
constants = [7, -5, 10]

solution = gauss_jordan(coefficients, constants)
```

## Running Tests

Run tests with code coverage:

```python
pytest --cov=src
```
