"""Example 66: SSE frame."""


def main() -> None:
    # => SSE frames are text payloads sent through a streaming response.
    frame = b"data: update\n\n"
    # => text/event-stream tells clients to parse this framing.
    print(frame.decode().strip())


if __name__ == "__main__":
    main()
