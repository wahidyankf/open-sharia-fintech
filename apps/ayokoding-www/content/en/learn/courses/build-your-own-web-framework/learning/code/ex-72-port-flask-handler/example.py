"""Example 72: port a Flask-shaped handler."""


def main() -> None:
    # => Endpoint behavior is independent from a particular framework decorator.
    handler = lambda: b"same response"
    # => The small framework can preserve response bytes.
    print(handler().decode())


if __name__ == "__main__":
    main()
