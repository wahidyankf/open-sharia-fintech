# learning/code/ex-20-secret-in-env-not-code/verify_secret_hygiene.py
"""Example 20: Secret in Env, Not Code -- verifies both sibling modules for real."""  # => co-17: docstring

from __future__ import (
    annotations,
)  # => co-17: DD-39 hygiene, unrelated to the verification itself

import os  # => co-17: os.environ -- sets the SAME key name secure_api.py reads at runtime below
from pathlib import (
    Path,
)  # => co-17: reads each sibling module's OWN source text for the grep-style check

import insecure_api  # => co-17: the VULNERABLE sibling module -- hardcodes the key at import time
import secure_api  # => co-17: the FIXED sibling module -- reads os.environ at call time, not import time

THIS_DIR = Path(
    __file__
).parent  # => co-17: the directory both sibling .py files live in
REAL_SECRET_VALUE = "sk-live-51HxT9mQ2vL7pRz3nK8wY0aB"  # => co-17: the literal string this whole check hunts for


if (
    __name__ == "__main__"
):  # => co-17: entry point -- grep both sources, then prove the fixed version still works
    print(
        "=== Grepping insecure_api.py for the literal secret ==="
    )  # => co-17: the VULNERABLE case
    insecure_source = (
        THIS_DIR / "insecure_api.py"
    ).read_text()  # => co-17: the ACTUAL source text on disk
    insecure_has_secret = (
        REAL_SECRET_VALUE in insecure_source
    )  # => co-17: a literal substring search, like `grep`
    print(
        f"secret literal found in insecure_api.py: {insecure_has_secret}"
    )  # => co-17: True -- confirms the leak

    print(
        "\n=== Grepping secure_api.py for the literal secret ==="
    )  # => co-17: the FIXED case
    secure_source = (
        THIS_DIR / "secure_api.py"
    ).read_text()  # => co-17: the ACTUAL source text on disk
    secure_has_secret = (
        REAL_SECRET_VALUE in secure_source
    )  # => co-17: the SAME substring search, different file
    print(
        f"secret literal found in secure_api.py: {secure_has_secret}"
    )  # => co-17: False -- proves no secret in source

    print(
        "\n=== secure_api.py still authenticates, sourced from the environment ==="
    )  # => co-17: the FIX still works
    os.environ["API_KEY"] = (
        REAL_SECRET_VALUE  # => co-17: this is what deploy tooling/`.env` would set, not source
    )
    authenticated = secure_api.authenticate(
        REAL_SECRET_VALUE
    )  # => co-17: a request presenting the REAL key
    rejected = secure_api.authenticate(
        "wrong-key-entirely"
    )  # => co-17: a request presenting the WRONG key
    print(
        f"authenticate(real key): {authenticated}"
    )  # => co-17: True -- works, sourced entirely from os.environ
    print(
        f"authenticate(wrong key): {rejected}"
    )  # => co-17: False -- correctness is unaffected by the fix

    assert (
        insecure_has_secret and not secure_has_secret and authenticated and not rejected
    )  # => co-17: all 4 checks pass
