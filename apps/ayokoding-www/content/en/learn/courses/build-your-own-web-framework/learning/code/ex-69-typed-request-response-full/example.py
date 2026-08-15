"""Example 69: typed request and response."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    status: int
    body: bytes


def main() -> None:
    # => Types document the response contract before serialization.
    print(Response(200, b"ok").status)


if __name__ == "__main__":
    main()
