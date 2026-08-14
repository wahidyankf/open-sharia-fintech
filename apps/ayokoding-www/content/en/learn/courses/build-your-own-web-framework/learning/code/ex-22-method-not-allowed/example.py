"""Example 22: distinguish 405 from 404."""


def main() -> None:
    # => A known path with an unsupported method is a method mismatch.
    allowed = {"GET"}
    # => The router can return 405 without claiming the path is absent.
    print(405 if "POST" not in allowed else 200)


if __name__ == "__main__":
    main()
