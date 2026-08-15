"""Example 60: singleton dependency."""


def main() -> None:
    # => An app-scoped object is deliberately reused.
    singleton = object()
    # => Two resolutions return the same stable instance.
    print(singleton is singleton)


if __name__ == "__main__":
    main()
