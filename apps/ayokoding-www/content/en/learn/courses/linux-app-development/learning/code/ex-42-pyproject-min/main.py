"""Show a minimal valid pyproject project table."""

import tomllib

pyproject = """[project]
name = "notes-linux"
version = "0.1.0"
"""
project = tomllib.loads(pyproject)["project"]
print(project["name"], project["version"])
