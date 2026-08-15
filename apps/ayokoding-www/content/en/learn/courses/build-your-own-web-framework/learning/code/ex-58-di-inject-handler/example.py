"""Example 58: inject a handler dependency."""


def main() -> None:
    # => The framework passes declared data into the handler.
    handler = lambda service: "uses " + service
    # => The handler does not construct its own service.
    print(handler("db"))


if __name__ == "__main__":
    main()
