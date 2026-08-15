"""Example 8: parse query strings."""

from urllib.parse import parse_qs


def main() -> None:
    # => parse_qs preserves repeated keys as lists.
    query = parse_qs("a=1&a=2")
    # => Repetition is request meaning, not a parsing accident.
    print(query["a"])


if __name__ == "__main__":
    main()
