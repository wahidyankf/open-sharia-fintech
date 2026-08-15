"""Example 9: read WSGI headers."""


def main() -> None:
    # => Inbound HTTP headers are transformed into HTTP_* environ keys.
    environ: dict[str, str] = {"HTTP_ACCEPT": "application/json"}
    # => A request wrapper later restores case-insensitive lookup.
    print(environ["HTTP_ACCEPT"])


if __name__ == "__main__":
    main()
