"""Example 41: pytest verification for the Lazily-Paged API Iterator."""

from example import FetchLog, PagedApiIterator


def test_constructing_the_iterator_fetches_nothing() -> None:
    log: FetchLog = FetchLog()
    PagedApiIterator(log)  # => construction alone must not touch the fake API
    assert log.fetched_pages == []


def test_pages_are_fetched_lazily_one_at_a_time() -> None:
    log: FetchLog = FetchLog()
    paged: PagedApiIterator = PagedApiIterator(log)
    first: str = next(iter(paged))  # => only enough to produce one item
    assert first == "item-a"
    assert log.fetched_pages == [1]  # => page 2 was NOT fetched yet


def test_draining_the_iterator_fetches_every_remaining_page() -> None:
    log: FetchLog = FetchLog()
    paged: PagedApiIterator = PagedApiIterator(log)
    all_items: list[str] = list(paged)  # => drains everything, across all pages
    assert all_items == ["item-a", "item-b", "item-c", "item-d"]
    assert log.fetched_pages == [1, 2, 3]  # => including the empty terminating page


# => Run: pytest -- Output: 3 passed
