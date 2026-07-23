"""Example 75: Reproduce a Flaky Test Caused by Shared State, Then Isolate It."""
# Both tests below pass together AND in isolation -- the autouse fixture removes the hidden
# order dependency that a module-level mutable cache, left un-reset, would otherwise cause.

from __future__ import annotations

from collections.abc import Iterator

import pytest

_shared_cache: list[int] = []  # => co-26: the SAME module-level mutable state that caused the flake  # fmt: skip


def add_to_cache(
    value: int,
) -> None:  # => the function under test -- unchanged from the flaky version
    _shared_cache.append(value)  # => the SAME mutation that caused the flake -- still here on purpose  # fmt: skip


@pytest.fixture(autouse=True)  # => co-26/co-05: runs before EVERY test in this file, no opt-in needed  # fmt: skip
def reset_shared_cache() -> Iterator[None]:  # => co-05: yield-based setup AND teardown, in one fixture  # fmt: skip
    _shared_cache.clear()  # => co-26: SETUP -- guarantees every test starts from a KNOWN, empty state  # fmt: skip
    yield  # => hands control to the test body -- everything below runs AFTER the test finishes  # fmt: skip
    _shared_cache.clear()  # => co-26: TEARDOWN too -- belt-and-braces, leaves nothing for the NEXT test  # fmt: skip


def test_first_write_sees_empty_cache() -> None:  # => co-26: now TRUE regardless of run order  # fmt: skip
    add_to_cache(1)  # => act: writes into the SHARED cache the fixture just reset  # fmt: skip
    assert len(_shared_cache) == 1  # => guaranteed by the fixture's reset, not by test ORDER anymore  # fmt: skip


def test_second_write_also_sees_empty_cache() -> None:  # => co-26: the FORMERLY order-dependent test  # fmt: skip
    # Before the fixture: this test ASSUMED test_first_write... had already run and left state
    # behind. Now it makes NO such assumption -- reset_shared_cache() guarantees a clean start.
    add_to_cache(2)  # => act: writes into a FRESH, reset cache, regardless of prior tests  # fmt: skip
    assert len(_shared_cache) == 1  # => co-26: independent of whichever test ran before it, or none  # fmt: skip
