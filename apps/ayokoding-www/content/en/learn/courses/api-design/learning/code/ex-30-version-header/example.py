# pyright: strict
"""Example 30: Versioning via a Request Header. (co-13)

Stripe pins a version per API key via `Stripe-Version`, rather than baking
it into the URI -- the SAME path resolves differently depending purely on a
header's value, keeping every version's URI identical.
"""

from typing import Callable  # => a handler is just a function, typed for clarity

HANDLERS: dict[str, Callable[[], dict[str, object]]] = {  # => co-13: header value -> its own handler
    "2025-01-01": lambda: {"id": 1, "title": "Hello"},  # => the OLDER API-Version shape
    "2026-01-01": lambda: {"id": 1, "title": "Hello", "author": "Ada"},  # => the NEWER shape
}  # => end of HANDLERS


def dispatch(path: str, api_version: str) -> dict[str, object]:  # => co-13: routes by header, not path
    handler = HANDLERS[api_version]  # => co-13: the SAME path, resolved by a header value instead
    return handler()  # => calls whichever version's handler the header selected


old = dispatch("/articles/1", api_version="2025-01-01")  # => request 1: the older header value
print(f"2025-01-01: {old}")  # => Output: {'id': 1, 'title': 'Hello'}

new = dispatch("/articles/1", api_version="2026-01-01")  # => request 2: SAME path, newer header
# => both calls used the identical path "/articles/1" -- only the header value changed the shape
print(f"2026-01-01: {new}")  # => Output: {'id': 1, 'title': 'Hello', 'author': 'Ada'}
