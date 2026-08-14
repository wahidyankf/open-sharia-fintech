"""Example 31: assemble ASGI body chunks."""


def main() -> None:
    # => more_body keeps the receive loop alive until the final event.
    events: list[dict[str, object]] = [
        {"body": b"a", "more_body": True},
        {"body": b"b", "more_body": False},
    ]
    # => Concatenation preserves transport order.
    print(b"".join(event["body"] for event in events))


if __name__ == "__main__":
    main()
