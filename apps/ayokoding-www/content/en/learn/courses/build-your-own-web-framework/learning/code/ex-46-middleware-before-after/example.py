"""Example 46: before and after order."""


def main() -> None:
    # => Request work runs before the inner handler and response work after it.
    events = ["before", "handler", "after"]
    # => This ordering defines the middleware onion.
    print(events)


if __name__ == "__main__":
    main()
