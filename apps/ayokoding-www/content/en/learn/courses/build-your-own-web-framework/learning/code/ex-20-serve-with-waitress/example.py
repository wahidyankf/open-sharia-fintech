"""Example 20: expose a server-callable WSGI app."""

from collections.abc import Callable, Iterable


def application(
    environ: dict[str, object], start: Callable[[str, list[tuple[str, str]]], None]
) -> Iterable[bytes]:
    # => A WSGI server such as Waitress invokes this callable.
    start("200 OK", [("Content-Type", "text/plain")])
    return [b"server owns sockets"]


def main() -> None:
    # => The example runs the app directly rather than binding a socket.
    print(b"".join(application({}, lambda status, headers: None)).decode())


if __name__ == "__main__":
    main()
