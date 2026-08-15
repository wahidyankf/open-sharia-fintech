"""Example 4: WSGI header tuples."""


def main() -> None:
    # => WSGI response headers are a list of native-string name/value tuples.
    headers: list[tuple[str, str]] = [("Content-Type", "text/plain")]
    # => This exact shape is passed to start_response.
    print(headers[0])


if __name__ == "__main__":
    main()
