"""Capstone middleware onion."""

from collections.abc import Callable

from router import Response


Handler = Callable[[], Response]


def errors(next_handler: Handler) -> Handler:
    # => The outer error boundary converts failures instead of leaking traces.
    def wrapped() -> Response:
        try:
            return next_handler()
        except Exception:
            return Response(500, b'{"detail":"internal server error"}')

    return wrapped


def logging(next_handler: Handler) -> Handler:
    # => Logging wraps the next layer, proving middleware ordering is observable.
    def wrapped() -> Response:
        print("request")
        return next_handler()

    return wrapped
