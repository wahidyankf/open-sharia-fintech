"""Example 71: normalize header lookup."""


def main() -> None:
    # => HTTP header names are case-insensitive.
    headers = {"content-type": "application/json"}
    # => Lowercasing lookup preserves HTTP semantics.
    print(headers["Content-Type".lower()])


if __name__ == "__main__":
    main()
