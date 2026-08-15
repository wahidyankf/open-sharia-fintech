"""Example 27: build a redirect."""


def main() -> None:
    # => A redirect combines its status with required Location metadata.
    headers: list[tuple[str, str]] = [("Location", "/new-home")]
    # => Clients decide whether to follow the target.
    print(302, headers[0][1])


if __name__ == "__main__":
    main()
