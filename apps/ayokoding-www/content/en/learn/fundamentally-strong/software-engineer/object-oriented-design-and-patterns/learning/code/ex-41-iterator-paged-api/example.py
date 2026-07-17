"""Example 41: An Iterator That Lazily Pages a Remote API."""

from collections.abc import Iterator  # => imports Iterator from collections.abc

# => a self-contained FAKE standing in for a real, network-backed API -- no real network call
_FAKE_REMOTE_PAGES: dict[int, list[str]] = {
    1: ["item-a", "item-b"],  # => page 1's two records
    2: ["item-c", "item-d"],  # => page 2's two records
    3: [],  # => an EMPTY page signals "no more data" -- the fetch loop stops here
}


class FetchLog:  # => an observable stand-in for "a network call happened"
    def __init__(self) -> None:  # => the constructor
        self.fetched_pages: list[int] = []  # => records EVERY page number actually fetched


def fetch_page(page_number: int, log: FetchLog) -> list[str]:  # => the "remote" call
    log.fetched_pages.append(page_number)  # => records that THIS page was fetched now
    return list(_FAKE_REMOTE_PAGES.get(page_number, []))  # => a COPY -- callers pop() their own buffer, never the shared fake dataset


class PagedApiIterator:  # => fetches ONE page at a time, only when the current page runs out
    def __init__(self, log: FetchLog) -> None:  # => the constructor
        self._log: FetchLog = log  # => shared so the example can OBSERVE fetch timing
        self._page_number: int = 1  # => starts at the first page
        self._buffer: list[str] = []  # => the current page's not-yet-yielded items
        self._exhausted: bool = False  # => True once an empty page has been seen

    def __iter__(self) -> Iterator[str]:  # => makes `for item in paged_iterator` work
        while True:  # => keeps pulling pages until the fake API returns an empty one
            if not self._buffer and not self._exhausted:  # => current page is used up
                self._buffer = fetch_page(self._page_number, self._log)  # => fetches lazily, exactly when needed
                self._page_number += 1  # => advances for the NEXT fetch, if one happens
                if not self._buffer:  # => an empty page means there is nothing left
                    self._exhausted = True  # => stops future fetch attempts
            if not self._buffer:  # => truly nothing left to yield
                return  # => stops the generator cleanly
            yield self._buffer.pop(0)  # => yields ONE item at a time, oldest first


log: FetchLog = FetchLog()  # => constructs log
paged: PagedApiIterator = PagedApiIterator(log)  # => cheap -- no page has been fetched yet
print(log.fetched_pages)  # => confirms NOTHING was fetched just by constructing the iterator
# => Output: []

first_item: str = next(iter(paged))  # => pulling ONE item triggers fetching page 1 only
print(first_item, log.fetched_pages)  # => page 2 was NOT fetched just to get one item
# => Output: item-a [1]

all_items: list[str] = list(paged)  # => draining the rest pulls page 1's remainder + page 2
print(all_items)  # => item-b was still buffered; item-c/item-d came from the page-2 fetch
# => Output: ['item-b', 'item-c', 'item-d']
print(log.fetched_pages)  # => page 3 (empty) was fetched too, to discover the data had ended
# => Output: [1, 2, 3]
# => Pages are fetched lazily, one at a time, only when the current buffer is exhausted
