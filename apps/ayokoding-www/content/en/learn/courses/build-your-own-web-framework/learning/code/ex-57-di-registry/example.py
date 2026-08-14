"""Example 57: DI registry."""


def main() -> None:
    # => Providers make construction explicit instead of global.
    providers = {"service": lambda: "ready"}
    # => Resolution invokes the registered factory.
    print(providers["service"]())


if __name__ == "__main__":
    main()
