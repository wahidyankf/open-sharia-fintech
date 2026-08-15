"""Example 59: per-request dependency."""


def main() -> None:
    # => Each provider call creates fresh request-scoped state.
    first, second = object(), object()
    # => Distinct identities prove requests do not share mutable values.
    print(first is not second)


if __name__ == "__main__":
    main()
