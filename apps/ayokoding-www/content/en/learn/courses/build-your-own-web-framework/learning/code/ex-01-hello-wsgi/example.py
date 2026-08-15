"""Example 1: hello WSGI."""

from collections.abc import Callable, Iterable

Start = Callable[[str, list[tuple[str, str]]], None]


def application(environ: dict[str, object], start: Start) -> Iterable[bytes]:
    # => WSGI gives the app raw request metadata and a response callback.
    body = b"Hello"
    # => Status and headers are native strings; body chunks are bytes.
    start("200 OK", [("Content-Type", "text/plain")])
    return [body]


def main() -> None:
    # => The fake callback lets this protocol example run without a server.
    print(b"".join(application({}, lambda status, headers: None)).decode())


if __name__ == "__main__":
    main()
