"""Kata 4 (after): catch only ValueError, and report what was skipped."""


def parse_all(raw_values: list[str]) -> list[int]:
    parsed: list[int] = []
    skipped: list[str] = []
    for raw in raw_values:
        try:
            parsed.append(int(raw))
        except ValueError:
            skipped.append(raw)
    if skipped:
        print(f"skipped invalid values: {skipped}")
    return parsed


print(parse_all(["1", "two", "3"]))
