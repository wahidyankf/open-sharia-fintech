"""Example 65: WSGI stream iterable."""


def main() -> None:
    # => WSGI streaming yields bytes one chunk at a time.
    chunks = (chunk for chunk in [b"a", b"b"])
    # => The server consumes this iterable lazily.
    print(b"".join(chunks))


if __name__ == "__main__":
    main()
