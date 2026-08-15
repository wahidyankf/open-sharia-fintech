"""Example 42: static route precedence."""


def main() -> None:
    # => Exact paths are checked before parameterized patterns.
    static = {"/users/me": "me"}
    # => Specificity prevents the parameter route swallowing this endpoint.
    print(static["/users/me"])


if __name__ == "__main__":
    main()
