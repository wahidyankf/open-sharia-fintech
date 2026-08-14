"""Example 53: exception handler map."""


class Missing(Exception):
    pass


def main() -> None:
    # => Exception type dispatch is declarative framework policy.
    handlers = {Missing: 404}
    # => A domain failure maps to its precise response status.
    print(handlers[Missing])


if __name__ == "__main__":
    main()
