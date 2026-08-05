"""Declare a console script entry point."""

import tomllib

pyproject = """[project]
name = "notes-linux"
version = "0.1.0"

[project.scripts]
notes-linux = "notes_linux.cli:main"
"""
print(tomllib.loads(pyproject)["project"]["scripts"]["notes-linux"])
