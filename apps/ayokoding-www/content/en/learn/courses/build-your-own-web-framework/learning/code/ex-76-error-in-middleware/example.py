"""Example 76: contain middleware error."""


def main() -> None:
    # => The outer boundary catches failures from inner middleware too.
    try:
        raise RuntimeError("inner")
    except RuntimeError:
        status = 500
    # => Client output remains a clean response.
    print(status)


if __name__ == "__main__":
    main()
