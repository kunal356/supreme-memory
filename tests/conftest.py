# tests/conftest.py
import os
import sys

# Add the parent directory (project root) to Python path so imports like `from funcs import ...` work
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
