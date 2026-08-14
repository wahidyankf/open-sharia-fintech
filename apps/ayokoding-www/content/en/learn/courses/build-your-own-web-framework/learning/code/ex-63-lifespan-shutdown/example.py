"""Example 63: ASGI shutdown."""


def main() -> None:
    # => Shutdown owns cleanup of shared application resources.
    state = {"closed": False}
    state["closed"] = True
    # => Completion confirms teardown ran.
    print(state["closed"])


if __name__ == "__main__":
    main()
