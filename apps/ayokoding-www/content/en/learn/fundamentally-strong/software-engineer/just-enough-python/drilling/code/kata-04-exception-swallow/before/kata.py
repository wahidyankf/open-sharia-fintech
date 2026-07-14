"""Kata 4 (before): a bare except silently swallows every error."""


def parse_all(raw_values: list[str]) -> list[int]:
    parsed: list[int] = []
    for raw in raw_values:
        try:
            parsed.append(int(raw))
        except Exception:
            pass
    return parsed


print(parse_all(["1", "two", "3"]))
