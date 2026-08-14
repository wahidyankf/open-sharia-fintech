"""Example 13: explicit 404."""


def main() -> None:
    # => Missing routes are normal outcomes, not uncaught exceptions.
    status, body = 404, b"not found"
    # => A router later chooses this fallback automatically.
    print(status, body.decode())


if __name__ == "__main__":
    main()
