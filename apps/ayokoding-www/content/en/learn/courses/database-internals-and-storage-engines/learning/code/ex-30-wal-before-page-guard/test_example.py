"""Example 30: pytest verification for the WAL-Before-Page Ordering Guard."""

import pytest

from example import WalOrderingError, durable_lsns, flush_page, make_durable


def test_flush_before_durable_raises() -> None:
    durable_lsns.clear()
    with pytest.raises(WalOrderingError):
        flush_page(page_lsn=1)


def test_flush_after_durable_succeeds() -> None:
    durable_lsns.clear()
    make_durable(2)
    flush_page(page_lsn=2)  # => no exception -- the guard passed


# => Run: pytest -- Output: 2 passed
