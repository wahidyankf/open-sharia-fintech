"""Example 32: ASGI response event order."""


def main() -> None:
    # => A response starts before any body event is sent.
    events = ["http.response.start", "http.response.body"]
    # => Servers require this ordering.
    print(events)


if __name__ == "__main__":
    main()
