"""Example 51: a chained exception (`raise ... from ...`) and pdb's `exceptions`
command for walking the exception chain during post-mortem debugging.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to exception chaining itself


def parse_int(
    raw: str,
) -> int:  # => co-04: the function that raises the ROOT-CAUSE exception
    return int(raw)  # => co-04: the ROOT cause -- raises ValueError on bad input


def load_config_value(
    raw: str,
) -> int:  # => co-04: the function that WRAPS the root cause in a new type
    try:  # => co-04: catches ONLY the root-cause type, never a bare `except Exception`
        return parse_int(
            raw
        )  # => co-04: delegates to the function that can genuinely fail
    except (
        ValueError
    ) as exc:  # => co-04: exc IS the root cause -- kept alive via `from exc` below
        # co-04: deliberately wrap with a new exception type, chaining the
        # original so the root cause is still reachable via __cause__.
        raise RuntimeError(
            f"config value {raw!r} could not be loaded"
        ) from exc  # => co-04: the CHAIN, not a swap


def main() -> (
    None
):  # => co-03: the entry point -- one call deep from the eventual uncaught exception
    load_config_value(
        "not-a-number"
    )  # => co-04: deliberately invalid input -- guarantees the chain forms


if (
    __name__ == "__main__"
):  # => co-03: guards the module-level call so importing this file stays side-effect-free
    main()  # => co-03: the ONE call whose uncaught exception drives ex-51's post-mortem session
