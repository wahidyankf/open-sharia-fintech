"""Example 37: route decorator."""

from collections.abc import Callable

routes: dict[str, Callable[[], str]] = {}


def route(path: str) -> Callable[[Callable[[], str]], Callable[[], str]]:
    # => Decoration registers a handler while preserving its callable form.
    return lambda handler: routes.setdefault(path, handler)


@route("/x")
def handler() -> str:
    return "x"


def main() -> None:
    print(routes["/x"]())


if __name__ == "__main__":
    main()
