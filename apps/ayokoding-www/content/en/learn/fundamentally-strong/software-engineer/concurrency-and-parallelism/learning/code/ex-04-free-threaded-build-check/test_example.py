"""Example 4: pytest verification for Detecting a Free-Threaded (No-GIL) Build."""

from example import built_free_threaded, gil_is_enabled


def test_standard_build_reports_gil_enabled() -> None:
    # => this suite runs on standard CPython, never the `python3.14t` free-threaded build
    assert gil_is_enabled() is True


def test_standard_build_was_not_compiled_free_threaded() -> None:
    assert built_free_threaded() is False


# => Run: pytest -- Output: 2 passed
