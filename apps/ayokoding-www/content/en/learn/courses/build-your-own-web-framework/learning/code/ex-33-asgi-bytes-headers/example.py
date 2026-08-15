"""Example 33: ASGI byte headers."""


def main() -> None:
    # => ASGI preserves headers as wire-format byte pairs.
    headers: list[tuple[bytes, bytes]] = [(b"content-type", b"text/plain")]
    # => Native strings would be a WSGI, not ASGI, representation.
    print(headers[0])


if __name__ == "__main__":
    main()
