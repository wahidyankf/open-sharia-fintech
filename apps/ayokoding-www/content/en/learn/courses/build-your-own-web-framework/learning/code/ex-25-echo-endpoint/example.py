"""Example 25: JSON echo endpoint."""

import json


def echo(body: bytes) -> bytes:
    # => Parse and encode through the same JSON codec for a round trip.
    return json.dumps(json.loads(body.decode("utf-8"))).encode("utf-8")


def main() -> None:
    # => The returned document preserves the request value.
    print(echo(b'{"name":"Ada"}').decode())


if __name__ == "__main__":
    main()
