"""Example 29: A Fluent Builder for HTTP Requests."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass(frozen=True)  # => the finished product -- immutable once built() returns it
class Request:  # => begins the Request class body
    method: str  # => a required field, part of the generated __init__
    url: str  # => a required field, part of the generated __init__
    headers: dict[str, str]  # => a required field, part of the generated __init__
    body: str | None  # => a required field, part of the generated __init__


class RequestBuilder:  # => begins the RequestBuilder class body
    def __init__(self, url: str) -> None:  # => only the ONE truly required piece
        self._url: str = url  # => stores the required url on this instance
        self._method: str = "GET"  # => a sensible default -- no need to always name it
        self._headers: dict[str, str] = {}  # => starts empty, grows via with_header
        self._body: str | None = None  # => optional -- most requests have no body

    def with_method(self, method: str) -> "RequestBuilder":  # => fluent step
        self._method = method  # => mutates this builder's own state
        return self  # => returning self is what enables the NEXT chained call

    def with_header(self, key: str, value: str) -> "RequestBuilder":  # => fluent step
        self._headers[key] = value  # => accumulates one header per call
        return self  # => returning self is what enables the NEXT chained call

    def with_body(self, body: str) -> "RequestBuilder":  # => fluent step
        self._body = body  # => mutates this builder's own state
        return self  # => returning self is what enables the NEXT chained call

    def build(self) -> Request:  # => the terminal step -- assembles the final object
        return Request(self._method, self._url, dict(self._headers), self._body)  # => a fresh, immutable snapshot -- not a live view of the builder


request: Request = (
    RequestBuilder("https://api.example.com/orders")  # => only the required piece
    .with_method("POST")  # => optional pieces chained in ANY order needed
    .with_header("Content-Type", "application/json")  # => optional pieces
    .with_body('{"item": "widget"}')  # => optional pieces
    .build()  # => terminal call -- returns the finished, immutable Request
)
print(request.method, request.url)  # => confirms the chained values landed correctly
# => Output: POST https://api.example.com/orders
print(request.headers, request.body)  # => confirms headers and body landed correctly
# => Output: {'Content-Type': 'application/json'} {"item": "widget"}
# => A fluent builder assembles optional parts step by step, with no telescoping constructor
