"""Example 50: attach request ID."""


def main() -> None:
    # => Middleware adds scoped metadata before the handler runs.
    request = {"request_id": "r-1"}
    # => The handler reads the value from this request only.
    print(request["request_id"])


if __name__ == "__main__":
    main()
