"""Read useful package metadata from a pyproject document."""

import tomllib

pyproject = """[project]
name = "notes-linux"
version = "0.1.0"
description = "Local notes service"
requires-python = ">=3.11"
"""
project = tomllib.loads(pyproject)["project"]
print(project["description"], project["requires-python"])
