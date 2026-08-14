"""Example 10: build a request object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    # => Typed fields keep raw environ parsing at the protocol edge.
    method: str
    path: str


def main() -> None:
    # => Handler code receives one ergonomic immutable value.
    print(Request("GET", "/health"))


if __name__ == "__main__":
    main()
