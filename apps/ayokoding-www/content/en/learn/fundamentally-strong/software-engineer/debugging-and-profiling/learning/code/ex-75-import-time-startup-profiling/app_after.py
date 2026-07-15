"""Example 75: AFTER -- defer the import until uses_pattern() is actually called."""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the fix itself


def main() -> (
    None
):  # => co-23: the SAME shape as app_before.py, but with NO module-level slow_module import at all
    print(
        "app started"
    )  # => co-23: identical output to app_before.py -- ONLY the startup cost should differ


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => co-23: the ONE call measure_startup.py times, to capture the DEFERRED-import cost
