"""Example 75: wrap ASGI app."""


def main() -> None:
    # => ASGI middleware sees scope, receive, and send.
    parts = ("scope", "receive", "send")
    # => It wraps the event pump rather than one handler call.
    print(parts)


if __name__ == "__main__":
    main()
