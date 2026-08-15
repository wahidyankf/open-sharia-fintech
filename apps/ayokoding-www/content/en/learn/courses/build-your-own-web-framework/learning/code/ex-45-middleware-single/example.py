"""Example 45: one middleware wrapper."""

from collections.abc import Callable


def log(next_handler: Callable[[], str]) -> Callable[[], str]:
    # => The wrapper observes a handler without changing handler code.
    return lambda: "before " + next_handler() + " after"


def main() -> None:
    # => The response is bracketed by middleware behavior.
    print(log(lambda: "handler")())


if __name__ == "__main__":
    main()
