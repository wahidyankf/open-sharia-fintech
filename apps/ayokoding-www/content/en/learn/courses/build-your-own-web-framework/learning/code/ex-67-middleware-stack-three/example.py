"""Example 67: three middleware layers."""


def main() -> None:
    # => The three-layer onion reverses on response flow.
    events = ["log", "auth", "time", "handler", "time", "auth", "log"]
    # => Ordering is observable correctness.
    print(events)


if __name__ == "__main__":
    main()
