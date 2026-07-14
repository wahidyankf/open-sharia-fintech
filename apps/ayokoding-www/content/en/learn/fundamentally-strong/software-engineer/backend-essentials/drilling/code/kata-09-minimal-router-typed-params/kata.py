from collections.abc import Callable

Handler = Callable[[dict[str, str]], str]  # => co-08: a handler takes parsed params, returns a body


class Router:  # => co-07: maps a method + path PATTERN to a handler function
    def __init__(self) -> None:
        self._routes: list[tuple[str, list[str], Handler]] = []  # => (method, pattern segments, handler)

    def add(self, method: str, pattern: str, handler: Handler) -> None:  # => co-07: register one route
        segments = pattern.strip("/").split("/")  # => "/items/{id}" -> ["items", "{id}"]
        self._routes.append((method.upper(), segments, handler))

    def dispatch(self, method: str, path: str) -> str:  # => co-07/co-12: match method + path, extract params
        path_segments = path.strip("/").split("/")  # => the ACTUAL incoming path, same segment shape
        for route_method, pattern_segments, handler in self._routes:
            if route_method != method.upper():  # => wrong verb -- this route can't handle this call
                continue
            if len(pattern_segments) != len(path_segments):  # => different segment counts can't match
                continue
            params: dict[str, str] = {}  # => co-12: path params extracted from this specific request
            matched = True
            for pattern_seg, path_seg in zip(pattern_segments, path_segments):  # => compare segment by segment
                if pattern_seg.startswith("{") and pattern_seg.endswith("}"):  # => a PARAM slot, e.g. {id}
                    params[pattern_seg[1:-1]] = path_seg  # => bind the literal path text to its param name
                elif pattern_seg != path_seg:  # => a literal segment that doesn't match -- not this route
                    matched = False
                    break
            if matched:
                return handler(params)  # => co-08: hand the extracted params to the matched handler
        raise LookupError(f"no route for {method} {path}")  # => co-03: caller should map this to a 404


def get_item(params: dict[str, str]) -> str:  # => a tiny handler -- holds no routing logic itself
    return f"item {params['id']}"


router = Router()
router.add("GET", "/items/{id}", get_item)  # => co-07: registers the pattern once

result = router.dispatch("GET", "/items/42")  # => co-12: "42" is extracted and bound to params["id"]
print(result)  # => Output: item 42

assert result == "item 42"
try:
    router.dispatch("GET", "/items/42/extra")  # => co-03: segment count mismatch -- no route matches
    raised = False
except LookupError:
    raised = True
print(raised)  # => Output: True
assert raised is True
print("kata-09 OK")
