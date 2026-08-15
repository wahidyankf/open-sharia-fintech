"""Example 26: empty 204 response."""


def main() -> None:
    # => No Content means successful work with no entity bytes.
    status, body = 204, b""
    # => The empty body honors the status semantics.
    print(status, len(body))


if __name__ == "__main__":
    main()
