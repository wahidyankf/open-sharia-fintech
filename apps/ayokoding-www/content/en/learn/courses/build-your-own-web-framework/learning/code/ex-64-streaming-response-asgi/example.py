"""Example 64: ASGI stream chunks."""


def main() -> None:
    # => more_body keeps an ASGI response stream open.
    events = [{"body": b"a", "more_body": True}, {"body": b"b", "more_body": False}]
    # => The client receives the ordered chunks.
    print(b"".join(event["body"] for event in events))


if __name__ == "__main__":
    main()
