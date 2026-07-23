"""Example 15: First Post-Mortem with python -m pdb."""

from __future__ import annotations


def parse_port(config: dict[str, str]) -> int:
    raw_port = config[
        "port"
    ]  # seeded bug: this config dict uses the key "PORT" (uppercase)
    return int(raw_port)


if __name__ == "__main__":
    settings = {"HOST": "localhost", "PORT": "8080"}
    print(parse_port(settings))
