"""Example 52: map exception to 500."""


def main() -> None:
    # => The error boundary hides exception details from clients.
    try:
        raise ValueError("internal")
    except ValueError:
        status, body = 500, "internal server error"
    # => Logging could keep details while the response stays safe.
    print(status, body)


if __name__ == "__main__":
    main()
