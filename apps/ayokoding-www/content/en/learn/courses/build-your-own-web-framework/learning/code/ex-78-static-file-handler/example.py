"""Example 78: static file response."""


def main() -> None:
    # => Static handlers return raw file bytes with matching metadata.
    body, content_type = b"asset", "text/plain"
    # => Binary data is never decoded unnecessarily.
    print(content_type, body.decode())


if __name__ == "__main__":
    main()
