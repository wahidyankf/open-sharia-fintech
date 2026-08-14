"""Example 2: inspect WSGI environ."""


def main() -> None:
    # => Servers place CGI-style request facts in this built-in dictionary.
    environ: dict[str, str] = {
        "REQUEST_METHOD": "GET",
        "PATH_INFO": "/items",
        "QUERY_STRING": "page=1",
    }
    # => A framework wrapper later centralizes these direct lookups.
    print(environ["REQUEST_METHOD"], environ["PATH_INFO"], environ["QUERY_STRING"])


if __name__ == "__main__":
    main()
