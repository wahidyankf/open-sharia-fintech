"""Example 7: read WSGI input."""

from io import BytesIO


def main() -> None:
    # => wsgi.input is a byte stream and CONTENT_LENGTH bounds the read.
    environ: dict[str, object] = {"wsgi.input": BytesIO(b"abc"), "CONTENT_LENGTH": "3"}
    # => Body parsing begins only after this framing read.
    body = environ["wsgi.input"].read(int(environ["CONTENT_LENGTH"]))  # type: ignore[union-attr]
    print(len(body))


if __name__ == "__main__":
    main()
