"""Example 28: framework as transformation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    status: int
    body: bytes


def application(path: str) -> Response:
    # => The core maps incoming request information to an explicit response.
    return Response(200, b"ok") if path == "/health" else Response(404, b"not found")


def main() -> None:
    # => Router-like behavior composes without hidden mutable state.
    print(application("/health").status)


if __name__ == "__main__":
    main()
