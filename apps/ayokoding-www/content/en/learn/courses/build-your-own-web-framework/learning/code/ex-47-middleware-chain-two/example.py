"""Example 47: two middleware layers."""


def main() -> None:
    # => Nested layers reverse their after phases.
    events = ["log-before", "time-before", "handler", "time-after", "log-after"]
    # => The list makes onion order assertable.
    print(events)


if __name__ == "__main__":
    main()
