"""Example 5: return bytes."""


def main() -> None:
    # => Text is encoded before it crosses the WSGI boundary.
    body = "hello".encode("utf-8")
    # => The server consumes an iterable of bytestrings.
    chunks: list[bytes] = [body]
    print(b"".join(chunks).decode())


if __name__ == "__main__":
    main()
