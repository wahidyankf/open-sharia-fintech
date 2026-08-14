"""Example 15: read JSON safely."""

import json


def parse(body: bytes) -> dict[str, object]:
    # => Decode bytes at the JSON boundary before handlers consume values.
    return json.loads(body.decode("utf-8"))


def main() -> None:
    # => Valid bodies become ordinary typed Python data.
    print(parse(b'{"name":"Ada"}')["name"])


if __name__ == "__main__":
    main()
