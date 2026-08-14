"""Example 18: validate WSGI header values."""


def valid(header: tuple[object, object]) -> bool:
    # => WSGI headers use native strings, not ASGI byte pairs.
    return isinstance(header[0], str) and isinstance(header[1], str)


def main() -> None:
    # => Bytes would be rejected at this WSGI protocol boundary.
    print(valid(("Content-Type", "text/plain")))


if __name__ == "__main__":
    main()
