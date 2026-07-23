"""Example 75: a module with a deliberately expensive import-time side effect --
the KIND of thing that silently slows down every process startup."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the import-time cost itself

import re  # => co-13/co-22: the module whose compile() call below is the entire import-time cost of this file

# co-13/co-22: a large, module-level regex compilation done unconditionally at
# IMPORT time, even for code paths that never end up using it.
_EXPENSIVE_PATTERN = re.compile(
    "|".join(f"pattern-{i}" for i in range(20_000))
)  # => co-13/co-22: runs on EVERY import


def uses_pattern(
    text: str,
) -> bool:  # => co-13: the ONE function that actually needs _EXPENSIVE_PATTERN
    return bool(
        _EXPENSIVE_PATTERN.search(text)
    )  # => co-13: the ONLY caller of the expensive module-level regex
