"""Example 74: wrap WSGI app."""


def main() -> None:
    # => WSGI middleware wraps the entire callable.
    wrapped = "middleware(app)"
    # => Every request passes through this wrapper.
    print(wrapped)


if __name__ == "__main__":
    main()
