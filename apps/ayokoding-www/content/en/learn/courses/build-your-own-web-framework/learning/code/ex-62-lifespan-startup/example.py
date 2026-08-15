"""Example 62: ASGI startup."""


def main() -> None:
    # => Startup creates shared resources before requests are accepted.
    state = {"ready": True}
    # => Completion makes readiness observable.
    print(state["ready"])


if __name__ == "__main__":
    main()
