"""Example 29: pytest verification for A Fluent Builder for HTTP Requests."""

from example import Request, RequestBuilder


def test_chained_builder_assembles_a_complete_request() -> None:
    request: Request = RequestBuilder("https://api.example.com/orders").with_method("POST").with_header("Content-Type", "application/json").with_body('{"item": "widget"}').build()
    assert request.method == "POST"
    assert request.headers == {"Content-Type": "application/json"}
    assert request.body == '{"item": "widget"}'


def test_omitted_optional_parts_use_sensible_defaults() -> None:
    request: Request = RequestBuilder("https://api.example.com/health").build()
    assert request.method == "GET"  # => no with_method() call, defaults apply
    assert request.headers == {}  # => no with_header() calls at all
    assert request.body is None  # => no with_body() call at all


# => Run: pytest -- Output: 2 passed
