"""Example 41: extract multiple params."""


def main() -> None:
    # => Nested resource segments become separate named handler inputs.
    uid, pid = "u/p".split("/")
    # => Names preserve URL meaning better than positional indexing.
    print(uid, pid)


if __name__ == "__main__":
    main()
