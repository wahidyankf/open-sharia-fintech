"""Example 21: dispatch with a route dictionary."""

from collections.abc import Callable


def main() -> None:
    # => The route table maps a fixed path directly to a handler.
    routes: dict[str, Callable[[], str]] = {"/health": lambda: "ok"}
    # => Dispatch is a lookup plus a safe fallback.
    print(routes.get("/health", lambda: "not found")())


if __name__ == "__main__":
    main()
