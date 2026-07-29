# pyright: strict
"""Example 29: Versioning via the URI Path. (co-13)

Routing `/v1/...` and `/v2/...` to different handlers is the most visible
versioning strategy -- Google's AIP-185 recommends "v1", not "v1.0", and the
version lives directly in every request's own path.
"""

from typing import Callable  # => a handler is just a function, typed for clarity

ROUTES: dict[str, Callable[[], dict[str, object]]] = {  # => co-13: path prefix -> its own handler
    "/v1/articles/1": lambda: {"id": 1, "title": "Hello"},  # => v1 shape: two fields
    "/v2/articles/1": lambda: {"id": 1, "title": "Hello", "author": "Ada"},  # => v2 adds a field
}  # => end of ROUTES
# => ROUTES has 2 keys, each mapped to a zero-arg callable returning that version's own shape


def dispatch(path: str) -> dict[str, object]:  # => co-13: routes purely by the path's own prefix
    handler = ROUTES[path]  # => co-13: the version is baked into the URI itself
    return handler()  # => calls whichever version's handler matched


v1_result = dispatch("/v1/articles/1")  # => request 1: explicitly asks for v1
print(f"v1: {v1_result}")  # => Output: {'id': 1, 'title': 'Hello'}

v2_result = dispatch("/v2/articles/1")  # => request 2: explicitly asks for v2
# => v2_result has one MORE key ("author") than v1_result -- a different URI, a different shape
print(f"v2: {v2_result}")  # => Output: {'id': 1, 'title': 'Hello', 'author': 'Ada'}
