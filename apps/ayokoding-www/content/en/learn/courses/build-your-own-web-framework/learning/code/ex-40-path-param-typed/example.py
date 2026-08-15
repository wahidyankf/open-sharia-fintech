"""Example 40: convert a path parameter."""


def main() -> None:
    # => Conversion validates a parameter at route-match time.
    value = int("42")
    # => Invalid text would be handled as a route miss.
    print(value + 1)


if __name__ == "__main__":
    main()
