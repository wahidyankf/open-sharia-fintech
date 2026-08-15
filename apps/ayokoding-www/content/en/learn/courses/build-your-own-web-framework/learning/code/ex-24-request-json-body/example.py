"""Example 24: JSON request helper."""

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    body: bytes

    def json(self) -> dict[str, object]:
        # => The helper owns decoding so handlers do not repeat it.
        return json.loads(self.body.decode("utf-8"))


def main() -> None:
    # => Parsed JSON is ordinary Python data at the handler boundary.
    print(Request(b'{"ok": true}').json()["ok"])


if __name__ == "__main__":
    main()
