"""Example 38: decorator identity."""

from collections.abc import Callable


def route(handler: Callable[[], str]) -> Callable[[], str]:
    # => Returning the original object keeps direct handler calls valid.
    return handler


def handler() -> str:
    return "ok"


def main() -> None:
    # => Identity preservation is the decorator contract being tested.
    print(route(handler) is handler)


if __name__ == "__main__":
    main()
