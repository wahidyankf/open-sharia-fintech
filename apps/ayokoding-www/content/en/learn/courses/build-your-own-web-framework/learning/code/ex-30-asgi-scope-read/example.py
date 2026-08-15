"""Example 30: read ASGI scope."""


def main() -> None:
    # => Scope is immutable connection metadata supplied once by the server.
    scope: dict[str, object] = {"type": "http", "method": "GET", "path": "/"}
    # => Handlers read method and path from this protocol dictionary.
    print(scope["type"], scope["method"], scope["path"])


if __name__ == "__main__":
    main()
