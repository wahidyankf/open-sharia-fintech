"""Example 61: inject database connection."""


def main() -> None:
    # => A fake connection stands in for a request-scoped resource.
    connection = {"request": "r1"}
    # => The handler receives it explicitly.
    print(connection["request"])


if __name__ == "__main__":
    main()
