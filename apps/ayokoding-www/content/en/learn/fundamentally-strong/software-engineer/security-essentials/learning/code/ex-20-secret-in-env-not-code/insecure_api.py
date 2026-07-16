# learning/code/ex-20-secret-in-env-not-code/insecure_api.py
"""Example 20 (VULNERABLE half): Secret in Env, Not Code -- the hardcoded version, do not copy."""  # => co-17: docstring

from __future__ import (
    annotations,
)  # => co-17: DD-39 hygiene, unrelated to the secret itself

API_KEY = "sk-live-51HxT9mQ2vL7pRz3nK8wY0aB"  # => co-17: VULNERABLE -- a real-shaped secret, committed to source


def authenticate(
    candidate_key: str,
) -> bool:  # => co-17: the check both the insecure and fixed versions share
    """Authenticate a request by comparing candidate_key against the module-level API_KEY."""  # => co-17: doc
    return (
        candidate_key == API_KEY
    )  # => co-17: works correctly -- the PROBLEM is WHERE API_KEY lives, not this check
