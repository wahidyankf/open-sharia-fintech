"""Define build and distribution commands for a Python package."""

import sys

print(f"{sys.executable} -m build")
print(f"{sys.executable} -m twine check dist/*")
