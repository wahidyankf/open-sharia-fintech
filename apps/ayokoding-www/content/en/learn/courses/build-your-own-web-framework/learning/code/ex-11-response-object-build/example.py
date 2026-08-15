"""Example 11: build a response object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    # => A response value is testable before protocol serialization.
    status: int
    body: bytes


def main() -> None:
    # => Status and body travel together through middleware.
    print(Response(200, b"ok").status)


if __name__ == "__main__":
    main()
