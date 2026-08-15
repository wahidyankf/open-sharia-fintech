"""Example 55: safe 500 response."""


def main() -> None:
    # => Client output omits exception names and stack-trace implementation details.
    body = "internal server error"
    # => Diagnostics belong in logs instead.
    print("Traceback" not in body, body)


if __name__ == "__main__":
    main()
