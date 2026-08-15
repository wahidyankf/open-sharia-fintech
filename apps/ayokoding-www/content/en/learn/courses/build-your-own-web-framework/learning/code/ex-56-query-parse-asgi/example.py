"""Example 56: parse ASGI query bytes."""

from urllib.parse import parse_qs


def main() -> None:
    # => ASGI query_string is bytes and must be decoded before parsing.
    params = parse_qs(b"a=1&a=2".decode("ascii"))
    # => The standard parser preserves repeated parameter values.
    print(params["a"])


if __name__ == "__main__":
    main()
