"""Example 70: select representation."""


def main() -> None:
    # => Accept drives representation selection.
    accept = "application/json"
    # => Content-Type follows the chosen body.
    print("json" if "json" in accept else "text")


if __name__ == "__main__":
    main()
