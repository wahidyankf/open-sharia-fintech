"""Example 73: Depends-like injection."""


def main() -> None:
    # => A provider supplies a declared handler requirement.
    provider = lambda: "dependency"
    # => The handler remains framework-neutral.
    print(provider())


if __name__ == "__main__":
    main()
