"""Example 64: app.__main__ -- entry point for `python3 -m app`."""

from app.util import shout  # => cross-module import within the SAME package


def main() -> None:  # => defines the entry point run by `python3 -m app`
    print(shout("hello from a package"))  # => Output: HELLO FROM A PACKAGE!


if __name__ == "__main__":  # => True when run via `python3 -m app`
    main()  # => calls main(), which prints the shouted greeting
# => `python3 -m app` finds __main__.py automatically -- no need to name the file explicitly
