"""Example 3: Create Venv Install -- run inside the venv after `pip install pytest`."""

# Resolves ONLY inside the venv's site-packages, not the system Python.
import pytest

# Proves the venv's pip install worked.
print(f"pytest {pytest.__version__} importable")
# => Output: pytest <installed-version> importable
