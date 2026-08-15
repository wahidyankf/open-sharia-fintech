"""Example 51: add a response header."""


def main() -> None:
    # => Outbound middleware can enforce common response metadata.
    headers = {"X-Request-ID": "r-1"}
    # => Clients receive the header after the handler returns.
    print(headers["X-Request-ID"])


if __name__ == "__main__":
    main()
