"""Declare and inspect an actual runtime dependency in pyproject syntax."""

import tomllib

pyproject = """[project]
name = "notes-linux"
version = "0.1.0"
dependencies = ["platformdirs>=4.2"]
"""
dependencies = tomllib.loads(pyproject)["project"]["dependencies"]
assert dependencies == ["platformdirs>=4.2"]
print(dependencies[0])
