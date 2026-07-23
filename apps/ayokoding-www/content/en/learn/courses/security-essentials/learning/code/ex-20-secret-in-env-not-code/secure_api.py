# learning/code/ex-20-secret-in-env-not-code/secure_api.py
"""Example 20 (FIXED half): Secret in Env, Not Code -- reads the key from the environment."""  # => co-17: docstring

from __future__ import (
    annotations,
)  # => co-17: DD-39 hygiene, unrelated to the secret itself

import os  # => co-17: os.environ is the ONLY place this module ever reads the key from


def get_api_key() -> (
    str
):  # => co-17: the fixed lookup -- no literal secret value anywhere in this file
    """Read the API key from the environment -- FIXED, no secret value appears in source."""  # => co-17: doc
    key = os.environ.get(
        "API_KEY"
    )  # => co-17: reads the process environment -- set by the deploy/run tooling, not code
    if (
        key is None
    ):  # => co-17: fails LOUDLY if the operator forgot to set it, instead of silently using a default
        raise RuntimeError(
            "API_KEY environment variable is not set"
        )  # => co-17: an explicit, actionable error
    return key  # => co-17: the real secret value, sourced OUTSIDE this file entirely


def authenticate(
    candidate_key: str,
) -> bool:  # => co-17: the SAME check as insecure_api.py -- only the SOURCE changed
    """Authenticate a request by comparing candidate_key against the env-sourced key."""  # => co-17: doc
    return (
        candidate_key == get_api_key()
    )  # => co-17: identical logic, zero hardcoded secret in this module
