"""Example 70: a real C-extension call (hashlib's OpenSSL-backed sha256) profiled
with cProfile -- confirms cProfile shows exactly ONE opaque line for it, with no
visibility into what happens inside the C implementation.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the profiling target itself

import hashlib  # => co-13/co-22: hashlib.sha256 is a REAL C extension (OpenSSL-backed) -- the opaque call this example profiles


def hash_many(
    data: bytes, times: int
) -> str:  # => co-13: the ONE function make cProfile's C-extension line comes from
    digest = b""  # => co-13: chains each round's OUTPUT into the next round's INPUT -- avoids the optimizer folding calls away
    for _ in range(
        times
    ):  # => co-13: repeats many times, so the C-extension cost genuinely dominates the profile
        digest = hashlib.sha256(
            data + digest
        ).digest()  # => co-13/co-22: the C-extension call -- opaque to cProfile
    return digest.hex()  # => co-13: returned but unused by the caller -- only the PROFILE, not the result, matters here
