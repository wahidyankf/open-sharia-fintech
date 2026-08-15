"""Example 48: flip middleware order."""


def main() -> None:
    # => Composition order changes observable before/after behavior.
    first, second = "logging(timing)", "timing(logging)"
    # => Equivalent layers are not commutative.
    print(first != second)


if __name__ == "__main__":
    main()
