"""Example 34: ASGI server callable."""

import asyncio


async def application() -> str:
    # => Uvicorn drives an async application rather than owning framework logic.
    return "served"


def main() -> None:
    # => This local harness proves the callable runs without a server package.
    print(asyncio.run(application()))


if __name__ == "__main__":
    main()
