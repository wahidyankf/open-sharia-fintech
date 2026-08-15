"""Example 39: extract a path parameter."""


def main() -> None:
    # => The router captures a segment and names it for the handler.
    params = {"id": "/users/42".split("/")[-1]}
    # => Extraction happens before handler execution.
    print(params["id"])


if __name__ == "__main__":
    main()
