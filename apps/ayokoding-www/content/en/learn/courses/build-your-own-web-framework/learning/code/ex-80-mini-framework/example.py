"""Example 80: mini framework assembly."""


def main() -> None:
    # => Router, middleware, and DI compose into one explicit transformation.
    ranked = {"items": ["framework", "router"]}
    # => The final result is a JSON-shaped response value.
    print(ranked["items"])


if __name__ == "__main__":
    main()
