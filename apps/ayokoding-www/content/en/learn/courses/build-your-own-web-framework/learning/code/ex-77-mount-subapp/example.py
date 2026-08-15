"""Example 77: mount subapp."""


def main() -> None:
    # => Prefix routing delegates a subtree to another application.
    path = "/admin/users"
    child = path.removeprefix("/admin")
    # => The child receives its path-relative request.
    print(child)


if __name__ == "__main__":
    main()
