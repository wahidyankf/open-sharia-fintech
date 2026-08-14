"""Example 68: lifecycle trace."""


def main() -> None:
    # => Every layer transforms the request once before response serialization.
    trace = ["environ", "router", "middleware", "handler", "response"]
    # => A trace makes the framework pipeline inspectable.
    print(trace)


if __name__ == "__main__":
    main()
