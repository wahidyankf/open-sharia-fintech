"""Example 35: compare contracts."""


def main() -> None:
    # => WSGI returns bytes while ASGI emits async event dictionaries.
    wsgi, asgi = b"ok", {"type": "http.response.body", "body": b"ok"}
    # => Endpoint meaning can match even when server protocols differ.
    print(wsgi == asgi["body"])


if __name__ == "__main__":
    main()
