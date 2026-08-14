"""Example 44: dispatch same path by method."""


def main() -> None:
    # => Method is included in the route key for one path.
    routes = {("GET", "/items"): "list", ("POST", "/items"): "create"}
    # => The selected handler follows the incoming method.
    print(routes[("POST", "/items")])


if __name__ == "__main__":
    main()
