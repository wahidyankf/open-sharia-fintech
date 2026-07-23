"""Example 75: BEFORE -- slow_module imported unconditionally at startup, even
though most runs of this program never call uses_pattern()."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the eager import itself

import slow_module  # noqa: F401 -- imported eagerly, at module load time  # => co-13: pays slow_module's FULL import cost every startup


def main() -> (
    None
):  # => co-13: never calls slow_module.uses_pattern() -- the import cost is paid for NOTHING here
    print(
        "app started"
    )  # => co-13: the ONLY output -- this program's real work never touches slow_module at all


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => co-13: the ONE call measure_startup.py times, to capture the EAGER-import cost
