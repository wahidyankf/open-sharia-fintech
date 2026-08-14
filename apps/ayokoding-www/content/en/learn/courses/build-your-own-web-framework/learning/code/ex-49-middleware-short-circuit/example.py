"""Example 49: auth short circuit."""


def main() -> None:
    # => Middleware can return before calling the protected handler.
    authorized = False
    # => Unauthorized work is skipped completely.
    print(200 if authorized else 401)


if __name__ == "__main__":
    main()
