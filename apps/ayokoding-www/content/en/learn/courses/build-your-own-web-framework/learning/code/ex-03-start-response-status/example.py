"""Example 3: format WSGI status."""


def main() -> None:
    # => WSGI status is one native string containing code and reason phrase.
    status = "200 OK"
    # => A fake callback exposes what a server receives.
    print(status)


if __name__ == "__main__":
    main()
