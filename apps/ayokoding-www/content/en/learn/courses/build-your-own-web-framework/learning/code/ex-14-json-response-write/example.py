"""Example 14: write JSON."""

import json


def main() -> None:
    # => JSON serialization produces text before the WSGI bytes boundary.
    body = json.dumps({"ok": True}).encode("utf-8")
    # => Content-Type tells clients which codec to use.
    print(body.decode(), "application/json")


if __name__ == "__main__":
    main()
