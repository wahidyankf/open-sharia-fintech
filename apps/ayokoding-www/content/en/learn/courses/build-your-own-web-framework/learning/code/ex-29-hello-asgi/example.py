"""Example 29: minimal ASGI response."""

import asyncio


async def main() -> None:
    # => ASGI sends events asynchronously rather than returning body chunks.
    event: dict[str, object] = {"type": "http.response.body", "body": b"hello"}
    # => The body event terminates this small response.
    print(event["body"])


if __name__ == "__main__":
    asyncio.run(main())
