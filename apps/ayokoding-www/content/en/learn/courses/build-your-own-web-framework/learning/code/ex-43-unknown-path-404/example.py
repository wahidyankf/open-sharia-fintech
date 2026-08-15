"""Example 43: router fallback."""


def main() -> None:
    # => An unmatched route yields a response, not a framework crash.
    status = 404
    # => The fallback gives every miss the same contract.
    print(status)


if __name__ == "__main__":
    main()
