"""Example 12: serialize Response to WSGI."""

from collections.abc import Callable, Iterable


class Response:
    def __call__(
        self,
        environ: dict[str, object],
        start: Callable[[str, list[tuple[str, str]]], None],
    ) -> Iterable[bytes]:
        # => The response object itself satisfies the WSGI callable contract.
        start("200 OK", [("Content-Type", "text/plain")])
        return [b"ok"]


def main() -> None:
    # => Invoking it directly tests serialization without a server.
    print(b"".join(Response()({}, lambda status, headers: None)).decode())


if __name__ == "__main__":
    main()
