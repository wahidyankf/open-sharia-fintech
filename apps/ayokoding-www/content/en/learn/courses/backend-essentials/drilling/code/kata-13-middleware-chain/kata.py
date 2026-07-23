from collections.abc import Callable
from typing import TypedDict


class Response(TypedDict):  # => co-04: a typed shape, so `headers` is always known to be dict[str, str]
    status: int
    body: str
    headers: dict[str, str]


Handler = Callable[[dict[str, str]], Response]  # => co-08: a plain handler -- knows nothing about middleware
Middleware = Callable[[Handler], Handler]  # => co-16: wraps a handler, returns a NEW handler


def request_id_middleware(counter: list[int]) -> Middleware:  # => co-16/co-04: adds X-Request-Id
    def wrap(handler: Handler) -> Handler:
        def wrapped(headers: dict[str, str]) -> Response:
            counter[0] += 1  # => a mocked id generator -- a real one might use uuid4()
            response = handler(headers)  # => call the INNER handler first
            response["headers"]["X-Request-Id"] = str(counter[0])  # => co-04: mutate the typed headers dict
            return response

        return wrapped

    return wrap


def timing_middleware(clock: Callable[[], float]) -> Middleware:  # => co-16: adds X-Process-Time
    def wrap(handler: Handler) -> Handler:
        def wrapped(headers: dict[str, str]) -> Response:
            start = clock()  # => mocked clock -- avoids real-time flakiness in this kata
            response = handler(headers)
            elapsed = clock() - start  # => wall-clock cost of the WRAPPED handler only
            response["headers"]["X-Process-Time"] = f"{elapsed:.3f}"  # => co-04/co-16
            return response

        return wrapped

    return wrap


def base_handler(headers: dict[str, str]) -> Response:  # => co-08: the actual endpoint logic, middleware-free
    return {"status": 200, "body": "ok", "headers": {}}


ticks = iter([0.0, 0.25])  # => mocked clock readings: start=0.0, end=0.25 -- deterministic, no real sleep
request_counter = [0]

wrapped_handler = timing_middleware(lambda: next(ticks))(  # => co-16: compose middlewares around base_handler
    request_id_middleware(request_counter)(base_handler)
)
response = wrapped_handler({})

print(response)  # => Output: {'status': 200, 'body': 'ok', 'headers': {'X-Request-Id': '1', 'X-Process-Time': '0.250'}}

headers = response["headers"]
assert headers["X-Request-Id"] == "1"  # => co-16/co-04: every response now carries a traceable id
assert headers["X-Process-Time"] == "0.250"  # => co-16: cross-cutting behavior added WITHOUT touching base_handler
print("kata-13 OK")
