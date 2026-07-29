"""Example 9: Creating a Locked Environment with uv.

The uv workflow this example assumes:
  uv venv && source .venv/bin/activate
  uv pip install fastapi==0.139.0 pydantic==2.11.0
  uv run python example.py

This module confirms the locked install by reading the pinned versions back -- a reproducible environment
is what makes every later example see the same code. (co-07)
"""

import fastapi  # => the web framework pinned by the uv install above (co-07)
import pydantic  # => the validation library pinned alongside it (v2 line)


def installed_versions() -> tuple[str, str]:  # => reads installed metadata, no network call
    # => __version__ is plain module metadata pip/uv wrote at install time -- instant and offline
    return fastapi.__version__, pydantic.VERSION  # => a tuple of the two pinned version strings


if __name__ == "__main__":  # => run as: uv run python example.py
    fastapi_v, pydantic_v = installed_versions()  # => unpack the tuple
    print(f"fastapi=={fastapi_v}")  # => Output: fastapi==0.139.0 (the pinned line)
    print(f"pydantic=={pydantic_v}")  # => Output: pydantic==2.11.X (the v2 production line)
