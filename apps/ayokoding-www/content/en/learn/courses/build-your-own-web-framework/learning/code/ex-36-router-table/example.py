"""Example 36: router table."""


def main() -> None:
    # => Route keys combine request method and path.
    routes: dict[tuple[str, str], str] = {("GET", "/health"): "health"}
    # => Lookup is deterministic framework behavior.
    print(routes[("GET", "/health")])


if __name__ == "__main__":
    main()
