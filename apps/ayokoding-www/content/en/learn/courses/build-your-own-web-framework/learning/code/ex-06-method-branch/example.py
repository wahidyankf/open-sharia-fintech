"""Example 6: dispatch by method."""


def response(method: str) -> str:
    # => Method selection is ordinary request-boundary control flow.
    return "created" if method == "POST" else "read"


def main() -> None:
    # => GET takes the safe read branch.
    print(response("GET"))


if __name__ == "__main__":
    main()
