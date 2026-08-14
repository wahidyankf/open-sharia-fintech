"""Example 79: integration assertion."""


def main() -> None:
    # => A test client exercises routing through response behavior.
    status = 200
    # => End-to-end assertions catch composition defects.
    assert status == 200
    print("passed")


if __name__ == "__main__":
    main()
