"""Show the command that installs the current project in editable mode."""

import sys

print(f"{sys.executable} -m pip install -e .")
