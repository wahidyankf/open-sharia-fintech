"""Example 16: format a WSGI status."""


def status(code: int, reason: str) -> str:
    # => WSGI requires code, one space, then a reason phrase.
    return f"{code} {reason}"


def main() -> None:
    # => This helper centralizes exact status formatting.
    print(status(201, "Created"))


if __name__ == "__main__":
    main()
