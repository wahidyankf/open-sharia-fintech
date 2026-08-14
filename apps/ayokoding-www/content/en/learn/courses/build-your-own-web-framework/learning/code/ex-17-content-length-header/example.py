"""Example 17: calculate Content-Length."""


def main() -> None:
    # => Transport framing counts encoded bytes rather than Python characters.
    body = "é".encode("utf-8")
    # => The header value itself remains a native string in WSGI.
    print(("Content-Length", str(len(body))))


if __name__ == "__main__":
    main()
